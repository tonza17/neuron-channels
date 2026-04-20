# ⏹ Tasks: Not Started

7 tasks. ⏹ **7 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0019 — <strong>Literature survey: voltage-gated channels in retinal
ganglion cells</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0019_literature_survey_voltage_gated_channels` |
| **Status** | not_started |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-05` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Task page** | [Literature survey: voltage-gated channels in retinal ganglion cells](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Task folder** | [`t0019_literature_survey_voltage_gated_channels/`](../../../tasks/t0019_literature_survey_voltage_gated_channels/) |

# Literature survey: voltage-gated channels in retinal ganglion cells

## Motivation

Research question RQ1 (Na/K combinations) drives the project's main optimisation experiment.
Good priors on which Nav and Kv subunits are expressed in RGCs, their kinetic parameters, and
their conductance densities are needed to constrain the search space before optimisation
begins. The t0002 corpus provides DSGC modelling context but does not systematically cover
channel-expression or channel-kinetics literature. Source suggestion: S-0014-05 from
t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Nav subunit expression in RGCs — Nav1.1, Nav1.2, Nav1.6 distributions across soma, AIS,
   dendrite.
2. Kv subunit expression in RGCs — Kv1, Kv2, Kv3, Kv4, BK, SK distributions.
3. HH-family kinetic models — published rate functions, activation/inactivation curves, time
   constants.
4. Subunit co-expression patterns — Nav + Kv combinations reported in specific RGC types.
5. ModelDB MOD-file provenance — which published MOD files implement which Nav/Kv kinetics.
6. Nav/Kv conductance-density estimates — somatic vs AIS vs dendritic densities.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, including explicit ModelDB searches for
   RGC-relevant Nav and Kv MOD files.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset mapping candidate Nav/Kv combinations to published DSGC tuning-curve
   fits, with a row per combination giving the subunits, their densities, and the source
   paper.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` mapping Nav/Kv combinations to DSGC tuning-curve
  fits.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and contains a combination table with at
  least five rows keyed by Nav/Kv subunits and source paper DOI.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

</details>

<details>
<summary>⏹ 0018 — <strong>Literature survey: synaptic integration in RGC-adjacent
systems</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0018_literature_survey_synaptic_integration` |
| **Status** | not_started |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-04` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Task page** | [Literature survey: synaptic integration in RGC-adjacent systems](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Task folder** | [`t0018_literature_survey_synaptic_integration/`](../../../tasks/t0018_literature_survey_synaptic_integration/) |

# Literature survey: synaptic integration in RGC-adjacent systems

## Motivation

Research question RQ3 (AMPA/GABA balance) and later synaptic-parameter optimisation need prior
distributions for receptor kinetics, E-I ratios, and spatial-distribution patterns. The
modelling literature in t0002 touches these parameters but does not systematically cover the
synaptic- integration experimental and theoretical work that underpins them. Source
suggestion: S-0014-04 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. AMPA/NMDA/GABA receptor kinetics — rise and decay time constants, reversal potentials.
2. Shunting inhibition — location-dependent vetoing, input resistance changes.
3. E-I balance — temporal co-tuning, conductance ratios in retinal and cortical systems.
4. Temporal summation — how closely spaced inputs integrate vs saturate.
5. Dendritic-location dependence — soma-vs-dendrite integration, attenuation before the spike
   initiation zone.
6. Synaptic-density scaling — synapses per micrometre of dendrite, bouton counts.
7. SAC/DSGC inhibitory asymmetry — starburst amacrine cell GABA output onto DSGC dendrites in
   the preferred vs null directions.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, preferring studies that publish fitted
   kinetic parameters or conductance-ratio measurements rather than qualitative reports.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset tabulating receptor kinetics and E-I ratios usable as prior
   distributions for later optimisation tasks.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` with a prior-distribution table for kinetics and E-I
  ratios, keyed by paper DOI and region.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and provides a numeric prior-distribution
  table.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

</details>

<details>
<summary>⏹ 0013 — <strong>Resolve dsgc-baseline-morphology source-paper
provenance</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0013_resolve_morphology_provenance` |
| **Status** | not_started |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0005-01` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/), [`correction`](../../../meta/task_types/correction/) |
| **Task page** | [Resolve dsgc-baseline-morphology source-paper provenance](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Task folder** | [`t0013_resolve_morphology_provenance/`](../../../tasks/t0013_resolve_morphology_provenance/) |

# Resolve dsgc-baseline-morphology source-paper provenance

## Motivation

The `dsgc-baseline-morphology` dataset asset (NeuroMorpho neuron 102976, 141009_Pair1DSGC)
currently has `source_paper_id = null` because two Feller-lab 2018 papers are plausibly the
source:

* Morrie & Feller 2018 Neuron (DOI `10.1016/j.neuron.2018.05.028`) — nominated in the t0005
  download plan.
* Murphy-Baum & Feller 2018 Current Biology (DOI `10.1016/j.cub.2018.03.001`) — reported as
  the source by NeuroMorpho's metadata.

Until this is resolved, every downstream paper that uses the morphology will cite it
incorrectly or omit a citation entirely. This task downloads both candidate papers, reads
their Methods sections, confirms which one introduced the 141009_Pair1DSGC reconstruction, and
files a corrections asset that updates `dsgc-baseline-morphology.source_paper_id` to the
correct slug.

Covers suggestion **S-0005-01**.

## Scope

1. Download Morrie & Feller 2018 Neuron via `/add-paper`. Register as a v3 paper asset under
   `assets/paper/10.1016_j.neuron.2018.05.028/`.
2. Download Murphy-Baum & Feller 2018 Current Biology via `/add-paper`. Register as a v3 paper
   asset under `assets/paper/10.1016_j.cub.2018.03.001/`.
3. Read both papers' Methods sections. Look specifically for:
   * The recording date `141009` (October 9, 2014) or neighbouring dates.
   * The `Pair1DSGC` / `Pair 1 DSGC` / `paired recording` language matching the NeuroMorpho
     reconstruction metadata.
   * An explicit citation of the 141009_Pair1DSGC reconstruction or its deposit to
     NeuroMorpho.
4. If one paper is unambiguously the source, file a correction asset
   (`corrections/dataset_dsgc-baseline-morphology.json`) that sets `source_paper_id` to the
   winning paper's DOI-slug. If neither is an unambiguous match, file a correction that
   records both DOIs under a new `candidate_source_paper_ids` field and opens an intervention
   file explaining that Feller-lab contact is required.
5. Record the full reasoning in `results/results_detailed.md` so the provenance decision is
   auditable.

## Dependencies

* **t0005_download_dsgc_morphology** — owns the `dsgc-baseline-morphology` asset this task
  corrects.

## Expected Outputs

* **2 paper assets** (Morrie & Feller 2018 Neuron, Murphy-Baum & Feller 2018 Current Biology),
  both v3-spec-compliant with full summaries.
* **1 correction asset** in `corrections/dataset_dsgc-baseline-morphology.json` setting
  `source_paper_id` to the resolved winner (or documenting ambiguity).
* A provenance-reasoning section in `results/results_detailed.md`.

## Approach

1. Run `/add-paper` twice, once per DOI, following the paper-asset spec v3.
2. Read both full PDFs and extract the Methods paragraphs that describe the paired
   recording(s) from which 141009_Pair1DSGC was reconstructed.
3. If both papers cite the same recording session, pick the earlier one (lower DOI publication
   date). If only one paper cites the recording session, pick that one. If neither paper cites
   it, treat as ambiguous and flag for human review.

## Questions the task answers

1. Which Feller-lab 2018 paper introduced the 141009_Pair1DSGC reconstruction?
2. Does NeuroMorpho's metadata attribution (Murphy-Baum & Feller 2018) match the paper's
   Methods section, or does it disagree?
3. If both papers plausibly cite the recording, what are the tie-breakers?

## Risks and Fallbacks

* **Neither paper explicitly cites the 141009 reconstruction**: file an intervention asking
  the researcher to email the Feller lab. Do not silently pick one.
* **Both papers cite it**: pick the earlier publication date and document the tie-break.
* **Paper downloads fail (paywall / captcha)**: fall back to metadata-only paper assets (v3
  spec `download_status: "failed"`) and raise an intervention file requesting library access.

</details>

<details>
<summary>⏹ 0012 — <strong>Tuning-curve scoring loss library</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0012_tuning_curve_scoring_loss_library` |
| **Status** | not_started |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-09` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Tuning-curve scoring loss library](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Task folder** | [`t0012_tuning_curve_scoring_loss_library/`](../../../tasks/t0012_tuning_curve_scoring_loss_library/) |

# Tuning-curve scoring loss library

## Motivation

The t0002 literature survey set four concurrent quantitative targets an optimised DSGC model
must hit: DSI **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM
**60-90°**. The project has four registered metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`). Every downstream
optimisation task (Na/K grid search S-0002-01, morphology sweep S-0002-04, E/I ratio scan
S-0002-05, active-vs-passive dendrites S-0002-02) needs a shared scoring function: same
target, same weighting, same tie-breaks. Without this library, each task will invent its own
scoring and cross-task comparisons of "who wins" become meaningless. This task provides that
canonical scorer.

Covers suggestion **S-0002-09** (and subsumes **S-0004-03** — see the t0006 correction file).

## Scope

The library `tuning_curve_loss` exposes:

1. `score(simulated_curve_csv, target_curve_csv | None) -> ScoreReport` — returns a frozen
   dataclass containing:
   * `loss_scalar` (float) — weighted-Euclidean-distance-in-normalised-space loss combining
     the four envelope targets.
   * `dsi_residual`, `peak_residual_hz`, `null_residual_hz`, `hwhm_residual_deg` — individual
     residuals with signs.
   * `rmse_vs_target` — point-wise RMSE of `(angle, firing_rate)` against the target curve
     (only when a target is supplied).
   * `reliability` — cross-trial coefficient of determination (maps onto the registered
     `tuning_curve_reliability` metric).
   * `passes_envelope` (bool) — whether the simulated curve lands inside the t0002 envelope on
     all four targets simultaneously.
   * `per_target_pass` — dict `{"dsi": bool, "peak": bool, "null": bool, "hwhm": bool}`.
2. `compute_dsi(curve_csv) -> float`
3. `compute_preferred_peak_hz(curve_csv) -> float`
4. `compute_null_residual_hz(curve_csv) -> float`
5. `compute_hwhm_deg(curve_csv) -> float`
6. Tuning-curve CSV schema constant: `(angle_deg, trial_seed, firing_rate_hz)`.
7. CLI: `python -m tuning_curve_loss.cli <simulated.csv> [--target <target.csv>]`.

Weights for the scalar loss default to **DSI 0.25, peak 0.25, null 0.25, HWHM 0.25** but are
user-overridable via a keyword argument and via a JSON config file; the defaults and rationale
are documented in the asset's `description.md`.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical `target-tuning-curve`
  dataset used as the default comparison target and as the smoke-test fixture.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-loss/`) with:
  * `description.md` covering API, weight defaults, and worked examples
  * `module_paths` pointing at `code/tuning_curve_loss/`
  * `test_paths` pointing at `code/tuning_curve_loss/test_*.py` with at least:
    * Identity test: `score(target, target)` must return `loss_scalar == 0.0` and
      `passes_envelope is True`.
    * Envelope-boundary tests: hand-crafted curves just inside and just outside each of the
      four envelope boundaries.
    * Reliability test: two curves with identical trial-means but very different
      trial-to-trial variance produce different `reliability` values.

## Approach

Pure Python + NumPy + pandas. No simulator dependency. The DSI and HWHM computations must
match the closed-form computations used in t0004 to produce the target curve, so that
`score(target, target)` is exactly zero. Use the registered metric keys from `meta/metrics/`
so that scored values can be written directly into `results/metrics.json` without post-hoc
renaming.

## Questions the task answers

1. Does `score(target, target)` return `loss_scalar == 0.0`?
2. Do the envelope-boundary tests flip `passes_envelope` at the correct boundary to within
   floating-point tolerance?
3. Does the scorer accept multi-trial CSVs and correctly combine trials into a mean before
   computing DSI, peak, null and HWHM?

## Risks and Fallbacks

* **The literature envelope numbers conflict with the t0004 target curve** (e.g., the target
  sits right at an envelope boundary): document the target's position on the envelope in the
  library description; do not silently redefine targets.
* **Trial-to-trial variance inflates `reliability` beyond sensible bounds**: clamp to [0, 1]
  and document the clamp.

</details>

<details>
<summary>⏹ 0011 — <strong>Response-visualisation library (firing rate vs angle
graphs)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0011_response_visualization_library` |
| **Status** | not_started |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | — |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Response-visualisation library (firing rate vs angle graphs)](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Task folder** | [`t0011_response_visualization_library/`](../../../tasks/t0011_response_visualization_library/) |

# Response-visualisation library (firing rate vs angle graphs)

## Motivation

Every downstream experiment in this project will produce angle-resolved firing-rate data
(tuning curves). Without a shared visualisation library, each task will re-implement its own
plotting code, the plots will drift in style, and cross-model comparisons will need manual
re-work. This task builds one library, used by every later task, that turns a standard-schema
tuning-curve CSV into a consistent set of publication-quality PNGs.

## Scope

The library `tuning_curve_viz` exposes four plotting functions:

1. `plot_cartesian_tuning_curve(curve_csv, out_png, *, show_trials=True, target_csv=None)` —
   firing rate (Hz) vs direction (deg). Shows per-trial points, mean line, and a 95% bootstrap
   confidence band. Optional overlay of a target curve (dashed line) from t0004's
   `target-tuning-curve`.
2. `plot_polar_tuning_curve(curve_csv, out_png, *, target_csv=None)` — classical polar plot
   with the preferred direction annotated.
3. `plot_multi_model_overlay(curves_dict, out_png, *, target_csv=None)` — side-by-side
   Cartesian + polar overlay of multiple models (e.g., the Poleg-Polsky port from t0008, any
   models ported in t0010, and the canonical target curve).
4. `plot_angle_raster_psth(spike_times_csv, out_png, *, angle_deg)` — per-trial spike raster
   above a PSTH (Peri-Stimulus-Time Histogram), one figure per angle.

A CLI `tuning_curve_viz.cli` consumes a tuning-curve CSV path and produces all four plot types
into an output directory.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical target curve for overlays
  and the smoke-test fixture.
* **t0008_port_modeldb_189347** — provides a real simulated tuning curve to smoke-test the
  library against alongside the target.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-viz/`) with:
  * `description.md` covering purpose, API, and example usage.
  * `module_paths` pointing at `code/tuning_curve_viz/`.
  * `test_paths` pointing at `code/tuning_curve_viz/test_*.py`.
  * Example output PNGs under the asset's `files/` (smoke-test outputs against
    `target-tuning-curve` and the t0008 simulated curve).

## Approach

Standard matplotlib + pandas. Tuning-curve CSV schema is fixed at `(angle_deg, trial_seed,
firing_rate_hz)`. Use `bootstrap` from scipy (or a small local implementation) for the 95% CI
band. For the multi-model overlay, auto-pick a colour-blind-safe palette (Okabe-Ito). No
animated plots, no interactive plots; PNG output only.

Smoke tests:

1. Generate all four plot types against `target-tuning-curve` (the pre-existing canonical
   curve).
2. Generate all four plot types against the t0008 Poleg-Polsky port's simulated tuning curve.
3. Generate the `plot_multi_model_overlay` figure combining both with the target as a dashed
   overlay.

Each smoke-test writes its output PNG to the library asset's `files/` folder so the asset
itself demonstrates what each plot looks like.

## Questions the task answers

1. Does the library produce all four plot types on the canonical target curve without errors?
2. Does it produce all four plot types on a real simulated curve (t0008) with the same code
   path?
3. Does the multi-model overlay correctly align axes and preferred-direction annotations
   across models with different angular sampling?

## Risks and Fallbacks

* **Polar-axis convention mismatch between matplotlib and the tuning-curve convention (0° =
  east)**: document the convention in the library's `description.md` and stick to
  `theta_direction=1, theta_offset=0` (standard).
* **`scipy.stats.bootstrap` unavailable**: fall back to a 4-line NumPy bootstrap.
* **Multi-model overlay becomes illegible with > 6 models**: cap overlay at 6 and surface a
  warning; the CLI batches additional models into separate PNGs.

</details>

<details>
<summary>⏹ 0010 — <strong>Hunt DSGC compartmental models missed by prior survey;
port runnable ones</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_hunt_missed_dsgc_models` |
| **Status** | not_started |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`download-paper`](../../../meta/task_types/download-paper/), [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Task page** | [Hunt DSGC compartmental models missed by prior survey; port runnable ones](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Task folder** | [`t0010_hunt_missed_dsgc_models/`](../../../tasks/t0010_hunt_missed_dsgc_models/) |

# Hunt DSGC compartmental models missed by t0002 and t0008; port any with code

## Motivation

The t0002 literature survey built a 20-paper corpus biased toward the six seed references from
`project/description.md` and adjacent DSGC papers. The t0008 ModelDB port focussed on entry
189347 (Poleg-Polsky & Diamond 2016) and its immediate siblings. Neither task exhaustively
searched post-2020 publications, non-ModelDB repositories (GitHub / OSF / Zenodo /
institutional pages), or adjacent computational neuroscience venues (NeurIPS, Cosyne, bioRxiv)
for DSGC compartmental models. This task closes that gap: actively hunt for DSGC compartmental
models the project might have missed, download their papers, and port any models that have
runnable code and are scientifically relevant.

## Scope

1. **Systematic search** across:
   * ModelDB full listing under keywords `direction selective`, `retina`, `DSGC`, `RGC`,
     `Starburst`, `SAC` (broader than the t0008 sweep).
   * GitHub search: `DSGC`, `retinal ganglion direction`, `NetPyNE direction`, `Arbor retina`,
     `NEURON DSGC`.
   * Google Scholar + Semantic Scholar forward-citation chains of:
     * Poleg-Polsky & Diamond 2016
     * Schachter et al. 2010
     * Park et al. 2014
     * Sethuramanujam et al. 2016
     * Hanson et al. 2019
   * bioRxiv + preprint servers, 2023-2025, keyword `direction-selective ganglion cell`.
2. **Download** any paper not already in `assets/paper/` that meets the inclusion bar:
   publishes a compartmental (not rate-coded / not purely statistical) DSGC model with at
   least partial biophysical detail.
3. **Port** any paper with public code that:
   * Runs in Python 3.12 + NEURON 8.2.7 (or Arbor 0.12.0).
   * Can load `dsgc-baseline-morphology-calibrated` or bring its own morphology.
   * Produces an angle-resolved tuning curve.
4. **Report** every candidate in a single answer asset with a per-model row: paper DOI, code
   URL, NEURON compatibility, whether ported, and if not, why not.

## Dependencies

* **t0008_port_modeldb_189347** — gives us a working NEURON-based reference implementation to
  contrast with any newly ported model and a pattern for how to port additional models.

## Expected Outputs

* **1 answer asset** (`assets/answer/missed-dsgc-models-hunt-report/`) summarising every
  candidate found and the outcome of each port attempt.
* **N paper assets** for any new papers (DOI-keyed, v3-spec-compliant). Exact count depends on
  what the search turns up.
* **0 or more library assets** for any successfully ported models
  (`assets/library/<model-slug>/`). Exact count depends on what was portable.
* **Simulated tuning-curve CSVs** under `data/tuning_curves/` for every ported model,
  formatted identically to the t0008 outputs so t0011 can render them side-by-side.

## Approach

Run the search in three passes (ModelDB full sweep, GitHub + OSF + Zenodo, Google Scholar
forward citations). Maintain a single `data/candidates.csv` that grows across passes and
records duplicate-vs-new status against t0002's corpus. Decide portability by actually cloning
the repo and running the demo, not by reading the README; record every port attempt's
stdout/stderr under `logs/` so reviewers can audit the call.

## Questions the task answers

1. Which DSGC compartmental models exist in the literature or in public code that the t0002
   survey and the t0008 ModelDB port missed?
2. Of those, which have runnable public code in this environment?
3. How does each successfully ported model's tuning curve compare with the t0008 Poleg-Polsky
   reproduction and with the canonical `target-tuning-curve`?
4. Are there consistent disagreements across ports (e.g., systematically narrower HWHM, higher
   null firing) that warrant new experiment suggestions?

## Risks and Fallbacks

* **Search finds no new portable models**: document the gap as a new suggestion; the answer
  asset's table should still be produced listing every candidate considered and why each was
  excluded.
* **Port attempts consistently fail**: surface that as a finding — published DSGC
  compartmental code is often fragile — rather than inventing fixes that change the original
  model's behaviour.
* **Search produces too many candidates to port within this task**: triage by (a) citation
  count, (b) publication year (newer first), (c) whether the code is in a simulator already on
  this workstation. Port the top 3-5 and list the rest as suggestions.

</details>

<details>
<summary>⏹ 0008 — <strong>Port ModelDB 189347 and similar DSGC compartmental models
to NEURON</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0008_port_modeldb_189347` |
| **Status** | not_started |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Expected assets** | 1 library, 1 answer |
| **Source suggestion** | `S-0002-03` |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/), [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Port ModelDB 189347 and similar DSGC compartmental models to NEURON](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Task folder** | [`t0008_port_modeldb_189347/`](../../../tasks/t0008_port_modeldb_189347/) |

# Port ModelDB 189347 and similar DSGC compartmental models to NEURON as library assets

## Motivation

Poleg-Polsky & Diamond 2016 (paper `10.1016_j.neuron.2016.02.013`, ModelDB 189347) is the
closest published match to this project's goal: a NEURON multi-compartmental mouse ON-OFF DSGC
model with **177 AMPA + 177 GABA** synapses and NMDA multiplicative gain. Reproducing it
creates the reference implementation that every later parameter-variation task (Na/K grid
S-0002-01, morphology sweep S-0002-04, E/I ratio scan S-0002-05, active-vs-passive dendrites
S-0002-02) will fork from. It is also the cleanest end-to-end test that the NEURON+NetPyNE
install from t0007 and the calibrated morphology from t0009 are fit for purpose.

Covers suggestions **S-0002-03** and **S-0003-02** (merged — the two suggestions describe the
same work from slightly different angles).

## Scope

### Phase A — Port the Poleg-Polsky 2016 baseline

1. Download ModelDB entry 189347 and register the resulting Python package under
   `assets/library/dsgc-polegpolsky-2016/` with a description, module paths, test paths, and a
   smoke-test that instantiates the model and runs a single angle.
2. Swap in the calibrated morphology produced by t0009 (`dsgc-baseline-morphology-calibrated`)
   in place of the ModelDB-bundled morphology. Document the swap and any geometric differences
   (compartment count, dendritic path length, branch points) vs the original ModelDB
   morphology.
3. Run the published stimulus: drifting bar / moving spot at 12 angles (30° spacing), synaptic
   configuration matching the paper, Poleg-Polsky NMDA parameters.
4. Compute the simulated tuning curve (firing rate vs angle, 20 trials per angle with fresh
   seeds) and score it with the t0012 scoring loss library against the envelope: DSI
   **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**.

### Phase B — Hunt for sibling DSGC compartmental models

5. Search ModelDB, SenseLab, OSF, and GitHub for additional DSGC compartmental models cited or
   adjacent in the literature (Schachter2010 derivatives, Briggman-lineage forks, 2017-2025
   updates of the Poleg-Polsky model, any post-2020 published code).
6. For each model found, record: source URL, NEURON compatibility, morphology it ships with,
   synaptic configuration, and whether it runs out-of-the-box in this environment.
7. Port any model that has public code and runs cleanly as a separate library asset under
   `assets/library/<model-slug>/`. If a model fails to run, record the failure in the Phase B
   answer asset and do not register a broken library.

## Dependencies

* **t0005_download_dsgc_morphology** — source of `dsgc-baseline-morphology`
* **t0007_install_neuron_netpyne** — NEURON+NetPyNE must work before any simulation runs
* **t0009_calibrate_dendritic_diameters** — needs calibrated morphology to avoid biasing the
  reproduction with placeholder 0.125 µm radii
* **t0012_tuning_curve_scoring_loss_library** — envelope verification must use the canonical
  scoring library, not an ad-hoc check

## Expected Outputs

* **1 library asset** (`assets/library/dsgc-polegpolsky-2016/`) — the ported ModelDB 189347.
* **1 answer asset** (`assets/answer/dsgc-modeldb-port-reproduction-report/`) covering:
  * Phase A: envelope verification table (DSI, peak, null, HWHM) vs targets
  * Phase B: a survey row-per-model listing each candidate found, its source, its NEURON
    compatibility, whether it was ported, and if not, why
* **0 or more additional library assets** for any sibling models successfully ported.
* **Simulated tuning-curve CSVs** under `data/tuning_curves/` (per model, per seed) for t0011
  to consume.

## Approach

* Write `code/port_modeldb_189347.py` that downloads the ModelDB zip, unpacks it into the
  library asset folder, compiles its MOD files with `nrnivmodl`, and runs the published demo
  to confirm the port is intact before any morphology swap.
* Write `code/run_tuning_curve.py` that takes a library name and a morphology (calibrated
  SWC), runs 12 angles × 20 seeded trials, writes `tuning_curve.csv` with `(angle_deg,
  trial_seed, firing_rate_hz)`.
* Write `code/score_envelope.py` that imports the t0012 scoring library and produces the
  verification table.
* For Phase B: write `code/hunt_sibling_models.py` that scrapes ModelDB's category listings
  (the author's own follow-up entries, neighbouring DSGC entries, 2017+ entries citing 189347)
  and writes a candidate-list CSV. Human review selects which candidates to attempt porting
  before Phase B code runs.

## Compute and Budget

Local only. 12 angles × 20 trials × ~5-10 s wall-clock per trial ≈ 20-40 minutes per model on
this workstation. Budget remains `$0.00`.

## Questions the task answers

1. Does the reproduced Poleg-Polsky 2016 model hit the envelope: DSI 0.7-0.85, peak 40-80 Hz,
   null < 10 Hz, HWHM 60-90°?
2. Does swapping the ModelDB morphology for the calibrated Feller morphology preserve envelope
   compliance, or does it shift the model outside the envelope?
3. Which sibling DSGC compartmental models exist in public repositories, and which run in this
   environment?
4. Are there published DSGC compartmental models whose tuning curves systematically disagree
   with the Poleg-Polsky envelope, and if so, by how much?

## Risks and Fallbacks

* **ModelDB 189347 has drifted or the Python wrapper is stale**: port the `hoc`/`mod` files
  directly and wrap in a minimal Python loader; record the drift in the answer asset.
* **Swapping to the calibrated morphology produces envelope failure**: treat that as a
  scientific finding, not a blocker — report it verbatim and surface a new suggestion for
  morphology- conditioned parameter retuning.
* **Phase B finds no portable sibling models**: document the gap as a new suggestion and do
  not invent models to port.

</details>
