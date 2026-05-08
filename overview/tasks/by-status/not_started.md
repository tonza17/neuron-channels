# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0096 — <strong>Literature survey: multi-objective optimisation of
single-neuron models</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0096_literature_survey_multi_objective_neuron_optimisation` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | — |
| **Expected assets** | 10 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`internet-research`](../../../meta/task_types/internet-research/), [`answer-question`](../../../meta/task_types/answer-question/) |
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
