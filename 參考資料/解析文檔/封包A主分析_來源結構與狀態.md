# 封包 A 主分析分支｜來源身分、結構與狀態

- 文件 ID：FORAVAR-ARCHIVE-A-BR-001
- 類型：BRANCH
- 狀態：CURRENT／封包 A 靜態分析；結論受列明證據範圍限制
- 唯一責任：保存封包 A 主報告指定章節的完整數據、來源、狀態與限制。
- 主軸回鏈：[封包 A 實體解析與完整性驗收主軸](./封包A_R3d130j_實體壓縮檔解析與完整性驗收_2026-10-21.md)
- 上層主軸：[壓縮檔解析總覽](./壓縮檔逆向分析與蒸餾紀錄.md)
- 追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [1. 來源身分與完整性](#section-1)
- [2. 封包結構與檔案分布](#section-2)
- [3. 架構與文件責任索引](#section-3)
- [4. 快照中的當前狀態](#section-4)

---

<a id="section-1"></a>
## 1. 來源身分與完整性

| 欄位 | 驗證結果 |
|---|---|
| 原始檔 | `P2-relay-R3d130j.zip` |
| 壓縮大小 | 1,885,519 bytes |
| 裸檔 SHA-256 | `f38cc51fcd443500d63e5693bd2946dfd099ee03e57bb105c9e7d86cf96cb521` |
| forAVAr 原始檔 Git Blob SHA-1 | `0e58526bd35c30a25f3b27033a4952ec5f25bf10` |
| ZIP 成員項目 | 774；唯一路徑 774；沒有重複項目名稱 |
| 展開總大小 | 5,479,985 bytes |
| 內附 Manifest | `MANIFEST.sha256`，773 筆內容檔紀錄 |
| Manifest SHA-256 | `65e10ebfee0150eab822d870284fff89525c8d87e584acc04281e83624cb1c02` |
| Manifest 驗證 | 773／773 全數匹配，0 個缺檔或未登錄成員 |
| ZIP CRC | `zipfile.testzip()` 回傳 `None` |
| 路徑安全 | 未發現絕對路徑、`..` 路徑穿越或反斜線路徑 |
| 巢狀壓縮簽章 | 未發現常見 ZIP／7z／gzip／RAR 內層壓縮檔簽章 |

Git Blob SHA-1、裸檔 SHA-256、ZIP 成員 CRC32、Manifest 成員 SHA-256 屬不同層次，不能互相替代。上述結果證明封裝及已登錄內容的位元組完整性，不證明程式邏輯正確或運行成功。

<a id="section-2"></a>
## 2. 封包結構與檔案分布

### 2.1 檔案類型

| 類型 | 數量 | 主要用途 |
|---|---:|---|
| Python（`.py`） | 374 | 控制層、工具、測試及模組 |
| JSON（`.json`） | 312 | Current、工作包、Schema、政策、登錄表及 fixtures |
| SARIF | 1 | 靜態掃描結果資料 |
| Markdown（`.md`） | 69 | 架構、規劃、研究、交接、稽核與說明 |
| YAML（`.yml`／`.yaml`） | 11 | 工作流及設定 |
| TXT | 3 | 輔助資料 |
| SHA-256 清單 | 2 | 雜湊資料 |
| 無副檔名 | 2 | 依內容與路徑判讀 |
| **合計** | **774** | 全部成員已納入清冊 |

### 2.2 目錄分布

| 主要路徑 | 檔案數 | 職責 |
|---|---:|---|
| `P1-Central-Control/` | 658 | 控制層、scripts、tests、schemas、policy、progress、evidence、canonical 與 fixtures |
| `docs/` | 59 | 藍圖、規劃、研究、交接及稽核 |
| `tools/` | 31 | 封包、啟動、預檢、引用／接線稽核與結案相關工具 |
| `.github/` | 12 | Actions 工作流與儲存庫協作設定 |
| `參考資料/` | 6 | 參考企劃及研究來源 |
| 其他根目錄／設定 | 8 | Current、README、Skill 與環境設定等 |

主要可數出的子集合：159 個 `P1-Central-Control/scripts/*.py`、27 個 `tools/*.py`、177 個 `P1-Central-Control/tests/test_*.py`、135 個 JSON Schema。檔案數不等於有效能力、正式 caller 或已通過測試的數量。

### 2.3 靜態／格式檢查結果

| 檢查 | 結果 | 可支持的結論 |
|---|---|---|
| Python AST | 374／374 通過 | Python 檔可解析；未執行程式 |
| JSON＋SARIF 語法 | 313／313 通過 | 可按 JSON 格式解析 |
| YAML 語法 | 11／11 通過 | 可按 YAML 格式解析 |
| 其他文字 UTF-8 解碼 | 76／76 通過 | 文字編碼可讀 |
| JSON Schema meta-validation | 135／135 通過 | Schema 本身符合宣告的 Draft 2020-12 meta-schema |
| 指定核心 JSON 實例 | 5／5 通過指定 Schema | Current、Feature Batch、Construction、Reconstruction Input Set、Canonical Blueprint 的指定驗證通過 |
| 外部相對 Schema `$ref` | 未發現缺失目標 | 不代表所有業務語意與相依關係已驗收 |

<a id="section-3"></a>
## 3. 架構與文件責任索引

| 來源 | 責任 | 使用限制 |
|---|---|---|
| `P1-CURRENT.json` | 唯一執行狀態與 Active Work 入口 | 不能以 HANDOFF、README 或摘要取代 |
| `docs/architecture/P2-System-Blueprint-v1.0.md` | P2 目標／施工藍圖；實際標題 v4.0，標示 DESIGN ONLY | 定義目標，不證明功能已實作 |
| `P1-Central-Control/progress/P2-B1-B8.work.json` | 當前工作單元、下一步、限制與接受條件 | 當前工作狀態，不代表已完成 |
| `P1-Central-Control/progress/construction/P2-B1-B8.construction.json` | 施工契約，狀態 BUILDING | 不等同驗收 |
| `P1-Central-Control/progress/P2-B1-B8.feature-batch.json` | F01–F30 範圍與局部案例／正式驗收閘門 | 凍結範圍不代表通過 |
| `docs/plans/P2-Feature-Triage.md` | 功能現況及實作證據矩陣 | 必須與 Current／Feature Batch 交叉核對 |
| `docs/plans/P2-Relay-Update-Plan.md` | 規劃參考 | 不能凌駕 Current 或凍結的 Feature Batch |
| `docs/handoffs/handoff.data.json`／`HANDOFF.md` | R3d130j 交接資料與閱讀視圖 | 歷史交接，不能替代 Current |
| `docs/audit/OPEN-ISSUES.md` | P2 未結問題清單 | 本快照已存在 002c 狀態一致性問題 |

<a id="section-4"></a>
## 4. 快照中的當前狀態

以下是封包內記錄的快照狀態，不是對即時 GitHub HEAD 的宣告。

| 欄位 | 快照值 |
|---|---|
| Current stage | `P2-B1-B8-CODE-FIRST`／`IN_PROGRESS` |
| Active Work | `P1-Central-Control/progress/P2-B1-B8.work.json` |
| Feature Batch | `REALIZATION`；30 項功能；`scope_frozen=true` |
| 正式測試範圍 | `INCOMPLETE_FOR_BATCH`；`official_test_roster=[]` |
| 功能狀態 | 20 項 `CODE_PRESENT_UNVERIFIED`，10 項 `PARTIAL` |
| 局部案例 | 90 個，全數 `NOT_RUN` |
| test_method | 33 個已綁定，57 個為 null |
| Work 的 Python 測試狀態 | `NOT_EXECUTED` |
| formal caller | `UNKNOWN` |
| Active Pack | `NOT_GENERATED` |
| Runtime Truth | `INCOMPLETE` |
| Construction | `BUILDING` |

快照內的下一個建議動作是在符合既有工作包限制的 Python 3.11 環境執行 `test_construction_progress_watchdog.py`，留存實際輸出、退出碼、HEAD 與 source hash，再處理已綁定的局部案例。若沒有符合限制的環境，維持 `NOT_EXECUTED／NOT_RUN`；不得提前宣告正式整批驗收通過。
