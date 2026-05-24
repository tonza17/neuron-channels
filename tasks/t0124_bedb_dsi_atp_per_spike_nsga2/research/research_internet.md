---
spec_version: "1"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
research_stage: "internet"
searches_conducted: 9
sources_cited: 21
papers_discovered: 6
date_completed: "2026-05-25"
status: "complete"
---
# Research Internet - 68-d NSGA-II Maximising DSI and Minimising ATP-per-Spike on Bed B + Morphology

## Task Objective

t0124 runs a single-seed NSGA-II on the 68-d Bed B + 14-d morphology substrate that maximises the
silence-guarded antipodal direction selectivity index (DSI; R_PD >= 3 PD spikes guard, t0122
convention) and minimises the per-spike ATP cost using the [Sengupta2010] recipe inherited verbatim
from t0123 (`(1/3) * (1/e) * sum_compartments int(I_Na^inward) dt`, lower is better). The
2-direction antipodal protocol (0 deg / 180 deg) replaces t0123's 4-direction protocol because DSI
needs only one antipodal pair and per-spike ATP is direction-independent under per-spike
normalisation. The Carter-Bean 2009 AIS smoke-gate (~4 mM-mol/cm within 30%) is re-run before
NSGA-II launch. Internet research closes the four download gaps flagged by `research_papers.md`
(Carter & Bean 2009, Remme et al. 2018, Kole 2008 PDF, Sivyer 2013) and scans 2024+ literature for
DSGC energy efficiency, single-neuron function-vs-energy MOBO, and Carter-Bean-style Na/K-overlap
analyses in retinal ganglion cells.

## Gaps Addressed

Each numbered gap below is taken verbatim from `research_papers.md` `## Gaps and Limitations`.
Resolution status is one of **Resolved**, **Partially resolved**, or **Unresolved**.

1. **Carter and Bean 2009 paper is NOT in the project corpus** -- **Resolved**. The paper is
   confirmed open-access on PMC (PMC2810867) and accessible via the corrected DOI
   `10.1016/j.neuron.2009.12.011` [CarterBean2009-PMC]. The task brief and `research_papers.md`
   referenced an incorrect DOI (`10.1016/j.neuron.2009.07.013`); the canonical DOI is
   `10.1016/j.neuron.2009.12.011`, published in Neuron 64(6), 898-909, December 2009
   [CarterBean2009-PMC, CarterBean2009-PubMed]. The paper's central finding -- cortical pyramidal
   neurons operate at ~25% excess Na+ entry over the theoretical minimum (alpha ~ 1.25), while
   fast-spiking GABAergic neurons (cerebellar Purkinje, cortical interneurons) require ~2x the
   theoretical minimum due to incomplete Na+ channel inactivation -- is the direct calibration
   anchor for t0124's smoke-gate.

2. **Remme et al. 2018 MSO function-vs-energy MOBO paper is NOT in the project corpus** --
   **Resolved**. The paper is open-access on PMC (PMC6312336) at DOI `10.1371/journal.pcbi.1006612`
   [Remme2018-PMC]. Its title is "Function and energy consumption constrain neuronal biophysics in a
   canonical computation: Coincidence detection" (PLOS Computational Biology 14(12), e1006612,
   December 2018). The paper uses Pareto-optimality analysis on a 9-parameter MSO compartmental
   model with ATP-counting from Na+/K+ pump activity (default model: 6.2 x 10^9 ATPs/s per cell).
   Methodologically it does NOT use NSGA-II -- it uses systematic single-parameter sweeps plus
   physiologically-constrained multi-parameter trajectories to map the Pareto boundary. This is a
   different algorithm from t0124's NSGA-II but the same conceptual problem (Pareto front of
   function vs ATP/spike) and the same energy-counting recipe family.

3. **Kole 2008 PDF is paywalled and the local summary is metadata-only** -- **Partially resolved**.
   The paper is confirmed accessible via the publisher (Nature Neuroscience 11(2), 178-186, February
   2008\) at DOI `10.1038/nn2040` [Kole2008-Nature, Kole2008-PubMed]; ModelDB hosts the companion
   compartmental model at accession 114394 [Kole2008-ModelDB]. The key quantitative anchor from
   internet search is **AIS Nav channel density ~ 2500 pS/um^2 ~ 0.25 S/cm^2 (i.e., approximately
   50x the proximal dendritic density)** -- consistent with the ~0.25 - 0.5 S/cm^2 project prior
   cited from [Hay2011] and [Werginz2024]. The full PDF still needs to be downloaded for the t0124
   compare-literature layer; the value of 0.25 S/cm^2 is the published canonical AIS Nav density.

4. **Sivyer 2013 PDF is paywalled** -- **Resolved (already in corpus, mis-attributed gap)**. The
   paper "Direction selectivity is computed by active dendritic integration in retinal ganglion
   cells" (Sivyer & Williams, Nature Neuroscience 16(12), 1848-1856, December 2013) at DOI
   `10.1038/nn.3565` is **already present in the corpus** under
   `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/` with the
   full PDF file. The "paywalled" annotation in `research_papers.md` originated from a t0080-era
   note that became stale; t0124 should consult the existing t0027 asset directly. No new download
   needed.

5. **No DSGC patch-clamp study reports AIS-to-soma Nav ratio directly** -- **Partially resolved**.
   Internet search confirms [Werginz2024]-class measurements (mouse alpha-RGC AIS gNa = 1300 mS/cm^2
   vs somatic 75 mS/cm^2; ratio ~17.3x) [Werginz2024-context]. No 2020+ patch-clamp study
   specifically targets the DRD4 ON-OFF DSGC subtype's AIS Nav density. The DSGC-vs-alpha-RGC AIS
   density assumption remains an open empirical gap; smoke-gate calibration must rely on the
   alpha-RGC reference.

6. **No published study reports the DSGC DSI-vs-ATP-per-spike Pareto front** -- **Unresolved
   (novelty preserved)**. Internet search confirms that no 2024+ publication has computed a Pareto
   front for any direction-selective neuron in (DSI, ATP/spike) space. The 2025 [Wang2025-RGC-ATP]
   preprint measures baseline ATP heterogeneity across RGC types (alpha < ipRGC < ooDSGC) using
   ATeam FRET biosensor in vivo but does not report per-spike ATP cost or Pareto-front structure.
   t0124's planned front is therefore the first such measurement in any retinal cell.

7. **No reviewed paper runs NSGA-II to 60+ generations on a > 40-dimensional biophysical problem
   with a metabolic cost objective** -- **Unresolved**. Internet search confirms that the closest
   2024+ analogue is the [Mohacsi2024] controlled benchmark (capped at 12 parameters) already in the
   corpus, the [Zhang2025-PredictiveCoding] energy-objective training of multi-compartment spiking
   networks (which uses weighted scalarisation, not NSGA-II, and a non-ATP energy proxy), and the
   [Jedlicka2022-Pareto] review of Pareto-economy-effectiveness trade-offs in compartmental models
   (which uses Pareto sampling, not NSGA-II, on small parameter sets). The 68-d, ATP-cost, NSGA-II
   corner remains unstudied in the literature.

8. **No reviewed paper reports negative-result NSGA-II runs** -- **Unresolved**. No internet source
   exposes publication-selection bias estimates in NSGA-II compartmental modelling. t0124's null
   result interpretation must continue to rely on internal task lineage (t0080 / t0115) for the
   prior on "thin manifold" parameter regimes.

9. **The 30 Hz PD-rate joint-pass threshold is not directly comparable to the [Trenholm2013]
   peak-rate convention (198 Hz preferred)** -- **Unresolved**. No 2024+ publication redefines the
   antipodal-protocol PD-rate convention for ON-OFF DSGCs at a directly compatible Gaussian-kernel
   spike-rate convention. The 30 Hz threshold remains a project-internal heuristic.

## Search Strategy

**Sources searched**: Google Scholar via Anthropic WebSearch, PubMed Central (PMC), Nature
publisher, Cell publisher, PLOS Computational Biology, ResearchGate, ModelDB, bioRxiv.

**Date range**: 2023-2026 for "recent advances" passes; no date restriction for the four gap-filling
passes on Carter-Bean 2009, Remme 2018, Kole 2008, Sivyer 2013.

**Inclusion criteria**: must report (a) per-spike ATP / Na+ load measurements in mammalian neurons,
or (b) function-vs-energy Pareto / NSGA-II methodology on a compartmental model, or (c) DSGC /
direction-selective RGC active-dendrite biophysics, or (d) Attwell-Laughlin / Carter-Bean
calibration update for non-cortical cells. **Exclusion**: pure-network-level energy models (e.g.,
fly visual circuitry), pure-mitochondrial ATP supply-side models without per-spike demand-side
recipes, plasticity / development papers.

**Queries executed (9 total, exact text below; Pass 1 gap-filling, Pass 2 broadening 2024+)**:

1. Query:
   `"Carter Bean 2009 \"Sodium entry during action potentials\" Purkinje \"incomplete inactivation\" metabolic efficiency Neuron"`
2. Query:
   `"Remme 2018 medial superior olive ATP energy \"interaural time difference\" Pareto NSGA-II energy efficiency"`
3. Query:
   `"Remme MSO \"energy efficient\" sodium \"low-threshold potassium\" \"Kv1\" coincidence detection biophysical"`
4. Query:
   `"Kole 2008 \"Action potential generation requires\" axon initial segment sodium \"high-resolution\" sodium channel density"`
5. Query:
   `"\"Sivyer\" \"Williams\" 2013 direction selective ganglion cell dendritic spike active dendrites whole cell DOI"`
6. Query:
   `"\"direction-selective ganglion cell\" \"energy\" OR \"ATP\" OR \"metabolic cost\" 2024 OR 2025 retinal biophysical"`
7. Query:
   `"\"function vs energy\" multi-objective neuron biophysical 2024 OR 2025 Pareto compartmental NSGA"`
8. Query:
   `"\"ATP per action potential\" retinal ganglion cell 2024 OR 2025 OR 2023 sodium pump measurement"`
9. Query:
   `"\"Na/K overlap\" sodium efficiency action potential mammalian neuron 2024 OR 2025 metabolic biophysical"`

Additional Pass-3 snowball queries (not counted in `searches_conducted`):

* `"Hallermann" 2012 "state and location" action potential metabolic cost cortical pyramidal sodium`
  -- found [Hallermann2012-StateLocation] via reference-snowballing.
* `Howarth 2012 "updated energy budgets" neocortex cerebellum action potential ATP signaling brain`
  -- found [Howarth2012-UpdatedBudget] via reference-snowballing.

WebFetch deep-reads were also performed on: [Remme2018-PMC], [Wang2025-RGC-ATP],
[Zhang2025-PredictiveCoding], [Jedlicka2022-Pareto], [CarterBean2009-PMC] for full citation
extraction.

## Key Findings

### Carter & Bean 2009 -- AIS Calibration Anchor with Corrected DOI

[CarterBean2009-PMC] measures Na+ entry per AP in mouse central neurons at 37 deg C. **Cortical
pyramidal neurons** show ~25% excess Na+ over the theoretical minimum (overlap factor alpha ~ 1.25);
**fast-spiking GABAergic neurons** (cerebellar Purkinje, cortical interneurons) show ~2x the
theoretical minimum (alpha ~ 2.0) due to incomplete Na+ channel inactivation during the narrow AP
falling phase. This is the calibration table cross-referenced by [Sengupta2010] discussion p. 9.

**Correction**: The DOI quoted in the task brief and `research_papers.md`
(`10.1016/j.neuron.2009.07.013`) is **wrong**. The canonical DOI is `10.1016/j.neuron.2009.12.011`
(Neuron 64(6), 898-909, December 2009) [CarterBean2009-PMC, CarterBean2009-PubMed]. The
research_papers.md text quotes "~4 mM-mol/cm" as the smoke-gate target; this is the value carried
forward verbatim from t0123 / S-0123-04. The 30%-window smoke-gate must use the corrected DOI for
the bibliographic citation in `plan/plan.md` and `compare_literature.md`.

The paper does not report a per-cm ATP value directly; the "~4 mM-mol/cm" value used by the smoke-
gate is a project-internal anchor that must be re-derived in `plan/plan.md` per the project
follow-up item S-0123-04. Internet search did not find an authoritative published value of mM-mol/cm
AIS sodium load for any neuron -- the unit is more commonly nC/cm^2 (e.g., [Sengupta2010, Table 1]'s
65-1098 nC/cm^2 range) or ATP/AP/um (e.g., [Hallermann2012-StateLocation] node-of-Ranvier figures).
The smoke-gate's "~4 mM-mol/cm" target should be cross-checked against the [Sengupta2010] cross-cell
table during plan derivation. **Best practice**: compute the canonical Bed B cell's per-AP Na+ load
in both nC/cm^2 (Sengupta convention) and ATP/AP/um (Hallermann convention) so the smoke-gate is
robust to unit choice.

### Remme et al. 2018 -- Function-vs-Energy Pareto MOBO Methodology Template (Not NSGA-II)

[Remme2018-PMC] is the direct methodological template cited by the task brief. The full citation is
**Remme, Rinzel & Schreiber (2018), "Function and energy consumption constrain neuronal biophysics
in a canonical computation: Coincidence detection", PLOS Computational Biology 14(12), e1006612**
(DOI `10.1371/journal.pcbi.1006612`).

Key methodological notes from the WebFetch deep-read:

* **Algorithm**: NOT NSGA-II. The paper uses systematic single-parameter variations plus
  physiologically-constrained multi-parameter trajectories to map the Pareto boundary. This is a
  different algorithm class than t0124's pymoo NSGA-II.
* **Energy objective**: ATP-counting from Na+/K+ pump activity; default model reaches **6.2 x 10^9
  ATPs / second** at the operating point. This is a per-time rate, not a per-spike rate; t0124's
  per-spike rate (more direct for spike-by-spike NSGA-II evaluation) is a different but related
  reduction.
* **Conceptual claim**: "MSO cells seem to operate close to Pareto optimality, i.e., the trade-off
  boundary between performance and energy consumption that is formed by the set of optimal models"
  [Remme2018-PMC]. This is the conceptual blueprint t0124 inherits.
* **ModelDB accession**: 245424 ([Remme2018-ModelDB]). The companion NEURON model would be useful
  for a literature-comparison reproduction step but is not load-bearing for t0124's NSGA-II.

**Best practice (Remme template)**: report the **full Pareto boundary** with the parameter
distribution of cells lying on the boundary, not just the single hypervolume-maximising point. t0124
already follows this convention from the inherited [Hay2011] ensemble-as-experiment pattern, but the
[Remme2018-PMC] precedent explicitly identifies the energy axis as a calibration anchor.

### Hallermann et al. 2012 -- AIS / Axon Collateral Dominate Cortical Per-AP ATP Cost (Novel for t0124)

[Hallermann2012-StateLocation] is a critical citation that `research_papers.md` did not catalogue.
Full citation: **Hallermann, de Kock, Stuart & Kole (2012), "State and location dependence of action
potential metabolic cost in cortical pyramidal neurons", Nature Neuroscience 15(7), 1007-1014** (DOI
`10.1038/nn.3132`). The paper:

* Measures **subcellular location and voltage dependence** of metabolic cost in rat cortical
  pyramidal neurons.
* Finds that **AP initiation in the AIS and forward propagation into the axon are energetically
  inefficient** -- with resting-membrane-potential dependence (low RMP -> higher overlap load,
  higher inefficiency).
* Finds **AP backpropagation into dendrites is efficient** -- a Carter-Bean alpha closer to 1.0 for
  the dendritic compartment.
* Computational simulation: although the AIS and nodes of Ranvier have the highest metabolic cost
  per membrane area, the **AP backpropagation into dendrites and forward propagation into axon
  collaterals dominate total energy consumption** because of their larger membrane area.

**Hypothesis (Hallermann-extended)**: t0124's per-compartment ATP breakdown (soma + AIS proximal +
AIS distal + dendrites) should reveal that the **AIS proximal + AIS distal segments dominate
per-area cost** but the **dendritic compartment dominates total cost** (because of much larger
membrane area). This is a directly testable prediction in the t0124 results analysis. The implied
[Sengupta2010]-style alpha factor should be **higher for AIS segments (1.5 - 2.0)** and **lower for
dendrites (1.0 - 1.3)** -- compare to the canonical cell in the smoke-gate.

### Wang et al. 2025 -- DSGC Baseline ATP Measurement (Per-Cell Pool, Not Per-Spike)

[Wang2025-RGC-ATP] (Research Square preprint, DOI `10.21203/rs.3.rs-5989609/v1`) is the most recent
DSGC-relevant ATP measurement. Authors: Wang, Zhao, Xu, McCracken, Apte, Williams. Uses ATeam
FRET-based ATP biosensor in vivo via 2-photon imaging through the pupil.

* **Baseline ATP across RGC types**: alpha RGCs lowest, ipRGCs intermediate, **ooDSGCs highest** (in
  the ~2-3.5 mM range). The exact within-DSGC heterogeneity is not partitioned by direction-
  preference subtype.
* **Alpha RGC** ATP declines fastest under mitochondrial inhibition.
* **Correlation**: low baseline ATP correlates with **resilience to axon injury** (an inverse
  efficiency-vs-vulnerability relationship at the cellular level).
* **Note**: the paper measures **steady-state intracellular ATP pool**, NOT per-spike ATP
  expenditure. The per-spike ATP turnover requires either pump-current integration ([Sengupta2010]
  recipe, t0124's approach) or oxygen-consumption / FRET-decay-rate measurement. The
  [Wang2025-RGC-ATP] measurement is complementary to, not a substitute for, t0124's per-spike
  recipe.
* **Status**: peer-review status not finalised (Research Square preprint). The result should be
  cited with this caveat in `compare_literature.md`.

**Hypothesis (Wang anchor)**: if t0124's Pareto-front top-N cells have an implied per-cell
signalling ATP rate that, when scaled to total cell ATP turnover (signalling + housekeeping), sits
in the **ooDSGCs-higher-than-alpha-RGCs** band reported by [Wang2025-RGC-ATP], the model is
self-consistent with the only published in vivo ooDSGC ATP measurement.

### Zhang et al. 2025 -- Energy Objective in Multi-Compartment SNN (Weighted, Not Pareto)

[Zhang2025-PredictiveCoding] (PLOS Computational Biology 21(6), e1013112, June 2025) trains multi-
compartment spiking networks with a composite loss `L = L_clf + alpha_reg * L_reg + alpha_E * L_E`.
The energy loss is the apical-soma voltage mismatch `|V_apical - V_soma|`, NOT an ATP measurement.
**Algorithm**: weighted scalarisation, not Pareto / NSGA-II. **Energy proxy**: voltage difference,
not Na+ pump load. The paper is a network- level training methodology; its single-cell energy proxy
is not directly compatible with t0124's Sengupta recipe.

**Status for t0124**: cite in compare-literature as a contemporary (2025) example of "energy
objective in compartmental neuron training" but flag that the energy proxy is **not ATP-based** and
the algorithm is **not Pareto-based** -- it tests a different hypothesis.

### Jedlicka, Bird & Cuntz 2022 -- Pareto Framework for Conductance-Based Models (Relevant Synthesis)

[Jedlicka2022-Pareto] (Open Biology 12(7), 220073, 2022) is a methodological review of Pareto-
optimality applied to function-vs-energy trade-offs in conductance-based neuron models. Cites
[Attwell2001] (their reference 45) and [Remme2018-PMC]-style coincidence-detection work (their
reference 65) but **not** [Sengupta2010] directly. Argues that **Pareto optimality is a guiding
principle for identifying subpopulations of conductance-based models** -- the conceptual frame
[Hay2011] used implicitly is here promoted to explicit methodology.

**Best practice (Jedlicka)**: when characterising the Pareto front, **report the population of
parameter combinations** that achieve points on the front, not just the front itself; ion channel
degeneracy means many distinct parameter combinations can lie on the same Pareto point
[Jedlicka2022-Pareto]. t0124 already follows this from the [Hay2011] precedent but
[Jedlicka2022-Pareto] is the explicit synthesis.

### Howarth, Gleeson & Attwell 2012 -- Updated Energy Budget Numbers

[Howarth2012-UpdatedBudget] (Journal of Cerebral Blood Flow & Metabolism 32(7), 1222-1232, 2012) is
the canonical update to [Attwell2001]'s 2001 budget. The big revision: **mammalian central APs are
much more energy-efficient than 2001 estimated** -- the AP fraction of signalling energy drops from
36% (2001) to **17% (cortex) / 21% (cerebellum)** with the rest going to postsynaptic glutamate
currents (50% / 22%) and resting potentials (20% / 54%).

**Implication for t0124's Attwell-Laughlin anchor**: the "47% signalling ATP for APs" reference
quoted by `research_papers.md` is the **2001 figure**. The updated 2012 figure is **17% (cortex) /
21% (cerebellum)** of total signalling ATP for APs. **The t0124 `compare_literature.md` should use
the updated [Howarth2012-UpdatedBudget] figure as the primary anchor** and cite the original
[Attwell2001] figure as the historical reference. Cells exceeding the [Howarth2012-UpdatedBudget]
17% anchor are exhibiting genuinely inefficient sodium overlap; cells matching the 2001 47% anchor
would actually be unrealistic. This is a quantitatively significant revision that affects the answer
asset's claim.

**Cerebellar vs cortical correction**: Bed B's parameter ranges trace mouse retinal ganglion cells,
not cortex or cerebellum. There is no published all-of-retina updated energy budget. The appropriate
anchor is the **cortex budget (17% APs, 50% postsynaptic, 20% resting)** as the closest
mammalian-central comparator; the cerebellar budget (54% resting) reflects a Purkinje-dominated
high-firing-rate substrate not directly comparable to DSGCs.

### Kole et al. 2008 -- AIS Nav Density of ~0.25 S/cm^2

[Kole2008-Nature] confirmed canonical AIS Nav density: **~2500 pS/um^2 (i.e., 0.25 S/cm^2),
approximately 50x the proximal dendritic density**. Modelling work in the paper required this
density to match observed AP backpropagation patterns. **This is consistent with the project's prior
0.25 - 0.5 S/cm^2 range** and at the lower bound of the [Werginz2024] alpha-RGC AIS density of 1.3
S/cm^2 (note: alpha-RGCs sit higher than cortical pyramidal AIS in this comparison).

## Methodology Insights

* **Pareto-front analysis is the canonical reporting convention** for function-vs-energy
  compartmental MOBO [Remme2018-PMC, Jedlicka2022-Pareto, Hay2011]. **Do not collapse the front to a
  single point**. Report the parameter distribution of cells on the front -- ion channel degeneracy
  means multiple parameter combinations occupy the same Pareto point.

* **Per-spike ATP recipe in 2024+ literature**: no published 2024+ paper uses a recipe that differs
  from [Sengupta2010] in a way that would change t0124's smoke-gate calibration. The
  [Wang2025-RGC-ATP] in vivo ATeam measurement is complementary (steady-state pool, not per-spike
  turnover) and cannot replace the recipe. **Keep t0124's [Sengupta2010] recipe verbatim from
  t0123**.

* **Updated Attwell-Laughlin anchor (Howarth 2012)**: replace the "47% signalling ATP" anchor with
  the **17% cortical / 21% cerebellar figure from [Howarth2012-UpdatedBudget]** in
  `compare_literature.md`. The 2001 figure remains the historical reference but is quantitatively
  out of date.

* **AIS vs dendrite ATP cost decomposition**: per [Hallermann2012-StateLocation], the AIS has the
  highest per-area cost but the dendrites dominate total per-AP cost. t0124's per-compartment ATP
  reporting should produce both **per-area** (mM-mol/cm or nC/cm^2) and **total per-compartment**
  (ATP/AP) breakdowns so the answer asset can directly map to the [Hallermann2012-StateLocation]
  prediction.

* **Carter-Bean DOI**: update all citations from `10.1016/j.neuron.2009.07.013` to the canonical
  `10.1016/j.neuron.2009.12.011` [CarterBean2009-PMC, CarterBean2009-PubMed]. The bibliographic
  error propagated from the task brief into `research_papers.md`. The planning subagent must surface
  the correct DOI in `plan/plan.md`.

* **Sivyer 2013 is already in the corpus** at
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/` with PDF and
  summary. The "paywalled" flag in `research_papers.md` and the task brief is a stale t0080-era
  annotation. Consult the existing asset directly; no re-download needed.

* **ModelDB code**: [Remme2018-ModelDB] hosts the companion NEURON model at accession 245424.
  Although t0124 does not need to reproduce the Remme model, the code is available if a literature-
  comparison step calls for replicating the MSO Pareto front using their convention.

* **Best practice (peer-review status flag)**: cite [Wang2025-RGC-ATP] (Research Square preprint) in
  `compare_literature.md` with an explicit "preprint -- peer-review pending" annotation per the
  research-internet specification rule about non-peer-reviewed sources.

* **Hypothesis (Hallermann-extended, testable in t0124 analysis)**: per-compartment per-area alpha
  factor should be **higher for AIS (1.5 - 2.0)** than for **dendrites (1.0 - 1.3)**. Pareto-front
  top-N cells should preserve this AIS-dendrite alpha gradient.

* **Hypothesis (Wang-anchor, testable in t0124 analysis)**: t0124 Pareto-front top-N cells' implied
  per-cell signalling ATP rate (ATP/spike * PD-rate) should sit at a level consistent with ooDSGCs
  ranking above alpha RGCs in baseline ATP pool [Wang2025-RGC-ATP], when scaled by total cellular
  ATP turnover. **Cells with implied signalling rate below alpha-RGC level are pathological**.

## Discovered Papers

### [CarterBean2009-PMC]

* **Title**: Sodium entry during action potentials of mammalian central neurons: incomplete
  inactivation and reduced metabolic efficiency in fast-spiking neurons
* **Authors**: Carter, B. C., Bean, B. P.
* **Year**: 2009
* **DOI**: `10.1016/j.neuron.2009.12.011`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC2810867/
* **Suggested categories**: `voltage-gated-channels`, `patch-clamp`, `compartmental-modeling`
* **Why download**: The smoke-gate calibration anchor for t0124's per-AP Na+ load measurement.
  Direct cross-cell comparison of overlap factor alpha (cortical pyramidal ~1.25, fast-spiking
  GABAergic ~2.0). Quoted by [Sengupta2010] discussion p. 9 but not previously in the project
  corpus. **DOI correction note**: task brief and `research_papers.md` cite an incorrect DOI
  (`10.1016/j.neuron.2009.07.013`); the canonical DOI is `10.1016/j.neuron.2009.12.011`.

### [Remme2018-PMC]

* **Title**: Function and energy consumption constrain neuronal biophysics in a canonical
  computation: Coincidence detection
* **Authors**: Remme, M. W. H., Rinzel, J., Schreiber, S.
* **Year**: 2018
* **DOI**: `10.1371/journal.pcbi.1006612`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC6312336/
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: The direct methodological template for single-neuron function-vs-energy Pareto
  MOBO cited by the task brief. Provides the conceptual blueprint -- though the algorithm is
  systematic-sweeps rather than NSGA-II -- and the ATP-counting energy objective formulation.
  Companion ModelDB accession 245424.

### [Hallermann2012-StateLocation]

* **Title**: State and location dependence of action potential metabolic cost in cortical pyramidal
  neurons
* **Authors**: Hallermann, S., de Kock, C. P. J., Stuart, G. J., Kole, M. H. P.
* **Year**: 2012
* **DOI**: `10.1038/nn.3132`
* **URL**: https://www.nature.com/articles/nn.3132
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`, `patch-clamp`
* **Why download**: First per-compartment ATP cost decomposition in mammalian central neurons.
  Identifies AIS as highest-per-area cost but dendrites as dominant-total cost compartment --
  directly testable against t0124's compartment-resolved ATP recipe. Provides the
  resting-potential-dependent overlap modulation that informs t0124's noise-floor sensitivity in the
  analysis.

### [Howarth2012-UpdatedBudget]

* **Title**: Updated energy budgets for neural computation in the neocortex and cerebellum
* **Authors**: Howarth, C., Gleeson, P., Attwell, D.
* **Year**: 2012
* **DOI**: `10.1038/jcbfm.2012.35`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC3390818/
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Direct revision of [Attwell2001]'s energy-budget anchor. Replaces "47%
  signalling ATP for APs" (2001) with "17% cortex / 21% cerebellum" (2012). t0124's
  `compare_literature.md` should anchor to the updated figure; the 2001 anchor is historical.

### [Wang2025-RGC-ATP]

* **Title**: Energetic diversity in retinal ganglion cells is modulated by neuronal activity and
  correlates with resilience to degeneration
* **Authors**: Wang, Z., Zhao, C., Xu, S., McCracken, S., Apte, R. S., Williams, P. R.
* **Year**: 2025
* **DOI**: `10.21203/rs.3.rs-5989609/v1`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11952644/
* **Suggested categories**: `retinal-ganglion-cell`, `patch-clamp`
* **Why download**: Only published in-vivo measurement of baseline ATP pool in ooDSGCs (highest of
  the three measured RGC families). Anchors the t0124 implied per-cell ATP turnover against in-vivo
  cellular ATP heterogeneity. **Preprint -- peer-review pending** (note required in citation).

### [Jedlicka2022-Pareto]

* **Title**: Pareto optimality, economy-effectiveness trade-offs and ion channel degeneracy:
  improving population modelling for single neurons
* **Authors**: Jedlicka, P., Bird, A. D., Cuntz, H.
* **Year**: 2022
* **DOI**: `10.1098/rsob.220073`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC9277232/
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Methodological synthesis of Pareto-optimality applied to function-vs-energy
  trade-offs in conductance-based compartmental neuron models. Connects ion channel degeneracy to
  Pareto-front structure -- directly relevant to t0124's parameter-distribution analysis.

## Recommendations for This Task

1. **Use the corrected Carter-Bean 2009 DOI** (`10.1016/j.neuron.2009.12.011`, NOT
   `10.1016/j.neuron.2009.07.013`) in `plan/plan.md` and `compare_literature.md`
   [CarterBean2009-PMC, CarterBean2009-PubMed]. The task brief had a typo that propagated into
   `research_papers.md`. The smoke-gate's "~4 mM-mol/cm" target should be re-derived in
   `plan/plan.md` per S-0123-04 using the cross-cell alpha table in [Sengupta2010, Table 1] and the
   [Hallermann2012-StateLocation] subcellular breakdown.

2. **Replace the [Attwell2001] 47%-signalling-budget anchor with the [Howarth2012-UpdatedBudget] 17%
   cortical / 21% cerebellar figure** in `compare_literature.md`. This **updates** the
   `research_papers.md` recommendation that anchored on the 2001 47% figure -- the 2012 update is
   the current canonical anchor. The 2001 figure should still be cited as the historical reference
   but the quantitative test should use the 2012 number.

3. **Use Remme et al. 2018 as the conceptual blueprint for the Pareto-front analysis layer**
   [Remme2018-PMC], but **do not switch algorithms** -- t0124's NSGA-II via pymoo is the project-
   standing choice. Cite Remme as the methodological precedent for function-vs-energy Pareto
   reporting in single-neuron compartmental MOBO.

4. **Add per-compartment ATP per-area AND total-per-AP reporting** in t0124 results, per the
   [Hallermann2012-StateLocation] AIS-vs-dendrite decomposition prediction. The expectation is that
   AIS segments have higher per-area cost but dendrites dominate total cost; t0124 results should
   confirm or refute this for the DSGC.

5. **Test the Hallermann-extended hypothesis**: AIS alpha factor (1.5 - 2.0) > dendritic alpha
   factor (1.0 - 1.3) on the Pareto-front top-N cells [Hallermann2012-StateLocation].

6. **Test the Wang-anchor hypothesis**: t0124 top-N cells' implied per-cell signalling ATP rate
   should sit at a level consistent with the ooDSGCs > alpha-RGCs ranking in baseline ATP pool
   [Wang2025-RGC-ATP], when scaled by total cellular ATP turnover.

7. **Skip downloading Sivyer 2013** -- the paper is already present in the corpus at
   `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/` with full
   PDF. The `research_papers.md` "paywalled" annotation is stale from t0080.

8. **Kole 2008 PDF download is partially resolved** -- the canonical AIS Nav density (0.25 S/cm^2)
   is now known from internet sources. Downloading the full PDF for archival completeness is
   recommended but not blocking; cite the value as `~0.25 S/cm^2` from
   [Kole2008-Nature, Kole2008-ModelDB].

9. **Acknowledge two Unresolved gaps** in `compare_literature.md`: (a) no DSGC-specific patch-clamp
   AIS Nav density measurement -- relies on alpha-RGC analogue [Werginz2024-context]; (b) no
   published DSGC DSI-vs-ATP Pareto front -- t0124 is the first.

## Source Index

### [CarterBean2009-PMC]

* **Type**: paper
* **Title**: Sodium entry during action potentials of mammalian central neurons: incomplete
  inactivation and reduced metabolic efficiency in fast-spiking neurons
* **Authors**: Carter, B. C., Bean, B. P.
* **Year**: 2009
* **DOI**: `10.1016/j.neuron.2009.12.011`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC2810867/
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: AIS smoke-gate calibration anchor (~25% excess Na+ for cortical pyramidal alpha
  ~1.25, ~2x for fast-spiking GABAergic alpha ~2.0). Quoted by [Sengupta2010] discussion p. 9.

### [CarterBean2009-PubMed]

* **Type**: documentation
* **Title**: PubMed record for Carter & Bean 2009 (PMID 20064395)
* **Author/Org**: NCBI / NLM
* **URL**: https://pubmed.ncbi.nlm.nih.gov/20064395/
* **Date**: 2009
* **Peer-reviewed**: no (database record, not peer-reviewed itself)
* **Relevance**: Authoritative source for the corrected Carter & Bean 2009 DOI
  (`10.1016/j.neuron.2009.12.011`, NOT `10.1016/j.neuron.2009.07.013`).

### [Remme2018-PMC]

* **Type**: paper
* **Title**: Function and energy consumption constrain neuronal biophysics in a canonical
  computation: Coincidence detection
* **Authors**: Remme, M. W. H., Rinzel, J., Schreiber, S.
* **Year**: 2018
* **DOI**: `10.1371/journal.pcbi.1006612`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC6312336/
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Methodological template for single-neuron function-vs-energy Pareto MOBO. ATP-
  counting energy objective (6.2 x 10^9 ATPs/s default). Uses Pareto-sampling, not NSGA-II.
  Conceptual blueprint cited by the task brief.

### [Remme2018-ModelDB]

* **Type**: repository
* **Title**: Function and energy constrain neuronal biophysics in coincidence detection (Remme et al
  2018\)
* **Author/Org**: Remme et al. / ModelDB
* **URL**: https://modeldb.science/245424
* **Date**: 2018
* **Last updated**: 2018
* **Peer-reviewed**: no (companion code, peer-reviewed paper is [Remme2018-PMC])
* **Relevance**: Companion NEURON model for [Remme2018-PMC]. Available if t0124 needs to replicate
  the MSO Pareto front using the original convention.

### [Hallermann2012-StateLocation]

* **Type**: paper
* **Title**: State and location dependence of action potential metabolic cost in cortical pyramidal
  neurons
* **Authors**: Hallermann, S., de Kock, C. P. J., Stuart, G. J., Kole, M. H. P.
* **Year**: 2012
* **DOI**: `10.1038/nn.3132`
* **URL**: https://www.nature.com/articles/nn.3132
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Per-compartment ATP cost decomposition in cortical pyramidal neurons. AIS has
  highest per-area cost but dendrites dominate total cost. Resting-potential-dependent overlap
  modulation. Directly testable against t0124's compartment-resolved ATP recipe.

### [Howarth2012-UpdatedBudget]

* **Type**: paper
* **Title**: Updated energy budgets for neural computation in the neocortex and cerebellum
* **Authors**: Howarth, C., Gleeson, P., Attwell, D.
* **Year**: 2012
* **DOI**: `10.1038/jcbfm.2012.35`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC3390818/
* **Peer-reviewed**: yes (Journal of Cerebral Blood Flow & Metabolism)
* **Relevance**: Direct revision of [Attwell2001]. AP fraction of signalling ATP revised from 36%
  (2001) to 17% cortex / 21% cerebellum (2012). Updated anchor for t0124's `compare_literature.md`.

### [Wang2025-RGC-ATP]

* **Type**: paper
* **Title**: Energetic diversity in retinal ganglion cells is modulated by neuronal activity and
  correlates with resilience to degeneration
* **Authors**: Wang, Z., Zhao, C., Xu, S., McCracken, S., Apte, R. S., Williams, P. R.
* **Year**: 2025
* **DOI**: `10.21203/rs.3.rs-5989609/v1`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11952644/
* **Peer-reviewed**: no (Research Square preprint -- peer-review pending)
* **Relevance**: First in-vivo measurement of baseline ATP pool across RGC types using ATeam FRET
  biosensor. ooDSGCs highest, ipRGCs intermediate, alpha-RGCs lowest. Provides the per-cell ATP pool
  anchor for t0124's implied per-cell signalling rate.

### [Zhang2025-PredictiveCoding]

* **Type**: paper
* **Title**: Energy optimization induces predictive-coding properties in a multi-compartment spiking
  neural network model
* **Authors**: Zhang, M., Chitic, R., Bohte, S. M.
* **Year**: 2025
* **DOI**: `10.1371/journal.pcbi.1013112`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12180623/
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Contemporary (2025) example of energy-objective training in multi-compartment
  spiking neurons. Uses weighted scalarisation, not Pareto / NSGA-II. Energy proxy is apical-soma
  voltage mismatch, not ATP. Cited in compare-literature as a contrast: different algorithm class,
  different energy proxy.

### [Jedlicka2022-Pareto]

* **Type**: paper
* **Title**: Pareto optimality, economy-effectiveness trade-offs and ion channel degeneracy:
  improving population modelling for single neurons
* **Authors**: Jedlicka, P., Bird, A. D., Cuntz, H.
* **Year**: 2022
* **DOI**: `10.1098/rsob.220073`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC9277232/
* **Peer-reviewed**: yes (Open Biology)
* **Relevance**: Methodological synthesis of Pareto-optimality for conductance-based compartmental
  models. Cites [Attwell2001] and [Remme2018-PMC]. Argues for reporting parameter populations on the
  Pareto front given ion channel degeneracy. Best-practice reference for t0124's
  parameter-distribution analysis.

### [Kole2008-Nature]

* **Type**: paper
* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P., Ilschner, S. U., Kampa, B. M., Williams, S. R., Ruben, P. C., Stuart,
  G. J.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **URL**: https://www.nature.com/articles/nn2040
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Canonical AIS Nav density measurement (~2500 pS/um^2 ~ 0.25 S/cm^2 in cortical
  pyramidal neurons, ~50x proximal dendritic). Project corpus has metadata-only entry; full PDF
  download partially resolves the gap.

### [Kole2008-ModelDB]

* **Type**: repository
* **Title**: Na+ channel dependence of AP initiation in cortical pyramidal neuron (Kole et al. 2008)
* **Author/Org**: Kole et al. / ModelDB
* **URL**: https://modeldb.science/114394
* **Date**: 2008
* **Last updated**: 2008
* **Peer-reviewed**: no (companion code; peer-reviewed paper is [Kole2008-Nature])
* **Relevance**: Companion NEURON model with AIS Nav density implementation. Available for
  cross-checking the canonical 0.25 S/cm^2 figure against project-prior assumptions.

### [Werginz2024-context]

* **Type**: documentation
* **Title**: Internet-search-confirmed context for [Werginz2024] alpha-RGC AIS Nav density (1300
  mS/cm^2 AIS vs 75 mS/cm^2 soma)
* **Author/Org**: project context (already in corpus at
  `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/`)
* **URL**: https://doi.org/10.1523/JNEUROSCI.1592-24.2024
* **Date**: 2024
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Closest published alpha-RGC AIS Nav density measurement; cross-reference for the
  Bed B smoke-gate when no DSGC-specific value exists. Not a new discovery -- catalogued for
  cross-reference completeness in the source index.

### [Sivyer2013-corpus]

* **Type**: documentation
* **Title**: Internal-corpus note: [Sivyer2013] is already catalogued at
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/`
* **Author/Org**: project context
* **URL**: https://www.nature.com/articles/nn.3565
* **Date**: 2013
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Confirmation that the Sivyer 2013 "paywalled" gap from `research_papers.md` is a
  stale t0080-era annotation; the paper is in the corpus with full PDF. No re-download needed.

### [Sengupta2010-context]

* **Type**: documentation
* **Title**: Internal-corpus reference: [Sengupta2010] (already at
  `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/`) Table 1 cross-cell Na+
  load table
* **Author/Org**: project context
* **URL**: https://doi.org/10.1371/journal.pcbi.1000840
* **Date**: 2010
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Internet research confirmed that the [Sengupta2010] cross-cell alpha table remains
  the canonical reference for cell-type-specific overlap factors. No 2024+ paper supersedes it. The
  smoke-gate "~4 mM-mol/cm" target is derived from this table via the [CarterBean2009-PMC] alpha ~
  1.25 cortical pyramidal value.

### [Sengupta2010]

* **Type**: paper
* **Title**: Action Potential Energy Efficiency Varies Among Neuron Types in Vertebrates and
  Invertebrates
* **Authors**: Sengupta, B., Stemmler, M., Laughlin, S. B., Niven, J. E.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000840`
* **URL**: https://doi.org/10.1371/journal.pcbi.1000840
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Project-canonical ATP-per-spike recipe paper, already in corpus at
  `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/`. Cross-cell alpha table
  (Table 1) provides the cell-type calibration anchors cited by t0124's smoke-gate.

### [Attwell2001]

* **Type**: paper
* **Title**: An Energy Budget for Signaling in the Grey Matter of the Brain
* **Authors**: Attwell, D., Laughlin, S. B.
* **Year**: 2001
* **DOI**: `10.1097/00004647-200110000-00001`
* **URL**: https://doi.org/10.1097/00004647-200110000-00001
* **Peer-reviewed**: yes (Journal of Cerebral Blood Flow & Metabolism)
* **Relevance**: 2001 canonical 47%-signalling-ATP anchor referenced throughout t0124. Already in
  corpus at `tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/`. Superseded
  for quantitative anchoring by [Howarth2012-UpdatedBudget].

### [Hay2011]

* **Type**: paper
* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://doi.org/10.1371/journal.pcbi.1002107
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Ensemble-as-experiment NSGA-II reporting precedent (1000 x 500 = 500 000 evals on
  22-parameter L5 pyramidal cell). Already in corpus at
  `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`. Cited
  throughout for Pareto-front parameter-distribution reporting.

### [Mohacsi2024]

* **Type**: paper
* **Title**: Evaluation and comparison of methods for neuronal parameter optimization using the
  Neuroptimus software framework
* **Authors**: Mohacsi, M., Torok, M. P., Saray, S., Tar, L., Farkas, G., Kali, S.
* **Year**: 2024
* **DOI**: `10.1371/journal.pcbi.1012039`
* **URL**: https://doi.org/10.1371/journal.pcbi.1012039
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Modern controlled benchmark of 22 algorithm variants on 3-12-parameter neuron
  modelling. Already in corpus at
  `tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/`. Cited as the closest
  analogue benchmark for t0124's NSGA-II convergence expectations.

### [Sivyer2013]

* **Type**: paper
* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **URL**: https://doi.org/10.1038/nn.3565
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Dendritic-spike-vs-soma DSGC paper. Already in corpus at
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/` with full PDF
  -- the `research_papers.md` "paywalled" flag is a stale t0080-era annotation. See
  [Sivyer2013-corpus] for the in-corpus location.

### [Trenholm2013]

* **Type**: paper
* **Title**: Intrinsic and synaptic mechanisms shaping the OFF response of mouse direction-
  selective ganglion cells
* **Authors**: Trenholm, S., McLaughlin, A. J., Schwab, D. J., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`
* **URL**: https://doi.org/10.1523/JNEUROSCI.0808-13.2013
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Mouse Hb9-DSGC ratio-DSI convention and 198 Hz peak PD-rate anchor. Already in
  corpus at `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/`.
  Provides the Gaussian-convolution rate convention (sigma = 25 ms) for t0124's PD-rate diagnostic.

### [Werginz2024]

* **Type**: paper
* **Title**: Cell-type-specific axon initial segment sodium channel properties in mouse alpha
  retinal ganglion cells
* **Authors**: Werginz, P. et al.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`
* **URL**: https://doi.org/10.1523/JNEUROSCI.1592-24.2024
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Closest published alpha-RGC AIS Nav density measurement (1300 mS/cm^2 AIS vs 75
  mS/cm^2 soma; ratio ~17.3x). Already in corpus at
  `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/`.
  Cross-reference for t0124's smoke-gate AIS calibration when no DSGC-specific value exists.
