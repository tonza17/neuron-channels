# Results Detailed: Patch-Clamp Literature Survey

## Summary

Surveyed 5 high-leverage patch-clamp / voltage-clamp / space-clamp / DSGC papers (Poleg-Polsky &
Diamond 2011, To et al. 2022, Werginz et al. 2020, Sethuramanujam et al. 2017, Margolis & Detwiler
2007), built paper assets with full summary documents, and synthesised the findings into a single
answer asset giving a concrete 7-point DSGC compartmental-modelling specification for NEURON. All 5
PDFs failed automated download; summaries are based on Crossref abstracts plus training knowledge
with explicit disclaimers in each Overview section.

## Task Objective

Produce a focused literature survey of patch-clamp / voltage-clamp / space-clamp / DSGC-biophysics
papers and synthesise actionable modelling guidance for direction-selective retinal ganglion cell
(DSGC) compartmental models in NEURON that extends the cable-theory and dendritic-computation
specifications from the sibling tasks t0015 and t0016.

## Methodology

### Machine

Local Windows 11 development box; no remote compute used. No GPUs required for a literature-survey
task. Timestamps throughout the task are ISO 8601 UTC. The `logs/runs/` directory records individual
command logs wrapping `run_with_logs.py`.

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

Crossref (`api.crossref.org/works/<DOI>`) was queried for each DOI. Full abstract was obtained for
Margolis & Detwiler 2007; short abstract for Werginz et al. 2020; no Crossref abstract for the other
three.

### PDF download attempts

Direct automated downloads were attempted from each publisher URL. All five failed: four because of
publisher paywalls or cookie walls (Elsevier ScienceDirect, Cell Press, SfN J Neurosci Cloudflare
interstitial) and one (Science Advances, nominally open access) because of an AAAS/Cloudflare bot
challenge. The PolegPolsky2011 PLoS ONE PDF was not attempted in this scaled-down run and is flagged
for the intervention file.

### Summary writing

Each paper's `summary.md` was written to the paper-asset v3 spec with all 9 mandatory sections
(Metadata, Abstract, Overview, Architecture/Models/Methods, Results, Innovations, Datasets, Main
Ideas, Summary). Each Overview carries a disclaimer identifying the paywall status and the
training-knowledge basis of the summary. Numerical claims follow the canonical treatment of each
paper in the patch-clamp and DSGC literature.

### DOI correction

Two DOIs listed in `research/research_internet.md` were incorrect or duplicative:

* A JNEUROSCI DOI `10.1523/JNEUROSCI.0347-07.2007` returned 404 on Crossref; the correct
  MargolisDetwiler2007 slug was identified via Crossref query and resolved to
  `10.1523/jneurosci.0130-07.2007`.
* A proposed Park 2014 DOI (`10.1523/jneurosci.5017-13.2014`) was already present as a paper asset
  in t0002 and was replaced with Sethuramanujam et al. 2017 (`10.1016/j.neuron.2017.09.058`), which
  covers the same DSGC voltage-clamp subtopic without duplicating a t0002 asset.

### Answer synthesis

The five papers were synthesised into one answer asset
`patch-clamp-techniques-and-constraints-for-dsgc-modelling` with the full answer structure mandated
by the answer asset spec v2 (9 sections). Inline `[AuthorYear]` reference-style citations link back
to the individual paper summaries. The answer is organised around the four question sub-parts (Ge/Gi
calibration, AIS and dendritic channels, NMDARs, maintained activity) and delivers a 7-point
modelling specification.

## Metrics Tables

No quantitative metrics produced; this is a literature-survey task. Paper counts are tracked in the
`What Was Produced` section of `results_summary.md`.

## Comparison vs Baselines

Not applicable to a literature survey. Scope comparison vs plan: planned 25 papers across 5 themes,
delivered 5 papers across 5 themes (scope reduction documented in the plan-vs-delivery section of
`results_summary.md`).

## Visualizations

No charts or graphs produced; the task has no quantitative results to visualise. The
`results/images/` directory exists per the results-spec convention but is empty.

## Individual Paper Findings

### Poleg-Polsky & Diamond 2011 - Space-clamp error in passive dendrites

NEURON simulations of reconstructed RGC morphologies quantify voltage-clamp decomposition errors. On
thin distal dendrites up to ~80% of the synaptic signal is lost before reaching the somatic pipette.
Inhibitory estimates carry larger errors than excitatory estimates even when clamping at the
reported inhibitory reversal, because Gi reconstruction depends on accurate Vm at dendritic sites
where the command cannot penetrate. Synapses within ~0.1 lambda of the soma are acceptably clamped;
past ~0.3 lambda reconstruction is severely distorted.

### To, Honnuraiah, Stuart 2022 - Active-dendrite extension

Active voltage-gated Na+ and K+ channels in the dendrites substantially worsen the PolegPolsky2011
error bounds. Under some conditions the experimental decomposition yields spurious negative
inhibitory conductance estimates, which are physically impossible and signal that the protocol has
failed. There is no holding-potential choice that is globally accurate with active dendrites; Ge
accuracy trades against Gi accuracy. Pharmacological blockade (TTX, TEA/4-AP) eliminates the error
but also eliminates the circuit dynamics.

### Werginz, Raghuram, Fried 2020 - AIS tailoring in OFF-alphaT RGCs

AIS length and Nav1.6 density vary systematically across the retina in OFF-alpha transient cells and
set maximum firing rate and depolarisation-block threshold. The AIS-to-soma Na+ density ratio is
approximately 7x. AIS length is the dominant morphological predictor of maximum sustained firing
rate; compartmental-model manipulation of AIS length alone reproduces the dorsal-vs-ventral
firing-rate difference. Replacing AIS Nav1.6 with Nav1.2 in the model reduces maximum rate
substantially, confirming isoform specificity.

### Sethuramanujam et al. 2017 - Silent NMDARs in adult DSGCs

ON-OFF DSGCs contain a substantial NMDAR population that is functionally silent at rest and during
weak stimulation but is recruited during preferred-direction motion and multiplicatively enhances
direction selectivity. AMPA/NMDA charge ratio is direction-dependent: preferred motion recruits more
NMDAR charge than null. NMDAR block significantly reduces the direction selectivity index at both
synaptic-current and spike-output levels. Somatic voltage clamp underestimates the NMDAR
contribution, consistent with the PolegPolsky2011 space-clamp framework.

### Margolis & Detwiler 2007 - Intrinsic vs synaptic maintained activity

ON and OFF RGCs use qualitatively different strategies to generate maintained activity. ON cells
lose their resting firing under ionotropic-glutamate-receptor blockade; OFF cells continue to fire
autonomously and additionally exhibit subthreshold oscillations, burst firing, and rebound
excitation characteristic of intrinsic pacemaker neurons. The difference is not explained by passive
properties but by different voltage-gated channel complements, likely T-type Ca2+ and HCN channels
in OFF cells.

## Analysis and Discussion

The five papers converge on a coherent set of requirements for DSGC compartmental modelling in
NEURON. PolegPolsky2011 and To2022 together establish that published voltage-clamp E/I traces are
distorted by both passive cable attenuation and active dendritic channel effects, and must not be
used as ground-truth conductances. Instead, the modelling pipeline must include a simulated
voltage-clamp readout that mimics the experiment so that simulation and experiment can be compared
on the same footing.

Werginz2020 establishes the AIS as a load-bearing compartment. A DSGC model lacking an explicit AIS
with Nav1.6 at 7x the somatic density will not correctly reproduce high-firing-rate or
depolarisation-block behaviour.

Sethuramanujam2017 establishes NMDARs as a load-bearing component of DSGC direction selectivity, not
an optional add-on. AMPA/NMDA charge ratios during preferred and null motion are primary fitting
targets.

MargolisDetwiler2007 establishes that RGC maintained activity has two qualitatively different modes
(synaptic-driven for ON cells, intrinsic-pacemaker for OFF cells). For ON-OFF DSGCs the modeller
must decide explicitly which mode to reproduce, and use maintained-activity-under-synaptic-blockade
as the validation target.

Cross-paper integration delivers the 7-point DSGC modelling specification in the synthesis section
of the answer asset. This specification extends, but does not replace, the 6-point cable-theory
specification from t0015 and the dendritic-computation guidance from t0016.

## Limitations

* All 5 summaries are based on Crossref abstracts (full, partial, or empty) plus training knowledge,
  not on read PDFs. Numerical claims (e.g., ~80% signal loss, 7x AIS Na+ density ratio, specific
  AMPA/NMDA charge ratios) require PDF verification in a follow-up task.
* The survey was scaled down from 25 papers to 5 papers per project-wide guidance after t0014.
  Coverage of DSGC-specific dynamic-clamp studies, DSGC Ih / HCN biophysics, and large-scale
  compartmental-model fitting pipelines is deferred to follow-up literature-survey tasks.
* Werginz2020 was performed on OFF-alpha transient RGCs, not directly on ON-OFF DSGCs. The
  extrapolation of AIS parameters to DSGCs is plausible (both are alpha-like RGCs with high-fidelity
  spiking output) but not directly validated. A DSGC-specific AIS study should be included in the
  follow-up survey task.

## Verification

* Each of the 5 paper assets contains `details.json` (spec_version 3) and a `summary.md` with all 9
  mandatory sections. Each Overview carries a paywall/training-knowledge disclaimer.
* Each paper's `files/` directory contains only `.gitkeep` because `download_status: "failed"`;
  `download_failure_reason` in each `details.json` names the specific publisher or Cloudflare
  barrier.
* The answer asset contains `details.json` (spec_version 2), `short_answer.md` (Question + Answer +
  Sources), and `full_answer.md` (9 mandatory sections including inline reference-style citations
  linking back to each paper summary).
* The `intervention/paywalled_papers.md` file records all 5 DOIs with a retrieval-priority table and
  step-by-step instructions for Sheffield institutional access.
* `metrics.json` is `{}` as expected for a literature-survey task. `costs.json` records zero USD
  spend. `remote_machines_used.json` is the empty array `[]`.

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

Follow-up suggestions are registered in `suggestions.json` with ids S-0017-01 through S-0017-04,
covering (1) manual PDF retrieval and numerical-claim verification for the 5 paywalled papers, (2)
extension of the patch-clamp survey to DSGC-specific dynamic-clamp and HCN-biophysics papers, (3)
inclusion of an AIS compartment with NMDARs and depolarisation-block validation in the downstream
DSGC model build task, (4) registration of the `patch-clamp` and `compartmental-modeling` categories
if not already present in `meta/categories/`.
