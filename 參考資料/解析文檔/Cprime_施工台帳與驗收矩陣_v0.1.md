# C′ 施工台帳與驗收矩陣 v0.1｜主軸彙整

- 文件 ID：FORAVAR-CPRIME-IMPLEMENTATION-LEDGER-001
- 類型：MASTER／施工追蹤
- 狀態：INITIALIZED／台帳已建立；尚無 Runtime 施工或驗收證據
- 唯一責任：提供施工階段、交付狀態、需求、風險、決策與驗收結果的唯一摘要及分支入口；完整台帳正文由兩個分支維護。
- 上層主軸：[C′ 主軸索引](../Cprime_主軸索引.md)
- 分流前備份：[C′ 施工台帳 v0.1（BACKUP_ONLY）](./Cprime_施工台帳_備份_v0.1_分流前.md)
- 追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

1. [目前狀態摘要](#current-status)
2. [責任分支](#branches)
3. [原章節相容索引](#legacy-index)
4. [狀態語義邊界](#state-boundary)

<a id="current-status"></a>
## 1. 目前狀態摘要

此台帳是 C′ 的施工／驗收追蹤工具，不是主企劃正文。需求被記錄、交付物被建立、靜態檢查完成和 Runtime 通過是不同狀態。所有未執行測試維持 NOT_RUN；未開始階段維持 NOT_STARTED；阻塞項保留 BLOCKED，不能由文字完整度推論為通過。

<a id="branches"></a>
## 2. 責任分支

| BRANCH_ID | 唯一責任 | 詳細文件 |
|---|---|---|
| CPRIME-LEDGER-BR-001 | 0. 本次接手先看這裡；1. 階段施工台帳；2. 需求與交付物登錄 | [施工台帳分支 A](./Cprime施工台帳_分支A.md) |
| CPRIME-LEDGER-BR-002 | 3. 驗收矩陣；4. Gate 退出證據規範；5. 決策台帳；6. 阻塞與待釐清事項；7. 風險登錄維護規則；8. 變更與文件一致性清單；9. 本次文件施工紀錄；10. 固定交接格式；11. 版本紀錄 | [施工台帳分支 B](./Cprime施工台帳_分支B.md) |

<a id="legacy-index"></a>
## 3. 原章節相容索引

<a id="section-1"></a>
## 0. 本次接手先看這裡

詳細內容：[施工台帳分支 A](./Cprime施工台帳_分支A.md#section-1)。

<a id="section-2"></a>
## 1. 階段施工台帳

詳細內容：[施工台帳分支 A](./Cprime施工台帳_分支A.md#section-2)。

<a id="section-3"></a>
## 2. 需求與交付物登錄

詳細內容：[施工台帳分支 A](./Cprime施工台帳_分支A.md#section-3)。

<a id="section-4"></a>
## 3. 驗收矩陣

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-1)。

<a id="section-5"></a>
## 4. Gate 退出證據規範

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-2)。

<a id="section-6"></a>
## 5. 決策台帳

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-3)。

<a id="section-7"></a>
## 6. 阻塞與待釐清事項

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-4)。

<a id="section-8"></a>
## 7. 風險登錄維護規則

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-5)。

<a id="section-9"></a>
## 8. 變更與文件一致性清單

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-6)。

<a id="section-10"></a>
## 9. 本次文件施工紀錄

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-7)。

<a id="section-11"></a>
## 10. 固定交接格式

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-8)。

<a id="section-12"></a>
## 11. 版本紀錄

詳細內容：[施工台帳分支 B](./Cprime施工台帳_分支B.md#section-9)。

<a id="state-boundary"></a>
## 4. 狀態語義邊界

- 本 MASTER 只摘要現況和指向詳細台帳；不改 C′ 主企劃的需求、架構或驗收門檻。
- 文件提交成功不代表相應功能已實作；NOT_RUN 不等於 PASS；BLOCKED 不等於失敗證據已完全取得。
- 對外引用應先使用本主軸，再按需要載入分支或正式企劃。原完整 v0.1 只供恢復與差異核對。
