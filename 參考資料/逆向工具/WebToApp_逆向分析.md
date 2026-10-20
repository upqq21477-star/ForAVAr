# WebToApp 專案逆向分析｜主軸彙整

- 文件 ID：FORAVAR-TOPIC-WEBTOAPP-001
- 類型：MASTER
- 版本：v1.0
- 狀態：CURRENT／指定外部 commit 的靜態逆向分析；未宣稱實機驗收
- 唯一責任：統整系統架構、資料契約、建置／執行分離、平台限制、安全與測試的主要結論，提供詳細分支唯一入口。
- 外部研究基準 commit：`25937cb8c14f467603276dd1dfaedb9bd7d55560`
- 上層索引：[文件與分支索引](../文件與分支索引.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)
- 備份：[分流前完整報告（BACKUP_ONLY）](./WebToApp_備份_分流前_2026-10-21.md)

## 目錄與索引

1. [核心結論](#core-conclusions)
2. [責任分支](#branch-list)
3. [原章節相容索引](#legacy-section-index)
4. [證據界線](#evidence-boundary)

<a id="core-conclusions"></a>
## 1. 核心結論

WebToApp 不只是 WebView 包裝器。主要鏈路是統一 `WebApp` 設定經映射成 APK 設定，序列化至 `app_config.json`，再由生成後的 Runtime 讀取。編輯器／建置端與 Runtime 端分離，降低責任耦合，但跨層欄位契約不一致會造成設定被忽略或回退預設值，且建置成功不代表功能正確。

APK 修改涉及 Manifest、資源表、資源注入、原生程式庫與簽章；增量建置和內容指紋可以降低重複工作，但需確認指紋覆蓋全部產物依賴。WebView／原生橋接、TLS 中介、安全擴充功能限制、Google Play 規範與 16 KB 記憶體頁面要求都需獨立檢查。靜態結構檢查、設定契約測試與實機／Runtime 測試不能互相代替。

<a id="branch-list"></a>
## 2. 責任分支

| BRANCH_ID | 唯一責任 | 分支入口 |
|---|---|---|
| WEBTOAPP-BR-001 | 系統全貌、資料模型、設定轉換、APK 建置、增量建置 | [系統全貌與核心程式](./WebToApp_系統全貌與核心程式.md) |
| WEBTOAPP-BR-002 | 架構品質、Android 平台限制、WebView／TLS／擴充功能安全 | [架構品質、平台限制與安全](./WebToApp_架構平台與安全.md) |
| WEBTOAPP-BR-003 | 測試證據、現代化路線與結論 | [測試證據與現代化路線](./WebToApp_測試與現代化路線.md) |

<a id="legacy-section-index"></a>
## 3. 原章節相容索引

保留原報告章節標題及錨點；詳細文字與來源仍在三個分支。完整拆分前正文只能從 BACKUP_ONLY 備份恢復，不作一般引用來源。

<a id="section-1"></a>
## 重要摘要

詳細內容：[系統全貌與核心程式](./WebToApp_系統全貌與核心程式.md#section-1)。

<a id="section-2"></a>
## 一、先還原整個系統

詳細內容：[系統全貌與核心程式](./WebToApp_系統全貌與核心程式.md#section-2)。

<a id="section-3"></a>
## 二、核心程式的逆向追蹤

詳細內容：[系統全貌與核心程式](./WebToApp_系統全貌與核心程式.md#section-3)。

<a id="section-4"></a>
## 三、架構品質：成熟之處與真正的風險

詳細內容：[架構品質、平台限制與安全](./WebToApp_架構平台與安全.md#section-1)。

<a id="section-5"></a>
## 四、外部研究：Android 平台對它施加的硬限制

詳細內容：[架構品質、平台限制與安全](./WebToApp_架構平台與安全.md#section-2)。

<a id="section-6"></a>
## 五、安全逆向：WebView、TLS 與擴充功能

詳細內容：[架構品質、平台限制與安全](./WebToApp_架構平台與安全.md#section-3)。

<a id="section-7"></a>
## 六、測試與品質保證：目前能證明什麼

詳細內容：[測試證據與現代化路線](./WebToApp_測試與現代化路線.md#section-1)。

<a id="section-8"></a>
## 七、建議的後續現代化路線

詳細內容：[測試證據與現代化路線](./WebToApp_測試與現代化路線.md#section-2)。

<a id="section-9"></a>
## 八、最終判斷

詳細內容：[測試證據與現代化路線](./WebToApp_測試與現代化路線.md#section-3)。

<a id="evidence-boundary"></a>
## 4. 證據界線

- 本分析依指定外部 commit 與公開文件進行靜態分析；未在本次治理變更中重新執行 APK 建置或真機測試。
- 源碼中的能力與風險不能直接推論為 forAVAr／P2 已具備相同實作。
- 已知限制、程式位置、設定欄位及外部來源保留在分支中；本主軸只保存導航和共同結論。
