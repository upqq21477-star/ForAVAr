# PR-001–PR-054 的新版候選責任路由｜v0.2

- 原始問題、根因證據、處理方向與狀態仍以[問題清單唯一索引](../%28S級%29問題清單.md)和各 PR 權威分支為準。
- 此表只表示候選路由，不代表問題已解決。表中狀態是搜尋摘要；完整問題狀態、根因與證據須回原始分支核對。

| 原 ID | 失效模式摘要 | 狀態摘要 | 候選主責 | 節點／入口 | 支援平面 | 路由理由 |
|---|---|---|---|---|---|---|
| PR-001 | 理解錯誤、目標漂移或把手段當成目的 | PERSISTENT_RISK | AX1 | KG-01 | SP1,SP3 | 目標／意圖漂移 |
| PR-002 | 幻覺、捏造事實或虛報來源 | PERSISTENT_RISK | AX2 | KG-07 | SP2,SP5 | 幻覺／主張證據 |
| PR-003 | 來源失真、引用錯配與知識過期 | PERSISTENT_RISK | AX2 | KG-06 | SP2,SP6 | 來源／時效 |
| PR-004 | 失憶、交接遺漏與跨會話狀態失效 | PERSISTENT_RISK | L4 | S1 | SP3,SP6 | 跨輪狀態恢復 |
| PR-005 | 長上下文中的關鍵資訊遺漏 | PERSISTENT_RISK | AX2 | KG-09 | SP2,SP3 | 上下文缺口 |
| PR-006 | 因果推理錯誤、根因誤判或因果鏈不閉合 | PERSISTENT_RISK | AX3 | KG-13 | SP2,SP5 | 因果／根因 |
| PR-007 | 不確定性被掩蓋、衝突被硬合併 | PERSISTENT_RISK | AX2 | KG-08 | SP2 | 未知／衝突 |
| PR-008 | 循環驗證、自我修正無效或把重述當證明 | PERSISTENT_RISK | AX6 | KG-23 | SP5 | 自我驗證失效 |
| PR-009 | 提示注入或不可信資料控制思考與行動 | PERSISTENT_RISK | AX5 | KG-20 | SP1,SP4 | 不可信輸入／工具安全 |
| PR-010 | 模型與工具更新造成行為漂移 | PERSISTENT_RISK | AX6 | KG-26 | SP5 | 模型／工具漂移 |
| PR-011 | 把失敗蒸餾成錯誤規則，或一直重犯同類錯誤 | PERSISTENT_RISK | AX6 | KG-24 | SP5,SP6 | 錯誤蒸餾／復發 |
| PR-012 | 選錯研究／求解方法，或把特定流程強套所有問題 | DESIGN_DEFINED_UNVERIFIED | AX4 | KG-17 | SP4,SP5 | 方法錯配 |
| PR-013 | 第一版問題框架錯誤，後續細化將錯誤放大 | DESIGN_DEFINED_UNVERIFIED | AX1 | KG-05 | SP2,SP5 | 初始框架失效 |
| PR-014 | 變更波及面過大、依賴爆炸 | DESIGN_DEFINED_UNVERIFIED | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-015 | 接口過多、隱性耦合、Schema／語意漂移 | PARTIAL | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-016 | 能力選錯、能力描述被誤當成可執行功能 | DESIGN_DEFINED_UNVERIFIED | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-017 | 升級不相容、部分發布或回退失敗 | DESIGN_DEFINED_UNVERIFIED | L4 | S5 | SP5,SP6 | 文件／流程／生命週期 |
| PR-018 | 權限過大、插件副作用或供應鏈風險 | PARTIAL | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-019 | Current、藍圖、索引與派生視圖衝突 | PARTIAL | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-020 | 確認過的差異與實際寫入內容不一致 | DESIGN_DEFINED_UNVERIFIED | AX6 | KG-23 | SP5 | 驗收／修正候選 |
| PR-021 | 規則寫入文件，但新會話沒有載入或遵守 | OPEN | AX5 | KG-20 | SP1,SP4,SP5 | 執行／工具／控制 |
| PR-022 | 角色分工名義獨立，實際權限與認知不獨立 | PARTIAL | AX3 | KG-13 | SP2,SP5 | 問題模型／根因 |
| PR-023 | 測試集錯誤、基準過擬合或指標被美化 | DESIGN_DEFINED_UNVERIFIED | AX6 | KG-23 | SP5 | 驗收／修正候選 |
| PR-024 | 無限研究、遞迴重試、成本失控或任務卡死 | PARTIAL | AX4 | KG-17 | SP4,SP5 | 方法選擇／診斷 |
| PR-025 | 能力關係分析規模爆炸或未知關係被當成相容 | DESIGN_DEFINED_UNVERIFIED | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-026 | 有版本紀錄但不能真正恢復 | DESIGN_DEFINED_UNVERIFIED | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-027 | 無基線，無法證明新框架比簡單方案更好 | OPEN | AX1 | KG-04 | SP1,SP6 | 意圖／範圍 |
| PR-028 | 多檔更新只完成一部分，形成不一致版本 | DESIGN_DEFINED_UNVERIFIED | L4 | S1 | SP3,SP6 | 狀態／恢復 |
| PR-029 | 外部資料／工具行為改變而本地知識未更新 | PARTIAL | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-030 | 風險分級、變更優先序缺乏一致判準 | DESIGN_DEFINED_UNVERIFIED | L4 | S5 | SP5,SP6 | 文件／流程／生命週期 |
| PR-031 | 所有任務承受同一套完整流程 | DESIGN_DEFINED_UNVERIFIED | L4 | S5 | SP5,SP6 | 文件／流程／生命週期 |
| PR-032 | 過度插件化、過早抽象 | DESIGN_DEFINED_UNVERIFIED | AX4 | KG-17 | SP4,SP5 | 方法選擇／診斷 |
| PR-033 | 規劃、施工、驗收各自建立平行流程 | DESIGN_DEFINED_UNVERIFIED | L4 | S1 | SP3,SP6 | 狀態／恢復 |
| PR-034 | 多份索引、Schema 或登錄表變成第二套控制系統 | PARTIAL | AX5 | KG-20 | SP1,SP4,SP5 | 執行／工具／控制 |
| PR-035 | 主題分流導致紀錄碎片化或難以找回 | DESIGN_DEFINED_UNVERIFIED | L4 | S1 | SP3,SP6 | 狀態／恢復 |
| PR-036 | 只修症狀，根因仍存在 | PARTIAL | AX3 | KG-13 | SP2,SP5 | 問題模型／根因 |
| PR-037 | 以人氣或新穎度代替能力適配 | DESIGN_DEFINED_UNVERIFIED | AX6 | KG-23 | SP5 | 驗收／修正候選 |
| PR-038 | 過期能力、重複規則與舊相容層無法退場 | PARTIAL | L4 | S5 | SP5,SP6 | 文件／流程／生命週期 |
| PR-039 | 一般更新缺乏前後比較 | PARTIAL | AX6 | KG-23 | SP5 | 驗收／修正候選 |
| PR-040 | 問題 ID 綁定嚴重度 | DOC_FIXED | AX2 | KG-07 | SP2,SP5 | 來源／知識狀態 |
| PR-041 | 跨專案術語或相近名稱造成歧義 | PARTIAL | AX1 | KG-04 | SP1,SP6 | 意圖／範圍 |
| PR-042 | 把「完成研究／文件完整」當作真正完成 | PARTIAL | AX4 | KG-17 | SP4,SP5 | 方法選擇／診斷 |
| PR-043 | 索引、路徑或連結失效 | PARTIAL | L4 | S5 | SP5,SP6 | 文件／流程／生命週期 |
| PR-044 | 命名、顯示或分類不一致 | PARTIAL | L4 | S5 | SP5,SP6 | 文件／流程／生命週期 |
| PR-045 | 重複提問或過度打斷 | DESIGN_DEFINED_UNVERIFIED | AX1 | KG-04 | SP1,SP6 | 意圖／範圍 |
| PR-046 | 視圖形式與任務複雜度不匹配 | PARTIAL | AX6 | KG-23 | SP7,SP5 | 呈現／驗收 |
| PR-047 | 文件格式、目錄或描述增加閱讀成本 | PARTIAL | L4 | S5 | SP5,SP6 | 文件／流程／生命週期 |
| PR-048 | 新模型、多模態或新協定能力的導入時機 | MONITOR | AX3 | KG-13 | SP2,SP5 | 問題模型／根因 |
| PR-049 | 低頻特殊領域問題 | MONITOR | AX6 | KG-23 | SP5 | 驗收／修正候選 |
| PR-050 | 自動修改核心與完全自主演化 | MONITOR | AX5 | KG-20 | SP1,SP4,SP5 | 執行／工具／控制 |
| PR-051 | 為假想需求預建完整抽象 | MONITOR | AX1 | KG-04 | SP1,SP6 | 意圖／範圍 |
| PR-052 | 無 GitHub 可用上下文包，藍圖／舊交接被迫代替 Current | OPEN | L4 | S1 | SP3,SP6 | 狀態恢復包缺口 |
| PR-053 | 已知治理規則未觸發前置檢查 | OPEN | AX1 | KG-04 | SP1,SP6 | 前置掃描漏失 |
| PR-054 | 資訊分類、唯一歸位與流程回寫未形成可驗收閉環 | OPEN | AX6 | KG-26 | SP5,SP6 | 資訊歸位／回寫 |


**映射限制：**PR-001–PR-013 與 PR-052–PR-054 使用明確指定的初始歸位；其他問題有部分依標題／摘要關鍵詞形成候選分類。所有項目都須與完整問題原文、根因證據及既有控制逐項複核。未複核前不可標為已映射，文件有對策也不代表已驗收。
