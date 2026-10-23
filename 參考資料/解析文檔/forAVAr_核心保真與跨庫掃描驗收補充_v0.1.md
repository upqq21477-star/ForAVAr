# 核心保真與跨庫掃描驗收補充 v0.1

- DOC_ID：FORAVAR-CORE-PRESERVATION-CROSSREPO-EVAL-001
- 狀態：TEST_SPEC_ONLY；測試規格不代表執行完成
- 唯一責任：補充核心保真、跨庫流程漏收和權限邊界驗收；一般運行模式由[矩陣 v0.3](./forAVAr_運行效率與架構候選驗收矩陣_v0.3.md)負責。
- 主藍圖：[核心重建施工藍圖 v0.6](./forAVAr_核心重建施工藍圖_v0.6_2026-10-23.md)
- 規劃依據：[forAVArb 更新規劃 v0.2](https://github.com/upqq21477-star/forAVArb/blob/main/%E8%92%B8%E9%A4%BE/%E6%95%B4%E9%AB%94%E6%A1%86%E6%9E%B6%E8%A9%95%E5%AF%A9/2026-10-23_%E6%95%B4%E9%AB%94%E6%A0%B8%E5%BF%83%E4%BF%9D%E7%9C%9F%E8%88%87%E6%AD%A3%E5%BC%8F%E8%97%8D%E5%9C%96%E6%9B%B4%E6%96%B0%E8%A6%8F%E5%8A%83_v0.2.md)。

## 測試契約

| ID | 情境 | 接受條件 | 初始狀態 |
|---|---|---|---|
| T-CORE-01 | 核心不變量 | 思考為唯一核心；Core→A1–A6→N01–N18→F0–F7 保持 | 待靜態讀回 |
| T-CORE-02 | 流程責任 | 一般任務循環、F0–F7 與四梯次各有唯一責任，無平行總控 | 待靜態讀回 |
| T-C07-01 | 觸發條件 | 只有架構／跨庫稽核、流程漏收、來源不一致、共享契約／責任衝突或基線過期時全域掃描 | 待驗 |
| T-C07-02 | 方法先於路徑列舉 | 遞迴列舉前先讀來源庫既有掃描計畫／Roadmap；沿用可用方法 | 待驗 |
| T-C07-03 | 舊分母漂移 | 刷新 commit/tree/blob 數；數量差額不直接視為遺失 | 待驗 |
| T-C07-04 | 證據分層 | 分開 path tree、content review、test/runtime；未讀不等於不存在或通過 | 待驗 |
| T-C02-01 | 去除重複 SOP | 不新增獨立 C-02；按需沿用來源 A0–A9 方法 | 待驗 |
| T-C01-01 | 文件與能力退場分離 | 一般文件退場不強制能力負載測試；能力／方法／路由退役才觸發 | 尚無真實案例 |
| T-C01-02 | 能力退場回復／等價 | 真實能力退役測正負／邊界／恢復、load-bearing 依賴、等價與 rollback | NOT_RUN |
| T-4STAGE-01 | 四梯次與 Phase 0–7 | Phase 0–7 僅在 PLANNING；其餘四梯次不重複 | 待靜態讀回 |
| T-4STAGE-02 | 批次放行 | 必要項未達 Gate 整批不進階；安全／權限 Gate 橫跨四梯次 | 待靜態讀回 |
| T-PERM-01 | P1／P2 唯讀 | write-capable metadata 不授權寫入；平台權限變更需另授權 | 規則核對；平台隔離未驗 |
| T-TRACE-01 | 追溯與連結 | 核心、四梯次、SOP、索引及追溯事件互相可定位 | 待讀回 |

## 證據結果分級

- `PASS_STATIC`：限於實際讀回、內容、相對連結與修改範圍檢查。
- `PASS_RETROSPECTIVE`：限已知答案的回溯重演，不是盲測。
- `PASS_RUNTIME`：必須有實際執行證據、版本與觀測結果。
- `PARTIAL／INCONCLUSIVE／BLOCKED／NOT_RUN`：列明剩餘項與原因，禁止把未知轉為 PASS。

這是測試規格；跨任務觸發、盲測、全量內容掃描、能力退場、平台權限隔離與 Runtime 尚未驗證。
