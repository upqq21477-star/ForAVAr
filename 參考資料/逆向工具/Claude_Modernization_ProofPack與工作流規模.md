# Claude Code Modernization 研究分支｜Proof Pack、輸出比較器與工作流規模

- 文件 ID：FORAVAR-CLAUDE-MOD-BR-004
- 類型：BRANCH
- 狀態：CURRENT／外部專案靜態逆向分析；非實機／Runtime 驗收
- 唯一責任：保存原報告中 12–14 節的完整細節、來源和限制。
- 主軸回鏈：[Claude Code Modernization 逆向分析主軸](./Claude_Code_Modernization_完整逆向分析.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [12. Proof Pack 的更深一層逆向：它如何避免被「看起來像證據」的內容騙過](#section-1)
- [13. 輸出比較器的具體保護與限制](#section-2)
- [14. 大型工作流的續作、確定性與規模控制](#section-3)

---

<a id="section-1"></a>
## 12. Proof Pack 的更深一層逆向：它如何避免被「看起來像證據」的內容騙過

檢查 `scripts/proof_pack.py`、`scripts/compare.py`、`scripts/trace_rules.py` 及其測試後，可以將驗證管線拆成以下步驟：

```text
讀取證據檔
  ├─ 僅接受一般檔案
  ├─ 拒絕符號連結與超出工作區的路徑
  ├─ 拒絕超出大小上限、格式錯誤或無法解析的內容
  └─ 對每種輸入記錄缺失、衝突或過期狀態
       ↓
解析測試報告與原始 runner 紀錄
  ├─ 判斷是否真的執行
  ├─ 解析通過、失敗、跳過與個別測試狀態
  └─ 對比程式修改時間，排除舊報告冒充新結果
       ↓
重新計算規則追蹤、行為等價、新輸入與 canary
       ↓
Uplift 額外檢查：基線是否量測、測試是否保留、靜默行為差異是否有測試
       ↓
由固定規則重新計算每個模組的狀態
       ↓
寫出 VERIFICATION.json 與 VERIFICATION.md
```

### 12.1 驗收器拒絕哪些「假證據」

從 `proof_pack.py` 的讀取與檢查函式，以及 `scripts/tests/test_proof_tools.py` 的測試案例，可以確認它特別處理：

- 只有手填測試數字、沒有可解析測試結果或原始日誌。
- 結果檔早於最新程式碼，或留下了舊的測試報告。
- 測試被 skip、pending，或根本沒有執行。
- `VERIFICATION.json` 被人手動修改成較好的判定；下一次計算要回到原始證據重新判斷。
- 規則只出現在報告摘要、轉換備註或未執行的測試中。
- 比對案例不存在、輸出檔缺失、舊新輸出不同，或聲稱有新輸入但實際重複了原本的輸入。
- canary 只在文字註記中宣稱測試失敗，卻沒有自己的測試結果檔或可解析日誌佐證。
- 惡意或損壞的 JSON、XML、日誌、大型檔案、連結及工作區外路徑。

這些限制不是文件上的承諾而已；測試套件包含針對「手填數字不算」、「舊報告不算」、「手改判定不能保留」、「工作區外連結不讀取」等情境的專門測試。

### 12.2 判定條件其實不是所有策略完全相同

`proof_pack.py` 定義六個通用驗證檢查：測試確實執行、規則追蹤、相同行為、新輸入、canary，以及來源未被改動。Uplift 另外加入三個檢查：基線量測、舊測試保留程度、版本差異目錄覆蓋情況。因此 Uplift 的最高判定需要通過九項，而不只是六項。

Uplift 的三項特殊檢查進一步降低「升級後舊測試變少，結果卻更綠」的風險：

- 逐檔對照舊測試與工作副本的測試檔案，將刪除測試或超過四分之一的舊測試檔被修改列為缺口。
- 檢查標為 Behavioral-silent 的版本差異是否被測試檔提及；沒有測試提及時，列出缺口。
- 若差異發生於建置或設定檔這類測試本身不容易直接提及的位置，列給人審查而非假稱已覆蓋。

**限制必須一起記錄：** 這個 uplift 檢查能辨認測試檔有無改動，但原始碼說明它無法單靠檔案差異判斷 assertion 是否被弱化；「測試檔提及某個 delta」也不等於測試一定充分執行了該行為。

### 12.3 規則追蹤仍是啟發式，不是語意證明

`trace_rules.py` 會將規則 ID（例如 `RULE-017`）與原始程式、測試檔及測試結果連接。它判讀：

- `tested`：有實際執行且通過的測試證據支持規則。
- `named, not run`：測試提到規則，但沒有執行成功的證據。
- `code only`：只在主程式找到提及。
- `claimed only`：只在轉換／升級備註提及。
- `none`：沒有找到相關引用。

但此處的規則 ID 關聯是以測試命名、識別符與測試結果為依據；它不是完整的語意分析，也不等同於 branch coverage、mutation score 或形式化驗證。因此，P2 可以移植「證據等級與追溯表」，但若要宣稱測試真的覆蓋到某條核心規則，仍應搭配 assertion 檢查、覆蓋率或 mutation testing 等獨立方法，按專案需要選用。

原始碼：
- [proof_pack.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/proof_pack.py)
- [trace_rules.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/trace_rules.py)
- [Proof Pack 測試](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/tests/test_proof_tools.py)

<a id="section-2"></a>
## 13. 輸出比較器的具體保護與限制

`scripts/compare.py` 的比較基準是輸出檔案的實際位元組，不是模型對輸出的文字評語。其輸入案例可指定舊程式輸出、新程式輸出、遮罩、容差及人工批准的差異理由。

### 13.1 路徑與資源邊界

- 預設輸入輸出路徑必須留在案例檔所在資料夾；只有明確的 `--allow-outside` 才放寬。
- 缺失、無法讀取或超出允許範圍的檔案會被標示為 missing，不會當成相等。
- 原始碼為普通檔案讀取及輸出寫入設定大小限制，避免無上限讀取大型或惡意輸出。
- 它會執行比較器自身的自我檢查：刻意改動一個輸出位元組，確認該修改會被偵測為差異。
- 遮罩範圍會替換成固定標記，避免只靠變動長度遮罩掩蓋後續差異的位置。

### 13.2 數值容差的設計

數值容差需要給定理由；預設允許的誤差幅度有上限。比較器只對符合其數字格式規則的數值套用容差，整數和一般文字仍要求一致，像版本號或 IP 類的多段數字也不會一概當成浮點數。比對結果會記錄使用了哪些容差與遮罩。

這種設計適用於編譯器或數學函式庫引入末位浮點差異的案例，但**不適合用過大的容差來掩蓋實際業務變更**。當 P2 引入通用輸出比對時，也應要求每一個遮罩／容差都有說明與審批記錄，並為可遮罩區段設定最大範圍。

來源：[compare.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3)

<a id="section-3"></a>
## 14. 大型工作流的續作、確定性與規模控制

### 14.1 分塊不是單純拆檔

`modernize-map` 對超過約 2,000 個來源檔或 500,000 行的系統，要求按 domain 或頂層目錄分塊，將每個 chunk 寫成獨立 JSON；重新執行時可以跳過已完成的 chunk，最後合併為總拓撲。仍未完成或跨 chunk 無法解析的邊應被明確列出，不能假稱整張圖完整。

它也明確要求優先使用語言生態已有的機器可讀圖譜，例如 Java 的 `jdeps`、.NET 的 project graph、JavaScript 的依賴分析工具、Python 的依賴圖，以及 Go／Rust 的套件圖；再人工抽查部分邊，並補上外部設定、入口、資料庫與業務流程等一般工具容易漏掉的關係。

這是重要的工具使用原則：**先重用可信既有的結構化輸出，再補缺口；不要為了看起來自動化，重新打造已存在的分析工具。**

### 14.2 可續作工作流需要固定呼叫順序

業務規則工作流記錄工作日誌，並要求同一組輸入重播時，代理的 spawn 順序也可預測。原因是完成代理結果能被重播利用；如果流程依代理完成時間決定下一步，重跑順序會變，已完成結果便較難重用。

Uplift 工作流以相依關係分批，並在擴大下一批之前檢查前一批成功率。這裡的關鍵不是「重試多少次」，而是把結果分類為可重跑的不同集合：

- 未嘗試的單元。
- 已嘗試但建置失敗的單元。
- 因依賴失敗而被阻擋的單元。

三類清單可重新輸入工作流，避免將錯誤擴散到整個任務。

### 14.3 可移植到 P2 的協調契約

如果 P2 要借鑑此方法，工作單元至少要有下列欄位：

| 欄位 | 用途 |
|---|---|
| `unit_id`、版本與來源 | 穩定識別本次工作 |
| `inputs`、`outputs` | 固定輸入與產出契約 |
| `depends_on` | 定義先後關係與批次可執行性 |
| `read_scope`、`write_scope` | 限制代理可讀、可寫的位置 |
| `attempt`、`state`、`failure_class` | 管理失敗、重跑與退場 |
| `evidence_refs` | 指向真實測試或其他可重算的證據 |
| `exit_criteria` | 明定什麼條件能結束，不能由代理臨時改標準 |

這是根據外掛的流程機制所做的設計建議，不代表 P2 目前沒有相同欄位。正式施工前仍須比對 P2 的既有 schema、呼叫者與 lifecycle 能力，優先 REUSE／MODIFY／MERGE。

來源：
- [modernize-map.md](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-map.md)
- [extract-rules.js](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/workflows/extract-rules.js)
- [uplift-migrate.js](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/workflows/uplift-migrate.js)
