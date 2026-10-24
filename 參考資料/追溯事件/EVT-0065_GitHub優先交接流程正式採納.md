# EVT-0065｜GitHub 優先交接流程納入正式系統

- EVENT_ID：EVT-0065
- 日期：2026-10-24
- 操作類型：ADOPT_GITHUB_FIRST_HANDOFF
- 狀態：COMMITTED／READBACK_PENDING
- 授權：使用者明確要求「更新企劃」，並指定將 GitHub 優先交接流程整合進正式 forAVAr。
- 唯一責任：記錄責任歸位、正式變更範圍、基線指紋、驗收與殘餘風險。
- 正式核心基線：[forAVAr 核心重建施工藍圖 v0.7](../解析文檔/forAVAr_核心重建施工藍圖_v0.7_2026-10-24.md)
- 正式操作規範：[SOP-HANDOFF-001 v1.0](../SOP_GitHub優先交接流程.md)
- 來源候選：[forAVArb SOP v0.1](https://github.com/upqq21477-star/forAVArb/blob/main/交接/SOP_GitHub優先交接流程_v0.1.md)
- 歸檔索引：[forAVArb 交接 README](https://github.com/upqq21477-star/forAVArb/blob/main/交接/README.md)

## 1. 正式裁決與責任歸位

本次不新增思考架構。比對 v0.7 藍圖、SOP-META-001、CF-004、StateBundle／工作封包、文件生命週期及版本治理後，責任歸位如下：

- SOP-META-001：SOP 選用、授權、執行、驗收、改良與退役。
- CF-004：對話成果持久化、索引更新、引用核對及交接觸發入口。
- SOP-HANDOFF-001：新增專用交接步驟與驗收規範，不另建 CF 編號。
- StateBundle／既有工作封包及文件生命週期：繼續承接跨階段狀態、恢復與證據連結，不另建封包契約。
- 文件索引、變更追溯表與 SOP 台帳：分別負責導航、檔案變更追溯及逐次執行結果。

正式核心藍圖 v0.7 未修改；Core → A1–A6 → N01–N18 → F0–F7 及 M/G/P/T 四維維持不變。P1、P2 未寫入。

## 2. 更新前基線指紋

讀取時正式主庫 main HEAD：c29f795bb4bb0232159ce48ed2347efb799c1e92；tree SHA：8e2628118c0a21a73ef04b82e8efb10de1afc559。

| 文件／來源 | 更新前 Blob SHA |
|---|---|
| 核心藍圖 v0.7（不修改） | cab6178593154e5402ec5ef0e6480c941f4223b2 |
| SOP-META-001 | 1845dbc80105f144c12a32ae41063298d92d1f09 |
| 對話流程列表／CF-004 | 36a1213831fe88a05f0683c66f39020f83102f22 |
| 文件與分支索引 | 6fd08fdbc2b2a88385789c4171168869685ba7a7 |
| 變更追溯總表 | c83683ac091f2e4d1f5f3572aca7c35e2c1262de |
| SOP 執行與演化台帳 | 78dc00bc7c5c3aeaf54a6dbd8dcc063301e040e0 |
| forAVArb 原候選 SOP v0.1 | f799735b7919e698db2ecee60ba7b2750cac070d |
| forAVArb 交接 README | ca03da39ef0353b6bcf6a2134780f8415948ef74 |

forAVArb 讀取時 main HEAD：f3802b12e708123e37b4cdd2ec0e9262c117f3e6。

## 3. 變更前後與修改理由

| 類別 | 檔案／操作 | 理由與範圍 |
|---|---|---|
| 新增 | [SOP-HANDOFF-001](../SOP_GitHub優先交接流程.md) | 將觸發、最小充分狀態、SHA 核對、GitHub 寫入、索引更新、讀回驗收、接手題詞與聊天節流集中在唯一專用規範。 |
| 修改 | [SOP-META-001](../SOP固定流程與演化管理.md) | 加入交接 SOP 入口、啟動條件與成熟度聲明；維持 8,000 字元內。 |
| 修改 | [對話流程列表／CF-004](../對話流程列表.md) | 既有 CF-004 已涵蓋交接，只補權威 SOP 連結，不新增重複流程 ID。 |
| 修改 | [文件與分支索引](../文件與分支索引.md) | 增加 GOV-012、REF-049；精簡重複內容並維持 8,000 字元內。 |
| 修改 | [變更追溯總表](../變更追溯總表.md) | 新增 EVT-0065 分類、事件入口及引用；精簡重複搜尋描述並維持 8,000 字元內。 |
| 修改 | [SOP 執行與演化台帳](../SOP執行與演化台帳.md) | 新增 RUN-20261024-001，記錄本次整合與未驗項。 |
| 來源狀態調整 | [forAVArb 候選 v0.1](https://github.com/upqq21477-star/forAVArb/blob/main/交接/SOP_GitHub優先交接流程_v0.1.md)、[交接 README](https://github.com/upqq21477-star/forAVArb/blob/main/交接/README.md) | 保留候選原文供追溯，改標為來源紀錄，現行操作以主庫正式 SOP 為準。 |

### 變更後 Blob SHA

| 文件 | Blob SHA |
|---|---|
| SOP-HANDOFF-001 | 0c960e96100186443a364ec76143d0648fd3bf18 |
| SOP-META-001 | b70a35340d3a8e727877094afce1185ea3009874 |
| 對話流程列表／CF-004 | 27063de6315618589d2b86315234bfb15fecab2b |
| 文件與分支索引 | 19e4192f4877241850861224c8f67f7ca004c84a |
| 變更追溯總表 | 7cb8743ffdcb92d4b5f32cd2ea49abd52b57f0c3 |
| SOP 執行與演化台帳 | 285a81b6051671a9045082c5a34cdc8ecec7eadc |
| forAVArb 候選來源紀錄 | c81ecb7fa4d18cf24ac8c1e7d4d16976d60d416a |
| forAVArb 交接 README | 73316195ed48a9ae400bf2690625f98d3fcabf27 |

主要提交：正式 SOP 462e431c87463bb5678b34b5e29a61e5bf45eeb8；SOP 治理 812db364d748794c081a0950767993c39f1bcc41；CF-004 6ea2fc1d69943e9f818a22b0d9cc9a917358a7d9；文件索引 2a7be3994ddbe67982407cf8e4fd0a7da4918ab1；追溯索引 c64e85daddf0df80cf5abb902516e28d199ad1b0；執行台帳 9e0f52e670cda7d9524f37b43a5416ac8d50245a；forAVArb 候選 857973c21da7c37f13b3179fa87d0aa51c77da36；forAVArb README d86637140172e0f5ac01209dc26beeb3f6f667e2。

## 4. 驗收結果與成熟度界線

- 本事件初始狀態記為 READBACK_PENDING；最終狀態須以正式 SOP、所有修改檔案、兩份 forAVArb 歸檔檔案及索引讀回為準。
- 提交成功、文件讀回、連結檢查、跨任務流程成效及 Runtime 自動強制是不同狀態。
- 本次未執行 Runtime 測試，未驗證工具自動觸發，也未以代表性多任務案例證明跨任務效果；不得宣稱這些項目通過。
- SOP-HANDOFF-001 先以 PROVISIONAL_CURRENT 手動執行；跨任務有效性須依 SOP-META-001 以代表性案例與回歸紀錄評估。
- 讀回、連結或索引若不一致，狀態維持 PARTIAL／BLOCKED，只修復受影響項。

## 5. 權限與不可變更邊界

本次只改 forAVAr 核准的正式治理文件及 forAVArb 候選／索引狀態。未修改 v0.7 核心藍圖、Runtime 程式碼、P1 或 P2；未更改 repository 權限，也未把候選稿當成已實作能力。
