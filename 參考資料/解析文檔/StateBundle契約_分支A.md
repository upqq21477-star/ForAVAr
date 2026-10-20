# State Bundle 最小資料契約分支｜A

- 文件 ID：FORAVAR-STATE-BUNDLE-CONTRACT-BR-001
- 類型：BRANCH
- 狀態：CURRENT／候選契約；NOT_APPROVED／NOT_IMPLEMENTED
- 唯一責任：保存原 v0.1 契約的原章節 0、1、2；完整欄位、狀態、例外、反例和驗收條件以原文為準。
- 主題回鏈：[State Bundle 主軸彙整](../StateBundle_主軸彙整.md)
- 舊入口相容頁：[原契約路徑](./可攜式StateBundle最小資料契約與防漂移反例驗收草案_v0.1.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [0. 目的與結論](#section-1)
- [1. 問題與非目標](#section-2)
- [2. 三個不同物件，不可互相替代](#section-3)

---

## 原始前置內容

# 可攜式 State Bundle｜最小資料契約與防漂移反例驗收草案 v0.1

> 主軸回鏈：[State Bundle｜主軸彙整](../StateBundle_主軸彙整.md) ｜ 分支 ID：STATE-BR-001 ｜ 本回鏈只提供導航，不改變本文件的證據邊界。

- 文件 ID：FORAVAR-STATE-BUNDLE-CONTRACT-001
- 日期：2026-10-21
- 狀態：PROPOSAL / NOT_APPROVED / NOT_IMPLEMENTED
- 類型：問題解決方法與最小資料契約研究草案，不是正式架構企劃的更新
- 來源問題：PR-052；關聯 PR-001、PR-004、PR-005、PR-019、PR-021、PR-042
- 寫入邊界：只新增於 forAVAr 參考資料；P1、P2 只讀



<a id="section-1"></a>
## 0. 目的與結論

本草案處理一個特定運行模式：AI／協作者無法直接讀取 GitHub 或最新 repository，卻仍需要安全接續工作。解決方法不是將全部對話、全部程式碼或初始藍圖無限制複製到提示，而是提供一份能驗證來源、重建工作狀態、限制目前工作範圍和保留證據的**可攜式工作快照**。

State Bundle 是快照，不是新的 Current，不是藍圖替代品，也不是企劃批准。它必須從既有權威來源生成；若不能證明來源版本及一致性，應清楚標記 `BLOCKED_CONTEXT` 或 `STALE_CONTEXT`，不得猜測當前狀態。

本草案的驗收目標是：一個沒有 repository 即時存取的新會話，只根據 State Bundle，就能辨識目前允許處理的工作、目前不能聲稱完成的事項、已批准與未批准的範圍、需要的來源證據及停止條件；當快照缺失、過期或衝突時，能拒絕依賴未確認現況的施工。

<a id="section-2"></a>
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

<a id="section-3"></a>
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
