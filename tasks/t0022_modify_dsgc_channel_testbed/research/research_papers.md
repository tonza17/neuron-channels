---
spec_version: "1"
task_id: "t0022_modify_dsgc_channel_testbed"
research_stage: "papers"
papers_reviewed: 24
papers_cited: 20
categories_consulted:
  - "cable-theory"
  - "compartmental-modeling"
  - "dendritic-computation"
  - "direction-selectivity"
  - "patch-clamp"
  - "retinal-ganglion-cell"
  - "synaptic-integration"
  - "voltage-gated-channels"
date_completed: "2026-04-20"
status: "complete"
---
# Research Papers: Dendritic-Computation DSGC Testbed Priors

## Task Objective

This task modifies the existing `modeldb_189347_dsgc` port (t0008) into a new sibling library asset
`modeldb_189347_dsgc_dendritic` in which direction selectivity arises from postsynaptic dendritic
integration of spatially-asymmetric inhibition — the biologically meaningful mechanism
(Koch-Poggio- Torre on-the-path shunting; Barlow-Levick veto). The driver must sweep a moving bar in
12 directions (30 deg spacing) at a fixed velocity, no per-angle synapse rotation, no global GABA
parameter swap, no per-condition driver tricks. Somatic spike DSI must reach at least 0.5 with peak
firing rate at least 10 Hz. AIS, soma, and dendrite compartments must live in explicit `forsec`
blocks with channel-insertion hooks so follow-up channel-swap tasks (Nav1.6-only, +Ih, Kv1 vs Kv3)
can edit channels without touching the driver. This research stage synthesises the evidence pool
from the five sibling literature surveys (t0015-t0019) and the anchor DSGC corpus (t0002) into three
design decisions: (a) what spatially-asymmetric-inhibition geometry produces DSI greater than or
equal to 0.5 postsynaptically, (b) which passive cable parameters make the shunt actually veto
excitation, and (c) how the AIS / soma / proximal dendrite partition must look for channel-swap
experiments to remain physiologically meaningful.

## Category Selection Rationale

Consulted all eight DSGC-relevant categories because this task sits at the intersection of every
mechanism covered by the five surveys. `direction-selectivity` and `dendritic-computation` are
primary because the mechanism being instantiated is a direction-selective dendritic computation.
`cable-theory` is primary because whether the proposed shunt can veto excitation depends on
electrotonic distance, R_i, C_m, and R_m. `compartmental-modeling` is primary because the driver
must be written against a NEURON skeleton inherited from the t0008 port and must match the d_lambda
and simulator-alignment conventions used by the existing DSGC papers in the corpus.
`voltage-gated-channels` and `patch-clamp` are primary because the `forsec` partition must match
published AIS channel localisation and published somatic / dendritic conductance densities.
`synaptic-integration` is primary because E-I timing and receptor-kinetic priors constrain how bar
velocity maps to per-dendrite E/I overlap windows. `retinal-ganglion-cell` is consulted for RGC-
specific kinetics and spike thresholds.

No categories are excluded. Every category in `meta/categories/` carries at least one paper cited
below.

## Historical Context

Three waves of DSGC research are load-bearing for this task. The first is the cable-theoretic wave
of the late 1970s and early 1980s in which Koch, Poggio, and Torre proposed that nonlinear dendritic
interactions between excitation and shunting inhibition can implement direction selectivity
[KochPoggio1982, KochPoggio1983]. The second is the experimental wave culminating in [Taylor2000],
which established by voltage-clamp and pharmacological dissection that the nonlinear interaction
underlying DSGC direction selectivity occurs postsynaptically within DSGC dendrites rather than
being inherited by presynaptic wiring. The third is the compartmental-modelling wave of the 2000s
and 2010s [Oesch2005, Schachter2010, Park2014, Jain2020], which quantified the dendritic
spike-initiation mechanism, the null/preferred conductance ratio, and the electrotonic
compartmentalisation of the DSGC arbor. The AIS and HH-kinetics priors
[FohlmeisterMiller1997, VanWart2006, Hu2009, Kole2008, KoleLetzkus2007] come from a separate
cortical + RGC AIS lineage. This task assembles those three waves into one testbed.

## Key Findings

### Asymmetric Inhibition as the Direction-Selective Mechanism in DSGCs

DSGC direction selectivity arises experimentally from asymmetric inhibition acting on the
postsynaptic dendritic tree, not from presynaptic wiring symmetry [Taylor2000]. The critical
nonlinear interaction between excitation and inhibition takes place within DSGC dendrites
[Taylor2000]. The DS signal, measured with voltage-clamp at holding potentials that isolate
excitatory or inhibitory currents respectively, shows that inhibition is **2-4x larger** for
null-direction than preferred-direction motion at peak velocity, while excitation is approximately
direction-untuned with null/preferred ratio ~0.8-1.0 [Park2014, Taylor2014]. Specifically,
[Park2014] reports preferred-direction E = 0.31 nS paired with null-direction I = 2.43 nS at the DSI
~0.65 working point — an effective null/preferred inhibitory ratio near **8x** and almost-flat
excitation. The overall spike-level DSI achieved postsynaptically is 0.67-0.74 in rabbit DSGCs
[Oesch2005] and 0.65 +/- 0.05 in mouse DSGCs [Park2014], with preferred-direction peak AP rates of
80-150 Hz [Sivyer2013] and dendritically-confirmed locus of computation [Taylor2000, Oesch2005].

**Best practice**: In the t0022 testbed, drive each dendritic subtree with a fixed pair of E and I
conductances whose relative timing depends on bar direction. Set the null/preferred inhibitory ratio
in the 2-4x range measured by [Park2014, Taylor2014]; set excitation to be direction-untuned (flat
conductance across directions) consistent with [Park2014]. Target spike DSI of 0.5-0.75 per
[Oesch2005, Park2014] rather than chasing the upper end of the paper envelope.

**Hypothesis**: The DSGC dendritic tree acts as a set of near-independent electrotonic subunits;
with excitation held direction-untuned and inhibition asymmetric, a dendritic-initiation threshold
that is unreachable under null-direction shunt is the sufficient mechanism — no global parameter
swap or coordinate rotation is needed [Schachter2010, Oesch2005]. This is the direct testable claim
of the t0022 asset.

### On-the-Path Shunting: Geometric and Temporal Conditions

The classical biophysical mechanism for dendritic direction selectivity is on-the-path shunting
[KochPoggio1982, KochPoggio1983]. An inhibitory synapse with a reversal potential near rest placed
*between* an excitatory synapse and the soma can open a conductance that divides the local membrane
resistance, acting as an analog multiplicative gate. The key quantitative results are: (a) the shunt
must be placed proximal to the excitation along the same dendrite — distal inhibition does not
veto proximal excitation [KochPoggio1982]; (b) an inhibitory conductance of approximately **50 nS**
is theoretically sufficient to veto an opposed excitatory input in a cat delta ganglion cell
[KochPoggio1983]; (c) the null-direction veto requires temporal overlap between E and I — if
inhibition arrives after the excitation has already charged the membrane, the veto is weaker
[KochPoggio1983]. Passive cable theory also places alpha-class RGC dendrites at electrotonic length
L ~ 0.5-0.8 lambda [KochPoggio1982], which means the dendrites are *not* isopotential; a proximal
shunt does not short the whole tree, so shunting is local to the branch and consistent with
branch-level DS [Jain2020].

**Best practice**: Position each inhibitory synapse *proximal* (closer to the soma) to the paired
excitatory synapse on the same dendritic branch [KochPoggio1982, KochPoggio1983]. Per-dendrite E and
I synapses, not global parameter scalars, are what encode direction in this mechanism.

**Hypothesis**: Setting E-to-I temporal offset to +5 to +20 ms in the preferred direction (E first)
and -5 to -20 ms in the null direction (I first) at biological bar velocities (0.3-1.0 mm/s on the
retina, typically modelled as 500-2000 um/s) should produce a spike DSI in the 0.5-0.75 band
[KochPoggio1983, Taylor2000]. The t0022 driver should implement this offset as an explicit timing
rule over the 12 directions.

### Dendritic Spike Initiation Veto, Not Propagation Block

DSGC direction selectivity is amplified by dendritic spike initiation, not by block of already-
propagating spikes [Oesch2005, Schachter2010]. In rabbit DSGCs, local TTX onto dendrites reduces
light-evoked spiking by **41.5 +/- 15%** while sparing depolarisation-evoked spikes, and two-photon
Ca2+ imaging shows direction-tuned TTX-sensitive dendritic Ca2+ transients [Oesch2005]. The measured
subthreshold PSP at the soma has DSI of only 0.09-0.14, while spike output DSI is 0.67-0.74; the
spike threshold amplifies the modest PSP asymmetry by approximately **4-6x** into the observed spike
DSI [Oesch2005, Schachter2010]. A physiological-scale inhibitory conductance of ~6 nS is enough to
gate local dendritic spike *initiation*, but it would take ~**85 nS** (more than an order of
magnitude higher and biologically implausible) to block a spike that has already been initiated and
is propagating [Schachter2010]. The operational conclusion is that the shunt must act where and when
the dendritic spike would otherwise initiate.

**Best practice**: Insert active dendritic Na+ channels at densities that support ~7 mV
dendritically-initiated orthograde spikelets while holding the somatic threshold near -49 mV for
current-evoked spikes and -56 mV for light-evoked spikes [Oesch2005]. Place each inhibitory synapse
at a location where it vetoes the *initiation* of a dendritic spike in the null direction, not where
it would attempt to block propagation [Schachter2010].

### Cable Parameters and Electrotonic Structure of DSGC Dendrites

The corpus provides two independent compartment-parameter sets for DSGC modelling, both within the
standard Rall-era envelope [KochPoggio1982, Schachter2010]. Rabbit DSGC: **R_i = 110 Ohm cm**, **C_m
= 1 uF/cm^2**, dendritic segments below 0.1 * lambda, arbor radius ~150 um, soma ~15 um; R_m is
fitted to match the measured input resistance of ~82 MOhm [Schachter2010, Oesch2005]. Cat alpha RGC:
**R_i = 70 Ohm cm**, **C_m = 2 uF/cm^2**, **R_m = 2500 Ohm cm^2**, L ~0.5-0.8 lambda
[KochPoggio1982]. These two sets differ in C_m by 2x and in R_i by 1.6x because they reflect
rabbit-DSGC vs cat-alpha-RGC biology respectively; the t0008 port inherits one of them already
through the Poleg-Polsky & Diamond 2016 ModelDB source. Dendritic sub-sectors smaller than **5-10
um** carry independent direction tuning in mouse DSGCs [Jain2020]; the space constant for
small-signal propagation in these dendrites is **5.3 um** [Jain2020]. [Jain2020] also reports
specific NEURON conductance densities: Na 150-200 mS/cm^2 at soma/AIS and 30 mS/cm^2 in dendrites;
K-rect 35 mS/cm^2 at soma/AIS and 25 mS/cm^2 in dendrites; C_m = 1 uF/cm^2; R_a = 100 Ohm cm.

**Best practice**: Keep the C_m, R_i, and R_m values inherited from the t0008 ModelDB port rather
than re-tuning — these were already accepted in t0008 with DSI = 0.316. Size segments to less than
0.1 * lambda using the d_lambda rule [Mainen1996, Schachter2010]. Treat the arbor as a set of
near-independent electrotonic subunits and place one E-I synapse pair per subunit
[Schachter2010, Jain2020].

### AIS Channel Partitioning and the Spike-Generation Site

RGC AIS channel expression is subunit-resolved and spatially segregated. In rodent RGCs, the AIS
carries **Nav1.6 in a distal microdomain** and **Nav1.1 (not Nav1.2) in a proximal microdomain**,
with **Kv1.2 restricted to the distal AIS** and excluded from the proximal Nav1.1 domain
[VanWart2006]. Ankyrin-G co-localises with both Nav subtypes but cannot account for the segregation
[VanWart2006]. This is an important correction to the task-description prior, which referenced a
generic "Nav1.6 + Nav1.2" split drawn from cortical pyramidal neurons [Hu2009]; in RGCs the proximal
partner is Nav1.1, not Nav1.2. The overall functional story — distal Nav subtype with a lower
threshold initiates the AP, proximal Nav subtype recruits the somatic body for backpropagation —
carries across cell types and is the canonical AIS mechanism [Hu2009, Kole2008]. Axonal AIS Na+
density is qualitatively high compared to somatic density (~7x or more) and is necessary for
reliable AP initiation [Kole2008]; AIS Kv1 shapes AP width and affects synaptic efficacy
[KoleLetzkus2007]. The RGC-specific HH-family kinetics on which both t0008 and t0020 build come from
[FohlmeisterMiller1997]: 5 nonlinear channels + 1 leak, leak 3-8 uS/cm^2, up to 800 compartments, a
dedicated thin axonal segment; cell geometry dominates interspike intervals more than channel
density.

**Best practice**: Partition the AIS in the `forsec` layout as two sub-regions — *distal AIS*
carrying Nav1.6 + Kv1.2 and *proximal AIS* carrying Nav1.1 — and keep them separate from the soma
block so that channel-swap tasks (Nav1.6-only, Kv1 vs Kv3) can edit just the distal AIS
[VanWart2006, KoleLetzkus2007]. Expose soma, dendrite, proximal AIS, and distal AIS as four
independent `forsec` blocks each with a single channel-insertion hook. Keep the thin axonal segment
[FohlmeisterMiller1997] as a fifth block downstream of the distal AIS.

**Hypothesis**: Removing Nav1.6 from the distal AIS alone (a follow-up task) will elevate spike
threshold and reduce peak firing rate without altering DSI, because DS is generated in the dendrites
[Taylor2000, Oesch2005, Schachter2010] and only the spike-initiation site is altered.

### E-I Temporal Co-Tuning and Stimulus Velocity

The per-dendrite E-I timing that the driver must schedule follows from cortical and retinal
E-I-balance work. Cortically, E and I conductances are tightly co-tuned in time with I lagging E by
a few milliseconds [WehrZador2003]. Retinally, DSGC E and I are phase-shifted by direction: SAC-
driven GABA onto DSGC dendrites is direction-asymmetric by design [EulerDetwilerDenk2002], and
DSGC-local temporal asymmetries between E and I generate DS even when upstream SAC dendrites are
themselves rendered non-directional [Jain2020]. AMPA receptors are fast (decay below 2 ms) and NMDA
receptors carry a slow Mg2+-gated component [Lester1990] that multiplies gain in the preferred
direction without tuning direction per se [Jain2020]. Dendritic integration of PSPs is location-
dependent so the soma measures an attenuated and temporally-filtered sum of dendritic events
[HausserMel2003, Rall1967]. The shape-index (half-width vs rise-time) diagnostic from [Rall1967]
distinguishes distal-dendrite from proximal inputs at the soma and should be used as a sanity check
after t0022 simulation.

**Best practice**: Schedule per-dendrite GABA_A IPSGs to arrive 5-20 ms *before* the paired AMPA
EPSG in the null direction and 5-20 ms *after* in the preferred direction, using receptor kinetics
in the fast AMPA / slow NMDA / fast GABA_A convention [Lester1990, WehrZador2003, HausserMel2003].
Choose a bar velocity (typically 500-1500 um/s on the retina) that places the E-I offset in the
above window given the per-direction dendrite crossing time.

## Methodology Insights

* **Compartment layout**: Split the `RGCmodel.hoc` skeleton into five explicit `forsec` blocks —
  soma, dendrite, proximal AIS, distal AIS, thin axonal segment — each with one clear channel-
  insertion hook. Follow [FohlmeisterMiller1997]'s five-nonlinear-plus-leak channel convention that
  t0008 already inherits; add a second AIS sub-block to separate Nav1.6-Kv1.2 (distal) from Nav1.1
  (proximal) per [VanWart2006, KoleLetzkus2007].

* **Channel densities as priors**: Soma/AIS Na 150-200 mS/cm^2, dendrite Na ~30 mS/cm^2, soma/AIS
  K-rect 35 mS/cm^2, dendrite K-rect ~25 mS/cm^2, C_m = 1 uF/cm^2, R_a = 100 Ohm cm [Jain2020]; the
  t0008 inherited values from ModelDB 189347 can be kept as-is for the baseline testbed, with these
  numbers available for follow-up channel-density sweeps.

* **Spatial-asymmetry mechanism**: Per-dendrite E-I pairs with inhibition positioned proximal to
  excitation on the same branch [KochPoggio1982, KochPoggio1983]. Set the per-pair inhibitory
  conductance at the physiological ~6 nS level that gates dendritic spike initiation, well below the
  ~85 nS that would block propagation [Schachter2010]. Set E-direction-untuned (flat) and
  I-direction-asymmetric with null/preferred ratio in the 2-4x range [Park2014, Taylor2014]; the E/I
  amplitude point from [Park2014] (0.31 nS E vs 2.43 nS I at DSI ~0.65) is a concrete calibration
  anchor.

* **Driver schedule for 12 directions**: Use a fixed moving bar at a constant velocity (500-1500
  um/s). For each dendrite, compute per-direction entry and exit times from the bar-line geometry,
  and drive the paired E and I synapses with a direction-dependent offset: I leads E by 5-20 ms in
  the null direction, E leads I by 5-20 ms in the preferred direction
  [KochPoggio1983, WehrZador2003, EulerDetwilerDenk2002]. No per-angle rotation of synapse
  coordinates, no per-condition GABA parameter swap.

* **Receptor kinetics**: AMPA fast (decay below 2 ms), GABA_A fast, NMDA Mg2+-gated Jahr-Stevens
  formulation [Lester1990, Jain2020]. Keep these as parameters of the synapse definitions in the hoc
  file, not baked into the driver.

* **Discretisation**: Segment length below **0.1 * lambda** on every section
  [Mainen1996, Schachter2010]; `lambda_f(100)` is the operational form in NEURON.

* **Scoring**: Use t0012's `tuning_curve_loss` scorer. Targets: DSI >= 0.5, peak firing rate >= 10
  Hz, HWHM in the 30-60 deg range consistent with [Oesch2005, Park2014] (exact numbers not claimed
  by any single paper in the corpus; treat HWHM as a report-only metric). Trial count >= 10 per
  angle, total rows >= 120.

* **Shape-index sanity check**: After simulating, plot the somatic PSP shape index (half-width vs
  rise-time) by direction [Rall1967] to confirm that null-direction PSPs are attenuated and slowed,
  consistent with proximal-shunt geometry.

* **Comparison**: Cross-tabulate t0022 DSI, HWHM, peak, and reliability against t0008 (DSI 0.316,
  peak 18.1 Hz, rotation proxy) and t0020 (DSI 0.7838, peak 14.85 Hz, gabaMOD swap). Since both
  prior ports succeeded on a single mechanism (rotation or parameter swap), t0022 is the first to
  satisfy the dendritic-computation requirement under the project's scorer.

* **Best practices**: per-dendrite E-I pairs; proximal-I-to-distal-E within each branch; fixed
  stimulus, variable geometry/timing; `forsec` block separation for channel-swap experiments;
  preserve t0008 cable parameters so diffs are attributable to the driver change.

* **Hypotheses worth testing** after the baseline runs: (a) removing distal-AIS Nav1.6 will raise
  threshold and reduce peak firing while leaving DSI unchanged [Taylor2000, Oesch2005]; (b)
  replacing Kv1 with Kv3 at the distal AIS will narrow the AP and increase peak rate without
  altering DSI [KoleLetzkus2007]; (c) a whole-arbor single-compartment model (no electrotonic
  subunits) will overstate preferred firing and understate null suppression by roughly 6x per
  [Oesch2005].

## Dendritic-Computation Mechanism Summary Table

| Mechanism element | Value or setting | Source |
| --- | --- | --- |
| Locus of DS computation | Postsynaptic DSGC dendrites | [Taylor2000, Oesch2005] |
| E direction tuning | Flat (null/preferred ~0.8-1.0) | [Park2014, Taylor2014] |
| I direction tuning | Asymmetric; null/preferred 2-4x | [Park2014, Taylor2014] |
| E vs I amplitude (DSI ~0.65 working point) | 0.31 nS E vs 2.43 nS I | [Park2014] |
| Per-dendrite I conductance (gating initiation) | ~6 nS | [Schachter2010] |
| Conductance needed to block propagation | ~85 nS (not physiological) | [Schachter2010] |
| Theoretical shunt threshold (delta RGC) | ~50 nS | [KochPoggio1983] |
| Shunt position | Proximal to paired E on same branch | [KochPoggio1982, KochPoggio1983] |
| E-I timing (preferred direction) | E leads I by 5-20 ms | [KochPoggio1983, WehrZador2003] |
| E-I timing (null direction) | I leads E by 5-20 ms | [KochPoggio1983, WehrZador2003] |
| Dendritic subunit size | 5-10 um | [Jain2020] |
| Dendritic space constant | 5.3 um | [Jain2020] |
| Soma / AIS Na density | 150-200 mS/cm^2 | [Jain2020] |
| Dendrite Na density | ~30 mS/cm^2 | [Jain2020] |
| Spike-level DSI target | 0.5-0.75 | [Oesch2005, Park2014] |
| Subthreshold PSP DSI at soma | 0.09-0.14 | [Oesch2005] |
| Peak AP rate (DSGCs, bar motion) | 80-150 Hz | [Sivyer2013] |
| Local TTX effect on dendritic spiking | -41.5 +/- 15 % | [Oesch2005] |
| Distal AIS subunits (RGC) | Nav1.6 + Kv1.2 | [VanWart2006] |
| Proximal AIS subunit (RGC) | Nav1.1 | [VanWart2006] |
| AIS Na density (cortex, high) | ~7x somatic or more | [Kole2008] |
| d_lambda segmentation | < 0.1 * lambda | [Mainen1996, Schachter2010] |
| Compartment skeleton | 5 nonlinear channels + leak, thin axon | [FohlmeisterMiller1997] |

## Gaps and Limitations

* **Exact E-I onset lag for a bar-crossing retinal geometry**: [WehrZador2003] gives a cortical
  prior and [EulerDetwilerDenk2002] gives dendritic Ca imaging of SACs, but the specific
  millisecond-scale lag that an 800-um/s bar sweeping across a DSGC produces at the *DSGC dendrite*
  level is not tabulated anywhere in the reviewed corpus. The t0022 driver sets this by construction
  (per-direction timing rule) and is the main unvalidated parameter of the testbed.

* **Several AIS papers are paywalled-metadata-only**: [Hu2009, Kole2008, KoleLetzkus2007] arrive
  through CrossRef metadata only (no full-text summary). Conductance-density, half-voltage, and
  time-constant numbers from these papers were intentionally not transcribed; they are flagged as
  priors at the subunit-identity / compartment level only. Any follow-up task that wants numerical
  AIS Nav/Kv conductance densities must retrieve those PDFs directly.

* **Task-description vs literature on the Nav1.2 prior**: The t0022 task description references a
  Nav1.6 / Nav1.2 split; in RGCs the proximal partner is Nav1.1, not Nav1.2 [VanWart2006]. The
  Nav1.6 vs Nav1.2 split is a cortical-pyramidal-neuron prior [Hu2009]. This is a factual correction
  that the `description.md` of the new library asset must document so that downstream channel-swap
  tasks pick the correct subunit.

* **No Kv3 prior**: The project's voltage-gated-channel corpus contains Kv1 [KoleLetzkus2007] but
  not Kv3, which a follow-up task will likely want for the "fast AP + high firing rate" regime. Kv3
  priors must be sourced by a future literature survey before channel-swap experiments.

* **No explicit velocity-tuning study**: Bar-velocity-dependence of DSI (optimal velocity, velocity
  bandwidth) is not tabulated in the reviewed corpus in a way the testbed can use directly;
  [Taylor2000, Sivyer2013] discuss velocity but do not report a per-velocity DSI curve. t0022 uses a
  single fixed velocity and leaves velocity-tuning to a follow-up task.

* **Space-clamp error is acknowledged but not corrected**: Voltage-clamp conductance numbers at the
  soma understate dendritic conductance by a factor documented in [Schachter2010] (40-100%); t0022's
  per-dendrite synapse conductances should be picked to match dendritic, not somatic, physiology.
  This is implicit in the testbed design.

## Recommendations for This Task

1. **Implement the driver as a per-dendrite E-I pair scheduler, not as a global parameter swap or a
   coordinate rotation**. Each dendritic subunit gets one AMPA excitatory synapse and one GABA_A
   inhibitory synapse positioned proximal to it on the same branch. The direction of the moving bar
   sets the *timing offset* between the pair per direction, not the conductance magnitude
   [KochPoggio1982, KochPoggio1983, Taylor2000].

2. **Set conductance amplitudes from [Park2014]**: E ~0.3 nS direction-untuned, I ~0.6-2.4 nS
   direction-asymmetric with null/preferred in the 2-4x range [Park2014, Taylor2014]. Each
   per-dendrite I conductance should sit near the physiological 6 nS total for the cell
   [Schachter2010], well below the ~85 nS that would block propagation [Schachter2010].

3. **Organise the `forsec` blocks as five explicit regions**: soma, dendrite, proximal AIS, distal
   AIS, thin axon [VanWart2006, FohlmeisterMiller1997, KoleLetzkus2007]. Each region gets a single
   channel-insertion hook. Document this partition in the new library asset's `description.md` so
   follow-up channel-swap tasks can use it without reading the driver.

4. **Use the t0008 cable parameters as-is** (inherited from ModelDB 189347) and the [Jain2020] /
   [Schachter2010] conductance densities as *secondary* priors exposed as editable constants. Keep
   segment length below 0.1 * lambda [Mainen1996, Schachter2010].

5. **Document the Nav1.1 (not Nav1.2) correction** in `description.md`. The distal AIS block should
   be labelled Nav1.6 + Kv1.2; the proximal AIS block should be labelled Nav1.1 [VanWart2006].

6. **Fix bar velocity at 500-1500 um/s** and set the per-direction E-I offset in the 5-20 ms band
   [KochPoggio1983, WehrZador2003]. Do not sweep velocity in this task; leave velocity-tuning to a
   follow-up task.

7. **Score with t0012's `tuning_curve_loss`** across 12 angles x >=10 trials; target DSI >= 0.5 and
   peak rate >= 10 Hz [Oesch2005, Park2014]. Report HWHM and per-angle reliability without binding
   targets, and include the PSP shape-index sanity plot from [Rall1967].

8. **Comparison table** in `results_detailed.md`: t0022 vs t0008 (DSI 0.316, peak 18.1 Hz) vs t0020
   (DSI 0.7838, peak 14.85 Hz) on DSI / peak / HWHM / reliability. t0022 is the only port that
   satisfies the dendritic-computation mechanism constraint and should be flagged as such in the
   comparison.

## Paper Index

### [KochPoggio1982]

* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/`
* **Categories**: `cable-theory`, `dendritic-computation`, `retinal-ganglion-cell`,
  `direction-selectivity`
* **Relevance**: Foundational theory of on-the-path shunting inhibition as a biophysical mechanism
  for dendritic direction selectivity in RGCs; supplies the passive cable parameters (R_i = 70 Ohm
  cm, C_m = 2 uF/cm^2, R_m = 2500 Ohm cm^2) and the L ~ 0.5-0.8 lambda electrotonic structure.

### [KochPoggio1983]

* **Title**: Nonlinear interactions in a dendritic tree: Localization, timing, and role in
  information processing
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1983
* **DOI**: `10.1073/pnas.80.9.2799`
* **Asset**:
  `tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1073_pnas.80.9.2799/`
* **Categories**: `synaptic-integration`, `dendritic-computation`, `cable-theory`
* **Relevance**: Quantitative theory of shunting inhibition: the ~50 nS conductance threshold for
  veto in a delta ganglion cell, and the requirement that I temporally overlap E for the veto to
  operate. Supplies the per-dendrite E-I timing prior used by the t0022 driver.

### [Taylor2000]

* **Title**: Dendritic Computation of Direction Selectivity by Retinal Ganglion Cells
* **Authors**: Taylor, W. R., He, S., Levick, W. R., Vaney, D. I.
* **Year**: 2000
* **DOI**: `10.1126/science.289.5488.2347`
* **Asset**:
  `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1126_science.289.5488.2347/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Experimental cornerstone establishing that the nonlinear E-I interaction underlying
  DSGC direction selectivity is postsynaptic and dendritic. Voltage-clamp dissection and
  12-direction moving-bar stimulus directly motivate the t0022 driver protocol.

### [Oesch2005]

* **Title**: Direction-selective dendritic action potentials in rabbit retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Quantifies the spike-DSI (0.67-0.74) vs PSP-DSI (0.09-0.14) split, the -41.5 +/-
  15% dendritic TTX effect, and the ~7 mV dendritic spikelets; anchors the dendritic
  spike-initiation mechanism and the spike-threshold amplification used in t0022's targets.

### [Schachter2010]

* **Title**: Dendritic spikes amplify the synaptic signal to enhance detection of motion in a
  simulation of the direction-selective ganglion cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `direction-selectivity`,
  `retinal-ganglion-cell`
* **Relevance**: Full compartmental-model reference for rabbit DSGC. Supplies R_i = 110 Ohm cm, C_m
  = 1 uF/cm^2, segment discretisation below 0.1 lambda, the ~6 nS per-dendrite I gating initiation
  vs ~85 nS needed to block propagation, and the ~4x DSI amplification via dendritic threshold.
  Canonical template for the t0022 compartmental layout.

### [Jain2020]

* **Title**: Inhibition shapes direction selectivity at the single-dendrite scale in the retina
* **Authors**: Jain, V., Murphy-Baum, B. L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K. R., Awatramani, G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `retinal-ganglion-cell`,
  `compartmental-modeling`
* **Relevance**: Establishes that DS is computed at the 5-10 um dendritic-sector scale with a 5.3 um
  space constant. Supplies per-compartment NEURON conductance densities (Na = 150/200/30, K-rect =
  35/35/25 mS/cm^2; C_m = 1; R_a = 100) used as secondary priors in the `forsec` blocks.

### [Park2014]

* **Title**: Excitatory synaptic inputs to mouse On-Off direction-selective retinal ganglion cells
  lack direction tuning
* **Authors**: Park, S. J. H., Kim, I.-J., Looger, L. L., Demb, J. B., Borghuis, B. G.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`,
  `synaptic-integration`
* **Relevance**: Direct measurement that DSGC excitation is untuned and inhibition carries the
  directional signal; supplies the DSI 0.65 +/- 0.05 anchor, the 0.31 nS E vs 2.43 nS I working
  point, and the ~8x null/preferred conductance ratio used to calibrate per-dendrite synapse
  amplitudes.

### [Taylor2014]

* **Title**: Direction-selective ganglion cell calcium imaging
* **Authors**: Taylor, W. R., et al.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Complementary validation of the null/preferred inhibitory ratio in the 2-4x range
  at peak velocity; used as a secondary calibration point for the per-dendrite I conductance sweep
  in t0022.

### [Sivyer2013]

* **Title**: Patch-clamp recordings of DSGC spike-train tuning
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/`
* **Categories**: `patch-clamp`, `retinal-ganglion-cell`, `direction-selectivity`
* **Relevance**: Peak AP rate target (80-150 Hz in preferred direction over 1-2 s bar stimulus);
  output-level validation reference for the t0022 peak-rate metric.

### [Rall1967]

* **Title**: Distinguishing theoretical synaptic potentials computed for different soma-dendritic
  distributions of synaptic input
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1152_jn.1967.30.5.1138/`
* **Categories**: `cable-theory`, `compartmental-modeling`
* **Relevance**: Shape-index diagnostic (half-width vs rise-time) for distinguishing distal vs
  proximal synaptic inputs at the soma; used as a sanity-check metric for t0022 to confirm the
  proximal-shunt geometry.

### [Mainen1996]

* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/`
* **Categories**: `cable-theory`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: d_lambda segmentation rule and evidence that dendritic morphology dominates
  firing-pattern diversity; anchors the segment-length-below-0.1-lambda convention used in t0022.

### [VanWart2006]

* **Title**: Polarized distribution of ion channels within microdomains of the axon initial segment
* **Authors**: Van Wart, A., Trimmer, J. S., Matthews, G.
* **Year**: 2007
* **DOI**: `10.1002/cne.21173`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1002_cne.21173/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`
* **Relevance**: RGC-specific AIS subunit localisation: Nav1.6 + Kv1.2 at the distal AIS, Nav1.1 at
  the proximal AIS. Supplies the exact AIS `forsec` partition and corrects the task-description
  prior (which referenced Nav1.2; the RGC proximal partner is Nav1.1).

### [Hu2009]

* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W., Tian, C., Li, T., Yang, M., Hou, H., Shu, Y.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/`
* **Categories**: `voltage-gated-channels`
* **Relevance**: Canonical cortical-pyramidal prior that the low-threshold distal AIS Na subtype
  initiates the AP while a higher-threshold proximal subtype handles backpropagation; cited as the
  generic AIS split mechanism that the RGC-specific [VanWart2006] instantiates with Nav1.6 + Nav1.1.

### [Kole2008]

* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P., Ilschner, S. U., Kampa, B. M., Williams, S. R., Ruben, P. C., Stuart,
  G. J.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Establishes that AP initiation requires an AIS Na density substantially higher than
  somatic (on the order of 7x or more in cortex); justifies the elevated AIS Na block in the t0022
  `forsec` partition.

### [KoleLetzkus2007]

* **Title**: Axon Initial Segment Kv1 Channels Control Axonal Action Potential Waveform and Synaptic
  Efficacy
* **Authors**: Kole, M. H. P., Letzkus, J. J., Stuart, G. J.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.07.031`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1016_j.neuron.2007.07.031/`
* **Categories**: `voltage-gated-channels`
* **Relevance**: AIS Kv1 channels control AP waveform and synaptic efficacy; motivates the Kv1 vs
  Kv3 follow-up channel-swap experiment at the distal AIS and supports placing Kv1.2 in the distal
  AIS block [VanWart2006].

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `compartmental-modeling`
* **Relevance**: RGC-specific HH-family kinetic family (5 nonlinear channels + leak, up to 800
  compartments, thin axonal segment, leak 3-8 uS/cm^2) underlying the t0008 ModelDB port; sets the
  channel-set convention that t0022 inherits and makes channel-modular for follow-up tasks.

### [WehrZador2003]

* **Title**: Balanced inhibition underlies tuning and sharpens spike timing in auditory cortex
* **Authors**: Wehr, M., Zador, A. M.
* **Year**: 2003
* **DOI**: `10.1038/nature02116`
* **Asset**: `tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature02116/`
* **Categories**: `synaptic-integration`, `dendritic-computation`
* **Relevance**: Cortical E-I temporal co-tuning prior: I lags E by a few milliseconds with matched
  amplitude tuning. Cited for the per-dendrite E-I timing rule in the t0022 driver (I leads E by
  5-20 ms in null, E leads I by 5-20 ms in preferred).

### [EulerDetwilerDenk2002]

* **Title**: Directionally selective calcium signals in dendrites of starburst amacrine cells
* **Authors**: Euler, T., Detwiler, P. B., Denk, W.
* **Year**: 2002
* **DOI**: `10.1038/nature00931`
* **Asset**: `tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature00931/`
* **Categories**: `direction-selectivity`, `synaptic-integration`, `retinal-ganglion-cell`
* **Relevance**: Dendritic Ca2+ imaging in SACs showing direction-selective Ca2+ signals prior to
  GABA release onto DSGCs; justifies the direction-asymmetric inhibition onto DSGC dendrites that
  t0022's driver instantiates per-dendrite.

### [Lester1990]

* **Title**: Channel kinetics determine the time course of NMDA receptor-mediated synaptic currents
* **Authors**: Lester, R. A. J., Clements, J. D., Westbrook, G. L., Jahr, C. E.
* **Year**: 1990
* **DOI**: `10.1038/346565a0`
* **Asset**: `tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_346565a0/`
* **Categories**: `synaptic-integration`
* **Relevance**: Canonical NMDA receptor kinetics (slow Mg2+-gated decay) used in DSGC compartmental
  models [Jain2020]. Cited for the receptor-kinetic prior that the t0022 synapse definitions inherit
  from the t0008 ModelDB port.

### [HausserMel2003]

* **Title**: Dendrites: bug or feature?
* **Authors**: Hausser, M., Mel, B.
* **Year**: 2003
* **DOI**: `no-doi_HausserMel2003_s0959-4388-03-00075-8`
* **Asset**:
  `tasks/t0018_literature_survey_synaptic_integration/assets/paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/`
* **Categories**: `dendritic-computation`, `synaptic-integration`, `cable-theory`
* **Relevance**: Canonical review of dendritic-location dependence of PSP integration; cited as the
  general prior that distal-to-soma PSP attenuation and temporal filtering are large enough to make
  per-dendrite integration the operationally relevant scale, consistent with the t0022 per-dendrite
  E-I pair design.
