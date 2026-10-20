# 封包 B｜DOCX 內層 OOXML 結構與範圍驗收

> 主軸回鏈：[壓縮檔解析總覽與文件導航](./壓縮檔逆向分析與蒸餾紀錄.md) ｜ 分支 ID：ARCHIVE-B-BR-004 ｜ 本回鏈只提供導航，不改變本文件的證據邊界。

- **稽核日期：** 2026-10-20
- **範圍：** 兩份 DOCX 的內層 ZIP、CRC、OOXML 部件、relationship targets、Content Types、主文件表格／正文抽取範圍，以及文件內部目錄連結。
- **來源 DOCX Blob SHA：** 對話紀錄 `6dccf5c5921f5d78087b4b20226c598dda616688`；企劃書 v0.1 `ae17de3f93355554c6d9c472bee7c1aa87fa94f4`.

## 1. 結論

**OOXML 結構：PASS。標題／表格：PASS。指定範圍內的正文差異裁定：PASS（有序字元差異均已分類）。**

兩份 DOCX 各有 17 個 OOXML 部件；所有成員大小／CRC、28 個內部關係目標及 Content Types 宣告均通過。企劃書 DOCX 的 20 個內部 TOC anchor 全部指向存在的 bookmark。對話紀錄的五個歷史 sandbox URL 字串可在主文件中找到，但 DOCX 沒有 hyperlink 元素或外部關係，因此網址文字保留、可點擊功能未保留。

此結論不宣稱 Markdown 與 DOCX 原始字元逐字完全相同，也不回補來源原本沒有的對話文字。訊息 1 前的助理回覆缺口仍由 GAP-001 追蹤。

## 2. 內層 ZIP／主文件結構

| DOCX | 外部檔案大小 | OOXML 部件數 | 部件大小／CRC | 非空主文件段落 | 表格／列／儲存格 |
|---|---:|---:|---|---:|---|
| 對話原文紀錄 | 32,555 bytes | 17 | 17/17 PASS | 444 | 9 / 59 / 123 |
| 企劃書 v0.1 | 36,445 bytes | 17 | 17/17 PASS | 591 | 4 / 78 / 256 |

兩份文件的內層 ZIP 均已逐件解壓；實際輸出長度與中央目錄記錄一致，CRC32 全部通過。

## 3. Relationship targets

| DOCX | 關係數 | 內部關係 | 外部關係 | 缺失內部目標 | 判定 |
|---|---:|---:|---:|---:|---|
| 對話原文紀錄 | 14 | 14 | 0 | 0 | PASS |
| 企劃書 v0.1 | 14 | 14 | 0 | 0 | PASS |
| **合計** | **28** | **28** | **0** | **0** | **PASS** |

每個內部 Target 均依來源關係檔位置正規化解析，並於 ZIP 成員清單中找到目標。關係涉及 office document、properties、styles、numbering、settings、theme、footnotes、comments、header、footer 等部件。

## 4. Content Types

| DOCX | Default 宣告 | Override 數 | 缺少 Content Type 的部件 | 指向不存在部件的 Override | 判定 |
|---|---|---:|---:|---:|---|
| 對話原文紀錄 | rels、xml | 14 | 0 | 0 | PASS |
| 企劃書 v0.1 | rels、xml | 14 | 0 | 0 | PASS |

每個實際部件均有可用的 Content Type；所有 Override 均指向存在的封裝部件。每份文件各有 2 種 Default 型別與 14 個 Override。

## 5. 表格、標題與內部目錄連結

| 檢查 | 對話紀錄 | 企劃書 v0.1 |
|---|---:|---:|
| Markdown 標題覆蓋 | 75/75 | 72/72 |
| 表格數 | 9 | 4 |
| 表格列 | 59 | 78 |
| 儲存格 | 123 | 256 |
| 正規化儲存格文字差異 | 0 | 0 |
| 內部 TOC anchor | 不適用於此表 | 20/20 targets 存在 |

合計 13 張表、137 列、379 個儲存格；列／欄結構與正規化文字差異均為 0。企劃書的 20 個 anchor 都對應到存在的 bookmark，未找到缺失內部導覽目標。

## 6. 非主文件部件與超連結範圍

- 兩份 DOCX 的註腳與註解 XML 均無文字。
- 兩份頁首文字為「P2 封包式問題解決架構｜討論整理稿」；頁尾文字為「P2 討論稿 •」。它們是 Word 版面識別資訊，不是未轉入的 Markdown 正文。
- 對話紀錄 Markdown 有五個 sandbox URL。五個 URL 字串都在 DOCX 主文件文字中，但 DOCX 有 0 個 hyperlink 元素、0 個外部 relationship；因此保留的是純文字，不是可點擊連結。
- 企劃書沒有外部 OOXML relationship。其內部 TOC 導覽已按第 5 節逐一核對。

## 7. 與正文差異報告的關係

非表格正文已用 NFKC、去除空白／標點／符號後做有序字元序列 diff。結果與差異分類詳見「封包B雙格式完整性與差異稽核.md」§9.6：

- 對話紀錄：Markdown 10,502 字元、DOCX 10,642 字元，共同有序字元 10,463；差異分類為 Word 編號、連結顯示／可點擊功能、短標籤及少量範圍措辭。
- 企劃書：Markdown 9,887 字元、DOCX 9,923 字元；Markdown 字元均被保留於共同有序序列，DOCX 額外 36 字元對應 Word 標題／層級編號。
- 差異全部已分類，在指定抽取與正規化範圍內未發現未解釋的實質內容缺失。這不等於兩格式原始字元逐字相同。

## 8. 證據邊界與專案權限

CRC／關係目標通過只證明 OOXML 套件結構完整，不證明外部 sandbox 目標仍可使用、歷史聊天來源零遺漏或提案已被 P2 採用。

固定差異標記：
- ERR-001：訊息 13／15 的範圍措辭歧義（SCOPE_CLARIFICATION）。
- GAP-001：訊息 1 前的助理回覆只有片段（KNOWN_GAP）。
- FMT-001：五個 sandbox URL 失去可點擊連結功能（CONFIRMED_FORMAT_LOSS）。
- GAP-002：指定範圍內差異已分類，判定 RESOLVED_WITH_LIMITATIONS。

只修改 forAVAr；P1、P2 僅作唯讀參考。
