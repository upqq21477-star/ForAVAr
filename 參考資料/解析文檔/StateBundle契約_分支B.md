# State Bundle 最小資料契約分支｜B

- 文件 ID：FORAVAR-STATE-BUNDLE-CONTRACT-BR-002
- 類型：BRANCH
- 狀態：CURRENT／候選契約；NOT_APPROVED／NOT_IMPLEMENTED
- 唯一責任：保存原 v0.1 契約的原章節 3、4；完整欄位、狀態、例外、反例和驗收條件以原文為準。
- 主題回鏈：[State Bundle 主軸彙整](../StateBundle_主軸彙整.md)
- 舊入口相容頁：[原契約路徑](./可攜式StateBundle最小資料契約與防漂移反例驗收草案_v0.1.md)
- 變更追溯：[變更追溯總表](../變更追溯總表.md)

## 目錄與索引

- [3. 最小可攜式資料結構](#section-1)
- [4. 生成規則：由既有權威來源派生，禁止雙重真相](#section-2)

---

<a id="section-1"></a>
## 3. 最小可攜式資料結構

以下是候選 JSON 形狀，用於討論欄位責任；**它不是已核准或已登錄的 JSON Schema，也不得直接當成 Runtime 接口。**

```json
{
  "bundle_schema_version": "0.1",
  "bundle_id": "STATE-BUNDLE-<stable-id>",
  "generated_at": "<ISO-8601>",
  "mode": "REPOSITORY_UNAVAILABLE",
  "source_snapshot": {
    "repository": "<owner/repository-or-unknown>",
    "branch": "<branch-or-unknown>",
    "commit_sha": "<sha-or-unknown>",
    "archive_sha256": "<sha256-or-unknown>",
    "manifest_ref": "<path-or-embedded-manifest>",
    "manifest_digest": "<sha256>",
    "integrity_status": "PASS | FAIL | UNKNOWN",
    "captured_at": "<ISO-8601>"
  },
  "load_status": {
    "status": "READY | BLOCKED_CONTEXT | STALE_CONTEXT | CONFLICT",
    "required_sources_present": true,
    "source_conflicts": [],
    "missing_sources": [],
    "reason": ""
  },
  "core_anchor": {
    "objective": {
      "text": "<brief, non-authoritative rendering>",
      "source_refs": []
    },
    "core_invariants": [],
    "non_goals": [],
    "success_conditions": [],
    "stop_conditions": [],
    "authority_refs": []
  },
  "current_state": {
    "current_authority_ref": "",
    "current_fingerprint": "",
    "active_work_ref": "",
    "active_work_fingerprint": "",
    "active_batch_ref": "",
    "active_batch_fingerprint": "",
    "construction_ref": "",
    "construction_fingerprint": "",
    "phase": "UNKNOWN",
    "status": "UNKNOWN",
    "next_action": "",
    "completed": [],
    "incomplete": [],
    "blockers": [],
    "evidence_refs": [],
    "open_conflicts": []
  },
  "task_contract": {
    "task_id": "",
    "objective": "",
    "problem_ids": [],
    "in_scope": [],
    "out_of_scope": [],
    "allowed_write_paths": [],
    "read_only_paths": [],
    "required_inputs": [],
    "acceptance_conditions": [],
    "stop_conditions": [],
    "authorization_ref": ""
  },
  "change_ledger": [],
  "handoff": {
    "next_action": "",
    "required_read_order": [],
    "prohibited_actions": [],
    "unresolved_questions": []
  }
}
```

Schema 需要進一步定義各狀態的條件、欄位是否必填、指紋算法、參照路徑規則、敏感資料排除、版本相容性以及衝突時的確定性排序。以上範例中的 placeholder 並不是可直接執行的實例。

<a id="section-2"></a>
## 4. 生成規則：由既有權威來源派生，禁止雙重真相

建議來源順序（需按實際專案裁定，不允許 State Bundle 自行凌駕來源）：

1. **Current／執行狀態權威：** 指明當前階段、Active Work 和狀態來源。
2. **唯一目標藍圖：** 讀取與本任務相關的核心原則、架構契約及要求。
3. **Active Work／Construction：** 讀取本輪下一步、範圍、前置條件和接受條件。
4. **凍結 Feature Batch／範圍指紋：** 確認不得無聲擴張或重設的工作範圍。
5. **具體實作、測試、證據及開放問題：** 只納入本工作需要的引用；每一項結論保留來源版本和證據層級。
6. **HANDOFF／README／文件索引：** 作導航、歷史和恢復輔助；若與權威狀態衝突，不得因它文字較完整就升格為權威。

生成器不應把整份 repository 的全文放進 Bundle，而要列明被納入／排除的來源與理由。若是手工製作的離線 Bundle，必須標記 `generation_method=MANUAL`，不能偽裝成自動由 Current 產生。
