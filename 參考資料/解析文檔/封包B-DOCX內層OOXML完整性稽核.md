# 封包 B：DOCX 內層 OOXML 結構與關係驗收

- **稽核日期：** 2026-10-20
- **範圍：** 兩份已歸檔 DOCX 的內層 ZIP、OOXML 部件、relationship targets、Content Types 與主文件結構。
- **來源：** 封包 B 原始 ZIP；兩份 DOCX 的 Git Blob SHA 分別為 `6dccf5c5921f5d78087b4b20226c598dda616688`、`ae17de3f93355554c6d9c472bee7c1aa87fa94f4`。

## 1. 結論

兩份 DOCX 均通過內層 ZIP 成員大小與 CRC32 驗證。每份各有 17 個部件，`word/document.xml`、主文件關係檔均存在；每份 14 個 OOXML relationship targets 全部指向存在的封裝部件。`[Content_Types].xml` 的預設型別與覆寫宣告覆蓋所有部件，沒有缺少宣告或指向不存在部件的 orphan override。

**結構完整性：PASS。全文語意完整性：仍未全部驗收。** 結構驗證只證明部件與關係可對應，不代表 Markdown／DOCX 每段正文逐字或語意等價，也不等於 Word 實際渲染結果已做視覺驗收。

## 2. 內層 ZIP／主文件檢查

| DOCX | 外層大小 | 內層部件數 | 成員大小／CRC | 非空主文件段落 | 表格／列／儲存格 |
|---|---:|---:|---|---:|---|
| `P2_封包式問題解決架構_對話原文紀錄.docx` | 32,555 bytes | 17 | 17/17 PASS | 444 | 9 / 59 / 123 |
| `P2_封包式問題解決架構企劃書_v0.1.docx` | 36,445 bytes | 17 | 17/17 PASS | 591 | 4 / 78 / 256 |

兩份文件的內層 ZIP 均已逐件解壓；每件的實際解壓長度與中央目錄記錄一致，CRC32 全部通過。

## 3. Relationship targets

| DOCX | Relationship 數 | 內部關係 | 外部關係 | 缺失內部目標 | 判定 |
|---|---:|---:|---:|---:|---|
| 對話原文紀錄 | 14 | 14 | 0 | 0 | PASS |
| 企劃書 v0.1 | 14 | 14 | 0 | 0 | PASS |
| **合計** | **28** | **28** | **0** | **0** | **PASS** |

關係檔包含 Package root 與 Word 主文件層級的連結，涵蓋 office document、properties、styles、numbering、settings、theme、footnotes、comments、header、footer 等部件類型。所有內部 Target 皆依來源關係檔位置正規化解析，並在 ZIP 成員清單中找到對應目標；外部 Target 數為 0。

「外部關係 0」只表示 DOCX OOXML relationship 中沒有外部 Target。對話紀錄 Markdown 中的五個歷史 sandbox 連結未在 DOCX 保留可點擊外部超連結，仍按 `FMT-001` 記錄為格式功能損失。

## 4. Content Types

| DOCX | Default 宣告 | Override 宣告 | 缺少 Content Type 的部件 | 指向不存在部件的 Override | 判定 |
|---|---|---:|---:|---:|---|
| 對話原文紀錄 | `rels`、`xml` | 14 | 0 | 0 | PASS |
| 企劃書 v0.1 | `rels`、`xml` | 14 | 0 | 0 | PASS |

檢查程序將每個實際部件映射至 `Override PartName` 或對應副檔名的 `Default Extension`；`[Content_Types].xml` 本身不要求以自身宣告覆蓋。所有實際部件均有可用的 Content Type，且所有 Override 都對應存在部件。

## 5. 尚未完成的內容層驗收

1. Markdown 與 DOCX 的非表格正文尚未逐段完成語意裁定；段落數差異不能直接解讀成缺文，因為 Word 可能把 Markdown 區塊轉為編號屬性、分段或表格。
2. 主文件以外的註腳、註解、頁首頁尾等部件已確認存在且有有效關係，但其文字是否完整對應 Markdown、是否包含轉換新增或遺失的內容，尚未完成逐部件語意對帳。
3. 對話紀錄中「共 13 則訊息」與編號 1–15 的範圍矛盾，以及訊息 1 前只保留片段的來源缺口，仍按 `ERR-001`、`GAP-001` 保留。
4. 企劃書標題與全部 13 張表的 379 個儲存格先前已通過比對；這不自動證明所有非表格文字等價。

## 6. 方法與證據邊界

1. 以內層 ZIP End of Central Directory 與中央目錄逐件定位並解壓。
2. 對每件核對實際輸出大小與 CRC32。
3. 解析 `[Content_Types].xml` 的 Default／Override。
4. 逐份讀取所有 `.rels`，對內部 Target 相對來源部件位置解析，並確認目標存在；External Target 另外計數。
5. 解析 `word/document.xml` 的段落與表格結構，供跨格式差異分析使用。

CRC 與關係目標通過不能證明 Word 渲染視覺一致、原始來源逐字完整、超連結目標仍可用或企劃書已被 P2 採用。

## 7. 專案邊界

僅新增／修改 `upqq21477-star/ForAVAr`。`P1`、`P2` 僅作唯讀參考；兩個來源 ZIP 的原始位元組未修改。
