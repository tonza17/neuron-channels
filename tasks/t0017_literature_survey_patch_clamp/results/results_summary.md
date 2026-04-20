# Results Summary: Patch-Clamp Literature Survey

## Summary

Surveyed 5 high-leverage patch-clamp / voltage-clamp / space-clamp / DSGC papers and produced a
single answer asset giving a concrete 7-point compartmental-modelling specification for DSGCs in
NEURON covering voltage-clamp pipeline, AIS compartment, NMDAR synaptic complement, and intrinsic vs
synaptic maintained-activity biophysics. All 5 PDFs failed to download (4 paywalls + 1
Cloudflare/cookie-wall); summaries are based on Crossref abstracts plus training knowledge with
explicit disclaimers.

## Objective

Survey foundational patch-clamp / voltage-clamp / space-clamp literature and synthesize concrete
compartmental-modelling guidance for direction-selective retinal ganglion cells (DSGCs) in NEURON,
covering experimental technique bias corrections and DSGC-specific biophysics.

## What Was Produced

* **5 paper assets** covering the core patch-clamp / DSGC-biophysics literature:
  * Poleg-Polsky & Diamond 2011 - space-clamp error in passive dendrites, ~80% signal loss bound
  * To, Honnuraiah, Stuart 2022 - space-clamp error with active dendritic channels
  * Werginz, Raghuram, Fried 2020 - AIS biophysics tuning RGC output, 7x Na+ density ratio
  * Sethuramanujam et al. 2017 - NMDAR contribution to DSGC direction selectivity
  * Margolis & Detwiler 2007 - intrinsic vs synaptic RGC maintained activity
* **1 answer asset** `patch-clamp-techniques-and-constraints-for-dsgc-modelling` synthesising all 5
  papers into a concrete 7-point DSGC modelling specification (voltage-clamp pipeline, voltage-clamp
  readiness, active dendritic channels, AIS compartment, synaptic complement with NMDARs, intrinsic
  vs synaptic maintained activity, experimental-data vetting).
* **1 intervention file** `paywalled_papers.md` listing all 5 DOIs for manual Sheffield-access
  retrieval.

## Scope Change

Task was planned for ~25 papers across 5 themes; delivered scope was reduced to 5 high-leverage
papers per project-wide guidance after t0014 (`intervention/paywalled_papers.md`). The 5 selected
papers still span all 5 originally-planned themes (somatic whole-cell RGC recordings, voltage-clamp
E/I dissection, space-clamp errors, spike-train tuning biophysics, intrinsic-activity stimulus
protocols). Additional breadth in each theme is deferred to follow-up tasks.

## Download Outcomes

All 5 PDFs failed automated download:

* Poleg-Polsky & Diamond 2011 (PLoS ONE open access, pipeline failure)
* To et al. 2022 (Elsevier ScienceDirect cookie wall)
* Werginz et al. 2020 (AAAS Science Advances Cloudflare bot challenge)
* Sethuramanujam et al. 2017 (Cell Press Neuron cookie wall)
* Margolis & Detwiler 2007 (SfN J Neurosci Cloudflare interstitial)

Summaries are based on Crossref abstracts (full for MargolisDetwiler2007, partial for Werginz2020,
empty for the other three) plus training knowledge of the canonical treatment of each paper; every
Overview section contains a disclaimer to this effect.

## Key Synthesis Output

DSGC compartmental models in NEURON must:

1. Treat published somatic voltage-clamp Ge/Gi traces as lower bounds on distal dendritic
   conductances, not ground truth; plan model fits to absorb several-fold calibration uncertainty.
2. Include a somatic voltage-clamp block that mimics the experimental amplifier for matched-readout
   comparison against experimental traces.
3. Include voltage-gated Na+ and K+ channels in the dendritic tree at published densities; these
   interact with the voltage-clamp readout.
4. Include an explicit AIS compartment with Nav1.6 at approximately 7x the somatic Na+ density, with
   AIS length a named tunable parameter constrained by immunohistochemistry.
5. Include NMDARs with standard Mg2+ block kinetics on DSGC dendrites; fit to AMPA/NMDA charge
   ratios during preferred and null motion, not only peak AMPA current.
6. Declare the target DSGC subtype's expected maintained-activity profile and include T-type Ca2+ /
   HCN channels if intrinsic-pacemaker biophysics are required; validate via
   maintained-activity-under-synaptic-blockade.
7. Vet experimental E/I traces for decomposition failure (spurious negative Gi, extreme distal
   components) and exclude failed traces from fitting training sets.

## Metrics

No quantitative metrics produced; this is a literature-survey task. `metrics.json` is `{}`.

## Costs

No API or compute costs. `costs.json` records `total_cost_usd: 0.00`.

## Verification

* 5 paper assets present in `assets/paper/` with `details.json` and `summary.md` each; `files/`
  contains `.gitkeep` (downloads failed).
* 1 answer asset present in
  `assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/` with `details.json`,
  `short_answer.md`, `full_answer.md`.
* All 5 paywalled DOIs documented in `intervention/paywalled_papers.md` with retrieval priority.
* `metrics.json` empty `{}` (expected - literature survey produces no quantitative metrics).
* `costs.json` and `remote_machines_used.json` record zero cost and no remote machines used.
