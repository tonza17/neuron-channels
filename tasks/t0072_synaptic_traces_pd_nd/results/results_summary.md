---
spec_version: "2"
task_id: "t0072_synaptic_traces_pd_nd"
date_completed: "2026-05-01"
status: "complete"
---
# Synaptic Conductance and Current Traces (PD vs ND)

## Summary

Recorded `g(t)` and `v_local(t)` from every synapse on each model bed (Bed A: 282 BIPsyn +
SACinhibsyn + SACexcsyn = 4 synapse types; Bed B: 177 Exp2Syn ACh + GABA = 2 types) for one PD and
one ND trial each at 1 ms resolution, computed `I = g · (v_local − E_rev)` post-hoc, and plotted
population mean ± 1 SD per synapse type with PD and ND overlaid. Two multi-panel figures (Bed A:
4×2; Bed B: 2×2) plus a 1.0 MB Typst-typeset PDF embedding both figures and the full methodology.

## Metrics

* **Bed A GABA peak conductance**: PD = **0.38 nS** vs ND = **0.70 nS** (1.87× ratio, matches the
  `gabaMOD = 0.99 / 0.33` envelope ratio diluted by post-synaptic v feedback).
* **Bed A NMDA peak conductance**: PD = **0.30 nS** vs ND = **0.19 nS** — counter-intuitive
  ND-suppression because stronger ND inhibition keeps dendritic v hyperpolarised, deepening the
  voltage-dependent Mg block on `g_NMDA`.
* **Bed A AMPA + ACh**: essentially identical between PD and ND (excitatory drive and cholinergic
  SAC drive are direction-symmetric on this bed).
* **Bed B GABA peak conductance**: PD = **0.16 nS** vs ND = **1.25 nS** (7.6× ratio driven by the
  per-event Bernoulli sigmoid going from p = 0.084 at 0° to p = 0.780 at 180°).
* **Bed B ACh peak conductance**: PD = **0.103 nS** vs ND = **0.107 nS** (well within the SD band;
  `BASE_ACH_PROB = 0.5` is direction-independent).
* **Recorded data volume**: 12 raw `.npz` per-synapse trace files in `data/` (~36 MB); shape (282,
  1000\) for Bed A and (177, 1000) for Bed B. Aggregated 49-key `.npz` for plotting.

## Verification

* `verify_research_code` — PASSED (0 errors, 0 warnings).
* `verify_plan` — PASSED (0 errors, 0 warnings).
* `verify_task_results` — PASSED (after Examples section was rewritten with 10 fenced-code
  Input/Output blocks per the task_results spec).
* `verify_task_metrics` — PASSED (`metrics.json = {}`; no registered metric applies).
* `verify_suggestions` — PASSED.
* `verify_task_dependencies` — PASSED (all 7 deps completed).
* `ruff check`, `ruff format`, `mypy -p tasks.t0072_synaptic_traces_pd_nd.code` — all PASSED.
* No upstream task source files modified; both NEURON cells built via registered library entry
  points (`build_dsgc` from t0008's `modeldb_189347_dsgc`, `build_dsgc_cell` from t0024's
  `de_rosenroll_2026_dsgc`).

## Key takeaways

The two figures (`results/images/bed_a_synaptic_traces.png` and
`results/images/bed_b_synaptic_traces.png`) make the direction-encoding mechanism viscerally
obvious. On Bed A, only the GABA channel changes shape between PD and ND — confirming the
gabaMOD-scalar mechanism. On Bed B, both ACh and GABA can change in principle (per-event sigmoid),
but in practice only GABA shows a strong PD/ND asymmetry because `BASE_ACH_PROB` is fixed at 0.5.
The Bed A NMDA's mild ND-suppression (Mg block deepens under stronger inhibition) is a real
biophysical consequence of the v-dependence of the NMDA channel — surfaced here for the first time
by per-synapse recording.

For full methodology, per-figure analysis, ten single-synapse examples, and the REQ-1..REQ-10
coverage table, see `results_detailed.md` and the typeset PDF at `results_detailed.pdf`.
