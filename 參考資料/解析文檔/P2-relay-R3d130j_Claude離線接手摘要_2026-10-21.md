# P2 R3d130j｜Claude 離線接手摘要（2026-10-21）

> 主軸回鏈：[State Bundle｜主軸彙整](../StateBundle_主軸彙整.md) ｜ 分支 ID：STATE-BR-004 ｜ 本回鏈只提供導航，不改變本文件的證據邊界。

> **用途：** 在 Claude 無法即時讀取 GitHub 時提供最低必要上下文，避免只依初始藍圖推測目前狀態。
>
> **重要狀態：CONFLICT。** 這是從使用者提供的 ZIP 建立的離線快照。它可用於只讀分析、根因診斷與引用核對，不可當作當前 GitHub HEAD 的證明，也不授權修改 P2。

## 1. 來源身分

- 原始檔：`P2-relay-R3d130j.zip`
- SHA-256：`f38cc51fcd443500d63e5693bd2946dfd099ee03e57bb105c9e7d86cf96cb521`
- Git Blob SHA-1：`0e58526bd35c30a25f3b27033a4952ec5f25bf10`
- ZIP 項目：774；展開大小：5,479,985 bytes
- 內附 `MANIFEST.sha256`：773 筆成員雜湊，773/773 全數通過
- 來源說明：使用者指定此 ZIP 為目前最新可得 P2 快照；本摘要不能獨立證明它等於 GitHub 所有分支中的最新 Commit。封包未提供可確認的當前 branch／HEAD SHA。

## 2. P2 核心目的與權威規則

P2 藍圖 `docs/architecture/P2-System-Blueprint-v1.0.md` 的實際標題為「P2 系統總體藍圖 v4.0」，狀態標示 `P2_TARGET_BLUEPRINT / DESIGN ONLY`。目的：理解目標、研究未知、選擇方法與能力、組建工程工作群、建造或修補系統，並在有限上下文下檢查結果。

權威規則：

1. `P1-CURRENT.json` 是唯一執行狀態來源。
2. `P1-CURRENT.json` 的 `p2_target_blueprint_ref` 才是 P2 目標施工藍圖指標；泛用 `blueprint` 欄位不能與它混用。
3. Active Work／Construction 定義本工作單元的範圍和接受條件。
4. Feature Batch 定義凍結的功能／案例範圍。
5. HANDOFF、README、索引、研究文件是交接或派生視圖；不可因內容較長、日期較新或語氣較肯定就替代 Current。
6. 任何檔案存在、程式碼存在、靜態檢查、歷史測試、當前 HEAD 測試與 Runtime 都是不同證據層級。

## 3. 快照中的當前執行狀態

- Current：`P1-CURRENT.json`
- Current SHA-256：`f06384fbb5a1e9ae0a2cabc75d1d89dad9ef29ea5f2d5f61db4e902b72804c49`
- Current stage：`P2-B1-B8-CODE-FIRST` / `IN_PROGRESS`
- Active Work：`P1-Central-Control/progress/P2-B1-B8.work.json`
- Active Work SHA-256：`21715e57f852b93581ff6b1b9bb4ec3ac4220abe70aac1b144dc3691142ed99e`
- Construction：`P1-Central-Control/progress/construction/P2-B1-B8.construction.json` / `BUILDING`
- Feature Batch：`P1-Central-Control/progress/P2-B1-B8.feature-batch.json`
- Feature Batch SHA-256：`11926cd9883ea5b523026e95cc05394f9c8a14540ffff2ba8e26fc634dcde883`
- Feature Batch：30 項，`REALIZATION`，`scope_frozen=true`；`official_test_scope_status=INCOMPLETE_FOR_BATCH`；`official_test_roster=[]`
- 局部案例：90 個（NORMAL／NEGATIVE／BOUNDARY 各 30）；90 個全部 `NOT_RUN`；33 個已有 `test_method` 綁定，57 個 `test_method=null`
- 工作結果：`code_status=IMPLEMENTED_UNVERIFIED`、`python_tests=NOT_EXECUTED`、`formal_caller=UNKNOWN`、`active_pack=NOT_GENERATED`、`runtime_truth=INCOMPLETE`

Current／Active Work 文件寫的下一項操作是：在已核准、Python 3.11 且不產生額外費用的環境執行 `python P1-Central-Control/tests/test_construction_progress_watchdog.py`，保存真實輸出、退出碼、HEAD 和 source hash；之後跑已綁定的六個 F28/F30 局部案例。若沒有符合條件的環境，維持 `NOT_EXECUTED/NOT_RUN`，不要使用未知成本環境或 archived Actions，不得提前進入 CLOSURE／FINAL_TEST。

**但本離線摘要的整體狀態為 CONFLICT，不能作為執行 P2 寫入／測試的授權。** 上述只是快照中的工作包要求；必須先確認可讀取的最新權威來源與執行環境。

## 4. 已核實的權威視圖衝突

1. `P1-CURRENT.json` 和 Active Work 指向 B1–B8 的 `IN_PROGRESS`；`docs/handoffs/handoff.data.json`／`HANDOFF.md` 卻仍標示 R3d130j，下一步寫成 R3d130k 的 W0／W1–W8。
2. 根目錄 `README.md` 的 Current 投影明示與 Current 衝突時以 Current 為準，但另一段凍結舊投影仍稱 HANDOFF 是進度／下一步的唯一權威。
3. `docs/README.md` 對 `docs/plans/P2-Relay-Update-Plan.md` 同時標記為「舊工作順序、已被取代」與「唯一企劃」。
4. `docs/audit/OPEN-ISSUES.md` 的 002c 已追蹤 Current、README、HANDOFF 與 M32／M33／B1–B8 工作記錄的狀態、HEAD SHA 和下一步是否互相矛盾。

不要把這些內容硬合併成新敘事，也不要建立第二份 Current。先依每份資料的唯一責任，將衝突列出並核對源檔版本。

## 5. 已核實的路徑引用缺口

- **REF-01：** Current／Work／Feature Batch 中 F15／F16 引用 `P1-Central-Control/tests/test_ai_github_baseline_cycle.py`，該路徑不存在於此 ZIP。尚不確定是漏包、移位或過期引用。
- **REF-02：** F27 引用的 `P1-Central-Control/scripts/presentation_selector.py` 及 `P1-Central-Control/tests/test_presentation_selector.py` 實際位於 `P1-Central-Control/archive/f27-presentation/`。在核對封存原因及活動 caller 前，不可只改路徑就當作有效接線。
- **REF-03：** `docs/plans/P2-Code-First-Execution-and-Distilled-Operational-Pack-v1.0.md` 指向不存在的 `P2-Test-Strategy-and-Free-Execution-Paths-v1.0.md`。需查其他來源或歷史，不能自行補寫不存在內容。

這些是封包內部的引用問題；不是證明原始 ZIP 的成員漏載，因所有 774 個成員都已清冊化，773 筆 manifest 雜湊全數通過。

## 6. 本次允許／禁止的工作

**可做：**
- 只讀分析、根因診斷、引用核對、狀態包格式與反例測試設計。
- 將每個發現標為 `OBSERVED`、`INFERENCE`、`HYPOTHESIS`、`UNKNOWN`、`CONFLICT` 或 `BLOCKED`，並保留檔案路徑及 SHA。
- 若無法查證最新 HEAD，明確說明離線快照限制。

**禁止：**
- 修改 P1 或 P2；此摘要不提供任何寫入授權。
- 宣稱 P2 的程式、測試、Runtime 已通過。
- 將歷史測試視為目前 HEAD 的收據。
- 修改凍結的 F01–F30／90 案例範圍，或自行增添常設能力。
- 將 HANDOFF 當作 Current 的替代品。
- 在找不到必要檔案時猜測其內容。

## 7. 延續工作的第一步

第一步不是立刻施工，而是處理權威與上下文：

1. 先讀本摘要及其來源指紋。
2. 有 repository 存取時，重新取得並比對 `P1-CURRENT.json`、Active Work、Feature Batch、Construction、目標藍圖、HANDOFF、README、`docs/README.md` 及 `OPEN-ISSUES.md` 002c。
3. 無 repository 存取時，只能依此封存快照完成只讀分析；把未解來源標成 UNKNOWN／CONFLICT。
4. 查明 REF-01／02／03 是缺包、移位、已退場或失效引用，再提出最小差異建議；在授權及證據不足時不要修改 P2。
5. 所有局部修補都必須能追溯到原始目標、問題 ID、核心不變量、接受條件及實際測試證據。若不能說明這條鏈，先將候選留在待辦，不把它變成永久架構。

## 8. forAVAr 中的研究紀錄

- 問題登錄：`參考資料/(S級)問題清單.md`，PR-052（A 級、OPEN）
- 根因樹與權威映射：`參考資料/解析文檔/P2核心漂移_根因分解與下一步權威狀態核對_2026-10-21.md`
- State Bundle 契約：`參考資料/解析文檔/可攜式StateBundle最小資料契約與防漂移反例驗收草案_v0.1.md`（PROPOSAL／NOT_IMPLEMENTED）
- 完整封包及防偏離分析：`參考資料/解析文檔/P2核心主軸漂移根因與forAVAr防偏離架構驗證_2026-10-21.md`

以上路徑是 forAVAr 中的追蹤入口；本檔案本身保留必要摘要，供無 GitHub 連線的 AI 使用。所有 forAVAr 研究文件都不是修改 P2 的授權。
