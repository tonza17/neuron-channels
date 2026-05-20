# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0115 — <strong>Seed-9354 NSGA-II replicate of t0106 with auto-stop
disabled</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0115_seed9354_no_autostop` |
| **Status** | not_started |
| **Effective date** | 2026-05-20 |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Expected assets** | 1 predictions |
| **Source suggestion** | `S-0112-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Seed-9354 NSGA-II replicate of t0106 with auto-stop disabled](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Task folder** | [`t0115_seed9354_no_autostop/`](../../../tasks/t0115_seed9354_no_autostop/) |

# t0115: Seed-9354 NSGA-II Replicate of t0106 Substrate with HV-Plateau Auto-Stop Disabled

## Motivation

This task is the **5th and final seed** of the `S-0112-01` substrate-rate confirmation batch
on the 68-d Bed B + 14-d morphology substrate. The prior four seeds are:

* `t0106_long_pdnd_nsga2_300gen` (seed 44): 123 legit joint-pass cells, 3.29 % acceptance,
  best legit DSI ~0.94 / PD ~95 Hz, plateau gen 40.
* `t0112_t0106_seed77_replicate` (seed 77): 7 legit joint-pass cells, 0.35 % acceptance, best
  legit 0.9535 / PD 114.8 Hz, plateau gen 21.
* `t0113_t0106_seed2247_replicate` (seed 2247): 0 legit joint-pass cells (2 silence-guard
  DSI=1.0 only), best legit 0.3651 / 10.24 Hz, premature auto-stop at gen 14.
* `t0114_seed7755_no_autostop` (seed 7755, this task's direct parent): 194 legit joint-pass
  cells, 4.30 % acceptance, best legit DSI 0.9868 / PD 107.86 Hz, operator-stopped at gen 62
  (auto-stop disabled).

The four-seed estimate of substrate acceptance density is therefore **mean 1.81 %, SD 1.86 %,
SE 0.93 %** with 95 % CI (-0.16 %, 3.78 %), still bracketing both literature baselines (Hay
2011 0.40 %, Druckmann 2007 0.10 %). A 5th seed is needed to bring the standard error below
0.5 % and to give the substrate-rate estimate enough power to reject or confirm the Hay
envelope. This task contributes that 5th seed.

The seed is **9354**, drawn locally by `secrets.randbelow(10000)` on 2026-05-20 by the
implementing agent. Random draw keeps the seed sample (44, 77, 2247, 7755, 9354)
well-distributed across [0, 10 000].

## Scope

* **In scope (unchanged from t0114)**: substrate (68 free parameters), objectives (2-direction
  ratio DSI + PD-rate at 0 deg), NSGA-II hyperparameters (pop = 96, SBX/PM operators),
  evaluation protocol (`N_EVAL_SEEDS = 3`, ratio DSI, silence guard active),
  `_POOL_RESTART_EVERY = 10` ("10th gen rule"), `N_GEN = 300` ceiling, HV-plateau auto-stop
  **DISABLED**, $25 per-task budget cap, $20 per-instance watchdog, predictions asset schema,
  cost-watchdog wiring, smoke-gate suite (including the new check 6 that asserts no
  `HVPlateauTermination` in the live termination list).
* **In scope, changed from t0114**:
  * GA seed: `7755 → 9354` (randomly drawn for this task).
  * Vast.ai instance: **fully independent** — provision a fresh node (not the t0114 instance,
    which has been destroyed).
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, the NSGA-II driver beyond the seed constant, the
  predictions asset schema, the metrics list, or the cost-watchdog wiring.

## Approach

1. **Fork t0114 code into `tasks/t0115_seed9354_no_autostop/code/`**: copy every algorithm-
   critical Python module from `tasks/t0114_seed7755_no_autostop/code/` (the canonical fork
   base — t0114 already carries the auto-stop-disabled `_build_termination()` helper, `N_GEN =
   300`, and `_POOL_RESTART_EVERY = 10`), plus the orchestration shell script.
2. **Rewrite package import paths**: replace `tasks.t0114_seed7755_no_autostop` with
   `tasks.t0115_seed9354_no_autostop` across every copied `.py` and `.sh` file. Do not touch
   upstream task references (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`,
   `tasks.t0092_*`, `tasks.t0093_*`, `tasks.t0106_*`).
3. **Apply exactly one constant patch**: in `constants.py`, rename `T0114_SEEDS = (7755,) →
   T0115_SEEDS = (9354,)` and update the backwards-compatibility aliases at the bottom of the
   file. Do NOT touch `N_GEN`, `_POOL_RESTART_EVERY`, or the termination construction in
   `nsga2_driver.py` — t0114's auto-stop-disabled wiring is the correct default for this task
   too.
4. **Smoke gate locally** (same 6 checks as t0114): single-eval driver run (deferred to
   remote), ratio DSI synthetic sanity, silence-guard unit tests, pool-restart sanity,
   cost-watchdog wiring, and the auto-stop-absent assertion.
5. **Provision Vast.ai single instance** with the same filter class as t0114 (EPYC-class CPU,
   ≥ 100 GB RAM, idle GPU, reliability ≥ 0.99, `dph ≤ 0.40`, EPYC family post-filter). Prefer
   a 64-core+ EPYC 7B13 / 7713P to inherit t0114's 160-200 s/gen wall-clock.
6. **Launch** with cost cap $25 per-task and per-instance watchdog $20. Termination triggers
   are (in order of expected firing): explicit operator stop, $25 budget cap, $20 per-instance
   watchdog, gen 300 ceiling. **Auto-stop is intentionally OFF.**
7. **Collect** the evaluator-side per-cell DSI / PD-rate / generation table as a predictions
   asset in the t0114 schema (`spec_version: "2"`, gzipped JSON, fields `generation`,
   `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` — back-compat field name storing
   ratio DSI — and `pd_rate_hz`).
8. **Compare** to t0106, t0112, t0113, t0114:
   * Joint-pass cell count (DSI ≥ 0.5 AND PD ≥ 30 Hz) absolute and as % of total evaluations.
   * Best ratio DSI and best PD-rate frontier vs the four prior seeds.
   * Full HV trajectory shape vs the four prior seeds.
   * Pareto front overlap in normalised z-scored 68-d parameter space against each prior seed.
   * **5-seed substrate-rate mean and SE** with the t0114 four-seed result as the prior.

## Expected Assets

* **1 predictions asset** at
  `tasks/t0115_seed9354_no_autostop/assets/predictions/t0115-bedb-morph-nsga2-seed9354/`
  containing the per-cell DSI / PD-rate / generation table for every evaluated cell, mirroring
  the t0114 predictions asset schema.

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is
  for CPU cores; the GPU sits idle on the selected Vast.ai offer.
* **Remote**: Vast.ai single instance, same provisioning class as t0114, fully independent
  from the (now destroyed) t0114 instance.
* **Cost cap**: $25 per-task hard cap. **Per-instance watchdog**: $20.
* **Expected actual cost**: ~$1-5 (t0114 spent $0.94 stopping at gen 62 of 300; expect a
  similar per-gen rate at ~180 s/gen on EPYC 64-core). If the operator runs t0115 to the gen
  300 ceiling, the cost lands near $5-6.
* **Project envelope check**: confirm project remaining budget covers $25 hard cap before
  provisioning. Project budget at t0114 start was $40.73; after t0114's $0.94 spend it is
  ~$39.79.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `hv_vs_gen_5seeds.png` — log-scale HV trajectory for all five seeds (44, 77, 2247, 7755,
   9354) on the same axes with pool-restart events annotated.
2. `pareto_front_5seeds.png` — overlay of strict Pareto fronts from all five tasks on DSI vs
   PD-rate axes, coloured by source task.
3. `joint_pass_yield_per_gen_5seeds.png` — joint-pass cell count discovered per generation
   across all five seeds.
4. `top50_morphologies_seed9354.png` — 10x5 grid of best 50 cells from t0115, coloured by
   archetype.
5. `substrate_rate_5seed_with_literature.png` — 5-seed mean ± SE bar chart vs Hay 2011 (0.40
   %) and Druckmann 2007 (0.10 %) literature baselines.

### Tables

* `results/data/joint_pass_summary_5seeds.csv` — per-seed (44, 77, 2247, 7755, 9354): total
  evals, joint-pass count, joint-pass %, best DSI, best PD-rate, stop trigger, stop
  generation.
* `results/data/pareto_front_overlap_5seeds.csv` — for each t0115 Pareto cell, the nearest-
  neighbour z-scored L2 distance in 68-d parameter space to its closest cell from each prior
  seed.

### Registered metrics

* `direction_selectivity_index` — best ratio DSI across all evaluated cells. Sub-variants
  `best_legit` (highest non-DSI = 1.0 cell), `overall_max`, `dsi_eq_one_count`.

Operational metrics (not registered): `joint_pass_count`, `best_pd_rate_hz`,
`n_cells_evaluated_total`, `n_gen_completed`, `stop_trigger`,
`efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`.

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative
answer:

1. **Seed-9354 joint-pass count.** Does seed 9354 produce ≥ 40 unique legit joint-pass cells
   (t0106-like), 7-39 cells (t0112-like), 1-6 cells (sparse), or 0 (substrate not populated)?
2. **Best ratio DSI.** Does seed 9354's best legit ratio DSI reach or exceed 0.95?
3. **Best PD-rate.** Does seed 9354's best PD-rate reach or exceed 100 Hz?
4. **5-seed substrate-rate estimate.** Combining all 5 seeds, what is the substrate-level mean
   joint-pass acceptance rate and its standard error? Does the 5-seed mean fall within the Hay
   2011 (0.40 %) / Druckmann 2007 (0.10 %) literature envelope, or above it?
5. **Stop trigger.** Which mechanism actually stopped the run (operator, budget cap, gen
   ceiling, instance watchdog)?
6. **Per-gen wall-clock at extended N_GEN.** Does the cadence-10 pool-restart cycle continue
   to keep wall-clock near t0114's 180 s/gen sustained average?

## Risks and Fallbacks

* **Risk**: seed 9354 lands in the sparse regime (t0113-like) and contributes very little to
  the 5-seed substrate-rate estimate. **Fallback**: this is still a valid datapoint; document
  prominently in results.
* **Risk**: Vast.ai instance is interrupted mid-run. **Fallback**: t0114-family driver writes
  HV trace + per-cell evaluations after every generation; resume from last completed
  generation if the orchestration shell script supports it, otherwise treat the partial run as
  the final result.
* **Risk**: operator forgets to issue a stop signal and the run goes to gen 300 / budget cap
  unattended. **Fallback**: acceptable — the gen ceiling and budget cap are the safety net for
  the "stop when I say so" directive.

## Cross-References

* **Parent tasks**: `t0106_long_pdnd_nsga2_300gen` (original substrate),
  `t0114_seed7755_no_autostop` (canonical fork base with auto-stop-disabled wiring).
* **Source suggestion**: `S-0112-01` (5-seed substrate-rate confirmation batch). This task is
  the 5th and final seed.
* **Related suggestion**: `S-0113-03` (HV-plateau detector reparameterisation). The t0115 HV
  trace, like the t0114 trace, contributes to the offline detector-replay sweep in t0114's
  results stage.
* **Related caveat tasks**: `t0107_t0106_polar_8dir_recheck` (8-direction polar re-evaluation
  showing 2-direction ratio DSI overstates selectivity by ~0.42 absolute). Polar re-evaluation
  of any t0115 joint-pass cells is out of scope for this task.

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
