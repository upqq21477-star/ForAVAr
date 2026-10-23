# 追溯分類分支｜檔案退場、壓縮檔移除與來源保存

- 文件 ID：FORAVAR-TRACE-CAT-004
- 類型：TRACE_BRANCH／SEMANTIC_CATEGORY
- 狀態：CURRENT_BRANCH／保留原事件紀錄摘要；個別驗收狀態不因分流而改變
- 唯一責任：按語意類型集中保存事件表，供主追溯索引搜尋與定位。
- 搜尋詞：ZIP、封包A/B、檔案退場、GitHub delete_file、安全阻擋、SHA、工作樹移除、Git歷史清除、來源保存、備份、回復
- 主追溯入口：[變更追溯總表](../變更追溯總表.md)
- 分流原則：事件 ID、日期、OP、重要變更摘要、來源證據及 VERIFY 原義保留；路徑只按新文件位置修正。

## 事件清單

| EVENT_ID | 日期（Asia/Taipei） | OP／主題 | 重要變更與目前定位 | 來源證據 | VERIFY |
|---|---|---|---|---|---|
| EVT-0028 | 2026-10-21 | `REMOVE_REDUNDANT_ARCHIVE_FROM_WORKTREE` | 封包 A ZIP 移出 main；P2 唯讀來源保留。 | [EVT-0028](./EVT-0028_封包A工作樹移除與來源引用遷移.md) | VERIFIED（限定修補） |
| EVT-0029 | 2026-10-21 | `RETIRE_ARCHIVE_AND_AUDIT_CANDIDATE_FILES` | 封包 B ZIP 移出 main，歷史來源保留。 | [EVT-0029](./EVT-0029_封包B壓縮檔退場與文件候選稽核.md) | VERIFIED（SHA／大小一致） |
| EVT-0056 | 2026-10-23 | `RETIRE_GITHUB_FILES_AND_VERIFY_HISTORY_BOUNDARY` | 53 個資料夾檔及 3 份專用紀錄從 main 移除；路徑／樹驗證通過，舊 Blob 仍可讀，歷史清除未完成。 | [EVT-0056](./EVT-0056_GitHub文件刪除失效分析與退場流程修正.md) | VERIFIED（main 路徑）／PARTIAL（Git 歷史） |
| EVT-0057 | 2026-10-23 | `REFINE_TEMP_REPOSITORY_INTAKE_CLOSEOUT_DESIGN` | 主／暫存庫分流候選、開案／結案清單及准入邊界；未採納、未實測。 | [EVT-0057](./EVT-0057_主儲存庫與暫存儲存庫分流設計補強.md) | DOCS_READBACK_VERIFIED／CANDIDATE |

## 使用規則

- 本分支只負責以上分類中的歷史事件摘要，不取代來源報告、SOP 或研究主軸。
- 查詢目前狀態時，以事件所連結的現行權威文件為準；歷史事件描述不得直接當成最新狀態。
- 後續新增事件先按語意類別歸位；若出現跨類型事件，選定一個唯一責任分支，再從主索引提供多個搜尋詞，避免重複保存同一事件。
