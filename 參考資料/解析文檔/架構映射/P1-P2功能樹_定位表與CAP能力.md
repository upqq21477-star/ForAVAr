# P1／P2 功能骨架樹分支｜P1／P2 功能定位表與 CAP 能力

- 文件 ID：FORAVAR-FUNCTION-TREE-MAPPING-001
- 類型：BRANCH
- 狀態：CURRENT／forAVAr 內的唯讀參考映射
- 唯一責任：保存功能定位／能力登錄／Current 控制／責任邊界所指定內容。
- 主軸回鏈：[P1／P2 功能骨架樹主軸](./P1-P2-功能骨架樹-全面重整版.md)
- 使用邊界：P1、P2 repository 唯讀；本映射不等於功能接線或 Runtime 驗收。
- 追溯：[變更追溯總表](../../變更追溯總表.md)

## 目錄與索引

- [3. P1 48 項功能定位對照](#section-1)
- [4. P2-F01～P2-F30 功能定位對照](#section-2)
- [5. CAP 能力登錄對照](#section-3)

---

<a id="section-1"></a>
## 3. P1 48 項功能定位對照

以下用來驗證原始 P1 A1 Function 全部有主要歸位；實際 H3 編號依上方分支內局部序號為準。

- `P1 A1-F01` 資料接收 → `H2-02-05`；`CAP-INGEST`。
- `P1 A1-F02` 資料清理 → `H2-02-05`；`CAP-INGEST`。
- `P1 A1-F03` 資料切分 → `H2-02-05`；`CAP-INGEST`。
- `P1 A1-F04` 資訊元素抽取 → `H2-02-05`；`CAP-EXTRACT`。
- `P1 A1-F05` 屬性抽取 → `H2-02-05`；`CAP-EXTRACT`。
- `P1 A1-F06` 主張／證據區分 → `H2-02-05`；`CAP-EVIDENCE`。
- `P1 A1-F07` 資料編碼 → `H2-02-05`；`CAP-INGEST`。
- `P1 A1-F08` 分類／重新分類 → `H2-02-05`；`CAP-CLASSIFY`。
- `P1 A1-F09` 新類別發現 → `H2-02-05`；`CAP-CLASSIFY`。
- `P1 A1-F10` 資料缺口辨識 → `H2-02-05`；`CAP-GAP`。
- `P1 A1-F11` 共現關係分析 → `H2-02-06`；`CAP-RELATION`。
- `P1 A1-F12` 方向關係分析 → `H2-02-06`；`CAP-RELATION`。
- `P1 A1-F13` 條件關係分析 → `H2-02-06`；`CAP-RELATION`。
- `P1 A1-F14` 依賴關係分析 → `H2-02-06`；`CAP-RELATION`。
- `P1 A1-F15` 衝突／支持分析 → `H2-02-06`；`CAP-RELATION`。
- `P1 A1-F16` 時間順序分析 → `H2-02-06`；`CAP-TEMPORAL`。
- `P1 A1-F17` 關係強度統計 → `H2-02-06`；`CAP-STATISTICS`。
- `P1 A1-F18` 關係鏈分析 → `H2-02-06`；`CAP-GRAPH`。
- `P1 A1-F19` 頻率模式 → `H2-02-07`；`CAP-STATISTICS`。
- `P1 A1-F20` 共同特徵 → `H2-02-07`；`CAP-PATTERN`。
- `P1 A1-F21` 差異模式 → `H2-02-07`；`CAP-PATTERN`。
- `P1 A1-F22` 趨勢 → `H2-02-07`；`CAP-TREND`。
- `P1 A1-F23` 群組／分群 → `H2-02-07`；`CAP-CLUSTER`。
- `P1 A1-F24` 條件模式 → `H2-02-07`；`CAP-PATTERN`。
- `P1 A1-F25` 週期 → `H2-02-07`；`CAP-TEMPORAL`。
- `P1 A1-F26` 異常 → `H2-02-07`；`CAP-ANOMALY`。
- `P1 A1-F27` 例外 → `H2-02-07`；`CAP-PATTERN`。
- `P1 A1-F28` 反常組合 → `H2-02-07`；`CAP-PATTERN`。
- `P1 A1-F29` 歸納 → `H2-02-08`；`CAP-HYPOTHESIS`。
- `P1 A1-F30` 模式解釋 → `H2-02-08`；`CAP-HYPOTHESIS`。
- `P1 A1-F31` 假設建立 → `H2-02-08`；`CAP-HYPOTHESIS`。
- `P1 A1-F32` 支持證據檢查 → `H2-02-08`；`CAP-EVIDENCE`。
- `P1 A1-F33` 反例搜尋 → `H2-02-08`；`CAP-COUNTEREXAMPLE`。
- `P1 A1-F34` 替代解釋 → `H2-02-08`；`CAP-HYPOTHESIS`。
- `P1 A1-F35` 假設範圍限制 → `H2-02-08`；`CAP-HYPOTHESIS`。
- `P1 A1-F36` 假設修正 → `H2-02-08`；`CAP-HYPOTHESIS`。
- `P1 A1-F37` 假設比較 → `H2-02-08`；`CAP-HYPOTHESIS`。
- `P1 A1-F38` 證據—推論鏈 → `H2-02-08`；`CAP-PROVENANCE`。
- `P1 A1-F39` 小結論 → `H2-02-09`；`CAP-SYNTHESIS`。
- `P1 A1-F40` 小結論檢查 → `H2-02-09`；`CAP-VERIFY`。
- `P1 A1-F41` 新問題生成 → `H2-02-09`；`CAP-ITERATE`。
- `P1 A1-F42` 缺口優先級 → `H2-02-09`；`CAP-GAP`。
- `P1 A1-F43` 迭代控制 → `H2-02-09`；`CAP-ITERATE`。
- `P1 A1-F44` 跨輪合併 → `H2-02-09`；`CAP-ITERATE`。
- `P1 A1-F45` 結論穩定度 → `H2-02-09`；`CAP-VERIFY`。
- `P1 A1-F46` 未解問題保留 → `H2-02-09`；`CAP-GAP`。
- `P1 A1-F47` 最終結論整合 → `H2-02-09`；`CAP-SYNTHESIS`。
- `P1 A1-F48` 完整回溯 → `H2-02-09`；`CAP-PROVENANCE`。

<a id="section-2"></a>
## 4. P2-F01～P2-F30 功能定位對照

- `P2-F01` 問題輸入封包與限制 → `H2-01-02`。
- `P2-F02` Brain Proposal 驗證／轉成 Command → `H2-05-16`。
- `P2-F03` Planner／Capability Cards → `H2-04-14`。
- `P2-F04` Method／Pattern 到 Task Set → `H2-04-13`。
- `P2-F05` Central 路由與狀態轉移 → `H2-05-19`。
- `P2-F06` Role 隔離與獨立驗收 → `H2-05-17`。
- `P2-F07` Current State、必要狀態轉移與執行真相 → `H2-07-23`。
- `P2-F08` 知識匯入與來源追溯 → `H2-03-12`。
- `P2-F09` 知識檢索、Context、失憶恢復 → `H2-07-24`。
- `P2-F10` 程式重建 Blueprint 與乾淨重建 → `H2-06-21`。
- `P2-F11` 來源／結果生命週期與封存治理 → `H2-09-32`。
- `P2-F12` 外部工具雷達與 Provider → `H2-09-30`。
- `P2-F13` 自我評估、變更影響與演進回退 → `H2-09-31`。
- `P2-F14` Current／文件投影／交接一致性 → `H2-07-23`。
- `P2-F15` 最低操作驗收與故障歸因 → `H2-08-26`。
- `P2-F16` AI 對話＋GitHub 最低操作模式 → `H2-07-25`。
- `P2-F17` Current-first 狀態與資料生命週期 → `H2-09-32`。
- `P2-F18` 必要能力納入與退場治理 → `H2-09-30`。
- `P2-F19` UNKNOWN 觸發的針對性診斷與補救 → `H2-08-28`。
- `P2-F20` 系統建置工廠：BUILD／REPAIR／EXTEND／REBUILD → `H2-04-15`。
- `P2-F21` Brain 常態認知控制與 THINKING↔CONSTRUCTION 切換 → `H2-01-04`。
- `P2-F22` 根因證據蒸餾與失效證據回收 → `H2-08-28`。
- `P2-F23` 思考／施工隔離、獨立系統與乾淨交接口 → `H2-05-17`。
- `P2-F24` 使用者意圖理解、歧義偵測與最小化澄清 → `H2-01-01`。
- `P2-F25` 蒸餾操作包生成、增量重建與 Code-first 閉環 → `H2-06-22`。
- `P2-F26` 整批更新、語意保真與單次整合驗收治理 → `H2-09-31`。
- `P2-F27` 適應式呈現、圖表即程式碼與可追溯性 → `H2-10-34`。
- `P2-F28` 系統性變更分類、職權路由、藍圖演進、需求排序與規則蒸餾 → `H2-09-31`。
- `P2-F29` 事件觸發式施工健康回溯與維護資源預算 → `H2-09-29`。
- `P2-F30` 四階段批次治理與受控藍圖更新交易 → `H2-09-31`。

<a id="section-3"></a>
## 5. CAP 能力登錄對照

P1/P2 的能力登錄是橫切能力，不等同於新的 H1/H2。以下列出 P2 目前 23 個 CAP，並對應其主要功能節點。

- `CAP-INGEST`：資料接收、清理、切分與穩定編碼 → `H2-02-05`。
- `CAP-SEARCH`：外部／庫外來源搜尋 → `H2-03-10`。
- `CAP-EXTRACT`：結構化欄位與事實片段抽取 → `H2-02-05`。
- `CAP-CLASSIFY`：分類與類別候選 → `H2-02-05`。
- `CAP-RELATION`：關係擷取與端點正規化 → `H2-02-06`。
- `CAP-TEMPORAL`：時間、區間與先後計算 → `H2-02-06`。
- `CAP-GRAPH`：關係圖、路徑與循環 → `H2-02-06`。
- `CAP-STATISTICS`：描述統計與頻率 → `H2-02-07`。
- `CAP-CLUSTER`：特徵分群 → `H2-02-07`。
- `CAP-TREND`：時間序列趨勢 → `H2-02-07`。
- `CAP-ANOMALY`：偏離基準的項目偵測 → `H2-02-07`。
- `CAP-EVIDENCE`：支持／反駁證據整理 → `H2-03-11`。
- `CAP-PROVENANCE`：來源追溯鏈 → `H2-03-11`。
- `CAP-VERIFY`：獨立驗收與判決 → `H2-08-26`。
- `CAP-SYNTHESIS`：已驗證材料整合 → `H2-02-09`。
- `CAP-COUNTEREXAMPLE`：反例搜尋 → `H2-02-08`。
- `CAP-GAP`：缺口、未解問題與優先級 → `H2-02-09`。
- `CAP-PATTERN`：共同特徵、差異、條件、例外、反常組合 → `H2-02-07`。
- `CAP-HYPOTHESIS`：假設建立、批判、替代解釋、修正 → `H2-02-08`。
- `CAP-ITERATE`：新問題、迭代與跨輪合併 → `H2-02-09`。
- `CAP-CONVERSATION-RECORD`：討論／會議紀錄及迭代合併 → `H2-10-33`。
- `CAP-INSTRUCTION-ROUTING`：指令配置、習慣詞及啟動路由 → `H2-10-33`。
- `CAP-RETIRE`：受限批次退場 → `H2-09-32`。
