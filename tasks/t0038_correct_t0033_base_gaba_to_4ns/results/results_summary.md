---
spec_version: "2"
task_id: "t0038_correct_t0033_base_gaba_to_4ns"
date_completed: "2026-04-24"
status: "complete"
---
# Results Summary: Correct t0033 Base GABA to 4 nS on t0022 Variant

## Summary

Wrote correction `C-0038-01` against t0033's answer asset
`vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation` encoding the t0037 finding that the
operational base parameter on t0022 is `GABA_CONDUCTANCE_NULL_NS = 4.0 nS`, not the original 12 nS
default. Closes suggestion **S-0037-02**. Verificator PASSED. No sweep, no code, no new assets.
Total cost $0.00, wall time under 10 minutes.

## Metrics

* **Correction files produced**: **1** (`answer_vastai-*.json`).
* **Correction ID**: `C-0038-01`.
* **Target kind / action**: `answer` / `update`.
* **Effective `short_title` overlay**: now ends
  `"(t0022 base GABA_CONDUCTANCE_NULL_NS = 4.0 nS per t0037)"`.
* **Evidence chain cited in rationale**: t0030 (12 nS → DSI pinned at 1.000), t0036 (6 nS →
  still pinned), t0037 (4 nS → DSI=0.429, preferred 40.8°).

## Verification

* `verify_corrections.py t0038_correct_t0033_base_gaba_to_4ns` — **PASSED**, 0 errors, 0 warnings.
* `verify_task_dependencies.py` — PASSED.
* `verify_task_file.py` — PASSED (1 warning: empty `expected_assets`, expected for correction
  tasks).
* `verify_logs.py` — PASSED.
* `verify_task_folder.py` — target 0 errors.
