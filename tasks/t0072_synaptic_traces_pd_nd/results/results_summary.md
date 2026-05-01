---
spec_version: "2"
task_id: "t0072_synaptic_traces_pd_nd"
date_completed: "2026-05-01"
status: "complete"
---
# Synaptic Conductance and Current Traces (PD vs ND): Summary

Two DSGC compartmental models — Bed A (Poleg-Polsky 2016 deposited variant under the t0020 `gabaMOD`
swap) and Bed B (de Rosenroll 2026 port under the t0066 bar-angle swap) — were each driven through
one PD and one ND trial with a fixed seed. Per-synapse conductance state variables (`gAMPA`,
`gNMDA`, `g_GABA`, `g_ACh`) and the local membrane voltage `v_local` were recorded at 1 ms
resolution from every synapse instance (Bed A: 282 ON-dendrite synapses per channel; Bed B: 177
terminal-dendrite Exp2Syn synapses per channel). Post-hoc current `I = g · (v_local − E_rev)` was
computed in pA, and population mean ± 1 SD across synapses was taken at each time point.

The two figures (Bed A 4×2 and Bed B 2×2) make the direction-encoding mechanism visually explicit:

* **Bed A** — only the GABA channel scales between PD and ND (mean peak `g_GABA` **0.38 nS** PD vs
  **0.70 nS** ND, a 1.87× ratio matching the `gabaMOD = 0.99 / 0.33` envelope ratio diluted by
  post-synaptic v feedback). AMPA and ACh traces are essentially identical between directions
  because the BIPsyn excitatory drive and the SACexc cholinergic drive are direction-symmetric on
  this bed. The NMDA channel shows a counter-intuitive **suppression** at ND (mean peak 0.30 nS PD
  vs 0.19 nS ND): stronger ND inhibition keeps the dendritic v more hyperpolarised, which deepens
  the voltage-dependent Mg block.

* **Bed B** — the GABA channel scales dramatically (mean peak `g_GABA` **0.16 nS** PD vs **1.25 nS**
  ND, a 7.6× ratio driven by the per-event Bernoulli sigmoid going from p = 0.084 at 0° to p = 0.780
  at 180°). The ACh channel uses a fixed `BASE_ACH_PROB = 0.5` and is direction-independent (mean
  peak 0.103 nS PD vs 0.107 nS ND, well within the SD band).

Outputs: 12 raw `.npz` per-synapse trace files in `data/`, `data/aggregated.npz` (49 keys),
`results/images/bed_a_synaptic_traces.png` (649 KB), `results/images/bed_b_synaptic_traces.png` (172
KB), `results/results_detailed.md`, `results/results_detailed.typ`, and the Typst-compiled
`results/results_detailed.pdf` (1.0 MB) embedding both figures. See `results_detailed.md` and the
PDF for full methodology, per-row analysis, six single-synapse examples, and the REQ-1..REQ-10
coverage table.

No upstream task source files were modified; both NEURON cells were built via registered library
entry points (`build_dsgc` from t0008's `modeldb_189347_dsgc`, `build_dsgc_cell` from t0024's
`de_rosenroll_2026_dsgc`); private helpers (`_setup_synapses`, `_bar_arrival_times`,
`_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events`, `SynapseBundle`) were
copied verbatim from t0024's `run_tuning_curve.py` into this task's `code/run_bed_b.py`.
