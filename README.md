# forAVAr｜單一開工入口

本頁是 forAVAr 系列工作的起始入口。**接手時先讀本 README，再只讀「目前交接文件」；不要整庫掃描、重讀歷史版本或尋找壓縮檔。** 交接文件會指出當前工作、證據、下一步、阻塞條件與必要檔案。

## 框架可視化網頁（GitHub Pages 已可達）

- **正式網址：** [https://upqq21477-star.github.io/ForAVAr/](https://upqq21477-star.github.io/ForAVAr/)。路徑請保留 `ForAVAr` 的大小寫。
- **已實測：** repository metadata 顯示 `private=false`、`has_pages=true`；正式網址可載入「ForAVAr｜唯讀框架可視化原型」。
- **已交付功能：** 本機 JSON 載入、樹狀／關係圖／卡片、搜尋、狀態篩選、局部診斷、引用往返、位置優先的跨視圖選取，以及 WU-C0-17 雙模型唯讀差異、WU-C0-18 關係規則驅動影響候選、WU-C0-19 全域 ID 衝突診斷、WU-C0-20 模型契約相容性與讀檔錯誤復原、WU-C0-21 巢狀 JSON 精確路徑差異、WU-C0-22 三方唯讀變更／衝突分析、WU-C0-23 差異篩選／定位、WU-C0-24 大型差異安全顯示上限、WU-C0-25 影響候選定位。
- **WU-C0-17～25 局部證據：** JavaScript 編譯檢查 `COMPILE_OK`。已記錄的純邏輯模擬數為：雙模型差異 10/10、關係規則影響 10/10、全域 ID 衝突 11/11、契約相容性／profile 防護 10/10、巢狀路徑差異 11/11、三方衝突分析 20/20、篩選與安全上限／定位條件 17/17。安全顯示限制：兩方／三方差異各最多展開 120 項、全域 ID 衝突每側最多 120 個、單一衝突 ID 最多 100 個位置、影響候選及關係端點清單最多 120 項、每候選最多 20 條影響路徑；達上限會明示未展開數量。路徑定位只允許精確全域唯一 ID 的目前版節點；歧義、缺失 ID 不會顯示錯誤的定位按鈕。這些均是純邏輯模擬，不是真實瀏覽器互動或正式驗證器結果；關係登錄表仍為草案。
- **仍待完成：** 真實瀏覽器互動 smoke test（切換四視圖、搜尋／篩選、重設、載入有效與錯誤 JSON、載入比較基準及查看差異）仍為 `NOT_RUN`。按你的要求，先繼續補齊其他功能，將互動測試及完整系統 E4 留到最後。
- **公開範圍提醒：** 整個 repository 是 public，所有已追蹤檔案（包括 `docs/`、`runtime/`、`研究/`、`進度/`）都可被他人查看，不只公開網站首頁。
- 不需要付費部署；GitHub Pages 已可達。已移除不再需要的 Cloudflare fallback 建置腳本，避免同一網頁維護兩套發布路徑。

## 目前工作狀態

- **施工主線：** WU-C0-17～WU-C0-25 已完成雙／三方差異、關係規則影響候選、全域 ID 衝突、契約相容性、精確巢狀 JSON 路徑、結果篩選、渲染上限與影響候選定位；下一步先完成剩餘可獨立施工功能，再依你的要求安排一次有限瀏覽器互動測試。
- **網站狀態：** GitHub Pages 已可達，正式網址見上方；無需再次檢查相同發布設定。
- **獨立驗證支線：** B27.11／T3-0 仍 PARTIAL／NOT_RUN；實際 Python 自比、unittest 載入數與 standard_verify 尚未執行。這只阻塞該驗證支線，不阻止唯讀 UI 施工。
- **唯一目前交接：** [HANDOFF_B27_11.md](https://github.com/upqq21477-star/forAVArb1/blob/main/HANDOFF_B27_11.md)。
- **四梯次原則：** E1 確認設計與判準；E2 檢查重複／衝突並重用既有機制；E3 代碼化及有限模擬；E4 完整系統實際驗收。網站可達或局部模擬不得冒充完整驗收。

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
