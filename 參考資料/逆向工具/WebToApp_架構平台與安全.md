# WebToApp 研究分支｜架構品質、平台限制與安全

- 文件 ID：FORAVAR-WEBTOAPP-BR-002
- 類型：BRANCH
- 狀態：CURRENT／指定外部版本的靜態分析；未宣稱實機驗收
- 唯一責任：保存 WebToApp 原報告中指定角度的完整分析、證據及限制。
- 主軸回鏈：[WebToApp 逆向分析主軸](./WebToApp_逆向分析.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [三、架構品質：成熟之處與真正的風險](#section-1)
- [四、外部研究：Android 平台對它施加的硬限制](#section-2)
- [五、安全逆向：WebView、TLS 與擴充功能](#section-3)

---

<a id="section-1"></a>
## 三、架構品質：成熟之處與真正的風險

### 3.1 已經做得較完整的地方

第一，**開發端與生成端分離**。`:app` 負責建立與編輯，`:shell` 負責提供生成應用需要的執行環境，而共享 Runtime 原始碼由 `app` 同步至 `shell`。這比長期維護兩套相似但逐漸分歧的實作更容易控制。

第二，**針對跨層錯誤建立自動防線**。專案有設定欄位漂移檢查、匯出接線測試、產物驗證及多個 APK 重建相關測試，並在 CI 執行編譯與單元測試。

第三，**產物層面的工程考量相當深入**。權限和元件的動態注入、原生函式庫處理、簽章身分、加密、資源表重建與快取指紋，都不是普通網站封裝工具所必需的內容。

第四，**已考慮不同分發渠道的差異**。專案有 Standard 和 Google Play 版本，也有 F-Droid 建置路徑，並試圖在產生 APK 前排除不適用的功能組合。

### 3.2 主要的維護風險：功能越多，跨層一致性越難保證

從原始碼規模可以直接確認，`ApkBuilder.kt` 約有 258,519 個字元，`WebViewManager.kt` 約有 332,411 個字元。

**這是推論：** 如此龐大的單檔實作，會增加程式碼審查、局部修改、錯誤定位及回歸測試的難度，尤其是 APK 建置涉及多種應用類型與原生程式庫。這不代表目前已有特定缺陷，但意味著重構時應優先降低各功能之間的隱性耦合。

建議未來將建置職責清楚拆分為：

- 建置協調與生命週期管理。
- Manifest、資源表及 ZIP 結構處理。
- 各類 Runtime 的資源注入。
- 快取計畫與指紋計算。
- 產物驗證、簽章及輸出交付。

重點不是為了縮短檔案而拆檔，而是讓每個子系統具有明確的輸入、輸出、錯誤責任及可獨立測試的契約。

### 3.3 應用複製功能有值得核實的限制

`AGENTS.md` 記載，`clone-host` 模組的 `syncCloneHostDex` 產生工作目前被刻意停用，理由包含降低防毒軟體誤報；同一份文件也指出，`AppCloner` 在缺少該資產時會採取 fail-soft 路徑。

因此，不能單憑存在 `clone-host` 資料夾與 `AppCloner.kt`，便認定所有應用複製能力都已完整交付。

後續驗證應追蹤：實際呼叫路徑、是否依賴該 DEX 資產、缺少資產時有哪些功能被停用，以及對使用者呈現的結果是否清楚。這屬於**需要進一步追蹤的功能完整性項目**，不是已證實的整體功能失效。

<a id="section-2"></a>
## 四、外部研究：Android 平台對它施加的硬限制

這部分是理解 WebToApp 實際產品價值與邊界的關鍵。

### 4.1 Google Play 發布與本機伺服器 Runtime 存在衝突

同一套工具有兩種不同的發布能力：

- **一般 WebView／HTML 類應用**：可依照應用需求處理 target SDK、權限與套件產物，再走適用的 Play 發布流程。
- **依賴本機原生程式執行的應用**：Node.js、PHP、Python、Go、WordPress 等類型受限於可執行檔政策，不能直接套用相同的 Google Play AAB 流程。

依據 [Android Developers 的 Android 10 變更文件](https://developer.android.com/about/versions/10/behavior-changes-10)，針對 Android 10（API 29）以上 target SDK 的應用，平台會限制從應用可寫入的 Home 目錄執行檔案。WebToApp 將受此限制影響的伺服器 Runtime 類型設為 `targetSdk 28`，並使用 [GeneratedSdkLevels.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/apkbuilder/GeneratedSdkLevels.kt) 集中處理 SDK 規則。

而專案的 [AabExportCoordinator.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/playstore/aab/AabExportCoordinator.kt) 會拒絕這些 `requiresProcessExec` 類型的 AAB 匯出，避免將 SDK 提升到要求值後，生成不能正常執行本機 Runtime 的產物。

截至 **2026 年 10 月 19 日**，Google Play 要求新應用程式及更新至少以 Android 16（API 36）為目標的政策期限，已於 2026 年 8 月 31 日到期。

這產生一個很重要的產品邊界：

**WebToApp 可以支援本機 Node.js、PHP、Python 或 Go Runtime，不代表這些應用類型也能直接走 Google Play 發布管線。** 工具的執行能力與平台分發資格是兩件不同的事。

參考：
- https://developer.android.com/about/versions/10/behavior-changes-10
- https://developer.android.com/google/play/requirements/target-sdk

### 4.2 16 KB 記憶體頁面對原生程式庫的要求

WebToApp 包含 Node.js、Go 等原生程式庫，也包含用於 APK 產物處理的 16 KB ELF 對齊邏輯。

Android 官方文件指出，使用原生程式庫的應用必須考慮 16 KB 記憶體頁面的相容性；Google Play 對 64 位元裝置及相應 target SDK 的要求也已將此列為重要條件。

因此，`ElfAligner16k.kt` 不只是建置最佳化，而是相容性工作的一部分。真正的驗收應包含生成的 APK、各 ABI 的 `.so`、實際安裝與執行結果，而非只檢查 Kotlin 編譯成功。

參考：
- https://developer.android.com/guide/practices/page-sizes

<a id="section-3"></a>
## 五、安全逆向：WebView、TLS 與擴充功能

以下是靜態程式碼審查的重點。沒有完成完整的動態滲透測試，因此不會直接將待驗證項目定性為已確認漏洞。

### 5.1 JavaScript 與原生橋接

[WebViewManager.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/webview/WebViewManager.kt) 會依應用設定控制 JavaScript、檔案存取、內容存取及混合內容等 WebView 行為；分享及接收分享資料的原生 JavaScript bridge 則有獨立啟用條件。

這種設計具有彈性，但 Android 官方文件特別警告，`addJavascriptInterface()` 會把原生介面暴露給網頁中的 JavaScript，對不受信任的網頁內容尤其需要謹慎。

應進一步驗證：

1. 啟用 bridge 後，能否被其他網域、重新導向後的網頁或彈出視窗存取。
2. 權限是否按應用及來源限制，而不是只根據某個全域開關。
3. 本機 HTML、`file://` 與遠端網頁之間是否存在不必要的跨來源存取。

Android 也明確警告，未妥善配置的 WebView 本機檔案存取會形成資料暴露風險；應審查 `allowFileAccess` 等選項及其配套限制。

參考：
- https://developer.android.com/develop/ui/views/layout/webapps/webview
- https://developer.android.com/privacy-and-security/risks/webview-unsafe-file-inclusion

### 5.2 TLS 中介代理：不要誤判 `AcceptAllTrustManager`

這個專案具有 TLS 指紋調整及本機 TLS 中介橋接功能，值得將其拆成兩條連線分別審查。

- **瀏覽器到本機橋接端：** `TlsMitmBridge.kt` 建立本機 TLS 伺服器端連線，為其提供本機產生的憑證。
- **本機橋接端到上游網站：** `TlsUpstreamConnector.kt` 使用系統信任來源與使用者匯入的 CA，並額外檢查上游憑證與目標主機名稱是否匹配。

`TlsMitmBridge.kt` 中存在 `AcceptAllTrustManager`，但它出現在本機 TLS 伺服器端的握手實作中；**不能僅因為找到這個類別，就斷言它會接受所有上游網站的錯誤憑證**。上游連線的程式碼明確採取另一套信任驗證路徑。

還有一項值得獨立驗證的差異：橋接端以主機白名單限制未經授權的連線，避免本機迴圈代理變成開放代理；程式碼也指出，在 GeckoView 引擎下，由於缺少相應的每請求回呼，白名單強制機制有不同的設定。

這不是已確認的漏洞，但屬於必須以威脅模型和實際請求測試確認的安全差異。

### 5.3 Chrome MV3 擴充功能的隔離限制

專案的 [Chrome MV3 文件](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/docs/extensions/chrome-mv3.md) 說明，Android WebView 只有單一 JavaScript 執行環境。擴充功能的 `world: "ISOLATED"` 與 `world: "MAIN"` 由注入機制模擬，並不等於 Chromium 桌面環境中的真正隔離世界。

這會影響擴充功能的安全邊界及相容性。若某個擴充功能把隔離世界當成防止網頁讀取敏感資料的安全保證，就不能直接假設它在 WebToApp 中仍具有相同保障。

這是產品架構本身的限制，而不是單純增加 API 函式就能消除的問題。
