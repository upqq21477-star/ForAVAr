# P1／P2 功能骨架樹分支｜Current 與控制模組歸位

- 文件 ID：FORAVAR-FUNCTION-TREE-CURRENT-001
- 類型：BRANCH
- 狀態：CURRENT／forAVAr 內的唯讀參考映射
- 唯一責任：保存功能定位／能力登錄／Current 控制／責任邊界所指定內容。
- 主軸回鏈：[P1／P2 功能骨架樹主軸](./P1-P2-功能骨架樹-全面重整版.md)
- 使用邊界：P1、P2 repository 唯讀；本映射不等於功能接線或 Runtime 驗收。
- 追溯：[變更追溯總表](../../變更追溯總表.md)

## 目錄與索引

- [6. P1/P2 Current 與控制模組的歸位](#section-1)

---

<a id="section-1"></a>
## 6. P1/P2 Current 與控制模組的歸位

這些是執行控制、狀態、治理或實作入口；它們不是另一套平行功能樹。以下把 Current 登錄的主控制面按責任歸位。

- `H2-05-19` — P1/P2 Current-control refs: control_gate_runtime; local_acceptance_runtime; ci_gate (legacy/reference only; P2 Actions policy remains archived); actions_execution_observer; actions_execution_replay; actions_execution_recovery; actions_execution_recovery_dispatch; actions_execution_local_fallback; actions_execution_closure; actions_execution_truth_adapter; actions_execution_diagnostic; p14_d_recovery_entrypoint; p14_d_runtime_closure; p14_d_recovery_e2e; actions_execution_recovery_mode.
- `H2-04-14` — Capability / instruction refs: capability_support_matrix; capability_namespace_budget; capability_runtime_consumption; capability_runtime_measurement; capability_usage_aggregator; capability_reevaluation; capability_retirement_gate; capability_state_store; capability_router; function_capability_gate; instruction_profile; effort_level_routing; external_tool_capability_binding.
- `H2-07-23` — Current / state refs: active_work_packet; active_construction_packet; current_truth_reconciliation; runtime_execution_truth; current_projection_sync; current_authority_schema; architecture_baseline; architecture_baseline_snapshot; architecture_spine; current projection/status and Current readback.
- `H2-03-12` — Knowledge / evidence refs: research_memory_box; research_memory_box_per_claim_provenance; research_source_normalization; knowledge_intake; knowledge_retrieval; knowledge_context; knowledge_canon; knowledge_versioning; reverse_context_selection; history_query; repository_architecture_evidence; external_architecture_evidence_adapter.
- `H2-07-24` — Continuity refs: context_sufficiency; context_budget_registry; continuation_context_box; simulated_amnesia_resume; isolated_update_handoff_recovery; task_admission_amnesia_boundary; construction_session_record; continuation_box_index.
- `H2-06-21` — Reconstruction/build refs: reverse_reconstruction; progressive_repository_scanner; partial_system_state; reconstruction_artifact_lifecycle; architecture_fit; architecture_reassessment; system_factory; system_factory_artifact_emitter; system_factory_construction_handoff; domain_system_standard_template; construction_factory; construction_registration; construction_entrypoint; construction_packet; construction_lifecycle.
- `H2-08-26` — Acceptance / regression refs: progress_gate; minimum_acceptance_policy; control_gate_report; local_acceptance; local_acceptance_capture; local_control_gate; local_p14_d_runtime_acceptance; scenario_oracle; regression_selection; regression_executor; e2e_regression; repository_hygiene_gate.
- `H2-08-28` — Diagnosis / recovery refs: anti_spin_policy; anti_spin_policy_mode; debug_escalation_policy; dynamic_boundary_runtime_probe; runtime_evidence_probe; update_closure_reconciliation; m31_close_reconciliation; root_cause_distillation; construction_failure_playbook.
- `H2-09-29` — Governance refs: change_impact_registry; change_impact_v2; change_scope_policy; change_scope_gate; control_gate_m23_p14; canonical_task_admission; external_tool_radar; external_tool_candidate_review; external_tool_candidate_bridge; github_native_governance; long_run_cost_observatory; adaptive_segment_sizing.
- `H2-09-30` — Capability evolution refs: native_replacement_measurement; native_replacement_evaluation; native_replacement_evolution_execution; native_replacement_adoption_closure; capability_runtime_consumption; external_tool_radar; external_tool_candidate_review; external_tool_candidate_bridge; external_tool_capability_binding.
- `H2-09-31` — Architecture/evolution refs: architecture_decision; blueprint_update_transaction; evolution_controller; evolution_cycle; evolution_cycle_execution; update_learning; plan_lifecycle_audit; progress_execution_contract; construction_efficiency_review; self_evolution_trust_evidence; maintenance_long_run_simulation.
- `H2-09-32` — Lifecycle/archive refs: artifact_lifecycle_policy; artifact_lifecycle_audit; obsolete_asset_audit; reconstruction_artifact_lifecycle; asset_quarantine; retention_gate; lifecycle_sweep; archive_governance; repository_budget.
- `H2-10-33` — Conversation / command refs: conversation_instruction_control; conversation_record; conversation_analysis_report; user_habit; habit_trigger; command_shortcuts; central_role_lifecycle; role_session_gate; role_command_router.
- `H2-10-34` — Presentation/handoff refs: presentation_selector; handoff_render; analysis_report_cli; operational_reference_pack; repository_result_writer; repository_result_ingestion.
- `H2-10-35` — Closeout refs: update_closure_reconciliation; current_truth_reconciliation; work_execution_record; construction_session_record; continuation_context_box; result_distillation; P1 update_learning.
- `H2-05-19` — P2 Current implementation-control refs: active_work_packet; active_construction_packet; construction_packet; canonical_task_admission.
- `H2-07-23` — P2 Current implementation-control refs: current_truth_reconciliation; runtime_execution_truth; current_projection_sync.
- `H2-06-21` — P2 Current implementation-control refs: reverse_reconstruction; partial_system_state.
- `H2-09-30` — P2 Current implementation-control refs: external_tool_radar.
