# B23.4 forAVAr 交接（梯次二 REALIZATION・段4 完成；STORE_KEY＝B23.4）

輸入：ForAVAr-main_B23_2.zip／輸出：ForAVAr-main_B23_4.zip（9e9ffe70350bb7d3）＋foravab_B23_4.zip（a8b5543172968468）＋本檔
回復點：ForAVAr-main_B23_2.zip／B1–B23.4 尚未推上 GitHub／本檔不放進 repo

## 接手規則（照做，不必提問）
1. 一批＝一個梯次；梯次內依段推進，斷點記在本檔；不跳梯次。真實運行延到 B25。
2. 直接開工。不整檔讀 `docs/progress_ledger.json`（約 110KB）；用 `python tools/ledger_query.py --todo | ID… | --status X | --realize R3`。批末才跑一次 `python tools/standard_verify.py`。
3. 疑義依藍圖核心（L1 不變量、A1–A6、N01–N18、F0–F7）自裁並記錄於本檔。
4. 放行只用 `python tools/stage_gate.py STAGE STATUS --batch Bxx --reviewer … --evidence …`，不手改 ledger 的 stage_gates。
5. 資料分離：主 repo 只放程式／測試／權威文件；實驗與已解資料放 `foravab_B<批號>.zip`（含 MANIFEST.md，只留下次會用的，用不到的刪除並留一行紀錄）。
6. 交付固定：本檔＋整體主 zip＋參考資料 zip。未達 SYSTEM_DONE 不得寫「建置完成」。
7. 免費帳號：每次只做一至兩段，上下文不足就在本檔記斷點交付。

## 本次完成（standard_verify OK；260 項測試通過；check_consistency 0 錯 0 資訊）
- **R5**：registry 與 problem_register 每項 `ledger_ref` 皆須指向 ledger 實際 id（check_consistency 驗證；problem_register 54 項補齊）。`tools/coverage.py` 層級／機制／備註全改讀 ledger，手寫 PROBLEMS／FUNCTIONS／FLOWS 退役，只留 `MECH`＋`PROCESS_FLOWS`（12 列 TASKFLOW／STAGE）。PR-034 雙軌結束。
- **R4** `runtime/frame_gate.py`（N02／N03）：邊界、排除理由、依賴宣告；高影響未知依賴必須列入 unknowns；高風險或 governance≥G2 須 ≥2 競爭框架＋採用理由。違規＝高風險／有副作用／G≥2 回 BLOCKED，否則 NOT_PROVEN。**選用**：`task.profile.frame_gate: true` 才啟用（既有行為不變）。N02／N03 → CONTRACT_TESTED。
- **R3-model** `runtime/model_gate.py`（N07–N09）：元素／關係／條件／未知齊備（空者須 `omitted_basis`）；EVIDENCED 關係須引用 OBSERVED 證據，否則標 HYPOTHESIS；≥2 競爭假說且 discriminating_test 各異；模型不得自標 OBSERVED。**選用**：slice 在提供 `adapters["model"]` 時於 evidence gate 後、route 前執行。`adapters/model_adapter.py` 新增 model 階段模板／契約。28 項 P1 函式＋N07／N08 → CONTRACT_TESTED。
- slice 0.8.0（結果新增 `frame_gate`／`model`／`model_gate` 欄位）；`error_exits.STAGE_EVENT` 加 model（例外→ADAPTER_FAULT）。
- ledger `change_set` 壓縮為只記 B23 累計；藍圖 maturity 更新（frame_gate、model_gate、測試數）。
- 裁決：frame／model gate 採選用而非預設開啟，理由＝避免破壞既有契約與 fixtures；是否改預設開啟留 B24 依跨檔回歸決定。

## 下一段（B23 段5，最後一段）
**R3-synthesis**（N14–N15；P1-F39／F44／F47，`ledger_query --realize R3` 取）：
- 新增 `runtime/synthesis_gate.py`＋`tests/test_synthesis_gate.py`，比照 model_gate：純函式、fail-closed、選用接入 slice（提供 `adapters["synthesis"]` 時於 evaluate 後執行）。
- 規則：每條結論引用存在且 OBSERVED 的證據 id；未解項（unknowns／conflicts）必須攜帶進結論；信心與證據相稱（無 OBSERVED 證據者信心不得為 HIGH）；模型不得自稱 OBSERVED。違規＝高風險 BLOCKED，否則 NOT_PROVEN／降 PARTIAL（對齊 R8 做法）。
- 同步：`adapters/model_adapter.py` 加 synthesis 階段模板；`coverage.py` MECH 加 SGATE；README 列檔；ledger 把 P1-F39／F44／F47、N14（已 CONTRACT_TESTED，加 SGATE）、N15、A3 轉狀態；R3 progress→DONE；藍圖 maturity。
- 批末：跑一次 `standard_verify`，再 `stage_gate REALIZATION PASSED --batch B23`（自評，註明非獨立審查）。

## 後續批次
- B24＝CLOSURE：跨檔依賴、來源引用、狀態、封包、權限、restore_drill、回歸（用 foravab 的 closure_resolved）、索引、變更記錄、退場風險；決定 frame／model／synthesis gate 是否預設開啟；產出差異清冊、影響圖、已解／未解項。
- B25＝FINAL_TEST：凍結版本；真實運行 C0／C1／C2、A1–A4、獨立確認集；沿用 rubric 指紋 ece6a3b7ce587fb8／5eed467fa27fda63；補 timeout_unknown_side_effect 樣本；只有此梯次可升 ACCEPTED。
- 單一梯次失敗：下一批重做同梯次（retry_of），不跳梯次。

## 待辦
| # | 項目 | 歸屬 |
|---|---|---|
| 1 | B23 段5：R3-synthesis、standard_verify、REALIZATION 放行 | 接手者 |
| 2 | B24 CLOSURE、B25 FINAL_TEST | 接手者 |
| 3 | GitHub 推送（B1–B23.4 全未推；建議立刻推） | 擁有者 |
| 4 | 真實 adapter／模型與執行環境（B25 前；OD-1） | 擁有者 |
| 5 | 中途取消維持 DEFERRED（OD-4） | FINAL_TEST 後再議 |

## 已知取捨（B24 處理）
①evidence gate 對任何 OBSERVED 過期記錄在高風險／有副作用任務一律擋，未限縮到被引用者；②`loop.json` 存完整 last_result，長任務會變大；③release_txn 每筆交易需全新 snapshot 目錄，restore_drill 須涵蓋 `snap_dir/ckpt-NNNN`；④R3／R4 的 gate 只驗形式與可追溯，內容好壞與真實 adapter 效果＝NOT_VERIFIED。

## 殘留限制
內容偵測為關鍵字式；壓縮非語意；鎖為檔案鎖；SLOT 效果、真實 adapter／handler wiring、handoff 自動化、獨立驗證皆 NOT_VERIFIED；PLANNING 放行為自評（PR-022）。ledger／blueprint 經腳本重寫（indent=0），內容不變。
