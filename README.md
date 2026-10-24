# forAVAr｜主系統入口

forAVAr 是以「受目標與證據約束的可靠認知與自我修正」為核心的主系統。正式架構與狀態以本庫的權威文件為準；封包、交接說明、研究紀錄與測試報告都不能自行取代正式基線。

## 權威入口

- 主系統索引：docs/index.json
- 核心藍圖：docs/blueprint.json
- 運作契約與變更規則：docs/operating_contract.json
- 能力登錄表：docs/capability_registry.json
- 問題登錄表：docs/problem_register.json
- Runtime：runtime/foravar_vertical_slice.py、runtime/policy_gate.py

目前正式藍圖基線為 v0.8（2026-10-24）。目前 Runtime 狀態為 POLICY_GATE_INTEGRATED_RUNTIME_NOT_VALIDATED；不得將政策閘門已整合描述成整體 Runtime 已驗收。

## 進度、壓縮檔與交接檔審核

從 [進度資料夾入口](進度/README.md) 開始。後續新增的 ZIP 壓縮檔與 HANDOFF 交接檔，均先視為「待審核輸入」，不是已採納的程式版本，也不會因為檔案較新就自動成為正式基線。

審核者必須依照 [審核標準與接手流程](進度/審核標準與接手流程.md) 執行，將審核結論、缺陷、核心／主軸偏移檢查、證據與未完成項目記錄在進度資料夾。若 ZIP 無法實際解包、比較或測試，必須明確標示審核範圍與 NOT_EXECUTED／NOT_VERIFIED，不得宣稱完成程式碼級審核。

每次交接至少核對：基線 commit、封包完整 SHA-256、變更檔案清單、實際執行的測試與結果、未執行項目、待裁決決策、回復方式與下一步。新版本請使用可區分的檔名或版本號，避免覆寫封包後無法重現先前審核。

進度資料夾是目前指定的交接輸入與審核入口；其中 ZIP 和交接檔不具有正式架構權威。研究、原始實驗、暫存輸出及需長期保存的驗證材料，依專案資料治理規則歸檔至 upqq21477-star/forAVArb。P1 與 P2 僅供讀取，不得新增、修改或刪除。

## 歷史與歸檔

研究、歷史版本、候選方案及舊來源文件位於 forAVArb。請先由 [歸檔 manifest](https://github.com/upqq21477-star/forAVArb/blob/main/歸檔/forAVAr_main_退場歸檔_2026-10-24/manifest.json) 查找原始路徑；歸檔內容不是現行權威，正式決策仍以本庫的權威文件為準。
