"""Fail-closed authorization gate for the forAVAr runtime seam.

This module does not grant permissions itself. It requires a trusted authorization
adapter to return a task-bound, scope-bound receipt before protected execution.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


PROTECTED_RISK_LEVELS = {"HIGH", "CRITICAL"}
KNOWN_NONPROTECTED_RISK_LEVELS = {"LOW", "MEDIUM"}


def authorization_required(profile: Mapping[str, Any], route: Mapping[str, Any]) -> bool:
    """Return True unless the route is explicitly low enough to bypass approval.

    A gate is mandatory when the route requests authorization, side effects are
    possible, or risk is high/critical/unknown. Missing side-effect metadata is
    treated as unknown rather than as a declaration of read-only behavior.
    """
    risk = profile.get("risk_level")
    side_effects = profile.get("side_effects")
    return (
        route.get("requires_authorization") is True
        or side_effects is not False
        or risk not in KNOWN_NONPROTECTED_RISK_LEVELS
        or risk in PROTECTED_RISK_LEVELS
    )


def evaluate_authorization(
    task: Mapping[str, Any],
    profile: Mapping[str, Any],
    route: Mapping[str, Any],
    adapters: Mapping[str, Callable[..., Any]],
) -> dict[str, Any]:
    """Evaluate the authorization boundary and return a traceable decision.

    Required adapter contract:
      authorize(task, route) -> mapping containing
      task_id, status='AUTHORIZED', authorization_id, authorized_scope.

    route.required_scope must list every permission required by the proposed
    action. Missing scope, a missing adapter, an exception, a mismatched task,
    or a partial scope grant fails closed and prevents execution.
    """
    task_id = task.get("task_id")
    required = authorization_required(profile, route)
    route_scope = route.get("required_scope", [])

    if not isinstance(route_scope, list) or any(
        not isinstance(scope, str) or not scope.strip() for scope in route_scope
    ):
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "route.required_scope must be a list of non-empty scope strings",
        }

    if not required:
        return {
            "task_id": task_id,
            "required": False,
            "status": "NOT_REQUIRED",
            "reason": "explicit low/medium risk and explicit no-side-effect profile; route did not require authorization",
        }

    if not route_scope:
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "protected execution has no explicit route.required_scope",
        }

    authorize = adapters.get("authorize")
    if not callable(authorize):
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "authorization adapter unavailable; protected execution blocked by default",
        }

    try:
        raw_grant = authorize(task, route)
    except Exception as exc:
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": f"authorization adapter failed ({type(exc).__name__}); protected execution blocked",
        }

    if not isinstance(raw_grant, Mapping):
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "authorization adapter did not return an object",
        }

    grant = dict(raw_grant)
    if grant.get("task_id") != task_id:
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "authorization receipt task_id does not match the active task",
            "authorization_receipt": grant,
        }

    if grant.get("status") != "AUTHORIZED":
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": str(grant.get("reason") or "authorization was not explicitly granted"),
            "authorization_receipt": grant,
        }

    authorization_id = grant.get("authorization_id")
    if not isinstance(authorization_id, str) or not authorization_id.strip():
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "authorization receipt is missing authorization_id",
            "authorization_receipt": grant,
        }

    granted_scope = grant.get("authorized_scope")
    if not isinstance(granted_scope, list) or any(
        not isinstance(scope, str) or not scope.strip() for scope in granted_scope
    ):
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "authorization receipt is missing a valid authorized_scope list",
            "authorization_receipt": grant,
        }

    missing_scope = sorted(set(route_scope) - set(granted_scope))
    if missing_scope:
        return {
            "task_id": task_id,
            "required": True,
            "status": "BLOCKED",
            "reason": "authorization receipt does not cover all required scopes",
            "missing_scope": missing_scope,
            "authorization_receipt": grant,
        }

    return {
        "task_id": task_id,
        "required": True,
        "status": "AUTHORIZED",
        "reason": "task-bound authorization receipt covers the declared route scope",
        "authorization_id": authorization_id.strip(),
        "authorized_scope": sorted(set(granted_scope)),
        "authorization_receipt": grant,
    }
