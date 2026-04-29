# Quick AMPA-Escape Test on t0059 Substrate at Preferred Direction with GABA = 0

## Source

User-commissioned quick diagnostic test (no brainstorm). Goal: characterise how the
from-scratch DSGC's somatic V(t) responds to a single bar moving in the preferred direction
when inhibition is fully removed (GABA = 0) and AMPA per-synapse conductance is swept across a
wide range — both with HH active (FULL mode) and disabled (EPSP_PASSIVE mode).

## Motivation

t0059 swept gAMPA in {0.5, 1, 2, 3, 4} nS with bar-arrival-locked GABA from 0.1 to 2 nS and found
the cell trapped in a single-spike-per-trial regime — max peak Hz = 2.143 Hz across all 25 grid
cells. The interpretation depended on whether the cap is set by inhibition timing, AMPA strength,
the absence of dendritic conductances, or driving-force saturation. Removing GABA entirely and
extending gAMPA up to 20 nS isolates the AMPA pathway alone, gives the upper-bound passive
depolarization (HH off) and the upper-bound spike count (HH on), and clarifies whether the
single-spike cap is set by AMPA insufficiency or by the morphology/active-channel substrate.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** (no inhibition, no I synapses driven) |
| Direction | **theta = 0 deg** only (preferred direction) |
| Trials per condition | **1** |
| `gAMPA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} (8 values) |
| Mode | `FULL` (HH on, soma + AIS) and `EPSP_PASSIVE` (HH off, save-and-zero gnabar / gkbar) |

Total: **8 gAMPA x 2 modes x 1 trial x 1 direction = 16 trials**. Wall-clock estimate: ~30-90
seconds on local CPU under CVODE.

## Outputs

* `results/voltage_traces_pd_only.csv` — 16 traces (one row group per (gAMPA, mode) cell), full
  V_soma(t) at native dt = 0.025 ms (no down-sampling — total data is small).
* `results/images/voltage_response_grid.png` — 8 panels (one per gAMPA), each panel overlays the
  FULL (HH-on) and EPSP_PASSIVE (HH-off) trace at theta = 0 deg.
* `results/images/voltage_response_overlay.png` — single combined panel with all 16 traces, 8
  colours for gAMPA, 2 line styles for HH on / off.
* `results/results_summary.md` — per-(gAMPA, mode) peak Vm, spike count (FULL only), description
  of the trend.

## Architecture

Reuses t0059's `minimal_dsgc_bar_locked_gaba_ampa_sweep` substrate verbatim with three runtime
overrides:

1. `GABA_BASE_NS_VALUES = (0.0,)` — single value at zero. The bar-arrival-locked window
   mechanism and centripetal-gating predicate remain in place but produce zero conductance per
   synapse.
2. `ANGLES_DEG = (0,)` — preferred direction only.
3. `AMPA_PEAK_NS_VALUES = (0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0)` — extended escape range.
4. `N_TRIALS_PER_ANGLE = 1` — single trial per condition (deterministic; trial-to-trial noise
   not relevant for a diagnostic test).

No code copy is needed. The t0059 entry point already supports CLI overrides for AMPA and GABA
subsets, angle subset, and n-trials. The plotting logic is task-specific (custom, not from
t0059) since t0059's plots are designed for the 25-cell grid.

## Out of Scope

* DSI / tuning curve analysis (only one direction).
* Compare-literature (diagnostic test, no published baseline match).
* Multi-trial statistics (single-trial design).
* Negative GABA / inhibition contributions (GABA = 0 by design).
* Asset production (this is a diagnostic — no library asset).

## Verification Criteria

* Both `voltage_traces_pd_only.csv` and the two PNGs exist.
* Each PNG shows monotonic peak-Vm-vs-gAMPA in EPSP_PASSIVE (no HH non-linearity expected) and a
  superlinear regime in FULL once gAMPA crosses spike threshold.
* `verify_task_file.py`, `verify_task_folder.py`, `verify_task_results.py`, `verify_logs.py` all
  pass with 0 errors.
