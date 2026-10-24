# forAVAr 交接 HANDOFF — B17（建置完成：feedback／intake 範本補齊）

task_id: FORAVAR-BUILD ／ 本檔不放進 forAVAr repo（可歸 forAVArb）
輸入：ForAVAr-main_B16.zip ＋ HANDOFF_B16.md ／ 輸出：ForAVAr-main_B17.zip（sha256 前 16 碼 909f94267638d853）＋ 本檔 ＋ COVERAGE_REPORT.md（工具產生，不入 repo）
基線 commit 460c0c7；B1–B17 **尚未推上 GitHub**
狀態：**建置完成，等待最終驗收**（blueprint maturity.build_scope＝BUILD_COMPLETE_PENDING_FINAL_ACCEPTANCE）。FINAL_TEST 尚未執行。

## ★ 待你處理
| # | 項目 | 建議 |
|---|---|---|
| 1 | GitHub 推送 | 現在推；驗收前先有可回復的遠端基線。 |
| 2 | DISC-SOP-001～007 裁決（見 HANDOFF_B13 §2） | 預設生效；有異議再說。 |

## 1. 本批完成
- **adapters/model_adapter.py 增兩個階段**（現共 6 階段）：
  - **feedback（N15）**：輸出 failure_branch／failure_class 必須在契約詞彙內；根因標 SUPPORTED 但沒有 evidence_ids → 降為 UNKNOWN；根因 UNKNOWN 時 rule_candidate 一律清為 null（PR-006、PR-011）。
  - **intake（P2-F12）**：決策限 ADOPT／REJECT／DEFER／MERGE／REPLACE；ADOPT 沒有「已測量」的基線比較（含 evidence_ids）→ 降為 DEFER（PR-037、PR-048）；有副作用的 ADOPT／REPLACE 強制 requires_authorization。
  - 兩者皆有 11 欄位宣告、提示範本（資料包進 UNTRUSTED_DATA）、make_adapter。
- 清冊：所有 SLOT（功能、流程、PR-049）都有 ADAPT 機制，GAP 0；層級仍是 SLOT（效果未驗證）。
- 本批更新以交易＋標準驗證套用，一次通過。
- 測試 131 項。

## 2. key decisions
1. 判定「建置完成」的依據：CODE 項目皆有測試；SLOT 皆有入口＋範本＋合約驗證；PROCESS 49 項依 B13 裁決維持流程；殘留限制皆已寫進 coverage note（內容偵測為關鍵字式、壓縮非語意、鎖為檔案鎖）。
2. 本批在交易前已就地改了 adapters/model_adapter.py 與其測試，所以交易快照的「前版」是修改後的檔案；本批回復點請用 B16 zip。

## 3. 實跑結果
`unittest discover` → Ran 131 tests OK（Python 3.12，沙盒）；`check_consistency.py` errors=0；`coverage.py` errors=[]，totals 54／121／44；CODE 問題 38／功能 42／流程 33；SLOT 功能 47／流程 9／問題 1；PROCESS 問題 15／功能 32／流程 2。
NOT_EXECUTED／NOT_VERIFIED：真實 adapter、真實 C0/C1/C2、SLOT 全部項目的實際效果、內容偵測誤報率。

## 4. 其餘欄位
- modified_paths：adapters/model_adapter.py、tests/test_model_adapter.py（+4）；tools/coverage.py；docs/blueprint.json（maturity：python_contract_tests、slot_adapter_pack、build_scope）。
- recovery：以 ForAVAr-main_B16.zip 回到本批起點。

## 5. 下一批（B18 = 最終驗收 FINAL_TEST）
- 依 tools/final_test_harness.py：rubric 指紋 ece6a3b7ce587fb8（執行前已固定，不得為了通過而改），C0／C1／C2 三條件、確定性樣本（expected_status 事先固定）。
- 做法：先以 reference adapter（C0）與 model_adapter＋可用模型（C1／C2）跑；**真實模型由我這個對話中的 Claude 代為產生輸出**，因此證據類別必須標為 CALLER_SUPPLIED／同一模型自評，不得標成獨立驗證（PR-008、PR-022）；結果只填入 maturity 與驗收報告，不為過關調整 rubric。
- 接手只讀本檔＋COVERAGE_REPORT.md＋tools/final_test_harness.py；批末只跑一次 `python tools/standard_verify.py`。
