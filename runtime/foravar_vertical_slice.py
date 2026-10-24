"""Minimal forAVAr thinking-loop integration seam.

This module orchestrates caller-supplied cognitive/tool adapters. It does not
implement a language model, permissions engine, task registry, persistence layer,
retry loop, or GitHub operations. Authorization remains an explicit adapter gate.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

try:
    from .policy_gate import evaluate_authorization
except ImportError:  # supports direct imports when runtime/ is on sys.path
    from policy_gate import evaluate_authorization

IMPLEMENTATION_VERSION = "0.2.0"
IMPLEMENTATION_STATUS = "POLICY_GATE_INTEGRATED_RUNTIME_NOT_VALIDATED"

EVIDENCE_KINDS = {
    "SOURCE_OBSERVATION",
    "STATIC_CHECK",
    "RETROSPECTIVE_REPLAY",
    "PROGRAM_TEST",
    "RUNTIME_OBSERVATION",
    "EXECUTION_OBSERVATION",
}
CRITERION_STATES = {"PASS", "FAIL", "UNKNOWN", "NOT_RUN"}
EXECUTION_STATES = {"EXECUTED", "PARTIAL", "BLOCKED", "FAILED", "NOT_RUN"}
RISK_LEVELS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
FAILURE_CLASSES = {
    "NONE",
    "LOCAL_FAILURE",
    "METHOD_FAILURE",
    "MODEL_FAILURE",
    "FRAME_FAILURE",
    "AUTHORIZATION_FAILURE",
    "EVIDENCE_GAP",
    "NO_FEASIBLE_SOLUTION",
}


class ContractError(ValueError):
    """Raised when an adapter violates the vertical-slice contract."""


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty string")
    return value.strip()


def _record(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{field} must be an object")
    return dict(value)


def _validate_task(task: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    _text(task.get("task_id"), "task.task_id")
    _text(task.get("goal"), "task.goal")
    raw_criteria = task.get("acceptance_criteria")
    if not isinstance(raw_criteria, list) or not raw_criteria:
        raise ContractError("task.acceptance_criteria must be a non-empty list")
    criteria: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_criteria):
        item = _record(raw, f"task.acceptance_criteria[{index}]")
        criterion_id = _text(item.get("id"), f"acceptance_criteria[{index}].id")
        _text(item.get("description"), f"acceptance_criteria[{index}].description")
        if criterion_id in seen:
            raise ContractError(f"duplicate acceptance criterion: {criterion_id}")
        seen.add(criterion_id)
        required_kinds = item.get("required_evidence_kinds", [])
        if not isinstance(required_kinds, list) or any(kind not in EVIDENCE_KINDS for kind in required_kinds):
            raise ContractError(f"invalid evidence kind requirement for {criterion_id}")
        criteria.append({**item, "id": criterion_id, "required_evidence_kinds": required_kinds})

    profile = task.get("profile", {})
    if not isinstance(profile, Mapping):
        raise ContractError("task.profile must be an object")
    profile = dict(profile)
    risk = profile.get("risk_level")
    if risk is not None and risk not in RISK_LEVELS:
        raise ContractError(f"invalid task.profile.risk_level: {risk}")
    for key in ("requires_external_evidence", "requires_diagnostic", "has_source_conflict", "has_critical_unknowns", "side_effects"):
        if key in profile and not isinstance(profile[key], bool):
            raise ContractError(f"task.profile.{key} must be boolean")
    return criteria, profile


def _simple_fast_path(profile: Mapping[str, Any]) -> bool:
    """Short-circuit only when every condition is explicit and low-risk."""
    return (
        profile.get("risk_level") == "LOW"
        and profile.get("requires_external_evidence") is False
        and profile.get("requires_diagnostic") is False
        and profile.get("has_source_conflict") is False
        and profile.get("has_critical_unknowns") is False
        and profile.get("side_effects") is False
    )


def _call(adapters: Mapping[str, Callable[..., Any]], name: str, *args: Any) -> dict[str, Any]:
    fn = adapters.get(name)
    if not callable(fn):
        raise ContractError(f"missing callable adapter: {name}")
    return _record(fn(*args), f"adapter.{name} result")


def _bind_task(value: Mapping[str, Any], task_id: str, field: str) -> None:
    if value.get("task_id") != task_id:
        raise ContractError(f"{field}.task_id does not match the active task")


def _early(status: str, task_id: str, trace: list[str], reason: str, **extra: Any) -> dict[str, Any]:
    action = {
        "BLOCKED": "STOP_BLOCKED",
        "NOT_PROVEN": "PRESERVE_UNKNOWN_AND_IDENTIFY_MISSING_EVIDENCE",
        "FAILED": "CLASSIFY_FAILURE_BEFORE_RETRY",
        "REJECTED": "REJECT_WITH_REASON",
    }.get(status, "STOP_AND_PRESERVE_STATE")
    return {
        "task_id": task_id,
        "implementation_version": IMPLEMENTATION_VERSION,
        "implementation_status": IMPLEMENTATION_STATUS,
        "status": status,
        "trace": list(trace),
        "feedback": {"action": action, "reason": reason},
        **extra,
    }


def _validate_evidence(records: Any, field: str) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        raise ContractError(f"{field} must be a list")
    index: dict[str, dict[str, Any]] = {}
    for n, raw in enumerate(records):
        record = _record(raw, f"{field}[{n}]")
        evidence_id = _text(record.get("evidence_id"), f"{field}[{n}].evidence_id")
        if evidence_id in index:
            raise ContractError(f"duplicate evidence_id: {evidence_id}")
        kind = record.get("kind")
        if kind not in EVIDENCE_KINDS:
            raise ContractError(f"invalid evidence kind for {evidence_id}: {kind}")
        # Declared or linked material is not evidence unless an observation is recorded.
        required = ("target_revision", "observed_at", "summary")
        if record.get("status") == "OBSERVED" and all(isinstance(record.get(k), str) and record[k].strip() for k in required):
            if kind in {"PROGRAM_TEST", "RUNTIME_OBSERVATION"}:
                if not isinstance(record.get("run_id"), str) or not record["run_id"].strip():
                    raise ContractError(f"{kind} evidence {evidence_id} requires run_id")
                if not isinstance(record.get("command"), str) or not record["command"].strip():
                    raise ContractError(f"{kind} evidence {evidence_id} requires command")
                if not isinstance(record.get("exit_code"), int):
                    raise ContractError(f"{kind} evidence {evidence_id} requires integer exit_code")
            if kind == "RUNTIME_OBSERVATION":
                for key in ("environment", "output_digest"):
                    if not isinstance(record.get(key), str) or not record[key].strip():
                        raise ContractError(f"RUNTIME_OBSERVATION evidence {evidence_id} requires {key}")
        index[evidence_id] = record
    return index


def _feedback(status: str, failure_class: str, reason: str = "") -> dict[str, str]:
    actions = {
        "ACCEPTED": "CLOSE",
        "PARTIAL": "PARTIAL_CLOSEOUT_WITH_OPEN_ITEMS",
        "BLOCKED": "STOP_BLOCKED",
        "NOT_PROVEN": "PRESERVE_UNKNOWN_AND_IDENTIFY_MISSING_EVIDENCE",
        "FAILED": {
            "LOCAL_FAILURE": "REPAIR_LOCAL_NODE_AND_REGRESS",
            "METHOD_FAILURE": "REROUTE_METHOD",
            "MODEL_FAILURE": "REVISE_PROBLEM_MODEL",
            "FRAME_FAILURE": "REFRAME_PROBLEM",
            "AUTHORIZATION_FAILURE": "STOP_AND_REQUEST_AUTHORIZATION",
            "EVIDENCE_GAP": "GATHER_DISCRIMINATING_EVIDENCE",
            "NO_FEASIBLE_SOLUTION": "REJECT_WITH_REASON",
            "NONE": "CLASSIFY_FAILURE_BEFORE_RETRY",
        }[failure_class],
    }
    action = actions[status]
    return {"action": action, "reason": reason or failure_class}


def run_vertical_slice(task: Mapping[str, Any], adapters: Mapping[str, Callable[..., Any]]) -> dict[str, Any]:
    """Run one conditional thinking loop; return a traceable, non-persistent receipt.

    Required adapters: frame(task), evidence(task, frame), route(task, frame, evidence),
    execute(task, frame, evidence, route), evaluate(task, execution, evidence).
    A low-risk direct task may bypass evidence gathering only when all short-circuit
    profile fields are explicitly false/LOW. A selected route never grants permission.
    """
    task_obj = _record(task, "task")
    criteria, profile = _validate_task(task_obj)
    task_id = task_obj["task_id"]
    trace: list[str] = []

    frame = _call(adapters, "frame", task_obj)
    trace.append("FRAME")
    _bind_task(frame, task_id, "frame")
    frame_status = frame.get("status")
    if frame_status != "READY":
        status = "BLOCKED" if frame_status == "BLOCKED" else "NOT_PROVEN"
        return _early(status, task_id, trace, str(frame.get("reason", "problem framing is incomplete")), frame=frame)
    _text(frame.get("frame_id"), "frame.frame_id")
    _text(frame.get("problem_statement"), "frame.problem_statement")
    for key in ("in_scope", "out_of_scope", "unknowns"):
        if not isinstance(frame.get(key), list):
            raise ContractError(f"frame.{key} must be a list")

    if _simple_fast_path(profile):
        evidence = {"task_id": task_id, "status": "NOT_REQUIRED", "records": [], "critical_unknowns": [], "reason": "explicit low-risk short path"}
        trace.append("EVIDENCE_SHORT_CIRCUIT")
    else:
        evidence = _call(adapters, "evidence", task_obj, frame)
        trace.append("EVIDENCE")
        _bind_task(evidence, task_id, "evidence")
        if evidence.get("status") not in {"READY", "PARTIAL", "CONFLICT", "BLOCKED"}:
            raise ContractError("adapter.evidence status must be READY, PARTIAL, CONFLICT, or BLOCKED")
        _validate_evidence(evidence.get("records", []), "evidence.records")
        if evidence.get("status") == "BLOCKED":
            return _early("BLOCKED", task_id, trace, str(evidence.get("reason", "evidence collection is blocked")), frame=frame, evidence=evidence)
        critical_unknowns = evidence.get("critical_unknowns", [])
        if not isinstance(critical_unknowns, list):
            raise ContractError("evidence.critical_unknowns must be a list")
        if critical_unknowns and (profile.get("risk_level") in {"HIGH", "CRITICAL"} or profile.get("side_effects") is True):
            return _early("BLOCKED", task_id, trace, "critical unknown affects a high-risk or side-effecting task", frame=frame, evidence=evidence)

    route = _call(adapters, "route", task_obj, frame, evidence)
    trace.append("ROUTE")
    _bind_task(route, task_id, "route")
    if route.get("status") in {"BLOCKED", "NOT_PROVEN", "REJECTED"}:
        status = route["status"]
        return _early(status, task_id, trace, str(route.get("reason", "route did not authorize execution")), frame=frame, evidence=evidence, route=route)
    if route.get("status") != "ROUTED":
        raise ContractError("adapter.route status must be ROUTED or a supported terminal status")
    candidates = route.get("candidate_methods")
    if not isinstance(candidates, list) or not candidates or any(not isinstance(x, str) or not x.strip() for x in candidates):
        raise ContractError("route.candidate_methods must be a non-empty list of method IDs")
    if len(set(candidates)) != len(candidates):
        raise ContractError("route.candidate_methods must not contain duplicates")
    selected = _text(route.get("selected_method"), "route.selected_method")
    if selected not in candidates:
        raise ContractError("route.selected_method must be one of candidate_methods")
    _text(route.get("reason"), "route.reason")
    _text(route.get("stop_rule"), "route.stop_rule")
    if not isinstance(route.get("requires_authorization"), bool):
        raise ContractError("route.requires_authorization must be boolean")
    required_scope = route.get("required_scope", [])
    if not isinstance(required_scope, list) or any(
        not isinstance(scope, str) or not scope.strip() for scope in required_scope
    ):
        raise ContractError("route.required_scope must be a list of non-empty scope strings")
    route["required_scope"] = required_scope

    authorization = evaluate_authorization(task_obj, profile, route, adapters)
    trace.append("POLICY_GATE")
    if authorization.get("required"):
        trace.append("AUTHORIZATION")
        if authorization.get("status") != "AUTHORIZED":
            return _early(
                "BLOCKED",
                task_id,
                trace,
                str(authorization.get("reason", "authorization was not granted")),
                frame=frame,
                evidence=evidence,
                route=route,
                authorization=authorization,
            )
    else:
        trace.append("AUTHORIZATION_NOT_REQUIRED")

    execution = _call(adapters, "execute", task_obj, frame, evidence, route)
    trace.append("EXECUTION")
    _bind_task(execution, task_id, "execution")
    execution_status = execution.get("status")
    if execution_status not in EXECUTION_STATES:
        raise ContractError(f"invalid execution.status: {execution_status}")
    if execution_status in {"BLOCKED", "FAILED", "NOT_RUN"}:
        status = "BLOCKED" if execution_status == "BLOCKED" else ("FAILED" if execution_status == "FAILED" else "NOT_PROVEN")
        return _early(status, task_id, trace, str(execution.get("reason", f"execution status: {execution_status}")), frame=frame, evidence=evidence, route=route, execution=execution)
    _text(execution.get("execution_id"), "execution.execution_id")
    _text(execution.get("result_summary"), "execution.result_summary")

    evaluation = _call(adapters, "evaluate", task_obj, execution, evidence)
    trace.append("EVALUATION")
    _bind_task(evaluation, task_id, "evaluation")
    raw_results = evaluation.get("criteria_results")
    if not isinstance(raw_results, list):
        raise ContractError("evaluation.criteria_results must be a list")
    results: dict[str, dict[str, Any]] = {}
    required_ids = {c["id"] for c in criteria}
    for i, raw in enumerate(raw_results):
        result = _record(raw, f"evaluation.criteria_results[{i}]")
        criterion_id = _text(result.get("criterion_id"), f"criteria_results[{i}].criterion_id")
        if criterion_id not in required_ids:
            raise ContractError(f"evaluation returned unknown criterion: {criterion_id}")
        if criterion_id in results:
            raise ContractError(f"duplicate evaluation result for criterion: {criterion_id}")
        if result.get("status") not in CRITERION_STATES:
            raise ContractError(f"invalid status for criterion {criterion_id}")
        results[criterion_id] = result

    all_records = list(evidence.get("records", [])) + list(execution.get("evidence_records", []))
    evidence_index = _validate_evidence(all_records, "evidence_records")
    normalized: list[dict[str, Any]] = []
    for criterion in criteria:
        criterion_id = criterion["id"]
        result = dict(results.get(criterion_id, {"criterion_id": criterion_id, "status": "NOT_RUN", "evidence_ids": []}))
        evidence_ids = result.get("evidence_ids", [])
        if not isinstance(evidence_ids, list) or any(not isinstance(x, str) for x in evidence_ids):
            raise ContractError(f"evidence_ids must be a list of strings for {criterion_id}")
        cited = [evidence_index.get(x) for x in evidence_ids]
        traceable = bool(cited) and all(item is not None and item.get("status") == "OBSERVED" for item in cited)
        required_kinds = set(criterion["required_evidence_kinds"])
        available_kinds = {item.get("kind") for item in cited if item is not None and item.get("status") == "OBSERVED"}
        if result["status"] in {"PASS", "FAIL"} and (not traceable or not required_kinds.issubset(available_kinds)):
            result["status"] = "UNKNOWN"
            result["reason"] = "evaluation claim lacks linked observed evidence of the required kind"
        result["evidence_ids"] = evidence_ids
        normalized.append(result)

    if any(r["status"] == "FAIL" for r in normalized):
        status = "FAILED"
    elif any(r["status"] in {"UNKNOWN", "NOT_RUN"} for r in normalized):
        status = "NOT_PROVEN"
    elif execution_status == "PARTIAL":
        status = "PARTIAL"
    else:
        status = "ACCEPTED"
    failure_class = evaluation.get("failure_class", "NONE")
    if failure_class not in FAILURE_CLASSES:
        raise ContractError(f"invalid evaluation.failure_class: {failure_class}")
    reason = str(evaluation.get("reason", ""))
    feedback = _feedback(status, failure_class, reason)
    trace.append("FEEDBACK")
    return {
        "task_id": task_id,
        "implementation_version": IMPLEMENTATION_VERSION,
        "implementation_status": IMPLEMENTATION_STATUS,
        "status": status,
        "trace": trace,
        "frame": frame,
        "evidence": evidence,
        "route": route,
        "authorization": authorization,
        "execution": execution,
        "acceptance": {"criteria_results": normalized, "failure_class": failure_class, "reason": reason},
        "feedback": feedback,
        "runtime_observation_present": any(
            item.get("kind") == "RUNTIME_OBSERVATION" and item.get("status") == "OBSERVED"
            and all(isinstance(item.get(k), str) and item[k].strip() for k in ("run_id", "command", "target_revision", "observed_at", "environment", "output_digest"))
            and isinstance(item.get("exit_code"), int)
            for item in evidence_index.values()
        ),
    }
