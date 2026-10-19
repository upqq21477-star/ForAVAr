# Claude Code Modernization 逆向分析

> 研究日期：2026-10-19  
> 對象：Anthropic 官方公開倉庫 `anthropics/claude-plugins-official/plugins/code-modernization`  
> 源碼基準：`claude-plugins-official` 的 `main` 分支快照，commit `ea10b213686c90bb1984b2016937310e05336cf3`（commit 日期：2026-10-16），外掛 manifest 標示版本 `1.0.0`。  
> 研究方式：原始碼、命令文件、工作流、測試與官方說明的靜態逆向分析；本文件未安裝或實際執行該外掛。  
> 施工邊界：本次只新增 forAVAr 根目錄研究文件；不修改 README、不寫入 P1 或 P2。

## 0. 核心摘要

**Code Modernization 的主要技術價值，是把舊系統現代化變成「以產物交接、以關卡控制、以證據驗收」的工程流程，而不是把重構提示詞串在一起。**

可以從原始碼直接確認的設計：

1. 先檢查環境、盤點系統、繪製相依關係及抽取業務規則，再產生需人工批准的現代化計畫。
2. 三種改造路徑分開處理：同技術版本升級（uplift）、逐模組改寫（transform）、新架構重建（reimagine）。
3. 專業代理負責不同子任務；大規模工作流支援有序分批、引用覆核、相依約束、失敗分類與有限重跑。
4. 將驗證工作獨立出來，由 Python 腳本根據測試結果、輸出差異及其他證據計算判定，而非採信模型自己的「完成」聲明。
5. 產出可供不同工作階段與人員接續的檔案；另有離線單頁報告與可選的即時進度介面。
6. 文件也清楚列出無法完成的驗證情境，以及會被判為 `PARTLY PROVEN` 或 `NOT PROVEN` 的情況。

**對 forAVAr/P2 的建議：借鑑它的流程契約與獨立證據驗收，不要直接照搬整套外掛。** 對 P2 尤其重要的部分是：建立一項工作前先比對既有能力、限制各代理的寫入範圍、把真實執行與模擬執行分開，以及禁止由施工者單方面裁定驗收成功。

---

## 1. 研究對象與程式結構

### 1.1 身分及可觀察範圍

- 官方原始碼：[code-modernization 外掛目錄](https://github.com/anthropics/claude-plugins-official/tree/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization)
- 外掛 manifest：[plugin.json](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/.claude-plugin/plugin.json)
- 工作流程、驗證及命令定義在同一個外掛目錄中；不是只有 README 範例。

### 1.2 逆向還原的層次

| 層 | 原始碼位置 | 職責 |
|---|---|---|
| 入口與命令協定 | `commands/*.md` | 把每一步的輸入、前置條件、操作順序、產物與停止條件寫成可呼叫的命令 |
| 專業代理 | `agents/*.md` | 業務規則抽取、舊系統分析、架構批判、安全審核、測試工程、版本差異分析、遷移與服務骨架建立 |
| 多代理工作流 | `workflows/*.js` | 分批平行處理、依賴排序、二次覆核、失敗後續作與代理結果整理 |
| 驗證與資料處理 | `scripts/*.py` | 解析測試證據、比較輸出、追蹤業務規則、比較升級前後基線、組成驗證報告 |
| 報告與可視化 | `assets/*.html`、報告產生腳本 | 離線單頁報告、依賴拓撲圖與互動式視圖 |
| 選配介面 | `hooks/*.ts`、`hooks/views/*` | 讀取已產生的檔案，顯示階段、模組進度、規則覆核及驗收資訊 |
| 自身測試 | `tests/*`、`scripts/tests/*` | 檢查工作流的邏輯、解析器、介面與證據判定 |

**重要逆向判斷：** 此架構把自然語言代理放在「理解、規劃、撰寫與檢查候選成果」的位置，把可被程式檢驗的驗收條件交給傳統腳本處理。這是「模型推理＋確定性驗收」的混合架構，不是純模型自主判斷。

---

## 2. 主流程與產物契約

### 2.1 流程圖

```text
/modernize
  └─ INTENT.md：記錄目標與改造類型
       ↓
/modernize-preflight
  └─ PREFLIGHT.md：環境、工具鏈、範圍、缺件與可執行性
       ↓
/modernize-assess
  └─ ASSESSMENT.md + ARCHITECTURE.mmd
       ↓
/modernize-map
  └─ topology.json + TOPOLOGY.html + Mermaid 圖
       ↓
/modernize-extract-rules
  └─ BUSINESS_RULES.md + DATA_OBJECTS.md
       ↓
/modernize-review
  └─ RULE_REVIEWS：人工確認、修正或標記存疑的規則
       ↓
/modernize-brief
  └─ MODERNIZATION_BRIEF.md：分階段方案、行為契約、批准關卡
       ↓
┌────────────────┬──────────────────┬─────────────────┐
│ uplift         │ transform        │ reimagine       │
│ 同技術版本升級  │ 逐模組跨技術改寫 │ 新架構重建       │
└────────────────┴──────────────────┴─────────────────┘
       ↓
/modernize-verify
  └─ VERIFICATION.md + VERIFICATION.json
       ↓
/modernize-harden
  └─ SECURITY_FINDINGS.md + 待人工審核的修補 patch
       ↓
REPORT.html / modernize-status
```

以上是完整主路徑的概念圖。各命令可獨立執行及停下來審查，但命令會依所需產物檢查前置條件；例如計畫所需的盤點、拓撲或業務規則缺失時，不應直接進入建置。

### 2.2 產物為何重要

外掛 README 明確指出，狀態放在檔案而不是聊天歷史中。後續命令會讀取 `INTENT.md`、`PREFLIGHT.md`、`MODERNIZATION_BRIEF.md` 等產物，因此不同工作階段或另一位工程師能從同一份工作區續接。

這種設計的實際作用：

- **降低對話脆弱性：** 不必依賴上一輪聊天是否完整留在上下文。
- **讓交接可稽核：** 每個結論能連回檔案、規則、計畫或測試證據。
- **讓計畫成為控制面：** 後續建置階段讀取已批准的計畫，而不是每次重新解讀最初需求。
- **暴露缺件：** 缺少必要的上游產物時停止，避免跳過理解階段直接施工。

對 P2 而言，這與「單一 Current、可追蹤工作單元、明確輸入／輸出、施工與驗收分離」的設計方向相容。

---

## 3. 三種改造策略不能混用

| 策略 | 目的 | 必要做法 | 常見誤判 |
|---|---|---|---|
| **Uplift** | 保留現有技術與大部分程式，只升級版本 | 建立版本差異目錄、雙版本基線、先做一個試點、形成 PLAYBOOK，再按相依關係分批升級 | 把版本升級錯當成重新設計，造成無必要的全面重寫 |
| **Transform** | 行為保持相同，但把單一模組改到另一種技術 | 先寫行為特徵測試，再改寫、以相同輸入比較舊新輸出；可採逐片替換而讓舊系統繼續運作 | 只追求新架構或語法，不保留原有行為及歷史邊界條件 |
| **Reimagine** | 基於新架構重建並允許有計畫地調整行為 | 從現有系統抽取規則與需求，形成規格，設計新架構並接受對抗式檢視，再分服務建立並附上可執行驗收測試 | 把尚未決議的行為改變藏在「重建」裡 |

原始碼中的 Uplift 流程尤其值得注意：版本、工具鏈或測試框架若尚未確認，就在前置階段顯式處理；它先遷移單一代表性單元並把成果寫成 PLAYBOOK，經批准後才擴展。當升級差異顯示大多數程式都必須被改寫時，流程會建議改走 Transform，而不是硬把整個任務塞進 Uplift。

官方命令依據：
- [Uplift 命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-uplift.md)
- [Transform 命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-transform.md)
- [Reimagine 命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-reimagine.md)

---

## 4. 多代理協調：不是單純同時開很多 AI

### 4.1 專業分工

外掛具備以下代理：

- `legacy-analyst`：讀取舊程式的結構、隱含相依及程式模式。
- `business-rules-extractor`：抽取業務規則並附來源位置。
- `architecture-critic`：檢查目標架構及改寫結果，指出過度設計。
- `security-auditor`：安全、憑證、依賴弱點與輸入檢查。
- `test-engineer`：特徵測試、等價性測試與回歸檢查。
- `version-delta-analyst`：辨識來源版本與目標版本之間實際影響該程式的變更。
- `uplift-migrator`：按既定 playbook 遷移獨立單元。
- `scaffolder`：建立重建方案中的單一服務。

### 4.2 規則抽取工作流的實際機制

`workflows/extract-rules.js` 定義了兩種模式：

1. **模組模式：** 根據模組清單切分工作；每個模組一個抽取代理，按固定順序分批執行；每批先抽取、去重，再對新規則逐項做來源引用覆核。
2. **整體視角模式：** 以計算、驗證、生命週期等視角抽取；按輪次補充，當新增規則低於設定門檻或達到輪次上限時停止。

兩種模式都包含關鍵規則（P0）的額外判讀與資料物件目錄。工作流還特別控制代理呼叫的次序，讓已完成的工作能被工作日誌重播，並讓失敗的模組或規則以清單方式重跑，而不需要無條件重做所有工作。

這揭示了它在大規模任務中的一項設計重點：**平行化之外，還必須確保分批邊界、重跑語義與產物合併規則穩定。**

### 4.3 Uplift 工作流的依賴約束與熔斷

`workflows/uplift-migrate.js` 要求：

- 先完成一個試點，寫好 PLAYBOOK，再開始多代理批次遷移。
- 單元可聲明對其他單元的依賴；未完成依賴者不能與依賴項同批執行。
- 每個代理只寫入自己的單元目錄；共用層級檔案由呼叫端負責，減少並行寫入衝突。
- 按遞增批次擴大工作；批次的建置成功率未達工作流的熔斷門檻時，停止擴張。
- 輸出剩餘、失敗、被相依阻擋的單元清單，供下一輪重新輸入。

從逆向分析看，它把多代理協調視為「有向相依圖＋有限批次＋失敗隔離＋可續跑清單」，而非無限制的 agent fan-out。

---

## 5. 最重要的機制：獨立驗證（Proof Pack）

原始碼中的 `scripts/proof_pack.py` 定義三種狀態：

- **PROVEN：** 所要求的六類證據條件均通過。
- **PARTLY PROVEN：** 沒有已確認的失敗，但至少一項證明條件無法完成；必須列明缺少什麼。
- **NOT PROVEN：** 有測試失敗、行為差異、缺失證據或其他明確的驗收失敗。

這些詞不是對「整個軟體絕對正確」的形式化證明；它們代表該工具定義的有限驗收條件是否由目前證據滿足。

### 5.1 六類證據檢查

| 檢查項 | 驗證器要求 | 它能防止的問題 |
|---|---|---|
| 1. 測試確實執行 | 清理建置產物後重新跑測試；從測試框架的結果檔或可解析紀錄讀取數據；檢查失敗、跳過與證據是否過期 | 把「有測試檔」誤當成測試通過；手填數字冒充實測 |
| 2. 關鍵規則有測試覆蓋 | Rewrite／Reimagine 中，每條 P0 規則要連到實際執行且通過的測試；只被跳過或待執行的測試提及不算 | 只有規則文件、沒有真的保護行為的測試 |
| 3. 舊新行為等價 | 比對兩邊在相同輸入的結果；Uplift 則檢查基線、失敗數及測試數等回歸 | 新程式能通過自有測試，卻與舊程式行為不同 |
| 4. 新增未用過的輸入 | 舊系統可以執行時，至少新增 10 個與開發測試不同的新輸入，實際跑舊新兩邊並比較 | 只用模型自己挑選的例子驗證模型自己的改寫 |
| 5. Canary 故意破壞測試 | 刻意改壞一個有意義的程式行為，保留測試結果證明測試確實失敗 | 測試套件即使程式已壞也會綠燈 |
| 6. 舊程式未被改動 | 透過檔案系統檢查舊程式是否出現晚於分析基準的修改 | 防止改寫過程偷偷變更作為對照組的舊程式 |

驗證器會重新讀取證據、重新比較，而不照抄建置階段留下的判定。測試執行數不能只由文字宣稱或手工填進 JSON 取得；它會解析實際測試結果格式或支援的 runner 日誌。

**重要限制：** 若舊系統無法在當前環境執行，只能與記錄的結果比較，官方設計規定最好的判定是 `PARTLY PROVEN`，不會直接升級成 `PROVEN`。

### 5.2 數值與非決定性輸出的比較

`scripts/compare.py` 對輸出比對提供明確的遮罩與數值容差機制。例如時間戳或生成 ID 可以按規則遮罩，浮點結果可依宣告的絕對／相對容差比較。這些遮罩、容差與獲准的差異都要留下原因與紀錄，不能默默略過差異。

這是務實的設計：嚴格位元比較適用於確定性輸出；對非決定性或數值輸出放寬時，放寬本身也必須是可檢查的決策。

### 5.3 驗證證據的邊界

- `PROVEN` 只代表已定義的檢查通過，不保證所有未知輸入、環境或生產狀態都沒有缺陷。
- 十個新輸入是最低驗收門檻，不是完整測試所有可能狀態。
- Canary 可以證明某些測試能抓住特定故障，但無法單獨證明整份測試套件完整。
- 業務規則由模型抽取，官方亦提醒兩次抽取可能不同，因此業務規則是需要人工覆核的研究成果，不是完全確定的編譯產物。
- 原始碼保護檢查主要依檔案時間；它有利於避免在不可信程式樹內呼叫版本控制命令，但單靠時間戳不是內容雜湊級別的完整防竄改證明。**對 P2 的移植應採更強的前後內容雜湊或受控 diff 驗收。**

程式依據：
- [proof_pack.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/proof_pack.py)
- [compare.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/compare.py)
- [驗證命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-verify.md)

---

## 6. 安全與治理設計

### 6.1 不信任被分析的程式碼

官方文件直接承認，舊程式、README、註解或檔名可能含有提示注入或誘導工具執行指令的內容。外掛要求代理把這些內容當成資料，不依指令執行；規則與安全發現需回到引用的原始程式碼重新核實；真正建置前須通過人工批准的 brief。

這種安全架構是多層防護，不是只在系統提示中寫「請小心」：

1. 把待分析的原始碼視為不可信輸入。
2. 分析結果必須帶來源；驗證者獨立回到來源確認。
3. 計畫與未決問題需要人工裁定。
4. 將敏感值遮罩；原始憑證只放入規定的本機隔離檔案。
5. 安全掃描只產出調查結果及待審 patch，由使用者或安全工程師決定是否套用。

### 6.2 寫入範圍

外掛以 `legacy/<system>` 作為舊程式參照位置；分析產物寫到 `analysis/<system>/`，新程式寫到 `modernized/` 下。它也會檢查連結與路徑，避免驗證腳本沿著連結讀取工作區外的任意檔案。

但必須區分「工作流設計要求不修改 legacy」與「作業系統層級絕對無法修改 legacy」。任意 shell 命令是否可改動檔案仍與執行權限、使用者核准及具體命令有關；只看 README 不能推定已有完全隔離的沙盒。實際使用時仍需檢查權限設定、Bash 操作與差異結果。

### 6.3 Telemetry

manifest 的使用計數設定預設為開啟，但外掛說明其資料經 Claude Code 自身 telemetry 傳送；若 Claude Code telemetry 關閉，就不會傳送。內容設計為整數計數，不傳原始程式碼、提示、名稱、路徑或錯誤文字；高於一定數量的計數會約略化。使用者應在組織環境中核對實際設定與資料政策，而非單看「沒有傳程式碼」便推定不必審查 telemetry。

---

## 7. 官方實作案例透露的真實能力與限制

官方 README 記錄了對多個公開程式庫的實際執行結果，且保留了驗證失敗的案例。這比只有成功示範更能看出它的邊界。

| 案例 | 官方記錄的結果 | 可確認的意義 |
|---|---|---|
| AWS CardDemo（COBOL） | 逐步重寫並反覆發現空白欄位、非數字帳戶鍵、負零及格式差異；最後的新輸入又發現差異，驗證結果為 NOT PROVEN | 新測試、更多輸入能揭露先前未發現的行為差異；「已改寫」不代表「已等價」 |
| Eclipse Jetty（Java 8 → 17） | 對雙版本測試及基線進行比對；除已知差異外，實際建置還暴露出工具、manifest 及版本相容性問題 | 靜態理解不能取代真實工具鏈與兩個目標環境的執行 |
| osCommerce（PHP → Python/FastAPI） | 產品頁切片完成大量測試與新輸入比對；官方記錄最終獨立驗證為 PROVEN | 在有可執行舊程式、測試證據與獨立驗收時，確實可能形成較強的行為等價證據 |
| JPetStore（重建 REST API） | 發現部分新舊輸出差異，驗證為 NOT PROVEN | 新架構和一部分通過的測試不足以掩蓋未解決的行為差異 |
| beets（Python 2 → 3） | 當前機器無法取得必要套件，舊測試無法執行；外掛沒有把環境失敗說成成功 | 工具鏈不可用是阻塞，不應以模型推論替代實際驗證 |

官方亦說明，大型規則抽取會啟動大量代理：其測試環境中一次規則抽取可啟動約 50–200 個代理。這表示它為覆蓋度投入實際的計算與協調成本；不能只看到工作流自動化，就推論它便宜、快速或適合每一種任務。

來源：[官方 README：案例、成本預期、安全與已知事項](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/README.md)

---

## 8. 對 forAVAr／P2 的可移植設計

### 8.1 直接值得借鑑

| Modernization 設計 | 可套用到 forAVAr/P2 的原則 | 建議驗收條件 |
|---|---|---|
| 前置盤點與正式計畫 | 任何新增功能前，先查找既有能力，做 REUSE／MODIFY／MERGE／NEW 比對，不能只因某功能缺少入口就複製重建 | 施工計畫引用既有候選；NEW 說明為何不能修改或合併 |
| 產物作為交接契約 | 每個階段留下固定欄位的產物，下一階段只消費已宣告且已驗證的輸入 | 缺少上游必備檔案時停止；每個產物記錄版本、狀態、來源與產出者 |
| 把規則連回來源 | P2 的常設規則、能力、生命週期、門檻與關閉條件應能追溯到定義位置及實際使用處 | 有來源位置、呼叫者／消費者、測試與生命週期狀態 |
| 施工與驗收分離 | 代理負責提出變更；另一個驗收步驟依證據判斷是否通過 | 驗收不只讀模型摘要；讀取實際測試記錄或可重算的證據 |
| 有限工作單元與寫入界線 | 任務分成輸入明確、輸出位置不重疊的 Work Unit，限制代理可改的路徑 | 寫入清單可檢查；共同檔案有唯一所有者 |
| 依賴排序與熔斷 | 以依賴圖安排批次；初期小批，達成門檻再加大；失敗只重跑失敗及被阻擋的單元 | 前置依賴先通過，失敗不會繼續擴散；每種失敗可重現及重跑 |
| 新輸入與故障注入 | 對核心規則補邊界案例，並故意破壞一個關鍵判斷，驗證測試會失敗 | 不只標示「有測試」，而是保存測試結果與 canary 證據 |
| 狀態分級 | 保留 P2 既有的真實執行、模擬、未驗與假說等證據分類，不用單一 DONE 混淆狀態 | 每個結論帶證據等級；SIMULATED_PASS 絕不能升格成實際執行通過 |
| 安全 patch 由人決定 | 將風險發現、修補候選、套用、驗收分離；安全修補不應由同一代理自動宣告完成 | patch 有差異、風險理由、測試及人工核准記錄 |

### 8.2 與已知 P2 交接規則的關聯

本次可直接讀取的 forAVAr 背景文件是 `R3d130j-HANDOFF.md`，其中描述了 P2 的通用工程大腦方向、F30 四階段、既有能力優先與證據標記。該交接文件亦記錄先前工作發現多套閉環／階段骨架並存，以及部分模組沒有引用或測試的疑慮。

因此，本研究建議把 Modernization 的「前置盤點」和「產物關卡」放在更高優先順序，而不是再新增一套獨立的現代化系統：

1. **先映射 P2 既有能力：** 對照 Brain、Central、Work Unit、Current State、System Factory、Assurance 及 F30，判斷哪些可以承載現代化流程。
2. **把 Modernization 定義為可重用的工作模板：** 不把每個步驟實作成各自獨立的重疊系統；由現有協調、能力與驗收機制承載。
3. **沿用明確的證據分類：** `PROGRAM_EXECUTED_PASS`、`SIMULATED_PASS`、`PATCHED_UNVERIFIED`、`NOT_EXECUTED`、`HYPOTHESIS` 必須保持語義分離。
4. **補強真實驗收，不複製表面狀態：** 若 P2 現有流程只能輸出成功字串或模擬通過，先擴充證據讀取與判定，不要只增加一份新報告。
5. **優先修正閉環重疊及孤兒模組：** 在建立新現代化功能之前，先確認舊模組是可接線、應合併、需修改，還是應依正式流程退場。

**範圍限制：** 這段對應只基於目前可讀取的 forAVAr README 與 `R3d130j-HANDOFF.md`，並非對 P2 全部壓縮檔或程式碼進行完整新一輪驗收。本文件不宣稱 P2 已有或缺少某項具體實作，除非交接文件明確記載。

### 8.3 不應直接照搬的部分

- **大量平行代理：** 官方記錄的 50–200 代理規則抽取有較高協調與推理成本。P2 應先做小批次試點，量測單位工作成本、合併衝突與重跑比例。
- **把 PROVEN 當成萬用完成狀態：** Modernization 的判定是為程式行為等價設計；P2 更廣泛的流程閉環還涉及啟動、退場、錯誤、中斷、預算、Current 更新與交接，不能用同一個六項檢查取代。
- **仰賴模型抽取作為唯一真相：** 業務規則和架構摘要會有抽取差異，必須保留原始證據與人工決策。
- **把時間戳當作不可竄改證據：** P2 若已有雜湊、原子寫入與封包驗證機制，應優先重用更強的既有能力，而不是退回只看修改時間。
- **把可選即時面板當核心：** 介面是呈現層；真正的狀態應來自已存檔案和機器可驗的證據，不應由 UI 自行維護另一份真相。

---

## 9. 建議的最小移植順序

### M0 — 流程盤點與覆蓋比對

輸入：目前能力清單、Current、生命周期／閉環骨架、登記表與測試目錄。  
產出：既有候選比對表、可重用流程映射、缺口清單。  
停止條件：未釐清重疊組前，不新增另一套階段骨架。

### M1 — 工作單元契約

每個 Work Unit 最少記錄：目標、範圍、依賴、可讀路徑、可寫路徑、預期輸出、完成條件、驗證方式、退場動作與失敗處理。  
驗收：輸入不完整時可停止；輸出不符合契約時不能直接登記完成。

### M2 — 獨立驗收器

優先建造或重用能解析真實測試結果、封包驗證結果、檔案雜湊及狀態登記的驗收能力。施工代理與驗收器分離。  
驗收：至少有一個預期成功案例、一個預期失敗案例、一個中斷或缺件案例；測試數不得靠手工輸入冒充執行證據。

### M3 — 有界批次與失敗隔離

每批先小後大，依依賴關係安排；失敗、被依賴阻擋、尚未開始須分開登記，並可單獨重跑。  
驗收：一個單元失敗時，不把依賴它的單元誤標成功，也不迫使整批無差別重做。

### M4 — 報告與交接呈現

把階段、證據等級、未解決問題、下一個可執行步驟呈現在報告或面板中；報告讀取既有 Current 與產物，不另存互相矛盾的進度。  
驗收：新會話只讀唯一 Current 與規定的交接文件，即可接續；未實測項仍清楚顯示未實測。

---

## 10. 最終結論

**這個外掛最可移植的不是它的提示詞，而是它把 AI 工程化的三道約束：**

1. **先建立可追溯的理解與計畫，再允許施工。**
2. **多代理只在有明確分工、相依、寫入邊界與重跑規則時才擴大。**
3. **用獨立驗收器消除「模型宣稱完成」與「證據真的成立」之間的落差。**

對 forAVAr/P2，應優先採納前置能力比對、產物契約、獨立證據驗收及有界批次協調；同時維持 P2 的生命周期、Current 與證據語義。不能把程式現代化的等價性判定直接等同於通用 AI 工程流程已閉環。

本文件為原始碼層的逆向分析與移植建議，並非已安裝並運行該外掛的實測報告，也不表示上述建議已經寫入 P2。

---

## 11. 來源與可重現入口

主要來源全部固定到研究時的外掛快照：

1. [Code Modernization README（完整流程、案例、安全與使用成本）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/README.md)
2. [Plugin manifest（版本與可設定選項）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/.claude-plugin/plugin.json)
3. [Uplift workflow（依賴、分批、熔斷與重跑）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/workflows/uplift-migrate.js)
4. [Business-rule extraction workflow（分片、引用覆核、P0 判讀）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/workflows/extract-rules.js)
5. [Proof pack（證據規則及三種判定）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/proof_pack.py)
6. [Output comparator（輸出差異、遮罩與數值容差）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/compare.py)
7. [Verification command（驗證操作及證據收集要求）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-verify.md)
8. [Anthropic：AI 驅動的程式現代化專案準備方式，2026-09-23](https://claude.com/resources/articles/how-to-prepare-for-ai-driven-code-modernization-projects?fcdaa149_sort_date=desc)
9. [forAVAr 既有交接：R3d130j-HANDOFF.md](https://github.com/upqq21477-star/forAVAr/blob/main/R3d130j-HANDOFF.md)
