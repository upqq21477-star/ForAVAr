# 封包 B｜雙格式完整性與差異稽核主軸

- 文件 ID：FORAVAR-ARCHIVE-B-FORMAT-AUDIT-001
- 類型：MASTER
- 狀態：CURRENT／封包 B 指定範圍格式與正文差異稽核
- 唯一責任：提供 ZIP／DOCX／OOXML 結構、差異檢查範圍、重要裁定和細節分支的唯一入口。
- 上層主軸：[壓縮檔解析總覽與文件導航](./壓縮檔逆向分析與蒸餾紀錄.md)
- 來源清冊：[原始檔案清冊](../原始檔案/清冊.md)
- 備份：[分流前完整報告（BACKUP_ONLY）](./封包B雙格式完整性與差異稽核_備份_分流前_2026-10-21.md)
- 追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

1. [共同結論](#common-conclusion)
2. [責任分支](#branch-index)
3. [原章節相容索引](#legacy-index)
4. [驗收界線](#verification-boundary)

<a id="common-conclusion"></a>
## 1. 共同結論

封包 B 的外層 ZIP、指定 DOCX 的 OOXML 部件、relationships／Content Types、標題／表格及非表格正文有序差異，均依各分支記載的範圍進行檢查。結論必須嚴格限定在實際抽取與比對項目；結構檢查通過不等於原始兩種格式逐字相同，也不代表企劃內容已被 P2 採納或實作。

<a id="branch-index"></a>
## 2. 責任分支

| BRANCH_ID | 唯一責任 | 分支入口 |
|---|---|---|
| ARCHIVE-B-BR-001 | ZIP／OOXML 內部完整性、Markdown／DOCX 對應、比對證據與範圍限制 | [結構完整性與格式對應](./封包B稽核_結構與格式對應.md) |
| ARCHIVE-B-BR-002 | 直接重新抽取、錯漏標記、OOXML relationships／Content Types 補驗 | [補充驗證與 OOXML 結構](./封包B稽核_補充驗證與OOXML.md) |
| ARCHIVE-B-BR-003 | 非表格正文第二輪覆蓋篩查及其限制 | [正文覆蓋篩查](./封包B稽核_正文覆蓋篩查.md) |

<a id="legacy-index"></a>
## 3. 原章節相容索引

<a id="section-1"></a>
## 1. 封包結構與內部完整性

詳細內容：[結構完整性與格式對應](./封包B稽核_結構與格式對應.md#section-1)。

<a id="section-2"></a>
## 2. Markdown／DOCX 對應結果總表

詳細內容：[結構完整性與格式對應](./封包B稽核_結構與格式對應.md#section-2)。

<a id="section-3"></a>
## 3. 正文比對的證據與限制

詳細內容：[結構完整性與格式對應](./封包B稽核_結構與格式對應.md#section-3)。

<a id="section-4"></a>
## 4. 完成範圍、保留限制與禁止推論

詳細內容：[結構完整性與格式對應](./封包B稽核_結構與格式對應.md#section-4)。

<a id="section-5"></a>
## 5. 已完成工作與後續工作

詳細內容：[結構完整性與格式對應](./封包B稽核_結構與格式對應.md#section-5)。

<a id="section-6"></a>
## 6. 2026-10-20 直接重新抽取與補充驗證

詳細內容：[補充驗證與 OOXML 結構](./封包B稽核_補充驗證與OOXML.md#section-1)。

<a id="section-7"></a>
## 7. 重複比對標記對照（2026-10-20）

詳細內容：[補充驗證與 OOXML 結構](./封包B稽核_補充驗證與OOXML.md#section-2)。

<a id="section-8"></a>
## 8. OOXML 關係與 Content Types 補驗（2026-10-20）

詳細內容：[補充驗證與 OOXML 結構](./封包B稽核_補充驗證與OOXML.md#section-3)。

<a id="section-9"></a>
## 9. 非表格正文第二輪覆蓋篩查（2026-10-20）

詳細內容：[非表格正文覆蓋篩查](./封包B稽核_正文覆蓋篩查.md#section-1)。

<a id="verification-boundary"></a>
## 4. 驗收界線

- 保留原始 ZIP／DOCX，不因摘要或對照表改寫來源。
- 所有數值和具體差異以三個細節分支為準，不在總覽重複保存。
- 「未發現未解釋的實質內容缺失」限於報告列明的抽取／正規化／有序序列檢查，不能擴大解讀為所有隱藏中繼資料或呈現功能完全相同。
- 本稽核是靜態內容／結構驗收，不代表企劃已採納或 Runtime 通過。
