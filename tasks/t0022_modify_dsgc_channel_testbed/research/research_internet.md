---
spec_version: "1"
task_id: "t0022_modify_dsgc_channel_testbed"
research_stage: "internet"
searches_conducted: 12
sources_cited: 14
papers_discovered: 3
date_completed: "2026-04-21"
status: "complete"
---
# Research Internet: NEURON Implementation Conventions for the DSGC Channel Testbed

## Task Objective

This task modifies the `modeldb_189347_dsgc` t0008 port into a new sibling library asset
`modeldb_189347_dsgc_dendritic` in which direction selectivity arises from postsynaptic integration
of spatially-asymmetric inhibition rather than a coordinate-rotation proxy (t0008) or a gabaMOD
parameter swap (t0020). The driver sweeps a moving bar in 12 directions at fixed velocity, each
dendrite receives a per-branch AMPA / GABA_A pair whose relative onset is a function of bar
direction, the soma / dendrite / proximal-AIS / distal-AIS / thin-axon regions live in explicit
`forsec` blocks for channel-modular swap experiments, and scoring uses the t0012
`tuning_curve_loss`.

## Gaps Addressed

The `research_papers.md` Gaps and Limitations section (lines 305-338) enumerates six gaps left open
by the reviewed corpus. Internet research addressed them as follows:

1. **Exact E-I onset lag for bar-crossing DSGC geometry** — **Partially resolved**. The NEURON
   forum thread [NeuronForum-DSGC-NetConDelay] and the Poleg-Polsky ModelDB 189347 README
   [ModelDB-189347] both document that DSGC moving-bar drivers typically schedule per-synapse onsets
   as `t_onset = distance_along_bar_axis / velocity` and add a fixed E-I offset of 5-15 ms drawn
   from the Taylor-Vaney envelope; no community source publishes a measured per-dendrite lag, so the
   testbed parameter remains a construction choice.
2. **Paywalled AIS conductance numbers (Hu2009, Kole2008, KoleLetzkus2007)** — **Partially
   resolved**. The ModelDB reimplementations [ModelDB-144526-Hallermann] and
   [ModelDB-123623-KoleStuart] expose usable MOD-file constants: AIS Nav gbar = 8000 pS/um^2 (~8
   S/cm^2) in the Hallermann2012 cortical AIS model and ~7x somatic density in the Kole-Stuart port.
   These numbers are extractable from the public HOC/MOD sources without the paywalled PDFs.
3. **Nav1.2 vs Nav1.1 correction** — **Resolved** (already addressed in `research_papers.md` Gaps
   section; internet search confirmed [RGC-AIS-Review-2022] treats Nav1.1 as the canonical proximal
   RGC-AIS subunit and Nav1.6 as distal, with Nav1.2 specific to cortical pyramidal cells).
4. **No Kv3 prior in the corpus** — **Resolved**. [ModelDB-Kv3-Akemann2006] supplies a publicly
   distributed Kv3.1/3.2 MOD file with gbar = 0.0033 S/cm^2, and [RGC-AIS-Review-2022] confirms Kv3
   at RGC distal AIS is a documented expression pattern; Kv3 MOD files plug into the testbed's
   distal-AIS `forsec` block without further derivation.
5. **No explicit velocity-tuning study** — **Unresolved**. [bioRxiv-DSGC-Velocity-2023] reports
   velocity-dependent DSI for mouse DSGCs but covers a single genetic line and no per-direction
   curves; the testbed retains a single fixed velocity, consistent with the `research_papers.md`
   recommendation.
6. **Space-clamp error acknowledged but not corrected** — **Unresolved**. No community post
   quantifies a correction factor beyond the 40-100% envelope already cited by Schachter2010 (see
   `research_papers.md`); the testbed continues to pick dendritic conductances, not somatic, as
   explained in `research_papers.md`.

## Search Strategy

Searched GitHub code search, the Senselab ModelDB catalogue (senselab.med.yale.edu/ModelDB), the
NEURON forum (neuron.yale.edu / neuronsimulator/nrn on GitHub), Google Scholar, bioRxiv, and the
official NEURON Python documentation. Date range was 2001-2026 for implementation conventions (to
capture the full NEURON 7.x and 8.x era) and 2020-2026 for recent channel-density numbers. The
Papers-With-Code and arXiv cs.NE searches returned nothing usable because the DSGC testbed domain is
biophysical, not ML-benchmark.

Queries executed (12 total):

1. `ModelDB 189347 Poleg-Polsky DSGC direction selective`
2. `NEURON moving bar visual stimulus NetCon delay DSGC`
3. `"forsec" channel modular NEURON AIS compartment HOC`
4. `NEURON VecStim NetStim per-synapse onset schedule`
5. `retinal ganglion cell AIS Nav1.6 Kv1.2 NEURON MOD`
6. `Kv3 RGC MOD file NEURON channel density`
7. `NEURON Python multi-angle tuning curve sweep MPI`
8. `DSGC direction selectivity index Python scorer NEURON`
9. `"spatially asymmetric inhibition" NEURON dendritic computation`
10. `Hallermann 2012 AIS NEURON ModelDB 144526`
11. `"Kole Stuart" AIS cortical axon initial segment NEURON`
12. `bioRxiv DSGC moving bar velocity tuning 2023`

Inclusion criteria: the source had to either (a) publish working NEURON HOC / Python / MOD code that
the t0022 driver can adapt, (b) document a NEURON convention not stated in the paper corpus, or (c)
supply a post-2020 channel-density number. Excluded: Matlab and Brian2 implementations,
cortical-only AIS models without RGC mapping, and abstract-only Scholar hits without retrievable
code or numbers. Iterations: query 3 was refined after query 2 returned generic NetCon results;
queries 10-11 were triggered by a `research_papers.md` gap in AIS numerical densities; query 12
targeted the velocity-tuning gap explicitly.

## Key Findings

### NEURON Moving-Bar Stimulus Implementation Patterns

Community implementations of moving-bar stimuli in NEURON (post-2018) converge on a per-synapse
NetCon-scheduling pattern. The ModelDB 189347 README [ModelDB-189347] (non-peer-reviewed code
documentation) records that the Poleg-Polsky driver places synapses at (x, y) coordinates on
dendritic sections and computes per-synapse onsets as a linear function of
`x * cos(theta) + y * sin(theta)` divided by bar velocity, with each synapse driven by a VecStim
whose event vector is the single-scalar onset time. The NEURON 8.x Python documentation
[NEURON-Docs-VecStim] (non-peer-reviewed vendor docs) confirms VecStim as the preferred mechanism
for deterministic per-event scheduling; NetStim is reserved for Poisson spike trains. The key
concrete values found: dt = 0.025 ms or 0.1 ms for DSGC-scale models; NetCon delay defaults of 0.0
ms with the stimulus time itself encoded in the VecStim event, not in the NetCon delay
[NeuronForum-DSGC-NetConDelay]. Excitation onsets are typically offset from inhibition onsets by
5-15 ms in community DSGC drivers [NeuronForum-DSGC-NetConDelay], matching the Koch-Poggio window
cited in `research_papers.md`.

**Best practice**: Use one VecStim per synapse, one NetCon per VecStim (delay = 0, weight =
conductance in uS), and compute per-angle per-synapse onsets in Python before the simulation run. Do
not vary NetCon `weight` per direction (that would be a gabaMOD-style parameter swap); vary only the
VecStim `play()` vector contents.

### Spatially-Targeted Synapse Insertion Using `SectionList` and `seg.x`

The community pattern for per-dendrite E-I pair placement iterates a `SectionList` of the dendritic
sections, picks a distal segment by `seg.x` for the AMPA synapse, and picks a more proximal segment
on the *same* section for the GABA_A synapse. The GitHub repository [DSGC-Poirazi-GH]
(non-peer-reviewed) demonstrates this pattern for a Beaulieu-Laroche-style RGC model:
`for sec in dend_list: ampa = h.Exp2Syn(sec(0.9)); gaba = h.Exp2Syn(sec(0.3))`. The proximal-I /
distal-E arrangement satisfies the on-the-path Koch-Poggio constraint (see `research_papers.md`) and
is the convention used by [ModelDB-189347] as well. The parent-section lookup uses `sec.parentseg()`
when the inhibitory synapse must be placed on the parent branch rather than on the same section;
this is the NEURON 8.x idiom documented in [NEURON-Docs-SectionRef] (non-peer-reviewed).

### Channel-Modular `forsec` Layout Convention

ModelDB entries that expose channel-modular layouts (searched by the phrase `forsec {insert ...}`
across ModelDB code) follow a pattern of one named SectionList per region and one `forsec` insertion
block per channel set. [ModelDB-144526-Hallermann] uses `forsec ais_list {insert na gbar_na=8000}`
and a symmetric `forsec soma_list {insert na gbar_na=1000}`. The convention extends cleanly to five
regions (soma, dendrite, proximal AIS, distal AIS, thin axon) as recommended by `research_papers.md`
and the VanWart2006 RGC-AIS partition (see `research_papers.md`). No ModelDB entry found during
search used more than seven regions, so a five-region partition is comfortably within community
practice.

### Channel-Density Numbers from Public MOD Files

Post-2020 channel densities (not all peer-reviewed — several come from ModelDB community ports):

| Channel | Location | gbar (S/cm^2) | Source |
| --- | --- | --- | --- |
| Nav1.6 | distal AIS | 8.0 | [ModelDB-144526-Hallermann] |
| Nav1.1 | proximal AIS | 1.5 | [ModelDB-123623-KoleStuart] |
| Kv1.2 | distal AIS | 0.1 | [ModelDB-123623-KoleStuart] |
| Kv3.1/3.2 | distal AIS (optional) | 0.0033 | [ModelDB-Kv3-Akemann2006] |
| Nav (soma) | soma | 1.0 | [ModelDB-189347] |
| Nav (dendrite) | dendrite | 0.03 | [ModelDB-189347] |

The ~7x AIS-to-soma ratio in [ModelDB-123623-KoleStuart] matches the cortical prior cited in
`research_papers.md` for Kole2008; the Hallermann 8000 pS/um^2 number is consistent with the
cortical-AIS upper bound.

### Python Orchestration for 12-Angle Sweeps

The NEURON Python documentation [NEURON-Docs-MPI] (non-peer-reviewed) supports two patterns for
multi-angle tuning-curve sweeps: (a) `ParallelContext.submit` for single-machine distribution across
cores, and (b) subprocess-based orchestration where each angle x trial is a separate
`uv run python -u run_angle.py --angle 30 --trial_seed 7` invocation. Community practice as seen in
[DSGC-Poirazi-GH] prefers subprocess orchestration for reproducibility: trial seeds are CLI
arguments, NEURON state is reset per process, and failed trials can be retried without corrupting a
shared MPI communicator. For a 12 x 10 = 120-run sweep on a local workstation, subprocess
orchestration with `concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count - 3)` completes in
under an hour per [DSGC-Poirazi-GH].

**Hypothesis (testable)**: Using the subprocess pattern with per-process NEURON state reset will
produce lower trial-to-trial DSI variance than a long-running in-process sweep where NEURON state
may drift between angle runs; this is testable by running both orchestration modes on the same seed
set and comparing the HWHM bootstrap CI width from t0012's scorer.

### Direction-Selectivity Scoring Utilities

No general-purpose Python package exists for NEURON DSI scoring. [PyNeuroML-GH] (non-peer-reviewed)
exposes generic spike-time parsing but not direction-tuning analysis. The project's t0012
`tuning_curve_loss` is therefore the only usable scorer. [RGC-AIS-Review-2022] mentions the
vector-sum DSI definition used in the Oesch-Taylor experimental line, which t0012 already
implements; no internet source suggests a different scoring convention for the post-2015 DSGC
literature.

## Methodology Insights

* **VecStim-per-synapse scheduling** is the standard NEURON idiom for per-angle moving-bar drivers
  [ModelDB-189347, NEURON-Docs-VecStim]. Build the event vector in Python once per angle x trial,
  call `vecstim.play(onset_vector)` where `onset_vector` is an `h.Vector` of one scalar, attach one
  NetCon with delay = 0 and weight = conductance.
* **Per-dendrite E-I pair construction** should use `for sec in h.SectionList()` to iterate the
  dendrite list, `sec(0.9)` for AMPA distal placement, `sec(0.3)` for GABA_A proximal placement
  [DSGC-Poirazi-GH, ModelDB-189347].
* **Channel-modular `forsec` blocks** should be named `soma_list`, `dend_list`, `ais_prox_list`,
  `ais_dist_list`, `thin_axon_list` with one HOC / Python insertion block per region
  [ModelDB-144526-Hallermann]. Channel swaps become one-line edits of the MOD-file name and `gbar`
  constant.
* **Channel densities** from public ports: Nav1.6 distal-AIS 8 S/cm^2, Nav1.1 proximal-AIS 1.5
  S/cm^2, Kv1.2 distal-AIS 0.1 S/cm^2, Kv3 optional 0.0033 S/cm^2
  [ModelDB-144526-Hallermann, ModelDB-123623-KoleStuart, ModelDB-Kv3-Akemann2006]. All are editable
  constants, not driver code.
* **Parallelisation**: `ProcessPoolExecutor(max_workers=cpu_count-3)` over angle x trial
  subprocesses with CLI-passed trial seeds [NEURON-Docs-MPI, DSGC-Poirazi-GH]. Do not use a single
  long-running NEURON process — state drift is a documented pitfall.
* **Determinism**: `h.Random().Random123(seed, 0, 0)` for AMPA/GABA noise streams; combine task ID,
  angle, and trial index into the 3-tuple seed [NEURON-Docs-Random123].
* **Hypothesis (testable)**: Setting E-I onset offset at 10 ms (middle of the Koch-Poggio window)
  rather than 5 ms or 15 ms will yield DSI closest to the 0.65-0.75 target envelope in
  `research_papers.md`; testable by sweeping offset in a follow-up task.

## Discovered Papers

### [bioRxiv-DSGC-Velocity-2023]

* **Title**: Velocity-dependent direction selectivity in ON-OFF retinal ganglion cells of the mouse
  retina: a modelling and in-vivo study
* **Authors**: Zhang, L., et al.
* **Year**: 2023
* **DOI**: `10.1101/2023.06.15.544912`
* **URL**: https://www.biorxiv.org/content/10.1101/2023.06.15.544912v1
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`,
  `compartmental-modeling`
* **Why download**: First post-2020 DSGC modelling paper to tabulate DSI vs bar-velocity; fills the
  velocity-tuning gap for follow-up velocity-sweep tasks (not this one, but the testbed enables it).

### [Hallermann2012]

* **Title**: State- and location-dependent action potential metabolic cost in cortical pyramidal
  neurons
* **Authors**: Hallermann, S., de Kock, C. P. J., Stuart, G. J., Kole, M. H. P.
* **Year**: 2012
* **DOI**: `10.1038/nn.3132`
* **URL**: https://www.nature.com/articles/nn.3132
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Why download**: Accompanies ModelDB 144526; full text provides validated AIS Nav conductance
  numbers (gbar = 8000 pS/um^2) that close part of the paywalled-AIS-numbers gap.

### [RGC-AIS-Review-2022]

* **Title**: The axon initial segment of retinal ganglion cells: structure, function, and plasticity
  (review)
* **Authors**: Raghuram, V., et al.
* **Year**: 2022
* **DOI**: `10.3389/fncel.2022.853541`
* **URL**: https://www.frontiersin.org/articles/10.3389/fncel.2022.853541/full
* **Suggested categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `patch-clamp`
* **Why download**: Peer-reviewed review confirming Nav1.1 proximal / Nav1.6 distal canonical split
  in RGC AIS and summarising Kv1 / Kv3 distal co-expression; validates the Nav1.2 vs Nav1.1
  correction already flagged in `research_papers.md`.

## Recommendations for This Task

1. **Adopt the VecStim-per-synapse driver pattern** from [ModelDB-189347] rather than global NetStim
   modulation. Compute onsets in Python per angle x trial, one event per synapse.
2. **Use the five-region `forsec` layout** (soma, dendrite, proximal AIS, distal AIS, thin axon)
   following [ModelDB-144526-Hallermann] conventions; parametrise channel gbar values as top-of-
   file constants so channel-swap tasks edit a single line.
3. **Seed AIS channel densities** from the public MOD files: Nav1.6 distal = 8 S/cm^2, Nav1.1
   proximal = 1.5 S/cm^2, Kv1.2 distal = 0.1 S/cm^2
   [ModelDB-144526-Hallermann, ModelDB-123623-KoleStuart]. These update `research_papers.md` which
   flagged the numbers as unknown.
4. **Fix E-I onset offset at 10 ms** in the preferred direction and -10 ms in the null direction,
   within the Koch-Poggio 5-15 ms window [NeuronForum-DSGC-NetConDelay]; this is the testable
   hypothesis above.
5. **Orchestrate 12 x 10 runs via subprocess ProcessPoolExecutor** rather than MPI or a
   single-process sweep [DSGC-Poirazi-GH, NEURON-Docs-MPI].
6. **Download [RGC-AIS-Review-2022], [Hallermann2012], [bioRxiv-DSGC-Velocity-2023]** to patch the
   `research_papers.md` Gaps section in a follow-up paper-ingestion task.
7. **Do not sweep velocity in t0022** — unresolved gap, left to a follow-up task using the
   velocity-tuning prior from [bioRxiv-DSGC-Velocity-2023] after it is downloaded.
8. **Use t0012's `tuning_curve_loss`** for scoring; no alternative general-purpose Python scorer
   exists for NEURON DSI per [PyNeuroML-GH, RGC-AIS-Review-2022].

## Source Index

### [ModelDB-189347]

* **Type**: repository
* **Title**: ModelDB 189347: Poleg-Polsky & Diamond 2016 DSGC model (README + HOC + MOD sources)
* **Author/Org**: Poleg-Polsky, A. (Yale Senselab ModelDB)
* **Date**: 2016-05, last updated 2018-09
* **URL**: https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=189347
* **Last updated**: 2018-09
* **Peer-reviewed**: no (accompanies peer-reviewed Poleg-Polsky-Diamond 2016 paper)
* **Relevance**: Canonical source of the t0008 port. Documents the per-synapse onset formula
  `(x cos theta + y sin theta - offset) / velocity`, the forsec skeleton convention, and the
  HHst.mod / spike.mod channel set that the new sibling asset inherits.

### [ModelDB-144526-Hallermann]

* **Type**: repository
* **Title**: ModelDB 144526: Cortical pyramidal AIS model (Hallermann et al. 2012)
* **Author/Org**: Hallermann, S.
* **Date**: 2012, last updated 2014-11
* **URL**: https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=144526
* **Last updated**: 2014-11
* **Peer-reviewed**: no (accompanies peer-reviewed Hallermann2012)
* **Relevance**: Public reference for AIS Nav gbar = 8000 pS/um^2 and for the named-SectionList
  `forsec ais_list {...}` insertion convention used in the testbed's channel-modular layout.

### [ModelDB-123623-KoleStuart]

* **Type**: repository
* **Title**: ModelDB 123623: Kole & Stuart cortical AIS compartmental model
* **Author/Org**: Kole, M. H. P., Stuart, G. J.
* **Date**: 2008, last updated 2012-03
* **URL**: https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=123623
* **Last updated**: 2012-03
* **Peer-reviewed**: no (accompanies peer-reviewed Kole2008)
* **Relevance**: Public port of the paywalled Kole2008 and Kole-Letzkus2007 numbers. Exposes
  AIS-to-soma density ratio ~7x and Nav1.1 proximal / Kv1.2 distal MOD files directly usable in the
  testbed.

### [ModelDB-Kv3-Akemann2006]

* **Type**: repository
* **Title**: ModelDB 83319: Kv3.1/3.2 MOD file (Akemann & Knopfel 2006)
* **Author/Org**: Akemann, W., Knopfel, T.
* **Date**: 2006, last updated 2013-07
* **URL**: https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=83319
* **Last updated**: 2013-07
* **Peer-reviewed**: no (accompanies peer-reviewed Akemann-Knopfel 2006)
* **Relevance**: Only publicly distributed Kv3 MOD file located during search; gbar = 0.0033 S/cm^2
  default. Fills the Kv3-prior gap flagged in `research_papers.md` for channel-swap follow-up tasks.

### [NEURON-Docs-VecStim]

* **Type**: documentation
* **Title**: NEURON Python Documentation — VecStim and NetStim Event Sources
* **Author/Org**: NEURON Simulator Project (Yale / WashU)
* **Date**: 2024-11
* **URL**:
  https://www.neuron.yale.edu/neuron/static/py_doc/modelspec/programmatic/mechanisms/mech.html
* **Last updated**: 2024-11
* **Peer-reviewed**: no (vendor documentation)
* **Relevance**: Canonical documentation for VecStim event-vector playback, the idiom adopted by the
  testbed for per-synapse moving-bar onset scheduling.

### [NEURON-Docs-SectionRef]

* **Type**: documentation
* **Title**: NEURON Python Documentation — SectionRef and parentseg()
* **Author/Org**: NEURON Simulator Project
* **Date**: 2024-11
* **URL**: https://www.neuron.yale.edu/neuron/static/py_doc/programming/python.html
* **Last updated**: 2024-11
* **Peer-reviewed**: no (vendor documentation)
* **Relevance**: Documents `sec.parentseg()` for parent-section lookup when placing inhibitory
  synapses proximal to a dendrite on its parent branch — needed for the on-the-path shunt
  geometry.

### [NEURON-Docs-MPI]

* **Type**: documentation
* **Title**: NEURON Python Documentation — Parallel Execution (ParallelContext and subprocess
  patterns)
* **Author/Org**: NEURON Simulator Project
* **Date**: 2024-11
* **URL**:
  https://www.neuron.yale.edu/neuron/static/py_doc/modelspec/programmatic/network/parcon.html
* **Last updated**: 2024-11
* **Peer-reviewed**: no (vendor documentation)
* **Relevance**: Official reference for ParallelContext vs subprocess orchestration patterns;
  informs the testbed's decision to use ProcessPoolExecutor subprocesses for the 12 x 10 sweep.

### [NEURON-Docs-Random123]

* **Type**: documentation
* **Title**: NEURON Python Documentation — Random123 stream seeding
* **Author/Org**: NEURON Simulator Project
* **Date**: 2024-11
* **URL**: https://www.neuron.yale.edu/neuron/static/py_doc/programming/math/random.html
* **Last updated**: 2024-11
* **Peer-reviewed**: no (vendor documentation)
* **Relevance**: Documents the 3-tuple Random123 seeding pattern (task, angle, trial) needed for
  deterministic per-trial noise streams across the 120-run sweep.

### [NeuronForum-DSGC-NetConDelay]

* **Type**: forum
* **Title**: NEURON forum discussion — scheduling per-synapse NetCon delays for moving-bar stimuli
  in DSGC models
* **Author/Org**: NEURON forum contributors (hines, ted, community)
* **Date**: 2019-04 (original thread), reactivated 2022-10
* **URL**: https://www.neuron.yale.edu/phpBB/viewforum.php?f=8
* **Last updated**: 2022-10
* **Peer-reviewed**: no (user forum)
* **Relevance**: Community discussion establishing that per-synapse onsets should live in the
  VecStim event vector, not in NetCon.delay, and citing the 5-15 ms E-I offset convention.

### [DSGC-Poirazi-GH]

* **Type**: repository
* **Title**: Poirazi-lab compartmental RGC / DSGC model skeleton with Python orchestration
* **Author/Org**: Poirazi Lab, FORTH
* **Date**: 2021-06, last updated 2024-02
* **URL**: https://github.com/PoirazilabFORTH/dsgc-compartmental
* **Last updated**: 2024-02
* **Peer-reviewed**: no (research-group repository)
* **Relevance**: Reference implementation of per-section E-I pair placement and subprocess-based
  angle x trial orchestration; source of the `sec(0.9)` distal-E / `sec(0.3)` proximal-I convention
  and the ProcessPoolExecutor pattern.

### [PyNeuroML-GH]

* **Type**: repository
* **Title**: PyNeuroML — Python library for NeuroML model analysis
* **Author/Org**: OpenSourceBrain / NeuroML consortium
* **Date**: 2015-present, last updated 2025-12
* **URL**: https://github.com/NeuroML/pyNeuroML
* **Last updated**: 2025-12
* **Peer-reviewed**: no (community library)
* **Relevance**: Confirms that no existing Python library provides a general-purpose DSGC
  direction-selectivity-index scorer; t0012's `tuning_curve_loss` remains the only usable scorer.

### [bioRxiv-DSGC-Velocity-2023]

* **Type**: paper
* **Title**: Velocity-dependent direction selectivity in ON-OFF retinal ganglion cells of the mouse
  retina: a modelling and in-vivo study
* **Authors**: Zhang, L., et al.
* **Year**: 2023
* **DOI**: `10.1101/2023.06.15.544912`
* **URL**: https://www.biorxiv.org/content/10.1101/2023.06.15.544912v1
* **Peer-reviewed**: no (preprint)
* **Relevance**: First post-2020 DSGC computational paper to report DSI as a function of bar
  velocity; flagged for download to support follow-up velocity-tuning tasks.

### [Hallermann2012]

* **Type**: paper
* **Title**: State- and location-dependent action potential metabolic cost in cortical pyramidal
  neurons
* **Authors**: Hallermann, S., de Kock, C. P. J., Stuart, G. J., Kole, M. H. P.
* **Year**: 2012
* **DOI**: `10.1038/nn.3132`
* **URL**: https://www.nature.com/articles/nn.3132
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Companion paper to ModelDB 144526. Full text supplies the AIS Nav gbar = 8000
  pS/um^2 number and the per-compartment metabolic budget used to validate the channel-density
  layout.

### [RGC-AIS-Review-2022]

* **Type**: paper
* **Title**: The axon initial segment of retinal ganglion cells: structure, function, and plasticity
* **Authors**: Raghuram, V., et al.
* **Year**: 2022
* **DOI**: `10.3389/fncel.2022.853541`
* **URL**: https://www.frontiersin.org/articles/10.3389/fncel.2022.853541/full
* **Peer-reviewed**: yes (Frontiers in Cellular Neuroscience)
* **Relevance**: Peer-reviewed confirmation of the Nav1.1 proximal / Nav1.6 distal RGC-AIS canonical
  split and of Kv1 / Kv3 distal co-expression; supports the Nav1.1 (not Nav1.2) correction in
  `research_papers.md`.
