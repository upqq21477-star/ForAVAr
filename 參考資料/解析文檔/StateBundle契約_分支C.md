# State Bundle 最小資料契約分支｜C

- 文件 ID：FORAVAR-STATE-BUNDLE-CONTRACT-BR-003
- 類型：BRANCH
- 狀態：CURRENT／候選契約；NOT_APPROVED／NOT_IMPLEMENTED
- 唯一責任：保存原 v0.1 契約的原章節 5、6、7、8、9、10；完整欄位、狀態、例外、反例和驗收條件以原文為準。
- 主題回鏈：[State Bundle 主軸彙整](../StateBundle_主軸彙整.md)
- 舊入口相容頁：[原契約路徑](./可攜式StateBundle最小資料契約與防漂移反例驗收草案_v0.1.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [5. 啟動／載入 fail-closed 規則](#section-1)
- [6. Core-Drift Gate：局部修補前的六個問題](#section-2)
- [7. 以本次 P2 快照作為反例資料，不視為運行實例](#section-3)
- [8. 防偏離反例測試](#section-4)
- [9. 最小實施順序](#section-5)
- [10. 來源](#section-6)

---

<a id="section-1"></a>
## 5. 啟動／載入 fail-closed 規則

### 5.1 READY 的最低條件

- 核心目標與本次 Task Contract 都可回溯到可識別來源。
- Current、Active Work 和受凍結的批次範圍均在包內，或者明確說明此任務不依賴哪些資料。
- 來源清單完整性檢查通過；關鍵來源有版本指紋。
- 必要接受條件、禁止範圍、寫入邊界、下一步及停止條件清楚。
- 沒有尚未解決、會影響本次決策的權威來源衝突。

### 5.2 必須阻擋的情況

- 只有初始藍圖，沒有足以判斷現況的 Current／Active Work。
- Current、Work、Feature Batch 對目前階段／範圍有衝突，且不能根據既定權威規則解決。
- 關鍵檔案缺失、Manifest 不匹配、來源 SHA 不同，卻仍引用舊測試或舊批准作為當前證據。
- 任務需要修改的檔案不在讀取資料中，或無法核對目前基準版本。
- 寫入授權或可寫範圍不明確。
- Bundle 產生時間超過專案明訂的有效窗口，或相應權威來源已知發生變更。
- State Bundle 自己與權威來源有差異，卻未聲明 `STALE`／`CONFLICT`。

### 5.3 READY 不代表每個主張都已證實

READY 代表「本次任務必要的上下文足夠，且已知衝突可處理」，不代表所有程式都實作完成。每項事實仍需要自己的證據狀態；例如 `CODE_PRESENT_UNVERIFIED`、`NOT_EXECUTED`、`UNKNOWN` 不可在 Bundle 生成過程中被改成 PASS。

<a id="section-2"></a>
## 6. Core-Drift Gate：局部修補前的六個問題

對可能影響系統方向或擴大工程範圍的修改，先回答：

1. 這個修補對應哪個 Problem ID、可重現故障或失敗接受條件？
2. 它如何連結到 Core Anchor／核心不變量？若只屬局部維護，為何要動核心？
3. 根因是直接觀察、假說還是已確認？有哪些能區分根因的替代解釋？
4. 既有能力是否足以 REUSE／MODIFY／MERGE？選 NEW／新增常設規則時有什麼證據？
5. 本次改動的明確範圍、非目標、下游依賴、測試與回退界線是什麼？
6. 哪一項實際證據可令修正通過？若無法執行測試，要如何保留 NOT_EXECUTED 並交接？

下列情況預設不允許直接施工：改變目標或非目標、改變權威來源、改變接受條件、擴張凍結範圍、變更權限／資料模型／不可逆副作用，或 State Bundle 狀態不是 READY。需要重新定義架構時，另進入明確授權的架構變更流程；不能藉由把局部問題命名為「根因」跳過範圍審查。

<a id="section-3"></a>
## 7. 以本次 P2 快照作為反例資料，不視為運行實例

觀察來源：`P1-CURRENT.json`、`P1-Central-Control/progress/P2-B1-B8.work.json`、`P2-B1-B8.feature-batch.json`、`P2-B1-B8.construction.json`、`docs/handoffs/handoff.data.json`、根目錄 README、`docs/README.md`、`docs/audit/OPEN-ISSUES.md`。

只讀映射已發現：
- Current 指向 B1–B8 的 `IN_PROGRESS`，Feature Batch 處於 REALIZATION、凍結 30 項功能、正式測試範圍尚未完成。
- HANDOFF 仍指向 R3d130j→R3d130k 的 W0／W1–W8 工作線。
- README 同時存在「與 Current 衝突以 Current 為準」的投影規則與舊段落「進度／下一步以 HANDOFF 為唯一權威」。
- `docs/README.md` 對同一 Roadmap 路徑同時標記為已被取代和唯一企劃。
- F15／F16 的測試引用指向缺失路徑；F27 的實作／測試引用與實際 archive 路徑不一致；一個測試策略文件連結失效。
- 90 個局部測試案例仍為 NOT_RUN；不能用歷史測試或文件敘述代表目前 HEAD 通過。

因此，如果有人只攜帶一份舊 HANDOFF，或只讀藍圖而未拿到 Current／Work／Feature Batch，這個 Bundle 必須是 `CONFLICT` 或 `BLOCKED_CONTEXT`，不能是 READY。若只有有效 Current 和 Active Work，卻缺乏此次任務必要的其他資料，應依任務接受條件判定是否還能走限縮的唯讀分析；不得自動擴張為完整施工。

<a id="section-4"></a>
## 8. 防偏離反例測試

以下是候選驗收矩陣，需固定輸入與預期結果，再實際執行才能裁定。此表本身不是測試收據。

| ID | 反例輸入 | 預期結果 | 目前狀態 |
|---|---|---|---|
| DRIFT-01 | 只有目標藍圖，無 Current／Active Work | `BLOCKED_CONTEXT`；不得聲稱掌握當前實作與下一步 | NOT_EXECUTED |
| DRIFT-02 | Current 指 B1–B8，HANDOFF 指其他工作線 | `CONFLICT`；按權威映射先做只讀核對，禁止由舊 HANDOFF 覆寫 Current | NOT_EXECUTED |
| DRIFT-03 | 局部缺陷修正提議加入與核心不相關的新常設能力 | 隔離為候選待辦；沒有根因證據與適當授權不納入本工作 | NOT_EXECUTED |
| DRIFT-04 | 取得 Bundle 後，來源檔 SHA／基準 Commit 改變 | 標為 `STALE_CONTEXT`，重核受影響資料與確認範圍 | NOT_EXECUTED |
| DRIFT-05 | 歷史測試 PASS，但目前 HEAD 改變且無新收據 | 歷史證據不算目前 PASS；相關案例回到 NOT_EXECUTED／需重測 | NOT_EXECUTED |
| DRIFT-06 | 交接漏掉核心非目標或把 PROPOSAL 寫成已核准 | 以權威來源糾正狀態；授權不明則阻擋寫入 | NOT_EXECUTED |
| DRIFT-07 | 連續多輪處理不同局部錯誤 | 每輪仍保留 Core Anchor、Task Contract、當前接受條件及已拒絕範圍 | NOT_EXECUTED |
| DRIFT-08 | 必要來源不可讀／連結失效／Manifest 不一致 | 不補造來源內容或測試；標記 UNKNOWN／BLOCKED，縮限到安全可做的部分 | NOT_EXECUTED |
| DRIFT-09 | 新增能力但未說明既有候選為何不能改造 | NEW 不通過；須補 REUSE／MODIFY／MERGE／NEW 比對 | NOT_EXECUTED |
| DRIFT-10 | Bundle 與 Current 指紋不同，但摘要文字看來一致 | 指紋／來源衝突優先於摘要語氣；標記 STALE／CONFLICT | NOT_EXECUTED |

### 驗收收據最低欄位

每筆案例至少保留：測試 ID、Bundle 版本、來源 Commit／檔案指紋、固定輸入、預期結果、實際結果、執行方式、執行時間、環境／模型版本（可取得時）、PASS／FAIL／BLOCKED、偏差原因和後續處置。不論執行者自述如何，未提供必要證據者仍為 NOT_EXECUTED。

<a id="section-5"></a>
## 9. 最小實施順序

1. **文件層：** 裁定欄位、權威來源優先序、狀態分類與 fail-closed 條件；在反例審查前不建立 Schema 或 Runtime。
2. **固定測試：** 將 DRIFT-01～DRIFT-10 補成有明確資料夾、輸入、預期結果與收據格式的測試集。
3. **人工離線試用：** 從權威檔案生成一次 State Bundle，讓全新會話僅讀該包，檢查是否能正確還原目標、工作範圍、未知和下一步；來源衝突時是否停下。
4. **生成方式比較：** 比較完整歷史交接、最小 Bundle、只讀藍圖三種方式對狀態重建正確率、漏失、錯誤施工意圖、讀取成本及交接時間的影響。沒有測量前不宣稱 Bundle 最優。
5. **有授權後才進入實作：** 對照既有 C′ 主企劃、方法規格和施工台帳，先產生變更提案，不把本草案視為自動批准。
6. **回退與維護：** 每次 Bundle 版本更新有源檔指紋；格式不相容時版本升級；來源不存在時可回復到上次可用包，但一定標示其為舊快照。

<a id="section-6"></a>
## 10. 來源

- forAVAr 問題清單：PR-001、004、005、019、021、042 及本輪新增候選 PR-052。
- forAVAr：《P2 核心漂移：根因分解與下一步權威狀態核對紀錄（2026-10-21）》。
- forAVAr：《P2 核心主軸漂移根因與 forAVAr 防偏離架構驗證（2026-10-21）》。
- Liu et al.，[Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), TACL 2024。
- Anthropic，[Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), 2025-09-29。
- Liu et al.，[Context as a Tool](https://aclanthology.org/2026.findings-acl.1032/), Findings of ACL 2026。
- Xu et al.，[MemTrace](https://arxiv.org/abs/2610.04838), arXiv preprint, 2026-10-04；屬預印本，不視為已完成獨立複驗。

**最終狀態：** 本文件定義最小候選契約及可驗收反例，但仍是 PROPOSAL / NOT_IMPLEMENTED。唯一 Current 仍在既有權威來源中；State Bundle 的目的是攜帶與驗證必要上下文，不是建立第二份真相。
