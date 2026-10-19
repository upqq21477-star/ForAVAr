# Claude Code Modernization 逆向分析

研究對象：[Anthropic 官方 code-modernization 外掛](https://github.com/anthropics/claude-plugins-official/tree/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization)

研究基準：`anthropics/claude-plugins-official` 的 commit `ea10b213686c90bb1984b2016937310e05336cf3`（2026-10-16）；外掛 manifest 版本 `1.0.0`。

研究方式：原始碼、工作流、命令、腳本、測試與官方案例的靜態逆向分析。**未在本研究中安裝或實際執行外掛**，故不宣稱已驗證其執行效能或完整可靠性。

## 重要摘要

**Code Modernization 的核心價值是將舊程式現代化組織成可追溯、可中斷續作、需人工批准、由獨立證據驗收的工程流程。** 它不只是多代理重寫程式的提示詞集合。

最重要的五項設計：

1. **先理解再施工：** 環境盤點、架構與依賴圖、業務規則抽取、人工審核、正式計畫。
2. **區分改造策略：** 同技術版本升級（Uplift）、逐模組改寫（Transform）、新架構重建（Reimagine）。
3. **多代理受到工作契約約束：** 分工、相依排序、分批擴大、寫入範圍、失敗分類與可重跑清單。
4. **驗收以實際證據計算：** 測試結果、舊新輸出比對、新增輸入、故意破壞測試（canary）及來源未被改動；不接受單靠文字宣稱成功。
5. **狀態由產物承載：** 命令透過分析檔、計畫與驗證結果交接，報告／面板呈現這些產物，不應另創第二份狀態真相。

對 forAVAr/P2 的採用方向：**優先重用現有能力，借鑑產物契約、獨立驗收及有界批次；不可直接複製一套重複的生命週期，也不可將模擬通過當成實際執行證據。**

---

## 一、系統架構還原

### 1.1 原始碼分層

| 層 | 主要路徑 | 職責 |
|---|---|---|
| 命令與工程規程 | `commands/*.md` | 定義輸入、前置條件、作業步驟、人工批准點及輸出 |
| 專業代理 | `agents/*.md` | 分別負責舊系統分析、規則抽取、架構評估、安全、測試、版本差異、遷移與服務骨架 |
| 多代理工作流 | `workflows/*.js` | 分片、依賴排序、平行批次、引用覆核、重跑及失敗彙整 |
| 證據與比較腳本 | `scripts/*.py` | 解析測試證據、追蹤規則、比較輸出、檢查升級差異、計算驗收判定 |
| 報告與拓撲視圖 | `assets/*`、`scripts/build_report.py` | 離線報告、相依圖與進度呈現 |
| 選配面板 | `hooks/*` | 從已產生的產物讀取進度、規則審核、驗收與下一步 |
| 自身測試 | `tests/*`、`scripts/tests/*` | 測試工作流、解析器、UI 狀態及證據判定的失效案例 |

**架構判斷：** AI 主要負責分析、提出計畫、產生程式與候選解釋；可程式檢查的驗收條件交給 Python 腳本計算。這是「模型推理＋確定性驗收」的混合架構。

### 1.2 主要產物與交接

主流程：

```text
/modernize
  -> INTENT.md
/modernize-preflight
  -> PREFLIGHT.md
/modernize-assess
  -> ASSESSMENT.md
/modernize-map
  -> topology.json、TOPOLOGY.html、圖檔
/modernize-extract-rules
  -> BUSINESS_RULES.md、DATA_OBJECTS.md
/modernize-review
  -> RULE_REVIEWS.json
/modernize-brief
  -> MODERNIZATION_BRIEF.md（人工批准）
  -> uplift / transform / reimagine
/modernize-verify
  -> VERIFICATION.md、VERIFICATION.json
/modernize-harden
  -> SECURITY_FINDINGS.md、待審查 patch
  -> REPORT.html / modernize-status
```

各命令可分開執行與審查；需要的上游產物缺失時，不應略過必要理解階段。狀態放在檔案而非聊天脈絡，因此新會話或另一位工程師可以讀取同一批產物接續。

### 1.3 人工控制點

需要人類判斷的內容不由代理代決：前置環境與範圍回答、存疑的業務規則、批准現代化計畫、決定是否接受行為差異、驗收簽署，以及是否套用安全修補。模型抽取的規則也可能因重跑而不同，所以業務規則必須被視為待審閱成果，不可直接當成絕對真相。

---

## 二、三種改造策略

| 策略 | 適用情境 | 主要流程 | 不應做的事 |
|---|---|---|---|
| **Uplift** | 保留原技術，升級執行環境或框架版本 | 確認版本與工具鏈 → 建立版本差異目錄／基線 → 遷移單一試點 → 形成 PLAYBOOK → 人工批准 → 按依賴分批遷移 → 比較舊新版本 | 不應借升級之名全面重寫 |
| **Transform** | 保留模組行為，改用不同技術逐步重寫 | 抽取業務規則 → 寫特徵測試 → 批准計畫 → 逐模組改寫 → 相同輸入比較舊新輸出 | 不能只看新程式測試通過，不比對舊行為 |
| **Reimagine** | 在新的目標架構下重建 | 由舊程式抽取規格 → 架構設計與批判 → 人工批准 → 建立服務與驗收測試 → 驗證 | 不可把尚未批准的行為變更隱藏在重建中 |

Uplift 會要求明確的來源／目標版本與可用工具鏈；如兩個版本無法在目前環境同時執行，證據就會降級。如果版本差異顯示大部分程式需要重寫，便應考慮轉用 Transform，而不是硬套 Uplift。

原始碼：
- [modernize-uplift.md](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-uplift.md)
- [modernize-transform.md](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-transform.md)
- [modernize-reimagine.md](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-reimagine.md)

---

## 三、多代理協調與續作機制

### 3.1 專業代理

外掛包含舊系統分析、業務規則抽取、架構批判、安全審核、測試工程、版本差異分析、Uplift 遷移及服務骨架建立等不同代理。重點不在代理數量，而在每個代理有明確任務與輸出邊界。

### 3.2 業務規則抽取

`workflows/extract-rules.js` 支援兩種模式：

- **模組模式：** 每個模組分配抽取工作，按順序分批；新規則先去重，再逐條執行來源引用覆核。
- **整體視角模式：** 以計算、驗證、生命週期等角度抽取，直到新增規則低於門檻或達到輪次上限。

通過引用覆核的關鍵規則（P0）還會進入額外判讀；工作流亦建立資料物件目錄。它使用可重播的工作日誌和固定的呼叫順序，使已完成代理結果可重用，失敗項可以被單獨重跑。

### 3.3 Uplift 分批、依賴與熔斷

`workflows/uplift-migrate.js` 明確要求：完成單一試點、形成 PLAYBOOK 並經人工批准後，才擴展到大量模組。單元的依賴未完成就不能與其依賴項同批執行；代理寫入各自的單元目錄，共享檔案則由呼叫端管理。

工作流以小批次開始，依建置成功率決定是否擴大；每次回傳三種可重輸入清單：

- 尚未嘗試的單元。
- 已嘗試但建置失敗的單元。
- 因相依失敗而被阻擋的單元。

這是「有限批次＋依賴圖＋失敗隔離＋明確重跑集合」，不是單純無限制平行啟動。

### 3.4 大型系統的分塊

`modernize-map.md` 對超過約 2,000 個來源檔或 500,000 行的系統，建議按領域或頂層目錄分塊，獨立寫入每塊的拓撲 JSON，完成後才合併。中斷後可略過已完成區塊，未完成或無法解析的連線要列出。

該命令還要求優先使用現有工具的機器可讀輸出（例如 Java、.NET、JavaScript、Python、Go 或 Rust 生態的依賴圖），再抽查部分關係並補上部署入口、外部設定、資料儲存與業務流程。**先重用現有可信工具，再補缺口**，比為自動化而重造工具更合理。

---

## 四、核心驗收器：Proof Pack

主要實作位於 `scripts/proof_pack.py`。它從當前證據重新計算每個模組的判定，輸出 Markdown 與 JSON，不直接相信先前報告中的結論。

### 4.1 三種判定

| 結果 | 定義 |
|---|---|
| `PROVEN` | 目前策略規定的驗收檢查全部通過 |
| `PARTLY PROVEN` | 沒有明確失敗，但至少一項必要證據無法取得或無法完整驗證 |
| `NOT PROVEN` | 有測試失敗、等價性差異或其他明確驗收失敗 |

這是有限工程條件下的證據判定，不是對軟體在所有輸入、部署環境與未來狀態下的絕對正確證明。

### 4.2 六項通用檢查

| 檢查 | 要求 |
|---|---|
| 1. 測試確實執行 | 清理產物後重跑測試；從可解析結果檔或支援的 runner 日誌取得執行證據，檢查失敗、跳過與過期結果 |
| 2. 關鍵規則受測試支持 | Transform／Reimagine 的每條 P0 規則，須有實際執行且通過的測試支持；被 skip／pending 的測試不算 |
| 3. 舊新行為一致 | 以同一批輸入比較結果，或按 Uplift 規則比較升級前後基線 |
| 4. 新增輸入 | 舊系統可以執行時，至少 10 個未被開發測試使用、且不重複既有輸出的新輸入，必須實際執行並比對 |
| 5. Canary | 刻意破壞一個有意義的程式行為，並有真實測試結果證明該變更造成測試失敗 |
| 6. 舊來源未被改動 | 透過檔案系統檢查來源相對於分析基準是否有新修改 |

Uplift 另外有三項檢查，因此該路徑最高判定需要通過九項：
- **基線量測：** 基線須有測試產物／紀錄支持，不可只手工填數字。
- **測試保留：** 比較舊版與工作副本的測試檔案；刪除舊測試或超過四分之一舊測試檔被修改會形成缺口。
- **版本差異覆蓋：** 標為 Behavioral-silent 的版本差異應有測試檔提及，無測試提及時列出缺口。

Uplift 的檔案差異檢查能發現測試檔被改，但不能僅靠檔案差異判斷 assertion 是否被弱化；測試檔有提及差異，也不等於測試充分覆蓋該行為。

### 4.3 比較器如何避免假證據

`scripts/compare.py` 對實際輸出檔執行位元組比較，而非採用模型的文字判斷。每個案例可設定舊新輸出、遮罩、容差及人工批准差異的理由。

- 缺失或無法讀取的輸出是 `missing`，不是相等。
- 路徑預設不得離開案例目錄；需要放寬時必須明確使用 `--allow-outside`。
- 檔案大小有上限；比較器還會以故意改動一個位元組的方式自檢差異偵測。
- 時間戳、生成 ID 等可以遮罩，但每個遮罩必須留下理由。
- 浮點結果可宣告絕對／相對容差，但容差要有理由及上限；其他文字及整數仍要求一致。
- 人工批准的差異仍會保留在報告中，不會被假裝成不存在。

### 4.4 規則追蹤的證據層級

`scripts/trace_rules.py` 將規則 ID 與新程式、測試檔及實際測試結果關聯，區分：
- `tested`：有實際通過的測試結果支持。
- `named, not run`：測試提到規則，但沒有成功執行證據。
- `code only`：只在主程式出現。
- `claimed only`：只在轉換／升級備註中聲稱。
- `none`：沒有找到引用。

**限制：** 這主要依測試名稱、識別符與測試結果判斷，並非完整的語意覆蓋證明，也不等同於 branch coverage、mutation score 或形式驗證。P2 如要宣稱核心規則已受保護，仍應按需要搭配 assertion、覆蓋率或 mutation testing 等獨立證據。

### 4.5 無法證明的情境

如果舊系統無法在目前環境執行，只能對照既存紀錄，外掛規定最佳判定為 `PARTLY PROVEN`，不能直接升格為 `PROVEN`。未執行的測試、缺失輸出、手填數據與只有文字敘述的 canary，都不能替代執行證據。

原始碼：
- [proof_pack.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/proof_pack.py)
- [compare.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/compare.py)
- [trace_rules.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/trace_rules.py)
- [uplift_checks.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/uplift_checks.py)
- [驗收命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-verify.md)

---

## 五、安全與信任邊界

### 5.1 將舊程式視為不可信輸入

程式碼註解、README、檔名與分析產物可能含有提示注入、惡意文字或不安全路徑。外掛要求代理把這些內容視為資料，不能照著其中的指令行動；發現與規則必須能回到來源重新核查，建置前仍需經過人工批准。

### 5.2 檔案與路徑保護

驗收與報告腳本會拒絕部分符號連結、工作區外路徑、非一般檔案、超大檔案及格式錯誤輸入；只讀取受限制的文字／結構化證據。報告建置器將不可信內容當作跳脫後的資料，不直接把它當成 HTML 執行，並限制外部請求。

這些屬於工具層防線，並不等於作業系統級沙盒。外掛面板本身不會阻擋編輯或命令；舊程式能否被寫入，仍依賴工作區權限設定。實際使用時必須另行確認權限及差異，不能只靠提示詞保證唯讀。

### 5.3 憑證與安全修補

安全掃描把原始憑證隔離在 gitignore 保護的本機檔案或使用者目錄，分享用的發現報告會遮罩敏感值。修補內容以待審核 patch 產出，由人員決定是否套用。這將「發現弱點」「提供修補」「實際修改」「修補驗證」分開，避免掃描代理自行宣告安全工作完成。

### 5.4 Telemetry 與進度面板

manifest 定義使用計數設定；README 說明計數透過 Claude Code 自身 telemetry 傳送，並提供停用方式。外掛宣稱不傳送原始程式碼、提示、系統名稱或路徑；組織使用前仍應核對實際設定與政策。

面板讀取磁碟上的產物並顯示狀態，不自行呼叫模型或自動執行下一個命令，也不阻擋編輯。它不是治理核心；真實權限、生命週期和驗收應在執行層實作。README 將 function hooks 標註為 early access；面板文件所述測試環境為 Claude Code 2.1.280，不宜推定所有版本均相容。

來源：
- [modernize-map.md](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-map.md)
- [build_report.py](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/build_report.py)
- [面板文件](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/hooks/README.md)
- [外掛 README（Safety、Telemetry、Good to know）](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/README.md)

---

## 六、官方案例：有效性與限制

官方 README 記錄了成功與失敗案例；數字是官方測試環境中的紀錄，不應當作所有系統的保證。

| 案例 | 官方記錄 | 能支持的結論 |
|---|---|---|
| AWS CardDemo（COBOL 改寫 Java） | 多輪獨立驗證發現空白欄位、非數字帳戶鍵、負零等差異；新增輸入仍發現問題，最後為 `NOT PROVEN` | 新的反例能持續暴露隱藏行為差異；已重寫不等於等價 |
| Eclipse Jetty（Java 8 → 17） | 雙版本執行與建置發現靜態閱讀未預測的相容性問題；官方記錄測試在兩版本比對 | 必須實際檢查工具鏈與雙版本行為 |
| osCommerce（PHP → Python/FastAPI） | 產品頁切片的測試、舊新輸出與新增輸入比對均有記錄，獨立驗收為 `PROVEN` | 特定切片在證據充足時可以通過行為等價驗收 |
| JPetStore（重建 REST API） | 新舊應用輸出仍有差異，獨立驗收為 `NOT PROVEN` | 新架構與通過的部分測試不足以掩蓋差異 |
| beets（Python 2 → 3） | 因機器環境無法取得套件，測試不能執行，未被宣告成功 | 工具鏈阻塞不能被模型推理替代 |

官方亦稱，較重的規則抽取在其測試中曾啟動約 50–200 個代理，代表多代理方案有實際成本；對百萬行級系統，官方建議按模組或單元進行。README 也提醒抽取數字會因重新執行而變化，應把這些數字視為個別案例而非固定效能保證。

來源：[官方 README](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/README.md)

---

## 七、對 forAVAr/P2 的移植判斷

可讀取的 forAVAr 交接依據為 `R3d130j-HANDOFF.md`。其中已記錄的 P2 原則包括：新增前先比對既有能力、優先 REUSE／MODIFY／MERGE、以 F30 四階段形成工作閉環、區分實際執行與模擬通過，以及不要因發現孤兒模組就直接刪除。

本次只據該交接資料對照，**未重新掃描 P2 全部程式、schema、呼叫鏈與測試**，因此以下是移植建議，不是對 P2 現況的完整驗收結論。

### 7.1 應優先重用的原理

| Modernization 原理 | forAVAr/P2 應對方向 | 驗收要求 |
|---|---|---|
| 前置盤點 | 每次新增前先找既有能力，輸出 REUSE／MODIFY／MERGE／NEW 比對 | NEW 必須說明候選能力為何不能修改或合併 |
| 產物作為契約 | 每階段產出固定結構的結果，下一階段消費並驗證 | 必要輸入缺失就停止；有明確來源及狀態 |
| 規則可追溯 | 常設規則與能力連回定義來源及實際消費者 | 有引用位置、呼叫者／消費者、測試與生命週期狀態 |
| 施工與驗收分離 | 代理產生變更，獨立驗收器依證據判定 | 不只讀施工者的文字摘要 |
| 有界工作單元 | 為任務指定輸入、輸出、依賴與可寫範圍 | 不同代理的寫入路徑不衝突，共享檔案有單一所有者 |
| 失敗隔離與重跑 | 將失敗、未嘗試、依賴阻擋分開記錄 | 失敗不能被標成功；能明確重跑必要單元 |
| Canary 與反例 | 對核心規則建立邊界測試並證明測試會失敗 | 有實際結果檔；模擬不能代替執行 |
| 報告只呈現真相 | UI 讀取權威 Current 與產物，不另造狀態 | UI 不能自行把未知狀態猜成成功 |

### 7.2 不應直接照搬

- **不要照搬大量代理規模。** 官方規則抽取在測試中會啟動大量代理；P2 應先小規模試點並量測成本、合併衝突及重跑比例。
- **不要以現代化的六項驗收代替 P2 的整體閉環。** P2 還需檢查啟動、正常結束、錯誤、中斷、退場、預算、Current 更新及交接。
- **不要依賴時間戳作為最高級防竄改證據。** 若可行，應優先採用 P2 既有的內容雜湊、差異及封包驗證機制。
- **不要將測試命名等同於充分覆蓋。** 規則 ID 與通過測試有關聯，不代表測試已覆蓋所有分支或確實驗證業務斷言。
- **不要建立另一套重複生命週期。** 將 Modernization 視為可重用的工程流程模板，先核對現有 Central、Work Unit、Current、Assurance、System Factory 與 F30 的承載能力。

### 7.3 最小移植次序

**M0 — 既有能力對照**

完成目前規劃中尚未讀完的重疊組；在沒有完整證據前不刪除或合併模組。

**M1 — Work Unit 契約**

至少記錄目標、輸入、依賴、可讀／可寫路徑、預期產物、驗收條件、失敗處理與退場動作。

**M2 — 獨立驗收器**

優先重用既有工具來解析真實測試結果、差異、內容雜湊及封包驗證；至少測試正常通過、明確失敗、證據缺失及中斷／被阻擋情境。

**M3 — 有界批次與重跑**

先小批次，依依賴關係執行；失敗單元與被阻擋單元分開追蹤，驗收失敗時不得擴張批次。

**M4 — 唯一狀態的報告與交接**

報告直接讀取權威 Current 和驗收產物；新會話依文件即可續作，未實測項仍標記為未實測。

---

## 八、最終判斷與未完成事項

### 已由原始碼支持的結論

- 外掛有分階段命令、專業代理、多代理工作流、Python 驗證器與自身測試。
- 它將程式建置與獨立驗收分離，支援輸出比較、測試證據解析、canary 及三種驗收狀態。
- 工作流有相依分批、人工批准與可重跑失敗清單。
- 安全設計包括將分析輸入視為不可信資料、限制檔案路徑與大小，以及避免報告把資料當成可執行 HTML。
- 官方案例中存在 `PROVEN` 和 `NOT PROVEN`，工具會報告未解決的差異。

### 尚未完成／不能推論

- 本研究沒有實際安裝外掛、執行驗收或量測 token、耗時與成本。
- 官方的 `PROVEN` 是依其定義的工程驗收條件計算，不是所有輸入與生產狀態的絕對正確證明。
- 規則抽取會有模型差異，規則追蹤也不等同形式驗證或完整測試覆蓋。
- 尚未掃描 P2 全部原始碼、schema、相依關係與測試，因此不能據此判定 P2 哪些具體能力已經存在或缺失。
- 本文件只提供設計借鑑；沒有把任何新功能寫入 P1 或 P2。

**結論：** 最值得移植的是「先盤點與批准、按明確契約施工、以獨立證據驗收」。對 forAVAr/P2，先重用既有生命週期、工作單元與 Current 機制，再補上證據不足處，比新造一套相似工具更合理。

---

## 來源索引

以下固定到研究基準 commit，避免後續上游變動造成引用指向不同程式：

1. [外掛 README：主流程、實作案例、成本、安全與已知事項](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/README.md)
2. [外掛 manifest](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/.claude-plugin/plugin.json)
3. [規則抽取工作流](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/workflows/extract-rules.js)
4. [Uplift 遷移工作流](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/workflows/uplift-migrate.js)
5. [Proof Pack 驗證器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/proof_pack.py)
6. [輸出比較器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/compare.py)
7. [規則追蹤器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/trace_rules.py)
8. [Uplift 差異與測試檢查](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/uplift_checks.py)
9. [Proof Pack 測試](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/tests/test_proof_tools.py)
10. [拓撲圖命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-map.md)
11. [驗證命令](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/commands/modernize-verify.md)
12. [報告產生器](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/scripts/build_report.py)
13. [即時面板文件](https://github.com/anthropics/claude-plugins-official/blob/ea10b213686c90bb1984b2016937310e05336cf3/plugins/code-modernization/hooks/README.md)
14. [forAVAr 交接依據：R3d130j-HANDOFF.md](https://github.com/upqq21477-star/forAVAr/blob/main/R3d130j-HANDOFF.md)
