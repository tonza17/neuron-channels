# ⏹ Tasks: Not Started

4 tasks. ⏹ **4 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0122 — <strong>NSGA-II maximising DSI and minimising cytoplasm volume
(Bed B + 14-d morph)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0122_dsi_cytoplasm_volume_nsga2` |
| **Status** | not_started |
| **Effective date** | 2026-05-23 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0119_brainstorm_results_23`](../../../overview/tasks/task_pages/t0119_brainstorm_results_23.md), [`t0120_morph_generator_geometry_audit`](../../../overview/tasks/task_pages/t0120_morph_generator_geometry_audit.md) |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0097-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [NSGA-II maximising DSI and minimising cytoplasm volume (Bed B + 14-d morph)](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Task folder** | [`t0122_dsi_cytoplasm_volume_nsga2/`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/) |

# NSGA-II Maximising DSI and Minimising Cytoplasm Volume

## Source Suggestion

S-0097-01: "Bed B NSGA-II maximising DSI and minimising cytoplasm volume."

## Motivation

The t0097 multi-objective optimisation catalogue ranked DSI vs cytoplasm volume as the most
biologically-grounded objective pair in the project:

* Cajal's cytoplasm-conservation principle and Chklovskii et al. 2002's wiring-cost rule (3/5
  of grey-matter volume is dendrites + axons for optimal wiring) make cytoplasm a primary
  evolutionary cost objective.
* Cuntz et al. 2010 (10.1371/journal.pcbi.1002107) operationalised this as a `balancing
  factor` `bf in [0.2, 0.7]` for real dendritic trees -- a falsifiable prediction the
  optimiser can be tested against.
* Cytoplasm volume per section = pi * (diameter / 2)^2 * length, summed over soma + dendrites
  + AIS. Easy to compute from the existing `MorphologyResult` without any new generator code.

This is the natural next NSGA-II direction after the 5-seed substrate-rate confirmation batch
closed at t0115. Recurring biological-plausibility concerns about pure-DSI-maximisation runs
(the optimiser hits NMDA / Nav densities 85-122 sigma above Sivyer 2013 priors) motivate
adding a biological cost objective. Cytoplasm volume was chosen over alternatives (ATP/spike,
+-10% robustness) for cost reasons -- it adds zero per-evaluation overhead since it is a pure
geometric quantity computable from the morphology.

## Gating Dependency

**This task must not start until `t0120_morph_generator_geometry_audit` has been completed and
the geometry-audit verdict is "rendering-only / no re-runs needed".** If the audit reveals a
real geometry bug, this task should be cancelled and a framework-level decision is needed
about whether to patch `_apply_asymmetry` and re-run all 68-d morphology-extended NSGA-II
lineage tasks first.

## Scope

One NSGA-II run, single GA seed, 2 objectives, on the 68-d Bed B + 14-d morphology substrate
that has been validated by the t0106-t0115 lineage.

## Approach

1. **Copy the t0115 NSGA-II substrate** end-to-end: 68-d parameter vector (54-d electrophys +
   14-d morphology), pop=96, N_EVAL_SEEDS=3, 2 antipodal directions (PD=0deg, ND=180deg),
   ratio DSI, silence-guard tightened to >= 3 PD spikes, `_POOL_RESTART_EVERY=10`, HV-plateau
   auto-stop DISABLED, $8 hard cap.
2. **Replace one objective**: drop the PD-rate objective from t0106's 2-objective
   configuration and replace with **cytoplasm volume**, computed as: `vol = sum(pi *
   (sec.diam/2)^2 * sec.L for sec in [soma, *all_dends, ais_proximal, ais_distal])`. Units:
   um^3. Objectives become (maximise DSI, minimise cytoplasm volume). PD-rate stays as a
   tracked diagnostic but is not an optimiser objective.
3. **GA seed**: draw via `secrets.randbelow(10000)` (avoid round-ish numbers; follow the t0113
   convention).
4. **Gen ceiling**: 60 (per the t0114/t0115 convention for auto-stop-disabled runs).
5. **Stop trigger**: operator stop when HV trajectory visibly plateaus, OR $8 cost cap, OR gen
   60 ceiling.
6. **Run on Vast.ai EPYC** (32-core or 64-core, whichever is cheapest at provisioning time);
   single-instance.
7. **Post-run analysis**: Pareto front in (DSI, cytoplasm_volume) space, joint-pass cells (DSI
   > = 0.5 AND PD-rate >= 30 Hz AND cytoplasm_volume <= TBD), per-cell morphology gallery for top
   > ranks, **Cuntz 2010 balancing-factor check**: compute `bf` for top-10 cells and verify whether
   > the high-DSI corner falls in the predicted `[0.2, 0.7]` band.
8. **Answer asset**: write one answer asset answering "Does NSGA-II with a cytoplasm-volume
   cost objective produce a high-DSI front in Cuntz 2010's predicted balancing-factor `[0.2,
   0.7]` band?"

## Expected Outputs

* `assets/predictions/nsga2-cytoplasm-volume-bedb-morph/` -- predictions asset per spec, with
  per-cell 68-d vector + per-objective + per-direction firing.
* `assets/answer/cuntz-balancing-factor-prediction-check/` -- 1 answer asset on the Cuntz
  prediction.
* `results/data/pareto_front_seed*.json` -- Pareto front cells in (DSI, cytoplasm_volume).
* `results/data/all_evaluations_seed*.json` -- every evaluation.
* `results/images/pareto_front_dsi_vs_volume.png` -- Pareto front chart.
* `results/images/top50_morphologies_seed*.png` -- top-50 morphology grid (full dendrite trees
  per the project default).
* `results/images/cuntz_balancing_factor_top10.png` -- bf distribution for top-10 cells with
  Cuntz [0.2, 0.7] band overlaid.
* `results/results_summary.md`, `results/results_detailed.md`, `results/compare_literature.md`
  comparing to Hay 2011 / Cuntz 2010 / Mohacsi 2024.

## Budget

* Cost cap: **$8** (per-task default).
* Expected: ~$4-8 (one Vast.ai EPYC instance for 6-12 hours).
* If the run exceeds $8 watchdog trip, stop and write up partial results.

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` -- canonical Bed B cell.
* `t0080_bedb_mobo_v3_dendritic_spike_nsga2` -- 54-d electrophys parameter scheme +
  apply_params.
* `t0090_morphology_generator_diversity_test` -- procedural morphology generator.
* `t0092_diagnose_morphology_generator_silence` -- `generate_fixed_morphology` wrapper.
* `t0106_long_pdnd_nsga2_300gen` -- NSGA-II driver substrate (parent of the lineage).
* `t0115_seed9354_no_autostop` -- most recent run conventions to copy from.
* `t0119_brainstorm_results_23` -- commissions this task.
* **`t0120_morph_generator_geometry_audit` -- GATING DEPENDENCY**.

## Verification Criteria

* `t0120` verdict is "rendering-only / no re-runs needed" before this task starts.
* Predictions asset passes `verify_predictions_asset`.
* `metrics.json` registers `direction_selectivity_index` with explicit variants for
  `best_legit`, `overall_max`, `dsi_eq_one_count`.
* Cytoplasm volume formula is documented in `results_detailed.md` with per-section breakdown.
* Cuntz 2010 balancing-factor test result is reported as either "consistent with [0.2, 0.7]
  band" or "violates band".
* `compare_literature.md` includes a row comparing top-cell `bf` distribution to Cuntz 2010.

## Cross-References

* Source suggestion: S-0097-01.
* Source paper: Cuntz et al. 2010 -- 10.1371/journal.pcbi.1002107.
* Related project answer: t0097
  `assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation`.
* Prior lineage: t0106, t0112, t0113, t0114, t0115.

</details>

<details>
<summary>⏹ 0121 — <strong>Canonical 5-seed substrate-rate report (S-0112-01 batch
closed)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0121_5seed_substrate_rate_canonical_report` |
| **Status** | not_started |
| **Effective date** | 2026-05-23 |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0119_brainstorm_results_23`](../../../overview/tasks/task_pages/t0119_brainstorm_results_23.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0115-02` |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [Canonical 5-seed substrate-rate report (S-0112-01 batch closed)](../../../overview/tasks/task_pages/t0121_5seed_substrate_rate_canonical_report.md) |
| **Task folder** | [`t0121_5seed_substrate_rate_canonical_report/`](../../../tasks/t0121_5seed_substrate_rate_canonical_report/) |

# Canonical 5-seed Substrate-Rate Report (S-0112-01 batch closed)

## Source Suggestion

S-0115-02: "5-seed substrate-rate batch (S-0112-01) is now complete; write canonical report."

## Motivation

The S-0112-01 substrate-rate confirmation batch closed with t0115 (seed 9354). The 5 GA seeds
(44, 77, 2247, 7755, 9354) on the 68-d Bed B + 14-d morphology substrate produced LEGIT
joint-pass acceptance rates of 3.23%, 0.35%, 0.00%, 8.13%, 1.19% respectively. The 5-seed mean
is 2.58% +/- SE 1.50%, with a 95% CI of (-0.36%, +5.52%) that still brackets both Hay 2011's
0.40% envelope upper bound and Druckmann 2007's 0.10% baseline -- but 3 of 5 seeds
individually beat Hay's envelope, and the point estimate is 6.5x above Hay and 25.8x above
Druckmann.

The data lives in five separate task folders with slightly different reporting conventions
(t0106 reported on a $25 cap; t0112 used a $25 cap; t0113/t0114/t0115 used auto-stop disabled;
t0106 used auto-stop enabled). A single canonical document with harmonised metric conventions
is needed before this finding can be referenced by downstream tasks or external write-ups.

## Scope

Pure write-up. No new simulation, no new NSGA-II runs. Re-read the 5 source tasks' results
parquets and produce one consolidated canonical document plus one answer asset.

## Approach

1. **Re-read source data**: load each of the 5 tasks' `results/data/pareto_front_seed*.json`
   (or equivalent) and `all_evaluations_seed*.json` if available. Verify total evaluation
   counts match the per-seed reports (3744, 2016, 1344, 5952, 5280).
2. **Harmonise conventions**: re-compute LEGIT joint-pass count per seed using the canonical
   definition (DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999). Cross-check against each
   task's reported number; flag and document any discrepancies.
3. **Compute 5-seed statistics**: per-seed acceptance rate, 5-seed mean, sample SD, sample SE,
   95% CI (normal approx), 95% CI (bootstrap with B=10000), and counts of seeds beating Hay
   envelope.
4. **Comparison table**: harmonise with Hay 2011's 0.40% upper envelope and 0.0104%
   perisomatic bottleneck, and with Druckmann 2007's 0.10% baseline.
5. **Per-seed convergence-trajectory comparison**: HV trajectory, plateau generation, total
   evaluations, wall-clock per generation.
6. **Charts**: (a) per-seed acceptance rate bar chart with Hay/Druckmann reference lines, (b)
   5-seed HV-trajectory overlay (one trace per seed), (c) DSI-vs-PD scatter for the pooled
   LEGIT joint-pass cells colored by seed.
7. **Answer asset**: write one answer asset answering "What is the LEGIT joint-pass acceptance
   rate on the 68-d Bed B + 14-d morphology substrate, estimated from a 5-seed random-init
   NSGA-II batch, and how does it compare to Hay 2011 and Druckmann 2007?"

## Expected Outputs

* `results/data/per_seed_substrate_rate_5seed.csv` -- one row per seed with all relevant
  statistics.
* `results/data/pooled_legit_jointpass_cells.parquet` -- pooled LEGIT joint-pass cells across
  the 5 seeds (DSI, PD, source-seed, generation, cell_id).
* `results/images/per_seed_acceptance_bar.png` -- per-seed acceptance bar chart.
* `results/images/hv_trajectory_5seed_overlay.png` -- 5-seed HV-trajectory overlay.
* `results/images/dsi_pd_scatter_5seed_pooled.png` -- pooled scatter colored by seed.
* `assets/answer/substrate-rate-5seed-canonical/` -- 1 answer asset.
* `results/results_summary.md` and `results/results_detailed.md` with the canonical numbers.

## Budget

Local CPU only, no remote machines. Estimate <$0.20.

## Dependencies

* `t0106_long_pdnd_nsga2_300gen` -- seed 44.
* `t0112_t0106_seed77_replicate` -- seed 77.
* `t0113_t0106_seed2247_replicate` -- seed 2247.
* `t0114_seed7755_no_autostop` -- seed 7755.
* `t0115_seed9354_no_autostop` -- seed 9354.
* `t0119_brainstorm_results_23` -- commissions this task.

## Verification Criteria

* All 5 per-seed acceptance rates match the source task reports within rounding.
* 5-seed mean and SE match the brainstorm-session-23 summary (2.58% +/- 1.50%) within
  rounding.
* Charts saved and embedded in `results_detailed.md`.
* Answer asset passes `verify_answer_asset` (or local fallback).

## Cross-References

* Source suggestion: S-0115-02.
* Source tasks: t0106, t0112, t0113, t0114, t0115.
* Hay 2011 -- 10.1371/journal.pcbi.1002107 (or t0114 `compare_literature.md` for citation).
* Druckmann 2007 -- as cited in t0114 `compare_literature.md`.

</details>

<details>
<summary>⏹ 0075 — <strong>Biologically-realistic AIS one-axis-at-a-time parameter
sweep on Bed A</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0075_bio_realistic_ais_param_sweep` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0069-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A](../../../overview/tasks/task_pages/t0075_bio_realistic_ais_param_sweep.md) |
| **Task folder** | [`t0075_bio_realistic_ais_param_sweep/`](../../../tasks/t0075_bio_realistic_ais_param_sweep/) |

# Biologically-Realistic AIS Parameter Sweep on Bed A

## Motivation

t0069 attached a virtual AIS plus 1 mm axon stub to Bed A (deposited Poleg-Polsky DSGC) and
re-ran the t0067 channel-addition sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the AIS
instead of the soma. The sweep falsified S-0067-03's prediction (AIS-localised channels show
*larger* DSI effects than soma-localised) — it actually showed the opposite, with 11 of 15
channel conditions producing zero detectable DSI change. The cause was identified clearly: the
AIS+axon halved baseline PD firing (14.2 → 6.4 spikes) and silenced ND firing (1.6 → 0.0),
pushing baseline DSI to the trivial computational ceiling 1.0. The passive AIS+axon adds an
electrical sink that quenches the cell rather than relocating spike initiation; AIS-localised
channels at our densities cannot overcome the somatic 400 mS/cm² HHst Na drive.

The follow-up question this task answers: is there *any* DSGC + AIS configuration that
simultaneously contains all the channels biologically present in a vertebrate AIS (HHst basal
Na+K, Nav1.6, Kv3, Kv7 — the canonical RGC AIS quartet) and produces non-trivial DSI at a
biologically reasonable peak rate? "Decent DSI, not 1, and reasonable firing rate" maps to the
operational pass band {DSI in [0.3, 0.95], peak Hz in [5, 50]}. The right tool is not
optimisation — it is one axis at a time. NaP is excluded from the AIS channel set on two
grounds: (a) AIS NaP expression in RGCs is controversial; (b) the t0067 NaP-high finding (DSI
sign flip) suggests NaP destabilises the DSI mechanism rather than supporting it. BK and SK
are excluded because they localise primarily to soma and dendrites in RGCs, not to the AIS.

This task addresses RQ1 (somatic + AIS VGC combinations) and RQ4 (active vs passive
components). Source suggestions covered: S-0068-04 (move Nav1.6 + Kv3 to AIS), S-0069-01
(halve somatic gnabar before AIS), S-0069-02 (shrink AIS diameter to 0.5 micrometre),
S-0069-03 (vary axon length to probe sink), S-0069-04 (Nav1.6 + Kv3 on AIS at biological
densities).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC) plus virtual AIS + axon stub.
* AIS channel set: **{HHst basal Na + K, Nav1.6, Kv3, Kv7}**. NaP, BK, SK explicitly excluded.
* Encoding: 12-angle bar-rotation protocol (same as t0074 — cross-task comparable).
* Two-stage design: Stage 1 baseline calibration; Stage 2 per-axis sweep.

### Stage 1 — Baseline calibration

* Literature-informed AIS configuration (Wang et al. 2011, Carter et al. 2008 on mouse RGC
  AIS): AIS diameter 0.8 micrometre, AIS length 30 micrometre, axon stub 1.0 mm, AIS
  gnabar_HHst 4 0 0 mS/cm^2, AIS Nav1.6 medium density (~0.3 S/cm^2 from t0067 medium), AIS
  Kv3 medium density (~0.3 S/cm^2), AIS Kv7 low density (~0.1 S/cm^2; distal AIS, weaker than
  Nav and Kv3).
* Sweep soma `gnabar_HHst` across 6 candidates: {100, 150, 200, 250, 300, 400} mS/cm^2 (the
  t0069 baseline = 400).
* 6 candidates x 12 angles x 1 seed = 72 trials, ~5 min wall-clock.
* Pick the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If multiple
  candidates qualify, pick the one closest to the centre of the band ({peak ~ 20 Hz, DSI ~
  0.6}).
* If no candidate qualifies, the task halts at Stage 1 and reports a negative result with a
  recommendation for a follow-up that loosens the AIS configuration further (e.g., reduce AIS
  Nav1.6 density first, then re-attempt).

### Stage 2 — Per-axis sweep

From the Stage-1 baseline, vary one parameter at a time with all others held at baseline:

| # | Axis | Values | Non-baseline points |
| --- | --- | --- | --- |
| 1 | Soma `gnabar_HHst` (mS / cm^2) | {100, 200, 300, 400} | 3 |
| 2 | AIS `gnabar_HHst` (mS / cm^2) | {0, 100, 200, 400, 800} | 4 |
| 3 | AIS diameter (micrometre) | {0.4, 0.6, 0.8, 1.0, 1.5} | 4 |
| 4 | AIS length (micrometre) | {15, 30, 45, 60} | 3 |
| 5 | AIS Nav1.6 density | {0, low, medium, high} | 3 |
| 6 | AIS Kv3 density | {0, low, medium, high} | 3 |
| 7 | AIS Kv7 density | {0, low, medium, high} | 3 |
| 8 | Axon length (mm) | {0.1, 0.5, 1.0, 2.0} | 3 |

Total Stage-2 conditions: 1 baseline + 26 non-baseline = **27 conditions x 12 angles x 5 seeds
= 1620 FULL trials**, ~100 min wall-clock at the t0067 measured ~3.75 s / trial under CVODE.

### Width metrics per axis (cross-comparable with t0074)

For each condition, compute:

* **HWHM** in degrees from the 12-angle tuning curve.
* **Vector-sum DSI** (circular concentration).
* **Peak rate (Hz)** at the angle with maximum mean rate.
* Rate at PD (axis-1 peak angle) and at the opposite angle.
* RMSE vs the t0004 cosine target.

### Outputs

* **Library asset**: `bed_a_with_bio_realistic_ais` — Bed A + AIS + axon model variant with
  the {HHst, Nav1.6, Kv3, Kv7} channel set wired in. Reusable by future tasks that need a
  working DSGC + AIS substrate.
* **Stage 1 candidate table** (`results/baseline_candidates.csv`) with 6 rows showing
  soma_gnabar_HHst, peak Hz, DSI, in-band y/n.
* **Stage 2 per-axis sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI,
  peak rate, RMSE vs cosine target, plotted against axis values.
* **Biologically-plausible AIS recommendation table**
  (`results/biological_ais_recommendation.md`): the band-constrained range for each axis (the
  values that keep the cell inside {DSI [0.3, 0.95], peak [5, 50] Hz}), plus a recommended
  canonical configuration.
* `results/metrics.json` with registered project metrics per condition.

## Approach

1. Fork t0069's AIS-attachment code into this task's `code/`. Replace the t0069
   channel-addition loop with the {HHst, Nav1.6, Kv3, Kv7} baseline channel set (with
   t0074-vendored Kv7).
2. Implement Stage 1 calibration as a 6-candidate sweep with explicit pass-band check and
   automated baseline selection.
3. Implement Stage 2 as 8 per-axis sweep functions sharing a common driver.
4. Run Stage 1, log selected baseline, run Stage 2.
5. Compute width metrics, generate per-axis plots, write the recommendation table.
6. Validate against t0069 sanity checks: trials with instability flags = 0, peak Vm bounded.

## Pass Criteria

* Stage 1 finds at least one in-band baseline (peak Hz in [5, 50] AND DSI in [0.3, 0.95]).
* All 1620 + 72 trials complete with no instability flags.
* Per-axis sensitivity plots show monotonic or unimodal sensitivity for at least 6 of the 8
  axes (the axes that don't are flagged as candidates for re-investigation; not a hard fail).
* Recommendation table produced with the band-constrained range for each axis.

## Compute Estimate

* ~2 h wall-clock on local CPU. 72 trials Stage 1 (~5 min) + 1620 trials Stage 2 (~100 min) +
  ~10 min plotting / metrics extraction.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code (Nav1.6, Kv3
  implementation patterns).
* `t0069_t0067_ais_localised_channel_sweep` — AIS attachment code; baseline characterisation
  of the passive-AIS sink effect.
* `t0074_channel_tuning_width_bed_a` — Kv7 MOD vendoring lands in t0074. This task inherits
  the vendored Kv7 mechanism and the calcium-pool unification (the latter is not actively used
  here but must remain compatible).

## Risks and Fallbacks

* **Stage 1 finds no in-band baseline**: the task halts after Stage 1 and reports a negative
  result with a follow-up recommendation. Time-cheap (~5 min). The follow-up would probably be
  a 2D Stage 1.5 sweep over {soma gnabar, AIS gnabar} or a baseline that further reduces AIS
  Nav1.6 density.
* **Stage 1 is over-fitted to soma_gnabar**: if the baseline soma_gnabar value is borderline
  (e.g., exactly at the edge of the in-band region), small parameter changes in Stage 2 may
  push the cell out of band rapidly. Mitigation: pick the Stage-1 baseline closest to the band
  centre, not the band edge.
* **Axes interact strongly**: the one-axis-at-a-time design assumes weak interactions. If a
  Stage-2 axis sweep produces non-monotonic behaviour (e.g., DSI rises then falls), report the
  non-monotonicity explicitly and flag the axis for a future joint sweep with one neighbouring
  axis.
* **AIS+axon discretisation artefacts**: if the segment count along the AIS or axon is too
  low, spike initiation and propagation may be artefactual. Mitigation: use NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) and validate that the
  chosen segment count doubles without changing peak Vm by more than 1 mV at the t0069
  baseline.

## Out of Scope

* Bed B (de Rosenroll) — explicitly out of scope per researcher decision; this task is Bed A
  only.
* Joint multi-axis optimisation — explicitly excluded; this is one-axis-at-a-time only.
* Other AIS channel candidates (Nav1.2, Kv1, Kv4 alpha-DTX-sensitive subtype) — out of scope;
  the channel set is fixed at {HHst, Nav1.6, Kv3, Kv7}. Future follow-ups may extend the
  channel set.

</details>

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
