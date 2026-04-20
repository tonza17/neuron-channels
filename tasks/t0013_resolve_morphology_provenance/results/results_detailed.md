---
spec_version: "2"
task_id: "t0013_resolve_morphology_provenance"
---
# Detailed Results: Resolve DSGC Morphology Provenance

## Summary

The dataset asset `dsgc-baseline-morphology` (NeuroMorpho neuron 102976, internal label
`141009_Pair1DSGC`, deposited by the Feller lab) was registered by `t0005_download_dsgc_morphology`
with `source_paper_id: null` because two Feller-lab 2018 papers were plausible sources. This task
downloaded both candidate papers as v3-compliant paper assets, read their Methods sections, applied
the pre-specified decision procedure from `task_description.md`, and filed a single correction that
updates `source_paper_id` from `null` to `10.1016_j.cub.2018.03.001` (Morrie & Feller 2018 *Current
Biology*, "A Dense Starburst Plexus Is Critical for Generating Direction Selectivity"). During
execution we discovered that the t0005 plan's "Morrie & Feller 2018 *Neuron*" nomination was an
erroneous DOI — `10.1016/j.neuron.2018.05.028` resolves to Li, Vaughan, Sturgill & Kepecs (2018), a
CSHL viral-tracing paper unrelated to retina or the Feller lab — so the two-candidate conflict was
illusory.

## Methodology

**Machine**: local Windows 11 workstation (Intel/AMD x86_64, 16+ GB RAM), no remote compute.

**Runtime**: implementation step wall clock was **~22 minutes** (started 2026-04-20T16:41:45Z,
completed 2026-04-20T17:04:17Z). Two `/add-paper` subagents ran in parallel; Methods extraction,
decision, and correction-file authoring were sequential in the orchestrator thread.

**Start / end timestamps (full task, as of this step)**:

* Task started: 2026-04-20T16:26:01Z (`task.json` `start_time`)
* Implementation completed: 2026-04-20T17:04:17Z
* Results step started: 2026-04-20T17:04:40Z

**Methods used**:

1. Two parallel `/add-paper` subagents were spawned — one per candidate DOI. Each subagent fetched
   CrossRef + PubMed metadata, attempted an Unpaywall-based PDF fetch, wrote `details.json` and
   `summary.md`, and ran `verify_paper_asset` before returning.
2. Methods sections were read from the successfully downloaded PDF (Candidate B) and from the
   abstract + PubMed record for the paywalled paper (Candidate A). Literal tokens `141009`,
   `Pair1DSGC`, `Pair 1 DSGC`, `paired recording`, `paired SAC`, `Sema6`, `October 9, 2014`, and
   `biocytin` / `Neurolucida` / `NeuroMorpho` were searched for in each paper's full text (where
   available).
3. The pre-specified decision procedure from `task_description.md` was applied:
   * criterion 1 — exactly one paper's Methods cites the reconstruction → that paper is the source
   * criterion 2 — both cite it → earlier-published paper wins
   * criterion 3 — neither cites it → intervention file
4. The correction asset was hand-written per `arf/specifications/corrections_specification.md` v3.
   No code was produced by this task.

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
* The `source_paper_id` value in the correction (`10.1016_j.cub.2018.03.001`) matches an actual
  paper-asset folder on disk. Verified.
* The winning slug was produced via the canonical converter `arf.scripts.utils.doi_to_slug` applied
  to `10.1016/j.cub.2018.03.001`. Verified.

## Limitations

* The *Neuron* candidate (`10.1016/j.neuron.2018.05.028`) was paywalled on Cell Press with no PMC
  deposit, so its full text was not inspected. However, the CrossRef + PubMed metadata were
  sufficient to establish that the paper is not a Feller-lab paper at all — it is Li et al. (2018),
  "A Viral Receptor Complementation Strategy to Overcome CAV-2 Tropism," a CSHL-authored paper on
  AAV retrograde tracing in rat and mouse forebrain. No retinal content, no starburst amacrine
  cells, no DSGCs, no paired recordings. Paywalled full-text would not change this disqualification.
* The winning paper's Methods describes paired SAC-DSGC recordings matching the deposition
  methodology but does not literally print the strings `141009`, `Pair1DSGC`, `biocytin`,
  `Neurolucida`, `NeuroMorpho`, or `October 2014`, and publishes only SAC (not DSGC)
  reconstructions. The deposited DSGC reconstruction is therefore **unpublished companion data**
  from the paired-recording sessions reported in the paper, covered by its data-availability clause
  ("available from the corresponding author on request"). This is consistent with the
  NeuroMorpho.org attribution but leaves a small residual uncertainty: we cannot prove the exact
  2014-10-09 session that produced `141009_Pair1DSGC` is one of the specific pairs reported in the
  paper. The methodological consistency plus the curated NeuroMorpho attribution are jointly strong,
  but not an exact-quote match.
* The original "Morrie & Feller 2018 *Neuron*" label in the t0005 plan was a planning-stage error.
  This task corrects the downstream impact (the `source_paper_id: null`) but does not retroactively
  edit the t0005 plan (which would violate the immutability rule); a follow-up suggestion captures
  the process-improvement lesson.

## Files Created

* `assets/paper/10.1016_j.neuron.2018.05.028/details.json` — metadata for the mis-nominated DOI
  (resolves to Li et al. 2018, not Feller lab); `download_status: "failed"`, full
  `download_failure_reason`.
* `assets/paper/10.1016_j.neuron.2018.05.028/summary.md` — metadata-only summary including the
  disqualifying evidence (wrong authors, wrong topic, no retinal content).
* `assets/paper/10.1016_j.neuron.2018.05.028/files/.gitkeep` — placeholder because no PDF was
  obtained.
* `assets/paper/10.1016_j.cub.2018.03.001/details.json` — full metadata for Morrie & Feller 2018
  *Current Biology* (PMID 29606419, PMCID PMC5916530).
* `assets/paper/10.1016_j.cub.2018.03.001/summary.md` — Methods-grounded summary with paired
  SAC-DSGC recording details and explicit note that no literal `141009`/`Pair1DSGC` token was found.
* `assets/paper/10.1016_j.cub.2018.03.001/files/morrie_2018_dense-starburst-plexus.pdf` — 1.82 MB
  open-access PDF from eScholarship.
* `corrections/dataset_dsgc-baseline-morphology.json` — correction `C-0013-01`, `action: "update"`,
  `changes: {"source_paper_id": "10.1016_j.cub.2018.03.001"}`, long rationale citing both papers'
  Methods evidence.
* `logs/steps/009_implementation/methods_evidence.md` — full evidence trail with per-candidate
  Methods excerpts, NeuroMorpho.org corroborating attribution, and the decision-procedure mapping.
* `results/results_summary.md` — this task's brief summary (see companion file).
* `results/results_detailed.md` — this file.
* `results/metrics.json`, `results/costs.json`, `results/remote_machines_used.json` — empty /
  zero-cost / empty-array stubs per task results spec v8.

## Provenance Decision

### Candidate A — DOI `10.1016/j.neuron.2018.05.028`

**Nominated as** "Morrie & Feller 2018 *Neuron*" by the t0005 plan. **Actually resolves to** Li,
Vaughan, Sturgill & Kepecs (2018), *Neuron* 98(5):905-917.e5 (PMID 29879392): "A Viral Receptor
Complementation Strategy to Overcome CAV-2 Tropism for Efficient Retrograde Targeting of Neurons."
All four authors are at Cold Spring Harbor Laboratory.

**Topic**: AAV-based co-expression of the coxsackievirus and adenovirus receptor (CAR) to potentiate
CAV-2 retrograde infection in long-range projection neurons (basolateral-amygdala to
medial-prefrontal-cortex) in rat and mouse forebrain.

**Retinal content**: **none**. No starburst amacrine cells, no DSGCs, no paired retinal recordings,
no retinal morphology reconstruction. The paper has nothing to do with the Feller lab or with
retinal direction selectivity.

**Match against target tokens** (`141009`, `Pair1DSGC`, `Pair 1 DSGC`, `paired SAC-DSGC`,
`October 9 2014`, `biocytin`, `Neurolucida`, `NeuroMorpho`): **none** found in the available
metadata; full text is paywalled but the disqualification from title/abstract/authors alone is
categorical.

### Candidate B — DOI `10.1016/j.cub.2018.03.001`

**Resolves to** Morrie & Feller (2018), *Current Biology* 28(8):1204-1212.e5 (PMID 29606419, PMCID
PMC5916530): "A Dense Starburst Plexus Is Critical for Generating Direction Selectivity." Both
authors at UC Berkeley.

**Topic**: How starburst amacrine cell (SAC) plexus density and SAC dendritic morphology shape DSGC
tuning. Uses Sema6A-/- mice, paired SAC-DSGC patch recordings, 2-photon Ca2+ imaging of SAC
varicosities, manual SAC reconstruction in FIJI Simple Neurite Tracer, and TREES-toolbox IPSC
simulations.

**Match against target tokens**: literal `141009` — **not found**. Literal `Pair1DSGC` — **not
found**. `biocytin`, `Neurolucida`, literal `NeuroMorpho` deposition statement, `October 9 2014`
recording date — **not found**. The paper's data-availability clause reads:

> Datasets generated... and all custom scripts and functions generated or used... are available from
> the corresponding author on request.

**Paired SAC-DSGC recordings matching the deposition methodology**: **found**. Methods section
"Paired SAC-DSGC recordings" describes:

> Inhibitory conductance was reconstructed from SAC-DSGC pairs following the algorithm of Miller and
> Lisberger (2013). DSGCs were held from -100 to +20 mV while SACs were depolarized three times from
> -70 mV to 0 mV for 50 ms.

DSGCs are filled with **0.025 mM AlexaFluor488** in a 110 mM CsMeSO4 internal; SACs are filled with
**AlexaFluor594**. Mouse line: **CNT (ChAT-Cre/nGFP/TrHr)**, p25-120, both sexes. 2-photon 1024x1024
stacks acquired post-recording at 0.5 micrometre z-step and 780 nm or 930 nm excitation. Sample
sizes (Fig 2): **n = 12 Control pairs + 9 Sema6A-/- null pairs + 6 Sema6A-/- preferred pairs** —
i.e., a substantial population of paired SAC-DSGC recordings methodologically identical to the one
that would produce a `Pair1DSGC` deposition. The paper publishes only the SAC side of these
recordings; the DSGC reconstructions are companion data covered by the "available on request"
clause.

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
Feller-lab-curated attribution for NeuroMorpho neuron 102976 (`141009_Pair1DSGC`). Per the research
notes, NeuroMorpho is corroborating evidence, not decisive — but here the corroboration aligns
unambiguously with the only Methods-consistent candidate.

### Decision-procedure mapping

* **Criterion 1** ("exactly one paper's Methods cites the reconstruction — `141009`, `Pair1DSGC`, or
  a paired SAC-DSGC recording matching the deposition"): satisfied by exactly one candidate
  (Candidate B) under the "paired SAC-DSGC recording matching the deposition" clause. Candidate A is
  categorically disqualified (not a Feller-lab paper, no retinal content).
* **Criterion 2** ("both cite it → earlier-published paper wins"): **does not apply** — only one
  paper satisfies criterion 1.
* **Criterion 3** ("neither cites it → intervention file"): **does not apply**.

**Decision**: `source_paper_id = "10.1016_j.cub.2018.03.001"`. The slug is generated by
`arf.scripts.utils.doi_to_slug("10.1016/j.cub.2018.03.001")`. No intervention file is required.

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
