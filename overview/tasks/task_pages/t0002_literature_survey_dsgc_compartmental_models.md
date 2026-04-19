# ✅ Literature survey: compartmental models of DS retinal ganglion cells

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_dsgc_compartmental_models` |
| **Status** | ✅ completed |
| **Started** | 2026-04-18T22:28:59Z |
| **Completed** | 2026-04-19T01:35:00Z |
| **Duration** | 3h 6m |
| **Task types** | `literature-survey` |
| **Categories** | [`cable-theory`](../../by-category/cable-theory.md), [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`patch-clamp`](../../by-category/patch-clamp.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 20 paper, 1 answer |
| **Step progress** | 9/15 |
| **Task folder** | [`t0002_literature_survey_dsgc_compartmental_models/`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/task_description.md)*

# Literature survey: compartmental models of DS retinal ganglion cells

## Motivation

This is the project's first research task. Before building any simulation we need a shared
knowledge base of what prior compartmental modelling work has done on direction-selective
retinal ganglion cells (DSGCs) and what each of the project's five research questions (RQs)
looks like in the literature. The survey feeds every downstream task: the target tuning curve
generator (t0004) needs published tuning-curve shapes, the morphology download (t0005) needs a
shortlist of reconstructed DSGCs, and the later Na/K optimisation and active-vs-passive
dendrite experiments need candidate channel models and parameter ranges.

## Scope

Cover all five project research questions at survey level:

1. **RQ1 Na/K combinations** — how published DSGC and related RGC models parameterise somatic
   sodium and potassium conductances, and what combinations reproduce directional AP firing.
2. **RQ2 morphology sensitivity** — how branching pattern, dendritic diameter, and compartment
   length have been shown to affect DS tuning.
3. **RQ3 AMPA/GABA balance** — ratio and spatial distribution of excitatory and inhibitory
   inputs, and their measured effect on DS sharpness.
4. **RQ4 active vs passive dendrites** — evidence for dendritic voltage-gated conductances in
   DSGCs, and modelling studies that compare active with passive dendrites.
5. **RQ5 angle-to-AP-frequency tuning curves** — reported tuning-curve shapes, peak rates,
   half-widths, and null-direction suppression levels that can serve as optimisation targets.

Minimum breadth:

* Include the six references already listed in `project/description.md` (Barlow & Levick 1965,
  Hines & Carnevale 1997, Vaney/Sivyer/Taylor 2012, Poleg-Polsky & Diamond 2016,
  Oesch/Euler/Taylor 2005, Branco/Clark/Häusser 2010).
* Add at least 14 more papers found by internet search, spread across the five research
  questions.
* Prefer papers with a clearly described compartmental model, published morphology, or
  quantitative angle-to-rate measurements.

## Approach

1. Run `/research-papers` using the six seed references to build initial paper assets.
2. Run `/research-internet` to find additional compartmental DSGC modelling papers and any
   patch-clamp studies that report tuning curves.
3. Download each selected paper via `/download-paper` so every cited paper becomes a paper
   asset with a summary.
4. Produce one answer asset that synthesises, across all five RQs, what the existing
   literature says about how to structure the DSGC modelling problem and what numbers to aim
   for.

## Expected Outputs

* ~20 paper assets under `assets/paper/` (each with `details.json`, `summary.md`, and the
  paper file under `files/`).
* One answer asset under `assets/answer/` summarising how existing compartmental DSGC models
  structure the five research questions and what numerical targets they provide.

## Compute and Budget

No external cost. Local LLM CLI only; no paid APIs or remote machines.

## Dependencies

None. This is the first research task.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses each of the five
  research questions.
* `compare_literature.md` is not required for a pure literature survey.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [How does the existing peer-reviewed literature on compartmental models of direction-selective retinal ganglion cells structure the five project research questions (Na/K conductances, morphology sensitivity, AMPA/GABA balance, active vs passive dendrites, and angle-to-AP-frequency tuning curves), and what quantitative targets does it provide?](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/) | [`full_answer.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/full_answer.md) |
| paper | [Two distinct types of ON directionally selective ganglion cells in the rabbit retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1002_cne.22678/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1002_cne.22678/summary.md) |
| paper | [Direction-Selective Dendritic Action Potentials in Rabbit Retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md) |
| paper | [NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion Discrimination in Retinal Ganglion Cells](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/summary.md) |
| paper | [A Central Role for Mixed Acetylcholine/GABA Transmission in Direction Coding in the Retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.04.041/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.04.041/summary.md) |
| paper | [Cross-compartmental Modulation of Dendritic Signals for Retinal Direction Selectivity](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/summary.md) |
| paper | [Wiring specificity in the direction-selectivity circuit of the retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/summary.md) |
| paper | [Species-specific wiring for direction selectivity in the mammalian retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature18609/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature18609/summary.md) |
| paper | [Direction selectivity in the retina: symmetry and asymmetry in structure and function](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/summary.md) |
| paper | [The mechanism of directionally selective units in rabbit's retina.](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.1965.sp007638/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.1965.sp007638/summary.md) |
| paper | [Physiological properties of direction-selective ganglion cells in early postnatal and adult mouse retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2008.161240/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2008.161240/summary.md) |
| paper | [Synaptic inputs and timing underlying the velocity tuning of direction-selective ganglion cells in rabbit retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/summary.md) |
| paper | [Dendritic Discrimination of Temporal Input Sequences in Cortical Neurons](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/summary.md) |
| paper | [Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using Temperature as an Independent Variable](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/summary.md) |
| paper | [The NEURON Simulation Environment](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/summary.md) |
| paper | [Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a Simulation of the Direction-Selective Ganglion Cell](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/summary.md) |
| paper | [Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and Inhibition in Retinal Direction-Selective Ganglion Cells](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/summary.md) |
| paper | [Diverse Synaptic Mechanisms Generate Direction Selectivity in the Rabbit Retina](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/summary.md) |
| paper | [Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells Lack Direction Tuning](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/summary.md) |
| paper | [Retinal direction selectivity in the absence of asymmetric starburst amacrine cell responses](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/summary.md) |
| paper | [The functional organization of excitation and inhibition in the dendrites of mouse direction-selective ganglion cells](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/) | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Factorial (g_Na, g_K) grid search on a DSGC compartmental model to
locate the DSI-maximising conductance ridge</strong> (S-0002-01)</summary>

**Kind**: experiment | **Priority**: high

No paper in the 20-paper corpus (including Fohlmeister2010, Schachter2010, PolegPolsky2016,
Vaney2012) reports a factorial grid search over somatic (g_Na, g_K) pairs for a DSGC — this is
the central gap identified for RQ1 by the survey. Run a grid with g_Na swept across 0.02-0.20
S/cm^2 and g_K (delayed rectifier) swept across 0.003-0.050 S/cm^2 on the baseline DSGC
morphology and 177+177 synaptic budget, record DSI, preferred peak, null residual, and
tuning-curve HWHM at each point, and publish the ridge of combinations that hit DSI 0.7-0.85
with peak 40-80 Hz and null < 10 Hz. This directly supplies the RQ1 answer the project needs.
Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Paired active-vs-passive dendrite experiment to reproduce the
Schachter2010 DSI gain (~0.3 -> ~0.7)</strong> (S-0002-02)</summary>

**Kind**: experiment | **Priority**: high

Schachter2010 reports that switching DSGC dendrites from passive to active (adding
Fohlmeister-like g_Na and g_K) raises DSI from ~0.3 to ~0.7 on the same morphology and
synaptic input, and Oesch2005 provides the TTX-sensitive dendritic Na+ spike patch-clamp data
that anchor this claim. Run two paired simulations that differ only in dendritic g_Na (0 vs
Schachter2010 density), holding morphology, synapse placement, and stimulus identical, and
report the DSI delta with 95% CI across synapse-placement seeds. This directly answers RQ4 and
isolates the dendritic-conductance contribution from morphology and synaptic effects.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Reproduce the PolegPolsky2016 baseline DSGC model from ModelDB
189347 as the project's starting compartmental simulation</strong>
(S-0002-03)</summary>

**Kind**: technique | **Priority**: high

PolegPolsky2016 (paper 10.1016_j.neuron.2016.02.013) is the closest published match to this
project's goal — a NEURON multi-compartmental mouse ON-OFF DSGC model with 177 AMPA + 177 GABA
synapses and NMDA multiplicative gain — with public code at ModelDB entry 189347. Download the
ModelDB code, run the original published stimulus, and verify the reproduced tuning curve
lands inside the published DSI 0.7-0.85 / peak 40-80 Hz / null < 10 Hz / HWHM 60-90 deg
envelope. This creates the reference implementation the later parameter-variation tasks (Na/K
grid, morphology sweep, E/I ratio scan) will fork from. Recommended task types:
code-reproduction.

</details>

<details>
<summary><strong>Factorial morphology sweep (branch orders, segment length, segment
diameter) at fixed synapse count</strong> (S-0002-04)</summary>

**Kind**: experiment | **Priority**: high

ElQuessny2021 concludes that global DSGC morphology has only a minor effect on the synaptic
E/I distribution, but the survey finds no paper that runs a clean factorial sweep over the
three local-electrotonic knobs separately. With synaptic count fixed at the PolegPolsky
177+177 baseline and dendrites set to active (Schachter2010 densities), vary (number of branch
orders, mean segment length, mean segment diameter) on an orthogonal grid, record DSI and HWHM
per point, and test whether segment diameter has the largest effect (as cable theory
predicts). This directly answers RQ2 and provides the morphology-sensitivity map the project
currently lacks. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>GABA/AMPA density ratio scan at fixed 3-5x null/preferred IPSC
asymmetry</strong> (S-0002-05)</summary>

**Kind**: experiment | **Priority**: medium

PolegPolsky2016 sets GABA/AMPA at 1:1 (177/177), while Park2014 and Taylor2002 constrain the
null/preferred IPSC ratio to 3-5x but not the total GABA density. Scan the GABA/AMPA density
ratio from 0.5 to 4.0 (keeping the 3-5x null asymmetry fixed, the 40-80 Hz preferred peak
fixed by the Na/K ridge, and the morphology and dendritic conductances fixed) and report how
tuning-curve HWHM and preferred peak rate co-vary. The expected pattern (sharper tuning at the
cost of lower peak rate) is stated in research_internet.md as hypothesis H4 but is not yet
tested in the literature. This directly refines the RQ3 answer. Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>NMDA multiplicative-gain ablation to isolate its contribution to
DSI</strong> (S-0002-06)</summary>

**Kind**: experiment | **Priority**: medium

PolegPolsky2016 reports that NMDA receptors multiplicatively scale excitatory drive by ~2x and
sharpen directional discrimination, but the survey did not find a published ablation that
isolates the NMDA contribution independently of the AMPA+GABA core. Run three configurations
on the reproduced DSGC baseline (AMPA+GABA only, AMPA+GABA+NMDA with PolegPolsky2016 NMDA
parameters, AMPA+GABA+NMDA with NMDA_gain swept 1-4x) and report the DSI, peak rate, and HWHM
trajectories. This answers a specific open RQ3/RQ4-adjacent question that the literature
states but does not isolate experimentally. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Download the four discovered papers not included in the 20-paper
budget (Sivyer2017, Euler2002, Enciso2010, Webvision)</strong> (S-0002-07)</summary>

**Kind**: dataset | **Priority**: medium

research_internet.md catalogues 22 peer-reviewed candidates but only 20 became paper assets.
The held-back items are Sivyer2017 (dendro-dendritic cholinergic control of dendritic spike
initiation, Nat Commun), Euler2002 (SAC dendritic Ca signals are themselves directional,
Nature), Enciso2010 (SAC-network compartmental model, J Comp Neurosci), and the Webvision-DSGC
review. Sivyer2017 and Euler2002 directly constrain RQ4 and the presynaptic drive for RQ3, and
Enciso2010 provides a compartmental SAC-network model that could seed the presynaptic GABA
input for the DSGC model. Download them via /add-paper in a dedicated task and extend the
corpus to 24 papers. Recommended task types: download-paper, literature-survey.

</details>

<details>
<summary><strong>Register SAC presynaptic drive model as an asset for downstream
DSGC input construction</strong> (S-0002-08)</summary>

**Kind**: library | **Priority**: medium

Briggman2011 (SBEM wiring) and Ding2016 (cross-species comparison) supply the structural E/I
bias; Park2014 and Taylor2002 supply the 3-5x null/preferred IPSC amplitudes;
Sethuramanujam2016 adds ACh/GABA co-release; Hanson2019 challenges the pure SAC-asymmetry
model. Consolidate these findings into a pre-built SAC presynaptic drive asset (a reusable
library or dataset: angle-dependent GABA conductance time courses, AMPA time courses, and
their spatial distributions on a DSGC) so downstream DSGC simulation tasks do not each
re-implement the presynaptic waveform construction. The asset should expose a pure-function
API that takes (stimulus angle, velocity, asymmetry parameter) and returns per-synapse
conductance time courses. Recommended task types: write-library, feature-engineering.

</details>

<details>
<summary><strong>Implement the tuning-curve scoring loss combining DSI, peak rate,
null residual, and HWHM targets</strong> (S-0002-09)</summary>

**Kind**: library | **Priority**: high

The survey surfaces four concurrent numerical targets an optimised DSGC model must hit (DSI
0.7-0.85, preferred peak 40-80 Hz, null residual < 10 Hz, HWHM 60-90 deg), and the project has
four registered metrics (direction_selectivity_index, tuning_curve_hwhm_deg,
tuning_curve_reliability, tuning_curve_rmse). Build a scoring library that takes a simulated
angle-to-AP-rate tuning curve plus the canonical target curve from t0004 and returns a single
scalar loss combining all four targets with documented weights (e.g., weighted Euclidean
distance in normalised space), plus per-metric residuals. This is the tool every downstream
optimisation task (Na/K grid, morphology sweep, E/I ratio scan) will depend on. Recommended
task types: write-library.

</details>

<details>
<summary><strong>Reproduce the Park2014 mouse ON-OFF DSGC tuning-curve dataset as
a validation benchmark</strong> (S-0002-10)</summary>

**Kind**: dataset | **Priority**: medium

Park2014 (paper 10.1523_JNEUROSCI.5017-13.2014) and Chen2009 (paper
10.1113_jphysiol.2008.161240) are the two papers that set the mouse ON-OFF DSGC RQ5 targets
(DSI 0.6-0.9, peak 40-80 Hz, HWHM 60-90 deg). Park2014 is available open-access. Digitise the
published tuning-curve figure(s) into a reusable dataset asset (angle in degrees, spike rate
in Hz, error bars, cell counts) so the model can be scored against measured data rather than
only against the analytic target in t0004. This gives the project a literature-grounded
validation benchmark distinct from the canonical analytic target. Recommended task types:
download-dataset, data-analysis.

</details>

## Research

* [`research_internet.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/research/research_internet.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/results/results_summary.md)*

# Results Summary: Literature Survey of Compartmental Models of DS Retinal Ganglion Cells

## Summary

Produced a 20-paper survey of compartmental models of direction-selective retinal ganglion
cells (DSGCs) covering all five project research questions, plus one synthesis answer asset
that integrates the findings with per-RQ quantitative targets. The corpus includes all six
seed references from `project/description.md` and 14 additional peer-reviewed papers spread
across the five RQs, and it establishes concrete numerical targets (DSI **0.7-0.85**,
preferred peak **40-80 Hz**, null residual **< 10 Hz**, half-width **60-90 deg**, **177 AMPA +
177 GABA** synapses, g_Na **0.04-0.10 S/cm^2**) that downstream compartmental-modelling tasks
must reproduce.

## Metrics

* **Paper assets produced**: **20** (6 seeds + 14 additional, matches
  `expected_assets.paper=20`)
* **Answer assets produced**: **1** (matches `expected_assets.answer=1`)
* **Papers with downloaded full text**: **17** (PDF/XML/markdown)
* **Papers with metadata-only assets**: **3** (Chen2009, Sivyer2010, Sethuramanujam2016, all
  paywalled, `download_status: "failed"` per spec v3)
* **RQ coverage by non-seed papers**: RQ1 **2**, RQ2 **3**, RQ3 **7**, RQ4 **3**, RQ5 **4** —
  every RQ has ≥ 2 non-seed papers (REQ-4)
* **Total cost**: **$0.00** (no paid APIs, no remote machines, matches
  `per_task_default_limit`)
* **Verificator pass rate**: **21/21** asset verificators (20 paper + 1 answer) return zero
  errors

## Verification

* `meta.asset_types.paper.verificator` — PASSED for all 20 paper assets (0 errors)
* `meta.asset_types.answer.verificator` — PASSED for the synthesis answer asset (0 errors, 0
  warnings)
* `grep -c "^### RQ" full_answer.md` — returns **5**, satisfying VC-5 of the plan
* `ls assets/paper/ | wc -l` — returns **20**, satisfying VC-3 of the plan
* `verify_step` on each completed step — PASSED (step tracker is consistent)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0002_literature_survey_dsgc_compartmental_models" ---
# Results Detailed: Literature Survey of Compartmental Models of DS Retinal Ganglion Cells

## Summary

This task produced a 20-paper literature survey of compartmental models of direction-selective
retinal ganglion cells (DSGCs) and one synthesis answer asset that integrates the findings
across all five project research questions. Every paper asset conforms to paper asset
specification v3 (with `details.json`, a canonical `summary.md`, and the paper file under
`files/` where downloadable or a `.gitkeep` plus `download_status: "failed"` where paywalled).
The answer asset conforms to answer asset specification v2 and provides per-RQ quantitative
targets that downstream compartmental modelling tasks (t0004 target tuning-curve generator,
t0005 morphology download, later Na/K optimisation and active-vs-passive dendrite experiments)
must reproduce.

## Methodology

**Machine**: Local developer workstation (Windows 11 Education, x86-64). No remote compute.

**Runtime**: Total wall-clock for the task from `create-branch` prestep (2026-04-18T23:05:41Z)
to the end of step 12 `results` poststep (approximately 2026-04-19T01:30:00Z) is **~2.5 h** of
orchestrator time, with the implementation step accounting for the bulk via parallel
`/add-paper` subagents (each paper ~15-25 min of subagent wall-clock). No simulation,
training, or inference was performed — the only compute activity was HTTP downloads and local
LLM CLI use.

**Start timestamp**: 2026-04-18T23:05:41Z (step 1 `create-branch` prestep)

**End timestamp**: 2026-04-19T01:30:00Z (step 12 `results` expected poststep)

**Methods used**:

* `papers` — peer-reviewed literature catalogued and summarized per paper asset spec v3
* `internet` — bibliographic metadata retrieval (DOIs, journal URLs, abstracts)

The `code-experiment` method was not used: this is a literature survey task and no simulation
code was written.

**Tools used**:

* `/add-paper` skill — invoked once per paper in a dedicated subagent
* `/planning` skill — used to produce `plan/plan.md`
* `meta.asset_types.paper.verificator` — validated every paper asset
* `meta.asset_types.answer.verificator` — validated the synthesis answer asset
* `arf.scripts.utils.doi_to_slug` — generated DOI-based folder slugs

## Metrics Tables

The project does not have a registered metric that applies to a pure literature survey, so
`metrics.json` is `{}` by design. The quantitative targets surfaced by the survey are recorded
as prose in the answer asset's `## Synthesis` section. Below is a condensed view of those
targets.

| RQ | Target / finding | Source paper IDs |
| --- | --- | --- |
| RQ1 Na/K conductances | g_Na peak 0.04-0.10 S/cm^2; g_K (DR) ~0.012 S/cm^2; g_K,A ~0.036 S/cm^2; g_K,Ca ~0.001 S/cm^2 | `10.1152_jn.00123.2009`, `10.1371_journal.pcbi.1000899`, `10.1016_j.neuron.2016.02.013`, `10.1038_nrn3165` |
| RQ2 morphology sensitivity | Global dendrite shape minimally changes the E/I synaptic map; local electrotonic compartments (lambda ~100-200 um) still matter | `10.1523_ENEURO.0261-21.2021`, `10.1126_science.1189664`, `10.1002_cne.22678`, `10.1016_j.neuron.2017.07.020`, `10.1038_nature09818`, `10.1038_nature18609` |
| RQ3 AMPA/GABA balance | 177 AMPA + 177 GABA synapses on reconstructed mouse DSGC; null-direction IPSC 3-5x preferred | `10.1016_j.neuron.2016.02.013`, `10.1523_JNEUROSCI.22-17-07712.2002`, `10.1523_JNEUROSCI.5017-13.2014`, `10.7554_eLife.52949`, `10.7554_eLife.42392`, `10.1016_j.neuron.2016.04.041`, `10.1113_jphysiol.1965.sp007638` |
| RQ4 active vs passive dendrites | Active dendrites with Fohlmeister densities raise DSI from ~0.3 (passive) to ~0.7 (active); TTX-sensitive dendritic Na+ spikes recorded in rabbit | `10.1371_journal.pcbi.1000899`, `10.1016_j.neuron.2005.06.036`, `10.1126_science.1189664`, `10.1016_j.neuron.2017.07.020`, `10.7554_eLife.52949` |
| RQ5 angle-to-AP-frequency tuning curves | Adult mouse ON-OFF DSGC: preferred peak 40-80 Hz; null 3-10 Hz; DSI 0.6-0.9; HWHM 60-90 deg | `10.1113_jphysiol.2008.161240`, `10.1523_JNEUROSCI.5017-13.2014`, `10.1113_jphysiol.1965.sp007638`, `10.1523_JNEUROSCI.22-17-07712.2002`, `10.1016_j.neuron.2005.06.036`, `10.1113_jphysiol.2010.192716` |

## Analysis

The 20 papers converge on a coherent compartmental-modelling recipe for mouse ON-OFF DSGCs.
The backbone (NEURON simulator per `10.1162_neco.1997.9.6.1179`) is uncontroversial. The
Fohlmeister ion-channel parameter set is the only point in the (g_Na, g_K) space that the
literature has calibrated against DSGC-like spiking — downstream task t0006+ should sweep
around this point rather than start from an uninformed grid. The Poleg-Polsky 177+177 synaptic
budget and the 3-5x null-to-preferred IPSC asymmetry are the two most load-bearing numbers for
any faithful compartmental DSGC: failing to reproduce both simultaneously means the resulting
DSI will miss the target window. The most surprising recent finding is the El-Quessny result
that global DSGC dendritic morphology only minimally influences the synaptic distribution of
excitation and inhibition; this means that morphology-swap experiments (t0005) should focus on
local electrotonic compartments and branching topology near the primary dendrite rather than
whole-tree shape. The weakest evidence is on RQ1 (there is no published factorial grid of
g_Na, g_K for DSGCs specifically) and on the downstream mapping from E/I synaptic drive to
angle-to-AP tuning-curve shape — these two gaps motivate the project's core experimental
agenda.

## Verification

* `meta.asset_types.paper.verificator` against every paper asset — 20/20 PASSED, 0 errors.
* `meta.asset_types.answer.verificator` against
  `how-does-dsgc-literature-structure-the-five-research-questions` — PASSED, 0 errors, 0
  warnings.
* `grep -c "^### RQ" full_answer.md` — **5** (matches plan VC-5: five per-RQ subsections).
* `ls tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/ | wc -l` — **20**
  (matches plan VC-3).
* `ls tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/ | wc -l` — **1**
  (matches expected_assets).
* Six seed paper folders (BarlowLevick1965, Hines1997, Vaney2012, PolegPolsky2016, Oesch2005,
  Branco2010) are present (matches plan VC-4).
* `verify_step` on every completed step — PASSED (step tracker is consistent and logs are in
  place).

## Limitations

Three papers could not be downloaded from open-access mirrors and remain as metadata-only
assets: Chen2009 (`10.1113_jphysiol.2008.161240`), Sivyer2010
(`10.1113_jphysiol.2010.192716`), and Sethuramanujam2016 (`10.1016_j.neuron.2016.04.041`). The
paper asset spec v3 explicitly supports this via `download_status: "failed"` and `.gitkeep`
under `files/`, and each metadata-only asset retains the journal-landing-page abstract. Key
quantitative claims attributed to these papers (Chen2009 and Sivyer2010 tuning-curve numbers,
Sethuramanujam2016 co-transmission result) come from their abstracts and not from full-text
re-reading, so the confidence on those specific numbers is lower than for the 17 fully
downloaded papers. Two ModelDB database entries flagged in `research/research_internet.md`
([ModelDB-PP2016], [Branco2010-MDB]) are not paper assets; they are code artefacts that belong
to a later implementation task. The survey does not include any literature on ON DSGCs in
non-mouse species beyond what Barlow & Levick 1965 (rabbit), Oesch 2005 (rabbit), and Taylor
2002 (rabbit) already provide — a downstream task could extend coverage to primate or
zebrafish DSGCs if needed.

## Files Created

* `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/` — 20 paper asset
  subfolders, each with `details.json`, `summary.md`, and `files/<...>` (or `.gitkeep`)
* `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/details.json`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/short_answer.md`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/full_answer.md`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/research/research_internet.md`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/plan/plan.md`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/results/results_summary.md`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/results/results_detailed.md`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/results/metrics.json`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/results/costs.json`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/results/remote_machines_used.json`
* `tasks/t0002_literature_survey_dsgc_compartmental_models/logs/steps/` — step logs for every
  executed and skipped canonical step

## Task Requirement Coverage

The operative task text from `task.json` and `task_description.md`:

```text
Name: Literature survey: compartmental models of DS retinal ganglion cells
Short description: Survey published compartmental models of direction-selective retinal ganglion
cells to inform all five project research questions.

Scope:
- Cover all five project research questions at survey level (RQ1-RQ5).
- Include the six seed references from project/description.md.
- Add at least 14 more papers found by internet search, spread across the five RQs.
- Prefer papers with a clearly described compartmental model, published morphology, or
  quantitative angle-to-rate measurements.
Expected outputs: ~20 paper assets; one answer asset synthesising all five RQs.
Verification: 20 paper assets pass verify_paper_asset; answer asset passes verify_answer_asset
and explicitly addresses each of the five RQs.
```

| ID | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Produce exactly 20 paper assets under `assets/paper/<paper_id>/`, each with the three mandatory artifacts | **Done** | `ls assets/paper/ \| wc -l` = 20; each folder contains `details.json`, canonical `summary.md`, and `files/<...>` or `.gitkeep` |
| REQ-2 | Include all six seed references | **Done** | Folders `10.1113_jphysiol.1965.sp007638`, `10.1162_neco.1997.9.6.1179`, `10.1038_nrn3165`, `10.1016_j.neuron.2016.02.013`, `10.1016_j.neuron.2005.06.036`, `10.1126_science.1189664` all exist |
| REQ-3 | Add ≥ 14 additional peer-reviewed papers beyond the seeds | **Done** | 14 additional DOIs downloaded: Schachter2010, Fohlmeister2010, Taylor2002, Chen2009, Park2014, Briggman2011, Ding2016, Sivyer2010, Hoshi2011, Koren2017, ElQuessny2021, Jain2020, Hanson2019, Sethuramanujam2016 |
| REQ-4 | Spread the 14 non-seed papers across all five RQs with ≥ 2 non-seed papers per RQ | **Done** | RQ1: 2 (Schachter2010, Fohlmeister2010); RQ2: 3 (Hoshi2011, Koren2017, ElQuessny2021); RQ3: 7 (Taylor2002, Park2014, Briggman2011, Ding2016, Jain2020, Hanson2019, Sethuramanujam2016); RQ4: 3 (Schachter2010, Koren2017, Jain2020); RQ5: 4 (Taylor2002, Chen2009, Park2014, Sivyer2010) — every RQ ≥ 2 |
| REQ-5 | Prefer papers satisfying a/b/c (compartmental model, morphology, angle-to-rate) | **Done** | Paper Selection table in `plan/plan.md` lines 150-170 maps each paper to its selection criterion; every selected paper satisfies ≥ 1 criterion |
| REQ-6 | Each paper asset conforms to paper asset spec v3 and verificator reports zero errors | **Done** | All 20 paper assets verified PASSED against `meta.asset_types.paper.verificator` with zero errors each |
| REQ-7 | Produce exactly one answer asset with five per-RQ subsections in `## Synthesis` | **Done** | `assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/full_answer.md` has `### RQ1 Na/K conductances`, `### RQ2 morphology sensitivity`, `### RQ3 AMPA/GABA balance`, `### RQ4 active vs passive dendrites`, `### RQ5 angle-to-AP-frequency tuning curves` (grep count = 5) |
| REQ-8 | Answer asset conforms to answer asset spec v2 | **Done** | `meta.asset_types.answer.verificator` reports PASSED with 0 errors and 0 warnings; `details.json` has `spec_version: "2"`, all required fields populated; short and full answers have all mandatory sections |
| REQ-9 | Zero external cost | **Done** | `results/costs.json` shows `total_cost_usd: 0`; no paid APIs or remote machines used |

</details>
