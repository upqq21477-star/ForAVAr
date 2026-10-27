# 讓人看得見、改得動的 AI 理解：藍圖確認介面企劃書

**版本**：v0.4 整合版　**日期**：2026-10-26　**性質**：僅談原理，不含實作

**整合版**：合併三個批次的研討內容。修訂歷程見附錄 G，重現用的腳本見附錄 H、I。

---

## 摘要

AI 在對話中形成的「理解」藏在文字裡，人很難確認它是否正確。本企劃提出一個介面：新對話第一輪結束後，由 AI 依使用者所說內容，自動畫出核心、主軸、骨架及其關係，供人類檢查、修改，再按「輸出」取得完整框架與改動清單。

核心主張有四：（一）所有畫面共用**單一正式資料**，圖只是看法，改圖就是改資料；（二）每項內容分開記錄「來源」與「確認」，不確定處留白而不硬補；（三）輸出時先給完整框架，再對照「基準版」列出改動，且「確認」本身作為獨立動作留下紀錄；（四）對話閘門只要求核心與主軸鏈先確認，其餘可逐步補。

外部研究支持這些方向，但也顯示「關係型共享狀態」尚無成熟驗證。因此本文同時提出評估設計，以植入錯誤的實驗與可重複的模擬測試檢驗效果。本文另將概念逐一拆解並對照外部方法，以模擬挑選儲存形式與過期傳遞規則（附錄 D、E），並以本專案的第一則訊息實測第一輪建圖規則（附錄 F）。

**關鍵詞**：AI 理解校正、關係圖、單一正式資料、來源與確認、對話閘門、差異輸出

---

## 目錄

1. 緒論
2. 設計需求
3. 外部研究回顧
4. 核心架構
5. 資料模型
6. 介面原理
7. 第一輪自動建圖
8. 編輯、檢查與差異
9. 輸出規格
10. 評估設計
11. 風險與限制
12. 建構順序
13. 結論

附錄 A　詞彙對照（人話版）
附錄 B　輸出範例
附錄 C　資料格式示意
附錄 D　概念原子拆解與選型矩陣
附錄 E　模擬結果
附錄 F　自我應用與來源盤點
附錄 G　修訂歷程
附錄 H　模擬腳本
附錄 I　自我應用腳本與原文
參考資料
索引

---

## 1. 緒論

### 1.1 問題
人與 AI 討論一件複雜的事，AI 的理解只存在於它的回答裡。人只能從文字去猜「它到底懂了沒」，錯了也很難指出是哪一處。

### 1.2 目標與範圍
- **目標**：把 AI 的理解變成可檢查、可修改、可輸出的圖，讓後續討論精準對齊。
- **範圍**：本文只談原理與規格。不涉及程式實作、版面美術、特定平台。
- **非目標**：不是漂亮的圖表產生器，也不取代對話本身。

---

## 2. 設計需求

| 編號 | 需求 |
|---|---|
| R1 | 展示目前的核心、主軸、骨架 |
| R2 | 顯示彼此關係，含「介紹、開啟、結束條件」 |
| R3 | 節點顯示名稱與功能 |
| R4 | 用樹狀、關係圖呈現，參考遊戲與公司報告的簡潔風格 |
| R5 | 內容淺白，少專業用語，講作用 |
| R6 | 新對話第一輪結束後，自動依使用者所說建圖 |
| R7 | 人可改連線、條件、關係、數據，可增刪節點與連結，含因果連線 |
| R8 | 輸出鍵：先給整體框架，再指出改動處 |
| R9 | 參考「拖拉、新增、連結即可組建軟體」的工具原理 |

---

## 3. 外部研究回顧

### 3.1 節點式編輯器
n8n、ComfyUI、React Flow 這類工具把一件事拆成節點與連線。設計指引整理出的經驗是：節點應是自成一體的卡片而非接線端子、連線上標出條件、執行時顯示資料流動。[3][4] 有工具以形狀區分節點種類，並把條件線畫成虛線。[2] 工具也把「邏輯」與「版面」分開匯出，使移動位置不影響內容。[5]

### 3.2 共享可編輯狀態
Transfiver 提出：模型與人共同更新同一份狀態，人的修正會改變後續運算所讀的內容，而不是另加一條指示。[1] 另有系統讓每條主張都連著其證據與推理，[7] 或以針對性的小修改（JSON Patch）更新狀態並保留修訂紀錄。[8] 需特別注意：Transfiver 自己表明，擴展到關係型與大規模狀態仍未解決。[1] 故本企劃的「關係圖版本」是待驗證的假設，不是已證明的結論。

### 3.3 差異呈現
圖形差異工具以顏色區分新增、刪除、修改。[6] 一項使用者研究發現，差異圖在判斷邊的增減時錯誤顯著較少，且受測者普遍偏好。[9] 另有工具把代理人提議的結構變更轉為可審閱的圖形差異，衝突時採原版、人類版、AI 版的三方比對。[10]

### 3.4 圖資料庫的取捨
圖資料庫擅長大量資料的多層關係查詢。本企劃的藍圖規模約為數十個節點，此優勢用不上，且需要伺服器。差異也必須比對兩份快照，資料庫本身只存當前狀態，無法直接給出改動。因此本文主張以一份文字檔加版本紀錄即可。以 Git 提交串作為共享記憶的做法已有先例。[11]

### 3.5 證據強度說明
- [1][7][8][11] 為預印本，未必經同行審查。
- [2][3][4][5][10] 為工具文件或社群文章，屬設計經驗，不是實證。
- [9] 為使用者研究，但針對動態圖，與本案情境相近而非相同。
- 「是哪一個 GitHub 拖拉建構工具」未能確認，本文只採用同類工具的共通原理。
- 來源與確認分欄、對話閘門、需複核等規則是本文的設計推演，**尚無外部實證**，列入第 10 章待驗證。
- [12]–[21] 為論文、課程講義、規格文件與實務文章混合。[15][16] 是經課程講義確認，未讀原文；[17] 為二手實務文章，證據最弱。

### 3.6 演算法與方法的外部對照
- **樹或圖的差異比對**：兩棵樹要找出最短的修改清單，含「搬移」時已知是 NP-hard，實務上靠啟發式配對，GumTree 為代表。[12] 啟示：若每個項目有穩定編號，配對問題就消失，差異可線性求得（8.3、附錄 E-T2）。
- **差異的表示**：JSON Patch 以一串 add、remove、replace、move、copy、test 操作描述改動；Merge Patch 只能整份替換陣列，沒有 move 與 test。[13] JSON Patch 的陣列路徑用位置序號，增刪後會位移，故資料宜以「編號為鍵的對照表」存放（5.5）。
- **隨時間變動的事實**：Graphiti 這類記憶圖不覆寫過時的邊，而是記下它何時失效。[14] 本案規模小且有 Git 歷史，不另設失效欄位（附錄 D）。
- **開啟與結束條件的歸屬**：狀態圖把「事件［條件］」放在轉移上，進入與離開動作則屬於狀態本身。[15] 對應本案：開啟條件在連線，完成條件在節點（5.1、5.2）。
- **過期的處理**：真值維護系統以依賴網路記錄每項信念靠什麼成立，前提被撤回時沿依賴往下標記失效，再嘗試找其他支持。[16] 「需複核」是其簡化版：由人重新支持，且只傳一步（5.1）。
- **審閱疲勞**：實務文章一致指出，確認次數多會讓審閱變成走過場；建議縮小需審項目、排優先、把相關變更整批看。[17] 多為二手或實務經驗，證據偏弱。
- **擷取的已知弱點**：模型對「反向關係」（A 依賴 B 與 B 依賴 A）的辨識較差。[18] 封閉本體（先定好關係種類）的擷取較守規則，但自動評分會低估品質，需搭配人工審。[19] 把擷取結果逐條對回原文檢驗的做法也有先例。[20]
- **版面**：樹用 Reingold–Tilford 一類的整齊排版，有向流程用 Sugiyama 分層排版，後者適合數百節點以內的小圖。[21]

---

## 4. 核心架構

### 4.1 單一正式資料
整個系統只有一份正式資料（節點、連線、條件、來源、確認）。樹狀圖、關係圖都只是同一份資料的不同看法。改圖等於改資料，不存在「圖改了、AI 用的還是舊的」。

### 4.2 資料流
使用者所說 → AI 建立草稿 → 正式資料 → 兩種視圖 → 人類編輯（每次產生一筆小修改）→ 正式資料更新 → AI 之後只讀這份資料 → 輸出（完整框架＋對基準版的差異）。

### 4.3 確認與鎖定
「確認」是一個**動作**，有時間與版本，不是順手帶過的屬性。確認後的內容進入鎖定範圍，AI 不得擅自改寫，要改須先提出。沒有確認紀錄，就不算過關。

### 4.4 部署限制
介面與 AI 之間以**純文字（JSON 加人讀版）**進出，貼上即可使用，因此同時適用自動（API）模式與手動模式。手動模式中 AI 可能只讀得到儲存庫首頁，故首頁應能放下當前確認版的摘要。

### 4.5 對話閘門
閘門決定「對話能不能往下走」，對應「對話主軸」模式。

| 階段 | 意思 | 進入條件 |
|---|---|---|
| G0 無圖 | 還沒有任何理解 | 新對話開始 |
| G1 草稿 | AI 已建出初稿 | 第一輪結束 |
| G2 審閱中 | 人正在檢查 | 人開啟介面 |
| G3 軸線已確認 | 閘門通過，可往下做 | 核心與主軸鏈皆為已確認 |
| G4 待複核 | 有已確認項目被牽動 | 出現「需複核」項目 |

規則：
1. **閘門只卡「核心＋主軸鏈」**（從核心出發的流程線與其節點）。骨架與細節可以是「待確認」，只做提醒，不擋路。理由：全部確認才放行會讓人疲勞，反而促成走過場。
2. 核心為空白時停在 G2，由 AI 協助使用者把核心講清楚，直到確認為止。
3. 若使用者開場就已講清楚主軸鏈，AI 直接把它整理成「你說的」並附原句，只請確認一次，不再追問。
4. G4 不擋路，但在輸出與回答前先提示哪幾項需複核。
5. 確認以**一條主軸鏈**為單位整批檢視，而不是逐項點同意（假設 H5，見 10.1）。

---

## 5. 資料模型

### 5.1 節點
| 欄位 | 說明 |
|---|---|
| 編號 | 隱形且永不改。改名不算刪除再新增 |
| 名稱＋作用 | 畫面只顯示這兩項；作用為一句話，動詞開頭 |
| 種類 | 核心、主軸、骨架、模組 |
| 所屬 | 屬於哪個上層節點 |
| **完成條件** | 有流程出口的節點必填：做到什麼程度算「做完」（取代連線上的結束條件） |
| **來源** | 誰提出的：使用者原話／AI 推測／人工編輯（畫面顯示為「你說的／AI 猜的／你改的」） |
| **確認** | 有沒有點頭：待確認／已確認／需複核 |
| 原句 | 來源為「使用者原話」時必填，附原話 |
| 備註、數據 | 選填，點開才看 |

**來源與確認分開的理由**：「你說的」不等於「已確認」，因為 AI 可能把你的話解讀錯；「AI 猜的」被你點頭後，仍保留「AI 猜的」。這樣之後可以算出「AI 猜對了多少」，而不是把功勞和修正混成一團。

規則：
- 人在介面上新增或修改的項目，來源記為「人工編輯」，確認自動為「已確認」（人親手做的就是人的決定）。
- 只按確認、沒修改：來源不變，確認改為「已確認」。
- **需複核**是系統推算出來的，不能手動設定：某節點被改動（改名、改作用、改完成條件、改掛上層、刪除）時，與它**直接相連**的連線與它的**直接子項**，若原為已確認，自動轉為需複核；某條連線被改動時，它兩端的節點同理。再次確認即解除。**只傳一步，不連鎖**：這是真值維護系統「撤回後沿依賴標記失效」[16] 的簡化版；完整連鎖在模擬中會牽動幾乎整張圖（附錄 E-T3），人無法逐項複核。

### 5.2 連線
連線分三族，欄位依族別而定：

| 族別 | 意思 | 開啟條件（在線上） | 結束條件 |
|---|---|---|---|
| 結構 | 包含、屬於 | 不用 | 不用 |
| 流程 | 先後、觸發 | 必填 | 不填在線上，由起點節點的「完成條件」決定 |
| 影響 | 因果、衝突 | 不用 | 不用 |

每條線都有：起點、終點、一句「介紹」（為何相連）、來源、確認、原句。**開啟條件**留在連線上（對應狀態圖的「事件［條件］」），**結束條件**屬於節點本身（對應狀態的離開條件）[15]：一個節點有多條出路時，只需寫一次「做完的標準」，不必在每條線重複，也不會出現同一節點的多條線寫得不一致（附錄 E-T4）。畫面上仍把兩者都顯示在線旁，使人一眼看到「何時開始、何時結束」。連線一律以**主動句**存放與顯示（「A 做完交給 B」），不用被動或反向寫法，以降低方向錯誤 [18]。流程與影響線建議附一個**例子**（一句具體情境，如「A 做完，B 才開始」），讓人用情境驗證而不只看線。類型清單可擴充，但新增前須確認與既有類型意思不同。

### 5.3 空白清單
記錄 AI 不確定、待你補充的問題。空白不畫成節點，不填入猜測。

### 5.4 識別與譜系
編號永不重用。節點被拆成兩個或合成一個時，新節點記錄「來自哪些舊編號」，稱為譜系，使改動可追溯而不被誤判為「全刪全增」。

### 5.5 儲存形式
- 節點與連線以**編號為鍵的對照表**存放，不用陣列：修改的路徑形如「某節點的作用」，不會因增刪而位移（3.6）。
- **版面座標另存**，不混入內容。位置變動因此不產生差異（附錄 E-T1）。
- 正式檔採**一行一項的純文字**（行式），機器用的 JSON 由它產生。實測三十個節點加三十六條連線：格式化 JSON 約 18.9 KB，行式約 8.5 KB（位元組少約 55%，字元少約 74%）；改一個節點的文字，行式與 JSON Lines 只動一行，單行壓縮 JSON 則整份檔案是一行（附錄 E-T5）。
- Mermaid 這類繪圖語法只作顯示輸出，不作正式資料：它放不下來源、確認與條件，實測連「改了節點作用」都無法表達。
- 歷史交給 Git 與基準版，檔內不保留已刪除項目的墓碑或雙時態欄位（附錄 D）。

---

## 6. 介面原理

### 6.1 兩種視圖
只做**樹狀圖**（看層級）與**關係圖**（看連結與條件）。簡報式摘要由輸出時的文字自動產生；遊戲科技樹只是流程族的一種畫法，不另設視圖。

### 6.2 分層展示
第一層：一句話核心。第二層：主軸與骨架，節點約 7 個。第三層：點開才看細節與條件。

### 6.3 手機操作
手機以樹狀清單為主畫面，關係圖為輔。連線用「點選起點、再點選終點」，取代拖拉。

### 6.4 人話用語
連線動詞固定：「由…開始」「做完交給」「直到…才結束」「因為…所以」。專業詞只在需要時出現，並附一句白話。狀態用三個小標：**你說的／AI 猜的／你改的**，加上 ✓（已確認）或「需複核」。

### 6.5 版面演算法
- 樹狀圖：手機用縮排清單；較大畫面用 Reingold–Tilford 一類的整齊樹狀排版 [21]。
- 流程圖：用 Sugiyama 式分層排版（ELK、dagre 這類引擎可用），數十節點規模沒有問題 [21]。
- 位置獨立儲存；只有新增的節點才自動擺放，**不在每次編輯後整張重排**，避免人腦中的「地圖」被打亂。

---

## 7. 第一輪自動建圖

### 7.1 輸入與時機
輸入為使用者第一輪的話與 AI 的首次回應，在第一輪結束時觸發。

### 7.2 抽取規則
| 規則 | 內容 |
|---|---|
| A | 只有使用者明說的內容，來源可記「使用者原話」，且須附原句；其餘一律記「AI 推測」。所有項目初始確認皆為「待確認」 |
| B | 核心至多一個；使用者未明說目的時，核心留空白 |
| C | 第一層節點不超過 7 個，多出的收進上層 |
| D | 連線族別依用語判斷：「X 後，Y」「先…再…」「直到」「當…時」→ 流程；「因為、導致」→ 影響；「包含、由…組成」→ 結構；無線索則不建線。口語連接詞「然後」單獨出現只算弱線索，不足以建流程線；比對「後」時須排除「然後」 |
| E | 有流程出口的節點若使用者沒說完成條件，列入空白清單，不自行補 |
| F | 只出現一次且無強調的名詞放備註，不建節點 |
| G | 標為「使用者原話」的原句，必須**逐字出現**在使用者實際說過的文字中（字串比對）；比對前先統一全半形、去掉空白與標點，因為使用者原文常有多餘空格；正規化後仍找不到就自動降為「AI 推測」。之後可再加「原句是否真的支持該項目」的檢驗 [20] |
| H | 同一行三個以上的並列項（如「新增刪除節點，新增連結，新增因果連線」）收成**同一節點的清單或備註**，不各自成為節點 |

### 7.3 不補空白
資料少是第一輪的常態。顯示「這裡我不確定」，比畫出完整但猜測的圖更可靠。

### 7.4 審閱順序與防走過場
審閱順序：先看「AI 猜的」，再看流程線，最後才看「你說的」。目的是避免人一口氣全按同意（橡皮圖章）。介面可記錄每項的停留與確認方式，供第 10 章評估使用。

### 7.5 失敗模式
| 失敗 | 例子 | 對策 |
|---|---|---|
| 過度推論 | 憑空長出使用者沒提的節點 | 規則 A：標「AI 猜的」，優先審閱 |
| 漏抽 | 使用者提過的重點沒上圖 | 規則 F 的備註保留；空白清單 |
| 概念合併或拆錯 | 兩件事被畫成一個 | 提供拆分與合併操作，並留譜系（5.4） |
| 方向反了 | 「A 依賴 B」畫成「B 依賴 A」 | 「例子」欄讓人用情境驗證；連線一律用主動句呈現（模型對反向關係本就較弱 [18]） |
| 族別錯 | 把先後當成因果 | 線上顯示族別圖示；規則 D 的用語線索 |
| 層級錯置 | 骨架被掛到錯的主軸下 | 樹狀圖一眼可見；改掛不算刪除新增（8.3） |
| 口語連接詞誤判 | 把「然後這個…還要有…」當成先後 | 規則 D：「然後」單獨不建線 |
| 列舉膨脹 | 一行並列的幾個項目全變成節點 | 規則 H：收成同一節點的清單 |
| 引用被誤降級 | 原話多了空格，逐字比對失敗 | 規則 G：比對前先正規化 |

### 7.6 後續回合：增量更新
第一輪之後，AI 不重建整張圖。新內容一律以「建議修改」提出，標為「AI 猜的、待確認」，由人一次審閱一批。鎖定範圍內的項目不得被覆寫；若新內容與已確認內容衝突，列為衝突項，不擅自取代任一方。

---

## 8. 編輯、檢查與差異

### 8.1 即時檢查（人話提醒）
1. 有流程出口的節點缺完成條件：「這件事不知道何時算做完」。流程線缺開啟條件：「不知道何時開始」。
2. 孤立節點：「它沒有跟任何東西相連」。
3. 流程族循環且無出口：「會一直轉下去」。影響族循環允許，因因果可有回饋。
4. 核心只能有一個，主軸必須連到核心。
5. 待確認的項目不可進入鎖定。
6. 出現需複核項目：「這幾項因為旁邊改了，請再看一眼」。

### 8.2 編輯動作
新增、刪除、改名、改作用、改連線的起訖或方向、改族別、改條件、改數據、增刪因果線、改掛上層、拆分、合併、撤銷。刪除節點前，先列出會連帶受影響的線。每個動作轉成一筆明確的小修改，而非讓 AI 重新用語言猜。

### 8.3 差異認定
- 以編號比對內容；**位置變動不算改動**。
- 分五類：新增、刪除、修改、改連線、**確認**。「確認」獨立成類，內容沒變但共識變了，混入修改會讓人分不出「AI 本來就對」與「你改過」。
- **改掛上層**算「修改」，不是刪除再新增；**拆分與合併**依譜系記為一組關聯的新增與刪除，並標明來自哪些舊編號。
- 影響範圍沿連線往下走一遍即可求得。
- 驗證性質：把基準版套上差異必須得到編輯後版本；只移動位置時差異為空。
- **為何靠編號**：不靠編號的樹差異，含搬移時最短修改清單已知是 NP-hard，只能用啟發式配對 [12]。模擬中，對重新產生、沒有編號的圖，只憑名稱配對時，節點改名後的配對成功率為 0%；先比名稱再比作用，改名可救回 87.5%，但名稱與作用同時改則只剩 0.1%（附錄 E-T2）。有編號則為線性比對、無歧義。這也是 7.6 規定「AI 不重建整圖」的原因。
- **差異格式**：只需 add、remove、replace 三種操作（改掛上層只是替換「所屬」欄，不需要 move），外加「基準版編號」前置檢查，對應 JSON Patch 的 test 操作 [13]：基準版不符就拒絕套用。

### 8.4 三方比對
之後若 AI 也改圖，採三方比對：基準版、人類版、AI 新版。衝突時標示，由人決定採用哪一方，不默默覆蓋。

---

## 9. 輸出規格

### 9.1 三段式
- **A　完整框架**：一句話核心、樹狀結構、節點清單、連線清單、空白清單；每項附來源與確認標記。
- **B　本次變更**：編號、類型、對象、改前→改後、影響到誰。
- **C　鎖定範圍**：已確認且未動的部分，以及目前需複核的項目。

### 9.2 基準版規則
差異一律對「上次確認版」比，不靠 AI 回想。初次輸出標為初始版，只有 A 與 C，B 註明「初始版，無舊內容」。

### 9.3 鎖定
C 段是 AI 後續工作的界線。若對話內容與已確認內容衝突，以圖為準，並由 AI 指出衝突。

### 9.4 格式
- 人讀：Markdown。
- 機器讀：JSON（保存編號、來源、確認、條件、修改，見附錄 C）。
- 圖片或簡報大綱為次要產出，因為圖片無法完整保存語意。

---

## 10. 評估設計

### 10.1 假設
- H1：用圖審閱，比用文字摘要審閱更能找出 AI 的誤解。
- H2：「來源標記＋優先審閱推測」能降低走過場。
- H3：確認後，AI 後續回答與已確認框架的矛盾次數下降。
- H4：閘門只卡核心與主軸鏈，比「全部確認才放行」更少走過場，且不增加主軸層級的錯誤。
- H5：以主軸鏈為單位整批確認，比逐項確認更少走過場，且不增加主軸層級的錯誤。

### 10.2 植入錯誤實驗
取一份已知正確的框架，讓 AI 的理解中植入數個錯誤，類型對應 7.5：方向反了、缺完成條件、層級錯置、多出節點、族別錯。受試者分別以文字摘要或圖來審閱（交叉對照，同一人兩種都做），記錄找出率、用時、誤報。另設一組對照：**先寫後看**，先請使用者自己寫下一句核心，再顯示 AI 的版本，比較兩者的錯誤找出率。此做法源自自動化偏誤的緩解建議 [17]，在本案是否有效未知。

### 10.3 指標
| 指標 | 意義 |
|---|---|
| 各類錯誤找出率 | 圖在哪類錯誤上有優勢 |
| 誤報率 | 是否讓人疑神疑鬼 |
| 走過場率 | 單次全選同意的比例、每項停留時間 |
| 差異準確度 | 輸出的改動對照真實編輯的精確度與召回率 |
| 漂移次數 | 確認後 AI 回答與框架矛盾的次數 |
| 首輪準確率 | 「AI 猜的」被原樣確認的比例（來源與確認分欄後才算得出） |
| 複核負擔 | 單次編輯平均牽動幾個需複核項目（模擬基準：一步傳遞約 2 項，附錄 E-T3） |
| 設計來源占比 | 框架中來自使用者原話與來自 AI 推測的項目比例，用來看使用者實際確認了多少（附錄 F-6） |
| 覆寫率 | 使用者改動或否決 AI 項目的比例；長期極低可能代表走過場（實務經驗，非定論）[17] |

### 10.4 模擬優先
差異與檢查屬於確定性規則，可先用腳本化的編輯集做模擬測試：預期差異完全吻合、僅移動位置時差異為空、套用差異可還原、改掛與拆合的譜系正確、需複核的觸發與解除符合 5.1。確定性測試的第一版結果見附錄 E（皆為對自身實作的內部一致性檢驗，不代表人類實驗結果）。人類實驗在其後進行。

### 10.5 通過門檻
確定性測試要求全部吻合。人類實驗的門檻（例如找出率差距、可接受的走過場率）**須在收集資料前訂定並記錄**，不在看到結果後調整，以免事後挑選標準。

---

## 11. 風險與限制

1. **圖是有損的投影**：圖正確不等於 AI 真的理解，故需要「例子」欄與評估實驗。
2. **證據有限**：關係型共享狀態尚未被證明有效，[1] 本案屬待驗證假設；來源與確認分欄、閘門、需複核等新規則也屬設計推演（3.5）。
3. **確認不等於正確**：人確認的是共識，可能一起錯。以版本與確認紀錄保留回溯能力。
4. **過度設計**：視圖、關係類型、狀態一多就違背「簡潔」。來源與確認雖是兩欄，畫面上仍只顯示一個小標加一個勾。
5. **小螢幕**：圖形編輯在手機上不易，需以清單為主。
6. **模擬的限制**：附錄 E 使用隨機產生的圖與編輯，只檢驗規則與實作是否自洽，不代表真實對話內容與人類行為。
7. **複核疲勞**：需複核若觸發太頻繁，人會學會忽略；10.3 的「複核負擔」即為監測此點。一步傳遞在模擬中平均約 2 項、最多 11 項（附錄 E-T3），但這只衡量負擔，不衡量「漏掉真正受牽動的項目」，後者仍待人類實驗。

---

## 12. 建構順序

| 階段 | 能力 | 完成後狀態 |
|---|---|---|
| 一 | 資料格式、節點與連線、樹狀與關係圖、細節編輯 | 能完整查看並修改 |
| 二 | 第一輪自動建圖、來源與確認、空白清單 | AI 理解以可編輯形式呈現 |
| 三 | 即時檢查、需複核、對話閘門 | 修改時能發現矛盾，對話能卡在主軸 |
| 四 | 基準版、差異、三段式輸出、增量更新 | 可讀可存可交接 |
| 五 | 評估實驗、其他展示方式 | 驗證成效並擴充 |

先建可信的資料模型，再做自動建圖與差異，最後才做展示效果。

---

## 13. 結論

本企劃把「AI 的理解」定義為一份可檢查的共同資料：單一正式資料、來源與確認分開記錄、可驗證的差異、獨立的確認動作，以及只卡主軸的對話閘門。圖形只是讓人看懂與修改的窗口。最需要優先確立的不是外觀，而是這些規則，以及用實驗檢驗它是否真的比文字更不易誤解。

---

## 附錄 A　詞彙對照（人話版）

| 專業說法 | 人話 |
|---|---|
| 節點 | 一件事、一個部分 |
| 連線／邊 | 兩件事之間的關係 |
| 單一正式資料 | 只有一份真正算數的內容 |
| 基準版 | 上一次你點頭確認的版本 |
| 差異 | 這次比上次改了什麼 |
| 來源 | 這是你說的、我猜的，還是你改的 |
| 確認 | 你有沒有點頭 |
| 需複核 | 旁邊改了，請再看一眼 |
| 鎖定 | 已確認的，不能偷偷改 |
| 閘門 | 主軸沒確認前，先不往下做 |
| 譜系 | 這個新項目是從哪些舊項目來的 |
| 完成條件 | 這件事做到什麼程度算做完 |
| 穩定編號 | 每個項目永不改變的身分證 |

## 附錄 B　輸出範例（虛構內容，僅示意格式）

**A　完整框架**
- 核心：讓使用者確認 AI 的理解（你說的 ✓）
- 節點：N1 建圖｜把第一輪對話整理成圖｜完成條件：使用者按確認｜AI 猜的 ✓
- 連線：N1 → N2｜建圖完成後交給審閱｜開啟：第一輪結束｜待確認
- 空白：審閱完成後要不要自動存檔？

**B　本次變更**
| 編號 | 類型 | 對象 | 改前→改後 | 影響 |
|---|---|---|---|---|
| N1 | 確認 | 建圖 | 待確認→已確認（來源仍為 AI 猜的） | 進入鎖定 |
| N1 | 修改 | 完成條件 | 空白→使用者按確認（來源改為你改的） | 流程完整 |

**C　鎖定範圍**：核心、N1。需複核：無。

## 附錄 C　資料格式示意（原理示意，欄位名稱實作時可改）
實際存檔採行式純文字（5.5），此處以 JSON 示意欄位。

```json
{
  "版本": 3,
  "基準版": 2,
  "節點": [
    {"id": "n1", "名稱": "建圖", "作用": "把第一輪對話整理成圖",
     "種類": "主軸", "所屬": "n0",
     "完成條件": "使用者按確認",
     "來源": "AI推測", "確認": "已確認", "原句": null}
  ],
  "連線": [
    {"id": "l1", "起": "n1", "終": "n2", "族": "流程",
     "介紹": "建圖完成後交給審閱",
     "開啟": "第一輪結束",
     "來源": "使用者原話", "確認": "待確認",
     "原句": "（使用者的原話）", "例子": "建圖完成，才開始審閱"}
  ],
  "空白": [{"id": "q1", "問題": "審閱完成後要不要自動存檔？"}],
  "譜系": [{"新": "n5", "來自": ["n3", "n4"], "操作": "合併"}],
  "確認紀錄": [{"對象": "n1", "版本": 3}]
}
```

---

## 附錄 D　概念原子拆解與選型矩陣

把整份企劃拆成最小的概念單位（原子），逐一對照外部方法，再依本案限制選型。

| 概念原子 | 要解決的問題 | 外部方法或演算法 | 本案選型 | 依據與強度 |
|---|---|---|---|---|
| 單一正式資料 | 圖與 AI 使用的內容不一致 | 共享可編輯狀態 [1]；共享脈絡圖 [7] | 採用 | 預印本；關係型狀態未證明 [1] |
| 項目身分 | 改名、改掛不被誤判 | 穩定編號；啟發式樹配對（GumTree）[12] | 穩定編號，不做配對 | 模擬 E-T2；NP-hard 論述來自 [12] |
| 差異表示 | 輸出改動且可還原 | JSON Patch、Merge Patch [13] | 編號為鍵＋ add／remove／replace＋基準版前置檢查 | 規格文件；模擬 E-T1 |
| 歷史與版本 | 對照基準版、可回溯 | Git 提交串 [11]；失效時間戳（Graphiti）[14] | Git＋基準版；不設失效欄位與墓碑 | 小規模、單一使用者；設計判斷 |
| 儲存形式 | 手機可貼、可讀、差異小 | 格式化 JSON、單行 JSON、JSON Lines、行式文字、Mermaid | 行式純文字為正式檔，JSON 由它產生；Mermaid 僅作輸出 | 模擬 E-T5 |
| 條件的歸屬 | 開啟與結束放哪裡 | 狀態圖：轉移上有事件［條件］，狀態上有進入與離開動作 [15] | 開啟在連線，完成在節點 | 設計推演；模擬 E-T4 |
| 關係分類 | 關係種類太多太亂 | 自訂三族（結構、流程、影響） | 採用 | 本文設計，無外部實證 |
| 來源與可追溯 | 分清你說的與猜的 | 證據連結 [7]；逐條對回原文 [20] | 來源與確認分欄；原句逐字比對 | 預印本；字串比對為確定性規則 |
| 確認與過期 | 周邊改動後確認是否仍有效 | 真值維護系統 [16] | 簡化版：需複核，只傳一步 | 設計推演；模擬 E-T3 |
| 抗疲勞 | 避免走過場 | 縮小需審範圍、優先排序、整批審閱、覆寫率 [17] | 閘門縮範圍；推測優先；鏈式確認（待驗證 H5） | 二手與實務文章，證據弱 |
| 擷取 | 第一輪自動建圖 | 封閉本體擷取 [19]；對回原文檢驗 [20]；反向關係弱點 [18] | 封閉本體（三族加四種類）；主動句；例子欄 | 工作坊論文與基準；本案未實測 |
| 版面 | 看得懂、不亂跳 | 整齊樹狀、Sugiyama 分層、力導向、樹圖 [21] | 樹：縮排清單；流程：分層；位置另存、不整圖重排 | 教材與綜述 |
| 圖資料庫 | 儲存與查詢 | 屬性圖資料庫 | 不採 | 規模小、需伺服器、無法直接給差異（3.4） |
| 評估 | 證明有效 | 植入錯誤實驗；確定性模擬 | 兩者並用，門檻事先訂定 | 第 10 章 |

**最優解的定義**：在本案限制（手機、純文字進出、數十節點的小圖、人話、複雜度越低越好）下，選出「滿足所有限制且最簡單」的組合。它不是全域最佳，也未在人類使用者身上驗證；表中標為「設計推演」或「證據弱」的項目，都是第 10 章要檢驗的假設。

---

## 附錄 E　模擬結果

**方法**：Python 腳本，固定亂數種子（7），隨機產生含核心、4–6 條主軸、其餘骨架的樹，再加流程線（約 0.5 倍節點數）與影響線（約 0.15 倍節點數）。腳本見附錄 H，可重現。

### E-T1　差異的確定性性質
3000 次隨機單一編輯（圖含 20、40、80 個節點各約三分之一）；另做 500 次連續 5–15 次編輯。

| 性質 | 結果 |
|---|---|
| 相同版本，差異為空 | 3000 / 3000 |
| 套用差異可還原編輯後版本 | 3000 / 3000 |
| 僅移動位置（版面另存），差異為空 | 324 / 324 |
| 只按確認，被歸為「確認」類 | 317 / 317 |
| 改名被歸為「修改」，而非新增加刪除 | 284 / 284 |
| 連續編輯後仍可還原 | 500 / 500 |

註：這是對自身實作的自洽檢驗；「位置不入差異」是因為版面另存的設計使然。

### E-T2　沒有編號時的節點配對成功率
重新產生的圖不帶編號，每格 2000 次。

| 編輯類型 | 只比名稱 | 先名稱後作用 | 穩定編號 |
|---|---|---|---|
| 只改名 | 0.0% | 87.5% | 100% |
| 只改作用 | 99.9% | 99.8% | 100% |
| 名稱與作用都改 | 0.0% | 0.1% | 100% |

假設：名稱與作用在圖內大致唯一。真實文字更常重複（會更差），也可用結構線索輔助（會更好，未實作）。

### E-T3　一次節點編輯造成的需複核項目數
30 張圖，每張 200 次編輯。

| 規模（約項目數） | 一步傳遞：平均（占比）／p90／最大 | 沿流程線連鎖：平均／p90／最大 | 全連鎖：平均（占比） |
|---|---|---|---|
| 20 節點（33） | 2.1（6.4%）／4／8 | 3.4／7／16 | 32.0（97.0%） |
| 40 節點（66） | 2.2（3.3%）／4／9 | 3.4／8／20 | 65.0（98.5%） |
| 80 節點（132） | 2.3（1.7%）／5／11 | 3.7／8／36 | 131.0（99.2%） |

解讀：全連鎖幾乎等於整張圖，不可用；一步傳遞的負擔幾乎不隨規模增加；沿流程線連鎖在大圖偶爾暴增（最多 36 項）。限制：此處只衡量**負擔**，不衡量**漏報**。

### E-T4　結束條件的存放位置
每格 200 張圖。

| 節點數 | 存在連線上要填 | 存在節點上要填 | 需寫相同內容的節點數 |
|---|---|---|---|
| 20 | 10.0 | 7.9 | 1.8 |
| 40 | 20.0 | 15.7 | 3.7 |
| 80 | 40.0 | 31.5 | 7.2 |

存在節點上約少填 21% 欄位；存在連線上時，有數個節點的多條出線必須重複寫一模一樣的內容，易生不一致。

### E-T5　序列化形式
30 個節點、36 條連線；改一個節點的作用文字。

| 格式 | 位元組 | 字元 | 變動行數 | 備註 |
|---|---|---|---|---|
| 格式化 JSON | 18853 | 14355 | 2（一刪一增） | 一項多行 |
| 單行壓縮 JSON | 13336 | 8838 | 2 | 整份檔案只有一行，差異粒度最差 |
| JSON Lines | 13644 | 9146 | 2 | 一行一項 |
| 行式文字 | 8526 | 3764 | 2 | 最小，一行一項 |
| Mermaid | 2304 | 1336 | 0 | 放不下來源、確認、條件，改作用無法表達 |

未量測語言模型的字詞單位數（無離線分詞器），僅以位元組與字元作代理。

---

## 附錄 F　自我應用與來源盤點

**做法**：把本專案使用者的第一則訊息當作「第一輪輸入」，依 7.2 的規則手工建出第一輪草稿，再用腳本驗證。驗證腳本與原文見附錄 I。

### F-1　第一輪草稿（只依第一則訊息）
- 核心：讓人類確認 AI 的理解沒有錯誤。
- 主軸四條：展示、自動建圖、編輯、輸出。骨架四項：節點顯示、呈現方式、淺白語言、拖拉建構工具原理。
- 流程線三條：自動建圖→展示（開啟：第一次對話結束）、展示→編輯（開啟：有錯誤時）、編輯→輸出（使用者沒說，記為 AI 推測）。影響線一條：拖拉工具原理→編輯（目標為 AI 推測）。
- 空白清單四項：「GitHub 工具」是哪一個、「整體框架內容」含哪些欄位、編輯何時算做完、建圖何時算做完。
- 統計：13 項（9 節點、4 連線），標「你說的」11 項、「AI 猜的」2 項、空白 4 項。

### F-2　規則 G（原句逐字比對）
- 13 項中的 12 條原句全部逐字存在於原文。
- **陷阱**：使用者寫的是「好理解 ，敘述」（逗號前有空格）。若 AI 把引文整理成「好理解，敘述」，逐字比對會失敗，正規化後則通過。故規則 G 須先正規化。
- 改寫過的句子（「讓使用者檢查 AI 有沒有理解錯」）逐字與正規化比對皆失敗，會被正確降為「AI 推測」。
- 限制：比對只證明「這句話存在」，不證明「這句話支持該項目」。

### F-3　規則 D（用語判斷流程線）
- 「然後」出現 3 次：一次是話題轉換（「然後這個 ui 還要有一個功能」）、一次是弱先後（「然後有一個輸出按鍵」）、一次是明確先後（「然後先輸出整體框架內容，再指出更改部分」）。只有「先…再…」可靠。
- 單字「後」在原文出現 4 次，其中 3 次是「然後」的一部分，真正的先後只有「開啟新對話後，第一次對話結束」。
- 結論：用語線索須成對判斷，不能只看單字。

### F-4　規則 H（列舉）
同一行三個以上並列的有 7 行、共 25 項。若各自成為節點，草稿會由 9 個節點膨脹到 34 個，違反 7.2 規則 C 的上限；應收成同一節點的清單。

### F-5　這個實驗的限制
- 草稿是作者在**已知後續內容**的情況下手工建的，「你說的 11／13」可能高估真實的自動建圖表現。
- 沒有請使用者確認，所以「首輪準確率」尚未量到。
- 只有一則訊息、一位使用者，不能推論到其他情況。

### F-6　來源盤點：本企劃的設計成分從哪來
以下為作者的**人工盤點**，粒度由作者決定，數字只供參考。

**來自使用者原話（10 項）**
1. 展示核心、主軸、骨架
2. 連線顯示介紹、開啟、結束條件
3. 節點顯示名稱與功能
4. 樹狀、關係圖，簡潔風格
5. 淺白人話
6. 第一輪結束後自動建圖
7. 用來確認 AI 的理解
8. 可直接修改（含增刪節點、連結、因果連線）
9. 輸出鍵：先整體、再改動處
10. 參考拖拉建構工具原理

**來自 AI 推測（15 項，待使用者確認）**
1. 單一正式資料：圖就是資料，改圖就是改資料
2. 來源與確認分欄
3. 連線分三族（結構、流程、影響）
4. 結束條件改存在節點（完成條件）
5. 空白清單：不確定的不硬補
6. 對話閘門只卡核心與主軸鏈
7. 需複核：已確認項目的周邊被改，要再看一眼，只傳一步
8. 基準版與確認紀錄
9. 穩定編號
10. 行式純文字儲存、版面另存
11. 原句逐字比對
12. 分層展示與手機優先
13. 輸出第三段「鎖定範圍」
14. 評估設計（植入錯誤實驗、模擬）
15. 不採圖資料庫

來自使用者原話約 40%（10／25）。其餘是 AI 的推演，使用者尚未逐項確認。沉默不等於確認。

---

## 附錄 G　修訂歷程


**v0.3 → v0.4**（自我應用：拿本專案第一則訊息實測第一輪建圖規則）
1. 規則 G 補上**正規化**：使用者原文常有多餘空格或全半形差異，逐字比對前須先統一，否則會誤降級（實測見附錄 F）。
2. 規則 D 修正：口語連接詞「然後」不能單獨當流程線索（實測 3 次出現只有 1 次是真正的先後）。
3. 新增規則 H：同一行三個以上的並列項**收成一個節點的清單**，不各自成節點（實測 7 行並列共 25 項，會讓草稿從 9 個節點膨脹到 34 個）。
4. 新增附錄 F：自我應用與**來源盤點**——本企劃的設計成分中，來自使用者原話與來自 AI 推測各占多少，並列出待使用者確認的 AI 新增項目。
5. 評估指標新增「設計來源占比」（10.3）。

**v0.2 → v0.3**（概念拆解、外部方法對照與模擬）
1. 新增附錄 D（概念原子拆解與選型矩陣）與附錄 E（模擬結果）。
2. **結構更正**：「結束條件」改存在**節點**（完成條件），「開啟條件」留在**連線**。依據：狀態圖把轉移條件與進出動作分開存放；模擬顯示可少填約 21% 欄位，並免去同一節點多條線內容不一致的問題。見 5.1、5.2。
3. 儲存形式定為「編號為鍵＋行式純文字」，版面座標另存（5.5）。
4. 「需複核」限定為**一步傳遞**（5.1）；連鎖傳遞在模擬中幾乎牽動整張圖。
5. 新增原句逐字比對（7.2 規則 G）與方向錯誤對策（7.5）。
6. 新增版面演算法選型（6.5）、鏈式確認假設 H5 與「先寫後看」對照（10.1、10.2）。
7. 新增外部方法對照（3.6）；參考資料新增 [12]–[21]。

**v0.1 → v0.2**
1. **結構更正**：v0.1 把「你說的／AI 推測／已確認」放在同一欄，混淆了兩件事。v0.2 拆成兩個獨立欄位：**來源**（誰提出的）與**確認**（有沒有被點頭）。詳見 5.1。
2. 新增 **需複核** 狀態：已確認的內容，若周邊被改動，需重新確認。
3. 新增 **對話閘門**（4.5）：閘門只卡「核心＋主軸鏈」，不要求整張圖全部確認。
4. 新增 **失敗模式**（7.5）與 **後續回合的增量更新**（7.6）。
5. 擴充差異規則（8.3）：改掛上層、拆分、合併的處理；新增 **譜系**（5.4）。
6. 評估補充「首輪準確率」「複核負擔」，並要求通過門檻事先訂定（10.5）。
7. 新增附錄 C：資料格式示意。

---

## 附錄 H　模擬腳本

附錄 E 的來源。需要 Python 3，不需額外套件；固定亂數種子，結果可重現。

```python
import random, json, copy, difflib, statistics as st
random.seed(7)
NAMES = ["建圖","審閱","確認","輸出","對照","鎖定","複核","抽取","標記","比對","展示","編輯","檢查","存檔","匯入","整理","排序","合併","拆分","回寫"]
ROLES = ["把第一輪對話整理成圖","讓使用者逐項點頭","比對兩個版本的差異","把結果寫成文字檔","找出需要再看一眼的項目","停止未確認的改動","把想法拆成幾個部分","標出哪些是猜的","列出本次改了什麼","把畫面上的修改存回資料"]
def rname(): return random.choice(NAMES)+random.choice(NAMES)+str(random.randint(0,99))
def rrole(): return random.choice(ROLES)+random.choice(["","，再交給下一步","，完成才往下"])+str(random.randint(0,9))

def gen(n=40, nflow=None, ninf=None):
    nodes={}; edges={}; layout={}
    nodes["n0"]=dict(name="核心",role="讓使用者確認AI的理解",kind="核心",parent=None,origin="使用者原話",confirm="待確認",quote="…")
    k=random.randint(4,6)
    for i in range(1,k+1):
        nodes[f"n{i}"]=dict(name=rname(),role=rrole(),kind="主軸",parent="n0",origin="AI推測",confirm="待確認",quote=None)
    for i in range(k+1,n):
        par=random.choice([x for x in nodes if x!="n0"])
        nodes[f"n{i}"]=dict(name=rname(),role=rrole(),kind="骨架",parent=par,origin="AI推測",confirm="待確認",quote=None)
    ids=[x for x in nodes if x!="n0"]
    nflow=nflow or int(0.5*n); ninf=ninf or int(0.15*n)
    eid=0
    for _ in range(nflow):
        a,b=random.sample(ids,2)
        edges[f"l{eid}"]=dict(src=a,dst=b,family="流程",intro=rrole(),open=rrole(),end=rrole(),origin="AI推測",confirm="待確認"); eid+=1
    for _ in range(ninf):
        a,b=random.sample(ids,2)
        edges[f"l{eid}"]=dict(src=a,dst=b,family="影響",intro=rrole(),open=None,end=None,origin="AI推測",confirm="待確認"); eid+=1
    for x in nodes: layout[x]=(random.random(),random.random())
    return dict(nodes=nodes,edges=edges),layout

# ---------- diff / patch (JSON-Patch-like, id-keyed maps) ----------
def diff(a,b):
    ops=[]
    for coll in ("nodes","edges"):
        A,B=a[coll],b[coll]
        for i in B:
            if i not in A: ops.append(("add",f"/{coll}/{i}",copy.deepcopy(B[i])))
        for i in A:
            if i not in B: ops.append(("remove",f"/{coll}/{i}",None))
        for i in A:
            if i in B:
                for f in B[i]:
                    if A[i].get(f)!=B[i][f]: ops.append(("replace",f"/{coll}/{i}/{f}",B[i][f]))
    return ops
def apply(a,ops):
    r=copy.deepcopy(a)
    for op,path,val in ops:
        p=path.strip("/").split("/")
        if op=="add": r[p[0]][p[1]]=copy.deepcopy(val)
        elif op=="remove": del r[p[0]][p[1]]
        else: r[p[0]][p[1]][p[2]]=val
    return r
def classify(ops):
    cats=set()
    for op,path,val in ops:
        p=path.strip("/").split("/")
        if op=="add": cats.add("新增")
        elif op=="remove": cats.add("刪除")
        else:
            f=p[2]
            if f=="confirm": cats.add("確認")
            elif p[0]=="edges" and f in("src","dst","family"): cats.add("改連線")
            else: cats.add("修改")
    return cats

def descendants(g,x):
    out=set(); st_=[x]
    while st_:
        y=st_.pop()
        for k,v in g["nodes"].items():
            if v["parent"]==y and k not in out: out.add(k); st_.append(k)
    return out
def rand_edit(g,layout,counter):
    g2=copy.deepcopy(g); L2=dict(layout)
    kind=random.choice(["rename","role","reparent","addnode","delleaf","addedge","deledge","retarget","confirm","move"])
    N=g2["nodes"]; E=g2["edges"]
    ids=[x for x in N if x!="n0"]
    if kind=="rename": N[random.choice(ids)]["name"]=rname()
    elif kind=="role": N[random.choice(ids)]["role"]=rrole()
    elif kind=="reparent":
        x=random.choice(ids); bad=descendants(g2,x)|{x}
        c=[y for y in N if y not in bad]; N[x]["parent"]=random.choice(c)
    elif kind=="addnode":
        counter[0]+=1; i=f"n{1000+counter[0]}"
        N[i]=dict(name=rname(),role=rrole(),kind="骨架",parent=random.choice(list(N)),origin="人工編輯",confirm="已確認",quote=None); L2[i]=(0.5,0.5)
    elif kind=="delleaf":
        leaves=[x for x in ids if not any(v["parent"]==x for v in N.values())]
        if leaves:
            x=random.choice(leaves); del N[x]
            for k in [k for k,v in E.items() if v["src"]==x or v["dst"]==x]: del E[k]
    elif kind=="addedge":
        counter[0]+=1; a,b=random.sample(ids,2)
        E[f"l{1000+counter[0]}"]=dict(src=a,dst=b,family="流程",intro=rrole(),open=rrole(),end=rrole(),origin="人工編輯",confirm="已確認")
    elif kind=="deledge":
        if E: del E[random.choice(list(E))]
    elif kind=="retarget":
        if E:
            k=random.choice(list(E)); E[k]["dst"]=random.choice([x for x in ids if x!=E[k]["src"]])
    elif kind=="confirm":
        t=random.choice(list(N)); N[t]["confirm"]="已確認"
    elif kind=="move":
        x=random.choice(list(L2)); L2[x]=(random.random(),random.random())
    return g2,L2,kind

# ---------- T1: diff properties ----------
trials=3000; ok_round=0; ok_ident=0; move_empty=0; moves=0; confirm_only=0; confirms=0
rename_as_modify=0; renames=0
for t in range(trials):
    g,L=gen(random.choice([20,40,80])); cnt=[0]
    ok_ident+= (diff(g,g)==[])
    g2,L2,kind=rand_edit(g,L,cnt)
    ops=diff(g,g2)
    ok_round+= (apply(g,ops)==g2)
    if kind=="move":
        moves+=1; move_empty+= (ops==[])   # layout is separate -> diff on logic data
    if kind=="confirm":
        confirms+=1; c=classify(ops); confirm_only+= (c=={"確認"} or c==set())
    if kind=="rename":
        renames+=1; rename_as_modify+= (classify(ops)=={"修改"})
print("T1 diff properties over",trials,"random single edits (n in 20/40/80)")
print("  identity -> empty diff:",ok_ident,"/",trials)
print("  apply(base,diff)==edited:",ok_round,"/",trials)
print("  position-only edit -> empty diff:",move_empty,"/",moves)
print("  confirm-only edit classified as 確認 only:",confirm_only,"/",confirms)
print("  rename classified as 修改 (not add+delete):",rename_as_modify,"/",renames)

# multi-edit sessions
sess=500; okS=0
for s in range(sess):
    g,L=gen(40); base=copy.deepcopy(g); cnt=[0]; cur=g; Lc=L
    for _ in range(random.randint(5,15)):
        cur,Lc,_k=rand_edit(cur,Lc,cnt)
    okS+= (apply(base,diff(base,cur))==cur)
print("  multi-edit sessions (5-15 edits) round trip:",okS,"/",sess)

# ---------- T2: identity-less matching vs stable ids ----------
def match_accuracy(strategy,kind,trials=2000):
    ok=0
    for _ in range(trials):
        g,L=gen(40); g2=copy.deepcopy(g); x=random.choice([k for k in g2["nodes"] if k!="n0"])
        if kind=="rename": g2["nodes"][x]["name"]=rname()
        elif kind=="role": g2["nodes"][x]["role"]=rrole()
        elif kind=="both": g2["nodes"][x]["name"]=rname(); g2["nodes"][x]["role"]=rrole()
        # regenerated graph without ids: shuffle ids
        old=g["nodes"]; new=g2["nodes"]
        newlist=list(new.items()); random.shuffle(newlist)
        # truth: id x maps to its edited counterpart
        found=None
        if strategy=="name":
            m=[k for k,v in newlist if v["name"]==old[x]["name"]]
            found=m[0] if len(m)==1 else None
        elif strategy=="name+role":
            m=[k for k,v in newlist if v["name"]==old[x]["name"]]
            if len(m)!=1: m=[k for k,v in newlist if v["role"]==old[x]["role"]]
            found=m[0] if len(m)==1 else None
        elif strategy=="id": found=x
        ok+= (found==x)
    return ok/trials
print("T2 node matching accuracy for the edited node (fresh graph without ids), 2000 trials each")
for kind in ("rename","role","both"):
    print(f"  edit={kind:7s} name-only={match_accuracy('name',kind):.3f} name-then-role={match_accuracy('name+role',kind):.3f} stable-id={match_accuracy('id',kind):.3f}")

# ---------- T3: stale propagation ----------
def adj(g):
    A={x:set() for x in g["nodes"]}
    for k,v in g["nodes"].items():
        if v["parent"]: A[k].add(v["parent"]); A[v["parent"]].add(k)
    return A
def items_total(g): return len(g["nodes"])+len(g["edges"])
def stale_sets(g,x,kind):
    """items made stale by an edit of node x (rule R1: 1-hop)"""
    inc=[k for k,v in g["edges"].items() if v["src"]==x or v["dst"]==x]
    ch=[k for k,v in g["nodes"].items() if v["parent"]==x]
    s1=set(inc)|set(ch)
    return s1,inc,ch
def propagate(g,x,rule):
    s1,inc,ch=stale_sets(g,x,"edit")
    stale=set(s1)
    if rule=="R1": return stale
    # frontier nodes: endpoints of stale edges + stale children
    def nodes_of(items):
        ns=set()
        for it in items:
            if it in g["edges"]: ns|={g["edges"][it]["src"],g["edges"][it]["dst"]}
            else: ns.add(it)
        return ns-{x}
    if rule=="R2":   # transitive only along flow edges downstream
        seen={x}; q=[x]
        while q:
            y=q.pop()
            for k,v in g["edges"].items():
                if v["family"]=="流程" and v["src"]==y:
                    stale.add(k)
                    if v["dst"] not in seen: seen.add(v["dst"]); stale.add(v["dst"]); q.append(v["dst"])
        return stale|s1
    if rule=="R3":   # TMS-style closure over every link
        A=adj(g)
        for k,v in g["edges"].items(): A[v["src"]].add(v["dst"]); A[v["dst"]].add(v["src"])
        seen={x}; q=[x]
        while q:
            y=q.pop()
            for z in A[y]:
                if z not in seen: seen.add(z); q.append(z)
        stale=set(seen)-{x}
        stale|={k for k,v in g["edges"].items() if v["src"] in seen or v["dst"] in seen}
        return stale
print("T3 stale ('需複核') items per single node edit; 30 graphs x 200 edits each")
for n in (20,40,80):
    res={r:[] for r in ("R1","R2","R3")}; tot=[]
    for _ in range(30):
        g,L=gen(n)
        for _ in range(200):
            x=random.choice([k for k in g["nodes"] if k!="n0"])
            for r in res: res[r].append(len(propagate(g,x,r)))
        tot.append(items_total(g))
    T=st.mean(tot)
    line=f"  n={n:3d} items~{T:5.1f} | "
    for r in res:
        v=sorted(res[r]); line+=f"{r}: mean {st.mean(v):5.1f} ({100*st.mean(v)/T:4.1f}%) p90 {v[int(.9*len(v))]:3d} max {v[-1]:3d} | "
    print(line)

# ---------- T4: end-condition placement ----------
print("T4 end-condition fields needed: stored on link vs on node (random flow graphs)")
for n in (20,40,80):
    L_,N_,D_=[],[],[]
    for _ in range(200):
        g,_l=gen(n)
        fl=[v for v in g["edges"].values() if v["family"]=="流程"]
        src={}
        for v in fl: src[v["src"]]=src.get(v["src"],0)+1
        L_.append(len(fl)); N_.append(len(src)); D_.append(sum(1 for c in src.values() if c>1))
    print(f"  n={n:3d} link-model fields {st.mean(L_):5.1f} | node-model fields {st.mean(N_):5.1f} | nodes whose several out-links must carry identical end text {st.mean(D_):4.1f}")

# ---------- T5: serialization ----------
g,L=gen(30,nflow=30,ninf=6)
pretty=json.dumps({"nodes":[dict(id=k,**v) for k,v in g["nodes"].items()],"edges":[dict(id=k,**v) for k,v in g["edges"].items()]},ensure_ascii=False,indent=2)
compact=json.dumps(g,ensure_ascii=False,separators=(",",":"))
jsonl="\n".join(json.dumps({"id":k,**v},ensure_ascii=False,separators=(",",":")) for k,v in list(g["nodes"].items())+list(g["edges"].items()))
dsl=[]
for k,v in g["nodes"].items(): dsl.append("|".join(map(lambda s:"" if s is None else str(s),[k,"節點",v["kind"],v["name"],v["role"],v["parent"],v["origin"],v["confirm"],v["quote"]])))
for k,v in g["edges"].items(): dsl.append("|".join(map(lambda s:"" if s is None else str(s),[k,"連線",v["family"],v["src"]+">"+v["dst"],v["intro"],v["open"],v["end"],v["origin"],v["confirm"]])))
dsl="\n".join(dsl)
mer=["flowchart TD"]+[f'{v["parent"]} --> {k}' for k,v in g["nodes"].items() if v["parent"]]+[f'{v["src"]} -->|{v["intro"]}| {v["dst"]}' for v in g["edges"].values()]
mer="\n".join(mer)
def edit_lines(text,fmt):
    t=text
    old=g["nodes"]["n5"]["role"]
    new="改過的作用"
    t2=t.replace(old,new,1)
    d=[l for l in difflib.unified_diff(t.splitlines(),t2.splitlines(),lineterm="",n=0) if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++","---"))]
    return len(d)
print("T5 serialization of a 30-node / 36-edge graph (UTF-8 bytes, chars, changed lines when one node's text is edited)")
for name,txt in (("pretty JSON (arrays)",pretty),("compact JSON (1 line)",compact),("JSON Lines",jsonl),("pipe-line text",dsl),("Mermaid (lossy: no origin/confirm/conditions)",mer)):
    print(f"  {name:46s} bytes {len(txt.encode()):6d} chars {len(txt):6d} changed-lines {edit_lines(txt,name)}")
```

---

## 附錄 I　自我應用腳本與原文

附錄 F 的來源。先把下方「原文」存成 `first_msg.txt`，再執行腳本（檔名需一致，並放在同一資料夾）。

**原文**（使用者的第一則訊息）

```text
我想要針對藍圖，主軸等內容
有一個ui介面
可以展示目前的核心，主軸，骨架
彼此關係（關係連結顯示：介紹，開啟，結束條件）
各節點顯示：名稱，功能

用樹狀，關係圖等等方式展示
參考遊戲，或是公司報告ppt等呈現方式
這是要給人類看的，內容要簡潔，好理解 ，敘述都簡述，不要過於複雜，而且語言要淺顯易懂的人類語言，減少專業用語，盡量講述作用

然後這個ui還要有一個功能

就是開啟新對話後，第一次對話結束
要根據用戶所說內容
建構一個這個互動介面
展示核心，骨架，架構，及關係圖

這個主要是用來展示，ai理解的部分
將其做成關係圖
讓人類確認ai理解沒有錯誤

有的話可以直接修改，更改關係圖連線，啟動結束條件，關係，數據
新增刪除節點，新增連結，新增因果連線等方式，去修改內容
然後有一個輸出按鍵

這個按鍵，可以分析改動了那些內容
然後先輸出整體框架內容，再指出更改部分

這樣可以更精確的進行討論
有一個GitHub 工具
是用來生成軟體的
有各類按鍵，視窗，互動介面等等內容
用拖拉，新增，連結的方式
就能組建一個新的軟體
可以參考這個設計原理
進行完善內容
```

**腳本**

```python
import re, unicodedata
raw=open("first_msg.txt",encoding="utf-8").read()
def norm(s):
    s=unicodedata.normalize("NFKC",s)
    return re.sub(r"[\s，,。．、；;：:！!？?（）()\[\]「」\"'“”]","",s).lower()
nraw=norm(raw)

# ---- round-1 draft built by hand from the first message only (rules A-G) ----
nodes=[ # id, kind, name, role, origin, quote
 ("n0","核心","確認AI理解","讓人類確認AI的理解沒有錯誤","使用者原話","讓人類確認ai理解沒有錯誤"),
 ("n1","主軸","展示","展示目前的核心、主軸、骨架與彼此關係","使用者原話","可以展示目前的核心，主軸，骨架"),
 ("n2","主軸","自動建圖","第一次對話結束後，依使用者所說內容建出介面","使用者原話","要根據用戶所說內容"),
 ("n3","主軸","編輯","讓人直接修改圖與內容","使用者原話","有的話可以直接修改"),
 ("n4","主軸","輸出","分析改了什麼；先輸出整體框架，再指出更改處","使用者原話","先輸出整體框架內容，再指出更改部分"),
 ("n5","骨架","節點顯示","每個節點顯示名稱與功能","使用者原話","各節點顯示：名稱，功能"),
 ("n6","骨架","呈現方式","用樹狀、關係圖展示，參考遊戲或公司報告","使用者原話","用樹狀，關係圖等等方式展示"),
 ("n7","骨架","淺白語言","簡短、好懂、少專業用語、講作用","使用者原話","語言要淺顯易懂的人類語言，減少專業用語，盡量講述作用"),
 ("n8","骨架","拖拉建構工具原理","參考以拖拉、新增、連結組建軟體的工具","使用者原話","用拖拉，新增，連結的方式"),
]
edges=[ # id, family, src, dst, intro, open, origin, quote
 ("l1","流程","n2","n1","建圖後交給展示","第一次對話結束","使用者原話","第一次對話結束"),
 ("l2","流程","n1","n3","看完圖，有錯就改","有錯誤時","使用者原話","有的話可以直接修改"),
 ("l3","流程","n3","n4","改完後輸出","（未說）","AI推測",None),
 ("l4","影響","n8","n3","工具原理影響編輯方式","—","AI推測","可以參考這個設計原理"),
]
blanks=["「GitHub 工具」是哪一個？（只說有這種工具，沒給名稱）",
        "「整體框架內容」要包含哪些欄位？",
        "編輯何時算做完？（n3 的完成條件）",
        "建圖何時算做完？（n2 的完成條件）"]

print("== Rule G: quote must appear verbatim in user's text ==")
ex_ok=ex_norm=bad=0
for it in nodes+edges:
    q=it[-1]
    if q is None: continue
    if q in raw: ex_ok+=1
    elif norm(q) in nraw: ex_norm+=1; print("  only passes after normalisation:",it[0],q)
    else: bad+=1; print("  NOT FOUND:",it[0],q)
print(f"  exact={ex_ok}  normalised-only={ex_norm}  missing={bad}")
# demonstrate the whitespace trap: user wrote '好理解 ，敘述' (space before comma)
q1="簡潔，好理解，敘述都簡述"
print("  trap test:", repr(q1), "exact:", q1 in raw, "| normalised:", norm(q1) in nraw)
# demonstrate paraphrase is rejected
q2="讓使用者檢查AI有沒有理解錯"
print("  paraphrase test:", repr(q2), "exact:", q2 in raw, "| normalised:", norm(q2) in nraw)

print("\n== Draft statistics ==")
items=nodes+edges
src=lambda it: it[4] if len(it)==6 else it[6]
said=sum(1 for it in items if src(it)=="使用者原話"); guess=len(items)-said
print(f"  items {len(items)} (nodes {len(nodes)}, links {len(edges)}): 你說的 {said}, AI猜的 {guess}, blanks {len(blanks)}")

print("\n== Rule D cue words: contexts in the first message ==")
cues=["然後","之後","後","先","再","直到","當","因為","導致","所以","包含","如果","有的話"]
for c in cues:
    for m in re.finditer(c,raw):
        a=max(0,m.start()-7); b=min(len(raw),m.end()+9)
        print(f"  [{c}] …{raw[a:b].replace(chr(10),'／')}…")

print("\n== Enumerations (>=3 comma items on one line) ==")
tot=0;n=0
for line in raw.splitlines():
    parts=[p for p in re.split(r"[，,、]",line) if p.strip()]
    if len(parts)>=3 and len(line)<60:
        n+=1; tot+=len(parts); print(f"  {len(parts)} items: {line}")
print(f"  {n} enumeration lines -> {tot} items; if each became a node the draft would gain {tot} nodes (draft now has {len(nodes)})")
```

---

## 參考資料

[1] Park, Yoon, Lim. *Transfiver: Human–AI Co-Inference through a Shared Editable State.* arXiv:2609.03797, 2026-09.（預印本）
[2] graphspec（把流程拓撲存成可版本化的檔案；以形狀區分節點種類，條件線畫成虛線並標出何時成立）. pypi.org/project/graphspec
[3] DAG Visual Editor Design（設計指引，彙整 n8n、ComfyUI、React Flow 等的經驗）. openskillindex.com
[4] React Flow 使用指引（@xyflow/react）. skills.cat
[5] node_program_editor（Flutter 節點編輯器，含邏輯與設計分開匯出）. pub.dev
[6] emviz（圖形差異：新增綠、刪除紅虛線、修改琥珀）. github.com/craftell/em
[7] Choudhury 等. *Networked Intelligence: Active Shared Context Graphs for Human-AI Team Science.* arXiv:2607.13220.（預印本）
[8] RAFT: A Stateful Retrieval-Augmented Framework for Troubleshooting Agents. arXiv:2609.20754.（預印本）
[9] Difference Map Readability for Dynamic Graphs. Monash University 研究出版。
[10] WorkBraid: Visual Architecture Diffs for Agent-Proposed Code Changes. dev.to（社群文章）
[11] Agora（以 Git 不可變提交圖作為多代理共享記憶）. arXiv:2609.18094.（預印本）
[12] Falleri 等. *Fine-grained and Accurate Source Code Differencing*（GumTree）. ASE 2014. labri.fr
[13] RFC 6902（JSON Patch）與 RFC 7396（JSON Merge Patch）；兩者差異經套件與說明文件確認（jsonlint.com、packagist 之 bumpcore/json-patch）。
[14] *Zep: A Temporal Knowledge Graph Architecture for Agent Memory.* arXiv:2501.13956；Graphiti 專案說明。
[15] Harel. *Statecharts: A Visual Formalism for Complex Systems.* Sci. Comput. Program. 8, 1987.（經課程講義確認條件與進出動作的分工，未讀原文）
[16] Doyle. *A Truth Maintenance System.* Artificial Intelligence 12, 1979.（經課程講義確認撤回與傳遞機制，未讀原文）
[17] 自動化偏誤與審閱疲勞：thinktech.ngo 風險庫、tianpan.co、dev.to（LoopRails）等實務文章。（二手，含轉述的醫療影像研究，未查原文）
[18] *An Investigation of LLMs' Inefficacy in Understanding Converse Relations*（ConvRe）. arXiv:2310.05163.
[19] Ilves, Barbu, Übi. *Large Language Models for Knowledge Graph Extraction: A Schema-Constrained Evaluation Framework.* KaLLM @ LREC 2026. aclanthology.org/2026.kallm-1.21
[20] Sansford 等. *GraphEval: A Knowledge-Graph Based LLM Hallucination Evaluation Framework.* arXiv:2407.10793.（輸出拆成三元組，逐條對回來源檢驗）
[21] 版面演算法：Heer, CS448B 講義；UW CSE442／CSE512 講義；*Why we live in hierarchies*, arXiv:1707.01744（Sugiyama 適用於小型網路）。

註：另有一篇 2026 年人機互動範疇回顧與 grapken-core 專案，出自他人整理的研究稿，本文**未能獨立查證**，故未列入引用。

---

## 索引

| 詞條 | 章節 |
|---|---|
| 三方比對 | 3.3、8.4 |
| 三族連線 | 5.2 |
| 位置不算改動 | 8.3 |
| 例子（情境驗證） | 5.2、7.5、11 |
| 兩種視圖 | 6.1 |
| 分層展示 | 6.2 |
| 來源（與確認分欄） | 5.1、7.2、修訂紀錄 |
| 單一正式資料 | 4.1、13 |
| 原句 | 5.1、7.2 |
| 基準版 | 8.3、9.2 |
| 失敗模式 | 7.5、10.2 |
| 差異（五類） | 8.3、9.1 |
| 開啟條件／結束條件 | 5.2、8.1 |
| 影響範圍 | 8.3 |
| 手動模式 | 4.4 |
| 手機操作 | 6.3、11 |
| 增量更新 | 7.6 |
| 對話主軸／對話閘門 | 4.5 |
| 改掛上層 | 8.3、8.2 |
| 拆分與合併 | 5.4、8.2、8.3 |
| 植入錯誤實驗 | 10.2 |
| 橡皮圖章（走過場） | 7.4、10.3 |
| 確認（動作） | 4.3、5.1、8.3 |
| 空白清單 | 5.3、7.3 |
| 編號 | 5.1、8.3 |
| 譜系 | 5.4、8.3、附錄 C |
| 資料格式（JSON） | 9.4、附錄 C |
| 通過門檻 | 10.5 |
| 鎖定範圍 | 4.3、9.3 |
| 需複核 | 5.1、4.5、8.1、11 |
| 首輪準確率 | 10.3 |
| 圖資料庫 | 3.4 |
| 人話提醒（即時檢查） | 8.1 |
| 模擬優先 | 10.4 |
| Transfiver | 3.2、11 |
| JSON Patch／小修改 | 3.2、3.6、8.2、8.3 |
| 一步傳遞 | 3.6、5.1、附錄 E |
| 行式文字（儲存形式） | 5.5、附錄 E |
| 版面演算法 | 6.5 |
| 完成條件 | 5.1、5.2、8.1 |
| 原句逐字比對 | 7.2 |
| 穩定編號 | 5.1、8.3、附錄 E |
| 選型矩陣、最優解（定義） | 附錄 D |
| 模擬結果 | 10.4、附錄 E |
| 自我應用、來源盤點 | 附錄 F |
| 口語連接詞 | 7.2、7.5、附錄 F-3 |
| 列舉收合 | 7.2、7.5、附錄 F-4 |
| 正規化（原句比對） | 7.2、附錄 F-2 |
| 設計來源占比 | 10.3、附錄 F-6 |
| 修訂歷程 | 附錄 G |
| 重現用腳本 | 附錄 H、I |
| 先寫後看 | 10.2 |
| 覆寫率 | 10.3 |
| 鏈式確認 | 4.5、10.1 |
| 真值維護系統 | 3.6、5.1 |
