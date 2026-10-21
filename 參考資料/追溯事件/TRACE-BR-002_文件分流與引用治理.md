# 追溯分類分支｜文件分流、索引遷移與引用治理

- 文件 ID：FORAVAR-TRACE-CAT-002
- 類型：TRACE_BRANCH／SEMANTIC_CATEGORY
- 狀態：CURRENT_BRANCH／保留原事件紀錄摘要；個別驗收狀態不因分流而改變
- 唯一責任：按語意類型集中保存事件表，供主追溯索引搜尋與定位。
- 搜尋詞：雙向引用、回鏈、問題清單分支、職責矩陣、P2封包、Claude Code、WebToApp、方法選擇、封包A、封包B、State Bundle、C′施工台帳、文件分流、SPLIT_TOPIC、BACKLINK_MIGRATION
- 主追溯入口：[變更追溯總表](../變更追溯總表.md)
- 分流原則：事件 ID、日期、OP、重要變更摘要、來源證據及 VERIFY 原義保留；路徑只按新文件位置修正。

## 事件清單

| EVENT_ID | 日期（Asia/Taipei） | OP／主題 | 重要變更與目前定位 | 來源證據 | VERIFY |
|---|---|---|---|---|---|
| EVT-0012 | 2026-10-21 | `BACKLINK_MIGRATION` | 35 個已知分支回鏈通過讀回檢查；全庫引用覆蓋仍 PARTIAL。 | [EVT-0012](./EVT-0012_雙向引用回鏈遷移.md) | VERIFIED（限定範圍） |
| EVT-0013 | 2026-10-21 | `SPLIT_PROBLEM_REGISTER` | 問題清單主軸＋五分支；v0.3／v0.2 原文備份保留，逐段對帳通過。 | [EVT-0013](./EVT-0013_問題清單主軸與分支分流.md) | VERIFIED |
| EVT-0014 | 2026-10-21 | `SPLIT_RESPONSIBILITY_MATRIX` | 權責矩陣主軸＋四分支；拆分前／初始版備份保留，逐章對帳通過。 | [EVT-0014](./EVT-0014_文件責任矩陣分流.md) | VERIFIED |
| EVT-0015 | 2026-10-21 | `SPLIT_P2_PACKAGE_SYNTHESIS` | P2 封包整合主軸＋四分支；全文與早期版備份保留，逐節對帳通過。 | [EVT-0015](./EVT-0015_P2封包整合主文件分流.md) | VERIFIED |
| EVT-0016 | 2026-10-21 | `SPLIT_CLAUDE_MODERNIZATION_REPORT` | Claude 外部研究報告主軸＋五分支；全文備份保留，逐節對帳通過。 | [EVT-0016](./EVT-0016_Claude_Code_Modernization長報告分流.md) | VERIFIED |
| EVT-0017 | 2026-10-21 | `SPLIT_WEBTOAPP_REPORT` | WebToApp 報告主軸＋三分支；全文備份保留，逐節對帳通過。 | [EVT-0017](./EVT-0017_WebToApp逆向報告分流.md) | VERIFIED |
| EVT-0018 | 2026-10-21 | `SPLIT_METHOD_SELECTOR_SPEC` | 方法選擇規格主軸＋三分支；v0.2 備份保留，11 節對帳通過。 | [EVT-0018](./EVT-0018_方法選擇規格分流.md) | VERIFIED |
| EVT-0019 | 2026-10-21 | `SPLIT_ARCHIVE_B_FORMAT_AUDIT` | 封包 B 稽核主軸＋三分支；全文備份保留，9 節對帳通過。 | [EVT-0019](./EVT-0019_封包B雙格式稽核分流.md) | VERIFIED |
| EVT-0020 | 2026-10-21 | `SPLIT_ARCHIVE_A_MASTER_REPORT` | 封包 A 主分析主軸＋三分支；全文備份保留，9 個實質章節對帳通過。 | [EVT-0020](./EVT-0020_封包A主分析分流.md) | VERIFIED |
| EVT-0021 | 2026-10-21 | `SPLIT_P1_P2_FUNCTION_TREE` | 功能骨架樹分十個 H1 子樹＋三個映射分支；全文備份保留，P1／P2 仍唯讀。 | [EVT-0021](./EVT-0021_P1P2功能骨架樹分流.md) | VERIFIED（forAVAr 映射檔） |
| EVT-0022 | 2026-10-21 | `SPLIT_STATEBUNDLE_CONTRACT` | State Bundle 契約分三支；原 v0.1 備份保留，契約仍 NOT_APPROVED／NOT_IMPLEMENTED。 | [EVT-0022](./EVT-0022_StateBundle契約分流.md) | VERIFIED |
| EVT-0023 | 2026-10-21 | `SPLIT_CPRIME_LEDGER` | C′ 施工台帳主軸＋兩分支；全文備份保留，主企劃正文未改動，逐節對帳通過。 | [EVT-0023](./EVT-0023_Cprime施工台帳分流.md) | VERIFIED（施工台帳） |

## 使用規則

- 本分支只負責以上分類中的歷史事件摘要，不取代來源報告、SOP 或研究主軸。
- 查詢目前狀態時，以事件所連結的現行權威文件為準；歷史事件描述不得直接當成最新狀態。
- 後續新增事件先按語意類別歸位；若出現跨類型事件，選定一個唯一責任分支，再從主索引提供多個搜尋詞，避免重複保存同一事件。
