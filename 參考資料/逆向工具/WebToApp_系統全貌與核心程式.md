# WebToApp 研究分支｜系統全貌與核心程式

- 文件 ID：FORAVAR-WEBTOAPP-BR-001
- 類型：BRANCH
- 狀態：CURRENT／指定外部版本的靜態分析；未宣稱實機驗收
- 唯一責任：保存 WebToApp 原報告中指定角度的完整分析、證據及限制。
- 主軸回鏈：[WebToApp 逆向分析主軸](./WebToApp_逆向分析.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [重要摘要](#section-1)
- [一、先還原整個系統](#section-2)
- [二、核心程式的逆向追蹤](#section-3)

---

## 原始前置內容

# WebToApp 專案逆向分析

> 主軸回鏈：[WebToApp｜主軸彙整](../WebToApp_主軸彙整.md) ｜ 分支 ID：WEBTOAPP-BR-001 ｜ 本回鏈只提供導航，不改變本文件的證據邊界。

研究對象：https://github.com/shiaho777/web-to-app
研究基準：GitHub `main` 分支；分析時讀取的原始碼提交樹 SHA：`25937cb8c14f467603276dd1dfaedb9bd7d55560`。



<a id="section-1"></a>
## 重要摘要

**WebToApp 的核心價值不是把網站包進 WebView，而是將 Android 手機本身變成一套應用程式建置、執行環境整合、APK 修改與簽章工作站。** 這是根據其原始碼、建置設定及架構文件得出的判斷，不代表所有功能均已經過實機驗證。

<a id="section-2"></a>
## 一、先還原整個系統

概念架構分為四層：

1. **應用程式定義與編輯器**：Kotlin、Jetpack Compose、Room；管理應用類型、設定、資源及匯出選項。
2. **建置與匯出引擎**：ApkBuilder、ApkConfigJsonFactory、APK 結構修改、簽章；把應用設定轉換成可安裝的套件。
3. **Shell 執行環境**：獨立 runtime host、WebView、本地伺服器；讀取匯出設定，實際執行生成的應用。
4. **平台與執行能力**：Android API、原生程式庫、網路層、Node.js／PHP／Python／Go 等執行環境。

這是概念架構圖，並非原始碼中的實際類別圖。

這個架構最值得研究的地方，是它將「開發工具」與「生成後的應用」分開：`:app` 負責完整建置功能，`:shell` 提供生成應用所需的執行環境，`:clone-host` 則負責應用複製相關的 Host 程式碼。原始碼中的 runtime 會從 `app` 同步至 `shell`，而不是維護兩套完全獨立的執行邏輯。

參考：
- https://github.com/shiaho777/web-to-app
- https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/settings.gradle.kts
- https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/build.gradle.kts
- https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/shell/build.gradle.kts

<a id="section-3"></a>
## 二、核心程式的逆向追蹤

這個專案最重要的分析方法，是順著一個應用程式從建立到生成 APK 的生命週期，逐層檢查資料如何流動，而不是單純按照資料夾分類。

### 2.1 資料模型：所有功能從哪裡開始

核心資料模型是 [WebApp.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/data/model/WebApp.kt)。

它不是單純儲存網址，而是儲存一份完整的應用程式定義，涵蓋：

| 資料領域 | 主要內容 |
|---|---|
| 應用身分 | 名稱、網址、套件名稱、應用類型 |
| 網頁行為 | JavaScript、快取、User-Agent、瀏覽器設定 |
| 原生與伺服器執行環境 | Node.js、PHP、Python、Go、WordPress |
| 資源 | HTML、圖片、影片、音訊及圖庫 |
| 網路 | Proxy、DNS、TLS、網路存取設定 |
| 功能擴充 | 外掛、廣告攔截、啟動畫面、通知、分享等 |
| 匯出 | APK 設定、版本號、SDK、簽章及加密選項 |

資料模型使用 Room 的 `@Entity`，並透過索引支援常見資料查詢。這份模型同時是編輯器的資料基礎，也是打包引擎的輸入。

**架構判斷：** 將整個應用收斂成統一的資料模型，能使不同的編輯畫面及匯出入口共用同一套設定；相對的，任何新增功能都必須確保資料模型、儲存、匯出及執行端同步更新。

### 2.2 設定轉換：最容易出現隱性錯誤的環節

這條路徑是專案最值得深入研究的部分。

資料鏈：

1. `WebApp`：使用者在編輯器設定的原始資料。
2. `WebApp.toApkConfig()`：將應用資料映射成匯出設定。
3. `ApkConfigJsonFactory`：產生 `app_config.json`，並執行設定驗證。
4. `ShellModeManager`：生成的 APK 讀取設定並反序列化。
5. `Runtime`：WebView、伺服器或其他功能真正執行。

原始碼依據：
- [ApkBuilder.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/apkbuilder/ApkBuilder.kt)
- [ApkConfigJsonFactory.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/apkbuilder/ApkConfigJsonFactory.kt)
- [ShellModeManager.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/shell/ShellModeManager.kt)

這條資料鏈存在一個已被專案文件明確記載的問題類型：JSON 欄位名稱不一致。

例如，匯出端輸出的欄位名稱和執行端 `@SerializedName` 指定的名稱若不匹配，Gson 可能直接忽略未知欄位或保留預設值，而不一定讓 APK 建置失敗。最終結果就可能是：編輯器顯示功能已啟用，生成的 APK 卻沒有按照設定執行。

專案已針對此問題建立 [config-drift.md](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/docs/developer/config-drift.md) 所描述的自動檢查，並透過 `scripts/check_config_field_drift.py` 及 `:app:checkConfigFieldDrift` 驗證欄位對應。

這是合理的防線，但仍有一個區別：

- 欄位名稱檢查，可以發現部分資料契約不一致。
- JSON 往返測試，可以驗證序列化與反序列化結果。
- 實際執行測試，才可以確認功能是否依據該設定產生預期行為。

三者不能互相取代。

### 2.3 APK 建置：它不是一般的網站包裝器

核心位於 [core/apkbuilder](https://github.com/shiaho777/web-to-app/tree/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/apkbuilder)。

按照原始碼及開發文件，建置流程如下：

```text
WebApp 應用定義
  -> 建立 ApkConfig
  -> 檢查 SDK、權限與輸入
  -> 選擇 Shell APK 模板
  -> 判斷增量建置模式
  -> 改寫 AndroidManifest / resources.arsc
  -> 注入 app_config.json 與應用資源
  -> 注入所需原生程式庫與執行環境
  -> 驗證 APK 內容
  -> 簽署 APK
  -> 驗證簽章與輸出
  -> 交付生成的 APK
```

主要元件：

| 元件 | 實際職責 |
|---|---|
| `ApkBuilder.kt` | 統籌完整建置流程 |
| `AxmlEditor`、`AxmlRebuilder` | 編輯與重建二進位 AndroidManifest |
| `ArscEditor`、`ArscRebuilder` | 處理 Android 資源表 |
| `RuntimeAssetEmbedder.kt` | 注入伺服器型應用的執行資源 |
| `ElfAligner16k.kt` | 處理原生 ELF 程式庫的 16 KB 對齊 |
| `ApkArtifactVerifier.kt` | 檢查生成套件中必要的資源與檔案 |
| `JarSigner.kt` | 執行 APK 簽章 |

以上職責可在 [export-pipeline.md](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/docs/developer/export-pipeline.md) 和對應原始碼中確認。

這套系統會修改既有套件結構、注入應用專屬內容，再重新簽署。它的工程難度與單純使用 Android WebView 載入網址有根本差異。

### 2.4 增量建置：如何減少重複工作

[ApkBuildCache.kt](https://github.com/shiaho777/web-to-app/blob/25937cb8c14f467603276dd1dfaedb9bd7d55560/app/src/main/java/com/webtoapp/core/apkbuilder/ApkBuildCache.kt) 有三種主要建置模式：

| 模式 | 作用 |
|---|---|
| `FULL` | 從模板重新建置 |
| `CONTENT_OVERLAY` | 在先前的未簽章 APK 上更新應用內容 |
| `REUSE_UNSIGNED` | 直接重用內容和身分指紋均符合的未簽章 APK，再進行簽章 |

專案不是只依靠檔案修改時間判斷快取，而是使用 SHA-256 模板身分及應用內容指紋，同時納入原生程式庫、Manifest 權限與元件、可選功能套件等會影響產物的因素。加密建置則強制採用完整重建。

另外，`ApkBuilder` 透過以套件名稱為鍵的 Mutex，避免多個匯出入口同時建置同一套件時互相破壞暫存檔。

這些設計說明作者已經處理了建置工具常見的效能和併發問題。但**快取指紋是否涵蓋所有會改變產物的輸入，仍然需要透過完整測試和持續追蹤驗證**，不能只因為存在指紋機制就認定快取完全正確。
