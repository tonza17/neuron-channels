# Results Summary: Test t0024 de Rosenroll DSGC under EPSP/IPSP/FULL protocol

## Summary

The de Rosenroll 2026 DSGC was driven through the EPSP_PASSIVE / IPSP_PASSIVE / FULL trial-mode
protocol — 120 trials (3 modes × 2 directions × 20 seeds) — decomposing the somatic Vm into
pure-excitatory and pure-inhibitory components. Headline finding: **the model's IPSP_PASSIVE trace
is flat at -60 mV in both PD and ND**, exactly as in t0065's deposited Poleg-Polsky cell. Two
structurally independent DSGC implementations therefore converge on the same design pattern
(`e_GABA = v_rest = -60 mV` → pure shunting inhibition); the t0065 finding is **not** a
Poleg-Polsky idiosyncrasy.

## Metrics

* **direction_selectivity_index (FULL trial-mean spike-count)**: **0.7391** — matches t0024's
  reference DSI = 0.776 (12-angle correlated) within sampling noise.
* **FULL PD spike count (mean ± SD across 20 trials)**: **5.00 ± 0.65 spikes/trial**, peak Vm
  **+37.29 ± 0.45 mV**.
* **FULL ND spike count**: **0.75 ± 0.55 spikes/trial**, peak Vm +10.02 ± 41.00 mV (high variance
  because most ND trials have no spike — peak Vm reflects subthreshold envelope).
* **EPSP_PASSIVE peak − baseline (mean ± SD)**: PD = **+24.36 ± 1.98 mV**, ND = **+25.97 ± 4.11
  mV**. Direction-coupled but only ~1.6 mV difference, driven by bar geometry (bar arrival time
  differs across directions even with GABA off).
* **IPSP_PASSIVE peak − baseline**: PD = **+0.16 ± 0.02 mV**, ND = **+0.30 ± 0.01 mV** — both
  at the noise floor. Cross-model match with t0065 (which also showed +0.10 / +0.11 mV).
* **Trials run**: 120 (20 trials × 3 modes × 2 directions).
* **Wall-clock**: **~60 min** for the 120-trial sweep on the local Windows workstation.

## Verification

* `verify_research_code.py` — PASSED (0 errors, 0 warnings) on `research/research_code.md`.
* `verify_plan.py` — PASSED (0 errors, 0 warnings) on `plan/plan.md`.
* `verify_task_dependencies.py` — PASSED at check-deps step (t0024 and t0065 both completed).
* `verify_task_metrics.py` — PASSED (registered DSI metric only).
* `verify_task_results.py` — PASSED (mandatory sections present in this file and
  `results_detailed.md`).
* Mypy, ruff check, ruff format — all PASSED on `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/`.
* Per-trial sanity gate: FULL traces show clean spike trains in PD with ND suppressed; passive modes
  never exceed -2 mV (no dendritic-spike escape after HHst zeroing).

## Conclusion

Three-line summary for follow-on tasks:

* **Cross-model convergence on shunting inhibition design**: both deposited Poleg-Polsky 2016
  (t0065) and de Rosenroll 2026 (t0066) place `e_GABA = v_rest = -60 mV`, making IPSP_PASSIVE a
  flat-at-reversal trace in both. This is a recurring DSGC modelling pattern, not an idiosyncrasy of
  one cell.
* **Direction selectivity in de Rosenroll is not encoded purely on the inhibitory side either**:
  EPSP_PASSIVE shows ~1.6 mV PD-vs-ND difference from bar geometry (BIP arrival timing varies with
  direction), but the bulk of the FULL DSI (0.74) comes from inhibitory shunting.
* **The voltage-only protocol cannot resolve g_inh(t) in either model** — both converged to
  IPSP-flat-at-reversal — motivating SEClamp follow-ups on both substrates to quantify the shunt
  magnitude directly.
