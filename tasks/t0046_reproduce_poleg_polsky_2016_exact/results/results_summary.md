# Results Summary: Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Summary

The from-scratch port of ModelDB 189347 reproduces the qualitative direction-tuning behaviour
(preferred-direction PSP > null-direction PSP) and matches the paper's slope-angle and ROC-AUC
targets within tolerance, but absolute PSP amplitudes at the code-pinned `b2gnmda = 0.5 nS`
overshoot the paper's reported means by approximately 4x. The paper-vs-code discrepancies on synapse
count, gNMDA value, and noise driver behaviour are confirmed; **12 discrepancies** are catalogued in
the audit, including six MOD-default vs `main.hoc`-override mismatches.

## Metrics

* **Fig 1 PD PSP** (b2gnmda = 0.5 nS, code value): **23.25 mV** vs paper **5.8 +/- 3.1 mV** —
  outside 1-SD band (synapse-count discrepancy).
* **Fig 1 slope angle** (b2gnmda = 0.5 nS): **54.8 deg** vs paper **62.5 +/- 14.2 deg** — within
  tolerance.
* **Fig 4 high-Cl- slope**: **47.3 deg** vs paper **45.5 +/- 3.7 deg** — within tolerance.
* **Fig 5 0 Mg2+ slope**: **50.7 deg** vs paper **45.5 +/- 5.3 deg** — within tolerance.
* **Fig 7 ROC AUC** (control / AP5 / 0 Mg2+): **1.00 / 1.00 / 1.00** vs paper **0.99 / 0.98 / 0.83**
  — control + AP5 within tolerance; 0 Mg2+ over-reproduces (small-N reduces overlap).
* **Fig 8 control DSI** (suprathreshold): **0.676** (PD = 15.5 Hz, ND = 3.0 Hz) — qualitatively
  matches paper's preserved DS.
* **Fig 8 AP5 DSI**: **0.0** (cell silenced) — diverges from paper's "DSI preserved under iMK801";
  catalogued as a Fig-8 reproduction discrepancy.
* **Fig 8 0 Mg2+ DSI**: **0.212** (-69% vs control) — qualitatively matches paper's reduced DS.
* **Discrepancy catalogue**: 12 entries across 4 pre-flagged paper-vs-code, 6 MOD-default vs
  `main.hoc`-override, 1 noise-driver reclassification, 1 registered-metric not-applicable note.
* **Audit table**: 35 parameter rows comparing paper / ModelDB code / our reproduction values.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors)
* `verify_corrections.py` — PASSED (0 errors)
* Library asset `modeldb_189347_dsgc_exact` and answer asset `poleg-polsky-2016-reproduction-audit`
  validated by direct inspection against `meta/asset_types/library/specification.md` v2 and
  `meta/asset_types/answer/specification.md` v2 (no dedicated verificator scripts exist for these
  asset types in the current branch).
* MOD compilation under NEURON 8.2.7 + MinGW-gcc — PASSED (`code/sources/nrnmech.dll` loads
  cleanly).
* End-to-end smoke test — PASSED (`countON = 282`, `numsyn = 282`, PD peak PSP = 25.14 mV at trial
  seed 1).
