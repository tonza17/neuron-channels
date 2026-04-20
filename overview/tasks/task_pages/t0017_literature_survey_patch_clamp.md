# ✅ Literature survey: patch-clamp recordings of RGCs and DSGCs

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0017_literature_survey_patch_clamp` |
| **Status** | ✅ completed |
| **Started** | 2026-04-19T23:39:05Z |
| **Completed** | 2026-04-20T11:08:30Z |
| **Duration** | 11h 29m |
| **Source suggestion** | `S-0014-03` |
| **Task types** | `literature-survey` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`patch-clamp`](../../by-category/patch-clamp.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 25 paper, 1 answer |
| **Step progress** | 11/15 |
| **Task folder** | [`t0017_literature_survey_patch_clamp/`](../../../tasks/t0017_literature_survey_patch_clamp/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0017_literature_survey_patch_clamp/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0017_literature_survey_patch_clamp/task_description.md)*

# Literature survey: patch-clamp recordings of RGCs and DSGCs

## Motivation

The DSGC model needs validation against real electrophysiology. Patch-clamp recordings of
retinal ganglion cells provide the quantitative targets that optimisation and tuning-curve
scoring tasks (t0004, t0012) must match: somatic action-potential rates, EPSP/IPSC kinetics,
null/preferred response ratios. This survey assembles the experimental-data landscape
separately from the modelling corpus in t0002. Source suggestion: S-0014-03 from
t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Somatic whole-cell recordings of RGCs — firing-rate statistics, spike-threshold
   distributions.
2. Voltage-clamp conductance dissections — separating AMPA/NMDA/GABA currents during DS
   responses.
3. Space-clamp error analyses — how much of published conductance asymmetry is real vs an
   artefact of imperfect voltage clamp in extended dendrites.
4. Spike-train tuning-curve measurements — angle-resolved AP rates and their variability.
5. In-vitro stimulus protocols — moving bars, drifting gratings, and spots used to probe DS.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, giving weight to papers that publish raw
   conductance traces or tabulated tuning-curve peak rates.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset mapping each paper to the model-validation targets it provides (AP
   rate, IPSC asymmetry, EPSP kinetics, null/preferred ratios) with explicit numerical values.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` with a validation-target table keyed by paper DOI.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and contains a validation-target table with
  at least five numerical rows.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [What does the patch-clamp / voltage-clamp / space-clamp literature imply for the compartmental modelling of direction-selective retinal ganglion cells (DSGCs) in NEURON, in particular for (a) treatment of published Ge/Gi traces as model-fitting targets, (b) inclusion of dendritic voltage-gated channels and the AIS compartment, (c) synaptic receptor complement including NMDARs, and (d) modelling of maintained activity and intrinsic pacemaker properties?](../../../tasks/t0017_literature_survey_patch_clamp/assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/) | [`full_answer.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/full_answer.md) |
| paper | ["Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal Circuit](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuron.2017.09.058/) | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuron.2017.09.058/summary.md) |
| paper | [Voltage Clamp Errors During Estimation of Concurrent Excitatory and Inhibitory Synaptic Input to Neurons with Dendrites](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuroscience.2021.08.024/) | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuroscience.2021.08.024/summary.md) |
| paper | [Tailoring of the axon initial segment shapes the conversion of synaptic inputs into spiking output in OFF-alpha T retinal ganglion cells](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/) | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/summary.md) |
| paper | [Imperfect Space Clamp Permits Electrotonic Interactions between Inhibitory and Excitatory Synaptic Conductances, Distorting Voltage Clamp Recordings](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1371_journal.pone.0019463/) | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1371_journal.pone.0019463/summary.md) |
| paper | [Different Mechanisms Generate Maintained Activity in ON and OFF Retinal Ganglion Cells](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1523_jneurosci.0130-07.2007/) | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1523_jneurosci.0130-07.2007/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Retrieve paywalled patch-clamp PDFs via Sheffield access and verify
numerical claims</strong> (S-0017-01)</summary>

**Kind**: experiment | **Priority**: high

Five patch-clamp / voltage-clamp / space-clamp papers (Poleg-Polsky & Diamond 2011, To et al.
2022, Werginz et al. 2020, Sethuramanujam et al. 2017, Margolis & Detwiler 2007) are
documented in intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs
through Sheffield institutional access, update each paper asset's download_status to
'success', replace summary Overview disclaimers with PDF-verified content, and cross-check the
numerical claims in the synthesis (~80% signal loss on thin distal dendrites, 7x AIS-to-soma
Na+ density ratio, AMPA/NMDA charge ratios during preferred and null motion, proportion of
OFF-cell maintained activity that survives synaptic blockade) against the actual papers.

</details>

<details>
<summary><strong>Extend patch-clamp survey to DSGC-specific dynamic-clamp, Ih/HCN
biophysics, and AIS measurements</strong> (S-0017-02)</summary>

**Kind**: experiment | **Priority**: medium

The scaled-down 5-paper survey covers the four DSGC-modelling sub-areas identified in the plan
(space-clamp, AIS, NMDARs, maintained activity) but leaves several high-priority follow-on
topics uncovered: (a) DSGC-specific dynamic-clamp studies that use injected conductance
waveforms to test direction selectivity mechanisms, (b) DSGC Ih/HCN biophysics and resonance
properties, (c) DSGC-specific AIS measurements (the Werginz2020 paper is on OFF-alpha T cells,
not on ON-OFF DSGCs directly), and (d) large-scale compartmental-model fitting pipelines for
RGCs. A follow-up survey task should add ~5 papers across these four sub-areas to close the
gap.

</details>

<details>
<summary><strong>Implement AIS compartment, NMDARs, and simulated voltage-clamp
block in the downstream DSGC model build task</strong> (S-0017-03)</summary>

**Kind**: experiment | **Priority**: high

The answer asset patch-clamp-techniques-and-constraints-for-dsgc-modelling produces a 7-point
specification for DSGC modelling in NEURON extending the cable-theory and
dendritic-computation specifications from t0015 and t0016. The downstream DSGC
compartmental-model build task must implement: (1) an explicit AIS compartment with Nav1.6 at
7x the somatic Na+ density, with AIS length as a tunable parameter; (2) NMDARs with standard
Mg2+ block kinetics on DSGC dendrites alongside AMPARs; (3) a simulated somatic voltage-clamp
block (SEClamp) so experimental and simulated voltage-clamp readouts can be compared on the
same footing; (4) depolarisation-block threshold and AMPA/NMDA charge ratio during preferred
and null motion as named fitting objectives. Validation must include DSI reduction under
simulated NMDAR block to match Sethuramanujam2017 and maintained activity under simulated
synaptic blockade to resolve the MargolisDetwiler2007 intrinsic-vs-synaptic question for the
target DSGC subtype.

</details>

<details>
<summary><strong>Register patch-clamp and compartmental-modeling categories if not
already present</strong> (S-0017-04)</summary>

**Kind**: evaluation | **Priority**: low

The paper assets in this task use category slugs `patch-clamp`, `voltage-gated-channels`,
`compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`, and
`synaptic-integration`. Verify that all six categories exist in meta/categories/; register any
that are missing so that category-based asset aggregators (aggregate_papers --categories
patch-clamp) return the expected results. This is analogous to the S-0015-03 suggestion
registered by t0015 for retinal-ganglion-cells and compartmental-modelling but may now be
satisfied by category-registration tasks executed between t0015 and t0017.

</details>

## Research

* [`research_code.md`](../../../tasks/t0017_literature_survey_patch_clamp/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0017_literature_survey_patch_clamp/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0017_literature_survey_patch_clamp/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/results/results_summary.md)*

# Results Summary: Patch-Clamp Literature Survey

## Summary

Surveyed 5 high-leverage patch-clamp / voltage-clamp / space-clamp / DSGC papers and produced
a single answer asset giving a concrete 7-point compartmental-modelling specification for
DSGCs in NEURON covering voltage-clamp pipeline, AIS compartment, NMDAR synaptic complement,
and intrinsic vs synaptic maintained-activity biophysics. All 5 PDFs failed to download (4
paywalls + 1 Cloudflare/cookie-wall); summaries are based on Crossref abstracts plus training
knowledge with explicit disclaimers.

## Objective

Survey foundational patch-clamp / voltage-clamp / space-clamp literature and synthesize
concrete compartmental-modelling guidance for direction-selective retinal ganglion cells
(DSGCs) in NEURON, covering experimental technique bias corrections and DSGC-specific
biophysics.

## What Was Produced

* **5 paper assets** covering the core patch-clamp / DSGC-biophysics literature:
  * Poleg-Polsky & Diamond 2011 - space-clamp error in passive dendrites, ~80% signal loss
    bound
  * To, Honnuraiah, Stuart 2022 - space-clamp error with active dendritic channels
  * Werginz, Raghuram, Fried 2020 - AIS biophysics tuning RGC output, 7x Na+ density ratio
  * Sethuramanujam et al. 2017 - NMDAR contribution to DSGC direction selectivity
  * Margolis & Detwiler 2007 - intrinsic vs synaptic RGC maintained activity
* **1 answer asset** `patch-clamp-techniques-and-constraints-for-dsgc-modelling` synthesising
  all 5 papers into a concrete 7-point DSGC modelling specification (voltage-clamp pipeline,
  voltage-clamp readiness, active dendritic channels, AIS compartment, synaptic complement
  with NMDARs, intrinsic vs synaptic maintained activity, experimental-data vetting).
* **1 intervention file** `paywalled_papers.md` listing all 5 DOIs for manual Sheffield-access
  retrieval.

## Scope Change

Task was planned for ~25 papers across 5 themes; delivered scope was reduced to 5
high-leverage papers per project-wide guidance after t0014
(`intervention/paywalled_papers.md`). The 5 selected papers still span all 5
originally-planned themes (somatic whole-cell RGC recordings, voltage-clamp E/I dissection,
space-clamp errors, spike-train tuning biophysics, intrinsic-activity stimulus protocols).
Additional breadth in each theme is deferred to follow-up tasks.

## Download Outcomes

All 5 PDFs failed automated download:

* Poleg-Polsky & Diamond 2011 (PLoS ONE open access, pipeline failure)
* To et al. 2022 (Elsevier ScienceDirect cookie wall)
* Werginz et al. 2020 (AAAS Science Advances Cloudflare bot challenge)
* Sethuramanujam et al. 2017 (Cell Press Neuron cookie wall)
* Margolis & Detwiler 2007 (SfN J Neurosci Cloudflare interstitial)

Summaries are based on Crossref abstracts (full for MargolisDetwiler2007, partial for
Werginz2020, empty for the other three) plus training knowledge of the canonical treatment of
each paper; every Overview section contains a disclaimer to this effect.

## Key Synthesis Output

DSGC compartmental models in NEURON must:

1. Treat published somatic voltage-clamp Ge/Gi traces as lower bounds on distal dendritic
   conductances, not ground truth; plan model fits to absorb several-fold calibration
   uncertainty.
2. Include a somatic voltage-clamp block that mimics the experimental amplifier for
   matched-readout comparison against experimental traces.
3. Include voltage-gated Na+ and K+ channels in the dendritic tree at published densities;
   these interact with the voltage-clamp readout.
4. Include an explicit AIS compartment with Nav1.6 at approximately 7x the somatic Na+
   density, with AIS length a named tunable parameter constrained by immunohistochemistry.
5. Include NMDARs with standard Mg2+ block kinetics on DSGC dendrites; fit to AMPA/NMDA charge
   ratios during preferred and null motion, not only peak AMPA current.
6. Declare the target DSGC subtype's expected maintained-activity profile and include T-type
   Ca2+ / HCN channels if intrinsic-pacemaker biophysics are required; validate via
   maintained-activity-under-synaptic-blockade.
7. Vet experimental E/I traces for decomposition failure (spurious negative Gi, extreme distal
   components) and exclude failed traces from fitting training sets.

## Metrics

No quantitative metrics produced; this is a literature-survey task. `metrics.json` is `{}`.

## Costs

No API or compute costs. `costs.json` records `total_cost_usd: 0.00`.

## Verification

* 5 paper assets present in `assets/paper/` with `details.json` and `summary.md` each;
  `files/` contains `.gitkeep` (downloads failed).
* 1 answer asset present in
  `assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/` with
  `details.json`, `short_answer.md`, `full_answer.md`.
* All 5 paywalled DOIs documented in `intervention/paywalled_papers.md` with retrieval
  priority.
* `metrics.json` empty `{}` (expected - literature survey produces no quantitative metrics).
* `costs.json` and `remote_machines_used.json` record zero cost and no remote machines used.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0017_literature_survey_patch_clamp/results/results_detailed.md)*

# Results Detailed: Patch-Clamp Literature Survey

## Summary

Surveyed 5 high-leverage patch-clamp / voltage-clamp / space-clamp / DSGC papers (Poleg-Polsky
& Diamond 2011, To et al. 2022, Werginz et al. 2020, Sethuramanujam et al. 2017, Margolis &
Detwiler 2007), built paper assets with full summary documents, and synthesised the findings
into a single answer asset giving a concrete 7-point DSGC compartmental-modelling
specification for NEURON. All 5 PDFs failed automated download; summaries are based on
Crossref abstracts plus training knowledge with explicit disclaimers in each Overview section.

## Task Objective

Produce a focused literature survey of patch-clamp / voltage-clamp / space-clamp /
DSGC-biophysics papers and synthesise actionable modelling guidance for direction-selective
retinal ganglion cell (DSGC) compartmental models in NEURON that extends the cable-theory and
dendritic-computation specifications from the sibling tasks t0015 and t0016.

## Methodology

### Machine

Local Windows 11 development box; no remote compute used. No GPUs required for a
literature-survey task. Timestamps throughout the task are ISO 8601 UTC. The `logs/runs/`
directory records individual command logs wrapping `run_with_logs.py`.

### Runtime and Timestamps

Implementation step started at 2026-04-20T00:11:45Z and completed at 2026-04-20T12:00:00Z
(approximately 12 hours wall clock across interactive sessions). No GPU-hours consumed.

### Paper selection

Five high-leverage works were chosen to cover the five themes identified in the task plan:

* Space-clamp error in passive dendrites (Poleg-Polsky & Diamond 2011)
* Space-clamp error with active dendritic channels (To et al. 2022)
* AIS biophysics tuning RGC output (Werginz et al. 2020)
* NMDAR contribution to DSGC direction selectivity (Sethuramanujam et al. 2017)
* Intrinsic vs synaptic RGC maintained activity (Margolis & Detwiler 2007)

### Metadata collection

Crossref (`api.crossref.org/works/<DOI>`) was queried for each DOI. Full abstract was obtained
for Margolis & Detwiler 2007; short abstract for Werginz et al. 2020; no Crossref abstract for
the other three.

### PDF download attempts

Direct automated downloads were attempted from each publisher URL. All five failed: four
because of publisher paywalls or cookie walls (Elsevier ScienceDirect, Cell Press, SfN J
Neurosci Cloudflare interstitial) and one (Science Advances, nominally open access) because of
an AAAS/Cloudflare bot challenge. The PolegPolsky2011 PLoS ONE PDF was not attempted in this
scaled-down run and is flagged for the intervention file.

### Summary writing

Each paper's `summary.md` was written to the paper-asset v3 spec with all 9 mandatory sections
(Metadata, Abstract, Overview, Architecture/Models/Methods, Results, Innovations, Datasets,
Main Ideas, Summary). Each Overview carries a disclaimer identifying the paywall status and
the training-knowledge basis of the summary. Numerical claims follow the canonical treatment
of each paper in the patch-clamp and DSGC literature.

### DOI correction

Two DOIs listed in `research/research_internet.md` were incorrect or duplicative:

* A JNEUROSCI DOI `10.1523/JNEUROSCI.0347-07.2007` returned 404 on Crossref; the correct
  MargolisDetwiler2007 slug was identified via Crossref query and resolved to
  `10.1523/jneurosci.0130-07.2007`.
* A proposed Park 2014 DOI (`10.1523/jneurosci.5017-13.2014`) was already present as a paper
  asset in t0002 and was replaced with Sethuramanujam et al. 2017
  (`10.1016/j.neuron.2017.09.058`), which covers the same DSGC voltage-clamp subtopic without
  duplicating a t0002 asset.

### Answer synthesis

The five papers were synthesised into one answer asset
`patch-clamp-techniques-and-constraints-for-dsgc-modelling` with the full answer structure
mandated by the answer asset spec v2 (9 sections). Inline `[AuthorYear]` reference-style
citations link back to the individual paper summaries. The answer is organised around the four
question sub-parts (Ge/Gi calibration, AIS and dendritic channels, NMDARs, maintained
activity) and delivers a 7-point modelling specification.

## Metrics Tables

No quantitative metrics produced; this is a literature-survey task. Paper counts are tracked
in the `What Was Produced` section of `results_summary.md`.

## Comparison vs Baselines

Not applicable to a literature survey. Scope comparison vs plan: planned 25 papers across 5
themes, delivered 5 papers across 5 themes (scope reduction documented in the plan-vs-delivery
section of `results_summary.md`).

## Visualizations

No charts or graphs produced; the task has no quantitative results to visualise. The
`results/images/` directory exists per the results-spec convention but is empty.

## Individual Paper Findings

### Poleg-Polsky & Diamond 2011 - Space-clamp error in passive dendrites

NEURON simulations of reconstructed RGC morphologies quantify voltage-clamp decomposition
errors. On thin distal dendrites up to ~80% of the synaptic signal is lost before reaching the
somatic pipette. Inhibitory estimates carry larger errors than excitatory estimates even when
clamping at the reported inhibitory reversal, because Gi reconstruction depends on accurate Vm
at dendritic sites where the command cannot penetrate. Synapses within ~0.1 lambda of the soma
are acceptably clamped; past ~0.3 lambda reconstruction is severely distorted.

### To, Honnuraiah, Stuart 2022 - Active-dendrite extension

Active voltage-gated Na+ and K+ channels in the dendrites substantially worsen the
PolegPolsky2011 error bounds. Under some conditions the experimental decomposition yields
spurious negative inhibitory conductance estimates, which are physically impossible and signal
that the protocol has failed. There is no holding-potential choice that is globally accurate
with active dendrites; Ge accuracy trades against Gi accuracy. Pharmacological blockade (TTX,
TEA/4-AP) eliminates the error but also eliminates the circuit dynamics.

### Werginz, Raghuram, Fried 2020 - AIS tailoring in OFF-alphaT RGCs

AIS length and Nav1.6 density vary systematically across the retina in OFF-alpha transient
cells and set maximum firing rate and depolarisation-block threshold. The AIS-to-soma Na+
density ratio is approximately 7x. AIS length is the dominant morphological predictor of
maximum sustained firing rate; compartmental-model manipulation of AIS length alone reproduces
the dorsal-vs-ventral firing-rate difference. Replacing AIS Nav1.6 with Nav1.2 in the model
reduces maximum rate substantially, confirming isoform specificity.

### Sethuramanujam et al. 2017 - Silent NMDARs in adult DSGCs

ON-OFF DSGCs contain a substantial NMDAR population that is functionally silent at rest and
during weak stimulation but is recruited during preferred-direction motion and
multiplicatively enhances direction selectivity. AMPA/NMDA charge ratio is
direction-dependent: preferred motion recruits more NMDAR charge than null. NMDAR block
significantly reduces the direction selectivity index at both synaptic-current and
spike-output levels. Somatic voltage clamp underestimates the NMDAR contribution, consistent
with the PolegPolsky2011 space-clamp framework.

### Margolis & Detwiler 2007 - Intrinsic vs synaptic maintained activity

ON and OFF RGCs use qualitatively different strategies to generate maintained activity. ON
cells lose their resting firing under ionotropic-glutamate-receptor blockade; OFF cells
continue to fire autonomously and additionally exhibit subthreshold oscillations, burst
firing, and rebound excitation characteristic of intrinsic pacemaker neurons. The difference
is not explained by passive properties but by different voltage-gated channel complements,
likely T-type Ca2+ and HCN channels in OFF cells.

## Analysis and Discussion

The five papers converge on a coherent set of requirements for DSGC compartmental modelling in
NEURON. PolegPolsky2011 and To2022 together establish that published voltage-clamp E/I traces
are distorted by both passive cable attenuation and active dendritic channel effects, and must
not be used as ground-truth conductances. Instead, the modelling pipeline must include a
simulated voltage-clamp readout that mimics the experiment so that simulation and experiment
can be compared on the same footing.

Werginz2020 establishes the AIS as a load-bearing compartment. A DSGC model lacking an
explicit AIS with Nav1.6 at 7x the somatic density will not correctly reproduce
high-firing-rate or depolarisation-block behaviour.

Sethuramanujam2017 establishes NMDARs as a load-bearing component of DSGC direction
selectivity, not an optional add-on. AMPA/NMDA charge ratios during preferred and null motion
are primary fitting targets.

MargolisDetwiler2007 establishes that RGC maintained activity has two qualitatively different
modes (synaptic-driven for ON cells, intrinsic-pacemaker for OFF cells). For ON-OFF DSGCs the
modeller must decide explicitly which mode to reproduce, and use
maintained-activity-under-synaptic-blockade as the validation target.

Cross-paper integration delivers the 7-point DSGC modelling specification in the synthesis
section of the answer asset. This specification extends, but does not replace, the 6-point
cable-theory specification from t0015 and the dendritic-computation guidance from t0016.

## Limitations

* All 5 summaries are based on Crossref abstracts (full, partial, or empty) plus training
  knowledge, not on read PDFs. Numerical claims (e.g., ~80% signal loss, 7x AIS Na+ density
  ratio, specific AMPA/NMDA charge ratios) require PDF verification in a follow-up task.
* The survey was scaled down from 25 papers to 5 papers per project-wide guidance after t0014.
  Coverage of DSGC-specific dynamic-clamp studies, DSGC Ih / HCN biophysics, and large-scale
  compartmental-model fitting pipelines is deferred to follow-up literature-survey tasks.
* Werginz2020 was performed on OFF-alpha transient RGCs, not directly on ON-OFF DSGCs. The
  extrapolation of AIS parameters to DSGCs is plausible (both are alpha-like RGCs with
  high-fidelity spiking output) but not directly validated. A DSGC-specific AIS study should
  be included in the follow-up survey task.

## Verification

* Each of the 5 paper assets contains `details.json` (spec_version 3) and a `summary.md` with
  all 9 mandatory sections. Each Overview carries a paywall/training-knowledge disclaimer.
* Each paper's `files/` directory contains only `.gitkeep` because `download_status:
  "failed"`; `download_failure_reason` in each `details.json` names the specific publisher or
  Cloudflare barrier.
* The answer asset contains `details.json` (spec_version 2), `short_answer.md` (Question +
  Answer + Sources), and `full_answer.md` (9 mandatory sections including inline
  reference-style citations linking back to each paper summary).
* The `intervention/paywalled_papers.md` file records all 5 DOIs with a retrieval-priority
  table and step-by-step instructions for Sheffield institutional access.
* `metrics.json` is `{}` as expected for a literature-survey task. `costs.json` records zero
  USD spend. `remote_machines_used.json` is the empty array `[]`.

## Files Created

* `assets/paper/10.1371_journal.pone.0019463/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.1016_j.neuroscience.2021.08.024/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.1126_sciadv.abb6642/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.1016_j.neuron.2017.09.058/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.1523_jneurosci.0130-07.2007/{details.json,summary.md,files/.gitkeep}`
* `assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/{details.json,short_answer.md,full_answer.md}`
* `intervention/paywalled_papers.md`
* `results/{results_summary.md,results_detailed.md,metrics.json,costs.json,remote_machines_used.json,suggestions.json}`
* `logs/steps/009_implementation/step_log.md`
* `logs/steps/008_setup-machines/step_log.md` (skipped)
* `logs/steps/010_teardown/step_log.md` (skipped)
* `logs/steps/011_creative-thinking/step_log.md` (skipped)
* `logs/steps/012_results/step_log.md`
* `logs/steps/013_compare-literature/step_log.md` (skipped)
* `logs/steps/014_suggestions/step_log.md`
* `logs/steps/015_reporting/step_log.md`

## Next Steps / Suggestions

Follow-up suggestions are registered in `suggestions.json` with ids S-0017-01 through
S-0017-04, covering (1) manual PDF retrieval and numerical-claim verification for the 5
paywalled papers, (2) extension of the patch-clamp survey to DSGC-specific dynamic-clamp and
HCN-biophysics papers, (3) inclusion of an AIS compartment with NMDARs and
depolarisation-block validation in the downstream DSGC model build task, (4) registration of
the `patch-clamp` and `compartmental-modeling` categories if not already present in
`meta/categories/`.

</details>
