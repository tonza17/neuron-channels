---
spec_version: "2"
task_id: "t0027_literature_survey_morphology_ds_modeling"
---
# Results: Literature Survey on Morphology Effects in Direction-Selectivity Modeling

## Summary

This task extended the project's morphology-and-direction-selectivity (DS) modeling corpus from 5
baseline papers to 20 total, adding **15 new paper assets** that collectively cover retinal
starburst amacrine cells (SACs), retinal direction-selective ganglion cells (DSGCs), fly vertical
system (VS) cells, fly T4 ON-motion neurons, primate SACs, cat V1 cortical neurons, and cable-theory
tools. The synthesis answer asset `morphology-direction-selectivity-modeling-synthesis` integrates
all 20 papers and maps each morphology variable to the mechanism(s) by which it shapes DS. Two PDFs
(Kim2014, Sivyer2013) were paywalled and are summarised from open abstracts with intervention files
filed.

## Methodology

* **Machine**: local Windows 11 workstation, no remote compute, no paid API.
* **Runtime**: research + implementation spanned 2026-04-21; per-paper work from discovery to
  summary averaged ~30 minutes.
* **Start timestamp**: 2026-04-21T18:33:02Z (per `task.json`).
* **End timestamp**: 2026-04-21 (results stage).
* **Methods**: structured web searches (Google Scholar, PubMed, bioRxiv) keyed on DS morphology
  terms; citation-graph expansion from the 5 baseline papers; paper-asset builder reused from t0018;
  manual reading of each PDF followed by nine-section `summary.md` authoring; paywalled PDFs handled
  via `intervention/` + abstract-only summary per paper-asset spec v3.

## Coverage Table

One row per included paper (baseline + new), listing the morphology variable manipulated, the DS
outcome measured, the model type, the organism, and the cell type. Rows are single-line by
specification; see each paper's `summary.md` for full detail.

| paper_id | citation_key | year | organism | cell type | morphology variable manipulated | DS outcome measured | model type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `10.1371_journal.pcbi.1000899` | Schachter2010 | 2010 | rabbit | ON-OFF DSGC | distal dendritic input resistance; Na/Ca channel spatial density | dendritic-spike-gated spike DSI | NeuronC compartmental |
| `10.7554_eLife.52949` | Jain2020 | 2020 | mouse | ON-OFF DSGC | dendritic subunit scale (<10 um); E/I co-location | local Ca2+ DSI per dendritic segment | NEURON compartmental + 2P Ca2+ imaging |
| `10.1016_j.cub.2018.03.001` | Morrie2018 | 2018 | mouse (Sema6A-/-) | SAC + DSGC | SAC plexus density; arbor symmetry | DSGC null-direction inhibition; vector-sum DSI | TREES-toolbox IPSC simulation + patch |
| `10.1038_s41467-026-70288-4` | PolegPolsky2026 | 2026 | generic mammalian | DSGC (352-segment) | bipolar input location; distance-graded delay; NMDA gating | DSI across ML-searched parameter space | NEURON + ML parameter search |
| `10.1016_j.celrep.2025.116833` | deRosenroll2026 | 2026 | mouse | SAC + DSGC | GABA/ACh spatial offset on SAC; E/I subunit layout | local vs global DSI per DSGC subunit | NEURON SAC-DSGC network |
| `10.1017_S0952523804214109` | Tukker2004 | 2004 | rabbit | SAC | dendritic length; electrotonic length; input density distribution | centrifugal calcium DSI at dendritic tips | compartmental (NeuronC) |
| `10.1371_journal.pbio.0050185` | Hausselt2007 | 2007 | mouse | SAC | Ca2+ channel distribution along dendrite; soma-to-tip voltage gradient | dendritic Ca2+ DSI | compartmental + whole-cell + 2P |
| `10.1016_j.neuron.2016.02.020` | Vlasits2016 | 2016 | mouse | SAC | proximal-restricted vs uniform excitatory input layout | distal-varicosity Ca2+ DSI | morphology-matched compartmental |
| `10.1038_nature13240` | Kim2014 | 2014 | mouse | SAC (EyeWire-reconstructed) + BCs | BC2 vs BC3a contact location on SAC dendrites | space-time receptive-field orientation; centrifugal DS | EM connectomics + cable simulation |
| `10.1038_nn.3565` | Sivyer2013 | 2013 | rabbit | ON-OFF DSGC | distal branch dendritic-spike threshold; branch independence | branch-local dendritic-spike DSI; somatic spike DSI | multi-site patch + simulation |
| `10.7554_eLife.81533` | Srivastava2022 | 2022 | mouse | SAC | proximal-distal input kinetics (sustained vs transient) | dendritic centrifugal DSI; velocity dependence | NEURON ball-and-stick + iGluSnFR imaging |
| `10.1371_journal.pcbi.1000877` | Cuntz2010 | 2010 | generic (multi-species) | multiple cell types | branching balancing factor (bf); synthetic vs reconstructed trees | electrotonic compartmentalization (no direct DSI) | TREES-toolbox synthetic morphology |
| `10.1523_JNEUROSCI.17-16-06023.1997` | Single1997 | 1997 | Drosophila/blowfly | lobula plate VS cell | dendritic cable; opponent E/I on passive dendrite | postsynaptic DS membrane potential and gain control | passive compartmental + pharmacology |
| `10.1038_s41467-024-46234-7` | Aldor2024 | 2024 | mouse | SAC | dendritic mGluR2 vs perisomatic Kv3 spatial segregation | dendritic Ca2+ DSI; DSGC DSI downstream | 2P voltage/Ca2+ imaging + compartmental |
| `10.1523_JNEUROSCI.4013-15.2016` | PolegPolsky2016 | 2016 | mouse | DSGC (121-compartment) | BC subtype heterogeneity; E/I contrast tuning on dendrite | suprathreshold spike DSI across contrast | stochastic compartmental |
| `10.1038_s41593-017-0046-4` | Gruntman2018 | 2018 | Drosophila | T4 neuron | full 344-section vs collapsed-to-base vs single-compartment dendrite | DSI vs speed tuning | FIB-SEM + passive conductance-based |
| `10.1371_journal.pcbi.1009754` | EzraTsur2021 | 2021 | mouse | SAC + DSGC | 8D input-layout parameter space (sustained-proximal / transient-distal) | centrifugal preference fraction; DSGC DSI | 1013-compartment NEURON + GA search |
| `10.1038_12194` | Anderson1999 | 1999 | cat | V1 Meynert / pyramidal | dendritic asymmetry of reconstructed cortical trees | directional-tuning index vs speed | detailed NEURON compartmental |
| `10.1017_S0952523823000019` | Wu2023 | 2023 | macaque (primate) | SAC | medial and distal dendritic diameter; morphological vs space-time mechanism | centrifugal Ca2+ DSI at dendritic tips | connectomics-informed compartmental |
| `10.1038_s41598-018-23998-9` | Dan2018 | 2018 | blowfly | VS cell | transfer-resistance (TR) weighting across 3D-reconstructed branchlets | axonal receptive-field DS; difference index | 3D passive cable + compartmental |

## Morphology Variable Taxonomy

Findings grouped by which morphology variable each paper manipulates.

### Dendritic length / electrotonic length

Papers that sweep overall dendrite length or the passive length constant: **Tukker2004**,
**Hausselt2007**, **Jain2020**.

* Tukker2004 sweeps SAC electrotonic length; DS peaks at intermediate **lambda ~400 um** comparable
  to the dendritic spread.
* Hausselt2007 swept SAC dendritic length from 50 to 200 um; DSI dropped monotonically from **~0.35
  at natural 150 um** to **~0.12 at 50 um** because shorter cables lose the soma-to-tip voltage
  gradient.
* Jain2020 reports an exponential decay of pairwise noise correlations along DSGC dendrites with a
  cable space constant of **5.3 um**, setting a spatial scale for independent DS subunits.

### Branch count, branch order, and branching pattern

Papers that manipulate branching: **Tukker2004**, **Hausselt2007**, **Cuntz2010**.

* Tukker2004 found SAC DSI nearly invariant to the distance of the first branch point but increased
  **up to 2-fold** when branches and synapse density were concentrated in the outer 20% of the tree.
* Hausselt2007 showed that placing Ca2+ conductance on higher-order (distal) branches raises DSI by
  **about +0.1** over uniform distribution.
* Cuntz2010 formalised the link: a single scalar balancing factor `bf` maps monotonically onto
  electrotonic compartmentalisation, so low-bf trees have many electrotonically isolated subtrees.

### Dendritic diameter

Papers that sweep segment diameter: **Wu2023**.

* Wu2023 performed the most explicit dendritic-diameter sweep to date: medial dendritic diameter
  around **0.2-0.25 um** maximises primate SAC DSI (matching measured 0.15-0.2 um), while distal
  diameter saturates DSI once it exceeds **~0.8 um**.
* No other paper in the corpus systematically sweeps diameter; this is both a finding and a gap.

### Asymmetric vs symmetric arbors; plexus density; tiling

Papers that compare symmetric to asymmetric arbors or that manipulate plexus density:
**Morrie2018**, **Sivyer2013**, **Anderson1999**, **Ezra-Tsur2021**.

* Morrie2018: in Sema6A-/- mice with halved SAC plexus density, DSGC ON-direction vector-sum
  magnitude collapses from **0.40 to 0.10**, and **30-40% of SAC varicosities** lose centrifugal
  tuning and instead follow the local distal-dendrite orientation.
* Sivyer2013 (abstract + summary) shows DSGC terminal dendrites behave as near-independent DS
  subunits driven by asymmetric SAC inhibition.
* Anderson1999 (cortical counterpoint) found no correlation between small biases in cortical
  dendritic morphology and direction preference across reconstructed V1 neurons.
* Ezra-Tsur2021 integrates connectomic asymmetry of SAC arbors in a 1013-compartment model.

### Input-on-dendrite spatial layout

Papers that vary where on the dendrite synaptic inputs land: **Vlasits2016**, **Kim2014**,
**Srivastava2022**, **Ezra-Tsur2021**, **PolegPolsky2016**, **PolegPolsky2026**.

* Vlasits2016: restricting excitation to the proximal two-thirds of the SAC dendrite raises
  distal-varicosity DSI to **0.34 +/- 0.23** versus **0.11 +/- 0.18** with uniform input placement.
* Kim2014: EyeWire reconstructions show BC2 contacts proximal SAC dendrites, BC3a contacts distal,
  with a **50-100 ms** temporal lag yielding a space-time-tilted receptive field.
* Srivastava2022: swapping proximal-distal input kinetics in a ball-and-stick SAC reverses the
  preferred direction; homogenising kinetics strongly reduces DSi.
* Ezra-Tsur2021 genetic-algorithm sweep over an 8D input-layout space finds **only the combined
  sustained-proximal + transient-distal arrangement** reproduces centrifugal preference.
* PolegPolsky2026: ML search across bipolar-input locations discovers multiple DS primitives.

### Input kinetic tiling

Papers that vary input time courses across the arbor: **Srivastava2022**, **Ezra-Tsur2021**,
**Wu2023**, **Kim2014**.

* Srivastava2022 deconvolves iGluSnFR responses and estimates the steady-state release rate at
  proximal sites to be **~3x larger** than at distal sites.
* Wu2023: the space-time mechanism dominates for large stimuli at low velocities; the morphological
  mechanism dominates for small stimuli at high velocities.

### Transfer-resistance weighting (branchlet decoupling)

Papers that measure or simulate local-to-axonal transfer resistance: **Dan2018**, **Single1997**.

* Dan2018 formalises TR weighting for fly VS cells; branchlets are electrotonically decoupled and
  TR-weighted summation reduces the direction-difference index from **0.411 (uniform)** to **0.293
  (TR-weighted)**, exceeding 2 SD of the shuffled-weight null.
* Single1997 showed that DS in the same fly VS cell is not inherited but generated postsynaptically
  by opponent excitation and shunting inhibition on the passive dendrite.

### Collapse-to-point-compartment controls

Papers that use collapse-to-base or single-compartment tests as a geometry null: **Gruntman2018**.

* Gruntman2018 collapses all 154 T4 synapses onto the dendritic base or replaces the cell with a
  single compartment; both reproduce the full 344-section DSI-vs-speed curve. The T4 arbor's role
  reduces to 1D input layout, not cable geometry.

## Mechanism Taxonomy

Findings grouped by the causal mechanism each paper invokes. A mechanism is listed with the
morphology variable(s) it is sensitive to.

### Electrotonic compartmentalisation (passive cable, transfer resistance)

Sensitive to dendritic length, diameter, branching pattern. **Papers**: Schachter2010, Tukker2004,
Dan2018, Cuntz2010, Jain2020, Wu2023, Single1997.

* Schachter2010 shows local input resistance scales from **150-200 MOhm proximally to > 1 GOhm
  distally**, creating electrotonically separable regions.
* Dan2018 formalises TR weighting; Cuntz2010 provides the scalar `bf` that predicts how
  compartmented a tree is.
* Jain2020 empirically measures the DSGC-side compartment scale at **5.3 um**.

### Dendritic spike thresholding (active Na/Ca conductances)

Sensitive to dendritic diameter, distal input resistance, channel spatial layout. **Papers**:
Schachter2010, Sivyer2013, Hausselt2007.

* Schachter2010: **~1 nS** suffices distally while **3-4 nS** is needed proximally to trigger
  spikes, yielding a **~4x amplification of DSI**.
* Sivyer2013: dual-patch evidence that DSGC terminal dendrites initiate fast spikes locally;
  passive-only (gNa = gCa = 0) models fail to reproduce observed DS gain.
* Hausselt2007: high-voltage-activated Ca2+ channels on distal SAC branches amplify the soma-to-tip
  voltage gradient.

### NMDA-mediated multiplicative gating in dendritic context

Sensitive to input location and spatial distribution across the arbor. **Papers**: PolegPolsky2026.

* PolegPolsky2026 shows NMDA multiplicative gating can **independently drive DSI > 0.5** in a
  352-segment DSGC when input locations and biophysics are appropriately tuned.

### Delay lines (cable-mediated propagation delay)

Sensitive to dendritic length and the soma-to-tip distance of each input. **Papers**: Tukker2004,
PolegPolsky2026, Kim2014.

* Tukker2004: the preferred-direction coincidence of local and global EPSP signals depends on cable
  propagation delay along the dendrite.
* PolegPolsky2026: distance-graded passive delay lines are one of several ML-discovered DS
  primitives.

### Coincidence detection at branch points or tips

Sensitive to branch-independence and branch-order. **Papers**: Schachter2010, Aldor2024,
PolegPolsky2026.

* Aldor2024: perisomatic Kv3 + dendritic mGluR2 partition the SAC into compartments so that local
  synaptic input + global motion signal coincide to drive supra-threshold Ca2+ only in the
  centrifugal direction.

### Asymmetric SAC inhibition driven by presynaptic geometry

Sensitive to SAC arbor symmetry, plexus density, SAC-DSGC wiring. **Papers**: Morrie2018,
Ezra-Tsur2021, PolegPolsky2016, deRosenroll2026, Jain2020.

* Morrie2018 is the paradigm case: halving plexus density collapses DSGC DSI.
* deRosenroll2026 shows the GABA/ACh spatial offset on the SAC is essential for local (subunit) DSI.
* PolegPolsky2016 shows E/I contrast tuning needs to be matched across the dendrite.

### Kinetic tiling of bipolar input (sustained-proximal, transient-distal)

Sensitive to where each input type sits on the dendrite. **Papers**: Srivastava2022, Kim2014,
Ezra-Tsur2021, Wu2023.

* Srivastava2022 directly measures the sustained-proximal vs transient-distal kinetic gradient.
* Kim2014 and Wu2023 tie it to specific bipolar-cell types contacting specific arbor zones.

## Gaps and Contradictions

### Under-explored morphology variables

* **Branch order**. Only Tukker2004, Hausselt2007, and Cuntz2010 touch branch order; none perform a
  systematic branch-order sweep on a reconstructed DSGC.
* **Dendritic diameter**. Only Wu2023 systematically sweeps diameter; on DSGCs the variable is
  effectively untouched. Given t0026's diameter uncertainty, this is a critical gap for our
  testbeds.
* **Soma size and soma-dendrite impedance mismatch**. No corpus paper sweeps soma radius; the
  somatic sink is a silent knob.
* **Branch angle at fixed length**. Cuntz2010 parameterises branching with a single scalar; no paper
  varies branch angle.
* **Spine density on DSGC dendrites**. No paper sweeps spines; Sivyer2013 and Schachter2010 treat
  terminals as smooth cables.
* **Non-retinal cortical morphology**. Only Anderson1999 addresses cortical DS morphology, and it
  rejects dendritic asymmetry as sufficient. No subsequent modelling has tested kinetic tiling on
  cortical morphology.

### Contradictions between papers

* **Dendritic spike DS**: Sivyer2013 argues distal Na/Ca-mediated dendritic spikes are necessary for
  DSGC DS (passive-only models fail). More passive-leaning views (e.g., Gruntman2018's T4 collapse
  control and the Dan2018 TR-weighted passive VS model) successfully reproduce DS without active
  dendritic conductances. The reconciliation likely is cell-type-specific: DSGCs need active
  conductances, fly VS and T4 cells may not.
* **Dominant compartmentalisation scale**: Schachter2010 places compartmentalisation at the
  whole-branch scale (local input resistance > 1 GOhm distally). Jain2020 places it at sub-10-um
  segments (cable space constant 5.3 um). Both are on ON-OFF DSGCs but with different experimental
  preparations and simulators.
* **Dendritic asymmetry as DS substrate**: Retinal SAC literature (Tukker2004, Morrie2018,
  Ezra-Tsur2021) treats asymmetric arbors and plexus density as causal; Anderson1999 explicitly
  rejects dendritic asymmetry as sufficient for cortical V1 DS.

### Replicable findings across labs and model frameworks

* **Asymmetric SAC inhibition of DSGCs drives DSGC DS**. Supported by Morrie2018, Ezra-Tsur2021,
  PolegPolsky2016, deRosenroll2026, and Jain2020 across mouse and rabbit, across TREES-toolbox,
  NEURON, and patch-clamp approaches. This is the most replicable finding in the corpus.
* **Electrotonic compartmentalisation converts distributed asymmetry into DS**. Supported by
  Schachter2010, Tukker2004, Dan2018, and Cuntz2010 across retinal DSGCs, SACs, and fly VS cells.
* **Proximal-restricted / sustained-proximal inputs are required for SAC centrifugal preference**.
  Supported by Vlasits2016, Srivastava2022, Ezra-Tsur2021, and Wu2023.

## Recommendations

Concrete morphology-sweep experiments worth running on our t0022 (deterministic ModelDB 189347 port)
and t0024 (de Rosenroll 2026 AR(2)-correlated stochastic port) testbeds, prioritised by expected
information gain and by whether the result discriminates between two competing mechanisms.
Recommendations are adapted from the falsifiable predictions in `creative_thinking.md`.

### Recommendation 1: Distal dendrite scaling (1.5x) on t0022 — discriminates passive TR weighting vs dendritic-spike branch independence

* **Vary**: multiply distal dendrite length by **1.5x** while preserving diameter and branching
  topology, then 2x, then 0.75x for a three-point sweep.
* **Measure**: somatic spike DSI; local dendritic-spike count per branch; peak firing rate.
* **Discriminates**: if passive TR weighting (Dan2018) dominates, DSI should drop > 30%; if
  dendritic-spike branch independence (Sivyer2013, Schachter2010) dominates, DSI should stay within
  10%.
* **Priority**: HIGH. This is the single experiment most likely to tell us whether our t0022 and
  t0024 DSI gap is geometry-driven or channel-driven.

### Recommendation 2: Distal branch thickening (halve distal input resistance) on t0022 — separates active amplification from passive filtering

* **Vary**: increase distal diameter to halve distal local input resistance; four-point sweep (1.0x,
  1.5x, 2.0x, 2.5x diameter).
* **Measure**: subthreshold DSI (PSP amplitude); suprathreshold DSI (spike rate); dendritic-spike
  threshold per branch.
* **Discriminates**: Schachter2010's gradient of dendritic-spike thresholds should collapse if
  distal input resistance drops. If subthreshold DSI is preserved but suprathreshold DSI collapses,
  active amplification is load-bearing; if both collapse, passive filtering is load-bearing.
* **Priority**: HIGH. Addresses the literature gap on diameter (only Wu2023 on primate SACs).

### Recommendation 3: Swap sustained vs transient BC input kinetics on t0024 — Srivastava2022 vs Kim2014 decomposition

* **Vary**: exchange proximal and distal bipolar-cell input kinetics (swap tau_rise / tau_decay
  between proximal and distal input populations). Include a third condition with homogenised
  kinetics (both locations get the mean kinetics).
* **Measure**: subunit DSI per dendrite; preferred-direction vector.
* **Discriminates**: if kinetic tiling (Srivastava2022, Ezra-Tsur2021) is causal, swapping should
  reverse the preferred direction; if cable delay (Kim2014) is causal, swapping should only reduce
  DSI magnitude.
* **Priority**: HIGH. t0024's upstream circuit already has this structure; the intervention is
  cheap.

### Recommendation 4: Random terminal-branch ablation on t0022 — branch independence vs global TR summation

* **Vary**: randomly ablate 10%, 25%, 50% of terminal branches; run N = 10 seeds per condition.
* **Measure**: global DSGC DSI; local subunit DSI on remaining branches.
* **Discriminates**: if branch independence (Sivyer2013, Jain2020) holds, 25% ablation should drop
  global DSI by < 15%; if global TR summation (Dan2018) dominates, 25% ablation should drop global
  DSI by > 40%.
* **Priority**: MEDIUM. Also addresses the literature gap on stochastic arbor perturbation noted in
  `creative_thinking.md`.

### Recommendation 5: Collapse t0024 to single compartment — T4-style geometry-null test

* **Vary**: collapse the DSGC morphology to (a) all-synapses-on-soma, (b) true one-compartment cell,
  (c) reduced 10-compartment cell. Preserve all synaptic kinetics and conductance totals.
* **Measure**: full DSI-vs-speed curve; peak firing rate; local DSI (loses meaning in single-comp;
  flag).
* **Discriminates**: if Gruntman2018-style geometry-nullity extends to DSGCs, the collapsed model
  should reproduce the full-model DSI-vs-speed curve within measurement noise; if the de Rosenroll
  local-DSI mechanism is load-bearing, the collapsed model should fail to reproduce DS dynamics
  above a critical speed.
* **Priority**: MEDIUM. Cheapest to run and provides a theoretical upper bound on how much
  morphology matters at all.

## Verification

* `verify_task_results.py` — target: 0 errors on the final pass.
* `verify_task_metrics.py` — target: 0 errors (empty `metrics.json` is valid).
* Paper-asset verificators (`verify_paper_assets.py`) were run per paper during Milestones 2-3 and
  are re-referenced here but not repeated; paywalled-paper warnings are expected and documented in
  `intervention/`.
* Answer-asset verificator (`verify_answer_assets.py`) was run in Phase 4 of the task and confirms
  all 20 paper_ids are cited.

## Limitations

* Coverage is not exhaustive. Only 15 new papers were added; the field includes additional cortical,
  fly lobula-plate, and zebrafish DS modeling work that was not reviewed.
* Non-English and gray-literature sources were not considered.
* Two key PDFs (Kim2014, Sivyer2013) were paywalled; summaries were built from open abstracts and
  citation-graph context rather than from the full text, so quantitative claims attributed to those
  two papers are limited to what the abstracts support.
* No in silico replication was performed. Quantitative claims in the Coverage Table and taxonomies
  are paraphrased from published summaries and have not been re-verified by re-running original
  models.
* DSI numbers reported across papers are not pooled — methods, metrics, and model assumptions vary
  between studies, so the taxonomy sections report representative rather than meta-analytic values.
* Dendritic diameter is systematically swept in only one paper (Wu2023) — both a finding and a
  survey limitation.
* The corpus is SAC-and-DSGC-heavy; cortical and invertebrate DS mechanisms are underrepresented.
  Roughly a quarter of the corpus comes from one senior-author cluster (Poleg-Polsky, Awatramani,
  Taylor), correlating methods and priors.

## Files Created

* `tasks/t0027_literature_survey_morphology_ds_modeling/results/results_summary.md`
* `tasks/t0027_literature_survey_morphology_ds_modeling/results/results_detailed.md` (this file)
* `tasks/t0027_literature_survey_morphology_ds_modeling/results/metrics.json`
* `tasks/t0027_literature_survey_morphology_ds_modeling/results/suggestions.json`
* `tasks/t0027_literature_survey_morphology_ds_modeling/results/costs.json`
* `tasks/t0027_literature_survey_morphology_ds_modeling/results/remote_machines_used.json`
* `tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/morphology-direction-selectivity-modeling-synthesis/`
  (synthesis answer asset)
* `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/<15 new paper folders>/` (15
  new paper assets)

## Task Requirement Coverage

The operative task request (from `task.json` `short_description` and the resolved
`task_description.md`):

> Survey computational/biophysical modeling papers on how dendritic morphology shapes direction
> selectivity in DSGCs, SACs, and other DS neurons. Add 12-20 new paper assets per paper-asset spec
> v3; write one synthesis answer asset; produce results files with Coverage Table,
> morphology-variable taxonomy, mechanism taxonomy, gaps and contradictions, and 3-5 prioritised
> morphology-sweep recommendations for t0022 / t0024.

Requirements below are tracked against the `REQ-*` IDs from `plan/plan.md`.

* **REQ-1** — Add 12-20 new paper assets per paper-asset spec v3. **Status: Done.** Added **15**
  new paper assets (target hit; midpoint of 12-20). Evidence:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/` contains 15 subfolders; each
  has `details.json` + `summary.md` + `files/` (or `.gitkeep` when download failed).

* **REQ-2** — Do not re-download the 5 baseline papers. **Status: Done.** The 5 baseline paper_ids
  (`10.1371_journal.pcbi.1000899`, `10.7554_eLife.52949`, `10.1016_j.cub.2018.03.001`,
  `10.1038_s41467-026-70288-4`, `10.1016_j.celrep.2025.116833`) do not appear in
  `tasks/t0027_.../assets/paper/`; they are cited by `paper_id` in the synthesis answer and in the
  Coverage Table above. Evidence: coverage-table rows 1-5 above.

* **REQ-3** — Mark each new paper with a subset of the project categories. **Status: Done.** Every
  new paper's `details.json` `categories` field includes at least one of `direction-selectivity`,
  `compartmental-modeling`, `dendritic-computation`, or `retinal-ganglion-cell`. Evidence: grep
  `categories` across the 15 new `details.json` files.

* **REQ-4** — Flag borderline cases (SAC, passive-cable, invertebrate, cortical). **Status:
  Done.** Flags are carried via the Coverage Table's organism and cell-type columns and are
  explicitly noted in each borderline `summary.md` Overview section (e.g., Single1997, Dan2018,
  Gruntman2018 flagged "Drosophila / blowfly"; Anderson1999 flagged "cat V1 cortical"; Cuntz2010
  flagged "cable-theory tool, no direct DSI").

* **REQ-5** — Write one synthesis answer asset citing every included paper. **Status: Done.** The
  answer asset at
  `tasks/t0027_.../assets/answer/morphology-direction-selectivity-modeling-synthesis/` cites all 20
  paper_ids (15 new + 5 baseline) in `details.json` `cited_paper_ids` and in the `full_answer.md`
  Sources list and inline references. Evidence: `full_answer.md` Sources section enumerates 20 Paper
  entries.

* **REQ-6** — Produce `results_detailed.md` with five required subsections (Coverage Table,
  Morphology Variable Taxonomy, Mechanism Taxonomy, Gaps and Contradictions, Recommendations).
  **Status: Done.** This file contains all five subsections in the required order with 20-row
  Coverage Table, 7-variable taxonomy, 7-mechanism taxonomy, explicit gaps and contradictions, and 5
  prioritised recommendations. Evidence: `results_detailed.md` sections above.

* **REQ-7** — Produce `results_summary.md` (2-3 paragraphs). **Status: Done.** See
  `tasks/t0027_.../results/results_summary.md` (this task); 2 paragraph executive summary with final
  paper count, consensus variable, disagreements, and first sweep. Evidence: `results_summary.md`.

* **REQ-8** — Flag PDF-retrieval blockers as intervention files. **Status: Done.** Two paywalled
  papers (Kim2014, Sivyer2013) triggered `intervention/Kim2014_paywalled.md` and
  `intervention/Sivyer2013_paywalled.md`; their `details.json` has `download_status: "failed"` with
  non-null `download_failure_reason`. deRosenroll2026 paywall was handled upstream in t0010.
  Evidence: two intervention files in `tasks/t0027_.../intervention/`.

* **REQ-9** — No remote compute, no paid API. **Status: Done.** `remote_machines_used.json` =
  `[]`; `costs.json` `total_cost_usd` = 0.0. Evidence: this file's `## Methodology` section and the
  two JSON files in `results/`.
