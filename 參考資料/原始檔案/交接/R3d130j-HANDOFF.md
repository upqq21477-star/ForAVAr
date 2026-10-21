# R3d130j｜P1 交接（2026-10-16）

STORE_KEY: R3d130j-OVERLAP-RULES-W0

**一句話：R3d130j：W0 部分完成——全功能重疊比對（規劃 §9）與規則分類（§10）：階段／閉環骨架有 5 套並存、15 個無引用無測試模組、多組蓋好未接；常設規則被當成本場條件手抄（「進度百分比」整個遺漏）。本場無新程式。下一場 R3d130k：W0 剩餘閱讀 → W1。**

## 1. 接力規則（照做；工具每場自動帶入）

只需要本文件與附件 zip；舊企劃、舊交接都不用讀。本章每場自動帶入，固定不改。

- **開工（1 次呼叫）：** 解壓 → `python3 tools/pack_handoff.py --verify <zip> && python3 tools/session_start.py` → 只讀「下一批輸入」；批次卡用 `python3 tools/slice.py docs/plans/P2-Relay-Update-Plan.md --heading "### R6"`。大檔一律 slice，不整檔讀。
- **預算：** 讀 ≤ 48 KB、寫 ≤ 36 KB、呼叫 ≤ 30 次；任一到 70% 就停止開新任務、進入收尾。
- **場次與驗證（使用者 2026-10-16 定）：** ① 題組依複雜度配對（規劃稿 `## 19.`），高搭低、各場總分接近，一場一次跑完，取 §19 的下一個場次組合 ② 驗證只留最低需求，不為「多驗一次」加步驟 ③ 所有測試一律用模擬運行（標 SIMULATED_PASS），R9 之前不跑真實依賴、不要求使用者實測 ④ 全部題組與施工完成後，才做一次整體實測（R9）。
- **做法：** 照「下一批輸入」的 MUST 順序做；需裁決就採其中的預設方向、一行記理由，不停下來問；同一問題試 2 次仍失敗＝寫 BLOCKER（假說標 HYPOTHESIS）並換題。
- **守則：** 測試期望不改（必改須寫原期望為何錯）；有實跑才說完成；模擬一律標 SIMULATED_PASS；`canonical/`、`schemas/`、`P1-CURRENT.json` 不動（卡片明載除外）。
- **既有優先（使用者 2026-10-16 定）：** 新增、修改、規劃、新建系統前，先找出原有流程並比對覆蓋度，決定 REUSE／MODIFY／MERGE／NEW；NEW 須寫明每個既有候選為何不能改；先更新規劃再施工，不得直接堆疊新模組（見規劃 §8）。
- **四階段（系統基本能力，不必再提）：** 任何新功能、規劃、新系統一律走 F30 四階段：①藍圖（大綱每節點有重點、待辦排序）②能運行（每功能有入口與退出碼 0）③閉環（被呼叫、結束、退場、蒸餾成程式）④實際運行（無證據標 NOT_EXECUTED）；階段未完成不得說完成。通用化進行中，見規劃 §8。
- **證據標記：** PROGRAM_EXECUTED_PASS／SIMULATED_PASS／PATCHED_UNVERIFIED／NOT_EXECUTED／HYPOTHESIS。
- **收尾（1 次呼叫，最低需求）：** 先覆寫好 `handoff.data.json`，再 `python3 tools/close_session.py <ID>`。預設只跑 render → precheck → 重封 → 打包；改過 .py 加 `--code`（多跑 run-tests）；動到登記表或要整體驗收才加 `--full`（再加 batch_gate、驗證、解壓副本 rebuild_check）。只交付 `P2-relay-<ID>.zip` 與 `<ID>-HANDOFF.md`。已結案內容一行蒸餾進 `docs/handoffs/LEDGER.md`（≤ 10 KB）。
- **交接寫法：** 交接檔只放「下一場要做什麼」；已裁決內容、歷史、未知清單放規劃稿或 LEDGER，用 `slice.py` 按需讀。複製現有 `handoff.data.json`，只改 headline／狀態摘要／任務表／證據／變更檔案／下一批輸入／啟動提示詞；必備章節不變。目標 6～8 KB（上限 12,000 B）。無 Python 時只做 DOC_ONLY。


## 2. 系統主軸（自動帶入；來源 docs/architecture/P2-Axis-v0.1.md）

P2 是通用 AI 工程大腦：理解目標、研究未知、選擇方法與能力、組建工程工作群、建造或修補系統，並在有限上下文下檢查結果。（藍圖 §1）（索引，非規範；細節以藍圖為準，每場自動帶入，開工不需另讀。）

```bash
P2 AI 工程大腦
├─ 4.0 主核心：自我判斷、運行模式選擇與適應
├─ 4.1 Brain：理解與決策
│   ├─ 使用者意圖理解與最小化澄清（P2-F24）
│   └─ 系統性變更分類、職權路由與藍圖演進（P2-F28）
├─ 4.2 Central：機械協調
├─ 4.3 Role 與臨時工程工作群
├─ 4.4 Current State 與執行事實
├─ 4.5 能力與知識
├─ 4.6 System Factory：建立與重建系統
├─ 4.7 Assurance：檢查與驗收
└─ 4.8 Batch Phase Orchestrator（P2-F30）
```

怎麼連：使用者目標 → 讀 Current 與必要藍圖 → Brain 理解並選方案 → 定義交接契約與有界 Work Unit → 臨時工作群施工 → 獨立驗收 → 更新唯一 Current → 蒸餾可重用結論


## 3. 狀態摘要

**狀態（R3d130j 收尾）：** 依使用者要求「檢查其他新增功能是否同樣重疊、比對全功能、檢查規則是否誤判為暫時條件」，掃描 182 個模組並盤點規則，結果寫入規劃 §9、§10，並修正 §8（兩套八步閉環須合併、新增 W7 常設規則單一來源、W8 小工具合併）。沒有改任何程式。


## 4. 任務表

| ID | 級別 | 狀態 | 結果 |
|---|---|---|---|
| R1～R8、Q1～Q8b、S1～S6、S7 批 a、R3d130c／d／e | M／S | DONE | 登記表 40/40；固定依賴下未驗 |
| 退場機制接進結案（退場閘門＋預算只降不升） | S | DONE | `exit_steps` 於 close_session；先紅後綠；SIMULATED_PASS |
| 查明原有新增功能流程並更新規劃（規劃 §8、接力規則加「既有優先」） | S | DONE | 文件＋規則文字；DOC_ONLY；沒有新程式 |
| 全功能重疊比對（§9）與規則分類（§10） | S | DONE | 文件；DOC_ONLY；§9.3 列出 W0 剩餘閱讀 |
| feature_lifecycle 檢查器＋p2_run BUILD 觸發（R3d130g／h） | M | PARTIAL | 與 F30 重複；W3 併入節點內容檢查後移除，併入前不再擴充 |
| W0 剩餘閱讀（§9.3）→ W1 防再發（含規則轉功能）→ W2 F30 通用化 → W3 PLANNING 出口 → W4 CLOSURE（合併兩套八步）→ W5 進件與執行接線 → W6 實跑（R9）→ W7 常設規則單一來源 → W8 小工具合併 | M | NOT_STARTED | R3d130k 起；詳規劃 §8.3、§9、§10 |
| 退場補強：①兩套預算對齊 ②2 個孤兒 schema 登入 `lifecycle.v1.0.json` declared_entries ③p2_run.close 的 LIFECYCLE 步實際清理 | S | NOT_STARTED | R3d130g 第一項；詳 §8 |
| progress/ 瘦身批 | M | NOT_STARTED | R3d130g 第二項；9 測試＋5 腳本讀 progress/，須先查欄位 |
| docs/plans 合併蒸餾（單一計畫＋目錄索引） | M | NOT_STARTED | R3d130g 第三項 |
| 施工 S7 批 b、S7 收口 | M | NOT_STARTED | 設計見 §8；批 b 的暫存須遵守退場規則 |
| S3b⑤ operating_mode 狀態檔 | S | PARTIAL | 等 Q4 評估器 |
| R9 前置延後項與 R9 整體實測 | — | NOT_STARTED | 延後項 SKIPPED；R9＝使用者一次真實測試 |


## 5. 證據

- **掃描（PROGRAM_EXECUTED，AST 掃描，只讀）：** 182 模組；名稱叢集（gate 15、execution 10、audit 8…）；無引用無測試 15 個；`canonical_json` 12 處、`content_hash` 13 處、原子寫入 14 處（12 個匯入共用模組）。
- **讀檔頭與函式名（HYPOTHESIS：邏輯未逐行驗證）：** 各重疊組的判定見規劃 §9.1；兩套八步閉環與五套階段骨架來自讀 `closure_chain`、`construction_lifecycle`、F30。
- **規則強制檢查：** 在 tools/ 與 scripts/ 搜尋，找不到「不動鎖定檔」「測試期望不改」「進度百分比」的機械檢查（可能有漏，W1 先確認）。
- **未驗：** §9.3 六項。


## 6. 變更檔案

- 修改：`docs/plans/P2-Relay-Update-Plan.md`（新增 §9、§10；修正 §8.2 閉環列；§8.3 加 W7、W8）、LEDGER、本交接。
- 未動：所有程式、canonical／schemas／P1-CURRENT.json、測試。


## 7. 阻塞與未知

- **可推翻決策（沒回覆＝我決定）：** D-R3d130j-SSOT：常設規則一律由程式從單一來源產生，不放手寫的本場文字；D-R3d130j-HELPERS：`canonical_json` 等小工具合併延後（輸出格式未必相同，須逐一驗證）；D-R3d130j-ORPHAN：無引用無測試模組先判斷接線或退場，不直接刪（交 `lifecycle_sweep`）。
- **風險／未知：** 重疊判定多依檔頭與函式名；§9.3 讀完前不要據此刪除或合併任何模組。`declared_entries` review_after 2026-11-08 到期風險、progress/ 讀取者問題沿用 R3d130f。
- **遺留：** 沿用 R3d130e 的 UNKNOWN／R9 清單。


## 8. 下一批輸入

下一場 ID：**R3d130k。** 先完成規劃 §9.3 的 W0 剩餘閱讀並把結論寫回 §9，再依 §8.3 做 W1～W8。

- **W0 剩餘：** 用 `python3 tools/slice.py docs/plans/P2-Relay-Update-Plan.md --heading "## 9."` 讀 §9；依 §9.3 六項逐一讀並回寫判定。
- **W1：** 先看 `precheck`／`caller_audit`／`workflow_audit` 能否承載：新增 .py 須附比對紀錄、鎖定檔與前一版雜湊比對、測試斷言變動須附理由、交接「紅證據」欄；優先併入既有。
- **W2～W8：** 見規劃 §8.3；W2 動 `schemas/` 前先問使用者；既有測試期望不改。
- **固定做法：** 每個新增或修改前先寫比對（REUSE／MODIFY／MERGE／NEW）；收尾 `close_session.py R3d130k --code`；測試用 `python3 -B -m unittest`。


> **來源位置更新（2026-10-21；後加註記，不改寫下方原始交接提示詞）：** 封包 A 原始 ZIP 目前由 [P2 main 唯讀來源](https://github.com/upqq21477-star/P2/blob/main/%E5%8F%83%E8%80%83%E8%B3%87%E6%96%99/P2-relay-R3d130j.zip) 提供；forAVAr 本地二進位副本已依 EVT-0028 退場。若依下方提示詞開啟新會話，請先從上述來源取得 ZIP 並作為附件提供；本檔內原先的附件要求與工具命令是交接當時的內容，實際可用成員及工具仍需以封包內容核對。

## 9. 啟動提示詞

新對話貼下面這段，並附 `P2-relay-R3d130j.zip` 與 `R3d130j-HANDOFF.md`（規程都在壓縮檔內）：

```bash
你是 P2 接力「施工」工作者。附件：P2-relay-R3d130j.zip、R3d130j-HANDOFF.md。本場 ID：R3d130k。
開工（1 次呼叫）：解壓 → python3 tools/pack_handoff.py --verify <zip> && python3 tools/session_start.py（不要讀 README）；確認 zip、交接檔、本場 ID 相符，不符先說。
本場依交接 §8 與規劃 §8、§9、§10 做：先完成 W0 剩餘閱讀，再依 W1～W8 順序；先盤點（只讀）、寫比對結論，再動手；任何新增前先比對既有（REUSE／MODIFY／MERGE／NEW）；開工先 grep 既有工具再決定是否新造。閉環條件：有正常呼叫（啟動）條件、有正確結束（關閉）條件、能順利運行（含運作到一半中斷、運作到一半出錯的處理）。
守則：canonical/、schemas/、P1-CURRENT.json 不動；測試期望不改；先紅後綠要先看到紅；測試一律模擬（SIMULATED_PASS）；有實跑才說完成。預算讀≤48KB／寫≤36KB／呼叫≤30，到 70% 停止並收尾。
收尾（1 次呼叫）：python3 tools/close_session.py R3d130k --code；只交付 P2-relay-R3d130k.zip 與 R3d130k-HANDOFF.md。
決策：我沒回覆＝你自己決定；可查外部資料、借鏡原理，判斷最優解。
```


## 10. 收尾檢核

進度：登記表 40/40 任務 DONE（100%）；規劃 §8 新增工作 W0～W8：W0 部分完成，其餘未開始（0/8）。- [x] R3d130c～i；- [x] 重疊比對與規則分類（R3d130j）；- [ ] W0 剩餘；- [ ] W1～W8；- [ ] 退場補強；- [ ] progress/ 瘦身；- [ ] docs/plans 合併；- [ ] S7 批 b／收口；- [ ] R9 整體實測。
