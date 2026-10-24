# forAVAr 覆蓋清冊（問題／功能／流程）

CODE＝程式強制且有測試；SLOT＝執行階段有契約入口、內容由 adapter 提供（未驗證）；PROCESS＝靠流程手動處理；DECISION＝待決策。

## 問題清單（54）

| ID | 名稱 | 層級 | 處理機制 | 限制／說明 |
|---|---|---|---|---|
| PR-001 | 理解錯誤、目標漂移或把手段當成目的 | CODE | TASK EVID | criteria are mandatory; result judged against them |
| PR-002 | 捏造事實、幻覺或虛報來源 | CODE | EVID UNK | claims without linked OBSERVED evidence downgrade to UNKNOWN |
| PR-003 | 來源失真、引用錯配或知識過期 | CODE | EVID | revision/date required; staleness judgement itself is adapter-supplied |
| PR-004 | 失憶、交接遺漏或跨會話狀態失效 | CODE | BUNDLE HANDOFF |  |
| PR-005 | 長上下文中的關鍵資訊遺漏 | CODE | BUNDLE | checkpoint + deterministic compaction (compact_bundle); no semantic summarisation |
| PR-006 | 因果推理錯誤、根因誤判或因果鏈不完整 | CODE | CORR | root cause UNKNOWN unless OBSERVED evidence supports it |
| PR-007 | 隱藏不確定性或強制合併衝突 | CODE | UNK CONFLICT |  |
| PR-008 | 循環驗證、自我修正無效或把重述當證明 | CODE | RETRY EVID | same input+method is not independent verification |
| PR-009 | 提示注入或不可信資料控制思考／行動 | CODE | POL GUARD | authorization fail-closed + heuristic content scan quarantines instruction-like evidence; paraphrased/encoded injection not detected |
| PR-010 | 模型或工具更新造成行為漂移 | CODE | BASE RUNREC | regression comparator + target_version/fingerprint; real drift detection needs FINAL_TEST |
| PR-011 | 將失敗蒸餾成錯誤規則或反覆重犯 | CODE | CORR | no rule from unsupported cause; promotion decision itself is manual |
| PR-012 | 方法選錯或對所有任務套用同一流程 | CODE | ROUTE RETRY |  |
| PR-013 | 初始問題框架錯誤並放大後續細化 | CODE | FRAME BRANCH | unready frame stops; FRAME_FAILURE routes to reframe |
| PR-014 | 變更波及面過大或依賴爆炸 | CODE | CORR |  |
| PR-015 | 接口過多、隱性耦合或 Schema／語意漂移 | CODE | PLUGIN CONSIST |  |
| PR-016 | 能力描述被誤當成可執行功能 | CODE | PLUGIN EVID | declared capability is not evidence |
| PR-017 | 升級不相容、部分發布或回退失敗 | CODE | TXN | verify-fail or crash -> full rollback from snapshot; applying is automated, choosing the change is not |
| PR-018 | 權限過大、插件副作用或供應鏈風險 | CODE | POL PLUGIN | declared side effects are not a security boundary |
| PR-019 | Current、藍圖、索引與派生視圖衝突 | CODE | CONSIST |  |
| PR-020 | 已確認差異與實際寫入內容不一致 | CODE | CHG |  |
| PR-021 | 規則存在但新會話未載入或未遵守 | PROCESS | HANDOFF | handoff export exists; cannot force a new session to load rules |
| PR-022 | 角色名義獨立但權限／認知不獨立 | PROCESS |  | logical roles do not prove independence (blueprint); independent review is manual |
| PR-023 | 測試集錯誤、基準過擬合或指標美化 | CODE | BASE | rubric fixed + fingerprinted before runs; required sample kinds |
| PR-024 | 無限研究、重試、成本失控或任務卡死 | CODE | RETRY |  |
| PR-025 | 能力關係分析爆炸或將未知當成相容 | CODE | UNK CORR | unknown is never treated as compatible; impact set is bounded |
| PR-026 | 有版本紀錄但無法真正恢復 | CODE | TXN BUNDLE | restore_drill re-hashes snapshot; retained zips remain the off-repo backup |
| PR-027 | 缺乏基線以證明新架構優於簡單方案 | CODE | BASE |  |
| PR-028 | 多檔更新部分成功造成版本不一致 | CODE | CORR CHG TXN | all-or-nothing change set via release_txn; lock file serialises writers |
| PR-029 | 外部資料／工具改變而本地知識未更新 | CODE | EVID | revision/date recorded; refresh trigger is manual |
| PR-030 | 風險分級或變更優先序不一致 | CODE | POL |  |
| PR-031 | 所有任務承受相同完整流程 | CODE | FAST |  |
| PR-032 | 過度插件化或過早抽象 | PROCESS | PLUGIN | map to existing capability IDs first (plugin_contract replacement rule) |
| PR-033 | 規劃、施工、驗收各自建立平行流程 | PROCESS | CONSIST | single authority order; checker catches listing drift only |
| PR-034 | 多份索引／Schema／登錄表形成第二套控制系統 | PROCESS | CONSIST | single authority order in operating_contract; checker catches listing drift only |
| PR-035 | 主題分流造成紀錄碎片化或難以找回 | PROCESS | CONSIST | topic routing by index.json id_lookup; manual placement |
| PR-036 | 只修症狀，未處理根因 | CODE | CORR |  |
| PR-037 | 以人氣或新穎度取代能力適配 | PROCESS | BASE | adoption requires baseline comparison |
| PR-038 | 過期能力、重複規則或舊相容層無法退場 | PROCESS |  | retirement governance is a procedure (VIEW-011) |
| PR-039 | 一般更新缺乏前後基線與成效比較 | CODE | BASE |  |
| PR-040 | 問題 ID 綁定嚴重度，升降級造成引用失效 | CODE | CONSIST | IDs unique and severity-independent |
| PR-041 | 跨專案術語或相似名稱造成歧義 | PROCESS |  | terminology disambiguation is editorial |
| PR-042 | 把研究／文件完整誤認為實作與驗收完成 | CODE | EVID | PROGRAM_TEST/RUNTIME_OBSERVATION need run_id/command; maturity labels separate research from execution |
| PR-043 | 索引、路徑或連結失效 | CODE | CONSIST |  |
| PR-044 | 命名、顯示或分類不一致 | CODE | CONSIST | status vocabulary checked against blueprint |
| PR-045 | 重複提問或過度打斷 | PROCESS |  | behavioral; minimal clarification is not machine-checkable |
| PR-046 | 呈現形式與任務複雜度不匹配 | PROCESS |  | presentation choice (VIEW-010) |
| PR-047 | 文件格式／目錄／描述增加閱讀成本 | PROCESS |  | format/readability is editorial review |
| PR-048 | 新模型、多模態或新協定的導入時機不明 | PROCESS | BASE | introduce only after baseline comparison |
| PR-049 | 低頻特殊領域問題 | SLOT | ROUTE PLUGIN ADAPT | domain adapters plug in via route + plugin_contract |
| PR-050 | 自動修改核心與完全自主演化風險 | CODE | BUNDLE POL | state writer refuses docs/ authority files; protected actions need authorization |
| PR-051 | 為假想需求預建完整抽象 | PROCESS |  | do not pre-build abstractions; enforced by review |
| PR-052 | 缺少 GitHub 可用上下文包造成狀態重建偏差 | CODE | BUNDLE HANDOFF | context bundle exists; no GitHub operations by design |
| PR-053 | 既有治理規則未觸發前置檢查 | CODE | TASK POL | task validated and gate runs before execution |
| PR-054 | 資訊分類、唯一歸位與流程回寫未形成可驗收閉環 | PROCESS | HANDOFF | placement/writeback loop is procedural |

## 功能清單（121）

| ID | 名稱 | 層級 | 處理機制 | 限制／說明 |
|---|---|---|---|---|
| P1-F01 | 資料接收 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F02 | 資料清理 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F03 | 資料切分 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F04 | 資訊元素抽取 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F05 | 屬性抽取 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F06 | 主張／證據區分 | CODE | EVID | claim vs evidence separated by kind/status |
| P1-F07 | 資料編碼 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F08 | 分類／重新分類 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F09 | 新類別發現 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F10 | 資料缺口辨識 | CODE | CRIT_UNK | critical unknowns block high-risk tasks |
| P1-F11 | 共現 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F12 | 方向 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F13 | 條件 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F14 | 依賴 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F15 | 衝突／支持 | CODE | CONFLICT |  |
| P1-F16 | 時間 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F17 | 關係強度 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F18 | 關係鏈 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F19 | 頻率模式 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F20 | 共同特徵 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F21 | 差異模式 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F22 | 趨勢 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F23 | 群組 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F24 | 條件模式 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F25 | 週期 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F26 | 異常 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F27 | 例外 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F28 | 反常組合 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F29 | 歸納 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F30 | 模式解釋 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F31 | 假設建立 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F32 | 支持證據檢查 | CODE | EVID |  |
| P1-F33 | 反例搜尋 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F34 | 替代解釋 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F35 | 假設範圍限制 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F36 | 假設修正 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F37 | 假設比較 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F38 | 證據—推論鏈 | CODE | EVID | criteria results must cite linked OBSERVED evidence |
| P1-F39 | 小結論 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F40 | 小結論檢查 | CODE | UNK |  |
| P1-F41 | 新問題生成 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F42 | 缺口優先級 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F43 | 迭代控制 | CODE | RETRY |  |
| P1-F44 | 跨輪合併 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F45 | 結論穩定度 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F46 | 未解問題保留 | CODE | UNK | unknowns preserved |
| P1-F47 | 最終結論整合 | SLOT | EVID ADAPT | analysis content supplied by evidence/frame/evaluate adapters |
| P1-F48 | 完整回溯 | CODE | RUNREC BUNDLE | trace + receipts + checkpoint |
| P2-F01 | 問題輸入封包與限制 | CODE | TASK |  |
| P2-F02 | Brain Proposal 驗證／轉成 Command | CODE | ROUTE | route contract validated before execution |
| P2-F03 | Planner／Capability Cards | CODE | PLUGIN |  |
| P2-F04 | Method／Pattern 到 Task Set | SLOT | ROUTE ADAPT |  |
| P2-F05 | Central 路由與狀態轉移 | CODE | ROUTE FEEDBACK |  |
| P2-F06 | Role 隔離與獨立驗收 | PROCESS |  | roles are logical only |
| P2-F07 | Current State、必要狀態轉移與執行真相 | CODE | RUNREC |  |
| P2-F08 | 知識匯入與來源追溯 | SLOT | EVID ADAPT |  |
| P2-F09 | 知識檢索、Context、失憶恢復 | CODE | BUNDLE |  |
| P2-F10 | 程式重建 Blueprint 與乾淨重建 | PROCESS |  | rebuild is manual |
| P2-F11 | 來源／結果生命週期與封存治理 | PROCESS |  | lifecycle/archive procedure |
| P2-F12 | 外部工具雷達與 Provider | SLOT | PLUGIN ADAPT |  |
| P2-F13 | 自我評估、變更影響與演進回退 | CODE | CORR |  |
| P2-F14 | Current／文件投影／交接一致性 | CODE | CONSIST HANDOFF |  |
| P2-F15 | 最低操作驗收與故障歸因 | CODE | BRANCH | failure_branch + failure_class |
| P2-F16 | AI 對話＋GitHub 最低操作模式 | PROCESS |  | chat+GitHub minimal mode is operational |
| P2-F17 | Current-first 狀態與資料生命週期 | CODE | BUNDLE |  |
| P2-F18 | 必要能力納入與退場治理 | PROCESS | PLUGIN | intake/retire is procedural |
| P2-F19 | UNKNOWN 觸發的針對性診斷與補救 | CODE | UNK FEEDBACK |  |
| P2-F20 | 系統建置工廠：按證據選擇 BUILD／REPAIR／EX | PROCESS |  | BUILD/REPAIR/EXTEND selection by owner/agent |
| P2-F21 | Brain 常態認知控制：架構／模式選擇、研究式根因診斷 | SLOT | ROUTE ADAPT |  |
| P2-F22 | 根因證據蒸餾與失效證據回收 | CODE | CORR |  |
| P2-F23 | 思考／施工隔離、獨立系統與乾淨交接口 | PROCESS |  | think/build isolation is operational |
| P2-F24 | 使用者意圖理解、語意歧義偵測與最小化澄清 | SLOT | FRAME ADAPT |  |
| P2-F25 | 蒸餾操作包生成、增量重建與 Code-first 工作閉 | PROCESS |  | distillation pack is manual |
| P2-F26 | 整批更新、語意保真與單次手動整合驗收治理 | PROCESS | CONSIST | batch update + one manual integration acceptance (build_stage_flow) |
| P2-F27 | 適應式呈現、圖表即程式碼與設計到可驗收程序的可追溯性 | PROCESS |  | presentation chosen per reader/purpose (VIEW-010) |
| P2-F28 | 系統性變更分類、職權路由、藍圖演進、需求優先級排序與規則 | PROCESS | CORR | classification manual; impact set automated |
| P2-F29 | 事件觸發式施工健康回溯與維護資源預算 | CODE | RETRY | budget only |
| P2-F30 | 四階段批次治理與受控藍圖更新交易（Batch Phase | PROCESS | BASE | four-stage governance is the operating flow; FINAL_TEST harness exists |
| CF-001 | 問題屬性判定與方法路由 | CODE | ROUTE |  |
| CF-002 | 原始資料／封裝檔解析 | SLOT | EVID ADAPT |  |
| CF-003 | 跨文件去重與蒸餾 | SLOT | EVID ADAPT |  |
| CF-004 | 對話成果轉成可追溯文件 | PROCESS | HANDOFF | dialog -> traceable doc via handoff template; manual |
| CF-005 | 問題登錄與追蹤 | CODE | CORR | problem ID reuse |
| CF-006 | 版本治理與備份輪替 | PROCESS |  | version governance & backup rotation: SOP in archive (registry source_status); manual, zip chain as backup |
| CF-007 | 主軸彙整與長度分流 | PROCESS |  | axis consolidation and length split: editorial SOP |
| CF-008 | 雙向引用與追溯更新 | CODE | CONSIST |  |
| CF-009 | SOP 固定流程與演化管理 | PROCESS |  | SOP fixed-flow evolution: SOP-META-001 procedure |
| CF-010 | SOP 建檔與對話蒸餾 | PROCESS |  | SOP creation/dialog distillation: SOP-DOC-001 procedure |
| SOP-CAND-005 | 意圖、既有職責與衝突的前置掃描 | PROCESS | POL CONSIST | pre-scan of intent/duties/conflicts: preflight checklist; gate+consistency checker partly automate |
| SOP-CAND-006 | 問題到控制再到回歸的閉環 | CODE | CORR |  |
| SOP-CAND-007 | 變更影響與完成閘門 | CODE | CORR |  |
| SOP-CAND-008 | 一致性靜態檢查 | CODE | CONSIST |  |
| SOP-CAND-009 | 改善成效基線與回歸量測 | CODE | BASE |  |
| SOP-CAND-010 | 重大決策紀錄 | CODE | HANDOFF |  |
| SOP-CAND-011 | 先批判框架再細化 | SLOT | FRAME ADAPT |  |
| SOP-CAND-012 | 自我更新控制面與回歸閘門 | CODE | BUNDLE BASE |  |
| SOP-META-001 | SOP 固定流程與演化管理 | PROCESS |  | SOP lifecycle procedure; owner-governed |
| SOP-DOC-001 | SOP 文件標準欄位與蒸餾建置流程 | PROCESS |  | SOP document standard fields; template-driven |
| VIEW-001 | 機器可讀功能登錄（JSON） | CODE | CONSIST |  |
| VIEW-002 | 人類可讀 HUD／功能面板（Markdown） | PROCESS |  | human HUD/panel in markdown: generated on demand by tools/coverage.py --md |
| VIEW-003 | 雙視圖一致性與差異檢查 | CODE | CONSIST |  |
| VIEW-004 | 樹狀圖與關係圖雙圖合約 | PROCESS |  | tree/relationship diagrams drawn on request from index.json |
| VIEW-005 | 來源／實作／測試／Runtime 分層狀態 | PROCESS |  | maturity layers live in blueprint.maturity |
| VIEW-006 | P1/P2 功能到 forAVAr 四層的雙向映射 | CODE | COVER |  |
| VIEW-007 | SOP／問題修正／新增功能分流標籤 | PROCESS |  | SOP/problem-fix/new-feature routing tags: applied by reviewer |
| VIEW-008 | 問題→控制點→回歸／復發檢查追溯 | CODE | COVER |  |
| VIEW-009 | 前置檢查：權威、唯一責任、衝突和影響範圍 | CODE | POL |  |
| VIEW-010 | 適應式呈現：依讀者／用途選文字、表格或圖 | PROCESS |  | adaptive presentation: reviewer/agent judgement |
| VIEW-011 | 能力採納／合併／替代／退場決策 | PROCESS |  | capability adopt/merge/replace/retire decision procedure; owner-governed |
| VIEW-012 | 文件權威與藍圖狀態鎖定 | CODE | BUNDLE CONSIST |  |
| CORE-001 | L1 核心：思考不變量 | CODE | ROUTE FEEDBACK |  |
| RENDER-001 | L2 主軸：第一次渲染 A1–A6 | CODE | FRAME EVID |  |
| SKELETON-001 | L3 骨架：十八個節點 N01–N18 | CODE | ROUTE EXEC |  |
| FRAMEWORK-001 | L4 框架：條件式流程 F0–F7 | CODE | FEEDBACK |  |
| DISC-SOP-001 | 前置閘門的文件歸位 | PROCESS |  | ruled: shared preflight segment, no standalone SOP (B13, by delegation) |
| DISC-SOP-002 | ADR／決策紀錄範圍 | PROCESS |  | ruled: ADR only for architecture/governance/vocabulary/authority (B13, by delegation) |
| DISC-SOP-003 | 自動化方式 | PROCESS |  | ruled: stdlib scripts primary, manual checklist secondary (B13, by delegation) |
| DISC-SOP-005 | 獨立審查角色 | PROCESS |  | ruled: L3 needs user approval + logical review (B13, by delegation) |
| DISC-SOP-006 | 流程分級與例外 | PROCESS |  | ruled: FAST default; full scan only L3/authority/protected/critical UNKNOWN (B13, by delegation) |
| DISC-SOP-007 | 自動自我維護的授權邊界 | PROCESS | POL | ruled: propose+sandbox-test automatic; authority writes need user approval (B13, by delegation) |
| DISC-SOP-004 | 回歸樣本與量測門檻 | CODE | BASE | ruled: harness rubric + sample kinds formally adopted (B13) |

## 流程清單（44）

| ID | 名稱 | 層級 | 處理機制 | 限制／說明 |
|---|---|---|---|---|
| F0 |  | CODE | TASK POL |  |
| F1 |  | CODE | FRAME |  |
| F2 |  | CODE | EVID CRIT_UNK |  |
| F3 |  | CODE | ROUTE RETRY |  |
| F4 |  | CODE | POL CANCEL EXEC RUNREC |  |
| F5 |  | CODE | UNK BRANCH FEEDBACK |  |
| F6 |  | CODE | BUNDLE HANDOFF | GitHub writeback is manual |
| F7 |  | CODE | FEEDBACK BASE | real C0/C1/C2 evaluation NOT_EXECUTED |
| N01 |  | CODE | TASK |  |
| N02 |  | SLOT | FRAME ADAPT |  |
| N03 |  | SLOT | FRAME ADAPT |  |
| N04 |  | SLOT | EVID ADAPT |  |
| N05 |  | CODE | EVID |  |
| N06 |  | CODE | CRIT_UNK CONFLICT |  |
| N07 |  | SLOT | EVID ADAPT |  |
| N08 |  | SLOT | EVID ADAPT |  |
| N09 |  | CODE | RETRY | discriminating_change recognised as retry justification |
| N10 |  | CODE | TASK FAST |  |
| N11 |  | CODE | ROUTE |  |
| N12 |  | CODE | RETRY |  |
| N13 |  | CODE | EXEC |  |
| N14 |  | CODE | BUNDLE |  |
| N15 |  | SLOT | FEEDBACK ADAPT |  |
| N16 |  | CODE | UNK EVID |  |
| N17 |  | CODE | CORR BRANCH |  |
| N18 |  | CODE | FEEDBACK BUNDLE HANDOFF |  |
| A1 |  | CODE | FRAME TASK |  |
| A2 |  | CODE | EVID |  |
| A3 |  | SLOT | EVID ADAPT |  |
| A4 |  | CODE | ROUTE RETRY |  |
| A5 |  | CODE | EXEC RUNREC |  |
| A6 |  | CODE | UNK BRANCH CORR FEEDBACK |  |
| TASKFLOW:INTAKE |  | CODE | TASK |  |
| TASKFLOW:AUTHORIZE |  | CODE | POL |  |
| TASKFLOW:SELECT_SOP |  | SLOT | ROUTE ADAPT |  |
| TASKFLOW:PLAN |  | SLOT | ROUTE ADAPT |  |
| TASKFLOW:EXECUTE |  | CODE | EXEC RUNREC |  |
| TASKFLOW:VERIFY |  | CODE | UNK EVID |  |
| TASKFLOW:PERSIST |  | CODE | BUNDLE TXN | persist_checkpoint: bundle+handoff written as one transaction |
| TASKFLOW:REVIEW |  | PROCESS | BASE | independent review is manual |
| STAGE:PLANNING |  | PROCESS | CORR | impact planning automated; plan authoring manual |
| STAGE:REALIZATION |  | CODE | CONSIST |  |
| STAGE:CLOSURE |  | CODE | CONSIST |  |
| STAGE:FINAL_TEST |  | CODE | BASE | harness only; real run is batch 4 (FINAL_TEST), NOT_EXECUTED |
