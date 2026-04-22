---
spec_version: "1"
task_id: "t0033_plan_dsgc_morphology_channel_optimisation"
research_stage: "papers"
papers_reviewed: 24
papers_cited: 16
categories_consulted:
  - "compartmental-modeling"
  - "cable-theory"
  - "dendritic-computation"
  - "direction-selectivity"
  - "voltage-gated-channels"
  - "retinal-ganglion-cell"
  - "synaptic-integration"
date_completed: "2026-04-22"
status: "complete"
---
## Task Objective

This task is a planning task: it must produce a cost and search-strategy envelope for a *future*
joint optimisation over DSGC dendritic morphology and the top-10 voltage-gated channel (VGC) types
that maximises direction-selectivity index (DSI) on the t0022 channel-modular testbed built atop the
Poleg-Polsky 2026 (de Rosenroll 2026) port (t0024). The downstream planning subagent will consume
this `research_papers.md` to estimate search-space dimensionality, expected simulation counts under
competing optimisation strategies, per-simulation wall-time scaling, and Vast.ai USD cost envelopes
for CoreNEURON-on-GPU, NN-surrogate-on-GPU, and many-core-CPU compute modes. Per researcher
constraint this stage uses the downloaded paper corpus only; no internet search.

## Category Selection Rationale

Consulted `compartmental-modeling` because every relevant precedent is a NEURON-style simulation
whose per-simulation wall-time and per-simulation free-parameter count constrain any joint
optimisation. Consulted `dendritic-computation` and `cable-theory` because the balance between
active-dendrite conductances and passive cable attenuation is the biophysical substrate that the
joint sweep will tune. Consulted `direction-selectivity` because this defines the DSI objective.
Consulted `voltage-gated-channels` because the top-10 VGC set is the channel axis of the
optimisation. Consulted `retinal-ganglion-cell` because DSGC is the target cell type. Consulted
`synaptic-integration` because the t0022 testbed instantiates direction-tuned Exp2Syn pairs whose
conductances and kinetics are held fixed during the future sweep but set the stimulus-side
constants. Excluded `patch-clamp` because patch-clamp papers primarily supply *targets* rather than
optimisation methodology. Explicitly searched for corpus coverage of high-dimensional parameter
optimisation, CoreNEURON/GPU-NEURON variants, and neural-network surrogate modelling; these keywords
do not map to any ARF category because the corpus is a DSGC-biophysics corpus, not a
numerical-methods corpus. That gap is documented in `## Gaps and Limitations`.

## Key Findings

### Gradient-Free Optimisation Is the Only Strategy the Corpus Actually Demonstrates for DSGC/SAC Biophysics

Two papers in the corpus directly implement gradient-free optimisation over compartmental-model
parameters with a DS-like objective. [PolegPolsky2026] built a 352-segment NEURON DSGC model and ran
a machine-learning outer loop described in the paper abstract as "gradient-free optimisation +
surrogate-model-assisted search" over a joint space that contains bipolar-cell input offsets,
weights, rise/decay kinetics, AMPA/NMDA ratio, A-type potassium density, and optional SAC-derived
inhibition, scoring each candidate by DSI computed from spike rates (or subthreshold somatic peak
voltage) under 12-direction moving-bar stimuli; the paper reports that "tens of thousands of
configurations" were simulated and that successful candidates were clustered *post hoc* and
dissected by targeted ablation to identify multiple qualitatively distinct DS-producing primitives
[PolegPolsky2026, Results]. [Ezra-Tsur2021] applied the DEAP library with NSGA-II, IBEA, and
rank-based selection to an 8-dimensional input-kinetics / input-density parameter space on a fixed
1013-compartment passive SAC morphology (NeuroMorpho NMO_139062); the GA used 100 individuals for
20-45 generations with crossover/mutation probability 0.4, and the authors confirmed "qualitatively
identical" convergence across six random seeds and across the three selection algorithms
[Ezra-Tsur2021, Methods]. These two papers are the corpus's only direct evidence for any specific
optimisation strategy on a DSGC/SAC compartmental model; they jointly establish a community default
of gradient-free search (evolutionary + surrogate-assisted) rather than Bayesian optimisation, CMA-
ES, or gradient-based training.

**Best practice** (converged across these two papers): treat DSGC-style parameter sweeps as a
gradient-free search over **O(10)-O(20)** free parameters with population sizes of
**O(100)-O(10,000)** and generation counts of **O(20)-O(50)** when paired with surrogate-assisted
acceleration. **Hypothesis**: Because both precedents converge on the same design pattern
(population + generations + optional surrogate acceleration), the future optimisation can adopt this
pattern without inventing a new method; any Bayesian-optimisation or CMA-ES baseline must be
justified against it, not assumed to dominate it.

### Surrogate-Model-Assisted Search Has Precedent but No Explicit Cost Accounting in the Corpus

[PolegPolsky2026] is the only DSGC paper in the corpus that explicitly names "surrogate-model-
assisted search" as part of its optimiser; the companion repository (`PolegPolskyLab/DS-mechanisms`)
is described in [PolegPolsky2026, Overview] as containing the NEURON model plus the ML outer loop,
but the paper summary does not break out (a) how many NEURON simulations trained the surrogate, (b)
which ML architecture was used (feed-forward, gradient-boosted, Gaussian process), (c) the
surrogate's wall-time speedup factor over direct NEURON evaluation, or (d) surrogate training vs
surrogate inference cost breakdown. The summary flags "Specific quantitative DSI values and velocity
thresholds are available in the PDF (which is downloaded) but are not reproduced here"
[PolegPolsky2026, Results], so the cost-accounting details are in-corpus but not yet summarised —
**not found in paper summary**. For the plan's cost-envelope work this is the most damaging gap: the
one paper that demonstrates a surrogate- assisted DSGC sweep does not quantify the economics of the
surrogate itself. No Bayesian optimisation, Gaussian-process regression, or CMA-ES is mentioned
anywhere in the corpus in the context of DSGC / SAC / RGC compartmental modelling.

### Morphology Dimensionality Can Be Reduced to 3-5 Scalar Parameters via Cuntz Generation

[Cuntz2010] is the single most important corpus paper for parameter-count reduction on the
morphology side of the joint optimisation. The authors reduce arbitrary dendritic morphology to an
extended minimum-spanning-tree construction driven by (a) a target density profile over a spanning
volume, (b) a single scalar balancing factor `bf` that weighs wiring length against root-to-leaf
path length, (c) the root location, and (d) Rall's 3/2 diameter-taper rule. Synthetic trees
generated under this construction match reconstructed fly LPTCs, hippocampal CA1 pyramidal cells,
and cerebellar Purkinje cells to **within a few percent** of total dendritic length, with
biologically realistic `bf` clustering at **0.2-0.7** [Cuntz2010, Results]. Critically for the DSGC
plan, the paper demonstrates that `bf` maps monotonically onto electrotonic compartmentalisation —
low `bf` produces electrotonically isolated subtrees, high `bf` produces electrotonically compact
trees — providing a direct single-parameter handle for controlling the subunit-structure of the
dendritic tree [Cuntz2010, Innovations]. **Best practice**: the future DSGC joint optimisation
should reduce the morphology axis to **O(3-5) scalar Cuntz parameters** (spanning volume, carrier-
point density / total wiring length, `bf`, root location, optional per-cell taper tweak) rather than
treat per-branch length and diameter as O(100-1000) free variables.

### Morphology Is a First-Class Determinant of Firing Pattern Even with Fixed Channel Biophysics

[Mainen1996] applied an identical set of Hodgkin-Huxley sodium, potassium, and calcium conductances
across four reconstructed cortical morphologies (layer-5 pyramidal, layer-3 pyramidal, stellate
interneuron, low-threshold-spiking interneuron) and reproduced the four canonical firing patterns
(regular spiking, bursting, fast spiking, low-threshold spiking) purely via morphological
differences [Mainen1996, Results]. The mechanism is the coupling between axonal spike initiation and
dendritic backpropagation: large trees load the soma with a slow capacitive current that re- excites
the axon initial segment and drives bursts; truncating the apical dendrite or removing dendritic Ca
conductance abolishes bursting [Mainen1996, Results]. This establishes a direct
morphology-biophysics coupling that the joint optimisation must respect: holding channels fixed and
sweeping morphology produces measurable output-firing differences, so the DSGC sweep cannot factor
cleanly into "morphology only" and "channels only" sub-problems. **Best practice** (converging with
[PolegPolsky2026] for DSGCs): never collapse the joint sweep into two independent marginal sweeps.

### Fine Spatial Discretisation Is Mandatory, Which Locks In Per-Simulation Cost

Multiple corpus papers converge on the requirement that DSGC compartmental models must be
discretised to well below the electrotonic space constant. [Schachter2010] reports each dendritic
segment `< 0.1 lambda` on a rabbit On-Off DSGC, producing thousands of compartments
[Schachter2010, Architecture]. [Ezra-Tsur2021] used 1013 compartments on both the SAC and the DSGC
morphologies. [PolegPolsky2026] fixed the search space on a **352-segment** DSGC morphology.
[deRosenroll2026] reports (citing Jain 2020 — not in this corpus) that ≤10 μm compartments are
required to resolve the experimentally-measured 5-10 μm local DS subunits. [Mainen1996] emphasises
the `d_lambda` discretisation rule as a prerequisite for trustworthy active-dendrite simulation. The
converged minimum is **hundreds of compartments** per DSGC; this is the dominant factor setting
per-simulation wall-time, because the cable-equation solver cost scales linearly with compartment
count ([Hines1997], see below) but the number of time steps required also grows with the fastest
gating kinetic and the finest compartment. **Best practice**: do not attempt to accelerate the joint
sweep by coarsening morphology below a few hundred compartments — doing so will invalidate the
local-DS-subunit structure that the DSI objective depends on.

### NEURON Numerics: O(N) Compartment Solver Is the Only Per-Simulation Scaling Result in the Corpus

[Hines1997] describes NEURON's branched-cable Gaussian-elimination solver with reordering that runs
in **O(N)** time versus **O(N^3)** for generic dense LU decomposition, a second-order staggered
Crank-Nicolson integrator at backward-Euler cost per step, and analytical HH gating updates via the
closed form `s_inf + (s - s_inf) * exp(-dt/tau)` [Hines1997, Results]. The paper reports "typical
simulation speeds on the order of **10^4 compartments** at subsecond simulated time per wall-clock
minute on 1990s workstations" [Hines1997, Results]; this is the only explicit
wall-time-vs-compartment-count scaling statement in the corpus. No corpus paper mentions CoreNEURON,
OpenACC, CUDA-accelerated NEURON, Intel MKL-accelerated NEURON, or any GPU-based alternative
simulator. This is a corpus gap (see `## Gaps and Limitations`); the downstream planning subagent
will need to estimate GPU speedups from outside the corpus or from empirical t0026 measurements.

### Per-Simulation Wall-Time Landmarks in the Corpus for DSGC/SAC Models

Three corpus points bracket the per-simulation wall-time question for DSGC/SAC compartmental models.
[Ezra-Tsur2021] reports on the Blue Brain V HPC (Intel Xeon 6140, 384 GB): single-SAC run time
**70.66 s**, SAC-network run time **421.47 s**, full DSGC-circuit run time **492.36 s** per trial
(post-compilation), with 1500 ms of simulated time at 0.025 ms dt [Ezra-Tsur2021, Methods].
[Schachter2010] does not report wall-time numbers — **not found in paper summary**.
[PolegPolsky2026] likewise does not report per-simulation wall-time in the available summary — **not
found in paper summary**. These points establish that a single NEURON-based DSGC-circuit evaluation
on a contemporary HPC node is in the **O(100)-O(500) s** range per run when the model includes an
embedding circuit; the t0026 empirical baselines of **3.8 s per (angle,trial)** on the t0022
deterministic isolated-cell model and **12.0 s per (angle,trial)** on the t0024 stochastic AR(2)
model fall inside this envelope once multiplied by the 12-angle × trial-count protocol.

### Top-10 VGC Set and Per-Channel Parameter Counts from t0019

[VanWart2006], [Kole2007], [FohlmeisterMiller1997], [Hu2009], and [Kole2008] together pin down the
RGC AIS channel complement. The `t0019` answer asset
(`tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md`)
consolidates these into a canonical set with explicit quantitative priors: Nav1.6 in the distal AIS
(V_half ~**-45 mV**, gbar ~**2500-5000 pS/μm²**), Nav1.2 in the proximal AIS (V_half ~**-32 mV**,
gbar ~**50× less than distal**), Kv1.1/Kv1.2 co-localising with Nav1.6 (V_half ~**-40 to -50 mV**, τ
~**0.5-1 ms**, gbar ~**100-300 pS/μm²**), Kv2.1 somatic, plus Fohlmeister-Miller Kdr/Ka/Ca kinetics
for the soma and dendrites (Nav V_half ~**-40 mV**, Kdr V_half ~**-30 mV**, Q10 ~3 from 22 °C to 37
°C) [VanWart2006, Kole2007, FohlmeisterMiller1997, Hu2009, Kole2008]. [Fohlmeister2010] extends this
with cell-type-specific conductance maps at 35 °C in mS/cm² across dendrites / soma / IS / TS / axon
for both rat and cat RGCs and reports dendritic channel densities (e.g. rat Type I: Na 79.5 / K 23.4
/ Ca 1.2 / K_A ~36 / K_Ca small in dendrites) [Fohlmeister2010, Results]. [Aldor2024] adds Kv3 in
the perisomatic SAC region with dendritic mGluR2 modulation [Aldor2024]. Under a gbar-only
parameterisation each VGC contributes **1 free parameter**; under a gbar+shift parameterisation each
VGC contributes **2 free parameters**. The top-10 set therefore contributes **10-20 free channel
parameters** before any region-specific gbar distinctions (soma / dendrite / AIS-proximal /
AIS-distal / thin-axon = 5 regions per channel, bounded above by **10 × 2 × 5 = 100** but in
practice most channels are restricted to 1-2 of the 5 regions by the `t0019` priors).

### Two Active Channels in Dendrites Are Sufficient to Convert Sub-DSI into Supra-DSI

[Schachter2010] shows that uniform dendritic Na density of **40 mS/cm²** (or a proximal-to-distal
gradient of **45 → 20 mS/cm²**) plus Kdr is sufficient to transform weak subthreshold directional
asymmetry (PSP DSI ~**0.2**) into strong somatic spike directional tuning (spike DSI ~**0.8**), a
**~4×** amplification via the local spike-initiation threshold [Schachter2010, Results].
[deRosenroll2026] (relaying Jain 2020, which is not in this corpus) sharpens this with
NMDA-dependent local amplification: for soft voltage thresholds of **-55 / -50 / -48 mV**, dendritic
DSI rises from **0.42 / 0.70 / 0.80**. This implies that for the joint optimisation, active
dendritic Na and K are *necessary* channels (not optional), and adding NMDA receptors creates a
further multiplicative gain lever. **Best practice**: fix an active-dendrite lower bound (at
minimum: Nav + Kdr) rather than allowing the optimiser to zero out dendritic channels, since
passive-dendrite configurations are known *a priori* to cap DSI below the achievable spike DSI band.

### The t0022 Region Partition Defines the Concrete Channel-Parameter Topology

The t0022 testbed (`tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc`)
declares exactly **5 named SectionLists** (SOMA_CHANNELS, DEND_CHANNELS, AIS_PROXIMAL, AIS_DISTAL,
THIN_AXON) with canonical per-region channel priors: soma Nav gbar 1.0 S/cm²; dend Nav gbar 0.03
S/cm²; AIS_PROXIMAL Nav1.1 gbar 1.5 S/cm²; AIS_DISTAL Nav1.6 gbar 8.0 S/cm², Kv1.2 gbar 0.1 S/cm²,
Kv3 gbar 0.0033 S/cm²; THIN_AXON inherits baseline HHst. These five regions × top-10 VGCs define the
maximum channel-parameter topology. Under a gbar-only single-region-per-channel parameterisation,
the channel axis is **10 parameters**; under a per-region-gbar parameterisation, the channel axis is
at most **50 parameters** (but sparsified by the `t0019` priors to ~**15-25** channel/region
combinations). This is the concrete dimensionality the downstream planner must operate on.

### Connectomic-Scale Reconstructions Supply Morphology Priors at No Simulation Cost

[deRosenroll2026] and [Srivastava2022] (together with Briggman 2011 and Kim 2014, which are present
in the corpus as paper assets but not needed as load-bearing citations here) collectively
demonstrate that connectome-derived DSGC morphologies and SAC-to-DSGC wiring are available at scale
and can be imported directly into NEURON-based sweeps. The space-time wiring rule relayed by
[Srivastava2022] from the connectomic literature uses **6 proximal (BC7, sustained) + 12 distal
(BC5, transient)** synapses sampled pseudo-randomly from Ding-2016 empirical PDFs, with synaptic
conductances scaling **172.2 pS proximal → 68.6 pS distal** [Srivastava2022, Methods]. This means
the morphology axis of the joint optimisation does not have to generate DSGC arbors *ab initio*:
real reconstructions (e.g., NeuroMorpho NMO_05318 from [Ezra-Tsur2021]) plus Cuntz-style synthetic
perturbations are both available as starting points. **Best practice**: anchor the morphology sweep
on a small set of seed reconstructions (Poleg-Polsky backbone, NMO_05318, and 1-2 further connectome
exports) and let Cuntz parameters interpolate between them, rather than sampling the morphology
generator uniformly.

## Methodology Insights

* **Default search strategy**: gradient-free evolutionary search with population = **O(100)**,
  generations = **O(20-45)**, crossover/mutation = **0.4**, multi-seed (>=3) validation
  [Ezra-Tsur2021, Methods]. NSGA-II is the first-line choice because it extends cleanly to
  multi-objective if DSI is later paired with a secondary objective.

* **Surrogate-assisted extension**: the [PolegPolsky2026] pipeline combines gradient-free search
  with a surrogate model. For the plan, assume the surrogate burns **O(10^3-10^4) NEURON
  simulations** to train (the PDF quantifies this but the summary does not — **not found in paper
  summary**) and provides O(>1000×) inference speedup. Include an explicit sensitivity row for
  surrogate training cost ranging 1000-50000 NEURON evaluations.

* **Morphology parameterisation**: use Cuntz [Cuntz2010] with **3-5 scalar parameters** (spanning
  volume, carrier-point density, balancing factor `bf` in **[0.2, 0.7]**, root location, optional
  per-cell taper tweak) rather than per-branch geometry.

* **Channel parameterisation**: use the t0022 5-region × top-10-VGC matrix from the `t0019` answer,
  holding `V_half` and kinetic τ at the Fohlmeister-Miller / Kole / Hu / VanWart / Kole-2008
  literature values and varying only `gbar` per (region, channel) combination to keep the channel
  axis at **~15-25 parameters**
  [VanWart2006, Kole2007, FohlmeisterMiller1997, Hu2009, Kole2008, Fohlmeister2010].

* **Joint dimensionality upper bound**: O(5) morphology + O(15-25) channel = **O(20-30) free
  parameters**. Under a classic "10× dimension per generation for evolutionary search" rule of thumb
  — uncorroborated by the corpus; flagged as an assumption the plan must own — that maps to
  **O(200-300) evaluations per generation × O(20-45) generations = O(4000-13500) NEURON
  simulations**, with a surrogate accelerant potentially reducing total NEURON-backed evaluations to
  O(1000-5000).

* **Per-simulation wall-time baseline**: empirical t0026 measurements are **3.8 s per (angle,trial)
  on t0022 deterministic** and **12.0 s per (angle,trial) on t0024 stochastic AR(2)**. Under the
  12-angle × 10-trial-replicates standard, that is **~7.6 min/sim on t0022** and **~24 min/sim on
  t0024** per candidate morphology+channel vector. For the joint sweep, the stochastic AR(2) path is
  the conservative upper bound; the deterministic path can be used for the surrogate-training phase.

* **Discretisation floor**: hundreds of compartments per cell, respecting `d_lambda < 0.1`
  [Mainen1996, Schachter2010, Ezra-Tsur2021]. Do *not* coarsen to accelerate — coarsening erases the
  5-10 μm local DS subunits that [deRosenroll2026] relays from Jain 2020 (not in this corpus), on
  which the DSI objective depends.

* **Active-dendrite lower bound**: the optimiser must not be allowed to zero out Nav + Kdr in the
  dendrites, since passive-dendrite configurations cap DSI [Schachter2010]. Encode this as a hard
  floor on dendritic gNa and gKdr.

* **Reproducibility**: record `dt`, `nseg` per section, random seeds, and NEURON version per run,
  per [Hines1997] section/segment abstraction concerns. Multi-seed (>=3) replication per
  [Ezra-Tsur2021] is mandatory — do not report DSI from a single seed.

* **DSI metric definition**: use the standard vector-angle / PD-ND difference definition across 12
  directions, matching the t0022 `ACCEPTANCE_MIN_DSI = 0.5` gate and the `METRIC_KEY_DSI` constant
  already registered in `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py`.

* **Hypotheses to test in the plan** (explicit):
  1. Surrogate-assisted search reduces total NEURON-backed simulations by **>=5×** relative to a
     pure GA, converging with [PolegPolsky2026].
  2. Cuntz `bf` has a monotonic effect on DSI within **[0.2, 0.7]** because `bf` monotonically
     controls electrotonic compartmentalisation and local DS subunits require electrotonic isolation
     [Cuntz2010], together with the 5-10 μm subunit constraint that [deRosenroll2026] relays from
     Jain 2020.
  3. AIS-distal Nav1.6 `gbar` in **[2000, 5000] pS/μm²** dominates DSI among channel parameters
     because it gates AP initiation at the microdomain that first fires
     [VanWart2006, Hu2009, Kole2008].

## Gaps and Limitations

The corpus has strong coverage of DSGC biophysics, morphology, and channel priors but weak or absent
coverage on five methodology questions the downstream planner must resolve:

* **CoreNEURON / GPU-NEURON variants**: zero corpus papers mention CoreNEURON, OpenACC, CUDA-based
  NEURON, or any GPU-accelerated cable-equation solver. [Hines1997] is the only numerical-methods
  paper and it predates GPUs. No speedup factor, no hardware requirement, and no per-simulation
  throughput is quantified in the corpus for any GPU variant. The planner must source these numbers
  elsewhere (e.g., CoreNEURON documentation or the Blue Brain Project outputs) — flag in the plan as
  an external-input dependency.

* **NN-surrogate training and inference economics**: [PolegPolsky2026] names surrogate-assisted
  search but the summary does not quantify surrogate training cost, inference cost, or speedup
  factor. The plan's NN-surrogate compute-strategy cost envelope therefore rests on an assumption,
  not on corpus evidence. Flag this as a **medium-priority** follow-up: either re-read the
  [PolegPolsky2026] PDF (downloaded) for the specific numbers, or accept the assumption and carry it
  through sensitivity analysis.

* **Bayesian optimisation and CMA-ES**: no corpus paper uses these strategies on a DSGC / SAC / RGC
  compartmental model. The plan cannot cite a DSGC-specific baseline for either; comparison must be
  at the level of generic gradient-free-optimiser literature or omitted.

* **Per-simulation wall-time scaling with compartment count and timestep**: [Hines1997] asserts O(N)
  compartment scaling but reports no measured throughput on modern hardware. [Ezra-Tsur2021] reports
  three per-simulation data points (70.66 / 421.47 / 492.36 s) on Blue Brain V Intel Xeon 6140 but
  does not vary N or dt systematically. The t0026 data provide two additional empirical points
  (t0022 deterministic 3.8 s, t0024 stochastic 12.0 s per angle-trial). There is no corpus curve for
  wall-time as a function of compartment count — the plan will have to fit an extrapolation on three
  points, which is weak.

* **Dimensionality-reduction for channels**: [Cuntz2010] solves this cleanly for morphology, but
  there is no corpus precedent for reducing the 10-VGC × 5-region channel space via hierarchical
  priors, parameter sharing across regions, or Sobol sampling. The plan must propose a
  dimensionality-reduction scheme (likely per-channel single-region assignment from the `t0019`
  priors) and acknowledge that no DSGC-specific paper validates it.

Additional narrower gaps: the Jain 2020 dendritic DSI numbers are accessed via [deRosenroll2026]'s
citation rather than a direct read (Jain 2020 is not present in this corpus as a paper asset) —
adding that paper would be a medium-priority corpus refresh. [Fohlmeister2010] per-region gbar
tables have only 4 RGC morphology types (rat Type I/II and cat alpha/beta) — DSGC-specific gbar
measurements are not in the corpus. [Koren2017] adds cross-compartmental SAC modulation but does not
bear directly on the DSGC joint- sweep dimensionality.

## Recommendations for This Task

1. **Fix the default search strategy as gradient-free evolutionary (DEAP-style GA or equivalent)
   with surrogate-assisted acceleration**, grounded in [PolegPolsky2026] and [Ezra-Tsur2021]. Use
   population **100-200**, generations **20-45**, crossover/mutation **0.4**, multi-seed (>=3)
   replication. Do not commit the plan to Bayesian optimisation or CMA-ES without an explicit caveat
   that no DSGC precedent exists in the corpus.

2. **Reduce the morphology axis to 3-5 Cuntz parameters** (spanning volume, carrier-point density,
   balancing factor `bf ∈ [0.2, 0.7]`, root location, optional per-cell tweak) per [Cuntz2010]
   rather than per-branch geometry. This caps the morphology search space at O(10^4-10^5) grid
   points even under coarse discretisation.

3. **Reduce the channel axis to ~15-25 region-channel gbar parameters** by combining the t0022
   5-region partition with the `t0019` top-10 VGC priors; hold V_half and τ constant at the
   Fohlmeister-Miller / Kole / Hu / VanWart / Kole-2008 literature values
   [VanWart2006, Kole2007, FohlmeisterMiller1997, Hu2009, Kole2008, Fohlmeister2010].

4. **Anchor per-simulation wall-time on t0026 empirical measurements** (3.8 s per angle-trial t0022,
   12.0 s per angle-trial t0024) and use [Ezra-Tsur2021]'s 70-500 s per-trial point as an
   upper-bound consistency check. Do not rely on [Hines1997]'s 1990s-hardware number.

5. **Flag the CoreNEURON / GPU-NEURON evidence gap as an external-input dependency** in the plan.
   The plan should either (a) commit to a specific speedup assumption (e.g., 5-20× for
   CoreNEURON-on-GPU vs CPU) with an explicit sensitivity band, or (b) exclude the GPU option from
   the recommended combination until a CoreNEURON-specific reference can be brought in.

6. **Build the cost model around three compute strategies as scoped** (CoreNEURON-on-GPU,
   NN-surrogate-on-GPU, many-core CPU), with the NN-surrogate option carrying an explicit assumption
   about surrogate-training cost (O(10^3-10^4) NEURON calls) since the corpus does not quantify it.

7. **Enforce a hard floor on dendritic Nav + Kdr** in the optimiser's search bounds so that the
   optimiser cannot degenerate to a passive-dendrite configuration that trivially fails DSI
   [Schachter2010].

8. **Record discretisation floor (`d_lambda < 0.1`, >=hundreds of compartments) as an inviolable
   constraint** on the morphology axis [Mainen1996, Schachter2010, Ezra-Tsur2021, deRosenroll2026].
   Do not offer a coarse-discretisation compute-reduction lever.

9. **Plan a sensitivity analysis** over per-sim cost (**0.5×, 1×, 2×**) and sample count (**0.5×,
   1×, 2×**) as pre-specified in `task_description.md`; this is what the downstream planner needs to
   close the loop on the cost envelope given the multiple corpus gaps.

10. **Defer any multi-objective formulation** (DSI + information + energy + Cajal cytoplasm
    minimisation) per the explicit out-of-scope notice in `task_description.md`; record it as a
    future-task suggestion only.

## Paper Index

### [Aldor2024]

* **Title**: Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic computation of mouse
  starburst amacrine cells
* **Authors**: Ledesma, H. A., Ding, J., Oosterboer, S., Huang, X., Chen, Q., Wang, S., Lin, M. Z.,
  Wei, W.
* **Year**: 2024
* **DOI**: `10.1038/s41467-024-46234-7`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_s41467-024-46234-7/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `synaptic-integration`,
  `voltage-gated-channels`
* **Relevance**: Adds perisomatic Kv3 to the top-10 VGC set for SAC/DSGC modelling and documents
  mGluR2 dendritic modulation; supports the t0022 channel partition's AIS_DISTAL Kv3 inclusion.

### [Cuntz2010]

* **Title**: One Rule to Grow Them All: A General Theory of Neuronal Branching and Its Practical
  Application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Häusser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `cable-theory`
* **Relevance**: Provides the 3-5-parameter Cuntz morphology generator and TREES toolbox. This is
  the load-bearing reference for reducing the morphology axis of the joint optimisation from
  O(100-1000) per-branch parameters to **O(3-5) scalars**.

### [deRosenroll2026]

* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: de Rosenroll, G., Sethuramanujam, S., Awatramani, G. B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Asset**: `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: The biophysical backbone that t0024 ports and t0022 extends; identifies that local
  subunit-level DSI is the sensitive objective and relays the Jain 2020 5-10 μm subunit scale that
  constrains the morphology-discretisation floor.

### [Ezra-Tsur2021]

* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  to starburst amacrine cells in direction selectivity
* **Authors**: Ezra-Tsur, E., Amsalem, O., Ankri, L., Patil, P., Segev, I., Rivlin-Etzion, M.
* **Year**: 2021
* **DOI**: `10.1371/journal.pcbi.1009754`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1009754/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`
* **Relevance**: Primary corpus precedent for GA-based (DEAP / NSGA-II / IBEA) parameter sweep of
  SAC / DSGC compartmental models, with explicit per-trial wall-time numbers on Blue Brain V HPC
  (70.66 / 421.47 / 492.36 s) and a documented 8-D parameter space.

### [Fohlmeister2010]

* **Title**: Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using
  Temperature as an Independent Variable
* **Authors**: Fohlmeister, J. F., Cohen, E. D., Newman, E. A.
* **Year**: 2010
* **DOI**: `10.1152/jn.00123.2009`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/`
* **Categories**: `retinal-ganglion-cell`, `compartmental-modeling`, `voltage-gated-channels`,
  `patch-clamp`
* **Relevance**: Per-region (dendrite / soma / IS / TS / axon) gbar tables for rat and cat RGCs at
  35 °C, providing the gbar search-range priors for the channel axis of the joint optimisation.

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Canonical HH rate functions for RGC Nav / Kdr / Ka / Ca at 22 °C with Q10 ~3. These
  kinetics define the V_half and τ values that the joint optimisation holds fixed while varying
  gbar.

### [Hines1997]

* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **Categories**: `compartmental-modeling`, `cable-theory`, `voltage-gated-channels`
* **Relevance**: The only corpus paper describing NEURON's O(N) cable solver, staggered
  Crank-Nicolson integrator, and analytical HH gating update. Establishes that per-simulation cost
  scales linearly in compartment count — the foundation of the wall-time model.

### [Hu2009]

* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W., Tian, C., Li, T., Yang, M., Hou, H., Shu, Y.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Establishes the **10-15 mV V_half split** between Nav1.6 (distal AIS, V_half ~-45
  mV) and Nav1.2 (proximal AIS, V_half ~-32 mV). Justifies keeping separate AIS_DISTAL /
  AIS_PROXIMAL gbar parameters in the joint optimisation.

### [Kole2007]

* **Title**: Axon Initial Segment Kv1 Channels Control Axonal Action Potential Waveform and Synaptic
  Efficacy
* **Authors**: Kole, M. H. P., Letzkus, J. J., Stuart, G. J.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.07.031`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1016_j.neuron.2007.07.031/`
* **Categories**: `voltage-gated-channels`, `dendritic-computation`
* **Relevance**: Provides the AIS-distal Kv1 priors (V_half ~**-40 to -50 mV**, τ ~**0.5-1 ms**,
  gbar ~**100-300 pS/μm²**) for the channel axis.

### [Kole2008]

* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P., Ilschner, S. U., Kampa, B. M., Williams, S. R., Ruben, P. C., Stuart,
  G. J.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Peak AIS Nav conductance density **2500-5000 pS/μm²** (~50× somatic density),
  setting the upper range for the AIS_DISTAL gbar search bound in the joint optimisation.

### [Koren2017]

* **Title**: Cross-compartmental Modulation of Dendritic Signals for Retinal Direction Selectivity
* **Authors**: Koren, D., Grove, J. C. R., Wei, W.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.07.020`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Demonstrates that cross-compartmental SAC modulation affects downstream DSGC
  function; motivates keeping the SAC→DSGC input schedule fixed during the sweep rather than
  co-optimising it (consistent with the out-of-scope note in `task_description.md`).

### [Mainen1996]

* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/`
* **Categories**: `cable-theory`, `dendritic-computation`, `compartmental-modeling`
* **Relevance**: Canonical demonstration that morphology alone reshapes firing patterns under fixed
  channel biophysics; establishes the `d_lambda` discretisation rule and the morphology- biophysics
  coupling that forbids factoring the joint sweep into marginal sweeps.

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: The corpus's primary reference for gradient-free + surrogate-assisted search
  applied directly to a 352-segment DSGC compartmental model with DSI as the objective. Defines the
  methodological template the plan should follow.

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`, `synaptic-integration`, `cable-theory`
* **Relevance**: Quantifies dendritic Na density **40 mS/cm²** (uniform) or **45→20 mS/cm²**
  (gradient) as the baseline active-dendrite configuration; shows the **4×** DSI amplification from
  PSPs to spikes that the joint optimisation is trying to preserve or extend. Also the source of the
  "active-dendrite is necessary, not optional" constraint.

### [Srivastava2022]

* **Title**: Spatiotemporal properties of glutamate input support direction selectivity in the
  dendrites of retinal starburst amacrine cells
* **Authors**: Srivastava, P., de Rosenroll, G., Matsumoto, A., Michaels, T., Turple, Z., Jain, V.,
  Sethuramanujam, S., Murphy-Baum, B. L., Yonehara, K., Awatramani, G. B.
* **Year**: 2022
* **DOI**: `10.7554/eLife.81533`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.7554_eLife.81533/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `synaptic-integration`, `retinal-ganglion-cell`
* **Relevance**: Provides per-synapse conductance scaling (**172.2 pS proximal → 68.6 pS distal**)
  and the 6-proximal + 12-distal BC synapse count that fix the synaptic-input axis (held constant
  during the sweep per scope).

### [VanWart2006]

* **Title**: Polarized distribution of ion channels within microdomains of the axon initial segment
* **Authors**: Van Wart, A., Trimmer, J. S., Matthews, G.
* **Year**: 2006
* **DOI**: `10.1002/cne.21173`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1002_cne.21173/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`
* **Relevance**: Demonstrates the RGC AIS subdivides into Nav1.6-distal + Nav1.2-proximal
  microdomains, justifying the t0022 5-region partition (SOMA / DEND / AIS_PROXIMAL / AIS_DISTAL /
  THIN_AXON) that anchors the channel-axis parameterisation.
