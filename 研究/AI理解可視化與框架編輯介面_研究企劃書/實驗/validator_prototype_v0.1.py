#!/usr/bin/env python3
"""ForAVAr semantic model validator prototype.

Experimental local tool; not production software.
Requires Python 3.10+ and jsonschema 4.x. No network or repository access.
"""
from __future__ import annotations
import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from importlib.metadata import version as package_version
from jsonschema import Draft202012Validator, FormatChecker


SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as stream:
        return json.load(stream)


def json_pointer(parts) -> str:
    escaped = [str(p).replace("~", "~0").replace("/", "~1") for p in parts]
    return "" if not escaped else "/" + "/".join(escaped)


class ModelValidator:
    def __init__(self, schema: dict, relations: dict, validation_rules: dict):
        self.schema = schema
        self.relations = relations
        self.validation_rules = validation_rules
        self.results = []
        self.warnings = []
        self.schema_validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def add(self, rule_id, severity, message, *, object_id="", path="", related_ids=None, action=""):
        item = {
            "rule_id": rule_id,
            "severity": severity,
            "object_id": object_id,
            "json_pointer": path,
            "message": message,
            "related_object_ids": sorted(set(related_ids or [])),
            "rule_profile_version": self.relations.get("contract_version", "unknown"),
            "action": action or ("block" if severity == "error" else "review"),
            "evidence_reference": ""
        }
        self.results.append(item)
        if severity == "warning":
            self.warnings.append(item)

    def check_schema(self):
        Draft202012Validator.check_schema(self.schema)

    def validate(self, model: dict):
        self.results, self.warnings = [], []
        if not isinstance(model, dict):
            self.add("VLD-001", "error", "Model root must be a JSON object", action="reject_input")
            return self.sorted_results()

        # L1: JSON Schema validation.
        schema_errors = sorted(
            self.schema_validator.iter_errors(model),
            key=lambda error: (json_pointer(error.absolute_path), error.validator or "")
        )
        for error in schema_errors:
            self.add("VLD-002", "error", error.message,
                     path=json_pointer(error.absolute_path), action="reject_input")

        schema_types = set(self.schema["$defs"]["edge"]["properties"]["relation_type"]["enum"])
        registry_types = set(self.relations.get("relations", {}))
        if schema_types != registry_types:
            self.add("VLD-003", "error", "Schema relation_type enum differs from registry keys",
                     path="/$defs/edge/properties/relation_type/enum",
                     action="block_publish_and_impact_analysis")
        if schema_errors:
            return self.sorted_results()

        if model.get("rule_profile") != self.relations.get("rule_profile"):
            self.add("VLD-204", "error", "Model rule_profile does not match loaded relation profile",
                     path="/rule_profile", action="block_publish_and_impact_analysis")
            return self.sorted_results()

        collections = {name: model.get(name, []) for name in ("nodes", "edges", "conditions", "sources")}
        objects = [(name, obj, idx) for name, group in collections.items()
                   for idx, obj in enumerate(group)]
        nodes = collections["nodes"]
        edges = collections["edges"]
        node_by_id = {node["id"]: node for node in nodes}
        sources = {source["id"] for source in collections["sources"]}
        conditions = {condition["id"] for condition in collections["conditions"]}

        # L2: global IDs and cross-object references.
        ids = defaultdict(list)
        for collection, obj, idx in objects:
            ids[obj["id"]].append(f"{collection}[{idx}]")
        for object_id, locations in ids.items():
            if len(locations) > 1:
                self.add("VLD-101", "error",
                         f"Duplicate global ID {object_id!r} at {locations}",
                         object_id=object_id, action="block_publish_and_report_all_collisions")

        for collection, obj, idx in objects:
            base = f"/{collection}/{idx}"
            for ref_idx, source_id in enumerate(obj.get("provenance_refs", [])):
                if source_id not in sources:
                    self.add("VLD-103", "error",
                             f"provenance_refs points to missing source {source_id!r}",
                             object_id=obj["id"], path=f"{base}/provenance_refs/{ref_idx}",
                             action="block_publish_and_report_missing_source")
            for ref_idx, condition_id in enumerate(obj.get("condition_refs", [])):
                if condition_id not in conditions:
                    self.add("VLD-104", "error",
                             f"condition_refs points to missing condition {condition_id!r}",
                             object_id=obj["id"], path=f"{base}/condition_refs/{ref_idx}",
                             action="block_publish_and_report_missing_condition")

        rules = self.relations.get("relations", {})
        semantic_keys = defaultdict(list)
        adjacency_all = defaultdict(list)

        for idx, edge in enumerate(edges):
            edge_id = edge["id"]
            source_id, target_id = edge["source_id"], edge["target_id"]
            relation_type = edge["relation_type"]
            base = f"/edges/{idx}"

            missing = [endpoint for endpoint in (source_id, target_id) if endpoint not in node_by_id]
            if missing:
                self.add("VLD-102", "error", f"Edge endpoint(s) do not resolve to nodes: {missing}",
                         object_id=edge_id, path=base, related_ids=[source_id, target_id],
                         action="block_publish_and_report_edge")
                continue
            if source_id == target_id:
                self.add("VLD-105", "error", "Self-loop is forbidden in profile v1",
                         object_id=edge_id, path=base, related_ids=[source_id],
                         action="block_publish_and_report_edge")

            rule = rules.get(relation_type)
            if not rule:
                self.add("VLD-204", "error", f"No rule for relation_type {relation_type!r}",
                         object_id=edge_id, path=f"{base}/relation_type",
                         action="block_impact_analysis_and_publish")
                continue

            endpoints = (source_id, target_id)
            if rule.get("symmetric") is True or rule.get("directed") is False:
                endpoints = tuple(sorted(endpoints))
            conditions_key = tuple(sorted(set(edge.get("condition_refs", []))))
            semantic_keys[(relation_type, endpoints, conditions_key)].append(edge_id)
            adjacency_all[source_id].append((target_id, edge))

            if relation_type in {"is_evidence_for", "refutes"}:
                source_node, target_node = node_by_id[source_id], node_by_id[target_id]
                target_is_claim = (
                    target_node.get("entity_kind") == "claim" or bool(target_node.get("claim_kind"))
                )
                if not source_node.get("provenance_refs") or not target_is_claim:
                    self.add("VLD-206", "error",
                             "Evidence/rebuttal edge requires a source-backed proposition and claim-bearing target; target evidence_status is never auto-mutated",
                             object_id=edge_id, path=base, related_ids=[source_id, target_id],
                             action="block_publish_and_report_edge_and_endpoint_ids")

        for key, edge_ids in semantic_keys.items():
            if len(edge_ids) > 1:
                self.add("VLD-106", "error", f"Duplicate semantic edge key {key!r}",
                         object_id=edge_ids[0], related_ids=edge_ids,
                         action="block_publish_and_report_duplicate_edges")

        # L3: enumerate simple directed cycles. The cap prevents a pathological dense
        # graph from exploding this planning prototype; hitting the cap is itself a warning.
        node_ids = sorted(node_by_id)
        node_order = {node_id: i for i, node_id in enumerate(node_ids)}
        cycle_cap = 1000

        def enumerate_cycles(adjacency):
            cycles, visited_count = {}, 0
            for start in node_ids:
                start_order = node_order[start]
                in_path = {start}
                path_edges = []

                def walk(current):
                    nonlocal visited_count
                    if visited_count >= cycle_cap:
                        return
                    for next_node, edge in sorted(adjacency.get(current, []),
                                                  key=lambda pair: (pair[0], pair[1]["id"])):
                        if next_node == start:
                            cycle = path_edges + [edge]
                            cycles[tuple(item["id"] for item in cycle)] = cycle
                            visited_count += 1
                        elif next_node not in in_path and node_order.get(next_node, -1) > start_order:
                            in_path.add(next_node)
                            path_edges.append(edge)
                            walk(next_node)
                            path_edges.pop()
                            in_path.remove(next_node)
                walk(start)
            return list(cycles.values()), visited_count >= cycle_cap

        cycles, truncated = enumerate_cycles(adjacency_all)
        if truncated:
            self.add("VLD-203", "warning",
                     f"Cycle enumeration reached prototype cap {cycle_cap}; review is incomplete, so absence of other cycles cannot be inferred",
                     action="manual_graph_review_required")

        for cycle in cycles:
            relation_types = {edge["relation_type"] for edge in cycle}
            edge_ids = [edge["id"] for edge in cycle]
            node_path = [cycle[0]["source_id"]] + [edge["target_id"] for edge in cycle]

            if len(relation_types) == 1:
                relation_type = next(iter(relation_types))
                policy = rules[relation_type].get("cycle_policy", "unknown")
                if policy == "forbidden":
                    self.add("VLD-201", "error",
                             f"Forbidden {relation_type!r} cycle: {' -> '.join(node_path)}",
                             object_id=edge_ids[0], related_ids=edge_ids + node_path,
                             action="block_publish_and_report_cycle_path")
                elif policy == "warn":
                    warning_id = f"VLD-202|{relation_type}|{','.join(sorted(edge_ids))}"
                    self.add("VLD-202", "warning",
                             f"Cycle warning {warning_id}; path: {' -> '.join(node_path)}",
                             object_id=edge_ids[0], related_ids=edge_ids + node_path,
                             action="draft_warning_publish_requires_acknowledgement")
            else:
                warning_id = f"VLD-203|{','.join(sorted(relation_types))}|{','.join(sorted(edge_ids))}"
                self.add("VLD-203", "warning",
                         f"Mixed-relation cycle warning {warning_id}; path: {' -> '.join(node_path)}",
                         object_id=edge_ids[0], related_ids=edge_ids + node_path,
                         action="warn_and_require_release_acknowledgement")

        return self.sorted_results()

    def validate_release(self, model: dict, release: dict | None):
        self.validate(model)
        if release is None:
            self.add("VLD-405", "error", "Publish attempt requires a separate release-record JSON",
                     action="block_publish")
            return self.sorted_results()

        required = self.validation_rules.get("release_record", {}).get("required_fields", [])
        for field in required:
            if field not in release or release[field] in (None, ""):
                self.add("VLD-405", "error", f"Release record lacks required field {field!r}",
                         path=f"/{field}", action="block_publish")

        schema_version = self.schema["properties"]["schema_version"]["const"]
        if release.get("schema_version") != schema_version:
            self.add("VLD-405", "error", "Release schema_version does not match loaded schema",
                     path="/schema_version", action="block_publish")
        if release.get("rule_profile") != model.get("rule_profile"):
            self.add("VLD-405", "error", "Release rule_profile does not match model",
                     path="/rule_profile", action="block_publish")
        if release.get("rule_profile_version") != self.relations.get("contract_version"):
            self.add("VLD-405", "error", "Release rule_profile_version does not match registry",
                     path="/rule_profile_version", action="block_publish")
        try:
            datetime.fromisoformat(str(release.get("published_at", "")).replace("Z", "+00:00"))
        except ValueError:
            self.add("VLD-405", "error", "published_at must be an ISO-8601 date-time",
                     path="/published_at", action="block_publish")

        if model.get("model_state") not in {"proposed", "published"}:
            self.add("VLD-401", "error", "Publish requires model_state=proposed",
                     path="/model_state", action="block_publish")
        for collection in ("nodes", "edges", "conditions"):
            for idx, obj in enumerate(model.get(collection, [])):
                if obj.get("review_status") != "accepted":
                    self.add("VLD-401", "error",
                             f"Publication requires accepted status, found {obj.get('review_status')!r}",
                             object_id=obj["id"], path=f"/{collection}/{idx}/review_status",
                             action="block_publish_and_report_object_ids")

        for idx, node in enumerate(model.get("nodes", [])):
            if node.get("structural_role") in {"core", "main_axis", "skeleton"} and not node.get("provenance_refs"):
                self.add("VLD-403", "error", "Core structural nodes require provenance",
                         object_id=node["id"], path=f"/nodes/{idx}/provenance_refs",
                         action="block_publish_and_report_node")
            if (node.get("structural_role") in {"core", "main_axis", "skeleton"}
                    and node.get("claim_kind") == "external_fact_claim"
                    and node.get("evidence_status") != "supported"):
                self.add("VLD-403", "error", "Critical external fact claim must be supported",
                         object_id=node["id"], path=f"/nodes/{idx}/evidence_status",
                         action="block_publish_and_report_node")

        ack_ids = set(release.get("acknowledged_warning_ids", []))
        release_warning_ids = {
            item.get("warning_id") for item in release.get("warnings", [])
            if isinstance(item, dict)
        }
        import re
        for warning in list(self.warnings):
            if warning["rule_id"] not in {"VLD-202", "VLD-203"}:
                continue
            match = re.search(r"warning (VLD-20[23][^;]+)", warning["message"])
            warning_id = match.group(1) if match else warning["rule_id"]
            if warning_id not in release_warning_ids:
                self.add("VLD-406", "error", f"Release record must preserve warning path {warning_id!r}",
                         object_id=warning["object_id"], related_ids=warning["related_object_ids"],
                         action="block_publish")
            if warning_id not in ack_ids:
                self.add("VLD-406", "error", f"Warning {warning_id!r} lacks explicit human acknowledgement",
                         object_id=warning["object_id"], related_ids=warning["related_object_ids"],
                         action="block_publish")
        return self.sorted_results()

    def sorted_results(self):
        def phase(item):
            if item["rule_id"] in {"VLD-001", "VLD-002", "VLD-003"}:
                return 0 if item["rule_id"] == "VLD-001" else 1
            return int(item["rule_id"].split("-")[1]) // 100 + 1
        return sorted(self.results, key=lambda item: (
            phase(item), SEVERITY_ORDER.get(item["severity"], 9),
            item["json_pointer"], item["rule_id"], item["object_id"], item["message"]
        ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, help="Path to pinned JSON Schema")
    parser.add_argument("--relations", required=True, help="Path to relation registry")
    parser.add_argument("--rules", required=True, help="Path to cross-object rules registry")
    parser.add_argument("--model", help="Path to model JSON")
    parser.add_argument("--release-record", help="Path to separate release-record JSON")
    parser.add_argument("--check-schema", action="store_true", help="Only run Draft 2020-12 meta-validation")
    parser.add_argument("--for-publish", action="store_true", help="Apply release gates; requires --release-record")
    args = parser.parse_args()

    try:
        schema, relations, rules = load_json(args.schema), load_json(args.relations), load_json(args.rules)
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        print(json.dumps({"status": "FAIL", "stage": "L0/L1", "error": str(error)},
                         ensure_ascii=False, indent=2))
        return 2 if isinstance(error, (OSError, json.JSONDecodeError)) else 1

    if args.check_schema:
        print(json.dumps({"status": "PASS", "stage": "L1_SCHEMA_META",
                          "jsonschema_version": package_version("jsonschema")},
                         ensure_ascii=False, indent=2))
        return 0
    if not args.model:
        parser.error("--model is required unless --check-schema is specified")

    try:
        model = load_json(args.model)
        release = load_json(args.release_record) if args.release_record else None
    except (OSError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL", "stage": "L0", "error": str(error)},
                         ensure_ascii=False, indent=2))
        return 2

    engine = ModelValidator(schema, relations, rules)
    results = engine.validate_release(model, release) if args.for_publish else engine.validate(model)
    error_count = sum(item["severity"] == "error" for item in results)
    warning_count = sum(item["severity"] == "warning" for item in results)
    report = {
        "status": "FAIL" if error_count else ("PASS_WITH_WARNINGS" if warning_count else "PASS"),
        "validator": "forAVAr-cross-object-prototype-v0.1",
        "schema_version": schema["properties"]["schema_version"]["const"],
        "rule_profile": relations.get("rule_profile"),
        "rule_profile_version": relations.get("contract_version"),
        "error_count": error_count,
        "warning_count": warning_count,
        "results": results
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
