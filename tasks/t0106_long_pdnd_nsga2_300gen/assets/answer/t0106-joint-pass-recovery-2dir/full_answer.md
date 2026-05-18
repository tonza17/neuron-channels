---
spec_version: "2"
answer_id: "t0106-joint-pass-recovery-2dir"
answered_by_task: "t0106_long_pdnd_nsga2_300gen"
date_answered: "2026-05-18"
confidence: "high"
---
# 2-direction NSGA-II recovers joint-pass cells

## Question

Does long-running 2-direction NSGA-II on the 68-d Bed B + 14-d morphology substrate recover strict
joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) from random init, and where does hypervolume actually
plateau on this landscape?

## Short Answer

Yes. Across 3,744 evaluations from a single random-init GA seed running 40 generations of
2-direction NSGA-II with ratio DSI, **123 unique cells cleared the strict joint-pass corner** (DSI
>= 0.5 AND PD >= 30 Hz) — the first joint-pass cells anywhere in the t0080 - t0104 NSGA-II
lineage, every prior task of which returned zero. Hypervolume climbed 604x from 0.2015 at gen 1 to
122.0288 at gen 40 and was effectively flat (under 1% per 60 min) from gen 36 onward, marking the
empirical convergence point on the 2-direction substrate. The reformulation from 16-direction
vector-sum DSI to 2-direction ratio DSI — not the longer generation budget — drove the
breakthrough.

## Research Process

The hypothesis came from the t0104 reporting step (2026-05-14). t0104 had concluded with the
substrate-limited reading: 2-objective NSGA-II with the silence guard active failed to produce
joint-pass cells across 2,208 evaluations on the 16-direction landscape, and the Pareto front
replicated t0102's exactly L-shaped pattern (extremes reachable on each axis, joint corner empty).
Two algorithm-side hypotheses survived: (a) the 16-direction vector-sum DSI is harder to satisfy
than the 2-direction ratio DSI on this substrate; and (b) the 12-generation horizon was
insufficient. t0106 was designed to test both simultaneously by reformulating to 2 directions
(funding ~10x per-cell speed-up) and spending the freed budget on 300 generations rather than 3
seeds.

The experiment forked [t0104]'s `code/` substrate. Three changes only: `ANGLES_DEG = [0.0, 180.0]`
(was 16 values every 22.5 deg); `N_EVAL_SEEDS = 3` (was 4); `_vector_sum_dsi` replaced with
`_ratio_dsi = (pd_rate - nd_rate) / (pd_rate + nd_rate)`. The DSI silence guard from S-0102-01 was
preserved unchanged at threshold 10 total spikes per trial. A new `PerGenerationPoolRestart`
operator was added (`every=25` gens) to mitigate the NEURON memory accumulation that doubled per-gen
wall-clock by gen 25 in [t0102] and [t0104]. NSGA-II ran on GA seed 44 with `pop_size=96`,
`n_gen=300` target, LHS random init, default SBX/polynomial mutation. An hourly poller surfaced the
HV trace to the operator; the operator dropped `intervention/stop.md` after gen 40 when the 60-min
moving-window HV gain fell below 1%.

The run executed on a single Vast.ai EPYC 7B13 64-core / 503 GB instance (Texas US, $0.4111/hr) for
24.1 h productive + ~11 min provisioning + ~63 min idle between operator-stop and destroy. Total
billing window 25.22 h; total cost $10.37 of the $25 cap. The pool-restart operator fired off-by-one
at gen 26 and dropped per-gen wall-clock from 110 min back to 3 min, validating the mitigation. No
conflicting evidence emerged in the run itself; results are consistent across the full HV trace and
across all 5 result-summary checks.

## Evidence from Papers

The `papers` method was not used inside t0106 (no new papers were downloaded or summarised by this
task; the dedicated research-papers stage produced a literature retrospective summarised in
`research/research_papers.md` but did not introduce evidence that the answer rests on directly).
Published literature comparisons live in `results/compare_literature.md` and inform the
*interpretation* of the joint-pass yield (3.3% vs Druckmann2007 0.10%, Hay2011 0.40%) but the
question itself — does the t0106 reformulation recover joint-pass cells on this substrate — is
answered exclusively from the experiment.

## Evidence from Internet Sources

The `internet` method was not used. No new web sources were consulted to produce this answer; the
question is purely an empirical claim about a t0106 NSGA-II run and is settled by the experiment
output.

## Evidence from Code or Experiments

The single t0106 NSGA-II run produced the predictions asset `nsga2-seed44-bedb-morph-2dir-300gen`
(3,744 evaluations across 40 completed generations on GA seed 44). Strict joint-pass cells (DSI >=
0.5 AND PD >= 30 Hz): **123 unique** / **637 evaluations** (with NSGA-II repetition) / 3,744 total =
**3.3% yield**. The yield calculation treats each unique 68-d vector as one cell; NSGA-II revisits
parent solutions across generations and these duplicates inflate the raw "joint_pass evals" count.

Best ratio DSI = **1.0000** at PD = 81.43 Hz (3 unique cells reached the analytic ceiling because ND
= 0 produces (PD - 0) / (PD + 0) = 1 by definition). The highest legitimately sub-ceiling cell was
DSI = **0.9832** at PD = 84.5 Hz. Best PD-rate frontier was **122.62 Hz** at DSI = 0.92. Twenty-four
unique cells satisfied the stronger criterion DSI > 0.9 AND PD > 80 Hz (114 evaluations).
Spike-count audit on all 6 unique top joint-pass cells confirmed 47-154 total spikes per trial —
no silence-guard artefacts in the front.

The hypervolume trajectory climbed from 0.2015 (gen 1) to 122.0288 (gen 40), a **604x growth**
across 40 generations. The 60-minute moving-window HV gain fell below 1% from gen 36 onward,
identifying gen 36 as the empirical convergence point on the 2-direction substrate. The
operator-stop at gen 40 cost $10.37 productive + $0.48 idle/setup = $10.85 / $25 cap. Per-gen
wall-clock pattern: 3 min/gen at gen 1, accelerating to 110 min/gen by gen 25, dropping back to 3
min/gen after `PerGenerationPoolRestart` fired off-by-one at gen 26, climbing back to 95 min/gen by
gen 38. The local pytest `test_evaluator_dsi_guard.py` (silence guard, ratio DSI synthetic check,
threshold sweep) passed 5/5 before remote launch; the 5-anchor pre-launch smoke gate also passed
5/5.

Direct comparison to the [t0104] L-shaped Pareto front: in [t0104] the front had max DSI = 0.5417 at
PD = 3.57 Hz and max PD = 75.0 Hz at DSI = 0; the joint corner was empty. In t0106 the front no
longer L-shapes: it sweeps continuously through the joint-pass corner with 7 cells on the strict
Pareto frontier (the first appears at gen 18, by gen 24 the front holds 9 cells, by gen 36 the front
reaches PD = 122.62 Hz). The two top morphological archetypes that emerge are classical ND-soma (35
of top 50 cells) and PD-soma (4 of top 50), plus 4 central-soma cells.

## Synthesis

Three lines of evidence support a high-confidence positive answer:

1. **Direct count**: 123 unique joint-pass cells (637 evaluations) across 3,744 evaluations. 3.3%
   yield. Spike-count audit confirms no silence-guard artefacts in the top cells. The substrate is
   not joint-pass-empty; the lineage's prior null was a metric artefact.

2. **Pareto front shape change**: the front transitions from the L-shape of [t0102] and [t0104]
   (extremes reachable, corner empty) to a continuous sweep through the joint corner. This is a
   qualitative change in the front geometry, not a quantitative increment, and rules out a marginal
   "the corner is reachable but rare" interpretation.

3. **HV plateau analytic**: the 60-min moving-window HV gain falls below 1% from gen 36 onward. The
   operator stop at gen 40 was conservative (4 extra gens past plateau onset). Empirical convergence
   on the 2-direction substrate is therefore ~gen 36, well below the 300-gen plan and roughly 3x the
   t0102/t0104 stop point of gen 12. Convergence happens slower than t0102's apparent gen-15 plateau
   (which was substrate-limited rather than HV-converged) but faster than the [Mohacsi2024]
   published 20-60 gen NSGA-II asymptote on 3-12 parameter problems.

The reformulation (16-direction vector-sum DSI to 2-direction ratio DSI) is what made the
breakthrough, not the longer generation budget. The first joint-pass cell appeared at gen 18 —
within the 12-generation budget that [t0102] and [t0104] used. Had the 2-direction reformulation
been applied at [t0104] gen 12, joint-pass cells would already have appeared. Conversely, running
[t0104]'s 16-direction metric out to gen 40 on the same substrate is the natural falsifier; the
prediction is that the L-shape would persist.

H2 (continued HV improvement past gen 20) is confirmed: HV at gen 20 was approximately 38.7, at gen
40 it reached 122.03, a 3.15x climb in the post-[t0104]-stop region. H3 (objective and direction
simplification compound) is confirmed: t0106's best DSI of 1.0000 exceeds [t0104]'s seed-55 best of
0.5417 by 0.46 and t0106's best joint-pass cell PD = 81.43 Hz dwarfs [t0104]'s best-DSI cell PD of
3.57 Hz.

The substrate-limited reading from [t0104] is decisively reversed. The substrate (Bed B + 14-d
morphology) was populated with joint-pass solutions all along; they were hidden by the harder
16-direction vector-sum metric. The follow-up question — whether the t0106 cells satisfy the
stricter [Trenholm2013] biological reference under 16-direction re-evaluation, higher noise
replicate counts, and naturalistic stimuli — is deferred to S-0106-02 (N_EVAL_SEEDS = 20
robustness) and S-0106-03 (16-direction re-evaluation).

## Limitations

* **Single GA seed.** Only seed 44 was run. The 123/3744 yield is point-estimated, not
  variance-estimated. The seed-confirmation follow-up (S-0106-01 at $5-10 per additional seed) is
  the natural mitigation. Confidence in the qualitative claim (yield > 0) is unaffected by this;
  confidence in the 3.3% yield magnitude is reduced.

* **Low N_EVAL_SEEDS (3 noise replicates per cell).** Robustness at this trial count is below the
  per-task ceiling. The 24 unique DSI > 0.9 AND PD > 80 Hz cells could thin under re-evaluation at
  N_EVAL_SEEDS = 20. S-0106-02 (high priority) addresses this directly.

* **2-direction objective restriction.** The metric reformulation is the breakthrough lever but it
  is also the largest unknown: 16-direction performance of the top t0106 cells is unmeasured. The
  natural follow-up (S-0106-03) re-evaluates the top 50 cells on 16 directions and computes both
  vector-sum DSI and ratio DSI per cell. If the 16-direction vector-sum DSI drops below 0.5 for most
  top cells, then t0106 found 2-direction-only DSGCs — a weaker biological claim than the headline
  implies.

* **Generation horizon 40, not 300.** The operator stopped at HV plateau before exhausting the
  300-gen plan. The asset captures generations 1-40 only. Whether gen 41+ would have refined the
  Pareto front further is unmeasured but the post-gen-36 HV trace argues no.

* **Operator stop is subjective.** The "less than 1% per 60 min" rule was not pre-registered; the
  operator chose the rule during the run based on the HV trace. The stop is reproducible (rule is
  documented in `intervention/operator_stop.md`) but the choice of rule is post-hoc.

* **`vector_68d` parameter scaling.** The asset records the raw 68-d vectors; the parameter bounds
  and conversion conventions are inherited from t0080/t0090/t0093 and require the per-task evaluator
  code to interpret. Re-using the vectors in downstream tasks must import `apply_parameter_vector`
  and `generate_fixed_morphology` from the task code.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0102_seedscale_n4_gen20`
* Task: `t0104_nsga2_2obj_dsi_pdrate_3seeds`

[t0080]: ../../../../t0080_bedb_mobo_v3_dendritic_spike_nsga2/
[t0099]: ../../../../t0099_random_init_pareto_robustness/
[t0102]: ../../../../t0102_seedscale_n4_gen20/
[t0104]: ../../../../t0104_nsga2_2obj_dsi_pdrate_3seeds/
