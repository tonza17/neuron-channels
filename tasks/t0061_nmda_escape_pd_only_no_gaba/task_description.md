# Quick NMDAR-Escape Test on t0059 Substrate at Preferred Direction with GABA = 0

## Source

User-commissioned diagnostic, parallel to t0060 but with NMDAR (Mg-block) replacing AMPA. Goal:
characterise how the from-scratch DSGC's somatic V(t) responds to a single bar moving in the
preferred direction when inhibition is fully removed (GABA = 0) and **NMDA**-only excitation is
swept across a wide range — both with HH active (FULL mode) and disabled (EPSP_PASSIVE mode).

## Mechanism Choice

This task uses the biologically correct **Mg-block NMDA** (Jahr-Stevens) mechanism inherited from
t0055's `NMDA_MgBlock.mod`. The Mg-block formula and parameter values are taken verbatim from
ModelDB 189347 (Poleg-Polsky 2016): `n = 0.25 /mM`, `gamma = 0.08 /mV`, `tau1 = 5 ms`,
`tau2 = 80 ms`, `e = 0 mV`, `Voff = 0` (voltage-dependent). Without AMPA priming, low-gNMDA
trials are expected to produce minimal response (Mg block is engaged at V_rest = -65 mV); the
sweep tests whether sufficiently high gNMDA can self-prime via leaky Mg-block conductance.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** (no inhibition) |
| AMPA | **0** (no AMPA — NMDA-only excitation) |
| Direction | **theta = 0 deg** only (preferred direction) |
| Trials per condition | **1** |
| `gNMDA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} (8 values) |
| Mode | `FULL` (HH on, soma + AIS) and `EPSP_PASSIVE` (HH off, save-and-zero gnabar / gkbar) |

Total: **8 gNMDA x 2 modes x 1 trial x 1 direction = 16 trials**. Wall-clock estimate: ~1-3
minutes on local CPU under CVODE.

## Outputs

* `results/voltage_traces_pd_only.csv` — 16 traces (one row group per (gNMDA, mode) cell), full
  V_soma(t).
* `results/summary_pd_only.csv` — per-(gNMDA, mode) peak / min Vm and spike count.
* `results/images/voltage_response_grid.png` — 8 panels (one per gNMDA), each panel overlays
  FULL (HH-on) and EPSP_PASSIVE (HH-off) trace at theta = 0 deg.
* `results/images/voltage_response_overlay.png` — single combined panel with all 16 traces.
* `results/results_summary.md` and `results_detailed.md`.

## Architecture

Reuses t0059's morphology, placement (seed 0), neuron bootstrap, and trial-mode dispatcher. The
synapse layer is replaced wholesale: each E location gets ONE `NMDA_MgBlock` POINT_PROCESS plus a
NetStim + NetCon (no AMPA Exp2Syn, no GABA tonic). Spatial gating is preserved but with
`GABA = 0` and no AMPA, only the NMDA mechanism is active.

The `NMDA_MgBlock.mod` source is copied verbatim from t0055 (provenance: ModelDB 189347
`bipolarNMDA.mod`) and recompiled in t0061's `code/mod/` for this task's NEURON kernel.

## Out of Scope

* AMPA + NMDA combination (that's t0054 / S-0057-06 territory).
* Voltage-independent NMDA (`Voff = 1`) — fixed `Voff = 0` (Mg-block on).
* Multi-trial statistics, DSI, compare-literature, suggestions.
* Asset production (no library produced).

## Verification Criteria

* Both `voltage_traces_pd_only.csv` and the two PNGs exist.
* `verify_task_file.py`, `verify_task_folder.py`, `verify_task_results.py`, `verify_logs.py` all
  pass with 0 errors.
