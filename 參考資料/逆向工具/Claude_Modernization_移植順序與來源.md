# Claude Code Modernization 研究分支｜移植順序、結論與來源

- 文件 ID：FORAVAR-CLAUDE-MOD-BR-003
- 類型：BRANCH
- 狀態：CURRENT／外部專案靜態逆向分析；非實機／Runtime 驗收
- 唯一責任：保存原報告中 9–11 節的完整細節、來源和限制。
- 主軸回鏈：[Claude Code Modernization 逆向分析主軸](./Claude_Code_Modernization_完整逆向分析.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [9. 建議的最小移植順序](#section-1)
- [10. 最終結論](#section-2)
- [11. 來源與可重現入口](#section-3)

---

<a id="section-1"></a>
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

<a id="section-2"></a>
## 10. 最終結論

**這個外掛最可移植的不是它的提示詞，而是它把 AI 工程化的三道約束：**

1. **先建立可追溯的理解與計畫，再允許施工。**
2. **多代理只在有明確分工、相依、寫入邊界與重跑規則時才擴大。**
3. **用獨立驗收器消除「模型宣稱完成」與「證據真的成立」之間的落差。**

對 forAVAr/P2，應優先採納前置能力比對、產物契約、獨立證據驗收及有界批次協調；同時維持 P2 的生命周期、Current 與證據語義。不能把程式現代化的等價性判定直接等同於通用 AI 工程流程已閉環。

本文件為原始碼層的逆向分析與移植建議，並非已安裝並運行該外掛的實測報告，也不表示上述建議已經寫入 P2。

---

<a id="section-3"></a>
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
9. [forAVAr 既有交接：R3d130j-HANDOFF.md](../原始檔案/交接/R3d130j-HANDOFF.md)


---
