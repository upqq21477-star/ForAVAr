# 封包 B 解壓歸檔驗收紀錄

## 結論

封包 B 的四個成員已從 ZIP 解壓，逐一核對解壓位元組數與 ZIP 中央目錄的 CRC32，全部通過；四個獨立檔案已寫入 forAVAr，並從 GitHub recursive tree 讀回確認路徑、Git Blob SHA 與檔案大小。原始 ZIP 未修改。

## 原始來源

- 路徑：`參考資料/原始檔案/壓縮檔/P2_封包式問題解決架構_文件套件.zip`
- Blob SHA：`184508e9def34ff546caac580533b6210aae3344`
- ZIP 大小：100,694 bytes
- ZIP 中央目錄成員數：4
- 解壓方式：DEFLATE（method 8）
- 驗證：解壓輸出長度符合中央目錄記錄，且 CRC32 全部一致。

## 已歸檔成員

目錄：`參考資料/原始檔案/解壓內容/封包B/`

| 成員 | 解壓大小 | CRC32 | Git Blob SHA | 歸檔驗收 |
|---|---:|---|---|---|
| `P2_封包式問題解決架構_對話原文紀錄.md` | 40,576 | `3b804cb7` | `2f43f4c7311e81df5d4dfc7da92febd2b60aa2e9` | Git tree 路徑與大小確認 |
| `P2_封包式問題解決架構_對話原文紀錄.docx` | 32,555 | `364d0636` | `6dccf5c5921f5d78087b4b20226c598dda616688` | Git tree 路徑與大小確認 |
| `P2_封包式問題解決架構企劃書_v0.1.md` | 42,550 | `552fbb06` | `a0f94fc229660ddfb4f3dc5ec8ad8a11fd66ff85` | Git tree 路徑與大小確認 |
| `P2_封包式問題解決架構企劃書_v0.1.docx` | 36,445 | `3ff5d6f3` | `ae17de3f93355554c6d9c472bee7c1aa87fa94f4` | Git tree 路徑與大小確認 |

## 邊界與後續工作

1. 上述 CRC32 驗證的是 ZIP 中解壓出的原始位元組與 ZIP 中央目錄記錄一致；Git tree 驗證的是檔案已存在於指定路徑且大小一致。
2. DOCX 是二進位 OOXML 套件；內層 ZIP 17/17 成員大小／CRC、每份 14 個 relationship targets 及 Content Types 覆蓋已通過。
3. 兩份 Markdown 與兩份 DOCX 的跨格式語意比對尚未全部完成。標題與表格比對通過不代表非表格正文、超連結功能、頁首頁尾、註腳、註解或其他 OOXML 部件均已完成語意對帳。
4. 封包 A `P2-relay-R3d130j.zip` 仍無法由目前讀取介面取得 Base64 位元組，不能推定其損壞。需另尋可讀取二進位內容的管道。
5. 僅寫入 forAVAr；P1、P2 維持唯讀。
