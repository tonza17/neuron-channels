# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0112 — <strong>Seed-77 minimum-change replicate of t0106 long 2-direction
NSGA-II</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0112_t0106_seed77_replicate` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Expected assets** | 1 predictions |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Task folder** | [`t0112_t0106_seed77_replicate/`](../../../tasks/t0112_t0106_seed77_replicate/) |

# t0112: Seed-77 Minimum-Change Replicate of t0106 Long 2-Direction NSGA-II

## Motivation

`t0106_long_pdnd_nsga2_300gen` produced the first joint-pass cells (DSI >= 0.5 AND PD-rate >=
30 Hz) in the entire `t0080` -> `t0104` NSGA-II lineage: **123 unique cells across 3,744
evaluations** from a single random-init GA seed (44) running 40 generations on the 68-d Bed B
+ 14-d morphology substrate. The breakthrough was driven by reformulating the selectivity
objective from 16-direction vector-sum DSI to 2-direction ratio DSI = (PD - ND) / (PD + ND),
not by additional compute.

Two open caveats motivate this task:

1. **Seed-specificity**: t0106 ran a single GA seed. Without at least one replicate, the 3.3%
   joint-pass acceptance rate is a single-realisation point estimate, not a substrate
   property. It cannot be reported as such in any future writeup.

2. **NEURON memory creep**: t0106's `_POOL_RESTART_EVERY = 25` (in `nsga2_driver.py:97`) was
   chosen before the long-horizon behaviour of the worker pool was characterised. Wall-clock
   telemetry from t0106 shows growing per-evaluation memory footprint between restarts,
   consistent with NEURON's known leak under repeated cell instantiation. A tighter restart
   cadence (every 10 generations) reduces this footprint at negligible wall-clock cost (~2
   extra minutes over a 40-gen run).

This task addresses both with a single minimum-change replicate.

## Scope

* **In scope**: identical substrate to t0106 (Bed B 54-d electrophys + 14-d morphology = 68
  free parameters), identical objectives (2-direction ratio DSI + PD-rate at 0 deg), identical
  NSGA-II hyperparameters (pop=96, SBX/PM operators, HV-plateau operator-stop criterion),
  identical evaluation protocol (N_EVAL_SEEDS = 3, ratio DSI, silence guard active).
* **In scope, changed**: GA seed (44 -> 77), pool-restart cadence (25 -> 10 gens), gen ceiling
  (300 -> 60 to keep budget bounded while still allowing slower plateaus to be discovered).
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, or the NSGA-II driver beyond the seed and
  pool-restart constants. Out-of-scope changes would compromise the like-for-like comparison.

## Approach

1. **Fork t0106 code into `tasks/t0112_t0106_seed77_replicate/code/`**: copy
   `nsga2_driver.py`, `constants.py`, `random_init.py`, and any helper modules. Update package
   imports.
2. **Change exactly two constants**:
   * `constants.py`: rename `T0106_SEEDS = (44,)` -> `T0112_SEEDS = (77,)`; bump
     `T0112_HARD_BUDGET_USD` if needed (default to $25 per-task cap).
   * `nsga2_driver.py:97`: `_POOL_RESTART_EVERY = 10` (was 25).
3. **Raise gen ceiling**: `N_GEN = 60` in `constants_morphology` import override, with
   HV-plateau stop preserved verbatim. The HV-plateau constants (`HV_PLATEAU_WINDOW`,
   `HV_PLATEAU_MIN_HV_HISTORY`, `HV_PLATEAU_REL_THRESHOLD`) are unchanged so the stopping
   criterion is identical to t0106.
4. **Smoke gate locally** (5 checks identical to t0106): single-eval driver run, ratio DSI
   synthetic sanity, silence-guard unit tests, pool-restart sanity, watchdog wiring.
5. **Provision remote** Vast.ai single instance (same provisioning class as t0106).
6. **Launch** with cost cap $25 per-task default and per-instance watchdog $20. Operator-stop
   on HV plateau (same window/threshold as t0106) or at gen 60 ceiling, whichever comes first.
7. **Collect** evaluator-side per-cell DSI / PD-rate / generation table as a predictions asset
   following the t0106 predictions asset format.
8. **Compare** to t0106:
   * Joint-pass cell count (DSI >= 0.5 AND PD >= 30 Hz) absolute number and as % of total
     evals.
   * Best ratio DSI and best PD-rate frontier vs t0106's 1.0000 / 122.6 Hz.
   * HV trajectory shape and plateau generation.
   * Pareto front overlap between seed-44 and seed-77 cells (parameter-space distance).

## Expected Assets

* **1 predictions asset** under `assets/predictions/t0112-bedb-morph-nsga2-seed77/` containing
  the per-cell DSI / PD-rate / generation table for all evaluated cells (mirroring t0106's
  predictions asset schema).

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is
  for CPU cores, not GPU.
* **Remote**: Vast.ai single instance, same provisioning class as t0106 (high-core-count CPU
  node).
* **Cost cap**: $25 per-task default. **Per-instance watchdog**: $20 (via
  `make_watchdog_from_machine_log`).
* **Expected actual cost**: ~$10-11 (mirroring t0106's $10.37 spend at the same pop/gen/eval
  budget).
* **Project envelope check**: $18.20 remaining of $75 prior to this task. Expected post-task
  reserve: ~$7-8.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `pareto_front_seed44_vs_seed77.png` — overlay of t0106 (seed 44) and t0112 (seed 77) strict
   Pareto fronts on DSI vs PD-rate axes; coloured by source task; answers "do the two seeds
   discover comparable Pareto frontiers?"
2. `hv_vs_gen_seed44_vs_seed77.png` — log-scale HV trajectory for both seeds on the same axes,
   with pool-restart events annotated; answers "does the tighter restart cadence change the HV
   trajectory shape?"
3. `joint_pass_yield_per_gen.png` — joint-pass cell count discovered per generation for both
   seeds; answers "when does each seed first hit the joint-pass corner, and what is the rate
   thereafter?"
4. `top50_morphologies_seed77.png` — 10x5 grid of best 50 cells, coloured by archetype (same
   format as t0106's `top50_morphologies.png`); answers "are the best-yield morphologies the
   same archetypes as t0106?"
5. `asymmetry_distribution_seed44_vs_seed77.png` — 4-panel histogram (soma offset, elongation,
   branch density gradient, primary branch PD concentration) for top-50 cells from both seeds;
   answers "is the morphology distribution of high-yield cells seed-independent?"

### Tables

* `results/data/joint_pass_summary.csv` — per-seed: total evals, joint-pass count, joint-pass
  %, best DSI, best PD-rate, plateau generation.
* `results/data/pareto_front_overlap.csv` — parameter-space nearest-neighbour distance between
  each t0112 Pareto cell and its closest t0106 Pareto cell; informs whether the two seeds find
  "the same" or "different" frontier solutions.

### Registered metrics

Run all registered metrics that apply to this task. Check `uv run python -u -m
arf.scripts.aggregators.aggregate_metrics --format json`. At minimum:

* `direction_selectivity_index` — best ratio DSI across all cells (variant: `best_legit` for
  the highest non-DSI=1.0 cell, plus the DSI=1.0 cell counts).
* `pd_rate_hz` — best PD-rate frontier (variant: `at_best_dsi`, `at_pareto_corner`).

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative
answer, not a hedge:

1. Does seed 77 produce >= 40 unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz)?
   * If yes: t0106 is replicated; substrate is genuinely populated.
   * If no but >= 10 unique cells: partial replication; multi-seed required.
   * If 0: t0106 was seed-specific; pivot strategy required.
2. Does seed 77's best ratio DSI reach or exceed 0.95?
3. Does seed 77's best PD-rate frontier reach or exceed 100 Hz?
4. Do the two seeds' Pareto fronts overlap in parameter space (median nearest-neighbour
   distance below the cross-seed noise floor)?
5. Did the tighter pool-restart cadence (every 10 gens) materially change the HV trajectory or
   wall-clock per generation vs t0106?

## Cross-References

* **Parent task**: `t0106_long_pdnd_nsga2_300gen` (substrate, driver, constants, baseline).
* **Caveat task**: `t0107_t0106_polar_8dir_recheck` (8-dir polar re-evaluation showing the
  conventional-protocol DSI is much lower; not in scope for this task but motivates a
  downstream re-evaluation across both t0106 + t0112 cells once t0112 completes).
* **Source suggestion**: none. This task generates new follow-up suggestions in its own
  `results/suggestions.json` based on the outcome.
* **Brainstorm source**: `t0111_brainstorm_results_22`.

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
