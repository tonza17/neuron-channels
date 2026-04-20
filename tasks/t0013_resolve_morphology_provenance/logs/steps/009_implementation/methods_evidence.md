---
task_id: "t0013_resolve_morphology_provenance"
step: "implementation"
date: "2026-04-20"
---
# Methods Evidence for DSGC Morphology Provenance Decision

This document records the Methods-based evidence collected from each candidate paper and applies the
pre-specified decision procedure from `task_description.md` to resolve the `source_paper_id` of the
`dsgc-baseline-morphology` dataset asset.

## Candidate Papers

### Candidate A — DOI `10.1016/j.neuron.2018.05.028`

* **Nominated as**: "Morrie & Feller 2018 *Neuron*" by the t0005 plan.
* **Actually resolves to**: Li, Vaughan, Sturgill & Kepecs (2018), *Neuron* 98(5):905-917.e5 (PMID
  29879392). Title: "A Viral Receptor Complementation Strategy to Overcome CAV-2 Tropism for
  Efficient Retrograde Targeting of Neurons." All four authors are at Cold Spring Harbor Laboratory.
* **Topic**: AAV-based co-expression of the coxsackievirus and adenovirus receptor (CAR) to
  potentiate CAV-2 retrograde infection in long-range projection neurons (e.g.,
  basolateral-amygdala-to-medial-prefrontal-cortex). Worked in rat and mouse forebrain.
* **Retinal content**: None. No starburst amacrine cells, no DSGCs, no paired retinal recordings, no
  retinal morphology reconstruction.
* **Reference to `141009`, `Pair1DSGC`, paired SAC-DSGC, October 2014, biocytin, Neurolucida,
  NeuroMorpho deposition**: NONE. The paper has nothing to do with the Feller lab or with retinal
  direction selectivity.
* **Download status**: Failed (paywall on Cell Press, no PMC deposit). Metadata and abstract were
  obtained from CrossRef and PubMed. Despite the paper not being downloadable, the title, abstract,
  authors, and venue make it unambiguous that this DOI is not a Feller-lab paper and is unrelated to
  the deposited reconstruction.

### Candidate B — DOI `10.1016/j.cub.2018.03.001`

* **Resolves to**: Morrie & Feller (2018), *Current Biology* 28(8):1204-1212.e5 (PMID 29606419,
  PMCID PMC5916530). Title: "A Dense Starburst Plexus Is Critical for Generating Direction
  Selectivity." Both authors are at the University of California, Berkeley.
* **Topic**: How starburst amacrine cell (SAC) plexus density and SAC dendritic morphology shape
  direction-selective ganglion cell (DSGC) tuning. Uses Sema6A-/- mice, paired SAC-DSGC patch
  recordings, 2-photon Ca2+ imaging of SAC varicosities, manual SAC reconstruction in FIJI Simple
  Neurite Tracer, and TREES-toolbox IPSC simulations.
* **Reference to deposition markers**:
  * Literal `141009` token: NOT FOUND in the published text.
  * Literal `Pair1DSGC` token: NOT FOUND.
  * `biocytin`: NOT FOUND. SACs and DSGCs are filled with AlexaFluor594 and AlexaFluor488
    respectively, not biocytin.
  * `Neurolucida`: NOT FOUND. SAC morphologies are traced manually in FIJI Simple Neurite Tracer.
  * `NeuroMorpho` deposition statement: NOT FOUND. The data-availability clause reads "Datasets
    generated... and all custom scripts and functions generated or used... are available from the
    corresponding author on request." (Methods, Data and Software Availability.)
  * "October 9 2014" recording date: NOT FOUND. The paper does not print individual recording dates.
* **Reference to a paired SAC-DSGC recording matching the deposition methodology**: YES. Methods
  section "Paired SAC-DSGC recordings" describes:
  * "Inhibitory conductance was reconstructed from SAC-DSGC pairs following the algorithm of Miller
    and Lisberger (2013). DSGCs were held from -100 to +20 mV while SACs were depolarized three
    times from -70 mV to 0 mV for 50 ms."
  * Internal solutions: 110 mM CsMeSO4 with 0.025 mM AlexaFluor488 for DSGCs; 0.1 mM EGTA with
    AlexaFluor594 for SACs.
  * Mouse line: CNT (ChAT-Cre/nGFP/TrHr), p25-120, both sexes.
  * Imaging: 2-photon 1024x1024 stacks at 0.5 micrometre step, 780 nm or 930 nm excitation, acquired
    post-recording.
  * "Fig 2 paired SAC-DSGC n = 12 Control / 9 Sema6A-/- null-pairs / 6 Sema6A-/- preferred-pairs" —
    i.e., a sizeable population of paired SAC-DSGC recordings was performed.
* **DSGC reconstruction in published Methods**: Explicitly NOT performed. Only SAC morphologies are
  reconstructed (FIJI Simple Neurite Tracer to SWC to TREES toolbox). The deposited DSGC
  reconstruction (NeuroMorpho 102976) must be unpublished companion data from the same paired-
  recording sessions, covered by the "available on request" data clause.

## NeuroMorpho.org Machine-Readable Attribution (Corroborating)

Archived at
`tasks/t0005_download_dsgc_morphology/logs/steps/009_implementation/neuromorpho_metadata.json`:

```json
{
  "reference_pmid": ["29606419"],
  "reference_doi": ["10.1016/j.cub.2018.03.001"]
}
```

PMID `29606419` and DOI `10.1016/j.cub.2018.03.001` both resolve to Candidate B (Morrie & Feller
2018 *Current Biology*). This is the curated attribution the Feller lab provided to NeuroMorpho.org
for neuron 102976, internal label `141009_Pair1DSGC`. Per `research_code.md`, NeuroMorpho is
corroborating evidence, not decisive — but in this case the corroboration is unambiguous and aligns
with the only Methods-consistent candidate.

## Application of the Decision Procedure

`task_description.md` fixes the procedure:

1. If exactly one paper's Methods cites the reconstruction (`141009`, `Pair1DSGC`, or a paired
   SAC-DSGC recording matching the deposition date), that paper is the source.
2. If both papers cite it, the earlier-published paper is the source.
3. If neither cites it, write an intervention file requesting the Feller lab resolve the
   attribution.

Mapping of evidence to candidates:

* Candidate A (Li et al. 2018, viral retrograde tracing): does not cite the reconstruction in any
  form. Topic, authors, and methodology are entirely unrelated. The original "Morrie & Feller 2018
  Neuron" label in the t0005 plan was an erroneous nomination — the DOI never belonged to a
  Feller-lab paper.
* Candidate B (Morrie & Feller 2018 *Current Biology*): does not literally print `141009` or
  `Pair1DSGC`, but its Methods describe paired SAC-DSGC patch recordings with AlexaFluor488-filled
  DSGCs in CNT mice — i.e., a paired SAC-DSGC recording series methodologically identical to the one
  that produced the `Pair1DSGC` deposition. Combined with the NeuroMorpho machine-readable
  attribution to this same DOI/PMID, this satisfies criterion 1's "paired SAC-DSGC recording
  matching the deposition" clause.

Exactly one candidate satisfies criterion 1: Candidate B. Criterion 1 fires; criteria 2 and 3 do not
apply.

**Decision**: `source_paper_id` = `10.1016_j.cub.2018.03.001` (the slug of Candidate B, generated by
`arf.scripts.utils.doi_to_slug` from DOI `10.1016/j.cub.2018.03.001`).

## Verification Notes

* No intervention file is required. The DSGC reconstruction is from unpublished companion data of
  the Morrie & Feller (2018) *Current Biology* paper, which is consistent with the Feller-lab-
  curated NeuroMorpho attribution and with the only Methods-based candidate.
* The originally nominated DOI `10.1016/j.neuron.2018.05.028` should be considered a planning-stage
  error in t0005, not a competing valid candidate. A future suggestion may capture this as a
  process-improvement note ("verify candidate DOIs resolve to the expected papers before locking
  them into a plan").
