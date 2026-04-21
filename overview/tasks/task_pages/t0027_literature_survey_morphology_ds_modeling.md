# ⏳ Literature survey: modeling effect of cell morphology on direction selectivity

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0027_literature_survey_morphology_ds_modeling` |
| **Status** | ⏳ in_progress |
| **Started** | 2026-04-21T18:33:02Z |
| **Task types** | `literature-survey`, `answer-question` |
| **Expected assets** | 15 paper, 1 answer |
| **Task folder** | [`t0027_literature_survey_morphology_ds_modeling/`](../../../tasks/t0027_literature_survey_morphology_ds_modeling/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0027_literature_survey_morphology_ds_modeling/task_description.md)*

# Literature Survey: Modeling the Effect of Cell Morphology on Direction Selectivity

## Motivation

Our recent V_rest sweep (`t0026`) on the t0022 (deterministic ModelDB 189347 port) and t0024
(de Rosenroll 2026 AR(2)-correlated stochastic port) DSGC compartmental models produced a
headline finding: neither port simultaneously reproduces the published DSI (0.45–0.67) and the
published peak firing rate (40–166 Hz) at any biologically plausible resting potential. Both
ports use a single fixed dendritic morphology — `dsgc-baseline-morphology` for t0022/t0024 —
and we have not yet asked how much of the gap is attributable to morphology versus channels,
synaptic kinetics, or input statistics.

Before we commit compute and engineering effort to a morphology-sweep experiment on these
testbeds, we need to know what the published modeling literature already says: which
morphology variables (dendritic length, branch order, segment diameter, asymmetry, input
layout on dendrites, soma-dendrite ratios, etc.) have been shown to affect direction
selectivity, by what causal mechanisms, and where the published findings disagree or have
gaps. This survey directly informs the design of follow-up experiments on t0022/t0024 and
constrains which morphology dimensions are worth sweeping.

## Scope

Survey the published computational, biophysical, and theoretical modeling literature on the
effect of neuronal cell morphology on direction selectivity. Primary focus: retinal
direction-selective ganglion cells (DSGCs — ON, OFF, ON-OFF subtypes) and starburst amacrine
cells (SACs). Secondary focus: other direction-selective neurons (cortical V1 / MT, fly lobula
plate / motion-sensitive neurons, vestibular nuclei) where morphology is treated as a
manipulated variable in a model.

### Already-covered baseline

Five papers in our existing corpus already meet the inclusion criteria below and were
identified during a prior in-session corpus search. **Do NOT re-download these** — link to
them by `paper_id` in the synthesis report and cite them alongside any new papers found:

* `10.1371_journal.pcbi.1000899` — Schachter 2010 — dendrite electrotonic length × Na density
  distribution → spike-DSI amplification (NeuronC compartmental)
* `10.7554_eLife.52949` — Jain 2020 — dendritic compartment scale (5–10 µm) × CaV/NMDA
  thresholding → dendritic Ca²⁺ DSI (NEURON + 2P imaging)
* `10.1016_j.cub.2018.03.001` — Morrie 2018 — SAC arbor size & plexus density (Sema6A−/−) →
  DSGC spike DSI collapse (TREES-toolbox IPSC simulation)
* `10.1038_s41467-026-70288-4` — Poleg-Polsky 2026 — bipolar input location on dendrite ×
  A-type K × NMDA ratio × passive Rm/Cm via ML search → DSI mechanisms (NEURON + ML)
* `10.1016_j.celrep.2025.116833` — de Rosenroll 2026 — SAC GABA/ACh spatial offset × subunit
  E/I geometry → subunit-level DSI (NEURON network)

The task's job is to **extend** coverage beyond these five, not duplicate them.

## Inclusion Criteria

A paper is included if it satisfies **all three** criteria:

1. **Builds a model** — compartmental simulation (NEURON, Arbor, NetPyNE, Brian, GENESIS,
   NeuronC, custom solver), cable-theory derivation, or abstract neural network model with
   explicit morphology (not just point neurons).
2. **Morphology is a manipulated or causally-relevant variable** — dendritic branching
   pattern, branch order, dendritic length, segment diameter, surface area, soma-dendrite
   ratio, asymmetric vs symmetric arbors, isotropic vs anisotropic arbors,
   primary/secondary/tertiary hierarchy, or the spatial layout of synaptic inputs ON the
   dendrites. Just *using* a morphology without varying it does not qualify.
3. **Direction selectivity as outcome** — directional tuning curves, DSI / DS index,
   preferred-vs- null direction asymmetry, vector-sum direction, or equivalent measure of
   direction-dependent firing or PSP.

### Borderline cases — include and flag

* **SAC morphology → DS** papers — include; flag as `"SAC, not DSGC"`.
* **Passive cable theory** papers deriving DS from input asymmetry on a passive cylinder —
  include; flag as `"passive cable, geometry-only"`.
* **Insect / invertebrate DS-circuit** modeling — include if morphology is varied; flag
  organism (e.g., `"Drosophila lobula plate"`, `"hawkmoth"`).
* **Cortical or subcortical DS neurons** modeled with morphology variation — include; flag
  region.

### Borderline cases — exclude

* Papers fitting DSI to **one fixed morphology** without varying it — exclude; they do not
  model the *effect* of morphology.
* Pure **NMDA-Mg-block** or pure **E/I-timing** papers without morphology variation — exclude.
* Pure experimental papers (no model) — exclude unless the experimental finding is explicitly
  used to constrain a model in the same paper.

## Search Strategy

### Citation-graph expansion

Pull forward and backward citations for each of the five baseline papers using:

* Google Scholar "Cited by" — forward citation graph
* OpenCitations / Semantic Scholar API — both directions
* Each paper's reference list — backward citations

### Targeted keyword searches

Run on Google Scholar, PubMed, bioRxiv, arXiv:

* `"DSGC compartmental model morphology"`
* `"direction selectivity dendritic geometry"`
* `"starburst amacrine cell morphology direction selectivity"`
* `"asymmetric dendritic arbor direction selective"`
* `"branch order morphology direction tuning"`
* `"compartmental model dendritic length DSI"`
* `"cable theory direction selective neuron"`
* `"synaptic input asymmetry dendritic compartment direction"`

### Author-targeted searches

Pull recent and seminal works from authors known to publish in this space:

* Sebastian Espinosa (Schachter senior author), Greg Field, Marla Feller, Jonathan Demb,
  Florentina Soto, Alex Poleg-Polsky, Justin de Rosenroll, Stuart Trenholm, Anastasia Jain,
  Adam Mani, Wei Wei, David Berson, Richard Masland, Robert Smith.

### Repository searches

* **ModelDB** (`modeldb.science`) — search for compartmental DSGC and SAC models; each model
  entry typically links to one or more publications.
* **SenseLab Yale** — DSGC-related model lookups.
* **Open Source Brain** — published compartmental model collection.

### Beyond retina

Do not limit to retinal DSGCs. Include:

* Classic cable-theory papers (Rall, Branco-Häusser-Clark) deriving DS from input pattern
  asymmetry on dendritic geometry.
* Cortical DS modeling (V1 simple/complex cells, MT) where morphology is varied.
* Fly motion-sensitive neuron modeling (HS/VS cells, T4/T5) where dendritic geometry is
  varied.

## Budget and Stop Criterion

**Target**: 12–20 new paper assets downloaded and summarised (in addition to the 5 baseline
papers, for a final corpus of ~17–25 morphology-DS papers).

**Stop criterion**: stop earlier if returns diminish — when newly-found candidates stop
satisfying the inclusion criteria or stop introducing novel mechanisms / morphology variables.
Push to **25 new papers** if novel mechanisms keep appearing (e.g., a previously-unknown class
of morphology manipulation shows up).

**Per-paper cost**: $0. No paid APIs. PDF retrieval is via open access, preprint servers, or
Sheffield institutional access (VPN / SSO). For paywalled PDFs that cannot be retrieved (e.g.,
Cell Press / Elsevier / Springer-Nature / Wiley), generate an intervention file in
`intervention/` rather than blocking the survey — record the metadata and abstract from the
landing page, mark `download_status: "failed"` in `details.json`, and proceed.

## Deliverables

`expected_assets`: `{"paper": 15, "answer": 1}` — the `15` is the midpoint of the 12–20 target
range; the actual count may legitimately fall anywhere in 12–25 depending on the stop
criterion.

### 1. Paper assets (target 12–20)

Each new paper assets goes under
`tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/<paper_id>/` and follows
`meta/asset_types/paper/specification.md` exactly:

* `details.json` with all required fields, including all relevant `categories` from
  `meta/categories/`
* `summary.md` with all mandatory sections (Metadata, Abstract, Overview, Architecture/Models/
  Methods, Results, Innovations, Datasets, Main Ideas, Summary), summarised after reading the
  full paper text per the spec
* `files/` containing at minimum the PDF (or markdown conversion if no PDF is available)

For every included paper, the `summary.md` must explicitly note in the `## Architecture,
Models and Methods` section: which morphology variable was manipulated, how it was manipulated
(range, levels, parametric vs categorical), and the DS metric reported.

### 2. Answer asset

One answer asset at
`tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/morphology-direction-selectivity-modeling-synthesis/`
following `meta/asset_types/answer/specification.md`.

Question (verbatim, to appear in the answer asset's `details.json`):

> **What variables of neuronal morphology have been shown by computational modeling to affect
> direction selectivity, by what mechanisms, and what gaps remain?**

The answer must cite by `paper_id` every paper used as evidence — both the 5 baseline papers
(from t0002, t0010, t0013, t0024) and every new paper added in this task. Confidence level
should reflect the consistency of findings across papers and across modelling approaches.

### 3. `results_detailed.md` synthesis

Required sections (in this order):

* **Coverage table** — one row per included paper (baseline + new). Columns: `paper_id`,
  first-author year, organism / cell type, morphology variable manipulated, DS outcome
  measured, model type, mechanism flag.
* **Morphology variable taxonomy** — group findings by which variable was studied: dendritic
  length, branch count, branch order, segment diameter, total surface area, asymmetric vs
  symmetric arbor, input-on-dendrite spatial layout, soma-dendrite ratio, dendritic
  compartmentalisation scale. For each variable: how many papers studied it, what range was
  swept, what direction the effect on DSI went, and the strength of the consensus.
* **Mechanism taxonomy** — group findings by causal mechanism: electrotonic
  compartmentalisation, dendritic spike thresholding, NMDA-Mg gating in dendritic context,
  delay lines via dendritic cable propagation, coincidence detection at branch points,
  asymmetric SAC inhibition driven by presynaptic geometry, leak-driven attenuation,
  axial-resistance-driven sequence selectivity.
* **Gaps and contradictions** — which morphology variables are under-explored in the
  literature, where published findings disagree (e.g., Schachter 2010 vs Jain 2020 on the
  dominant scale of compartmentalisation), and which findings are most replicable across labs
  / model frameworks.
* **Recommendations** — 3–5 concrete morphology-sweep experiments worth running on our t0022 /
  t0024 testbeds, prioritised by expected information gain. Each recommendation must specify:
  the morphology variable to sweep, the range and step size, the predicted effect on DSI /
  peak firing rate based on the literature, and which baseline paper the prediction comes
  from.

### 4. `results_summary.md`

A 2–3 paragraph executive summary with headline findings: how many papers were found in total
(baseline + new), which morphology variables have the strongest cross-paper evidence, what the
field disagrees on, what the project should sweep first on the t0022 / t0024 testbeds.

## Categories

For each new paper, mark with the most specific applicable subset of: `direction-selectivity`,
`compartmental-modeling`, `dendritic-computation`, `retinal-ganglion-cell`. Add `cable-theory`
for passive-cable theoretical papers, `patch-clamp` only if the paper jointly contributes
patch-clamp data plus a morphology-varying model, `synaptic-integration` if the morphology
variation is on synaptic input layout.

## Dependencies

**None.** This is an independent literature survey that runs in parallel with any active
experimental work on t0022 / t0024 / t0026 follow-ups.

## Compute and Budget

* No remote compute.
* No paid API.
* Runs entirely on the local Windows workstation using existing tooling (paper-download skill,
  paper-asset spec).
* PDF retrieval may require Sheffield VPN or institutional SSO for paywalled journals — flag
  as intervention if a needed PDF cannot be retrieved.
* Estimated wall time: 4–8 hours of human-supervised execution, depending on how many
  borderline papers require careful judgment calls and how many PDFs are paywalled.

## Key Questions (numbered, falsifiable)

1. Which morphology variable (dendritic length, branch count, segment diameter, asymmetry,
   input layout) has the **most cross-paper evidence** for affecting DSI in DSGCs and SACs?
2. Is the **dominant compartmentalisation scale** for direction selectivity at the level of
   whole dendrites (Schachter 2010), 5–10 µm sub-segments (Jain 2020), or somewhere else?
3. Where do **published findings disagree**, and is the disagreement attributable to species
   (mouse vs rabbit), cell-type (ON vs OFF vs ON-OFF), simulator (NEURON vs NeuronC vs
   custom), or genuine biological diversity?
4. Which **3–5 morphology sweeps** should we prioritise on t0022 / t0024 next, given our
   headline gap (peak firing rate 15 Hz at DSI 0.66, vs published 148 Hz)?
5. Is there a **published morphology that simultaneously reproduces DSI ≈ 0.5 AND peak firing
   rate ≈ 100 Hz** in a compartmental model? If so, what makes that morphology different from
   `dsgc-baseline-morphology`?

## Risks and Fallbacks

* **PDF paywall**: flag as intervention; abstract-only summary is acceptable for paywalled
  papers if the abstract contains enough information to confirm inclusion.
* **Borderline judgment calls**: when the inclusion criteria are ambiguous for a given paper,
  default to **include and flag**, with a brief borderline note in the paper's `summary.md`.
  The synthesis report can re-exclude flagged papers if the synthesis-stage review finds the
  morphology link too weak.
* **Search exhaustion before target hit**: if fewer than 12 new papers are found after
  exhausting the search strategy, document the gap in `results_summary.md` and proceed with
  whatever coverage was achieved. Do not pad the corpus with weakly-relevant papers to meet
  the count.
* **Search overshoot**: if more than 25 strong candidates are found, prioritise by recency
  (post-2010) and by mechanism novelty, and defer the rest to a follow-up survey task
  suggestion.

## Verification Criteria

* Each new paper asset passes `verify_paper_asset.py` with 0 errors.
* `details.json` for every new paper has a non-empty `categories` field including at least one
  of `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`, or
  `retinal-ganglion-cell`.
* The answer asset cites every included paper by `paper_id` (no orphan citations, no missing
  evidence).
* `results_detailed.md` Coverage Table includes a row for every included paper (baseline +
  new).
* `results_summary.md` opens with a single sentence stating the final paper count and the most
  consensus-supported morphology variable.

</details>
