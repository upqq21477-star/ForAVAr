# forAVAr｜單一開工入口

本頁是 forAVAr 系列工作的起始入口。**接手時先讀本 README，再只讀「目前交接文件」；不要整庫掃描、重讀歷史版本或尋找壓縮檔。** 交接文件會指出當前工作、證據、下一步、阻塞條件與必要檔案。

## 可直接開啟的框架可視化網頁

- **網頁入口：** [index.html](./index.html)
- **GitHub Pages 預期網址：** https://upqq21477-star.github.io/forAVAr/
- 此網頁使用專案根目錄的 \`index.html\` 作為唯一入口；不再維護研究資料夾中的第二份 HTML。網站是否已由 GitHub Pages 發布，以實際站點回應為準，不能只由檔案存在推定已部署。

## 目前工作狀態

- **目前工作單元：** B27.11／T3-0「基線＋同名測試類別」。
- **狀態：** PARTIAL／NOT_RUN；已完成遠端檔案的靜態核對，實際 Python 執行與標準驗證尚未完成。
- **唯一目前交接：** [HANDOFF_B27_11.md](https://github.com/upqq21477-star/forAVArb1/blob/main/HANDOFF_B27_11.md)。
- **下一步：** 依交接文件完成 T3-0 的實際自比、unittest 載入數核對及要求的驗證，將原始輸出與結果直接寫回 GitHub。**T3-0 未完成前不得進入 T3-1。**
- **若執行環境不具備兩個專案的可讀工作目錄及 Python 執行能力：** 明確回報 BLOCKED／NOT_RUN；不得用靜態推論代替執行結果，不得將工作單元標為完成。

## 接手流程（最低讀取路徑）

1. 讀本頁，了解專案邊界與當前阻塞。
2. 讀唯一目前交接：[HANDOFF_B27_11.md](https://github.com/upqq21477-star/forAVArb1/blob/main/HANDOFF_B27_11.md)。只讀它指定的當前工作單元；不要整讀其他文件。
3. 按交接列出的路徑執行。只在需要確認架構或規則時，查閱 [正式藍圖](https://github.com/upqq21477-star/forAVAr1/blob/main/docs/blueprint.json)、[運作契約](https://github.com/upqq21477-star/forAVAr1/blob/main/docs/operating_contract.json) 或 [進度帳本](https://github.com/upqq21477-star/forAVAr1/blob/main/docs/progress_ledger.json) 中相關段落。
4. 將研究、驗證、實驗輸出與交接紀錄直接提交至資料倉庫；讀回核對路徑、blob SHA 與 commit。交接只保留下一步需要的索引，不重複抄寫整份規格。

## 專案職責與權威順序

- **[forAVAr](https://github.com/upqq21477-star/forAVAr)：** 研究、框架整理及相關專案文件。
- **[forAVAr1](https://github.com/upqq21477-star/forAVAr1)：** 目前主體 Runtime／正式藍圖、運作契約、登錄表、進度及驗收文件的工作來源。
- **[forAVArb](https://github.com/upqq21477-star/forAVArb)：** 可管理的研究／驗證／暫存／實驗資料倉庫；既有退場歸檔路徑只作歷史追溯。
- **[forAVArb1](https://github.com/upqq21477-star/forAVArb1)：** 目前資料、實驗、驗證、工作計畫及交接的主要入口。
- **[P1](https://github.com/upqq21477-star/P1) 與 [P2](https://github.com/upqq21477-star/P2)：** 唯讀；不得新增、修改或刪除。

正式規則以 forAVAr1 的現行運作契約為準；架構以正式藍圖為準；進度／驗收以進度帳本為準。交接負責描述當前工作與下一步，不得覆蓋正式基線。

## 檔案更新規則

- 直接修改授權的 GitHub 專案檔案；每次寫入後讀回核對實際內容。
- **ZIP 不作為工作來源、例行交付物、驗收條件或交接前置條件。** 只有使用者明確要求可攜快照，或有具體備份／復原需求時才建立。
- 不因 README 或交接寫了測試命令，就宣稱已執行或通過；只記錄實際輸出。
- 不得跳過當前工作單元、不得將 NOT_RUN 改寫為 PASS，也不得未經授權提前進入 E4／F2／F3。
