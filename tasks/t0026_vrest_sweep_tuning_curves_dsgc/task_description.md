# V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Motivation

Two of the four DSGC compartmental-model ports in this project
(`modeldb_189347_dsgc_channel_testbed` from t0022 and `de_rosenroll_2026_dsgc` from t0024) produce
direction-selective tuning curves at the default resting potential of `-60 mV`. The project's
research questions (RQ1, RQ4) ask how the cell's biophysics — particularly voltage-gated-channel
availability and dendritic integration — shape tuning. Resting potential is the single most direct
experimental knob for probing those mechanisms because it controls:

1. **Na channel inactivation availability**: at hyperpolarized holding (e.g. `-90 mV`) the fast
   sodium gate sits in its deinactivated state, producing a larger pool available for spiking; at
   depolarized holding (e.g. `-30 mV`) a large fraction is tonically inactivated.
2. **NMDA receptor Mg block**: the voltage-dependent Mg block relieves as the membrane depolarizes,
   so NMDA contribution to synaptic integration grows with V_rest. This should shift the E/I balance
   that implements asymmetric inhibition in both ports.
3. **Leak driving force and input resistance**: with `eleak` pinned to a new holding, the leak
   current's reversal and the cell's apparent input resistance both change, altering how strong
   BIP/SAC input currents look to the soma.

The two driver paradigms under test — deterministic per-dendrite E-I scheduling in t0022 versus
AR(2)-correlated stochastic release in t0024 — should respond differently to V_rest because they
differ in how they compose inhibitory current magnitude against voltage-gated drive.

## Scope

Run a V_rest sweep on both ports. All other protocol knobs (bar velocity, 12 angles, tstop,
morphology) are held fixed to the defaults of the respective library assets.

### V_rest values

Exactly eight values, all in mV: `-90, -80, -70, -60, -50, -40, -30, -20`.

### Holding strategy

At every V_rest value, set **both** `V_INIT_MV` **and** `ELEAK_MV` (leak reversal) to the sweep
value before initialising NEURON. Moving only `v_init` re-settles to `eleak` within a few
milliseconds and does not implement a true resting-potential shift; moving only `eleak` leaves the
initial condition mismatched. Both must move together.

### Models and trial budgets

| Model | Task | Driver | Trials per angle | Total trials |
| --- | --- | --- | --- | --- |
| `modeldb_189347_dsgc_channel_testbed` | t0022 | Deterministic per-dendrite E-I | 1 | 1 × 12 × 8 = 96 |
| `de_rosenroll_2026_dsgc` (correlated `rho=0.6`) | t0024 | AR(2)-correlated stochastic release | 10 | 10 × 12 × 8 = 960 |

One trial per angle is sufficient for t0022 because its driver is deterministic; only the V_rest
value changes between (angle, V_rest) runs. Ten trials per angle are retained for t0024 so that
trial-to-trial variance in the AR(2) release process remains visible in the tuning curve — lower
counts would fold V_rest effects into noise.

### Protocol

For each model and each V_rest value, run the existing 12-angle protocol (`0, 30, 60, …, 330`
degrees) using the library asset's stock `run_trial` / `run_one_trial` function. Only override the
two holding-potential constants — do not modify the library asset itself (immutability rule 5) and
do not change bar velocity, tstop, or any other constant.

## Approach

### Implementation

Two thin wrapper drivers live in `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/`:

* `run_vrest_sweep_t0022.py` — imports from `tasks.t0022_modify_dsgc_channel_testbed.code`,
  parameterises `V_REST_MV`, sets both `h.v_init` and every leak section's `e` parameter to that
  value, then invokes the stock tuning-curve routine across the 12 angles. Loops the 8 V_rest values
  serially.
* `run_vrest_sweep_t0024.py` — same idea against `tasks.t0024_port_de_rosenroll_2026_dsgc.code`.
  Uses the correlated `rho=0.6` AR(2) path (the task's headline condition).

Each wrapper writes one CSV per V_rest value under `data/t0022/` or `data/t0024/`, then concatenates
them into `data/t0022/vrest_sweep_tidy.csv` and `data/t0024/vrest_sweep_tidy.csv` with columns
`(v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`. Also records per-V_rest
wall time to `data/t0022/wall_time_by_vrest.json` and `data/t0024/wall_time_by_vrest.json`.

### Analysis

A single analysis script computes, for each (model, V_rest):

* Preferred direction and DSI (reusing the t0012 `tuning_curve_loss` scorer's DSI formula)
* Peak firing rate (Hz)
* Null-direction firing rate (Hz)
* HWHM (degrees)

Those values are written to `data/t0022/vrest_metrics.csv` and `data/t0024/vrest_metrics.csv`, and
summary tables are embedded in `results/results_detailed.md`.

### Plots (all in `results/images/`)

* 16 individual polar plots: `polar_<model>_vrest_<value>.png` (one per model × V_rest pair,
  plotting firing rate in Hz vs direction in degrees on a polar axis).
* 2 overlay polar plots: `polar_overlay_t0022.png` and `polar_overlay_t0024.png` showing all 8
  V_rest tuning curves on the same polar axes with a perceptually ordered colormap. Each answers the
  question "how does the tuning curve morph as V_rest moves from hyperpolarized to depolarized?"
* 2 Cartesian summary plots: `dsi_vs_vrest.png` and `peak_hz_vs_vrest.png` with both models
  overlaid, showing how DSI and peak firing rate trend with V_rest.

## Expected Assets

Two predictions assets, one per model. Each contains:

* `details.json` (predictions asset metadata following `meta/asset_types/predictions/`)
* The full tidy CSV as the predictions payload
* A short description linking back to this task and the source model's library asset

`expected_assets` in `task.json` is `{"predictions": 2}`.

## Dependencies

* `t0022_modify_dsgc_channel_testbed` — provides the `modeldb_189347_dsgc_channel_testbed` library
  asset and the `run_tuning_curve.py` driver that this task reuses.
* `t0024_port_de_rosenroll_2026_dsgc` — provides the `de_rosenroll_2026_dsgc` library asset and
  the correlated-AR(2) driver.

Both dependencies are completed and on main.

## Compute and Budget

* No remote compute, no paid API calls, no GPUs.
* Runs entirely on the local Windows workstation using the existing NEURON + Python stack.
* Expected wall time: ~25 min for t0022 (96 trials) + ~4 h 15 min for t0024 (960 trials at scale
  comparable to t0024's original 800-trial run).
* Total budget: `$0`.

## Metrics

Register the following if not already registered in `meta/metrics/` (propose as suggestions
otherwise; do not block on meta gaps):

* `dsi_at_vrest_<mv>` for each V_rest value
* `peak_hz_at_vrest_<mv>` for each V_rest value
* `hwhm_deg_at_vrest_<mv>` for each V_rest value
* `efficiency_wall_time_per_trial_seconds` (one value per model — total wall time / total trial
  count)

## Output Specification

### Charts (all in `results/images/`, embedded in `results_detailed.md`)

| Chart | Axes | Question answered |
| --- | --- | --- |
| `polar_<model>_vrest_<value>.png` | θ = direction (deg), r = firing rate (Hz) | What is the tuning curve shape at this specific V_rest? |
| `polar_overlay_<model>.png` | θ = direction (deg), r = firing rate (Hz), 8 curves | How does the tuning curve morph with V_rest? |
| `dsi_vs_vrest.png` | x = V_rest (mV), y = DSI, 2 lines (one per model) | Is there a V_rest that maximises direction selectivity? |
| `peak_hz_vs_vrest.png` | x = V_rest (mV), y = peak firing rate (Hz), 2 lines | Where is peak firing rate highest? Does the 40-80 Hz envelope open up? |

### Tables in `results_detailed.md`

* Per-(model, V_rest) metrics: V_rest, DSI, peak_hz, null_hz, HWHM, wall_time_s
* Per-model aggregate efficiency: total trials, total wall time, seconds per trial

## Key Questions

1. Does either DSGC port show a V_rest value at which DSI is higher than at the default `-60 mV`
   baseline?
2. Does either port reach the t0004 target peak-firing-rate envelope (40-80 Hz) at any V_rest value?
   This is the headline unresolved problem across all four existing ports.
3. Is the direction-selectivity mechanism in t0022 (deterministic per-dendrite E-I) more or less
   V_rest-dependent than in t0024 (AR(2) stochastic release)?
4. At what V_rest does each port silence (all-angle firing rate ≈ 0 Hz) on the hyperpolarized end,
   and at what V_rest does it enter depolarization block on the depolarized end?
5. Does HWHM narrow systematically as V_rest increases (depolarization-driven gain change), or is it
   relatively flat across the sweep (consistent with inhibition-dominated tuning)?

## Source Suggestion

None. Researcher-directed experiment captured in brainstorming session 5
(`t0025_brainstorm_results_5`).
