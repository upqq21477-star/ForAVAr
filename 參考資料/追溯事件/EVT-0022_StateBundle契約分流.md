# EVT-0022｜State Bundle 最小資料契約草案分流

- EVENT_ID：EVT-0022
- 狀態：VERIFIED（原章節逐節對帳至三個分支）
- 日期：2026-10-21（Asia/Taipei）
- 主題 MASTER：[State Bundle 主軸彙整](../StateBundle_主軸彙整.md)
- 原始文件：`參考資料/解析文檔/可攜式StateBundle最小資料契約與防漂移反例驗收草案_v0.1.md`
- 規範：[版本治理與分流規範](../版本治理與分流規範.md)

## 目錄與索引

1. [基線](#1-基線)
2. [分流方式](#2-分流方式)
3. [驗收條件](#3-驗收條件)

## 1. 基線

- 原稿 9234 原始字元／8970 字元（不計 CR/LF），超過 8,000 字元硬上限。
- 原稿狀態是 PROPOSAL／NOT_APPROVED／NOT_IMPLEMENTED；此分流只改善可讀性與引用，不採納或改變契約語義。
- 原始 JSON 快照、結構核對紀錄與離線摘要是不同資料物件，不與契約草案合併為同一正文。

## 2. 分流方式

- 保留原稿全文為 BACKUP_ONLY。
- 依原章節順序把規格分成三個 BRANCH；分支檔名採中性 A/B/C，具體章節名由目錄和主軸列明。
- 原契約路徑降為 ALIAS／舊入口相容頁；唯一主題入口仍為 State Bundle 主軸彙整。

## 3. 驗收條件

原文標題、欄位、狀態、失效條件、DRIFT 案例、驗收要求、限制和來源完整保留。分支各低於 8,000 字元，State Bundle 主軸低於 6,000 字元；只有讀回與對帳通過後才標記 VERIFIED。


## 實際交付與驗收

- 完整分流前 v0.1 備份：`StateBundle契約_備份_v0.1_分流前.md`，標記 BACKUP_ONLY。
- 原契約路徑已轉為 ALIAS，保留原章節標題與 legacy 錨點；日常索引仍只指向 [State Bundle 主軸彙整](../StateBundle_主軸彙整.md)。
- 分支 A：`StateBundle契約_分支A.md`（2672 字元，不計 CR/LF）。
- 分支 B：`StateBundle契約_分支B.md`（2949 字元，不計 CR/LF）。
- 分支 C：`StateBundle契約_分支C.md`（4934 字元，不計 CR/LF）。
- 原章節逐節正文包含檢查全部通過；三個分支均有 TOC、State Bundle 主軸回鏈並符合 8,000 字元限制。
- 契約語義維持 PROPOSAL／NOT_APPROVED／NOT_IMPLEMENTED，不代表被採納或已運行。
