# Claude Code Modernization 研究分支｜呈現層、官方案例與差距分析

- 文件 ID：FORAVAR-CLAUDE-MOD-BR-005
- 類型：BRANCH
- 狀態：CURRENT／外部專案靜態逆向分析；非實機／Runtime 驗收
- 唯一責任：保存原報告中 15–18 節的完整細節、來源和限制。
- 主軸回鏈：[Claude Code Modernization 逆向分析主軸](./Claude_Code_Modernization_完整逆向分析.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [15. 報告與即時面板：呈現層不等於治理層](#section-1)
- [16. 對官方案例的修正性解讀](#section-2)
- [17. 結合 forAVAr/P2 的深度差距分析](#section-3)
- [18. 本次追加研究的主要來源](#section-4)

---

<a id="section-1"></a>
## 15. 報告與即時面板：呈現層不等於治理層

### 15.1 單頁報告的安全實作

`scripts/build_report.py` 的文件說明指出：分析檔案可能來自不可信程式碼，因此報告不把檔案內容直接當成 HTML 執行，而是將內容作為經跳脫的 JSON、以 `textContent` 方式建立 DOM，並用 Content Security Policy 限制頁面允許執行的腳本與外部請求。報告也拒讀 `*.local.*`、`SECRETS*` 和透過符號連結抵達的檔案，並設單檔與總讀取量上限。

這讓離線報告不只是美觀 UI，而是具備基本的不可信資料輸出處理策略。不過，HTML 安全仍須依具體來源、瀏覽器與腳本變更做持續測試，不能僅因使用 CSP 就宣稱完全安全。

### 15.2 即時面板的權責很有限

外掛 hook README 對面板的非職責說明得很清楚：

- 它讀取分析目錄、新程式與驗證 JSON 來顯示狀態，不自行再呼叫模型。
- 它不會自動執行下一個命令；按鈕只是把命令放進提示欄，仍由人員確認與執行。
- 它不攔截、不改寫命令或檔案修改。
- 它本身不是權限沙盒；保護舊程式寫入範圍的是工作區權限設定。
- 它對升級差異的部分可視化比較以檔名與大小為基礎，同大小的內容修改可能不會被該視圖直接發現。
- live traffic diff、自動 fallback 及手機核准等能力並未實作完成。
- 即時面板使用的 function hooks 被官方標註為 early access，且需手動開啟；官方 README 記載其面板測試版本為 Claude Code 2.1.280，不能在沒有再查版本的前提下宣稱各版本均相容。

因此，面板只負責呈現「已存在的狀態」，並不構成流程完整性的證據。P2 若建立進度介面，應把它視為 Current 與驗收資料的唯讀投影；真正的安全限制、退場與阻擋規則必須在執行層實現。

來源：
- [build_report.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/build_report.py)
- [hooks/README.md](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/hooks/README.md)

<a id="section-2"></a>
## 16. 對官方案例的修正性解讀

官方列舉的案例同時包括通過與未通過的實例，因此不能只選擇成功案例評估效益。

| 觀察 | 證據支持的判斷 | 不能因此推論 |
|---|---|---|
| CardDemo 在多次驗證後，新增輸入仍找到多個差異，最終為 NOT PROVEN | 迭代測試與反例搜尋能繼續揭露隱藏行為差異；工具願意輸出負面判定 | 整個 COBOL 系統已成功等價改寫 |
| osCommerce 產品頁的某一切片通過獨立驗證 | 在可執行的舊程式、對照輸出及測試證據充分時，切片級等價驗證可成功 | 整個商城或其他業務頁面都已證明 |
| JPetStore 重建服務仍有新舊差異，驗證為 NOT PROVEN | 新架構即使有通過的測試，仍可能保留沒有被測試抓到的行為差異 | 重建只要測試數多就等於完成 |
| beets 因環境無法取得套件，測試無法執行 | 工具鏈和環境本身是驗收前置條件；不能把不可執行轉成成功 | 靜態分析能完全替代實際執行 |
| 官方 README 自述數字可因重跑而不同，且早期案例曾出現判讀缺陷 | 此工具仍是持續演進的工程產品；其驗證腳本也需要自身測試與修正 | 單一版本的宣傳數字是普遍、固定的效能保證 |

**這些案例的最大價值是顯示工具的失敗處理原則，而不是證明它能自動成功改寫任意軟體。**

<a id="section-3"></a>
## 17. 結合 forAVAr/P2 的深度差距分析

依本次已閱讀的 `R3d130j-HANDOFF.md`，forAVAr/P2 的既有交接原則已強調：新增之前先比對舊能力、常設規則應有單一來源、工作需要依生命週期閉環、模擬通過不得冒充實際執行。這些方向和 Modernization 的核心設計相似，因此實作策略應優先研究如何擴充既有機制。

| 項目 | Modernization 展示的具體做法 | forAVAr/P2 建議行動 | 目前可確認程度 |
|---|---|---|---|
| 能力重疊管理 | Map 與 Preflight 先利用已有圖譜及工具，再補缺口 | 先完成交接文件所列的 W0 剩餘重疊分析，再裁定 REUSE／MODIFY／MERGE／NEW | 交接文件有記載，尚不能由本次研究斷定現有程式都已實作 |
| 業務規則轉機器可檢查規則 | 規則卡、原始碼引用、獨立引用覆核、人工判定 | 為 P2 的常設規則建立單一權威來源與可驗證的消費者清單 | 可移植原理，需核對目前規則儲存與產生方式 |
| 工作閉環 | 前置輸入、階段產物、批准門、建置與驗證 | 把 F30 作為既有整合候選，不另創另一套同功能生命週期 | 交接文件明載 F30；實際接線須重新驗收 |
| 失敗後續作 | 依賴感知的批次、可重跑工作清單、工作日誌 | 在現有 Work Unit 與 Current 流程上核對失敗分類、重跑與退場是否閉合 | 需依 P2 schema／呼叫鏈核對 |
| 驗收證據 | 實際 runner 產物、等價性案例、canary 與獨立判定 | 保持 P2 的證據標記並增加可重算證據；不以文字狀態取代真實執行 | 可直接借鑑，仍需選定每種能力的證據來源 |
| UI／報告 | 報告讀取產物而不創造狀態 | 面板只呈現權威 Current，不另存第二份進度真相 | 移植原則；未對 P2 UI 做完整檢查 |

### 17.1 建議排序

1. **先收完 W0 盤點。** 交接文件明確指出部分重疊判斷依檔頭與函式名，並要求完成剩餘逐項閱讀前不要刪除或合併。不能因 Modernization 有相似機制，就直接新增同名模組。
2. **選一個小型工作單元作為試點。** 將輸入契約、可寫範圍、產物、證據與失敗退場全部寫清楚；不要一開始就啟動大規模平行代理。
3. **先驗證驗收器，後擴大施工。** 建立成功、失敗、缺證據與被依賴阻擋的案例，確認判定不會只信任人工填寫的狀態字串。
4. **在已有 Current／lifecycle 能力中做接線。** 若缺失的是呼叫關係、狀態轉移或機械驗收，就先補那個缺口，而非再造完整的新工作流系統。
5. **保留真實與模擬的語義區隔。** 只有程式或測試實際執行且保存證據，才能使用實際執行通過的狀態；模擬結果只代表模擬。

### 17.2 目前尚未完成的工作

- 尚未安裝、執行或量測外掛的 token／時間／成本；官方僅提供典型時間與代理數字，並提醒工作量因系統而異。
- 尚未對外掛執行完整動態安全檢測、效能基準或逐檔程式測試。
- 尚未掃描 P2 的全部程式、schema、呼叫者與測試；本次對 P2 的映射限於目前讀得的交接資料。
- 尚未將移植建議寫入 P2，且本專案的寫入邊界不允許這麼做；任何 P2 實作都必須在其相應施工專案中獨立進行。

---

<a id="section-4"></a>
## 18. 本次追加研究的主要來源

以下連結指向研究快照的具體實作或官方文件，供後續接手者直接核查：

1. [Proof Pack 判定器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/proof_pack.py)
2. [Proof Pack 自動化測試](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/tests/test_proof_tools.py)
3. [輸出等價比較器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/compare.py)
4. [業務規則測試追蹤器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/trace_rules.py)
5. [Uplift 專屬檢查器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/uplift_checks.py)
6. [離線報告建置器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/build_report.py)
7. [拓撲圖建立命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-map.md)
8. [面板權責與相容性說明](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/hooks/README.md)
9. [官方主 README](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/README.md)
10. [forAVAr 交接依據：R3d130j-HANDOFF.md](../原始檔案/交接/R3d130j-HANDOFF.md)

追加部分屬於源碼靜態分析；除非明確標註為官方 README 記錄的案例，本文沒有聲稱自行執行成功、效能提升或完整驗收。
