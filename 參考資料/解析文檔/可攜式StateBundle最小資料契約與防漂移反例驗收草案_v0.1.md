# 可攜式 State Bundle｜最小資料契約與防漂移反例驗收草案 v0.1

> 主軸回鏈：[State Bundle｜主軸彙整](../StateBundle_主軸彙整.md) ｜ 分支 ID：STATE-BR-001 ｜ 本回鏈只提供導航，不改變本文件的證據邊界。

- 文件 ID：FORAVAR-STATE-BUNDLE-CONTRACT-001
- 日期：2026-10-21
- 狀態：PROPOSAL / NOT_APPROVED / NOT_IMPLEMENTED
- 類型：問題解決方法與最小資料契約研究草案，不是正式架構企劃的更新
- 來源問題：PR-052；關聯 PR-001、PR-004、PR-005、PR-019、PR-021、PR-042
- 寫入邊界：只新增於 forAVAr 參考資料；P1、P2 只讀

## 0. 目的與結論

本草案處理一個特定運行模式：AI／協作者無法直接讀取 GitHub 或最新 repository，卻仍需要安全接續工作。解決方法不是將全部對話、全部程式碼或初始藍圖無限制複製到提示，而是提供一份能驗證來源、重建工作狀態、限制目前工作範圍和保留證據的**可攜式工作快照**。

State Bundle 是快照，不是新的 Current，不是藍圖替代品，也不是企劃批准。它必須從既有權威來源生成；若不能證明來源版本及一致性，應清楚標記 `BLOCKED_CONTEXT` 或 `STALE_CONTEXT`，不得猜測當前狀態。

本草案的驗收目標是：一個沒有 repository 即時存取的新會話，只根據 State Bundle，就能辨識目前允許處理的工作、目前不能聲稱完成的事項、已批准與未批准的範圍、需要的來源證據及停止條件；當快照缺失、過期或衝突時，能拒絕依賴未確認現況的施工。

## 1. 問題與非目標

### 1.1 目標解決的問題

- 當前 repository 不可讀，AI 只取得初始藍圖或歷史對話。
- Current、工作包、Feature Batch、README、HANDOFF 的資訊不一致。
- 新會話無法區分當前工作、歷史工作、預期產物及已驗收產物。
- 局部修補沒有與原始目標、核心不變量、非目標和接受條件建立明確關聯。
- 歷史測試／舊 Commit 的結果被誤當成目前版本證據。
- 新增模組、規則或架構節點沒有先比較既有候選。

### 1.2 明確不處理

- 不把 State Bundle 變成第二份 Current 或永久的完整 repository 複本。
- 不將所有任務都強制變成高成本的完整研究工作流。
- 不以新增另一套通用狀態機取代既有生命週期／工作流程。
- 不藉本草案直接修改 C′ 主企劃、P1 或 P2。
- 不宣稱本草案已解決 Claude 免費版、帳戶權限、網路或平台功能限制；它提供無即時 repository 存取時可使用的資料契約。
- 不將檔案存在、測試案例登錄或靜態檢查等同於 Runtime 通過。

## 2. 三個不同物件，不可互相替代

### 2.1 Core Anchor：穩定核心

負責回答「整個工作為什麼存在、哪些內容不可以為局部修補而改變」。

必要欄位：
- `objective`：原始目的，以來源參照綁定，不能只保留經摘要改寫的一句話。
- `core_invariants`：不可變原則及其 ID／權威位置。
- `non_goals`：目前明確不做的事項。
- `success_conditions`：整體成功條件，與本次局部測試通過分開。
- `stop_conditions`：哪些情形需停止、回報阻塞或重新取得授權。
- `authority_ref`：每一項核心主張回指的權威文件及版本指紋。

### 2.2 Current State：動態現況

負責回答「目前 repository／系統到底處於什麼狀態」。

必要欄位：
- `snapshot_id`、來源 repository／branch／commit SHA（若來源提供）、產生時間。
- `manifest_digest`、清單格式版本和來源完整性檢查結果。
- 唯一 Current 位置與指紋、Active Work、Construction／Feature Batch 狀態及引用。
- 目前階段、目前工作範圍、明確下一步、已完成／未完成項目。
- 各項證據狀態與其綁定的版本／來源指紋。
- 開放衝突、缺失來源、失效連結和已知阻塞。
- 新鮮度狀態：`FRESH_AT_CAPTURE`、`STALE`、`CONFLICT` 或 `UNKNOWN`。

### 2.3 Task Contract：本次任務契約

負責回答「這一輪被允許做什麼」。

必要欄位：
- `task_id`、`task_objective` 與它對應的 Core Anchor／Problem ID。
- `in_scope`、`out_of_scope`、`allowed_write_paths`、`read_only_paths`。
- 所需來源清單與必要上下文；來源不在包內時的處理規則。
- 前置條件、接受條件、應保存的輸出。
- 失敗／未知／衝突的停止條件和交接要求。
- 授權參照或授權狀態。沒有可驗證授權的範圍不得因 State Bundle 出現就自動獲批。

## 3. 最小可攜式資料結構

以下是候選 JSON 形狀，用於討論欄位責任；**它不是已核准或已登錄的 JSON Schema，也不得直接當成 Runtime 接口。**

```json
{
  "bundle_schema_version": "0.1",
  "bundle_id": "STATE-BUNDLE-<stable-id>",
  "generated_at": "<ISO-8601>",
  "mode": "REPOSITORY_UNAVAILABLE",
  "source_snapshot": {
    "repository": "<owner/repository-or-unknown>",
    "branch": "<branch-or-unknown>",
    "commit_sha": "<sha-or-unknown>",
    "archive_sha256": "<sha256-or-unknown>",
    "manifest_ref": "<path-or-embedded-manifest>",
    "manifest_digest": "<sha256>",
    "integrity_status": "PASS | FAIL | UNKNOWN",
    "captured_at": "<ISO-8601>"
  },
  "load_status": {
    "status": "READY | BLOCKED_CONTEXT | STALE_CONTEXT | CONFLICT",
    "required_sources_present": true,
    "source_conflicts": [],
    "missing_sources": [],
    "reason": ""
  },
  "core_anchor": {
    "objective": {
      "text": "<brief, non-authoritative rendering>",
      "source_refs": []
    },
    "core_invariants": [],
    "non_goals": [],
    "success_conditions": [],
    "stop_conditions": [],
    "authority_refs": []
  },
  "current_state": {
    "current_authority_ref": "",
    "current_fingerprint": "",
    "active_work_ref": "",
    "active_work_fingerprint": "",
    "active_batch_ref": "",
    "active_batch_fingerprint": "",
    "construction_ref": "",
    "construction_fingerprint": "",
    "phase": "UNKNOWN",
    "status": "UNKNOWN",
    "next_action": "",
    "completed": [],
    "incomplete": [],
    "blockers": [],
    "evidence_refs": [],
    "open_conflicts": []
  },
  "task_contract": {
    "task_id": "",
    "objective": "",
    "problem_ids": [],
    "in_scope": [],
    "out_of_scope": [],
    "allowed_write_paths": [],
    "read_only_paths": [],
    "required_inputs": [],
    "acceptance_conditions": [],
    "stop_conditions": [],
    "authorization_ref": ""
  },
  "change_ledger": [],
  "handoff": {
    "next_action": "",
    "required_read_order": [],
    "prohibited_actions": [],
    "unresolved_questions": []
  }
}
```

Schema 需要進一步定義各狀態的條件、欄位是否必填、指紋算法、參照路徑規則、敏感資料排除、版本相容性以及衝突時的確定性排序。以上範例中的 placeholder 並不是可直接執行的實例。

## 4. 生成規則：由既有權威來源派生，禁止雙重真相

建議來源順序（需按實際專案裁定，不允許 State Bundle 自行凌駕來源）：

1. **Current／執行狀態權威：** 指明當前階段、Active Work 和狀態來源。
2. **唯一目標藍圖：** 讀取與本任務相關的核心原則、架構契約及要求。
3. **Active Work／Construction：** 讀取本輪下一步、範圍、前置條件和接受條件。
4. **凍結 Feature Batch／範圍指紋：** 確認不得無聲擴張或重設的工作範圍。
5. **具體實作、測試、證據及開放問題：** 只納入本工作需要的引用；每一項結論保留來源版本和證據層級。
6. **HANDOFF／README／文件索引：** 作導航、歷史和恢復輔助；若與權威狀態衝突，不得因它文字較完整就升格為權威。

生成器不應把整份 repository 的全文放進 Bundle，而要列明被納入／排除的來源與理由。若是手工製作的離線 Bundle，必須標記 `generation_method=MANUAL`，不能偽裝成自動由 Current 產生。

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

## 6. Core-Drift Gate：局部修補前的六個問題

對可能影響系統方向或擴大工程範圍的修改，先回答：

1. 這個修補對應哪個 Problem ID、可重現故障或失敗接受條件？
2. 它如何連結到 Core Anchor／核心不變量？若只屬局部維護，為何要動核心？
3. 根因是直接觀察、假說還是已確認？有哪些能區分根因的替代解釋？
4. 既有能力是否足以 REUSE／MODIFY／MERGE？選 NEW／新增常設規則時有什麼證據？
5. 本次改動的明確範圍、非目標、下游依賴、測試與回退界線是什麼？
6. 哪一項實際證據可令修正通過？若無法執行測試，要如何保留 NOT_EXECUTED 並交接？

下列情況預設不允許直接施工：改變目標或非目標、改變權威來源、改變接受條件、擴張凍結範圍、變更權限／資料模型／不可逆副作用，或 State Bundle 狀態不是 READY。需要重新定義架構時，另進入明確授權的架構變更流程；不能藉由把局部問題命名為「根因」跳過範圍審查。

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

## 9. 最小實施順序

1. **文件層：** 裁定欄位、權威來源優先序、狀態分類與 fail-closed 條件；在反例審查前不建立 Schema 或 Runtime。
2. **固定測試：** 將 DRIFT-01～DRIFT-10 補成有明確資料夾、輸入、預期結果與收據格式的測試集。
3. **人工離線試用：** 從權威檔案生成一次 State Bundle，讓全新會話僅讀該包，檢查是否能正確還原目標、工作範圍、未知和下一步；來源衝突時是否停下。
4. **生成方式比較：** 比較完整歷史交接、最小 Bundle、只讀藍圖三種方式對狀態重建正確率、漏失、錯誤施工意圖、讀取成本及交接時間的影響。沒有測量前不宣稱 Bundle 最優。
5. **有授權後才進入實作：** 對照既有 C′ 主企劃、方法規格和施工台帳，先產生變更提案，不把本草案視為自動批准。
6. **回退與維護：** 每次 Bundle 版本更新有源檔指紋；格式不相容時版本升級；來源不存在時可回復到上次可用包，但一定標示其為舊快照。

## 10. 來源

- forAVAr 問題清單：PR-001、004、005、019、021、042 及本輪新增候選 PR-052。
- forAVAr：《P2 核心漂移：根因分解與下一步權威狀態核對紀錄（2026-10-21）》。
- forAVAr：《P2 核心主軸漂移根因與 forAVAr 防偏離架構驗證（2026-10-21）》。
- Liu et al.，[Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), TACL 2024。
- Anthropic，[Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), 2025-09-29。
- Liu et al.，[Context as a Tool](https://aclanthology.org/2026.findings-acl.1032/), Findings of ACL 2026。
- Xu et al.，[MemTrace](https://arxiv.org/abs/2610.04838), arXiv preprint, 2026-10-04；屬預印本，不視為已完成獨立複驗。

**最終狀態：** 本文件定義最小候選契約及可驗收反例，但仍是 PROPOSAL / NOT_IMPLEMENTED。唯一 Current 仍在既有權威來源中；State Bundle 的目的是攜帶與驗證必要上下文，不是建立第二份真相。
