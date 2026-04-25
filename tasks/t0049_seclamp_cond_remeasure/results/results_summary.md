# Results Summary: SEClamp Conductance Re-Measurement

## Summary

Measuring per-channel conductance under a somatic SEClamp at -65 mV on the deposited DSGC (gNMDA =
0.5 nS, exptype = control) yields values that lie **between** paper Fig 3A-E targets and t0047's
per-synapse-direct measurements — but match **neither** within tolerance. Verdict: **H2
(intermediate)** for all 6 channel × direction cells. SEClamp is closer to paper than
per-synapse-direct (5-10x reduction from t0047) but still 1.7-5x over paper. **Critically: GABA
PD/ND symmetry under SEClamp** (PD = 47.47 nS, ND = 48.04 nS, DSI = -0.006) **contradicts the
paper's stated PD ~12.5 / ND ~30 nS** (DSI ≈ -0.41). Modality alone does not reconcile the
deposited code with paper Fig 3A-E.

## Metrics

* **NMDA SEClamp at gNMDA = 0.5 nS**: PD **13.89 +/- 0.38 nS**, ND **13.71 +/- 0.19 nS**. Paper: PD
  ~7.0, ND ~5.0. Delta: PD +98%, ND +174%. PD/ND ratio = **1.01** (paper expects ~1.4 with PD bias).
* **AMPA SEClamp at gNMDA = 0.5 nS**: PD **5.93 +/- 0.27 nS**, ND **5.79 +/- 0.19 nS**. Paper: PD
  ~3.5, ND ~3.5. Delta: PD +69%, ND +65%. PD/ND ratio = **1.02** (paper expects ~1.0, qualitative
  match for AMPA-no-DSI claim).
* **GABA SEClamp at gNMDA = 0.5 nS**: PD **47.47 +/- 1.98 nS**, ND **48.04 +/- 1.76 nS**. Paper: PD
  ~12.5, ND ~30.0. Delta: PD +280%, ND +60%. PD/ND ratio = **0.99** vs paper's **0.42** — GABA
  ND-bias completely vanishes under SEClamp. Major discrepancy.
* **Modality reduction (t0047 per-syn-summed → SEClamp)**: NMDA 5.0x reduction, AMPA 1.8x
  reduction, GABA 2.2x reduction (PD) / 4.5x reduction (ND, but ratios collapse).
* **Voltage clamp quality**: soma voltage SD = 1-3e-4 mV across all 32 trials — well below the 0.5
  mV tolerance. The 0.001 MOhm series resistance behaves as a pure voltage source.
* **6/6 H2 verdicts**: every channel × direction cell sits strictly between paper and t0047
  per-synapse-direct, but matches neither within +/- 25%.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors) on the 6-variant `metrics.json`
* `verify_plan.py` — PASSED (0 errors)
* `verify_research_code.py` — PASSED (0 errors)
* `verify_task_folder.py` — PASSED (0 errors)
* `ruff check`, `ruff format`, `mypy -p tasks.t0049_seclamp_cond_remeasure.code` — clean
* Validation gate (2-trial smoke test asserting clamp holds at +/-0.5 mV and conductances in
  [0.5, 200] nS): PASSED before launching the full 32-trial sweep
* SEClamp-current sign convention bug caught and fixed during implementation
  (`g[nS] = abs(i[pA]) / abs(V[mV] - E_rev[mV])`, no extra unit conversion); re-verified against the
  validation gate's plausibility band
