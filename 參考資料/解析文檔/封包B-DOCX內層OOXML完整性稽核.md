# 封包 B：DOCX 內層 OOXML 完整性稽核

## 結論

兩份 DOCX 均可作為 ZIP/OOXML 套件解析；內層中央目錄、`word/document.xml` 與 `word/_rels/document.xml.rels` 均存在。逐一解壓全部內層成員後，實際長度與中央目錄記錄相符，CRC32 全部通過。

## 驗證結果

| DOCX | 外層解壓大小 | OOXML 成員數 | 成員 CRC 通過 | 核心部件 |
|---|---:|---:|---|---|
| `P2_封包式問題解決架構_對話原文紀錄.docx` | 32,555 bytes | 17 | 17/17 | `word/document.xml`、`word/_rels/document.xml.rels` 存在 |
| `P2_封包式問題解決架構企劃書_v0.1.docx` | 36,445 bytes | 17 | 17/17 | `word/document.xml`、`word/_rels/document.xml.rels` 存在 |

## 方法

1. 由原始 ZIP 中按中央目錄的 local-header offset 取出 DOCX 壓縮資料。
2. 解壓 DOCX 外層成員，核對大小與外層 CRC32。
3. 將 DOCX 視為內層 ZIP，解析 EOCD 與中央目錄。
4. 依每個內層成員的壓縮方法解壓，再核對輸出大小及 CRC32。
5. 確認主文件 XML 與主文件關係檔存在。

## 限制

- CRC32 通過表示各成員與其 ZIP 中央目錄記錄一致，不等於已完整驗證 Microsoft Word 渲染結果或所有語意。
- 尚需檢查 OOXML 關係目標是否全部存在、內容型別宣告是否一致，以及頁首頁尾、註腳、註解、圖片、超連結等部件的實際語意。
- 尚需與對應 Markdown 做完整逐段對帳。先前標題與表格比對通過，不代表非表格正文及所有格式資訊都已完成核對。
- 僅寫入 forAVAr；P1、P2 維持唯讀。
