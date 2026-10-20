# Claude Code Modernization 研究分支｜程式結構與主流程

- 文件 ID：FORAVAR-CLAUDE-MOD-BR-001
- 類型：BRANCH
- 狀態：CURRENT／外部專案靜態逆向分析；非實機／Runtime 驗收
- 唯一責任：保存原報告中 0–4 節的完整細節、來源和限制。
- 主軸回鏈：[Claude Code Modernization 逆向分析主軸](./Claude_Code_Modernization_完整逆向分析.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [0. 核心摘要](#section-1)
- [1. 研究對象與程式結構](#section-2)
- [2. 主流程與產物契約](#section-3)
- [3. 三種改造策略不能混用](#section-4)
- [4. 多代理協調：不是單純同時開很多 AI](#section-5)

---

# Claude Code Modernization 逆向分析

> 主軸回鏈：[Claude Code Modernization｜主軸彙整](../Claude_Code_Modernization_主軸彙整.md) ｜ 分支 ID：CLAUDE-MOD-BR-001 ｜ 本回鏈只提供導航，不改變本文件的證據邊界。

> 研究日期：2026-10-19  
> 對象：Anthropic 官方公開倉庫 `anthropics/claude-plugins-official/plugins/code-modernization`  
> 源碼基準：`claude-plugins-official` 的 `main` 分支快照，commit `ea10b213686c90bb1984b2016937310e05336cf3`（commit 日期：2026-10-16），外掛 manifest 標示版本 `1.0.0`。  
> 研究方式：原始碼、命令文件、工作流、測試與官方說明的靜態逆向分析；本文件未安裝或實際執行該外掛。  
> 施工邊界：本次只新增 forAVAr 根目錄研究文件；不修改 README、不寫入 P1 或 P2。

## 來源前言（原始前置內容）

# Claude Code Modernization 逆向分析

> 主軸回鏈：[Claude Code Modernization｜主軸彙整](../Claude_Code_Modernization_主軸彙整.md) ｜ 分支 ID：CLAUDE-MOD-BR-001 ｜ 本回鏈只提供導航，不改變本文件的證據邊界。

> 研究日期：2026-10-19  
> 對象：Anthropic 官方公開倉庫 `anthropics/claude-plugins-official/plugins/code-modernization`  
> 源碼基準：`claude-plugins-official` 的 `main` 分支快照，commit `ea10b213686c90bb1984b2016937310e05336cf3`（commit 日期：2026-10-16），外掛 manifest 標示版本 `1.0.0`。  
> 研究方式：原始碼、命令文件、工作流、測試與官方說明的靜態逆向分析；本文件未安裝或實際執行該外掛。  
> 施工邊界：本次只新增 forAVAr 根目錄研究文件；不修改 README、不寫入 P1 或 P2。



<a id="section-1"></a>
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

<a id="section-2"></a>
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

<a id="section-3"></a>
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

<a id="section-4"></a>
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

<a id="section-5"></a>
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
