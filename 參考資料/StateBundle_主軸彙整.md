# State Bundle｜主軸彙整

- 文件 ID：FORAVAR-TOPIC-STATE-BUNDLE-001
- 類型：MASTER
- 版本：v1.0
- 狀態：CURRENT／契約候選；未證明自動生成、載入或跨會話防漂移
- 唯一責任：統一 State Bundle 契約、個案快照、結構驗收收據及離線接手摘要的導航與共同狀態。
- 上層索引：[文件與分支索引](./文件與分支索引.md)
- 追溯：[變更追溯總表](./變更追溯總表.md)

## 目錄與索引

1. [共同狀態](#1-共同狀態)
2. [分支登錄](#2-分支登錄)
3. [不得混淆的證據邊界](#3-不得混淆的證據邊界)

## 1. 共同狀態

State Bundle 是將特定時間、特定來源版本的必要狀態打包，用於減少跨會話重建偏差的候選契約。Core Anchor、Current State、Task Contract 的責任不同。快照若與 GitHub 現況不能核對，必須標記 CONFLICT／STALE_CONTEXT／BLOCKED_CONTEXT，不得當作現行權威狀態。

## 2. 分支登錄

| BRANCH_ID | 唯一責任 | 路徑 |
|---|---|---|
| STATE-BR-001 | 最小資料契約、欄位意義及防漂移反例 | [State Bundle 契約草案 v0.1](./解析文檔/可攜式StateBundle最小資料契約與防漂移反例驗收草案_v0.1.md) |
| STATE-BR-002 | 特定 P2-relay 封包的 JSON 快照 | [State Bundle 實例 JSON](./解析文檔/StateBundle_實例_P2-relay-R3d130j_2026-10-21.json) |
| STATE-BR-003 | 特定快照的結構檢查結果 | [初次結構核對紀錄](./解析文檔/StateBundle_實例初次結構核對紀錄_2026-10-21.md) |
| STATE-BR-004 | 無法即時連接 GitHub 時的衍生接手摘要 | [Claude 離線接手摘要](./解析文檔/P2-relay-R3d130j_Claude離線接手摘要_2026-10-21.md) |

## 3. 不得混淆的證據邊界

- 契約草案不是已實作 Schema 或載入器。
- JSON 是特定來源版本的快照，不是 P2 的 Current。
- 結構檢查 19/19 通過只代表已測欄位與結構，不代表行為驗收已執行。
- 離線接手摘要是衍生視圖，不可反向覆寫 GitHub 權威來源。
- 四分支必須保留各自職責，日常引用優先指向本 MASTER；舊分支版本僅由追溯總表調閱。


## 契約草案詳細分支

原 v0.1 契約路徑目前只作舊入口相容指標；日常引用只從本主軸進入以下分支。三者均保留原始章節正文，契約仍處於 NOT_APPROVED／NOT_IMPLEMENTED。

- [契約分支 A](./解析文檔/StateBundle契約_分支A.md)
- [契約分支 B](./解析文檔/StateBundle契約_分支B.md)
- [契約分支 C](./解析文檔/StateBundle契約_分支C.md)
