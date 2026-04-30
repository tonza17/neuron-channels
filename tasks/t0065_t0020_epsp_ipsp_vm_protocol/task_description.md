# Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Motivation

The from-scratch DSGC family (t0052-t0059) is trapped in a binary regime — single-spike-per-trial
giving a trivial DSI of 1.0, or full suppression giving DSI of 0. Diagnostic tasks t0060-t0064
characterised that trap from several angles (AMPA-only escape, NMDA-only escape, AMPA priming, HH
voltage-step and current-step tests) but the central question remains open: how does a model that
*does* show graded direction selectivity decompose into excitatory and inhibitory drives?

Task t0020 is one of the few prior runs that produced both a non-trivial firing rate (~14.85 Hz
peak) and a meaningful DSI (0.7838) — using the deposited Poleg-Polsky & Diamond 2016 ModelDB
189347 cell under the native `gabaMOD` parameter-swap protocol (PD = 0.33, ND = 0.99). That same
deposited model has not yet been measured with the new EPSP_PASSIVE / IPSP_PASSIVE / FULL trial-mode
protocol that the from-scratch family standardised in t0059.

The goal of this task is to apply that protocol to the deposited model:

* **EPSP_PASSIVE** — Hodgkin-Huxley (HH) channels off, GABA off, AMPA + NMDA active. Records the
  pure excitatory PSP at the soma.
* **IPSP_PASSIVE** — HH off, AMPA + NMDA off, GABA active. Records the pure inhibitory PSP.
* **FULL** — HH on, all synapses at canonical defaults. Records full somatic Vm (the t0020
  reference condition).

Together these three traces decompose the FULL Vm into its excitatory and inhibitory components
under exactly the same stimulus, in a model that is known to produce graded direction selectivity.
This gives us a reference Vm/EPSP/IPSP triplet to compare against the from-scratch family's
binary-regime traces — telling us whether the binary regime is (a) excitatory under-drive, (b)
inhibitory over-shunt, or (c) HH miscalibration.

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as built in
  `tasks/t0008_port_modeldb_189347/code/build_cell.py::build_dsgc()`.
* Stimulus: deposited drifting-bar stimulus, default parameters from `t0008.apply_params`.
* Directions: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`) — matching t0020.
* Trial modes: `EPSP_PASSIVE`, `IPSP_PASSIVE`, `FULL` (the same enum used in t0059's
  `code/trial.py`, redefined locally because we are running on the deposited cell, not the
  from-scratch one).
* Per-trial Vm trace: full somatic voltage trace recorded at every NEURON timestep; saved to a
  per-mode CSV.
* Trials per (mode, direction) cell: 1 (single seed = 1). This is a diagnostic decomposition, not a
  tuning-curve sweep — one trace per condition is sufficient to read off EPSP/IPSP shape.

This gives 6 trials total: 3 modes × 2 directions × 1 trial.

## Approach

1. Reuse `t0008.apply_params` and `t0008.build_dsgc` to construct the deposited cell.
2. Reuse `t0020.run_gabamod_sweep::run_one_trial_gabamod`'s structure as a starting template.
3. Channel-isolation overrides follow the t0049 pattern:
   * Call `apply_params(h, seed=1)` and `h("update()")` and `h("placeBIP()")` first (so that the
     default conductances are written to all point processes),
   * Override the relevant globals from Python (`h.SpikesOn`, `h.gabaMOD`, `h.b2gampa`,
     `h.b2gnmda`),
   * Re-call `h("update()")` and `h("placeBIP()")` so the synaptic point processes pick up the
     overridden globals,
   * Attach Vm + t recorders, `finitialize`, `continuerun`.
4. Save raw traces to `data/voltage_traces.csv` (long-format: `mode, direction, t_ms, v_mv`) so a
   downstream plot script can re-read without re-simulating.
5. Plot per-mode 2-panel figures (PD vs ND) and a 3-mode summary panel; embed in
   `results_detailed.md`.

The `EPSP_PASSIVE` setting `gabaMOD = 0` collapses PD and ND to the same condition (no inhibition to
swap). We still run both directions for completeness — they should overlay exactly. If they do
not, the deposited model has direction-dependent state we have not yet identified.

## Configurations

Six trials, all `seed = 1`:

| Mode | Direction | SpikesOn | gabaMOD | b2gampa | b2gnmda |
| --- | --- | --- | --- | --- | --- |
| EPSP_PASSIVE | PD | 0 | 0.0 | default | default |
| EPSP_PASSIVE | ND | 0 | 0.0 | default | default |
| IPSP_PASSIVE | PD | 0 | 0.33 | 0.0 | 0.0 |
| IPSP_PASSIVE | ND | 0 | 0.99 | 0.0 | 0.0 |
| FULL | PD | 1 | 0.33 | default | default |
| FULL | ND | 1 | 0.99 | default | default |

`default` means whatever value `apply_params(h, seed=1)` writes (canonical paper values).
`SpikesOn = 0` activates the deposited model's built-in HH disable path (the same one t0046 and
t0049 already use for sub-threshold measurements).

## Outputs

* `data/voltage_traces.csv` — long-format per-sample table.
* `results/metrics.json` — per-trial scalar summaries: peak Vm, baseline-subtracted peak
  amplitude, spike count (FULL only), trial duration.
* `results/images/vm_full_pd_vs_nd.png` — FULL-mode Vm trace, PD overlaid with ND.
* `results/images/epsp_pd_vs_nd.png` — EPSP_PASSIVE trace, PD overlaid with ND (expected to
  superimpose).
* `results/images/ipsp_pd_vs_nd.png` — IPSP_PASSIVE trace, PD overlaid with ND.
* `results/images/three_mode_pd_overlay.png` — PD direction across all three modes on one axis.
* `results/images/three_mode_nd_overlay.png` — ND direction across all three modes on one axis.
* `results/results_summary.md`, `results/results_detailed.md` with per-mode peak amplitudes and a
  qualitative description of the decomposition.

## Key Questions

1. What is the peak EPSP amplitude (passive, GABA-off) in PD versus ND? Are they identical?
2. What is the peak IPSP deflection in PD versus ND, and does the PD-vs-ND difference quantitatively
   match the gabaMOD scalar ratio (0.33 vs 0.99)?
3. When EPSP and IPSP are summed by hand, does the result resemble the FULL Vm under HH-off
   conditions? Or is the cell's nonlinear summation contributing meaningfully?
4. How do the deposited model's EPSP and IPSP shapes compare to the from-scratch family's EPSP/IPSP
   traces from t0059? This contextualises whether the binary regime is a synaptic-balance issue or
   an HH-calibration issue.

## Compute and Budget

* Local Windows workstation. Six trials × ~1.5 minutes each ≈ 10 minutes wall-clock.
* No paid API or remote GPU costs.

## Time Estimation

* Implementation: 1 hour.
* Run + plotting: 30 minutes.
* Reporting: 30 minutes.

## Dependencies

* `t0020_port_modeldb_189347_gabamod` — provides `run_one_trial_gabamod` template, the
  `apply_params` import, the `_assert_bip_positions_baseline` guard, and the validated PD/ND scalar
  values.

We do not formally depend on t0059 because that task uses the from-scratch cell substrate. We do
copy its `TrialMode` enum spelling for consistency, but the implementation is independent.

## Risks and Fallbacks

* If the deposited model's `b2gampa = 0` + `b2gnmda = 0` does not actually silence excitatory drive
  (the deposited code is a HOC tangle), we will detect this by the EPSP_PASSIVE-vs-IPSP_PASSIVE
  trace shapes being non-orthogonal. Fallback: also zero `nmdaOn = 0` and verify excitatory drive
  vanishes.
* If `SpikesOn = 0` does not fully suppress HH (it should, per t0046 / t0049 usage), the FULL-vs-
  passive traces will be ambiguous. Fallback: explicitly zero the soma `gnabar_hh` and `gkbar_hh`
  via Python after `apply_params` and verify Vm cannot exceed -20 mV in passive trials.

## Verification Criteria

* All six trials complete without raising `_assert_bip_positions_baseline`.
* EPSP_PASSIVE PD and ND traces are bit-identical (gabaMOD = 0 in both).
* IPSP_PASSIVE peak amplitude in ND > peak amplitude in PD (more inhibition → larger
  hyperpolarisation in ND).
* FULL-mode PD trace shows higher firing rate than ND, consistent with t0020's headline result.
* Plots embedded in `results_detailed.md` render correctly on GitHub.
