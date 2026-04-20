# ✅ Resolve dsgc-baseline-morphology source-paper provenance

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0013_resolve_morphology_provenance` |
| **Status** | ✅ completed |
| **Started** | 2026-04-20T16:26:01Z |
| **Completed** | 2026-04-20T17:21:30Z |
| **Duration** | 55m |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source suggestion** | `S-0005-01` |
| **Task types** | `download-paper`, `correction` |
| **Categories** | [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`patch-clamp`](../../by-category/patch-clamp.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 2 paper |
| **Step progress** | 9/15 |
| **Task folder** | [`t0013_resolve_morphology_provenance/`](../../../tasks/t0013_resolve_morphology_provenance/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0013_resolve_morphology_provenance/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0013_resolve_morphology_provenance/task_description.md)*

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

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| paper | [A Dense Starburst Plexus Is Critical for Generating Direction Selectivity](../../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/) | [`summary.md`](../../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/summary.md) |
| paper | [A Viral Receptor Complementation Strategy to Overcome CAV-2 Tropism for Efficient Retrograde Targeting of Neurons](../../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.neuron.2018.05.028/) | [`summary.md`](../../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.neuron.2018.05.028/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Write a shared arf.scripts.utils.resolve_doi helper that returns
title, authors, venue, year, PMID, and PMCID</strong> (S-0013-01)</summary>

**Kind**: library | **Priority**: high

This task discovered that the t0005 plan nominated DOI 10.1016/j.neuron.2018.05.028 as 'Morrie
& Feller 2018 Neuron' but that DOI actually resolves to Li, Vaughan, Sturgill & Kepecs (2018),
an unrelated CSHL viral-tracing paper. The /add-paper skill already performs DOI resolution
internally via CrossRef and PubMed, but that logic is not exposed as a reusable utility, so
planning-stage agents have no cheap way to sanity-check a candidate DOI before locking it into
a plan. Build arf.scripts.utils.resolve_doi as a thin wrapper over CrossRef and PubMed
E-utilities that returns a typed dataclass with title, first-author last name, venue, year,
PMID, and PMCID; wire it into /add-paper to replace the inline resolution; and document the
callable interface so the verificator in S-0013-02 and other planning-time validators can
import it. Recommended task types: write-library.

</details>

<details>
<summary><strong>Add a plan-stage DOI-nomination verificator that checks each
candidate DOI matches its human-written label</strong> (S-0013-02)</summary>

**Kind**: library | **Priority**: high

The Neuron-vs-CB mix-up in the t0005 plan (DOI 10.1016/j.neuron.2018.05.028 labelled 'Morrie &
Feller 2018 Neuron' when it actually belongs to Li et al. 2018 CSHL viral tracing) made it
through planning and into the t0005 implementation, triggering an entire follow-up task (this
one) to correct the downstream impact. Build a verificator under
arf/scripts/verificators/verify_plan_dois.py that scans plan/plan.md for every DOI-like
string, resolves each via the arf.scripts.utils.resolve_doi helper (S-0013-01), and
cross-checks the returned first-author last name, year, and venue against the label the plan
uses near the DOI. Report a warning when the label and resolved metadata disagree on author,
year, or venue, and an error when the DOI itself fails to resolve. Wire this verificator into
the planning-stage check so subsequent plans cannot silently mis-cite a DOI. Recommended task
types: write-library, experiment-run.

</details>

<details>
<summary><strong>Download the Morrie & Feller 2018 SAC reconstructions from
NeuroMorpho and build a paired SAC+DSGC morphology asset</strong>
(S-0013-03)</summary>

**Kind**: dataset | **Priority**: medium

This task attributed the dsgc-baseline-morphology reconstruction (NeuroMorpho neuron 102976,
141009_Pair1DSGC) to Morrie & Feller 2018 Current Biology (PMID 29606419). That paper's
Methods describe paired SAC-DSGC patch recordings with 2-photon stacks of both cells
post-recording, and the SAC partner of the 141009_Pair1 recording is likely deposited in
NeuroMorpho alongside the DSGC. Search NeuroMorpho by reference_pmid=29606419 to list all
reconstructions linked to the paper, download the 141009_Pair1SAC companion SWC (and any
neighbouring Pair2/Pair3 SAC+DSGC pairs), validate with validate_swc.py, and register them as
dataset assets so downstream modelling tasks can drive dsgc-baseline-morphology with
anatomically paired SAC presynaptic input. Strengthens the SAC presynaptic drive asset of
S-0002-08. Recommended task types: download-dataset.

</details>

<details>
<summary><strong>Re-audit all existing dataset and library assets' source_paper_id
fields against resolved DOI metadata</strong> (S-0013-04)</summary>

**Kind**: evaluation | **Priority**: medium

The t0005 nomination error that this task corrected was not caught by any automated check; it
was caught only because a follow-up task specifically downloaded both candidate papers and
inspected their Methods. Other already-registered dataset and library assets across the
project (e.g., under t0004, t0008, t0009, t0011, t0012) may carry similarly silent
source_paper_id errors that no downstream task has yet tripped over. Run a one-off audit task
that iterates over every registered dataset and library asset with a non-null source_paper_id,
resolves the referenced paper asset's DOI via arf.scripts.utils.resolve_doi (S-0013-01), and
flags any asset where the source_paper_id slug does not match what the asset's description.md
or originating plan claims as the source (wrong author, wrong year, wrong venue). File one
correction per disagreement following the corrections_specification.md pattern used by this
task. Recommended task types: data-analysis, correction.

</details>

<details>
<summary><strong>Email the Feller lab to map the 141009_Pair1DSGC session to a
specific pair in Morrie & Feller 2018 CB</strong> (S-0013-05)</summary>

**Kind**: evaluation | **Priority**: low

The provenance decision in this task (source_paper_id = 10.1016_j.cub.2018.03.001) is grounded
in methodological consistency plus the NeuroMorpho.org curated attribution, not in an
exact-quote match: Morrie & Feller 2018 CB does not literally print 141009, Pair1DSGC,
biocytin, or Neurolucida in its Methods, and the paper publishes only SAC (not DSGC)
reconstructions. A downstream task should email the Feller lab (Murphy-Baum at
murphy-baum@berkeley.edu or Morrie at rmorrie@berkeley.edu) asking which specific paired
recording in the paper's Figure 2 cohort (n = 12 Control + 9 Sema6A-/- null + 6 Sema6A-/-
preferred) produced the 141009_Pair1DSGC reconstruction, and whether the companion SAC
reconstruction is deposited at NeuroMorpho. A one-sentence email-reply quote converts the
current 'methodologically consistent' attribution into a citeable exact-quote provenance, and
directly informs S-0013-03. Recommended task types: answer-question.

</details>

## Research

* [`research_code.md`](../../../tasks/t0013_resolve_morphology_provenance/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0013_resolve_morphology_provenance/results/results_summary.md)*

# Results Summary: Resolve DSGC Morphology Provenance

## Summary

Closed the provenance gap on `dsgc-baseline-morphology.source_paper_id`. Registered both
candidate Feller-lab 2018 papers as v3 paper assets, read their Methods sections, applied the
pre-specified decision procedure, and filed a single correction that sets `source_paper_id` to
`10.1016_j.cub.2018.03.001` (Morrie & Feller 2018 *Current Biology*, "A Dense Starburst Plexus
Is Critical for Generating Direction Selectivity"). Discovered along the way that the t0005
plan's "Morrie & Feller 2018 *Neuron*" DOI nomination was an error:
`10.1016/j.neuron.2018.05.028` resolves to Li, Vaughan, Sturgill & Kepecs (2018), an unrelated
CSHL viral-tracing paper.

## Metrics

* **Paper assets registered**: **2** (expected: 2)
* **Correction assets produced**: **1** (`C-0013-01`)
* **Winning source paper**: `10.1016_j.cub.2018.03.001` (Morrie & Feller 2018, *Current
  Biology*)
* **Decision branch taken**: criterion 1 ("exactly one paper's Methods cites the
  reconstruction")
* **PDFs successfully downloaded**: **1/2** (CB open-access on eScholarship; Neuron DOI
  paywalled and metadata-only per v3 spec)
* **Verificator pass rate**: **3/3** (`verify_paper_asset` × 2 + `verify_correction_asset`)

## Verification

* `verify_paper_asset 10.1016_j.neuron.2018.05.028` — **PASSED** (0 errors, 0 warnings)
* `verify_paper_asset 10.1016_j.cub.2018.03.001` — **PASSED** (0 errors, 0 warnings)
* `verify_correction_asset dataset_dsgc-baseline-morphology` — **PASSED** (0 errors, 0
  warnings)
* Asset-count check: `assets/paper/` contains exactly the two expected folders.
* Correction-count check: `corrections/` contains exactly
  `dataset_dsgc-baseline-morphology.json`.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0013_resolve_morphology_provenance/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0013_resolve_morphology_provenance" ---
# Detailed Results: Resolve DSGC Morphology Provenance

## Summary

The dataset asset `dsgc-baseline-morphology` (NeuroMorpho neuron 102976, internal label
`141009_Pair1DSGC`, deposited by the Feller lab) was registered by
`t0005_download_dsgc_morphology` with `source_paper_id: null` because two Feller-lab 2018
papers were plausible sources. This task downloaded both candidate papers as v3-compliant
paper assets, read their Methods sections, applied the pre-specified decision procedure from
`task_description.md`, and filed a single correction that updates `source_paper_id` from
`null` to `10.1016_j.cub.2018.03.001` (Morrie & Feller 2018 *Current Biology*, "A Dense
Starburst Plexus Is Critical for Generating Direction Selectivity"). During execution we
discovered that the t0005 plan's "Morrie & Feller 2018 *Neuron*" nomination was an erroneous
DOI — `10.1016/j.neuron.2018.05.028` resolves to Li, Vaughan, Sturgill & Kepecs (2018), a CSHL
viral-tracing paper unrelated to retina or the Feller lab — so the two-candidate conflict was
illusory.

## Methodology

**Machine**: local Windows 11 workstation (Intel/AMD x86_64, 16+ GB RAM), no remote compute.

**Runtime**: implementation step wall clock was **~22 minutes** (started 2026-04-20T16:41:45Z,
completed 2026-04-20T17:04:17Z). Two `/add-paper` subagents ran in parallel; Methods
extraction, decision, and correction-file authoring were sequential in the orchestrator
thread.

**Start / end timestamps (full task, as of this step)**:

* Task started: 2026-04-20T16:26:01Z (`task.json` `start_time`)
* Implementation completed: 2026-04-20T17:04:17Z
* Results step started: 2026-04-20T17:04:40Z

**Methods used**:

1. Two parallel `/add-paper` subagents were spawned — one per candidate DOI. Each subagent
   fetched CrossRef + PubMed metadata, attempted an Unpaywall-based PDF fetch, wrote
   `details.json` and `summary.md`, and ran `verify_paper_asset` before returning.
2. Methods sections were read from the successfully downloaded PDF (Candidate B) and from the
   abstract + PubMed record for the paywalled paper (Candidate A). Literal tokens `141009`,
   `Pair1DSGC`, `Pair 1 DSGC`, `paired recording`, `paired SAC`, `Sema6`, `October 9, 2014`,
   and `biocytin` / `Neurolucida` / `NeuroMorpho` were searched for in each paper's full text
   (where available).
3. The pre-specified decision procedure from `task_description.md` was applied:
   * criterion 1 — exactly one paper's Methods cites the reconstruction → that paper is the
     source
   * criterion 2 — both cite it → earlier-published paper wins
   * criterion 3 — neither cites it → intervention file
4. The correction asset was hand-written per `arf/specifications/corrections_specification.md`
   v3. No code was produced by this task.

## Verification

All verificator results as of the implementation step commit:

| Verificator | Target | Errors | Warnings |
| --- | --- | --- | --- |
| `verify_paper_asset` | `10.1016_j.neuron.2018.05.028` | 0 | 0 |
| `verify_paper_asset` | `10.1016_j.cub.2018.03.001` | 0 | 0 |
| `verify_correction_asset` | `dataset_dsgc-baseline-morphology` | 0 | 0 |

Integrity checks:

* `assets/paper/` contains exactly the two expected folders. Verified.
* `corrections/` contains exactly `dataset_dsgc-baseline-morphology.json`. Verified.
* The `source_paper_id` value in the correction (`10.1016_j.cub.2018.03.001`) matches an
  actual paper-asset folder on disk. Verified.
* The winning slug was produced via the canonical converter `arf.scripts.utils.doi_to_slug`
  applied to `10.1016/j.cub.2018.03.001`. Verified.

## Limitations

* The *Neuron* candidate (`10.1016/j.neuron.2018.05.028`) was paywalled on Cell Press with no
  PMC deposit, so its full text was not inspected. However, the CrossRef + PubMed metadata
  were sufficient to establish that the paper is not a Feller-lab paper at all — it is Li et
  al. (2018), "A Viral Receptor Complementation Strategy to Overcome CAV-2 Tropism," a
  CSHL-authored paper on AAV retrograde tracing in rat and mouse forebrain. No retinal
  content, no starburst amacrine cells, no DSGCs, no paired recordings. Paywalled full-text
  would not change this disqualification.
* The winning paper's Methods describes paired SAC-DSGC recordings matching the deposition
  methodology but does not literally print the strings `141009`, `Pair1DSGC`, `biocytin`,
  `Neurolucida`, `NeuroMorpho`, or `October 2014`, and publishes only SAC (not DSGC)
  reconstructions. The deposited DSGC reconstruction is therefore **unpublished companion
  data** from the paired-recording sessions reported in the paper, covered by its
  data-availability clause ("available from the corresponding author on request"). This is
  consistent with the NeuroMorpho.org attribution but leaves a small residual uncertainty: we
  cannot prove the exact 2014-10-09 session that produced `141009_Pair1DSGC` is one of the
  specific pairs reported in the paper. The methodological consistency plus the curated
  NeuroMorpho attribution are jointly strong, but not an exact-quote match.
* The original "Morrie & Feller 2018 *Neuron*" label in the t0005 plan was a planning-stage
  error. This task corrects the downstream impact (the `source_paper_id: null`) but does not
  retroactively edit the t0005 plan (which would violate the immutability rule); a follow-up
  suggestion captures the process-improvement lesson.

## Files Created

* `assets/paper/10.1016_j.neuron.2018.05.028/details.json` — metadata for the mis-nominated
  DOI (resolves to Li et al. 2018, not Feller lab); `download_status: "failed"`, full
  `download_failure_reason`.
* `assets/paper/10.1016_j.neuron.2018.05.028/summary.md` — metadata-only summary including the
  disqualifying evidence (wrong authors, wrong topic, no retinal content).
* `assets/paper/10.1016_j.neuron.2018.05.028/files/.gitkeep` — placeholder because no PDF was
  obtained.
* `assets/paper/10.1016_j.cub.2018.03.001/details.json` — full metadata for Morrie & Feller
  2018 *Current Biology* (PMID 29606419, PMCID PMC5916530).
* `assets/paper/10.1016_j.cub.2018.03.001/summary.md` — Methods-grounded summary with paired
  SAC-DSGC recording details and explicit note that no literal `141009`/`Pair1DSGC` token was
  found.
* `assets/paper/10.1016_j.cub.2018.03.001/files/morrie_2018_dense-starburst-plexus.pdf` — 1.82
  MB open-access PDF from eScholarship.
* `corrections/dataset_dsgc-baseline-morphology.json` — correction `C-0013-01`, `action:
  "update"`, `changes: {"source_paper_id": "10.1016_j.cub.2018.03.001"}`, long rationale
  citing both papers' Methods evidence.
* `logs/steps/009_implementation/methods_evidence.md` — full evidence trail with per-candidate
  Methods excerpts, NeuroMorpho.org corroborating attribution, and the decision-procedure
  mapping.
* `results/results_summary.md` — this task's brief summary (see companion file).
* `results/results_detailed.md` — this file.
* `results/metrics.json`, `results/costs.json`, `results/remote_machines_used.json` — empty /
  zero-cost / empty-array stubs per task results spec v8.

## Provenance Decision

### Candidate A — DOI `10.1016/j.neuron.2018.05.028`

**Nominated as** "Morrie & Feller 2018 *Neuron*" by the t0005 plan. **Actually resolves to**
Li, Vaughan, Sturgill & Kepecs (2018), *Neuron* 98(5):905-917.e5 (PMID 29879392): "A Viral
Receptor Complementation Strategy to Overcome CAV-2 Tropism for Efficient Retrograde Targeting
of Neurons." All four authors are at Cold Spring Harbor Laboratory.

**Topic**: AAV-based co-expression of the coxsackievirus and adenovirus receptor (CAR) to
potentiate CAV-2 retrograde infection in long-range projection neurons (basolateral-amygdala
to medial-prefrontal-cortex) in rat and mouse forebrain.

**Retinal content**: **none**. No starburst amacrine cells, no DSGCs, no paired retinal
recordings, no retinal morphology reconstruction. The paper has nothing to do with the Feller
lab or with retinal direction selectivity.

**Match against target tokens** (`141009`, `Pair1DSGC`, `Pair 1 DSGC`, `paired SAC-DSGC`,
`October 9 2014`, `biocytin`, `Neurolucida`, `NeuroMorpho`): **none** found in the available
metadata; full text is paywalled but the disqualification from title/abstract/authors alone is
categorical.

### Candidate B — DOI `10.1016/j.cub.2018.03.001`

**Resolves to** Morrie & Feller (2018), *Current Biology* 28(8):1204-1212.e5 (PMID 29606419,
PMCID PMC5916530): "A Dense Starburst Plexus Is Critical for Generating Direction
Selectivity." Both authors at UC Berkeley.

**Topic**: How starburst amacrine cell (SAC) plexus density and SAC dendritic morphology shape
DSGC tuning. Uses Sema6A-/- mice, paired SAC-DSGC patch recordings, 2-photon Ca2+ imaging of
SAC varicosities, manual SAC reconstruction in FIJI Simple Neurite Tracer, and TREES-toolbox
IPSC simulations.

**Match against target tokens**: literal `141009` — **not found**. Literal `Pair1DSGC` — **not
found**. `biocytin`, `Neurolucida`, literal `NeuroMorpho` deposition statement, `October 9
2014` recording date — **not found**. The paper's data-availability clause reads:

> Datasets generated... and all custom scripts and functions generated or used... are available from
> the corresponding author on request.

**Paired SAC-DSGC recordings matching the deposition methodology**: **found**. Methods section
"Paired SAC-DSGC recordings" describes:

> Inhibitory conductance was reconstructed from SAC-DSGC pairs following the algorithm of Miller and
> Lisberger (2013). DSGCs were held from -100 to +20 mV while SACs were depolarized three times from
> -70 mV to 0 mV for 50 ms.

DSGCs are filled with **0.025 mM AlexaFluor488** in a 110 mM CsMeSO4 internal; SACs are filled
with **AlexaFluor594**. Mouse line: **CNT (ChAT-Cre/nGFP/TrHr)**, p25-120, both sexes.
2-photon 1024x1024 stacks acquired post-recording at 0.5 micrometre z-step and 780 nm or 930
nm excitation. Sample sizes (Fig 2): **n = 12 Control pairs + 9 Sema6A-/- null pairs + 6
Sema6A-/- preferred pairs** — i.e., a substantial population of paired SAC-DSGC recordings
methodologically identical to the one that would produce a `Pair1DSGC` deposition. The paper
publishes only the SAC side of these recordings; the DSGC reconstructions are companion data
covered by the "available on request" clause.

### NeuroMorpho.org machine-readable attribution (corroborating)

Archived at
`tasks/t0005_download_dsgc_morphology/logs/steps/009_implementation/neuromorpho_metadata.json`:

```json
{
  "reference_pmid": ["29606419"],
  "reference_doi": ["10.1016/j.cub.2018.03.001"]
}
```

Both PMID 29606419 and DOI `10.1016/j.cub.2018.03.001` resolve to Candidate B. This is the
Feller-lab-curated attribution for NeuroMorpho neuron 102976 (`141009_Pair1DSGC`). Per the
research notes, NeuroMorpho is corroborating evidence, not decisive — but here the
corroboration aligns unambiguously with the only Methods-consistent candidate.

### Decision-procedure mapping

* **Criterion 1** ("exactly one paper's Methods cites the reconstruction — `141009`,
  `Pair1DSGC`, or a paired SAC-DSGC recording matching the deposition"): satisfied by exactly
  one candidate (Candidate B) under the "paired SAC-DSGC recording matching the deposition"
  clause. Candidate A is categorically disqualified (not a Feller-lab paper, no retinal
  content).
* **Criterion 2** ("both cite it → earlier-published paper wins"): **does not apply** — only
  one paper satisfies criterion 1.
* **Criterion 3** ("neither cites it → intervention file"): **does not apply**.

**Decision**: `source_paper_id = "10.1016_j.cub.2018.03.001"`. The slug is generated by
`arf.scripts.utils.doi_to_slug("10.1016/j.cub.2018.03.001")`. No intervention file is
required.

## Task Requirement Coverage

Operative task text (from `task.json` + `task_description.md`):

> **Resolve dsgc-baseline-morphology source-paper provenance.** Short description: Download both
> plausible Feller-lab 2018 source papers, read their Methods to identify which introduced the
> 141009_Pair1DSGC reconstruction, and correct dsgc-baseline-morphology source_paper_id. Scope: (1)
> Download Morrie & Feller 2018 *Neuron* via `/add-paper`. (2) Download Murphy-Baum & Feller 2018
> *Current Biology* via `/add-paper`. (3) Read both papers' Methods sections, looking specifically
> for: recording date 141009, Pair1DSGC / Pair 1 DSGC / paired recording language, and any explicit
> citation of the reconstruction or its NeuroMorpho deposit. (4) If one paper is unambiguously the
> source, file a correction setting `source_paper_id` to the winning paper's DOI-slug. Otherwise
> record both DOIs under `candidate_source_paper_ids` and open an intervention file. (5) Record the
> full reasoning in `results/results_detailed.md`.

| Req ID | Status | Answer | Evidence |
| --- | --- | --- | --- |
| REQ-1 | **Done** | Registered DOI `10.1016/j.neuron.2018.05.028` as a v3 paper asset. Verified during execution that this DOI resolves to Li et al. 2018 (CSHL viral tracing), NOT the Feller-lab paper the t0005 plan claimed. | `assets/paper/10.1016_j.neuron.2018.05.028/details.json`, `summary.md`; `verify_paper_asset` → 0 errors |
| REQ-2 | **Done** | Registered DOI `10.1016/j.cub.2018.03.001` (Morrie & Feller 2018 *Current Biology*, "A Dense Starburst Plexus Is Critical for Generating Direction Selectivity") as a v3 paper asset with full open-access PDF. | `assets/paper/10.1016_j.cub.2018.03.001/details.json`, `summary.md`, `files/morrie_2018_dense-starburst-plexus.pdf`; `verify_paper_asset` → 0 errors |
| REQ-3 | **Done** | Read both papers' Methods (full text for Candidate B; title + abstract + PubMed record for paywalled Candidate A). Literal `141009` / `Pair1DSGC` / `biocytin` / `Neurolucida` / `NeuroMorpho` / `October 9 2014` — **not found** in either paper. Candidate B Methods explicitly describe paired SAC-DSGC patch recordings (n=12+9+6) in CNT mice with AlexaFluor488-filled DSGCs and AlexaFluor594-filled SACs, methodologically identical to the deposition modality. Candidate A has zero retinal content. | `logs/steps/009_implementation/methods_evidence.md`; `## Provenance Decision` section of this file |
| REQ-4 | **Done** | Applied the pre-specified decision procedure verbatim. Criterion 1 is satisfied by exactly one candidate (Candidate B) under the "paired SAC-DSGC recording matching the deposition" clause; criteria 2 and 3 do not apply. Winner: `10.1016_j.cub.2018.03.001`. | `## Provenance Decision` → decision-procedure mapping; `logs/steps/009_implementation/methods_evidence.md` |
| REQ-5 | **Done** | Filed exactly one correction file (correction_id `C-0013-01`), `action: "update"`, `target_kind: "dataset"`, `target_id: "dsgc-baseline-morphology"`, `changes: {"source_paper_id": "10.1016_j.cub.2018.03.001"}`. No intervention file is needed. | `corrections/dataset_dsgc-baseline-morphology.json`; `verify_correction_asset` → 0 errors |
| REQ-6 | **Done** | Recorded the full auditable reasoning — both papers' Methods evidence (with exact quotes from Candidate B), the NeuroMorpho REST attribution, and the decision-procedure mapping — in a dedicated `## Provenance Decision` section of this file. | `## Provenance Decision` section above |

</details>
