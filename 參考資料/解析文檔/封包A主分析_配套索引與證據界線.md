# 封包 A 主分析分支｜配套索引、證據界線與外部研究

- 文件 ID：FORAVAR-ARCHIVE-A-BR-003
- 類型：BRANCH
- 狀態：CURRENT／封包 A 靜態分析；結論受列明證據範圍限制
- 唯一責任：保存封包 A 主報告指定章節的完整數據、來源、狀態與限制。
- 主軸回鏈：[封包 A 實體解析與完整性驗收主軸](./封包A_R3d130j_實體壓縮檔解析與完整性驗收_2026-10-21.md)
- 上層主軸：[壓縮檔解析總覽](./壓縮檔逆向分析與蒸餾紀錄.md)
- 追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [7. 相關文件與資料產物索引](#section-1)
- [8. 本次完成、未完成與證據界線](#section-2)
- [9. 外部研究入口](#section-3)

---

<a id="section-1"></a>
## 7. 相關文件與資料產物索引

| 文件 | 唯一用途 |
|---|---|
| [原始 ZIP（P2 唯讀來源）](https://github.com/upqq21477-star/P2/blob/main/%E5%8F%83%E8%80%83%E8%B3%87%E6%96%99/P2-relay-R3d130j.zip) | 封包 A 原件回查入口；forAVAr `main` 只保留驗證資料、分析與分類骨架，不保留二進位副本 |
| [S 級問題清單](../%28S級%29問題清單.md) | PR-052 及其與 PR-001／004／005／019／021／016／023／042／043 的關係；完整根因、證據與處理方向集中於此 |
| [P2 核心主軸漂移根因與防偏離架構驗證](./P2核心主軸漂移根因與forAVAr防偏離架構驗證_2026-10-21.md) | 外部研究與整體架構有效性裁定摘要；根因細節不在此重複 |
| [P2 核心漂移根因分解與權威狀態核對](./P2核心漂移_根因分解與下一步權威狀態核對_2026-10-21.md) | Current／Work／Feature Batch／HANDOFF 權威映射簡述 |
| [State Bundle 最小資料契約草案](./可攜式StateBundle最小資料契約與防漂移反例驗收草案_v0.1.md) | 候選資料契約、載入條件、Core-Drift Gate 和 DRIFT-01～DRIFT-10 |
| [State Bundle 快照實例](./StateBundle_實例_P2-relay-R3d130j_2026-10-21.json) | 依本次 ZIP 建立的離線 JSON；狀態為 CONFLICT，只供只讀分析 |
| [State Bundle 結構核對紀錄](./StateBundle_實例初次結構核對紀錄_2026-10-21.md) | JSON 的 19 項結構自洽檢查；不是行為驗收 |
| [Claude 離線接手摘要](./P2-relay-R3d130j_Claude離線接手摘要_2026-10-21.md) | 無 GitHub 連線的新會話快速載入；不取代來源指紋或權威資料 |
| 完整 774 項成員清冊 | 以本次對話提供的 CSV 附件下載；此 CSV 不在 GitHub 參考資料樹內。原始 ZIP 的 Manifest 仍是封包完整性依據。 |

<a id="section-2"></a>
## 8. 本次完成、未完成與證據界線

**已完成：** ZIP 身分比對、CRC／Manifest 驗證、774 項路徑盤點、格式適用的靜態解析、135 個 Schema meta-validation、5 個核心 JSON 指定驗證、Current／工作包／交接狀態核對、已知引用缺口記錄、問題清單及分析索引同步。

**未完成：** P2 程式與測試執行、Runtime 驗收、所有模組的逐行業務語意審查、所有正式 caller 的動態驗證、REF-01／02／03 的 Git 歷史裁定、State Bundle 自動產生／載入與跨會話行為驗收。

因此：
- 不宣稱 P2 程式或 Runtime 已通過。
- 不宣稱 PR-052 已解決。
- 不把此離線 ZIP 當成可證實的最新 GitHub HEAD。
- 不以 State Bundle 結構檢查取代跨會話反例測試。
- 不在本次修改 P1、P2 或 C′ 主企劃本體。

<a id="section-3"></a>
## 9. 外部研究入口

外部研究的來源、適用邊界及主要結論集中於 [P2 核心主軸漂移根因與防偏離架構驗證](./P2核心主軸漂移根因與forAVAr防偏離架構驗證_2026-10-21.md)。核心參考包括：

- [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/)：長上下文資訊位置及取用風險。
- [Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)：結構化、最小充分的上下文管理。
- [Context as a Tool: Context Management for Long-Horizon SWE-Agents](https://aclanthology.org/2026.findings-acl.1032/)：長程程式代理的上下文管理方法。
- [MemTrace: State-Consistent Memory for Long-Horizon Coding Agents](https://arxiv.org/abs/2610.04838)：歷史證據需核對它是否仍對應目前程式狀態；該文為預印本。

**最終裁定：** 封包完整性和所列靜態檢查通過；P2 執行狀態與引用缺口仍待處理。問題詳情以 PR ID 集中管理，本報告只保留摘要、證據基線和搜尋導航。
