---
spec_version: "2"
answer_id: "does-signed-dsi-change-t0126-pareto-structure"
answered_by_task: "t0129_t0126_signed_dsi_real_rates_1seed"
date_answered: "2026-05-26"
---
# Does the signed-DSI re-evaluation change t0126's Pareto structure?

## Question

Does the signed-DSI re-evaluation of t0126's protocol change the Pareto structure, or is the
vector-sum / signed distinction immaterial on the antipodal pair?

## Answer

Yes. The signed-DSI re-evaluation surfaces structure that vector-sum DSI silently discards: on this
single seed (3517) 95 viable cells out of 5,496 have genuinely reversed preference (R_ND > R_PD,
deepest reversal `dsi_signed = -0.778`) and would have been collapsed to positive magnitude under
vector-sum DSI. None of these reversed cells reach the t0129 final Pareto front (they are dominated
in F-space by the silent / DSI=0 cluster at the ATP minimum), but they would have been Pareto
candidates under the t0126 vector-sum objective, polluting the high-magnitude region of t0126's
front with cells whose preferred direction is actually opposite to what vector-sum suggests. The
sign-flip count for t0126's own Pareto cells cannot be recovered because t0126 did not persist
per-direction spike counts and its `pd_rate_hz = 40` is a synthesised placeholder.

## Sources

* Task: `t0126_bedb_dsi_atp_per_spike_nsga2_60gen`
* Predictions asset:
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/`
* Comparator chart:
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/pareto_t0126_vs_t0129_overlay.png`
* Per-cell data: `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/cell_params.jsonl`
