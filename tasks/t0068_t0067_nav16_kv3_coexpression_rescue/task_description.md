# Nav1.6 + Kv3 co-expression: does Kv3 rescue the DSI loss caused by Nav1.6?

## Motivation

t0067 found that adding Nav1.6 to the deposited Poleg-Polsky soma monotonically erodes direction
selectivity (DSI = 0.80 → 0.75 → 0.48 → 0.23 across baseline → low → med → high
density). Nav1.6 alone raises both PD and ND firing, but ND climbs faster proportionally because the
baseline ND firing was sub-threshold. The hypothesis (suggestion S-0067-02): if we ALSO add Kv3 at
the same time, Kv3's fast repolarisation could allow the cell to recover from each AP faster and let
the inhibitory shunt regain modulatory power — restoring the DSI gap.

This task tests that hypothesis directly by sweeping Kv3 density at two fixed Nav1.6 densities (med
= 30 mS/cm², high = 90 mS/cm²) and measuring whether Kv3 co-expression progressively rescues DSI
back toward baseline.

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as in t0008 / t0065 / t0067.
* Mode: only `FULL` (HH on, all synapses at canonical defaults). Same gabaMOD-swap protocol as
  t0067.
* Direction: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`).
* Seeds per condition: 5.
* Channels: Nav1.6 + Kv3 from t0067's vendored MODs (kinetics from Carter-Bean 2009 and Erisir 1999
  respectively).

## Conditions

9 conditions × 2 directions × 5 seeds = **90 FULL trials**.

| condition_id | Nav1.6 (mS/cm²) | Kv3 (mS/cm²) | Notes |
| --- | --- | --- | --- |
| baseline | 0 | 0 | Reference (matches t0067 baseline DSI = 0.80) |
| nav16_med | 30 | 0 | t0067 anchor (DSI = 0.48) |
| nav16_med_kv3_low | 30 | 7 | Co-insertion: low Kv3 |
| nav16_med_kv3_med | 30 | 20 | Co-insertion: med Kv3 |
| nav16_med_kv3_high | 30 | 60 | Co-insertion: high Kv3 |
| nav16_high | 90 | 0 | t0067 anchor (DSI = 0.23) |
| nav16_high_kv3_low | 90 | 7 | Co-insertion: low Kv3 |
| nav16_high_kv3_med | 90 | 20 | Co-insertion: med Kv3 |
| nav16_high_kv3_high | 90 | 60 | Co-insertion: high Kv3 |

## Approach

1. Vendor the same 5 MOD files from t0067 (`nav16t67`, `napt67`, `nart67`, `kv3t67`, `kv4t67`) into
   the task's `code/mods/`. The t0067 MOD files are reused verbatim — same kinetics, same
   NONSPECIFIC_CURRENT pattern.
2. Compile a task-local DLL.
3. Build the t0008 cell once. Insert all 5 mechanisms on the soma at gbar=0; per-trial set the
   active Nav1.6 and Kv3 gbars to the target densities (others stay at 0).
4. Run 90 FULL-mode trials using the t0067 trial-driver structure adapted to support simultaneous
   setting of Nav1.6 and Kv3 densities.
5. Aggregate per-trial scalars to per-condition mean ± SD; compute DSI per condition.

## Outputs

* `data/per_trial_metrics.json` — 90 trial records.
* `data/dsi_by_condition.json` — 9 conditions.
* `results/metrics.json` — registered `direction_selectivity_index` for the baseline.
* `results/images/dsi_rescue_curve.png` — DSI vs Kv3 density at fixed Nav1.6 (2 lines for
  Nav1.6_med vs Nav1.6_high, with baseline reference).
* `results/images/firing_rate_rescue.png` — PD and ND firing rate vs Kv3 density at fixed Nav1.6
  (2 sub-panels).
* `results/results_summary.md`, `results/results_detailed.md` (spec_version 2) with rescue-effect
  interpretation.

## Failure-mode policy

Same as t0067: peak Vm > +60 mV or < −80 mV → flag `is_unstable = true`. Trial data still saved.

## Key Questions

1. Does Kv3 co-insertion progressively rescue DSI as Kv3 density increases? Specifically: is
   DSI(nav16_high + kv3_high) > DSI(nav16_high) by a meaningful margin (Δ > 0.1)?
2. Does Kv3 reduce firing rate (the expected effect of fast K+ repolarisation) preferentially in ND
   (which would scale DSI back up) or in both directions equally (which would not)?
3. Is the rescue effect different for Nav1.6_med vs Nav1.6_high? At med, the cell is in a regime
   where DSI was 0.48 (still quite directional); at high, DSI was 0.23 (close to collapse). Which
   regime benefits more from Kv3?

## Compute and Budget

* Local Windows workstation. ~3 s/trial × 90 trials ≈ 5 min.
* External costs: $0.

## Time Estimation

* Implementation (port t0067 code, adapt for co-expression): 1 hour.
* Sweep: 5 min.
* Plotting + reporting: 45 min.
* Verification + PR: 30 min.
* Total: ~2.5 hours.

## Dependencies

* `t0008_port_modeldb_189347` — cell builder + base nrnmech.dll.
* `t0065_t0020_epsp_ipsp_vm_protocol` — gabaMOD-swap baseline.
* `t0067_t0065_soma_channel_addition_sweep` — vendored MOD files (Nav1.6 + Kv3 reused verbatim),
  trial driver template, baseline DSI = 0.80, Nav1.6 anchor DSIs (med = 0.48, high = 0.23).

## Risks and Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Kv3 at high density breaks the cell at Nav1.6_high (e.g., AP suppressed entirely). | spike_count = 0 in BOTH directions. | Document as "rescue-overshoot": Kv3 reverses Nav1.6's effect too aggressively. |
| 2 | Kv3 has no rescue effect at either Nav1.6 level (DSI unchanged from t0067 anchors). | DSI(Nav1.6_X + Kv3_Y) ≈ DSI(Nav1.6_X) for all Y. | Report null result; the rescue hypothesis is falsified. Kv3 alone may have been inert in t0067 because the cell wasn't in a fast-spiking regime; it may also be inert when added to Nav1.6 because the kinetic regime still doesn't engage Kv3 strongly. |
| 3 | Kv3 actually amplifies DSI loss (DSI drops further than Nav1.6 alone). | DSI(co-insertion) < DSI(Nav1.6 alone). | Surprising but possible. Document and explore in suggestions. |

## Verification Criteria

* All 90 trials complete.
* `data/per_trial_metrics.json` has 90 entries.
* `data/dsi_by_condition.json` has 9 entries.
* Both PNG plots exist and are embedded in `results_detailed.md`.
* All standard verificators pass.
