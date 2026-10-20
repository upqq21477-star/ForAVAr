# EVT-0017｜WebToApp 逆向分析長報告分流

- EVENT_ID：EVT-0017
- 狀態：VERIFIED（原 9 個章節逐節對帳至三個分支）
- 日期：2026-10-21（Asia/Taipei）
- DOC_ID：FORAVAR-TOPIC-WEBTOAPP-001
- 原始路徑：`參考資料/逆向工具/WebToApp_逆向分析.md`
- 唯一主軸：[WebToApp 逆向分析主軸](../WebToApp_主軸彙整.md)
- 全域索引：[文件與分支索引](../文件與分支索引.md)
- 規範：[版本治理與分流規範](../版本治理與分流規範.md)

## 目錄與索引

1. [現況與分流方案](#1-現況與分流方案)
2. [保留規則](#2-保留規則)
3. [驗收條件](#3-驗收條件)

## 1. 現況與分流方案

- 原報告 10899 原始字元／10610 字元（不計 CR/LF），超過 8,000 字元硬上限。
- 分支一：重要摘要、系統全貌、核心程式與資料／設定／APK 建置追蹤。
- 分支二：架構品質、Android 平台限制、WebView/TLS/擴充功能安全。
- 分支三：測試證據、現代化路線與總結。
- 原路徑保留為 canonical MASTER，原章節標題／錨點保留作相容索引；現有根目錄摘要改作 ALIAS。

## 2. 保留規則

- 分流前全文保存為 BACKUP_ONLY；原始來源、程式路徑、欄位、URL、限制和未驗證事項不得蒸餾掉。
- 每個 BRANCH 保留一個 CURRENT 及最多兩個舊版；SOURCE 與原始附件不計為 MASTER 版本。
- 日常索引只指向 MASTER；詳細分支由 MASTER 導航，分支回鏈 MASTER。

## 3. 驗收條件

- 各分支有摘要／TOC／主軸回鏈，且低於 8,000 字元；MASTER 低於 6,000 字元。
- 原 9 個主要章節全部在分支全文中找到；主軸保留所有原章節標題／錨點。
- 寫後讀回、路徑核對及全域索引更新完成後才將事件標記 VERIFIED。


## 實際交付與驗收

| 交付物 | 提交 | 字元數（不計 CR/LF）／結果 |
|---|---|---|
| 分流前完整報告 BACKUP_ONLY | [d1e6920](https://github.com/upqq21477-star/ForAVAr/commit/d1e69202b20ca8f30653bf5ebe093501e1c5643f) | 10,610；備份正文與變更前原文一致 |
| 系統全貌與核心程式 | [bcebb2a](https://github.com/upqq21477-star/ForAVAr/commit/bcebb2ad202ea84d19544e92d071d41c59935fc7) | 5,096；原重要摘要及第 1–2 節保留 |
| 架構平台與安全 | [22a7dbf](https://github.com/upqq21477-star/ForAVAr/commit/22a7dbfbd789415302c13be5c7fc1b881e77a112) | 4,836；原第 3–5 節保留 |
| 測試與現代化路線 | [78abf55](https://github.com/upqq21477-star/ForAVAr/commit/78abf55c06f68b6a83719d548ee2e3c093a086d5) | 1,824；原第 6–8 節保留 |
| 現行 MASTER | [d7424fd](https://github.com/upqq21477-star/ForAVAr/commit/d7424fd256561c9d76d4c7fabba1c938222b1616) | 2,281；原 9 個 H2 標題及相容錨點保留 |
| 舊主軸入口 ALIAS | [2b2493f](https://github.com/upqq21477-star/ForAVAr/commit/2b2493f849b989de56934ec8dc5016712e4b219b) | 不再作第二份主軸 |
| 全域索引 | [bd4a92a](https://github.com/upqq21477-star/ForAVAr/commit/bd4a92a9efa0854333ac06a16564211d72429387) | EXT-002 已導向 canonical MASTER |

- 九個原章節逐節正文包含檢查全部通過。
- 三個分支都有 TOC、主軸回鏈，均低於 8,000 字元；MASTER 低於 6,000 字元。
- 靜態逆向研究不等於程式已被實際執行或已在真機驗收。
