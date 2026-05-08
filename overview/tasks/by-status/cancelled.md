# ❌ Tasks: Cancelled

5 tasks. ❌ **5 cancelled**.

[Back to all tasks](../README.md)

---

## ❌ Cancelled

<details>
<summary>❌ 0042 — <strong>Fine-grained null-GABA ladder (3.5, 3.0, 2.5 nS) on
t0022</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0042_fine_grained_null_gaba_ladder_t0022` |
| **Status** | cancelled |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Fine-grained null-GABA ladder (3.5, 3.0, 2.5 nS) on t0022](../../../overview/tasks/task_pages/t0042_fine_grained_null_gaba_ladder_t0022.md) |
| **Task folder** | [`t0042_fine_grained_null_gaba_ladder_t0022/`](../../../tasks/t0042_fine_grained_null_gaba_ladder_t0022/) |

# Fine-Grained Null-GABA Ladder on t0022

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact**. The researcher has
paused all t0022-substrate modification tasks until the faithful ModelDB 189347 reproduction
establishes whether the observed DSI and peak-rate values in t0022 reflect genuine mechanism
gaps (justifying this task) or accumulated deviations from Poleg-Polsky 2016 (making this
task's target irrelevant). Reassess after t0046 merges.

## Motivation

t0037 swept null-GABA at {0, 0.5, 1, 2, 4} nS on t0022 and identified a sweet spot at 4 nS
(primary DSI 0.429, preferred direction 40.8 deg, matching Park 2014's in vivo band
0.40–0.60). Below 2 nS the cell over-excites and preferred direction randomises. t0039 then
showed that at GABA = 4 nS the t0022 diameter axis produces a monotonic DSI decline (slope
-0.034, p=0.008) — passive-filtering rather than Schachter 2010 active amplification.

What t0037 did not probe is the interval between 2 and 4 nS. Brainstorm session 8 requested a
fine-grained ladder at {3.5, 3.0, 2.5} nS to answer: does t0022 admit a GABA level below 4 nS
where DSI exceeds 0.5 without destabilising preferred direction? This directly informs whether
t0022 is usable as an optimisation substrate above its current 0.429 ceiling.

## Objective

Run the t0037 protocol (12 directions × 10 trials per direction, baseline diameter, V_rest =
-60 mV) at three additional null-GABA levels: 3.5 nS, 3.0 nS, 2.5 nS. Report primary DSI,
vector-sum DSI, preferred direction, peak firing rate, and null firing rate at each level.
Compare against t0037's 4 nS and 2 nS anchors.

Pass criterion: at any of the three new levels, primary DSI >= 0.50 AND preferred direction
stability across trials under 10 deg standard deviation. If pass, that GABA level becomes a
candidate new base parameter for t0022 optimisation; emit a suggestion for a follow-up
correction task (analogous to t0038) to propagate the new base into t0033.

Fail criterion: all three new levels yield DSI < 0.50 or preferred-direction standard
deviation
> 10 deg. If fail, report that 4 nS is the effective t0022 ceiling and recommend the t0033 optimiser
> switch substrates to t0024 per S-0034-07.

## Scope

* Local CPU only. No remote compute. ~1 hour total wall-clock.
* Reuse the t0037 trial_runner with only the null-GABA parameter changed; no code changes to
  the testbed.
* Produce tuning curves (Cartesian and polar) at each GABA level.

## Out of Scope

* Morphology sweeps (covered by t0039 at 4 nS).
* Channel-inventory modifications (covered by t0043).
* Schachter re-test (covered by t0044).

## Deliverables

* Per-GABA-level tuning-curve CSV + polar plot under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections,
  explicit Pass/Fail verdict against the criterion above.
* `results/metrics.json` with primary DSI, vector-sum DSI, preferred direction (mean and sd),
  peak Hz, and null Hz at each of the three new GABA levels, plus the two t0037 anchors.
* If Pass: one new suggestion in `results/suggestions.json` proposing a correction task to set
  the new GABA base value in t0033.

## Anticipated Risks

* Narrow sampling (three points) may miss a non-monotonic optimum between 2 and 4 nS; if
  results look non-monotonic, emit a follow-up suggestion for a denser sweep rather than
  extrapolating.
* If the cell destabilises at 2.5 nS or 3.0 nS, record the destabilisation metrics (preferred
  direction sd, coefficient of variation of peak rate) rather than treating those runs as
  failures.

</details>

<details>
<summary>❌ 0043 — <strong>Nav1.6 + Kv3 + NMDA restoration on t0022 channel
testbed</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0043_nav16_kv3_nmda_restoration_t0022` |
| **Status** | cancelled |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0019-03` |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Nav1.6 + Kv3 + NMDA restoration on t0022 channel testbed](../../../overview/tasks/task_pages/t0043_nav16_kv3_nmda_restoration_t0022.md) |
| **Task folder** | [`t0043_nav16_kv3_nmda_restoration_t0022/`](../../../tasks/t0043_nav16_kv3_nmda_restoration_t0022/) |

# Nav1.6 + Kv3 + NMDA Restoration on t0022

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact**. This task proposes
channel inventory modifications beyond Poleg-Polsky 2016's original model to close the
observed peak-rate gap (15 Hz vs paper's 40-80 Hz range). If t0046 shows the peak-rate gap is
inherent to the faithful reproduction of the paper (present in their code too), this task's
motivation evaporates and the gap must be addressed differently (stimulus duration, drive
amplitude, paper claim re-interpretation). If t0046 matches the paper's firing rates, then our
prior modifications introduced the gap and this task's channel-additions become a well-founded
fix. Reassess after t0046 merges.

## Source Suggestion

S-0019-03 primary (implement Nav1.6 / Nav1.2 / Kv1 / Kv3 channels with AIS-specific
densities). This task covers the Nav1.6 and Kv3 portion of S-0019-03. It also partially covers
S-0018-03 (NMDA restoration) and S-0022-02 (Nav1.6 distal-AIS density).

## Motivation

The cross-task audit in brainstorm session 8 (see
`tasks/t0040_brainstorm_results_8/results/test_vs_literature_table.md`) identifies peak firing
rate as the most universal mismatch: 15 Hz across t0022 baseline and every t0022-based sweep,
vs 30–150 Hz in every cited published source (Oesch 2005: 148 Hz; Chen 2009: 166 Hz; Sivyer
2013: 80–150 Hz). The likely causes stack: (a) t0022 uses lumped HHst which lacks Nav1.6
persistent Na current and Kv3 fast repolarisation, both of which are needed for high-frequency
AP firing; (b) the t0022 E-I schedule zeros NMDA at both PD and ND BIPs, removing the expected
NMDA-mediated gain boost; (c) AMPA-only drive caps the effective depolarisation.

The audit also shows that Schachter 2010's predicted active-amplification diameter signature
is absent on every diameter sweep we have run (t0030, t0035, t0039). One candidate explanation
is that without Nav1.6 / Kv3 in the distal dendrite, the regenerative threshold-crossing
regime Schachter 2010 relies on cannot be recruited.

This task restores the channel inventory and NMDA drive so the peak-rate mismatch can be
attacked, and so the Schachter re-test in t0044 runs against a model that matches published
DSGC channel priors.

## Objective

Produce a new library asset (tentatively `modeldb_189347_dsgc_t0043` or similar) that is a
fork of the t0022 testbed with three modifications:

1. Nav1.6 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~8
   mS/cm^2 (per t0019's cited DSGC priors). If a Nav1.6 MOD file is not already available,
   adapt one from the t0019 channel corpus.
2. Kv3 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~5
   mS/cm^2.
3. NMDA synapse component restored at both PD and ND BIP terminals with conductance matching
   the Poleg-Polsky 2016 parameter backbone (read from t0008's library asset if available,
   else sourced from the Poleg-Polsky 2016 paper).

Hold the t0037 null-GABA sweet spot of 4 nS as the base parameter per t0038's correction. Keep
the 12-direction × 10-trial sweep protocol identical to t0022 / t0037 / t0039 so results are
directly comparable.

Pass criterion (both must hold):

* Peak firing rate in [40, 80] Hz at V_rest = -60 mV.
* Primary DSI within +/- 0.1 of the t0037 anchor of 0.429 at the 1.0x baseline diameter.

## Scope

* Local CPU only. No remote compute. ~6 hours wall-clock including MOD recompilation.
* Produce a library asset with the modified model plus a baseline 12-direction x 10-trial
  sweep at V_rest = -60 mV, GABA = 4 nS.
* Write a test harness that can be reused by t0044 for the diameter sweep.

## Out of Scope

* Nav1.2 and Kv1 (part of the fuller S-0019-03 scope, deferred).
* Morphology sweeps (covered by t0044 which uses this task's output as substrate).
* V_rest sweep (covered by t0026 on the prior testbed; a re-run on the new testbed could be a
  follow-up suggestion emitted from this task).

## Deliverables

* `assets/library/modeldb_189347_dsgc_t0043/` — library asset with the modified model,
  compiled MOD files, and baseline sweep driver.
* Baseline 12-direction x 10-trial sweep CSV under `results/`.
* Tuning curve (Cartesian and polar) under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections
  and an explicit Pass/Fail verdict against both criteria above.
* `results/metrics.json` with baseline primary DSI, vector-sum DSI, preferred direction, peak
  Hz, null Hz, and a boolean `peak_rate_pass` and `dsi_preserved_pass`.
* If Pass: the library asset is fit for use as t0044's substrate. If Fail: emit a suggestion
  for a follow-up calibration task (BIP burst rate + AMPA scale; see S-0040-01 or analogous)
  and stop before t0044.

## Anticipated Risks

* Nav1.6 MOD files in the t0019 corpus may not compile under NEURON 8.2.7 without adaptation;
  budget time for MOD debugging.
* Adding Nav1.6 may push the cell into runaway firing if the Kv3 density is too low; tune Kv3
  first, Nav1.6 second.
* Restoring NMDA may break the t0037 4 nS sweet spot by over-exciting at the null direction;
  if this happens, emit a follow-up suggestion to repeat a GABA sweet-spot search on the new
  testbed.

</details>

<details>
<summary>❌ 0044 — <strong>Schachter 2010 re-test via 7-diameter sweep on t0043 at
GABA = 4 nS</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0044_schachter_retest_on_t0043` |
| **Status** | cancelled |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0043_nav16_kv3_nmda_restoration_t0022`](../../../overview/tasks/task_pages/t0043_nav16_kv3_nmda_restoration_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0002-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Schachter 2010 re-test via 7-diameter sweep on t0043 at GABA = 4 nS](../../../overview/tasks/task_pages/t0044_schachter_retest_on_t0043.md) |
| **Task folder** | [`t0044_schachter_retest_on_t0043/`](../../../tasks/t0044_schachter_retest_on_t0043/) |

# Schachter 2010 Re-Test on t0043 Substrate

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact** and of this task's
upstream dependency **t0043** (which is itself blocked on t0046). This task depends on the
t0043 substrate. Reassess after t0046 merges and t0043's block is reviewed.

## Source Suggestion

S-0002-02 (paired active-vs-passive dendrite experiment to reproduce Schachter 2010 DSI gain
~0.3 -> ~0.7).

## Motivation

Three independent diameter sweeps across two testbeds have failed to show Schachter 2010's
predicted active-amplification signature:

* t0030 on t0022 at GABA = 12 nS: slope +0.008 (p=0.177), DSI pinned at 1.000 (deterministic
  schedule saturates the metric).
* t0035 on t0024 (AR(2) stochastic) at paper-default GABA: slope +0.004 (p=0.88), flat.
* t0039 on t0022 at GABA = 4 nS (t0037 sweet spot): slope -0.034 (p=0.008), monotonic decline
  consistent with passive filtering rather than the predicted concave-down interior peak.

One candidate explanation, surfaced in brainstorm session 8's cross-task audit, is that lumped
HHst lacks the distal Nav1.6 and Kv3 channels needed to recruit the regenerative
threshold-crossing regime Schachter 2010 relies on. t0043 fixes that inventory and restores
NMDA. If Schachter 2010 is correct and our previous null results were confounded by the
channel gap, the same 7-diameter sweep on the t0043 substrate should show a concave-down
DSI-vs-diameter curve with a significant negative quadratic coefficient.

If the curve is still monotonic after t0043, we can close the Schachter 2010 hypothesis on the
Poleg-Polsky-derived morphology and commit to a passive-filtering framing for the t0033
optimiser.

## Objective

Run a 7-diameter distal-section sweep (multipliers 0.5, 0.67, 0.85, 1.0, 1.2, 1.5, 2.0 — same
grid as t0030, t0039, t0035) on the t0043 library asset at GABA = 4 nS. Protocol matches
t0039: 12 directions x 10 trials per direction per multiplier, V_rest = -60 mV. Primary
outcome is the DSI-vs-diameter curve shape; fit both linear and quadratic models and report
the coefficients with p-values.

Pass criterion (Schachter 2010 signature recovered):

* Quadratic fit coefficient significantly negative (p < 0.05) with a peak at an interior
  multiplier (between 0.6 and 1.5).

Fail criterion (Schachter hypothesis rejected on Poleg-Polsky morphology):

* Monotonic (linear fit significant, quadratic not significant), or no significant trend. In
  this case, emit a suggestion to formally close S-0002-02 and to add a clarifying note to the
  t0033 plan recommending the passive-filtering framing.

## Scope

* Local CPU only. No remote compute. ~8 hours wall-clock.
* Use the t0043 library asset. Do not modify the channel inventory; this is a pure morphology
  sweep.
* Keep per-trial stochasticity identical to t0039 so the results are directly comparable.

## Out of Scope

* Nav ablation (covered by S-0029-02, currently medium priority).
* Length-axis sweep on the t0043 substrate (possible follow-up, not this task).
* Re-running on t0024 (possible follow-up under S-0039-01).

## Deliverables

* 7-diameter tuning-curve CSVs under `results/`.
* Overlay plot of DSI-vs-diameter with linear and quadratic fits under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections
  and an explicit Schachter-recovered / Schachter-rejected verdict.
* `results/metrics.json` with the linear slope, quadratic coefficient, and their p-values,
  plus primary DSI, vector-sum DSI, and peak Hz at each multiplier.
* `results/compare_literature.md` explicitly comparing the recovered (or absent) curvature
  against Schachter 2010 and the passive-filtering prediction.

## Anticipated Risks

* If t0043 fails its own Pass criterion (peak rate or DSI preservation), do not proceed with
  this task; the substrate is not fit for use.
* Adding Nav1.6 may change the effective preferred direction; re-seed the E-I schedule only if
  the preferred direction has shifted by more than 30 deg from the t0037 40.8 deg anchor.
* Quadratic fits on 7 points are under-powered if noise is high; if the quadratic p-value is
  borderline (0.05 < p < 0.15), emit a suggestion for a denser 11-point sweep rather than
  declaring a verdict.

</details>

<details>
<summary>❌ 0045 — <strong>CoreNEURON Vast.ai RTX 4090 speedup benchmark</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0045_coreneuron_vastai_speedup_benchmark` |
| **Status** | cancelled |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0033-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`baseline-evaluation`](../../../meta/task_types/baseline-evaluation/) |
| **End time** | 2026-05-03T12:55:00Z |
| **Task page** | [CoreNEURON Vast.ai RTX 4090 speedup benchmark](../../../overview/tasks/task_pages/t0045_coreneuron_vastai_speedup_benchmark.md) |
| **Task folder** | [`t0045_coreneuron_vastai_speedup_benchmark/`](../../../tasks/t0045_coreneuron_vastai_speedup_benchmark/) |

# CoreNEURON Vast.ai RTX 4090 Speedup Benchmark

## Source Suggestion

S-0033-01 (CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the assumed 5x speedup
in the t0033 cost model).

## Motivation

The t0033 planning task estimated a $50.54 central Vast.ai budget for the future joint DSGC
morphology + top-10 VGC DSI-maximisation optimiser. That estimate rests on an unvalidated
CoreNEURON-on-GPU-over-stock-CPU-NEURON speedup factor of 5x (91 s deterministic sim on RTX
4090 vs 456 s on single CPU core). The corpus documents Hines 1997 O(N) cable-solver scaling
but predates GPU NEURON variants, so the 5x figure is a literature-less guess that drives the
largest sensitivity-band column ($23–$119 under 0.5x–2x perturbations).

Brainstorm session 8 (t0040) considered offloading t0041–t0044 to Vast.ai to cut wall-clock,
and rejected that plan because the per-task compute is small and the 5x speedup is
unvalidated. This task directly addresses the validation gap: run a short, well-scoped Vast.ai
experiment that replaces the 5x assumption with a measured value and tightens (or widens) the
$23–$119 sensitivity band before the joint optimiser is commissioned.

This also exercises the project's Vast.ai provisioning workflow for the first time (total
project spend to date: $0.00 / $1.00), surfacing any setup issues before the far more
expensive t0033 optimiser run.

## Objective

Provision one Vast.ai RTX 4090 instance under the existing `setup-remote-machine` filters.
Build CoreNEURON against NEURON 8.2.7 with OpenACC / CUDA. Run the t0022 deterministic
12-angle x 10-trial protocol (same sim used in t0022 baseline) under:

1. Stock NEURON on CPU (single core).
2. CoreNEURON on GPU (RTX 4090).

Report wall-clock per sim, throughput (sims/hour), measured speedup factor, cost per sim in
USD at RTX 4090 Vast.ai rate, and a recommended replacement value for t0033's 5x assumption.
Produce one answer asset capturing the measured speedup and its implications for the t0033
cost envelope.

## Scope

* One Vast.ai RTX 4090 instance. Estimated wall-clock 1–3 h; estimated cost $2–5 at $0.50/h.
* Use t0022's `trial_runner` unchanged; do not modify biophysics or protocol.
* Match stock-NEURON and CoreNEURON runs trial-for-trial for apples-to-apples comparison.
* Record provisioning time and setup friction separately so the t0033 plan can budget for it.

## Out of Scope

* Multi-GPU scaling (t0033 assumes single-GPU).
* A100 / H100 benchmarks (cost column in t0033 already recomputes from measured RTX 4090
  speedup).
* CPU-96 many-core benchmark (t0033 already recommends ignoring that column).
* Any morphology or channel modifications (pure runtime benchmark).

## Deliverables

* `assets/answer/coreneuron-rtx4090-speedup-vs-stock-neuron/` — full answer asset with
  measured speedup, per-sim cost, and recommended t0033 budget update.
* `results/results_summary.md` and `results/results_detailed.md` with Methodology, Metrics,
  Comparison vs Baselines (5x assumption), and Next Steps.
* `results/metrics.json` with: `stock_neuron_s_per_sim`, `coreneuron_s_per_sim`,
  `speedup_factor`, `coreneuron_usd_per_sim`, `provisioning_minutes`, `setup_minutes`.
* `results/compare_literature.md` comparing the measured speedup to Hines 1997 cable-solver
  scaling expectations and any CoreNEURON GPU benchmarks found in the corpus.
* `results/suggestions.json` with at minimum a follow-up proposing a correction to t0033's
  answer asset if the measured speedup differs from 5x by more than 20%.
* `results/costs.json` and `results/remote_machines_used.json` with the full Vast.ai
  provisioning record.

## Anticipated Risks

* **Vast.ai provisioning may fail or block on verification**: the project has never
  provisioned a Vast.ai instance; the `setup-remote-machine` skill may hit unexpected
  friction. Budget extra time for first-run troubleshooting and record every setup step for
  future tasks.
* **CoreNEURON build may require NEURON 8.2.7 patch or a newer version**: if CoreNEURON does
  not build cleanly against the project's NEURON version, document the workaround or flag the
  task as intervention_blocked rather than silently bumping the NEURON version.
* **Deterministic-reproducibility caveat**: stock NEURON on CPU and CoreNEURON on GPU may not
  produce bit-identical spike trains due to floating-point ordering differences; report the
  max-spike-time-deviation and any DSI delta explicitly so the t0033 optimiser knows whether
  GPU and CPU runs are substitutable.
* **Cost overrun**: hard-cap the instance runtime at 3 hours. If the benchmark cannot finish
  within the cap, post-mortem the provisioning and setup overhead and re-scope before a second
  attempt.

## Verification Criteria

* `measured_speedup_factor` is reported with both mean and 95% CI.
* `coreneuron_usd_per_sim` is reported at the actual Vast.ai instance rate at runtime (not the
  snapshot rate from t0033).
* At least one answer asset is produced per the answer specification.
* If the measured speedup differs from 5x by more than 20%, a correction-proposal suggestion
  is filed in `results/suggestions.json` against t0033's answer asset.

</details>

<details>
<summary>❌ 0096 — <strong>Literature survey: multi-objective optimisation of
single-neuron models</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0096_literature_survey_multi_objective_neuron_optimisation` |
| **Status** | cancelled |
| **Effective date** | 2026-05-08 |
| **Dependencies** | — |
| **Expected assets** | 10 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`internet-research`](../../../meta/task_types/internet-research/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-08T15:13:18Z |
| **End time** | 2026-05-08T15:30:00Z |
| **Task page** | [Literature survey: multi-objective optimisation of single-neuron models](../../../overview/tasks/task_pages/t0096_literature_survey_multi_objective_neuron_optimisation.md) |
| **Task folder** | [`t0096_literature_survey_multi_objective_neuron_optimisation/`](../../../tasks/t0096_literature_survey_multi_objective_neuron_optimisation/) |

# Literature Survey: Multi-Objective Optimisation of Single-Neuron Compartmental Models

## Motivation

The morphology + channel optimisation pipeline is now production-ready: t0091
(`morphology_extended_nsga2_v1`) is currently running the first joint 68-d NSGA-II (54-d
electrophys \+ 14-d morphology) on the t0092-patched procedural generator validated at scale
by t0093. Every multi-objective optimisation task this project has run so far (t0076, t0078,
t0080, t0081, t0083, t0086, t0091) has used the same two objectives: direction selectivity
index (DSI) and firing rate. That objective pair was the right choice for the project's
first-question ("which channels maximise DS?") phase, but it leaves the broader
multi-objective landscape unexplored.

The researcher's strategic directive (brainstorm session 20, 2026-05-08) is to broaden the
optimisation objective space:

> Now that we have working optimisation for both morphology and channel composition we can optimise
> for different things. Currently we optimise for DSI and firing rate. However I would like to
> compare results for all sorts of stuff. For example, I would like to optimise for DSI and
> information transfer rate; DSI and energy spent, DSI and minimisation of citoplasm volume etc.
> Perform an extensive literature search and find papers that use different forms of optimisation.
> It does not need to be DSGC but can be any neurons.

This task is the literature-research foundation for that broadening. It catalogues every
objective function used in the published multi-objective single-neuron optimisation
literature, delivers formulas + computational recipes for each, and produces a ranked list of
future MOBO tasks to commission once budget permits. The deliverable is intentionally
actionable: each catalogued objective must be implementable on top of the existing Bed B
NSGA-II loop without infrastructure rewrites.

The task is also the right test of biological plausibility as an optimisation criterion. The
researcher's recurring concern across this project has been that pure DSI maximisation admits
non-physical solutions; jointly optimising DSI vs energy, vs cytoplasm volume, or vs
robustness forces the optimiser into bio-realistic regions of the parameter space. The survey
should explicitly document, per objective, whether published work treats it as a biological
constraint or only as a performance proxy.

## Scope

### In Scope

* **Multi-objective methodology papers** covering single-neuron compartmental models:
  Druckmann et al. 2007 ("A novel multiple objective optimization framework for constraining
  conductance-based neuron models by experimental data"), Druckmann et al. 2011 (eFEL
  precursor), Achard & De Schutter 2006 (first MOEA Purkinje fits), Van Geit et al.
  (NeuroFitter / BluePyOpt), Rumbell et al. (cortical L5 PC MOBO), Hay et al. 2011 (BBP
  cortical L5 multi-objective).
* **Information-theoretic objective functions**: mutual information between stimulus and spike
  train (Bialek, De Ruyter van Steveninck, Strong et al.), Fisher information / discrimination
  capacity (Brunel, Nadal), channel capacity, stimulus-reconstruction MSE, spike-train metrics
  (Victor & Purpura, van Rossum).
* **Metabolic / energy objective functions**: ATP per spike, total ionic flux, Na+/K+ pump
  cost (Attwell & Laughlin 2001 "An energy budget for signaling in the grey matter of the
  brain"), bits-per-ATP energy efficiency (Niven & Laughlin 2008, Sengupta et al. 2010 "Action
  potential energy efficiency varies among neuron types in vertebrates and invertebrates").
* **Structural / wiring objective functions**: total dendritic length, total membrane area,
  cytoplasm / dendritic volume, wiring economy (Chklovskii et al., Cuntz, Forstner, Borst &
  Hausser 2010 "One rule to grow them all").
* **Robustness / degeneracy objective functions**: parameter-perturbation sensitivity, noise
  tolerance (Marder & Goaillard 2006 "Variability, compensation and homeostasis in neuron and
  network function"; Prinz, Bucher & Marder 2004 "Similar network activity from disparate
  circuit parameters").
* **Temporal / coding objective functions**: latency, jitter, spike-timing precision,
  bandwidth, dynamic range.
* **Methods / codebases**: BluePyOpt (Van Geit), NeuroFitter, NSGA-II + NSGA-III in pymoo,
  MOEA literature (Deb et al.), Pareto-front analysis methods (hypervolume, IGD, R2
  indicator).

### Out of Scope

* Network-level optimisation (multi-neuron). Stay on single-neuron compartmental models.
* Reinforcement-learning / deep-learning policy optimisation. Stay on classical MOBO / MOEA.
* Phenomenological integrate-and-fire models without compartmental structure (mention briefly
  if they yield reusable objectives, but do not deep-dive).

## Must-Find Objective Categories

The survey must deliver formula + units + NEURON-side computational recipe for at least one
representative objective in each of these four categories:

1. **Information transfer rate / mutual information** — between stimulus angle and spike-train
   output for our DSGC case. Concrete recipe must specify how to estimate MI from a
   t0091-style 8-direction trial output (e.g., binned spike counts per direction, direct
   method, or extrapolation method).

2. **Metabolic energy / ATP per spike** — computable from HH ionic currents in NEURON.
   Concrete recipe must specify which currents to integrate (Na+ influx, K+ efflux, leak) and
   the conversion factor from charge to ATP molecules (3 Na+ exchanged per ATP via Na+/K+
   ATPase).

3. **Cytoplasm volume / wiring cost** — computable directly from morphology. Concrete recipe:
   sum over compartments of pi * r^2 * L; or total surface area as an alternative; or wiring
   cost = sum of section lengths weighted by diameter.

4. **Robustness / degeneracy** — parameter-perturbation sensitivity of DSI; multi-conductance
   solution-space volume. Concrete recipe must specify a Marder-style protocol: e.g., +/- 10
   percent random perturbation of all channel densities and report DSI standard deviation as
   the objective.

If the literature search uncovers more well-defined objective categories not in this list, add
them to the catalogue and rank them by biological plausibility and computational feasibility.

## Approach

### Stage 1: Research Papers

Survey methodology and biological objective-function origin papers. Download canonical
citations for each objective category. Read full text where available; abstract +
supplementary info otherwise. Produce `research/research_papers.md` with:

* Per-objective subsection grouping the 2-3 canonical papers
* Per-paper extracted formula, units, computational recipe
* Notes on biological plausibility and how the objective would interact with DSI in a
  multi-objective setting

### Stage 2: Research Internet

Survey codebases, tutorials, review articles, and online resources for multi-objective
single-neuron optimisation. Targets: BluePyOpt (Van Geit, github.com/BlueBrain/BluePyOpt),
NeuroFitter, eFEL, pymoo NSGA-II + NSGA-III tutorials, Pareto-front diagnostic libraries
(pyDOE, paretoset). Document API surfaces and example usage that the project could adopt
without rewrites. Produce `research/research_internet.md`.

### Stage 3: Answer Asset

Synthesise findings into a single answer asset
`objective-functions-for-single-neuron-multi-objective-optimisation` (under `assets/answer/`).
Each catalogued objective gets a uniform record:

| Field | Content |
| --- | --- |
| Name | e.g. `mutual_information_stimulus_spike_train` |
| Mathematical formula | LaTeX |
| Units | e.g. bits per second, ATP per spike, um^3 |
| NEURON-side quantities required | Vm trace, ionic currents, spike times, morphology, etc. |
| Recipe | Step-by-step computation from a t0091-style 8-direction trial output |
| Biological plausibility | Notes on whether the objective is a hard biological constraint or a soft proxy |
| Direction-of-optimisation | Maximise / minimise / target value |
| Papers using it | At least 2 citations |

### Stage 4: Suggestions

Emit a ranked list of future MOBO tasks in `results/suggestions.json`. Each suggestion must
include:

* Title (e.g. "Bed B NSGA-II maximising DSI and ITR")
* Kind, priority
* Categories, source_paper if applicable
* Biological plausibility notes
* Budget feasibility estimate (Vast.ai EPYC + GPU hours)
* Cross-references to the catalogued objective entries

Suggestions must be ranked by combined biological-plausibility and budget-feasibility scores.
Aim for 3-6 ranked suggestions; do not pad.

## Cost Estimation

* **Total**: $0
* **Compute**: none. Local-only.
* **Paid services**: none.
* **Risk-of-going-over**: zero. The task is paper download + reading + writing.

## Step by Step

1. `init-folders`, `check-deps` (no deps to check).
2. Stage 1: research papers — download 10+ canonical papers; read; populate
   `research/research_papers.md`; create paper assets.
3. Stage 2: research internet — survey codebases, tutorials, review articles; populate
   `research/research_internet.md`.
4. Stage 3: answer asset — write the consolidated objective-function catalogue.
5. Stage 4: suggestions — write `results/suggestions.json` with the ranked future-MOBO list.
6. Reporting — write `results/results_summary.md` and `results/results_detailed.md`; run
   verificators; PR; merge.

## Remote Machines

None.

## Assets Needed

None. The task downloads its own paper assets.

## Expected Assets

* `paper`: at least 10 (covering methodology + four must-find categories)
* `answer`: 1 (the consolidated objective-function catalogue)

## Time Estimation

Approximately 2-4 hours wall-clock by an autonomous research agent. Roughly: 60-90 min paper
download + reading; 30-60 min internet survey + codebase review; 30-60 min answer asset
writing; 15-30 min suggestions + reporting + verification.

## Risks & Fallbacks

* **Paywalled paper not accessible** via Sci-Hub or institutional proxy: mark in
  `intervention/` and proceed with abstract + citation analysis. Do not block the task.
* **Cytoplasm volume has no direct precedent** in single-neuron optimisation literature: use
  the wiring-cost / total-length proxy and flag it as a novel objective contribution. The
  computational recipe is already trivial (sum over compartments of pi * r^2 * L) so the
  objective stays usable even without a published precedent.
* **Answer asset becomes too long** (>5000 words): split per category but keep one
  consolidated `short_answer.md` as the entry point. Each category subsection in
  `full_answer.md` may be a separate H2 section.
* **Literature search dilutes** because too many off-target papers come up: enforce the
  Out-of-Scope filter; prefer 2-3 canonical citations per category over comprehensive
  coverage.

## Verification Criteria

* All four must-find objective categories covered with formulas and computational recipes.
* At least 5 multi-objective compartmental-model methodology papers reviewed.
* At least 10 paper assets created and passing the paper asset verificator.
* Answer asset passes `meta/asset_types/answer/specification.md`.
* At least 3 ranked, budget-realistic future MOBO suggestions emitted in
  `results/suggestions.json`.
* All standard task verificators pass: `verify_task_file`, `verify_logs`,
  `verify_research_papers`, `verify_research_internet`, `verify_assets`, `verify_suggestions`,
  `verify_task_results`, `verify_pr_premerge`.

## Cross-References

* **t0091_morphology_extended_nsga2_v1** — current MOBO frontier (DSI + firing rate);
  catalogue's recipes must compose with t0091's trial-output format.
* **t0095_brainstorm_results_20** — commissioned this task.
* **t0002_literature_survey_dsgc_compartmental_models** — prior literature survey for
  stylistic consistency.
* **t0015 / t0016 / t0017 / t0018 / t0019 / t0027** — prior literature surveys for stylistic
  consistency and for any cross-cited references.

</details>
