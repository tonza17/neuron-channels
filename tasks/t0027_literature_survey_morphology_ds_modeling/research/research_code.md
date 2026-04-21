---
spec_version: "1"
task_id: "t0027_literature_survey_morphology_ds_modeling"
research_stage: "code"
tasks_reviewed: 25
tasks_cited: 19
libraries_found: 6
libraries_relevant: 0
date_completed: "2026-04-21"
status: "complete"
---
# Research Code: Prior Task Assets for the Morphology-and-DS Literature Survey

## Task Objective

Survey the project's own prior code, libraries, answer assets, and literature-survey conventions to
support this task, whose job is to extend the five-paper morphology-and-direction-selectivity (DS)
baseline corpus to 12-25 papers, produce nine-section `summary.md` documents for each new paper, and
synthesise one answer asset about "what morphology variables shape DS and by what mechanisms". The
task has no computational component beyond paper-asset creation and answer-asset writing — there are
no tuning-curve simulations, no morphology sweeps, and no channel-parameter optimisation in-scope.
This research-code step therefore focuses on (a) the paper-asset and answer-asset pipelines
established by prior literature surveys, (b) project-level helper utilities (`doi_to_slug`,
`find_similar_papers`, the `add-paper` / `download_paper` skills), (c) the ten existing answer
assets that the synthesis answer should cite as related prior conclusions, and (d) the five seed
papers the task already plans to link from prior task folders.

## Library Landscape

The library aggregator (`meta.asset_types.library.aggregator`) returned **six** registered
libraries, **none of which are relevant** to this task. All six are computational / simulation
libraries for running NEURON-based DSGC models and scoring tuning curves, which this task does not
do. No library produces, downloads, summarises, or verifies paper or answer assets — that work is
handled by project-level skills (`add-paper`, `download_paper`) plus `meta/asset_types/*/`
verificators, not by registered libraries. The aggregator output did not carry any correction or
replacement markers. The inventory, in aggregator order:

* `modeldb_189347_dsgc` (created by [t0008]) — NEURON driver + HOC/MOD port of Poleg-Polsky &
  Diamond 2016 DSGC with 12-angle tuning-curve sweep. **Not relevant** — this task does not
  simulate.
* `tuning_curve_viz` (created by [t0011]) — matplotlib library turning tuning-curve CSVs into
  Cartesian, polar, and PSTH PNGs. **Not relevant** — this task produces no tuning-curve CSVs.
* `tuning_curve_loss` (created by [t0012]) — scalar-loss scorer for 12-angle DS tuning curves vs the
  [t0004] target envelope. **Not relevant** — this task produces no tuning curves to score.
* `modeldb_189347_dsgc_gabamod` (created by [t0020]) — sibling port using the paper's native
  `gabaMOD` PD/ND swap rather than spatial rotation. **Not relevant** — this task does not simulate.
* `modeldb_189347_dsgc_dendritic` (created by [t0022]) — per-dendrite E/I shunting driver with a
  channel-modular AIS partition. **Not relevant** — this task does not simulate, though this library
  is a natural downstream consumer of this task's morphology-sweep recommendations.
* `de_rosenroll_2026_dsgc` (created by [t0024]) — NEURON port of de Rosenroll 2026 with AR(2)
  correlated stochastic release. **Not relevant** — this task does not simulate, though it will cite
  de Rosenroll 2026 as a baseline paper.

No `import via library` path exists for any code this task needs. All reuse for this task is via
read-only templates (prior paper summaries, prior answer assets) and helper scripts that live in
`arf/scripts/utils/` and `meta/asset_types/`.

## Key Findings

### Literature-Survey Task Template Is Well Established Across Six Prior Tasks

Six completed tasks share the `literature-survey` task type: [t0002] (20 DSGC papers, the original
20-paper survey), [t0010] (missed-DSGC-model hunt, 2 new papers + port attempts), [t0015] (cable
theory, 5 paywalled papers), [t0016] (dendritic computation, 5 paywalled papers), [t0017]
(patch-clamp, ~5 papers), [t0018] (synaptic integration, 5 paywalled papers), [t0019] (voltage-
gated channels, 5 paywalled papers). The step structure is identical: `prestep` / `create-branch` /
`init-folders` / `research-papers` / `research-internet` / `research-code` / `planning` /
`implementation` / `results` / `suggestions` / `reporting` / `poststep`, with `setup-machines` /
`teardown` / `creative-thinking` / `compare-literature` skipped. this task is following the same
stage sequence; the only novelty is the larger target paper count (12-25 vs the 5-20 of prior
surveys) and the morphology-variable-taxonomy synthesis structure.

### Paper-Asset Pipeline Is Standardised at Spec v3

[t0002] produced the project's 20 canonical paper assets at `spec_version: "3"`. [t0010]'s 2 paper
assets (Poleg-Polsky 2026 and de Rosenroll 2026) and [t0013]'s 2 paper assets (the Feller- lab 2018
provenance-resolution pair) follow the same pattern. Each paper lives at
`tasks/<task_id>/assets/paper/<paper_id>/` with `details.json`, `summary.md`, and a `files/`
subfolder. The `paper_id` folder name is produced by `arf.scripts.utils.doi_to_slug` (see
`meta/asset_types/paper/specification.md` Section "Paper ID"). The summary document must contain
nine mandatory sections (Metadata, Abstract, Overview, Architecture/Models/Methods, Results,
Innovations, Datasets, Main Ideas, Summary) with 500+ words total, 5+ Results bullets, 3+ Main Ideas
bullets, and a 4-paragraph Summary. this task's 12-25 new papers must follow this exact format.

### Paywalled Papers Are Handled Uniformly via `download_status: "failed"`

[t0015], [t0016], [t0018], and [t0019] all delivered paywalled-only corpora (Nature / Science /
Nature Neuroscience / Annual Reviews). Each set `download_status: "failed"`, populated
`download_failure_reason` with the paywall reason, left `files: []` with only a `.gitkeep` to
preserve the folder, and wrote `intervention/paywalled_papers.md` listing all failed DOIs. The
`summary.md` for failed downloads is written from the Crossref / OpenAlex abstract plus
training-data recall, with an explicit disclaimer in the Overview. this task should plan for a
similar pattern because many of the target morphology-DS papers will come from paywalled venues
(Cell Press, Nature, Elsevier); three of the ten [research_papers.md] corpus references already have
`download_status: "failed"` for this reason.

### Answer-Asset Format Is Standardised at Spec v2 with 3-Doc Layout

Every prior literature-survey task produced **exactly one** answer asset. The folder layout is
identical across [t0002], [t0003], [t0007], [t0008], [t0010], [t0015], [t0016], [t0017], [t0018],
[t0019]: `details.json` (spec_version "2") + `short_answer.md` + `full_answer.md`. The
`details.json` lists `question`, `short_title`, `categories`, `answer_methods`, `source_paper_ids`,
`confidence`, `created_by_task`, `date_created`. `short_answer.md` is approximately 200 words and
answers the question in prose; `full_answer.md` is the long synthesis with structured sections (in
literature surveys, one section per theme or per research question). The [t0002] answer (which
answers "how does the DSGC literature structure the five project RQs") is the closest stylistic
template for this task because it synthesises a large corpus across multiple themes; its
`source_paper_ids` field lists all 20 [t0002] papers as evidence.

### Ten Prior Answer Assets Supply Partial Coverage of this task's Synthesis Question

The answer aggregator returned ten answers. Three are directly relevant and this task's synthesis
answer should explicitly cite or build on them:

1. `how-does-dsgc-literature-structure-the-five-research-questions` ([t0002]) — covers project RQ2
   (morphology sensitivity) in its full answer; provides the per-RQ structure this task can mirror
   at paper-variable granularity.

2. `dendritic-computation-motifs-for-dsgc-direction-selectivity` ([t0016]) — names NMDA spikes, Ca2+
   plateaus, branch-level supralinear integration as motifs plausibly transferable to DSGC
   dendrites. Each motif maps onto a morphology variable (NMDA → input location on dendrite; Ca2+
   plateau → dendritic diameter + branch-order depth; branch supralinearity → branch count and
   branch-order structure). this task should cite this answer in the Mechanism Taxonomy.

3. `cable-theory-implications-for-dsgc-modelling` ([t0015]) — establishes that DS arises from
   postsynaptic dendritic shunting inhibition via the Koch-Poggio-Torre on-the-path mechanism, and
   that models must discretise with the `d_lambda` rule on morphologically accurate reconstructions.
   this task's passive-geometry taxonomy entry is the direct extension of this answer to the
   morphology-sweep question.

Four further answers are tangentially relevant and should be cited as context:
`dsgc-missed- models-survey` ([t0010], lists de Rosenroll 2026 and Poleg-Polsky 2026 as baseline
morphology-DS references), `patch-clamp-techniques-and-constraints-for-dsgc-modelling` ([t0017],
constrains experimental grounding for any predicted DSI),
`synaptic-integration-priors-for-dsgc-modelling` ([t0018], supplies AMPA/NMDA/GABA kinetics that
mediate morphology-DS coupling), and `nav-kv- combinations-for-dsgc-modelling` ([t0019], supplies
AIS Nav/Kv densities that the Schachter 2010 mechanism depends on). The remaining three answers are
about simulator choice, install report, and the ModelDB port and are not referenced in the
morphology-DS synthesis.

### Helper Scripts Exist for DOI Slugging and Duplicate Detection

Two project-level utilities under `arf/scripts/utils/` are directly reusable by this task:

* `arf/scripts/utils/doi_to_slug.py` — canonical DOI-to-folder-name converter. Callable as
  `uv run python -u -m arf.scripts.utils.doi_to_slug "10.1371/journal.pcbi.1000899"` →
  `10.1371_journal.pcbi.1000899`. Required by paper-asset spec v3 (error `PA-E011` is raised on
  hand-converted slugs). Used by every prior literature-survey task.

* `arf/scripts/utils/find_similar_papers.py` — scans every `details.json` across the project,
  detects duplicates by DOI exact match + title-similarity (SequenceMatcher, default threshold 0.5,
  title weight 0.60, author weight 0.30) + year proximity. this task should run this before adding
  each new paper to catch accidental re-download of any of the 48 existing paper assets (especially
  the 5 baseline morphology-DS papers).

### Paper-Download Skills Live Under `meta/asset_types/paper/skills/`

The `add-paper` skill (at `meta/asset_types/paper/skills/add-paper/SKILL.md`, v2) and the
`download_paper` skill (at `meta/asset_types/paper/skills/download_paper/SKILL.md`) encapsulate the
paper-asset creation workflow: identifier resolution, PDF download, `details.json` generation,
9-section `summary.md` authoring, and verificator invocation. this task should invoke `/add-paper`
for each of the 12-25 new papers rather than hand-authoring `details.json` and `summary.md`. The
skills handle the `download_status: "failed"` path for paywalled venues automatically.

### Paper-Asset and Answer-Asset Verificators Live Under `meta/asset_types/`

Rather than under `arf/scripts/verificators/`, the asset-type verificators for papers and answers
live at `meta/asset_types/paper/verificator.py` and `meta/asset_types/answer/verificator.py`. This
mirror-layout is a recent refactor and differs from the older `arf/scripts/verificators/` pattern
shown in some prior `research_code.md` files. The canonical invocation is
`uv run python -u -m meta.asset_types.paper.verificator --task-id <task_id>` and
`uv run python -u -m meta.asset_types.answer.verificator --task-id <task_id>`. this task must run
both before marking the implementation step complete.

### Aggregator Set in This Repository Is Asymmetric

The `arf/scripts/aggregators/` folder ships aggregators only for tasks, costs, machines, metrics,
metric-results, suggestions, categories, and task-types. The asset aggregators (papers, answers,
libraries, datasets, models, predictions) live under `meta/asset_types/<type>/aggregator.py` and are
invoked as `uv run python -u -m meta.asset_types.<type>.aggregator`. The
`arf/docs/reference/aggregators.md` document lists both sets and is authoritative. this task's
synthesis reporting should use the `meta.asset_types.paper.aggregator` to enumerate the final corpus
rather than walking `tasks/` directly, per project Rule 9.

## Reusable Code and Assets

Because no library in `assets/library/` is relevant, every item below is either a **copy into task**
read-only template or a **project-level utility** invoked directly (not copied, not
imported-as-library — used via `uv run python -u -m <module>`).

* **Source**: `meta/asset_types/paper/specification.md` (project-level spec, v3)
  * **What it does**: Authoritative format for every paper asset — `details.json` fields,
    `summary.md` frontmatter, 9 mandatory sections, `files/` layout, verificator error codes
    (`PA-E001`-`PA-E015`) and warning codes (`PA-W001`-`PA-W011`).
  * **Reuse method**: read-only specification; **no copy needed**. Read once before authoring any
    paper asset.
  * **Adaptation needed**: None.

* **Source**: `meta/asset_types/answer/specification.md` (project-level spec, v2)
  * **What it does**: Authoritative format for answer assets — `details.json` (spec_version "2"),
    `short_answer.md` (~200 words), `full_answer.md` (long synthesis).
  * **Reuse method**: read-only specification; **no copy needed**.
  * **Adaptation needed**: None.

* **Source**: `arf/scripts/utils/doi_to_slug.py` (project-level utility, ~100 lines)
  * **What it does**: Converts a DOI (or `https://doi.org/...` URL) to a filesystem-safe folder
    slug. Strips prefixes, replaces `/` with `_`, validates output. Required by paper spec v3
    (`PA-E011`).
  * **Reuse method**: **invoke as CLI module** —
    `uv run python -u -m arf.scripts.utils.doi_to_slug "<doi>"`. Not a library import.
  * **Function signatures**: module exposes `doi_to_slug(doi: str) -> str`.
  * **Adaptation needed**: None.

* **Source**: `arf/scripts/utils/find_similar_papers.py` (project-level utility)
  * **What it does**: Scans every paper `details.json` in the project, reports potential duplicates
    by DOI + title-similarity + author-set overlap + year proximity. Default threshold 0.5.
  * **Reuse method**: **invoke as CLI module** before adding a new paper asset. Not a library.
  * **Adaptation needed**: None.

* **Source**: `meta/asset_types/paper/skills/add-paper/SKILL.md` (project-level skill, v2)
  * **What it does**: End-to-end paper addition — resolves identifiers, downloads the PDF, writes
    `details.json`, generates the 9-section `summary.md`, runs the verificator.
  * **Reuse method**: **invoke as `/add-paper` in each paper step**. No code copy.
  * **Adaptation needed**: pass the DOI / title / arXiv ID per paper.

* **Source**: `meta/asset_types/paper/skills/download_paper/SKILL.md` (project-level skill)
  * **What it does**: Lower-level helper — resolves a paper identifier to a PDF and metadata without
    building the full asset. Used by `/add-paper` as a sub-step and callable standalone for PDF-only
    fetch experiments.
  * **Reuse method**: **invoke as `/download_paper` for edge cases** where `/add-paper`'s full
    pipeline is not wanted.
  * **Adaptation needed**: None.

* **Source**: `tasks/t0018_literature_survey_synaptic_integration/code/fetch_paper_metadata.py` (~78
  lines)
  * **What it does**: Bulk Crossref metadata fetcher driven by a `SHORTLIST` constant. Useful when
    `/add-paper` is too interactive for a 15-paper batch and a machine-readable metadata cache is
    wanted as a preflight.
  * **Reuse method**: **copy into `tasks/t0027_.../code/` and adjust `SHORTLIST`** to the ~15 target
    DOIs. Only needed if the batch is authored as a parallel paper-asset build rather than one
    `/add-paper` invocation at a time.
  * **Function signatures**: `fetch(doi: str, polite_email: str) -> MetadataRecord`, driven by
    `main() -> None` that iterates `SHORTLIST`.
  * **Adaptation needed**: replace `SHORTLIST` entries with the ~15 morphology-DS DOIs; adjust
    output path. Keep `polite_email` pointing to the user's email for the Crossref User-Agent.
  * **Line count**: ~78 lines (near-verbatim copy).

* **Source**: `tasks/t0018_literature_survey_synaptic_integration/code/build_paper_asset.py` (~829
  lines)
  * **What it does**: Consumes the Crossref cache and materialises each paper folder with a spec-v3
    `details.json` and a 9-section `summary.md` template pre-filled with Crossref abstract. Handles
    the `download_status: "failed"` path including `.gitkeep` in `files/`.
  * **Reuse method**: **copy into `tasks/t0027_.../code/` and adjust `TASK_ID`, `THEME_CATEGORIES`,
    and per-theme abstract-to-summary templates**. Alternative to the per-paper `/add-paper`
    invocation for bulk builds.
  * **Function signatures**: `build_asset(record: MetadataRecord) -> None`, `main() -> None`.
  * **Adaptation needed**: moderate — update category assignment logic so each paper gets
    `direction-selectivity` + `compartmental-modeling` (or `dendritic-computation`,
    `retinal-ganglion-cell`) per the task description's category rules; update the per-theme
    Overview seed text.
  * **Line count**: ~829 lines (most changes concentrated in the top constants block).

* **Source**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md`
  (215 lines)
  * **What it does**: Canonical full-PDF paper summary following spec v3 — 9 sections, 1000+ words,
    specific quantitative numbers in Results. Used as stylistic template by [t0016] and [t0019].
  * **Reuse method**: **read-only template** for the morphology-DS summaries that are downloaded
    successfully (Schachter 2010, Jain 2020 pattern).
  * **Adaptation needed**: None — used as a stylistic reference.

* **Source**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/full_answer.md`
  * **What it does**: Canonical large-corpus synthesis answer. Groups 20 papers by project RQ,
    supplies quantitative targets per RQ, lists all 20 papers in `source_paper_ids`.
  * **Reuse method**: **read-only structural template** for this task's answer asset. The sectioning
    (one `##` per theme) maps directly onto this task's "morphology variable taxonomy" + "mechanism
    taxonomy" structure.
  * **Adaptation needed**: restructure sections from per-RQ to per-morphology-variable plus
    per-mechanism; replace `source_paper_ids` with the 5 baseline + 12-25 new DOIs.

* **Source**:
  `tasks/t0016_literature_survey_dendritic_computation/assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/`
  * **What it does**: Concise 5-paper synthesis with per-motif sections and per-motif caveats.
    Closer in scale to this task's synthesis if the corpus lands at ~15 new + 5 baseline.
  * **Reuse method**: **read-only template**. Second choice after [t0002]'s answer.
  * **Adaptation needed**: extend to ~20 papers; add the "gaps and contradictions" section required
    by this task's task description.

* **Source**: `meta/asset_types/paper/verificator.py` and `meta/asset_types/answer/verificator.py`
  * **What it does**: Enforce spec v3 (papers) / spec v2 (answers). Error codes `PA-E001`-`PA-E015`
    and `AN-E*`. Must pass with zero errors before commit.
  * **Reuse method**: **invoke as CLI** —
    `uv run python -u -m meta.asset_types.paper.verificator --task-id <task_id>` and
    `uv run python -u -m meta.asset_types.answer.verificator --task-id <task_id>`.
  * **Adaptation needed**: None.

* **Source**: `arf/scripts/verificators/verify_research_code.py` (used by this very step)
  * **What it does**: Validates `research_code.md` against the spec — frontmatter fields, mandatory
    sections, citation-to-index round-trip, per-section minimum word counts.
  * **Reuse method**: **invoke as CLI** —
    `uv run python -u -m arf.scripts.verificators.verify_research_code t0027_literature_survey_morphology_ds_modeling`.
  * **Adaptation needed**: None.

There is no computational code to copy for the actual analytical work of this task. The paper
summarisation, the morphology-variable taxonomy, and the mechanism taxonomy are authored by hand
from paper content; no pre-existing library fits. The Crossref fetcher and paper-asset builder from
[t0018] are mechanical helpers for batch construction — optional if `/add-paper` is invoked per
paper.

## Lessons Learned

Drawn from the results and plans of prior literature-survey tasks ([t0002], [t0010], [t0013],
[t0015], [t0016], [t0017], [t0018], [t0019]) and the dependency ports ([t0008], [t0022], [t0024]):

* **Paywall rate is high in morphology-DS venues.** [t0015], [t0016], [t0018], [t0019] each saw 100%
  paywall-failure rates (Nature, Science, Nat Neurosci, Annual Reviews, AAAS). Three of ten papers
  in this task's own `research_papers.md` corpus already have `download_status: "failed"`. Plan for
  ~30-50% of new DOIs to fail automated download and require `intervention/paywalled_papers.md`
  handling.

* **`doi_to_slug` is mandatory.** Hand-conversion of DOIs triggers `PA-E011` and fails the
  verificator. Every prior task enforces this.

* **Summary word-count minimums matter.** `PA-W001` (summary < 500 words), `PA-W002` (Results < 5
  bullets), `PA-W003` (Main Ideas < 3 bullets), `PA-W004` (Summary section not 4 paragraphs). Prior
  tasks found ~800-1200 words per summary is the safe operating point; paywalled-abstract summaries
  can still reach this with training-data recall but require the explicit "abstract-based with
  training-data augmentation" disclaimer.

* **Flowmark is mandatory pre-commit.** Every completed literature-survey task had at least one
  pre-commit failure that was fixed by running `uv run flowmark --inplace --nobackup <file.md>`.
  Batch all edited markdown through flowmark before any commit.

* **Answer asset `source_paper_ids` must list every cited DOI.** [t0002]'s answer lists all 20
  papers; [t0016]'s lists all 5. Orphan citations (inline reference without a `source_paper_ids`
  entry) and unused entries (listed but never cited in `full_answer.md`) both trigger verificator
  issues.

* **Duplication detection saves re-work.** [t0010] found two "missed" DSGC models that turned out to
  be the same model under two different ModelDB entries. Run `find_similar_papers.py` on every
  candidate DOI before adding to avoid re-downloading existing assets (including the five this task
  baseline papers that live in [t0002], [t0010], [t0013] folders).

* **Prior tasks recommended sweeping morphology but never did.** [t0002]'s RQ2 ("morphology
  sensitivity"), [t0009]'s diameter calibration, [t0013]'s provenance resolution, and [t0026]'s
  V_rest sweep all end with the same observation: the morphology-variable effect on DSI is unknown
  within this project's testbeds. this task is the literature prelude to the sweep that neither
  [t0022]/[t0024] nor [t0026] could run; its synthesis should rank morphology variables by expected
  information gain on that downstream sweep.

* **The `de_rosenroll_2026_dsgc` and `modeldb_189347_dsgc_dendritic` libraries are the natural
  downstream consumers.** [t0024] and [t0022] already have the scaffolding to plug a new morphology
  in and re-run the 12-angle sweep. this task's morphology-variable recommendations should be framed
  in terms of what these two libraries can evaluate without further library changes (i.e., what
  knobs already exist: `build_cell.py` parameters, HOC morphology file swaps).

* **Aggregators must be preferred over filesystem walks.** Project Rule 9 and the prior [t0019]
  research_code step both reinforce using `meta.asset_types.paper.aggregator` over
  `ls tasks/*/assets/paper/`; raw walks miss the corrections overlay from [t0013] and any future
  morphology-related corrections.

## Recommendations for This Task

Prioritised and concrete, derived from the findings above:

1. **Invoke `/add-paper` per new DOI** rather than hand-authoring paper folders. The skill handles
   identifier resolution, PDF attempt, `details.json` generation, and the 9-section `summary.md`
   template end-to-end. Fall back to the [t0018] `fetch_paper_metadata.py` + `build_paper_asset.py`
   batch path only if the ~15-paper scale makes interactive per-paper authoring prohibitive.

2. **Run `find_similar_papers.py` before every new paper addition** to guarantee no duplicate of the
   5 baseline papers (which live in [t0002], [t0010], [t0013] folders) or of any of the other 43
   project papers. Use the default 0.5 threshold.

3. **Plan for ~30-50% paywall failure rate.** Seed `intervention/paywalled_papers.md` up front with
   a blank list. For failed downloads, write abstract-based summaries with the explicit disclaimer
   used by [t0015] and [t0016]; keep the 9-section format.

4. **Mirror [t0002]'s answer structure for the synthesis answer.** Use `details.json` spec v2 with
   `source_paper_ids` listing all 5 baseline + new DOIs. Structure `full_answer.md` as (a)
   morphology-variable taxonomy (one `##` per variable), (b) mechanism taxonomy (one `##` per
   mechanism), (c) gaps-and-contradictions, (d) 3-5 morphology-sweep recommendations for
   [t0022]/[t0024]. `short_answer.md` at ~200 words.

5. **Cite the three directly-related prior answers** in the synthesis: [t0002]'s five-RQ answer (RQ2
   morphology sensitivity), [t0016]'s dendritic-computation motifs answer (mechanism transfer to
   DSGCs), [t0015]'s cable-theory answer (passive-geometry baseline). List their `answer_id`s in a
   "Related Prior Conclusions" subsection of `full_answer.md`.

6. **Frame recommendations in terms of the existing [t0022] / [t0024] libraries' knobs.** The
   downstream morphology-sweep experiment cannot invent new scaffolding — each recommended sweep
   must be phrased as a change to either `modeldb_189347_dsgc_dendritic.build_cell.py` parameters or
   `de_rosenroll_2026_dsgc.build_cell.py` parameters (or as an HOC-morphology- file swap that those
   libraries can consume).

7. **Use `meta.asset_types.paper.aggregator --task-id t0027_... --format ids`** in the
   results-reporting step to enumerate this task's final paper corpus rather than walking
   `tasks/t0027_.../assets/paper/`.

8. **Do not build a new library.** The task is pure literature + answer synthesis; no Python module
   should be registered under `assets/library/`. Any helper scripts (e.g., a duplicate-adjusted copy
   of [t0018]'s builder) stay in `tasks/t0027_.../code/` and are never registered.

9. **Run the paper and answer verificators before commit.** Invoke
   `uv run python -u -m meta.asset_types.paper.verificator --task-id t0027_literature_survey_morphology_ds_modeling`
   and
   `uv run python -u -m meta.asset_types.answer.verificator --task-id t0027_literature_survey_morphology_ds_modeling`,
   and fix all errors before the implementation step's final commit.

## Task Index

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: compartmental models of DS retinal ganglion cells
* **Status**: completed
* **Relevance**: Original 20-paper DSGC survey. Holds two of the five this task baseline papers
  (Schachter 2010 `10.1371_journal.pcbi.1000899`; Jain 2020 `10.7554_eLife.52949`; Hanson 2019;
  Taylor 2002). Its answer `how-does-dsgc-literature-structure-the-five-research-questions` is the
  closest stylistic template for this task's synthesis answer, and its 20 summaries define the
  spec-v3 paper-summary layout this task must reproduce.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Produced the `modeldb_189347_dsgc` library. this task does not use this library
  directly but cites it in recommendations as the t0022/t0024 testbed chain's origin; [t0022]'s
  `modeldb_189347_dsgc_dendritic` is a descendant.

### [t0010]

* **Task ID**: `t0010_hunt_missed_dsgc_models`
* **Name**: Hunt DSGC compartmental models missed by prior survey; port runnable ones
* **Status**: completed
* **Relevance**: Holds two of the five this task baseline papers (Poleg-Polsky 2026
  `10.1038_s41467-026-70288-4`; de Rosenroll 2026 `10.1016_j.celrep.2025.116833`). Its answer
  `dsgc-missed-models-survey` lists both as the two newest morphology-DS references.

### [t0013]

* **Task ID**: `t0013_resolve_morphology_provenance`
* **Name**: Resolve dsgc-baseline-morphology source-paper provenance
* **Status**: completed
* **Relevance**: Holds the fifth this task baseline paper (Morrie & Feller 2018
  `10.1016_j.cub.2018.03.001`). Its correction asset (`C-0013-01`) sets the dsgc-baseline-morphology
  source paper — this task's morphology-sweep recommendations run on top of that morphology.

### [t0015]

* **Task ID**: `t0015_literature_survey_cable_theory`
* **Name**: Literature survey: cable theory and dendritic filtering
* **Status**: completed
* **Relevance**: Paywalled-only survey template. Its answer
  `cable-theory-implications-for-dsgc-modelling` is directly cited in this task's passive- geometry
  taxonomy entry (Koch-Poggio-Torre on-the-path shunting). Also demonstrates the
  paywalled-paper-with-abstract-only summary pattern.

### [t0016]

* **Task ID**: `t0016_literature_survey_dendritic_computation`
* **Name**: Literature survey: dendritic computation beyond DSGCs
* **Status**: completed
* **Relevance**: Its answer `dendritic-computation-motifs-for-dsgc-direction-selectivity` maps NMDA
  spikes, Ca2+ plateaus, branch-supralinearity onto DSGC dendrites — each motif corresponds to a
  morphology variable this task must index. Second-choice answer-asset structural template.

### [t0017]

* **Task ID**: `t0017_literature_survey_patch_clamp`
* **Name**: Literature survey: patch-clamp recordings of RGCs and DSGCs
* **Status**: completed
* **Relevance**: Its answer `patch-clamp-techniques-and-constraints-for-dsgc-modelling` constrains
  the experimental grounding for any morphology-predicted DSI; provides space-clamp-error priors
  this task will cite alongside Schachter 2010's 40-100% distal space-clamp-error finding.

### [t0018]

* **Task ID**: `t0018_literature_survey_synaptic_integration`
* **Name**: Literature survey: synaptic integration in RGC-adjacent systems
* **Status**: completed
* **Relevance**: Ships `fetch_paper_metadata.py` (~78 lines) and `build_paper_asset.py` (~829 lines)
  — the optional batch pipeline this task can copy if `/add-paper` is too interactive for a 15-paper
  batch. Also supplies AMPA/NMDA/GABA kinetic priors the synthesis cites.

### [t0019]

* **Task ID**: `t0019_literature_survey_voltage_gated_channels`
* **Name**: Literature survey: voltage-gated channels in retinal ganglion cells
* **Status**: completed
* **Relevance**: Its answer `nav-kv-combinations-for-dsgc-modelling` supplies the AIS Nav/Kv density
  priors the Schachter 2010 active-dendritic-spike mechanism depends on; cited as context in this
  task's mechanism taxonomy.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: Produced the `modeldb_189347_dsgc_dendritic` library, one of the two downstream
  testbeds this task's morphology-sweep recommendations target. Its `build_cell.py` and HOC
  morphology-swap hooks determine which morphology knobs this task should prioritise.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Produced the `de_rosenroll_2026_dsgc` library, the second downstream testbed. Its
  `ar2_noise.py` + `build_cell.py` define the second set of knobs this task's morphology sweeps will
  target. Its paper asset (de Rosenroll 2026) is one of the five baseline references.

### [t0026]

* **Task ID**: `t0026_vrest_sweep_tuning_curves_dsgc`
* **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
* **Status**: completed
* **Relevance**: Found that neither [t0022] nor [t0024] simultaneously reproduces published DSI and
  peak firing rate at any biologically plausible V_rest. This is the headline motivation for this
  task — the morphology-variable survey that must identify which morphology variable to sweep next
  to close the 15 Hz vs 148 Hz peak-rate gap at DSI ~0.66.

### [t0003]

* **Task ID**: `t0003_simulator_library_survey`
* **Name**: Simulator library survey for DSGC compartmental modelling
* **Status**: completed
* **Relevance**: Produced the `dsgc-compartmental-simulator-choice` answer asset establishing the
  answer-asset layout that this task mirrors. Cited as one of the tasks whose answer-asset folder
  structure is the structural precedent for this task's synthesis answer.

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate canonical target angle-to-AP-rate tuning curve
* **Status**: completed
* **Relevance**: Produced the `target-tuning-curve` dataset that the downstream morphology-sweep
  experiments (on the `modeldb_189347_dsgc_dendritic` and `de_rosenroll_2026_dsgc` libraries) score
  against. This task's morphology recommendations are framed relative to that target envelope.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain
* **Status**: completed
* **Relevance**: Produced the `neuron-netpyne-install-report` answer asset, one of the ten
  pre-existing answers enumerated by the answer aggregator. Cited as context in the answer-asset
  format discussion.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: Calibrated the DSGC dendritic diameter taper — this is one of the morphology
  variables this task's synthesis will analyse; cited as the project's prior in-scope work on
  dendritic diameter.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: Produced the `tuning_curve_viz` library, one of the six in the Library Landscape
  inventory. Listed as not-relevant to this task because it consumes tuning-curve CSVs that this
  task does not generate.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Produced the `tuning_curve_loss` library, one of the six in the Library Landscape
  inventory. Downstream morphology-sweep experiments on t0022/t0024 will consume this library but
  this task itself does not.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Produced the `modeldb_189347_dsgc_gabamod` library, one of the six in the Library
  Landscape inventory. Not relevant to this task directly, but demonstrates the pattern of producing
  a sibling port under a different DS-induction protocol — a pattern that a morphology-sweep
  follow-up task could follow.
