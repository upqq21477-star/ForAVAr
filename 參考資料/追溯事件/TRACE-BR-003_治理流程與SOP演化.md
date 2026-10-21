# 追溯分類分支｜治理流程、SOP制度與模擬閘門

- 文件 ID：FORAVAR-TRACE-CAT-003
- 類型：TRACE_BRANCH／SEMANTIC_CATEGORY
- 狀態：CURRENT_BRANCH／保留原事件紀錄摘要；個別驗收狀態不因分流而改變
- 唯一責任：按語意類型集中保存事件表，供主追溯索引搜尋與定位。
- 搜尋詞：SOP-META-001、SOP-DOC-001、CF-009、CF-010、治理診斷、PR-053、自我改善、一萬次更新、100k、流程精簡、配對模擬、GO、NO-GO
- 主追溯入口：[變更追溯總表](../變更追溯總表.md)
- 分流原則：事件 ID、日期、OP、重要變更摘要、來源證據及 VERIFY 原義保留；路徑只按新文件位置修正。

## 事件清單

| EVENT_ID | 日期（Asia/Taipei） | OP／主題 | 重要變更與目前定位 | 來源證據 | VERIFY |
|---|---|---|---|---|---|
| EVT-0024 | 2026-10-21 | `ADD_SOP_GOVERNANCE` | SOP-META-001 v0.2 暫行主軸、執行／演化台帳及 CF-009 已接入啟動索引；通用性仍待驗證。 | [EVT-0024](./EVT-0024_SOP固定流程與演化管理.md) | VERIFIED（文件／索引限定範圍） |
| EVT-0025 | 2026-10-21 | `ADD_SOP_AUTHORING_SPEC` | 新增 SOP-DOC-001 欄位模板／蒸餾流程、對談參考紀錄及 CF-010；同步治理、索引與權責。 | [EVT-0025](./EVT-0025_SOP文件標準欄位與對話紀錄分流.md) | VERIFIED（限定文件／索引範圍） |
| EVT-0026 | 2026-10-21 | `ADD_GOVERNANCE_DIAGNOSIS_AND_SOP_CATALOG` | 記錄治理缺口、PR-053 與 SOP 分組。 | [EVT-0026](./EVT-0026_AI主動問題發現不足與SOP清單分組.md) | VERIFIED（限定） |
| EVT-0027 | 2026-10-21 | `ADD_GOVERNANCE_SELF_IMPROVEMENT_SIM` | 新增 10k／100k 合成負載模擬、對抗失效測試、自我更新邊界與條件式 SOP 候選。 | [EVT-0027](./EVT-0027_治理系統自我改善壓力模擬.md) | VERIFIED（限定文件／合成模擬範圍） |
| EVT-0034 | 2026-10-21 | OPTIMIZE_SOP_META_001 | SOP v0.4 加入 L0–L3 精簡路徑；效益未測。 | [SOP](../SOP固定流程與演化管理.md)；[問題](../問題清單_近期補入與ID對照.md#sop-efficiency-review-2026-10-21) | PARTIAL |
| EVT-0035 | 2026-10-21 | SIMULATE_KEY_RULE_GATE | 桌上比較三種閘門；淨效率未證實，不改 SOP，列 DISC-SOP-008。 | [問題紀錄](../問題清單_近期補入與ID對照.md#key-change-simulation-gate-2026-10-21) | PARTIAL |
| EVT-0036 | 2026-10-21 | SIM_GATE_ACTIVE | SOP v0.5 模擬閘門生效。 | [裁定](../問題清單_近期補入與ID對照.md#key-change-simulation-gate-2026-10-21) | PARTIAL（效益／Runtime 未測） |

## 使用規則

- 本分支只負責以上分類中的歷史事件摘要，不取代來源報告、SOP 或研究主軸。
- 查詢目前狀態時，以事件所連結的現行權威文件為準；歷史事件描述不得直接當成最新狀態。
- 後續新增事件先按語意類別歸位；若出現跨類型事件，選定一個唯一責任分支，再從主索引提供多個搜尋詞，避免重複保存同一事件。
