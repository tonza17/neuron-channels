# Test t0024 de Rosenroll DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Motivation

Task t0065 applied the EPSP_PASSIVE / IPSP_PASSIVE / FULL trial-mode decomposition to the deposited
Poleg-Polsky & Diamond 2016 DSGC and produced a clean diagnostic finding: direction selectivity in
that cell is purely shunting-driven, because the model's design choice of
`e_SACinhib = v_rest = -60 mV` makes inhibitory current vanish at rest. The IPSP_PASSIVE traces were
flat at -60 mV in both PD and ND despite a 3× difference in inhibitory conductance.

The de Rosenroll et al. 2026 DSGC (ported in t0024) is structurally independent from the
Poleg-Polsky lineage: a 341-section morphology with `HHst_noiseless` channels, `Exp2Syn` ACh (E = 0
mV) and `Exp2Syn` GABA (E = -60 mV) synapses on 177 terminal dendrites, AR(2)-correlated Poisson
release, and a per-synapse GABA release-probability sigmoid that swings from 0.05 (PD) to 0.80 (ND)
— a much steeper directional asymmetry than Poleg-Polsky's 3× scalar swap.

Because the de Rosenroll resting potential is set by `HHst_noiseless` parameters (not pinned to
e_GABA), the IPSP_PASSIVE trace should be a **real hyperpolarising response** rather than a flat
trace. This gives us a direct test of whether the t0065 shunting-only finding is generic to DSGC
modelling or specific to Poleg-Polsky's design choice.

## Scope

Apply the same EPSP_PASSIVE / IPSP_PASSIVE / FULL decomposition to the de Rosenroll cell, recording
somatic Vm in PD (0°) and ND (180°). The protocol mapping is:

* **EPSP_PASSIVE** — Set GABA `Exp2Syn` weight to 0 on every terminal dendrite; zero HH
  conductances on soma + AIS (turn off `HHst_noiseless` Na and K). Records the pure excitatory PSP
  from ACh + AR(2) noise drive.
* **IPSP_PASSIVE** — Set ACh `Exp2Syn` weight to 0 on every terminal dendrite; zero HH
  conductances. Records the pure inhibitory PSP, with the per-synapse GABA release-probability
  sigmoid still encoding direction (PD: ~5% release prob, ND: ~80%).
* **FULL** — All synapses + HH active at canonical t0024 defaults. Standard PD/ND condition
  matching the t0024 12-angle tuning curve at 0° and 180°.

Unlike t0065 (which is deterministic given seed and used 1 trial per cell), the de Rosenroll model
is stochastic — release rates are AR(2) noise → Poisson → NetCon.event injection. A single
seed gives a noisy single realisation. We use **20 trials per (mode, direction) cell** to match
t0024's existing tuning-curve practice and obtain a noise-averaged trace plus per-trial scalar
distributions.

This gives 6 cells × 20 trials = 120 trials total.

## Approach

1. Reuse `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.build_dsgc_cell()` to construct
   the cell exactly as in t0024.
2. Reuse `tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve.py`'s per-trial driver as a
   starting template, including the AR(2) noise generator and the per-synapse Poisson injection
   (`FInitializeHandler` + `NetCon.event`).
3. Channel-isolation overrides happen at the synapse-weight / HH-conductance level, set after cell
   construction and before each trial:
   * EPSP_PASSIVE: iterate the GABA NetCon list and set each `weight[0] = 0`; iterate soma + AIS
     sections and zero `gnabar_HHst_noiseless` and `gkbar_HHst_noiseless`.
   * IPSP_PASSIVE: iterate the ACh NetCon list and set each `weight[0] = 0`; zero HH as above.
   * FULL: no overrides — accept canonical t0024 weights.
4. Per-trial sequence: build cell → apply overrides → set seed → generate AR(2) noise +
   Poisson spike times → schedule `NetCon.event` injections → attach Vm + t recorders + spike
   NetCon → `h.finitialize` → `h.continuerun(TSTOP_MS)`.
5. Save raw traces to `data/voltage_traces.csv` (long-format: `mode, direction, trial, t_ms, v_mv`)
   and per-trial scalars to `data/per_trial_metrics.json` (mode, direction, trial, peak_v_mv,
   baseline_v_mv, peak_minus_baseline_mv, spike_count, n_samples).
6. Plot per-mode 2-panel figures (PD vs ND, mean trace + IQR shading) and 3-mode summary panels
   (mean ± IQR per mode, PD and ND on separate axes).

## Configurations

Six cells (3 modes × 2 directions), 20 trials per cell, all using AR(2) `rho = 0.6` (correlated
condition matching t0024's primary protocol):

| Mode | Direction | ACh weight | GABA weight | HH | Bar direction (deg) |
| --- | --- | --- | --- | --- | --- |
| EPSP_PASSIVE | PD | canonical | 0 (all syn) | OFF (gnabar = gkbar = 0) | 0 |
| EPSP_PASSIVE | ND | canonical | 0 (all syn) | OFF | 180 |
| IPSP_PASSIVE | PD | 0 (all syn) | canonical | OFF | 0 |
| IPSP_PASSIVE | ND | 0 (all syn) | canonical | OFF | 180 |
| FULL | PD | canonical | canonical | ON | 0 |
| FULL | ND | canonical | canonical | ON | 180 |

`canonical` means the t0024 default weights and conductances. The 20 trials per cell use seeds
`base + trial_index` per `code/ar2_noise.py`'s seed protocol.

## Outputs

* `data/voltage_traces.csv` — long-format per-sample table (~120 trials × ~tstop/dt samples).
* `data/per_trial_metrics.json` — per-trial scalar summaries.
* `results/metrics.json` — registered metric: `direction_selectivity_index` from FULL mode trial
  averages.
* `results/images/vm_full_pd_vs_nd.png` — FULL mean Vm trace, PD vs ND with IQR shading.
* `results/images/epsp_pd_vs_nd.png` — EPSP_PASSIVE mean trace, PD vs ND with IQR shading.
* `results/images/ipsp_pd_vs_nd.png` — IPSP_PASSIVE mean trace, PD vs ND with IQR shading
  (expected to show clear hyperpolarising deflection in this model, unlike t0065).
* `results/images/three_mode_pd_overlay.png` — PD direction across all three modes.
* `results/images/three_mode_nd_overlay.png` — ND direction across all three modes.
* `results/images/comparison_t0065_vs_t0066_ipsp.png` — side-by-side IPSP_PASSIVE comparison
  between deposited (t0065, flat at -60 mV) and de Rosenroll (t0066, expected hyperpolarising).
* `results/results_summary.md`, `results/results_detailed.md` with per-mode peak/trough amplitudes,
  the cross-model IPSP comparison, and DSI from FULL mode.

## Key Questions

1. What is the peak EPSP amplitude (passive, GABA off, HH off) in PD versus ND in the de Rosenroll
   cell? Does the AR(2) noise produce direction-coupled trace differences even with GABA off?
2. What is the peak/trough IPSP deflection in PD versus ND, and is this a real hyperpolarising
   response (expected, given e_GABA = -60 mV with v_rest typically lower than -60 mV)?
3. How does the de Rosenroll IPSP_PASSIVE trace shape compare to the t0065 deposited cell's flat
   IPSP_PASSIVE trace? Does the cross-model contrast confirm that t0065's flat result was a
   model-specific design artefact?
4. What is the FULL-mode DSI (spike count or firing rate) in PD vs ND? Does it match t0024's
   tuning-curve mean (DSI 12-angle correlated = 0.7759 at 0° vs 180°)?

## Compute and Budget

* Local Windows workstation. Per-trial wall-clock for de Rosenroll is ~64 s based on t0024's 4h15m
  for 240 trials. 120 trials × 64 s ≈ **2h10m** wall-clock for the sweep, plus ~5 minutes for
  plotting.
* External costs: **$0** total. No paid API calls, no remote GPU rental.

## Time Estimation

* Implementation (code + paths + constants + per-mode override functions): 1.5 hours.
* Sweep run: 2.5 hours wall-clock.
* Plotting + analysis + reporting: 1 hour.
* Verification + PR: 30 minutes.
* Total: ~5.5 hours including buffer.

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` — provides `build_dsgc_cell`, the AR(2) noise generator,
  per-synapse Exp2Syn / NetCon construction, and the per-trial driver template.
* `t0065_t0020_epsp_ipsp_vm_protocol` — provides the protocol design, the `TrialMode` enum
  pattern, and the t0065 IPSP_PASSIVE result (flat at -60 mV) which is the reference comparison
  point. Also supplies the `## Examples` and `## Task Requirement Coverage` formatting pattern
  refined in t0065's results.

## Risks and Fallbacks

* **Risk 1**: Setting GABA `weight[0] = 0` does not silence the synapse if t0024 also injects the
  release event via a separate mechanism (Poisson FInitializeHandler may pre-bind weights).
  Detection: IPSP_PASSIVE PD with GABA-weight=0 still shows hyperpolarising deflection. Fallback:
  instead set `gaba_netcon.event(0, weight=-1)` invalid, or skip the GABA spike-time injection
  entirely in the EPSP_PASSIVE branch by zeroing the per-synapse release-probability sigmoid output.
* **Risk 2**: Zeroing `gnabar_HHst_noiseless` may not fully suppress AP firing if the mechanism has
  a passive depolarisation path. Detection: EPSP_PASSIVE traces show spike-shaped events above -20
  mV. Fallback: also zero `gkbar_HHst_noiseless` and `gcal_*` and verify Vm cannot exceed -10 mV in
  any passive trial.
* **Risk 3**: 20 trials per cell may take longer than the 64 s/trial t0024 baseline if HH-off trials
  are slower (CVODE step density may grow with subthreshold dynamics). Detection: per-trial
  wall-clock > 90 s after first 5 trials. Fallback: drop to 10 trials per cell (60 trials total, ~1h
  compute) and document the reduced statistics.

## Verification Criteria

* All 120 trials complete, each producing a non-empty Vm trace.
* Per-trial sanity: EPSP_PASSIVE peak Vm > IPSP_PASSIVE trough Vm (excitation depolarises,
  inhibition hyperpolarises).
* Mean IPSP_PASSIVE trough in ND < mean trough in PD (more inhibition → deeper hyperpolarisation).
* FULL-mode mean spike count in PD > ND (consistent with t0024's tuning-curve DSI = 0.78).
* Cross-model comparison plot renders both t0065 and t0066 IPSP_PASSIVE traces with consistent axes
  for direct visual comparison.
* `verify_logs`, `verify_step_tracker`, `verify_research_code`, `verify_task_results`,
  `verify_task_metrics`, and `verify_pr_premerge` all pass.
