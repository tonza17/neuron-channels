# Results Summary: Patched-Generator 60-Morph Re-Sweep + t0090 Correction Overlay

## Summary

The t0092 soma-pt3d fix is fully validated at scale: **60 / 60 cells STABLE-firing** post-fix (51
NAN_VOLTAGE→firing, 9 STABLE-silent→firing, 0 regressions). Pass criterion (≥50/60 with
non-zero PD-rate) met at **56/60**; stretch (≥55/60) also exceeded. Mean DSI different=0.323,
similar=0.352. The `replace` correction overlay against t0090's
`procedural_dsgc_morphology_generator` library asset is in place and `verify_corrections.py` PASSES;
supersession check confirms the redirect to t0092's `procedural_dsgc_morphology_generator_fix`.

## Metrics

* **Total cells re-swept**: **60** (30 different + 30 similar).
* **Post-fix stability**: **60 / 60 STABLE** (vs t0090 pre-fix: 9 / 60).
* **Cells firing post-fix (any direction)**: **60 / 60** (vs 0 / 60 pre-fix).
* **Cells with PD-rate > 0 Hz**: **56 / 60** — pass criterion ≥50 met; stretch ≥55 also met.
* **Cells with DSI > 0.5**: **21 / 60**.
* **Total spikes across re-sweep**: **16,107** (different=5,608, similar=10,499) vs 0 pre-fix.
* **Mean direction_selectivity_index, different_set_post_fix**: **0.432** (over the 30 STABLE cells
  in `metrics.json`).
* **Mean direction_selectivity_index, similar_set_post_fix**: **0.365**.
* **Pre→post transitions**: nan_to_stable_firing=**51**, stable_silent_to_stable_firing=**9**,
  regressions=**0**.
* **Re-sweep wall-clock**: ~50 min on local 64-core EPYC, 16 workers.
* **Cost**: **$0**.

## Verification

* `verify_research_code.py` — PASSED (0/0)
* `verify_plan.py` — PASSED (0/0)
* `verify_corrections.py t0093_resweep_and_t0090_correction` — **PASSED (0/0)**
* Library supersession check — verified
* `verify_task_metrics.py` — PASSED
* `ruff check . && ruff format .` clean
* `mypy -p tasks.t0093_resweep_and_t0090_correction.code` clean
* `verify_task_results.py`, `verify_logs.py`, `verify_task_folder.py`, `verify_suggestions.py` —
  to be run during the reporting step
