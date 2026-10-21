# 追溯分類分支｜APSGA（原 C′）架構選型與外部研究

- 文件 ID：FORAVAR-TRACE-CAT-007
- 類型：TRACE_BRANCH／ARCHITECTURE_RESEARCH
- 狀態：CURRENT_BRANCH；負責架構選型及 APSGA 藍圖事件導航，不代表所有候選設計已採納或實作
- 唯一責任：定位 C′ 架構比較、外部證據、語言選型與驗證設計。
- 主追溯入口：[變更追溯總表](../變更追溯總表.md)
- 研究主軸：[C′ 架構選型再評估](../解析文檔/Cprime架構選型再評估與外部研究_2026-10-21.md)

## 事件清單

| EVENT_ID | 日期 | OP／主題 | 摘要 | 詳細事件 | VERIFY |
|---|---|---|---|---|---|
| EVT-0039 | 2026-10-21 | REASSESS_CPRIME_ARCHITECTURE_WITH_EXTERNAL_EVIDENCE | 比較問題清單、SOP、C′ 與外部架構研究；提出收斂原型和 A／B／C′ 驗證方案。 | [EVT-0039](./EVT-0039_Cprime架構選型研究.md) | PARTIAL |
| EVT-0040 | 2026-10-21 | COMPARE_CPRIME_PACKET_P1_ROLE_SYSTEM_PLUGIN_ARCHITECTURES | 比較五種架構，建議 C′ 作上層並條件式採用封包、角色、獨立系統和插件工作流。 | [EVT-0040](./EVT-0040_Cprime五種架構對比研究.md) | PARTIAL |
| EVT-0041 | 2026-10-21 | CREATE_APSGA_FIRST_AND_SECOND_RENDER_BLUEPRINT | 建立 APSGA 核心骨架、總體藍圖及 X01–X12 擴充模組地圖。 | [EVT-0041](./EVT-0041_APSGA核心骨架首輪渲染.md) | PARTIAL |
| EVT-0042 | 2026-10-21 | ADD_APSGA_GLOBAL_CLOSURE_AND_SELECTION_RULES | 建立 S01–S16 情境基線、全局閉環、擴充方案比較程序及反製造問題 Gate。 | [EVT-0042](./EVT-0042_APSGA全局情境閉環與架構選擇規則.md) | PARTIAL |
| EVT-0043 | 2026-10-21 | AUDIT_APSGA_COVERAGE_AGAINST_PROBLEM_REGISTER | 對照 PR-001–PR-054；確認 Preflight、分類／回寫、基線及 Runtime 證據缺口。 | [EVT-0043](./EVT-0043_APSGA問題清單覆蓋驗收與缺口審查.md) | PARTIAL |
| EVT-0044 | 2026-10-21 | ADD_APSGA_PROBLEM_STATUS_AND_TEST_READINESS_SUPPLEMENT | 補充問題清單現行狀態分布、逐項殘餘驗收條件與 S01–S16 測試就緒度。 | [EVT-0044](./EVT-0044_APSGA問題清單狀態分布補充稽核.md) | PARTIAL |
| EVT-0045 | 2026-10-21 | ASSESS_APSGA_COGNITIVE_CORE_DRIFT | 判定認知原則未被正式推翻，但架構展開重心偏向治理、控制、狀態與生命週期；思考核心規格仍未充分展開。 | [EVT-0045](./EVT-0045_APSGA核心偏移評估.md) | RECORDED |

## 使用規則

- 本分支只做事件定位；外部來源與限制見研究分支 B，完整結論見研究 MASTER。
- 研究建議與 APSGA 藍圖候選不能直接當成已實作 Runtime 能力。
- 僅在授權決策和可重複驗收完成後，才可把採納狀態更新至相應權威文件。
