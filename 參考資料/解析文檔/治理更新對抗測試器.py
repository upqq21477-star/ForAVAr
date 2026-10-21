#!/usr/bin/env python3
"""Fault-injection tests for governance rules; outcomes depend on declared assumptions."""
import json, random

def residual_failures(n, rollback_success, seed):
    r=random.Random(seed)
    return sum(r.random() >= rollback_success for _ in range(n))

def main():
    n=1000
    r=random.Random(20261021)
    # A resolvable URL is not proof that its contents support a claim.
    v3_false_accepts=sum(r.random()<.90 for _ in range(n))
    r=random.Random(99)
    common_mode=0
    for _ in range(n):
        if r.random()<.005:
            common_mode+=1             # shared premise defeats both checkers
        elif r.random()<.001 and r.random()<.001:
            common_mode+=1             # two nominally independent misses
    result={
      "notice":"Synthetic fault injection, not measured model accuracy or live runtime tests.",
      "fake_citations_1000":{
        "source_exists_only_assumed_false_accepts_V3":v3_false_accepts,
        "dual_checker_independence_assumption_false_accepts_V5":0,
        "after_0.5pct_common_mode_failure_injection":common_mode},
      "unapproved_control_plane_changes_1000":{
        "unprotected_design_accepts_by_definition":1000,
        "protected_design_without_explicit_authorization":0},
      "same_source_repeated_1000":{
        "occurrence_count_threshold_3_false_promotions":n//3,
        "provenance_cluster_without_independent_evidence":0},
      "forced_transaction_failures_1000":{
        "rollback_success_99.5pct_residual":residual_failures(n,.995,310),
        "rollback_success_99.99pct_residual":residual_failures(n,.9999,511)},
      "design_implication":[
        "Two checks are not independent when they share the same model, source, assumptions, or grader.",
        "Repeated observations from one origin count as one evidence cluster, not independent corroboration.",
        "Policy/evaluation/permission files form a protected control plane; updates require explicit authorization and regression checks.",
        "When evidence conflicts or a source does not support a claim, retain a candidate/quarantine record rather than promoting it."
      ]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
