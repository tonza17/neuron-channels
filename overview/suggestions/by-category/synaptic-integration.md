# Suggestions: `synaptic-integration`

60 suggestion(s) in category
[`synaptic-integration`](../../../meta/categories/synaptic-integration/) **50 open** (13 high,
34 medium, 3 low), **10 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>🧪 <strong>AMPA per-synapse conductance sweep on t0052 minimal DSGC to close
the 30-150x peak-rate gap</strong> (S-0052-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0052 hits primary DSI 1.0 but peak rate is only 0.667 Hz, ~22x below the t0004 target (30 Hz)
and 30-150x below the in vivo / in vitro DSGC range (30-100 Hz, Park2014 / PolegPolsky2016).
The current AMPA conductance is 0.5 nS x 100 synapses (AMPA-only by design) and the cell is
locked in a single-spike-per-trial regime that makes DSI = 1.0 trivially. Sweep the
per-synapse AMPA peak conductance over {0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0} nS at fixed synapse
count and gabaMOD design, re-run the 12-direction x 10-trial FULL sweep, and report peak Hz,
vector-sum DSI, HWHM, and reliability per gAMPA. Goal: locate the gAMPA where peak rate enters
the 30-100 Hz band and the cell leaves the binary on/off regime, so DSI dynamics become
biologically informative. Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Conductance-matched t0052 vs t0053 comparison at fixed mean GABA
mass per trial</strong> (S-0053-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

S-0052-04 proposes a t0052 vs t0053 side-by-side comparison at matched placement, but does not
control for total GABA mass (t0052 = 66 nS mean / trial, t0053 = 100 nS mean / trial; 1.5x
difference fully accounts for t0053's flat-zero result). Run a dedicated comparative task at
conductance-matched mean GABA mass: e.g., t0052 standard gabaMOD (66 nS) vs t0053 at 1.32 nS x
50 active = 66 nS, or matched at 100 nS. Use placement_seed0.json shared between tasks. Report
all six output classes (V(t), EPSP, IPSP, PSTH, tuning curve, active-fraction) plus
per-direction trial-for-trial diffs in soma V(t). Goal: isolate the spatial-vs-amplitude
mechanism contribution to DSI from the GABA-mass confound, settling the graded-vs-binary
question at matched mean drive. Recommended task types: comparative-analysis.

</details>

<details>
<summary>📊 <strong>Cross-comparison task: t0052 (scalar gabaMOD) vs t0053 (spatial
PD/ND-asymmetric inhibition) once t0053 finishes</strong> (S-0052-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0053 (not_started, dependencies = same morphology + library-asset substrate as t0052)
implements spatial PD/ND-asymmetric SAC inhibition rather than scalar gabaMOD. Once t0053 is
completed, run a comparison task that side-by-side analyses the two minimal DSGCs at matched
100 E + 100 I synapse counts: peak Hz, primary and vector-sum DSI, HWHM, reliability, ND/PD
IPSP voltage ratio, ND/PD IPSP conductance ratio (where applicable), per-direction soma V(t)
overlays, and polar tuning overlays. Use the same placement seed (PLACEMENT_SEED = 0, recorded
in tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json) so synapse placement is
exactly matched. Goal: quantify the DS / firing-rate / IPSP-saturation differences
attributable to the inhibition-mechanism choice (scalar mod vs spatial asymmetry) on an
otherwise identical from-scratch substrate. Recommended task types: comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Excitation-side sensitivity sweep under gabaMOD-swap to close
the 25 Hz peak-firing-rate gap</strong> (S-0020-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Under the native gabaMOD-swap protocol, DSI (0.7838) sits inside the [0.70, 0.85] envelope but
PD peak (14.85 Hz) is 25.15 Hz below the 40 Hz floor. Protocol is now ruled out, so the
shortfall must live on the excitation side. Run a factorial sweep over (a) BIP synapse count
{88, 177, 354}, (b) excMOD on AMPA+NMDA in {0.5, 1.0, 1.5, 2.0, 3.0}, (c) stimulus drive
{baseline, +50%, +100%}, holding gabaMOD at the 0.33/0.99 PD/ND pair. Report the smallest
config shift that moves peak into [40, 80] Hz without dragging DSI outside [0.70, 0.85].
Distinct from S-0008-04 (sweeps all parameters including GABA side under the rotation-proxy
protocol); this is excitation-only under the native driver, addressable only now that t0020
localised the gap. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>GABA-synapse-count sweep on t0052 to characterise driving-force
saturation of scalar gabaMOD IPSPs</strong> (S-0052-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0052_minimal_dsgc_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

The headline secondary finding of t0052 is that the somatic IPSP voltage ratio (1.54x)
substantially under-predicts the gabaMOD conductance ratio (3.0x) because driving force (V -
E_GABA) saturates as ~100 GABA synapses fire near-synchronously and local Vm approaches E_GABA
= -75 mV. Characterise this saturation curve by sweeping the number of GABA synapses N_I in
{10, 25, 50, 75, 100, 150, 200, 300} at fixed per-synapse peak (2 nS) and fixed gabaMOD(theta)
design, holding 100 AMPA synapses constant. Report somatic IPSP voltage ratio (gNULL_voltage /
gPD_voltage), peak / null PSP magnitudes, primary and vector-sum DSI, and peak Hz per N_I.
Goal: produce a quantitative voltage-vs-conductance saturation curve that future
scalar-gabaMOD models can use to translate nominal conductance ratios into expected somatic
suppression. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Hand-port deRosenroll2026 ds-circuit-ei model and remap 8-angle
grid to 12 angles</strong> (S-0010-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Port geoffder/ds-circuit-ei-microarchitecture (Zenodo 10.5281/zenodo.17666157, MIT LICENSE).
Requires adding statsmodels, h5py, fastparquet, oiffile as optional deps (or extracting a
minimal driver subset without them), then extending the hardcoded 8-direction ANGLES_DEG list
to the canonical 12-angle protocol before scoring. t0010 exited at P2 within the 90-min cap;
budget 4-6 hours for full P3.

</details>

<details>
<summary>🧪 <strong>Implement AMPA + NMDA + GABA_A synapses with E-I temporal
co-tuning and SAC-to-DSGC asymmetric inhibition in downstream DSGC
model</strong> (S-0018-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The answer asset synaptic-integration-priors-for-dsgc-modelling produces a 6-point
specification for DSGC synaptic integration in NEURON extending the space-clamp/AIS/NMDAR
constraints from t0017. The downstream DSGC compartmental-model build task must implement: (1)
AMPA with dual-exponential kinetics (tau_rise 0.2-0.4 ms, tau_decay 1-3 ms) and NMDA with
Mg2+-block + tau_decay 100-200 ms at 32 degC on glutamatergic inputs, (2) GABA_A with shunting
(reversal near resting Vm) and tau_decay 5-20 ms on SAC inputs, (3) E->I temporal lag of 15-50
ms on preferred-direction stimuli reproducing Wehr & Zador 2003 co-tuning, (4) asymmetric
GABAergic inputs that are strong on null-side dendrites (to match Euler-Detwiler-Denk 2002 SAC
Ca2+ DS index 0.3-0.5) and weak on preferred-side dendrites, (5) dendritic-location-dependent
EPSP attenuation consistent with Hausser-Mel lambda_DC 100-300 um, (6) named fitting
objectives for DSI under shunting-inhibition block (should drop toward 0) and EPSP/IPSP charge
balance during null-direction motion.

</details>

<details>
<summary>🧪 <strong>Joint (gAMPA, gNMDA, gGABA) conductance sweep on t0054 minimal
architecture to locate a DSI-preserving operating point</strong>
(S-0054-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0054 fixed AMPA at 0.5 nS and used the unchanged t0052 scalar gabaMOD (2 nS base, ratio 3.0),
varying only gNMDA. The DSI collapse may be recoverable by rebalancing the three conductances
jointly. Run a 3-D grid: gAMPA in {0.25, 0.5, 1.0} nS, gNMDA in {0.0, 0.1, 0.25, 0.5} nS, base
gGABA in {2, 4, 8, 16} nS, all on the t0054 codebase with placement seed 0 unchanged,
voltage-independent NMDA kept (so this is the no-Mg-block control complementary to S-0054-01).
Use 12 dirs x 5 trials per cell = 60 trials per (gAMPA, gNMDA, gGABA) point; 48 grid cells =
2880 trials. Apply early stop on cells where E_ONLY peak Hz > 30 Hz to prune the saturated
subgrid. Pass criterion: locate at least one (gAMPA, gNMDA, gGABA) triple with vector-sum DSI
>= 0.5 and peak Hz in 10-50 Hz, or rule out such an operating point in the voltage-independent
regime. Recommended task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Port the full upstream SacNetwork with bp_locs/probs/deltas to
reproduce the deRosenroll correlation-drop effect</strong> (S-0024-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-01` |
| **Kind** | technique |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The t0024 port misses REQ-5 on all three sub-criteria (corr DSI 0.82 vs paper target
[0.30,0.50]; uncorr DSI 0.84 vs [0.18,0.35]; drop fraction 0.000 vs >=0.20) because the AR(2)
correlation was applied at per-terminal Exp2Syn drivers rather than across the
spatially-distributed SAC varicosity release network that the paper identifies as the causal
substrate. Port the upstream SacNetwork class (bp_locs, probs, deltas) from
geoffder/ds-circuit-ei-microarchitecture into a new sibling library asset, drive the same
cell, and rerun the 8-direction correlated/uncorrelated sweep. Target: reproduce the ~0.39 ->
~0.25 DSI drop.

</details>

<details>
<summary>📊 <strong>Reproduce Poleg-Polsky 2016 Fig 1D/H subthreshold validation
targets (PSP amplitude, NMDAR slope angle)</strong> (S-0020-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

compare_literature.md flags that the paper reports concrete subthreshold validation targets
that this task did not measure: PD NMDAR-mediated PSP component 5.8 +/- 3.1 mV and ND 3.3 +/-
2.8 mV (Fig 1D, n=19), and NMDAR multiplicative scaling slope angle 62.5 +/- 14.2 deg (Fig 1H,
additive baseline 45 deg). Extend the gabaMOD-swap driver to record somatic whole-cell voltage
traces (v_soma, not just spike count) across the 40-trial sweep, compute (1) the peak PSP
amplitude in a 0-200 ms post-stimulus window per condition and (2) the slope-angle regression
over a scan of AMPA vs NMDA drive ratios, then gate each against the paper's n=19 mean +/- SD
intervals. This turns a single spike-output check into a multi-level subthreshold validation
that exercises the cell's passive and NMDA-block biophysics independently of spike
thresholding. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Root-cause the 282-vs-177 synapse-count discrepancy in ModelDB
189347 vs Poleg-Polsky 2016 paper text</strong> (S-0046-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Inspect `RGCmodel.hoc`'s ON/OFF cut plane (`z >= -0.16 * y + 46`) and `placeBIP()` to
determine why the deposited code instantiates 282 BIP/SACinhib/SACexc terminals when the paper
Methods text states 177 synapses. Test alternative cut-plane thresholds, density-based
sub-sampling, or supplementary-text geometry rules to find a code configuration that matches
the paper count. The 1.6x synapse overcount is the leading mechanistic hypothesis for the ~4x
PSP amplitude inflation observed in t0046 (PD PSP 23.25 mV vs paper 5.8 +/- 3.1 mV);
reconciling the count is a prerequisite for a quantitatively faithful Fig 1 reproduction.
Recommended task types: experiment-run, code-reproduction.

</details>

<details>
<summary>🧪 <strong>Stricter centripetal-gating threshold sweep (cos < -0.5, -0.7) to
halve active-fraction on t0053</strong> (S-0053-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0053's centripetal-gating rule fires every I synapse whose centrifugal vector is anywhere on
the bar-incoming hemisphere (cos(theta_stim - theta_centrifugal) < 0), giving a roughly 50%
active fraction averaged over directions and a 0.34-0.66 per-direction spread. With 2 nS GABA
per active synapse this is enough to fully suppress spiking. Tighten the threshold to T in
{-0.3, -0.5, -0.7, -0.866} so only synapses whose centrifugal vector is within (90 - acos|T|)
of being directly anti-aligned with the bar fire. T = -0.5 reduces mean active fraction to
~0.33; T = -0.866 to ~0.17. Re-run the 12-direction x 10-trial FULL sweep at fixed 2 nS GABA
per synapse and report peak Hz, DSI, HWHM, active-fraction polar curve, and aggregate IPSP per
T. Goal: test whether a stricter threshold recovers a measurable DSI without changing
per-synapse conductance, isolating the active-fraction-vs-amplitude contributions to
suppression. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Swap bipolar-cell sustained vs transient kinetics on t0024 to
discriminate kinetic tiling from cable delay</strong> (S-0027-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Run t0024 (de Rosenroll 2026 port) with bipolar-cell kinetic identities swapped: assign
sustained kinetics to distal terminals and transient kinetics to proximal terminals, opposite
to the wild-type tiling. Prediction (creative_thinking.md #2): if [Srivastava2022]
kinetic-tiling is causally responsible for SAC DS, the swap reverses preferred direction; if
[Kim2014] cable delay is causal, the swap only reduces DSI magnitude without flipping
preferred direction. Critical for choosing between two competing centrifugal-DS mechanisms
before committing to a morphology sweep design.

</details>

## Medium Priority

<details>
<summary>📚 <strong>Add a Starburst Amacrine Cell feedforward layer to drive
inhibition physiologically</strong> (S-0022-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-04` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1038_nature00931`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1038_nature00931/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 driver schedules GABA directly onto each DSGC dendrite, skipping the SAC (Starburst
Amacrine Cell) layer that shapes DS inhibition in vivo (Euler-Detwiler-Denk 2002). Extend the
modeldb_189347_dsgc_dendritic library with a configurable SAC layer: an array of simplified
SAC models (single-compartment or 2-compartment) whose dendritic output drives DSGC GABA
synapses via NetCon, with SAC dendrites themselves direction-tuned per Euler2002. Expected
outcome: DSI becomes graded rather than saturated (real SAC output is not a hard half-plane
step) and peak firing rate may rise because SAC inhibition is timed to bar arrival not to a
global half-plane rule. This is a library extension not just a channel swap; produces a fourth
DSGC library asset modeldb_189347_dsgc_sac. Dependencies: t0022 library asset, Euler2002
paper. Effort ~40 hours. Recommended task type: write-library, code-reproduction.

</details>

<details>
<summary>📚 <strong>Add an iMK801 analogue MOD modification (selective dendritic
NMDAR block) to enable Fig 8 AP5 reproduction</strong> (S-0046-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-03` |
| **Kind** | library |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Author a new MOD mechanism (or extend `bipolarNMDA.mod`) that selectively blocks NMDAR
conductance in dendritic compartments while leaving somatic NMDAR + AMPA intact, mirroring the
paper's intracellular MK801 (iMK801) protocol. The current AP5 analogue used in t0046
(`b2gnmda = 0`) removes ALL NMDAR contribution and silences the cell entirely (DSI = 0 under
AP5); the paper's iMK801 leaves PD spiking, allowing the qualitative 'DSI preserved under AP5'
Fig 8 claim to be reproduced. This unblocks a faithful Fig 8 AP5 reproduction and resolves the
AP5-vs-iMK801 mechanistic divergence catalogued as discrepancy 1 of 12 in t0046's audit.
Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>AMPA conductance scan at Voff_bipNMDA=1 as a secondary check
on the residual DSI gap</strong> (S-0048-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Complementary to S-0048-01's GABA scan: re-run the same 7-point gNMDA sweep at exptype=2 with
the AMPA conductance scaled across {1.0, 0.5, 0.25, 0.125} of the deposited b2gampa = 0.25 nS
value. t0048's per-class conductance comparison shows AMPA summed conductance is similar
between PD/ND (~11 nS each), so AMPA changes alone cannot create direction selectivity, but
lowering AMPA at fixed GABA could shift the AMPA/GABA balance enough to amplify whatever
residual selectivity GABA provides. This is an essential negative control for S-0048-01: if
AMPA reduction matches GABA reduction in DSI effect, the gap is symmetric and not purely GABA.
4 trials per direction x 7 gNMDA x 4 AMPA scales = 224 trials, ~30 min CPU. Recommended task
types: experiment-run.

</details>

<details>
<summary>🧪 <strong>AR(2) rho sweep at t0024 baseline morphology to isolate
stochastic-release smoothing from cable biophysics</strong> (S-0034-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Creative-thinking (alternative 5) proposed that AR(2)-correlated release with rho=0.6
temporally smooths the null-direction noise floor, potentially contributing to the observed
primary-DSI non-monotonicity independently of cable filtering. This hypothesis must be ruled
in or out before the cable-filtering interpretation is credible. Run the 12-direction x
10-trial protocol on t0024 at baseline morphology (length=1.0x, diameter=1.0x) with rho in
{0.0, 0.3, 0.6, 0.9} (four points) and compare primary-DSI, vector-sum DSI, null Hz, and HWHM
trajectories. If DSI is flat across rho, stochastic-release smoothing is not the driver; if
DSI varies with rho, the effect is release-noise-mediated. Distinct from S-0026-02 (which
crosses rho with V_rest to disambiguate noise vs depolarisation) because this sweeps rho at
fixed V_rest and fixed morphology to isolate the release-noise-vs-cable-biophysics axis.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Diagnose and fix t0022's 15 Hz peak-firing cap (inherited
AMPA-only drive issue)</strong> (S-0039-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Peak firing at the preferred direction is 15 Hz across the diameter sweep, well below
Schachter2010's 40-80 Hz baseline. The same 15 Hz ceiling appeared in t0030 at 12 nS GABA, so
it is a pre-existing t0022 drive issue, not a diameter or GABA artefact. Duplicate of
S-0037-04 but now blocking quantitative literature comparisons for the discriminator task too.
Likely fix: add NMDA back into the E-I schedule, or boost AMPA conductance, or both. Run a
diagnostic trace of soma voltage at preferred direction and compare to Schachter2010's
published traces.

</details>

<details>
<summary>🧪 <strong>Diagnose and fix the low peak firing rate in t0022 (15 Hz vs
40-80 Hz Schachter2010)</strong> (S-0037-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

At the 4 nS sweet spot the preferred-direction peak firing is 15 Hz, an order of magnitude
below Schachter2010's 40-80 Hz baseline. The same low rate was observed in t0030 at 12 nS
GABA, so this is a pre-existing t0022 drive issue (likely the AMPA-only schedule lacking NMDA
or compensatory excitation), not a GABA ladder artefact. A task should add NMDA back into the
t0022 E-I schedule (or increase AMPA gain) and verify peak firing reaches 40+ Hz without
re-pinning DSI. Until this is fixed, any cross-testbed peak-rate comparison is invalid.

</details>

<details>
<summary>📂 <strong>Download the four discovered papers not included in the 20-paper
budget (Sivyer2017, Euler2002, Enciso2010, Webvision)</strong> (S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

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
<summary>📚 <strong>Driving-force-corrected gabaMOD: calibrate conductance ratio to
target somatic-voltage IPSP modulation depth</strong> (S-0052-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-05` |
| **Kind** | library |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0052 establishes that scalar gabaMOD models systematically over-promise somatic IPSP
suppression: the nominal conductance ratio 3.0x (gabaMOD(180)/gabaMOD(0)) produces only a
1.54x somatic IPSP voltage ratio under realistic 100-synapse crowding, because driving force
(V - E_GABA) saturates locally. Define and document a corrected `gabaMOD_eff(theta)` whose
conductance ratio is calibrated to produce the intended somatic-voltage IPSP modulation depth
(e.g., 3.0x somatic IPSP requires ~5-7x conductance ratio under crowding). Add a small library
helper that, given target voltage modulation depth and synapse count, returns the calibrated
gabaMOD curve via a one-time calibration run on the placement, and recommends using that curve
in downstream tasks (this would be applied via correction overlay or as a successor library
asset). Goal: future scalar-gabaMOD reports do not silently confuse conductance modulation
with voltage modulation. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Extend synaptic-integration survey with DSGC-specific
receptor-kinetic, dynamic-clamp, and connectomic SAC-DSGC papers</strong>
(S-0018-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The scaled-down 5-paper survey covers the five canonical themes (AMPA/NMDA/GABA kinetics,
shunting inhibition, E-I balance, dendritic-location integration, SAC-to-DSGC asymmetry) but
with one paper per theme, selected from the most-cited classical literature. A follow-up
survey task should add ~5 DSGC-targeted papers across: (a) modern DSGC-specific AMPA and NMDA
kinetic measurements at near-physiological temperature, (b) DSGC dynamic-clamp studies that
inject measured conductance waveforms, (c) connectomic reconstructions of SAC-to-DSGC wiring
(Briggman et al. 2011, Kim et al. 2014), (d) recent E-I temporal co-tuning studies in retina
(rather than auditory cortex), and (e) DSGC dendritic computation (Oesch, Euler, Taylor,
Sivyer). This closes the gap between canonical theory and DSGC-specific parameters.

</details>

<details>
<summary>📚 <strong>Extract the t0022 GABA-override monkey-patch into a reusable
library asset for downstream tasks</strong> (S-0036-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-04` |
| **Kind** | library |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0036 introduced code/gaba_override.py which monkey-patches
_t0022_constants.GABA_CONDUCTANCE_NULL_NS at import time and re-binds the local name inside
trial_runner_diameter.py so the schedule_ei_onsets ratio is computed against the overridden
value. This pattern is immediately needed for S-0036-01 (further null-GABA reductions) and
S-0036-02 (GABA-AMPA timing offset). Rather than each task reimplementing the monkey-patch,
lift it into a library asset (working name: dsgc_t0022_schedule_overrides) exposing a typed
context-manager or setup function accepting gaba_null_ns, gaba_preferred_ns,
gaba_to_ampa_lead_ms, returning a provenance dict logged at task start. Ships a smoke test
asserting the override survived a fresh import and that the null/preferred ratio matches the
requested value. Distinct from S-0033-06 (DSI objective evaluator) which wraps the scoring
side - this wraps the schedule-parameter side. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>GABA conductance scan at Voff_bipNMDA=1 to close the residual
DSI gap to paper's 0.30 line</strong> (S-0048-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0048 confirmed that switching to voltage-independent NMDA (exptype=2) flattens the DSI vs
gNMDA curve to 0.04-0.10 but never reaches the paper's claimed flat ~0.30. The residual gap
must come from non-NMDA mechanisms; the leading candidate is GABA, where t0047 measured
deposited PD ~106 / ND ~216 nS summed conductance vs paper's PD ~12.5 / ND ~30 nS (8x over) at
gNMDA = 0.5 nS. Run a parameter sweep at exptype=2 over a GABA scale factor in {1.0, 0.5,
0.25, 0.125, 0.06} (ratios chosen to bracket paper's 12.5x reduction toward biological values)
at the same 7 gNMDA grid points x 4 trials per direction used here. Track DSI vs (gNMDA, GABA
scale) and report whether any GABA setting produces flat DSI ~0.30 across the gNMDA range.
Pass criterion: identify a GABA scale (if any) that simultaneously satisfies the H1
range/slope thresholds and a mean-DSI > 0.20 target. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA conductance scan under SEClamp toward paper PD 12.5 / ND
30 nS at fixed gNMDA = 0.5 nS</strong> (S-0049-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0049-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0049_seclamp_cond_remeasure/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

SEClamp at -65 mV yielded GABA PD = 47.47 / ND = 48.04 nS vs paper's 12.5 / 30 nS. Run a
`gabaMOD` (or per-synapse GABA) scan under SEClamp at gNMDA = 0.5 nS, exptype = control, with
multiplier values across {1.0, 0.5, 0.25, 0.125} of the deposited base, and additionally test
introducing PD/ND spatial asymmetry (e.g., scale ND-side GABA up by 2-3x and PD-side GABA
down) to see whether the paper's ND-bias DSI -0.41 is recoverable by a spatial redistribution
at the soma. Distinct from S-0048-01 which scans GABA at exptype = 2 across a gNMDA sweep
without SEClamp; this task uses SEClamp modality at single gNMDA. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA-to-AMPA timing offset sweep on t0022 diameter testbed to
test timing-dominates-conductance hypothesis</strong> (S-0036-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0036's creative_thinking cited 'timing dominates conductance' as the second-leading
explanation for why halving null-GABA from 12 nS to 6 nS did not unpin null firing: the t0022
schedule delivers GABA 10 ms BEFORE AMPA on null trials, and the integrated kinetic profile
(not the peak) may clamp the distal membrane below Nav threshold for the whole AMPA window.
Sweep the GABA-leads-AMPA offset across {10 ms (default), 5 ms, 0 ms, -5 ms (AMPA leads GABA)}
at two fixed GABA conductances (12 nS baseline and 6 nS) at diameter 1.0x only (12 angles x 10
trials x 4 offsets x 2 GABA = 960 trials, ~35 min CPU). Primary outcome: find the offset at
which null firing first exceeds 0.1 Hz, isolating timing as an independent rescue axis
orthogonal to S-0036-01's conductance axis. Distinct from S-0030-02 (Poisson) and S-0036-01
(conductance) - this targets the GABA-AMPA offset specifically. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA/AMPA density ratio scan at fixed 3-5x null/preferred IPSC
asymmetry</strong> (S-0002-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

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
<summary>🔧 <strong>Hybrid spatial-gating + amplitude-scaling inhibition mechanism
on minimal DSGC</strong> (S-0053-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-05` |
| **Kind** | technique |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0053_minimal_dsgc_spatial_gaba/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0052 scales all 100 I synapses by a graded gabaMOD(theta); t0053 binary-gates a subset at
full amplitude. A biologically motivated hybrid gates which I synapses fire (t0053's
per-synapse centripetal threshold) AND scales their amplitude by a global gabaMOD(theta)
factor (t0052's amplitude curve). This decomposition matches the SAC network's
centrifugal-release preference (spatial gating) layered on top of any global drive modulation.
Build a variant library `minimal_dsgc_hybrid_gaba` implementing both rules, sweep the gabaMOD
amplitude floor in {0.33, 0.5, 0.66, 1.0} at fixed centripetal threshold cos < 0, and report
DSI, peak Hz, HWHM, IPSP modulation, and active-fraction per floor. Goal: test whether
combining the two mechanisms produces a tuning curve closer to Park2014 / deRosenroll2026
bands than either alone. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>Inject Poisson background rate on the t0022 driver to moderate
DSI from 1.0 toward the 0.5-0.8 published band</strong> (S-0022-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1016_j.neuron.2005.06.036`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1016_j.neuron.2005.06.036/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 NetStim burst driver uses noise = 0 and baseline synapses are silenced, so DSI
saturates at 1.0 across all 60 null-direction trials. Park2014, Oesch2005, and Poleg-Polsky &
Diamond 2016 all report DSI in the 0.5-0.8 range because real DSGCs have 2-5 Hz per-trial
spike jitter from stochastic bipolar release. Extend the driver with a configurable background
Poisson process (1, 2, 3, 5 Hz baseline rate on all synapses) and rerun the 12-angle x
10-trial sweep at each noise level. Expected outcome: DSI curve drops from 1.0 to ~0.8 at 2 Hz
bg to ~0.6 at 5 Hz bg, bracketing the literature envelope, with per-angle std rising from 0 Hz
to ~2-4 Hz matching Schachter2010 trial-to-trial variability. Dependencies: t0022 library
asset. Effort ~8 hours. Recommended task type: experiment-run.

</details>

<details>
<summary>🧪 <strong>Intermediate-gabaMOD sensitivity sweep to map the PD-ND
transition curve</strong> (S-0020-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The canonical protocol uses only the two endpoints gabaMOD = 0.33 (PD) and 0.99 (ND).
Task_description Scope explicitly deferred intermediate values as follow-up work. Run 20
trials per condition at gabaMOD in {0.20, 0.33, 0.50, 0.66, 0.83, 0.99} and plot firing rate
vs gabaMOD plus DSI computed as (rate_at_0.33 - rate_at_X)/(rate_at_0.33 + rate_at_X).
Outputs: (1) a firing-rate-vs-gabaMOD curve that shows whether the 0.33 -> 0.99 transition is
sigmoidal, threshold-like, or linear; (2) the critical gabaMOD value at which DSI crosses 0.5
(useful for later calibration); (3) a CSV with schema (gabamod, trial_seed, firing_rate_hz).
Probes whether the paper's two-point choice lies on a plateau or a steep-response region of
the inhibition axis, directly informing the inhibition-strength free parameter for later
optimisation. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Joint (GABA, diameter) sweep to separate passive filtering from
GABA-suppressed active amplification</strong> (S-0039-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0022 shows passive_filtering at 4 nS. Two explanations: (a) t0022 lacks active machinery, or
(b) 4 nS GABA shunts regenerative events that would otherwise produce Schachter2010
concave-down. A joint sweep GABA in {5, 4, 3, 2} x D in {0.5, 1.0, 2.0} = 12 conditions x 12
angles x 10 trials = 1440 trials (~60 min) would distinguish: if lower-GABA runs produce
concave-down curves, mechanism (b) is right; if all GABA levels show passive signatures,
mechanism (a) is right.

</details>

<details>
<summary>🧪 <strong>Localise the GABA unpinning threshold with a fine sweep (5.0,
4.5, 4.0, 3.5, 3.0 nS)</strong> (S-0037-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The current sweep places the unpinning threshold between 6 nS (t0036 pinned) and 4 nS (t0037
unpinned). A 0.5 nS-spaced sweep over {5.0, 4.5, 4.0, 3.5, 3.0} nS at baseline diameter on
t0022 (5 levels x 12 angles x 10 trials = 600 trials, ~20 min local CPU) would localise the
threshold to within 0.5 nS and reveal whether the DSI vs GABA curve is sharp or gradual.
Important for characterising how fragile the operational window really is.

</details>

<details>
<summary>🧪 <strong>NMDA decay-time tau2 sweep at fixed gNMDA on t0054 to disentangle
conductance amplitude from kinetic time constant</strong> (S-0054-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0054 fixed NMDA tau2 at 80 ms and varied only gNMDA, conflating conductance amplitude with
kinetic time constant. Biological NMDA decay tau spans 50-200 ms across DSGC literature
(PolegPolsky2016 reports tau1NMDA = 50 ms; t0018 cites 100-200 ms). Hold gNMDA fixed at 0.25
nS (the 12x peak-rate-boost point) and sweep tau2 in {30, 60, 80, 120, 200} ms x 12 directions
x 10 trials x 2 modes (FULL, E_ONLY) = 1200 trials, on the t0054 minimal architecture with
placement seed 0, voltage-independent NMDA kept. Report per-tau2 EPSP decay tau (using the
improved metric from S-0054-03), peak Hz, and vector-sum DSI. Pass criterion: identify whether
tau2 alone (independent of gNMDA) drives the DSI collapse, or whether the collapse is
dominated by gNMDA. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>NMDA multiplicative-gain ablation to isolate its contribution
to DSI</strong> (S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

PolegPolsky2016 reports that NMDA receptors multiplicatively scale excitatory drive by ~2x and
sharpen directional discrimination, but the survey did not find a published ablation that
isolates the NMDA contribution independently of the AMPA+GABA core. Run three configurations
on the reproduced DSGC baseline (AMPA+GABA only, AMPA+GABA+NMDA with PolegPolsky2016 NMDA
parameters, AMPA+GABA+NMDA with NMDA_gain swept 1-4x) and report the DSI, peak rate, and HWHM
trajectories. This answers a specific open RQ3/RQ4-adjacent question that the literature
states but does not isolate experimentally. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Null-GABA conductance sweep (3, 6, 9, 12 nS) to release the
deterministic ceiling on t0022</strong> (S-0029-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The t0022 scheduler uses GABA_CONDUCTANCE_NULL_NS = 12 nS applied 10 ms before AMPA on
null-direction trials - about 4x the preferred value (3 nS) and 2x Schachter2010's measured
compound null inhibition (~6 nS). This oversized early shunt forces null-direction firing to
exactly 0 Hz, pinning the pref/null DSI denominator and the ratio at 1.000 before cable
mechanics have any effect. Sweep GABA_CONDUCTANCE_NULL_NS across {3, 6, 9, 12} nS at a fixed
length multiplier of 1.0x and locate the conductance at which null-direction firing first
exceeds 1 Hz. That value is the testbed's sensitivity edge. Prerequisite for S-0029-01 and
S-0029-02: rerunning the length sweep at 6 nS instead of 12 nS gives the
mechanism-discrimination experiment a fighting chance without needing to inject noise. ~30 min
CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Per-dendrite E-I parameter sweep to map the DSI response
surface</strong> (S-0022-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1523_JNEUROSCI.5017-13.2014`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 driver has three free per-dendrite parameters fixed at single points:
EI_OFFSET_PREFERRED_MS = 10 ms, GABA_NULL/GABA_PREF ratio = 4x (12 nS / 3 nS), AMPA
conductance = 6 nS. Run a factorial sweep over EI_OFFSET in {5, 10, 15} ms, GABA ratio in {2,
3, 4, 6}, and AMPA in {0.15, 0.3, 0.6} nS (the last anchored to Park2014's 0.31 nS somatic
measurement) to quantify mechanism robustness. Expected outcome: a (3 x 4 x 3) = 36-point DSI
response surface showing which E-I corner of the parameter space saturates DSI at 1.0 (driver
is too deterministic) vs produces a graded DSI in the Park2014 0.65 +/- 0.05 band (mechanism
tracks continuous inhibition as real DSGCs do). Dependencies: t0022 library asset. Effort ~20
hours with the existing process-pool orchestrator. Recommended task type: experiment-run,
data-analysis.

</details>

<details>
<summary>🧪 <strong>Poisson-noise desaturation rerun of the distal-dendrite diameter
sweep on t0022</strong> (S-0030-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Sibling of S-0029-01 (Poisson + length sweep) targeting the diameter axis. The t0030
deterministic testbed yields reliability = 1.000 and null firing 0 Hz at every diameter, which
collapses the rate-code noise floor that Schachter2010's dendritic-spike-threshold mechanism
and Dan2018's passive-TR derivation both assume. Add an independent 5 Hz background Poisson
NetStim per distal dendrite (independent seed, no direction bias) to the t0022 scheduler and
rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials).
Expected: DSI drops from 1.000 into the 0.6-0.8 Park2014 envelope, reliability drops below
1.0, and diameter regains discrimination power between Schachter2010 active amplification
(+slope) and passive filtering (-slope). Distinct from S-0022-05 (Poisson at a single
length/diameter) and S-0029-01 (length axis). Recommended task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Re-distribute SACinhib synapses asymmetrically across PD-side and
ND-side dendrites in RGCmodel.hoc</strong> (S-0050-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0050-02` |
| **Kind** | technique |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0050_audit_syn_distribution/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Alternative 'fix path B' to S-0050-01: instead of modulating gabaMOD per synapse, modify the
construction loop in RGCmodel.hoc:11839-11857 so SACinhib synapses are placed asymmetrically
across the dendritic field (more on the ND-side, fewer on the PD-side) while leaving BIPsyn
and SACexcsyn at the deposited 282-symmetric distribution. t0050 found total dendritic length
per side is essentially identical (2311 vs 2296 um) so the dendritic substrate supports an
asymmetric placement at construction. Test whether the somatic SEClamp PD/ND asymmetry reaches
paper Fig 3C targets without changing per-synapse gabaMOD. This decouples the deposited 'three
channels share parent sections per index' design and is a more invasive but mechanistically
cleaner option. Recommended task types: feature-engineering, experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-enable NMDA (b2gnmda nonzero) crossed with distal-dendrite
length sweep on t0022</strong> (S-0029-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 `_silence_baseline_hoc_synapses` sets b2gnmda = 0 and installs single-component
AMPA-only E-I pairs, removing the Espinosa2010 AMPA/NMDA kinetic-tiling mechanism from the
testable space entirely. Espinosa2010 proposes that DSGC DS arises from different activation
time courses of AMPA and NMDA interacting with cable propagation delay - predicting
non-monotonic DSI-vs-length because NMDA's 50-150 ms time constant resonates with propagation
delay at specific lengths. Modify `_silence_baseline_hoc_synapses` to restore b2gnmda at 30%
of the 189347 baseline and rerun the 7-point length sweep. If DSI drops below 1.000 with
non-monotonic length dependence, kinetic tiling is a real third mechanism and the current null
result was partially a function of NMDA silencing. Requires a sibling library asset (clone of
t0022 with NMDA enabled) to preserve t0022's immutability. ~1 hour CPU plus ~1 hour coding.
Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🔧 <strong>Re-implement placeBIP() to spatially gate gabaMOD by per-synapse
locx</strong> (S-0050-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0050-01` |
| **Kind** | technique |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0050_audit_syn_distribution/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0050 confirmed deposited PD/ND swap is a single global scalar gabaMOD = 0.33 + 0.66*direction
applied uniformly to every SAC inhibitory synapse with no spatial threshold
(dsgc_model_exact.hoc:316-334). Modify placeBIP() (or wrap it in a helper) so gabaMOD is
computed per synapse from each synapse's locx relative to the BIPsyn-locx median (88.77 um) or
soma_x (104.58 um), scaling up ND-side synapses and down PD-side synapses while preserving the
population mean. Re-run t0049's somatic SEClamp protocol to test whether somatic GABA recovers
an ND-bias toward paper Fig 3C (PD ~12.5 / ND ~30 nS, DSI ~ -0.41). This is the primary 'fix
path A' identified by t0050's mechanism analysis. Recommended task types: feature-engineering,
experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-run t0046 figure sweeps at paper-N (12-19 trials per
condition, full 8-direction sweep)</strong> (S-0046-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Re-execute every figure-reproduction sweep in t0046 (`code/run_all_figures.py`) at the paper's
reported N (12-19 trials per condition) and the full 8-direction sweep instead of the
wall-clock-budget-reduced 2-4 trials and PD/ND-only collapse used in t0046. This will (a)
tighten the SD bands on PSP and AP-rate distributions, (b) replace the `atan2(mean PD PSP,
mean ND PSP)` slope approximation with a fit to the 8-direction tuning curve as the paper
does, and (c) reveal the true Fig 7 0 Mg2+ ROC AUC instead of the small-N saturation at 1.00
(paper reports 0.83). Recommended task types: experiment-run.

</details>

<details>
<summary>📚 <strong>Register SAC presynaptic drive model as an asset for downstream
DSGC input construction</strong> (S-0002-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-08` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1038_nature09818`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

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
<summary>🔧 <strong>Replace 1/e-crossing EPSP-decay metric with an exponential fit
and lengthen the post-stimulus window</strong> (S-0054-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-03` |
| **Kind** | technique |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`cable-theory`](../../../meta/categories/cable-theory/) |

REQ-20 (epsp_decay_to_1e_ms per gNMDA) returned null at all four gNMDA values because the 1500
ms trial window is shorter than the time the cell needs to drop below V_rest + (V_peak -
V_rest)/e once 100 simultaneous NMDA Exp2Syn events with tau2=80 ms keep Vm depolarised. The
headline numerical answer to 'how does EPSP tau scale with gNMDA?' is missing -- this is a
metric implementation gap, not a biological null result. Implement two changes: (1) extend the
recorded E_ONLY trace to 3000-5000 ms post-stimulus, (2) replace the 1/e-crossing search with
a least-squares exponential fit V(t) = V_rest + A * exp(-t / tau_decay). Validate against
t0052 baseline (expected tau_decay ~ 30 ms). Acceptance: tau is finite for all 4 gNMDA values,
falls in 30-300 ms, and rises monotonically. Recommended task types: write-library,
experiment-run.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled synaptic-integration PDFs via Sheffield access
and verify numerical priors</strong> (S-0018-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Five synaptic-integration papers (Lester et al. 1990, Koch-Poggio-Torre 1983, Wehr & Zador
2003, Hausser & Mel 2003, Euler-Detwiler-Denk 2002) are documented in
intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs through
Sheffield institutional access, update each paper asset's download_status to 'success',
replace summary Overview disclaimers with PDF-verified content, and cross-check the numerical
priors tabulated in the Prior Distribution Table of the answer asset (NMDAR tau_decay 100-200
ms at 22-32 degC, AMPA tau_rise 0.2-0.4 ms / tau_decay 1-3 ms, GABA_A tau_decay 5-20 ms,
lambda_DC 100-300 um for RGC dendrites, DSGC E-I lag 15-50 ms, SAC dendritic Ca2+ DS index
0.3-0.5) against the actual papers before adopting them as tight compartmental-model fitting
targets.

</details>

<details>
<summary>🧪 <strong>SEClamp Fig 3A-E re-measurement across multiple V_clamp levels
(-85, -65, -45 mV) to vary GABA driving force</strong> (S-0049-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0049-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0049_seclamp_cond_remeasure/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0049 ran SEClamp at the single V_clamp = -65 mV which yields a small GABA driving force (-5
mV vs E_GABA = -60 mV) and amplifies noise on the GABA conductance estimate (SD +/- 1.98 nS at
PD). Repeat the per-channel isolation sweep at V_clamp in {-85, -65, -45} mV. The -85 mV
condition gives a 25 mV GABA driving force (5x improvement in GABA SNR) and inverts the
AMPA/NMDA driving force; the -45 mV condition reverses the GABA driving force sign and
increases NMDA Mg-block relief. Tests (a) whether the GABA PD/ND symmetry persists across
V_clamp (ruling out driving-force noise), (b) whether NMDA over-amplification depends on
holding voltage. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Sweep AR(2) rho x V_rest for t0024 to separate noise correlation
from depolarisation effects</strong> (S-0026-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The t0024 V_rest sweep ran only at rho=0.6 and showed a 1.9x U-shaped DSI curve with HWHM
pinned at 65-83 deg. Repeat the sweep at rho in {0.0, 0.3, 0.6, 0.9} to test whether the
tuning-smoothing is dominated by AR(2) correlation or by the depolarisation itself. Expected
outcome: rho=0.0 should recover tuning sharpness closer to t0022 while preserving the
Na-inactivation-independent peak firing behaviour.

</details>

<details>
<summary>📚 <strong>Two-point driving-force saturation calibration library from t0052
+ t0053 IPSP data</strong> (S-0053-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-06` |
| **Kind** | library |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

S-0052-05 proposes a single-task library to translate nominal gabaMOD conductance ratios into
somatic-voltage IPSP modulation using t0052's observation alone (3.0x conductance -> 1.54x
voltage). t0053 provides a second calibration point on the same morphology and placement:
1.94x active-count ratio -> 1.24x voltage ratio at fixed 2 nS per synapse. Build a calibration
library `gaba_drive_saturation` taking both t0052 and t0053 IPSP data and fitting a two-point
(extensible via S-0052-02 GABA-count sweep) voltage-vs-conductance saturation curve, exposing
`gaba_eff(n_active_synapses, peak_g_per_syn)` returning predicted somatic IPSP modulation
depth. Future scalar / spatial / hybrid inhibition models call this during design to check
whether their nominal parameters land in the saturating regime. Sharpens S-0052-05 with a
two-point dataset. Recommended task types: write-library.

</details>

## Low Priority

<details>
<summary>🔧 <strong>Add preferred-direction GABA asymmetry to t0022 (cartwheel SAC
offset)</strong> (S-0037-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-06` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0022 applies only null-direction GABA. Published DSGC models (Park2014, Schachter2010)
include a directionally-offset SAC inhibition where preferred-direction trials see much lower
GABA than null. Implement the cartwheel asymmetry as a new parameter
`GABA_CONDUCTANCE_PREF_NS` (probably 0-1 nS based on t0037's over-excitation regime below 2
nS), and measure whether primary DSI improves toward the 0.5-0.6 Park2014 centre. This moves
t0022 closer to the canonical DSGC E-I motif rather than relying on a single null-only scalar.

</details>

<details>
<summary>📚 <strong>Package per-synapse conductance recorder and qualitative-shape
verdict helpers as a reusable library</strong> (S-0047-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0047-04` |
| **Kind** | library |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0047's `code/run_with_conductances.py` attaches `Vector.record(syn._ref_gAMPA / _ref_gNMDA /
_ref_g)` to every BIPsyn, SACexcsyn, and SACinhibsyn at cell-build time. It is the only
audited per-channel conductance recorder in the project and a prerequisite for any future Fig
3A-E reproduction (including S-0047-02's SEClamp variant). Package it as a reusable library
asset with: (a) `attach_conductance_recorders(cell, dt_record_ms)` that operates on any
t0046-derived cell; (b) qualitative-shape verdict helpers from `code/compute_metrics.py`
reporting PD/ND ratios per channel as a positive finding (AMPA flat across gNMDA, GABA ND ~2x
PD reproduce paper qualitative claims even though absolute amplitudes do not match); (c) a
single-trial smoke test. Distinct from S-0046-06 which packages the GUI-free `simplerun()`
driver. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Re-run t0047's noise (flickerVAR) sweep at Voff_bipNMDA=1 to test
noise-DSI behavior under voltage-independent NMDA</strong> (S-0048-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0047 ran a noise sweep at exptype=1 (Voff_bipNMDA=0). Now that t0048 establishes
Voff_bipNMDA=1 as the paper-faithful NMDA condition, the corresponding question is whether
t0047's noise vs DSI relationship (DSI declining with flickerVAR across the three gNMDA
conditions) holds under the voltage-independent setting. Re-run the same flickerVAR x gNMDA
grid t0047 used (or a reduced 3 x 3 grid to bound CPU) at exptype=2 and compare the
noise-vs-DSI shape. Useful corollary to t0048's gNMDA finding because it tells us whether the
noise sensitivity is dominated by NMDA voltage-dependence or by AMPA/GABA balance. Lower
priority because (a) t0047 already provides the qualitative noise-vs-DSI shape and (b) the H2
verdict for the Voff=1 DSI baseline is unlikely to be qualitatively different under noise.
Recommended task types: experiment-run.

</details>

## Closed

<details>
<summary>✅ <s>Add NMDA component to t0052 minimal DSGC and measure DSI / peak-rate
response</s> — covered by <a
href="../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/"><code>t0054_minimal_dsgc_ampa_nmda_scalar_gaba</code></a>
(S-0052-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0052_minimal_dsgc_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0052 is AMPA-only by design; PolegPolsky2016 attributes ~35% of PD PSP magnitude to NMDA (5.8
mV / 16.5 mV total) and shows NMDARs contribute multiplicatively at depolarised potentials.
Add a NEURON Exp2Syn-based NMDA component (rise 5 ms, decay 50 ms, e=0, Mg-block via
voltage-dependent gating or a simplified gating function) co-located with each AMPA synapse,
and sweep gNMDA in {0, 0.1, 0.25, 0.5, 1.0, 1.5} nS at the t0052 baseline (100 E + 100 I,
gAMPA = 0.5 nS, scalar gabaMOD). Report peak Hz, primary and vector-sum DSI, HWHM, and PD/ND
PSP magnitudes per gNMDA. Goal: test whether NMDA addition closes the peak-rate gap toward the
t0004 30 Hz target without breaking the DSI = 1.0 design from gabaMOD, in a
minimal-from-scratch substrate (not the deposited 189347 paper-port substrate of t0046-t0049).
Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Add voltage-dependent NMDA Mg block to recover DSI in the t0054
minimal AMPA + NMDA + scalar gabaMOD architecture</s> — covered by <a
href="../../../tasks/t0055_nmda_mg_block_dsi_recovery/"><code>t0055_nmda_mg_block_dsi_recovery</code></a>
(S-0054-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0054 demonstrated that voltage-independent NMDA (Exp2Syn, no Mg block) collapses vector-sum
DSI from 0.746 (gNMDA=0) to 0.082 (gNMDA=0.25) to 0.017 (gNMDA=1.0), confirming
PolegPolsky2016's prediction [Fig 5] that the Boltzmann Mg block is required for
multiplicative DSI scaling. Replace the NMDA Exp2Syn with a Jahr-Stevens Mg-block point
process (e.g., bipolarNMDA.mod from PolegPolsky2016 or an equivalent NMDA_Mg2 MOD), keeping
all other t0054 parameters fixed (placement seed 0, AMPA tau1=0.5/tau2=2.5/0.5 nS, scalar
gabaMOD with PD=0.33 ND=0.99 base 2 nS, soma+AIS HH). Re-run the {0, 0.25, 0.5, 1.0} nS gNMDA
sweep with the same 12 dirs x 10 trials x 3 modes protocol. Pass criterion: vector-sum DSI at
gNMDA=0.25 must exceed 0.50 and peak Hz must reach >= 5 Hz. This directly addresses the
headline negative result of t0054. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>✅ <s>Audit deposited GABA and NMDA spatial synapse coordinates against
Poleg-Polsky 2016 paper text</s> — covered by <a
href="../../../tasks/t0050_audit_syn_distribution/"><code>t0050_audit_syn_distribution</code></a>
(S-0049-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0049-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0049_seclamp_cond_remeasure/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Under SEClamp at -65 mV, the deposited code's GABA shows PD/ND symmetry (47.47 vs 48.04 nS,
DSI -0.006) instead of the paper's clear ND-bias (12.5 vs 30 nS, DSI -0.41). NMDA also
collapses to symmetry (DSI 0.006 vs paper +0.17). Modality alone does not reconcile this.
Audit `placeBIP()` and any GABA-placement HOC code in the deposited DSGC: extract per-synapse
3D coordinates and section assignments, classify each synapse by PD-side vs ND-side dendrite,
and compare the distribution against paper text and figure descriptions. This explains the
somatic asymmetry collapse and informs whether the deposited model needs a spatial
redistribution correction or a per-side conductance scaling. Recommended task types:
data-analysis.

</details>

<details>
<summary>✅ <s>GABA peak-conductance sweep on t0053 spatial DSGC to recover a
non-zero FULL tuning curve</s> — covered by <a
href="../../../tasks/t0057_tonic_gaba_sweep_t0053/"><code>t0057_tonic_gaba_sweep_t0053</code></a>
(S-0053-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0053 reports DSI = 0.0 / peak Hz = 0.0 in FULL mode because 2 nS GABA on ~50% of 100 synapses
(100 nS mean total per trial) fully suppresses spiking on the t0009-calibrated morphology.
AMPA-only fires at 0.667 Hz uniformly, so excitation is at threshold and any inhibition
crosses below threshold. Re-run the 12-direction x 10-trial FULL sweep on the t0053 substrate
(same placement seed 0, same centripetal-gating rule) at GABA peak conductances g_GABA in
{0.5, 1.0, 1.32, 1.5, 2.0} nS while holding everything else fixed. The 1.32 nS point is
conductance-matched to t0052's 66 nS mean total per trial. Report peak Hz, primary and
vector-sum DSI, HWHM, and reliability per g_GABA. Goal: locate the operating point where
spatial gating produces a measurable DSI on this morphology so it can be compared meaningfully
to t0052 and to in vivo / in vitro DSGC bands. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Literature survey: synaptic integration in RGC-adjacent systems
(target ~25 papers)</s> — covered by <a
href="../../../tasks/t0018_literature_survey_synaptic_integration/"><code>t0018_literature_survey_synaptic_integration</code></a>
(S-0014-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Systematically survey synaptic-integration literature relevant to DSGC dendrites. Target ~25
category-relevant papers covering AMPA/NMDA/GABA receptor kinetics, shunting inhibition, E-I
balance, temporal summation, dendritic-location dependence, synaptic-density scaling, and
SAC/DSGC inhibitory asymmetry. Exclude the 20 DOIs already in the t0002 corpus. Output: paper
assets + synthesis of kinetics parameters and E-I ratios usable as prior distributions in
later optimisation tasks.

</details>

<details>
<summary>✅ <s>Re-measure per-channel conductances under a somatic SEClamp on the
deposited DSGC to match paper Fig 3A-E modality</s> — covered by <a
href="../../../tasks/t0049_seclamp_cond_remeasure/"><code>t0049_seclamp_cond_remeasure</code></a>
(S-0047-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0047-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0047 records `_ref_g` directly at each synapse and obtains summed peak conductances 6-9x the
paper's Fig 3A-E targets and per-synapse-mean values 28-90x under. Neither interpretation
reconciles. The paper's Fig 3A-E most likely reports a somatic voltage-clamp-recorded compound
conductance — a third quantity not measured here. Implement a NEURON SEClamp at the soma held
at -65 mV across the same 7-point gNMDA sweep, record `_ref_i` on the clamp, and deconvolve
per-channel conductance via `g(t) = i(t) / (V_clamp - e_rev)` with `e_NMDA = e_AMPA = 0` and
`e_SACinhib = -60 mV`. Compare against paper targets within +/- 25%. Distinct from S-0046-02
(synapse-count) and S-0046-05 (supplementary PDF); also distinct from S-0019-XX which targets
a downstream model build, not the deposited code. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Re-run t0046 gNMDA sweep at exptype=2 (Voff_bipNMDA=1) to test whether
voltage-independent NMDA flattens DSI vs gNMDA</s> — covered by <a
href="../../../tasks/t0048_voff_nmda1_dsi_test/"><code>t0048_voff_nmda1_dsi_test</code></a>
(S-0047-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0047-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0047 confirms DSI vs gNMDA peaks at 0.19 near b2gnmda = 0.5 nS and decays to 0.018 by 3.0 nS,
never reaching the paper's claimed flat ~0.30. Most plausible source: the deposited control's
`Voff_bipNMDA = 0` (voltage-dependent NMDA with Mg block). As gNMDA rises, ND dendrites
depolarise enough to relieve Mg block and ND NMDA catches up to PD, collapsing DSI. The
paper's biological NMDA is voltage-INDEPENDENT. Direct test: re-execute the same 7-point sweep
(PD/ND, 4+ trials) at `exptype = 2` (sets `Voff_bipNMDA = 1`, the same setting used by 0Mg)
instead of `exptype = 1`. Expected: DSI flattens toward ~0.20-0.30 across the sweep. Not a
model modification — only an exptype choice. Re-uses t0046 library and t0047's
`code/run_with_conductances.py` directly. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Reproduce the PolegPolsky2016 baseline DSGC model from ModelDB 189347
as the project's starting compartmental simulation</s> — covered by <a
href="../../../tasks/t0008_port_modeldb_189347/"><code>t0008_port_modeldb_189347</code></a>
(S-0002-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-03` |
| **Kind** | technique |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

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
<summary>✅ <s>Rerun the distal-diameter sweep on t0022 with null-GABA conductance
reduced from 12 nS to 6 nS</s> — covered by <a
href="../../../tasks/t0036_rerun_t0030_halved_null_gaba/"><code>t0036_rerun_t0030_halved_null_gaba</code></a>
(S-0030-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

The t0030 sweep failed as a Schachter2010-vs-passive-filtering discriminator because primary
DSI is pinned at 1.000 at every diameter multiplier (null firing 0 Hz under the t0022 E-I
schedule). compare_literature.md traces the ceiling to GABA_CONDUCTANCE_NULL_NS = 12 nS
delivered 10 ms before AMPA on null trials, about 2x Schachter2010's compound null inhibition
(~6 nS). Rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials)
with GABA_CONDUCTANCE_NULL_NS lowered to 6 nS so null firing becomes non-zero and primary DSI
regains dynamic range. Distinct from S-0029-04 (null-GABA sweep at fixed length 1.0x) and
S-0029-01 (Poisson + length sweep): this targets the diameter axis specifically. Expected
cost: local CPU, ~2 h wall time. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Sequential further null-GABA reductions (4, 2, 1 nS) on the t0022
distal-diameter sweep</s> — covered by <a
href="../../../tasks/t0037_null_gaba_reduction_ladder_t0022/"><code>t0037_null_gaba_reduction_ladder_t0022</code></a>
(S-0036-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0036 halved GABA_CONDUCTANCE_NULL_NS from 12 nS to 6 nS and null firing stayed pinned at 0.0
Hz at every diameter multiplier, falsifying the Schachter2010 ~6 nS compound-inhibition
rescue. The classifier auto-recommendation was 'reduce null-GABA further to ~4 nS'. Rerun the
t0036 diameter sweep at 4 nS, 2 nS, and 1 nS (stop as soon as mean null firing exceeds 0.1 Hz
at 1.0x); each rerun is ~30 min CPU so worst case ~1.5 h. If null firing unpins at 4 or 2 nS,
primary DSI becomes measurable and the Schachter2010-vs-passive slope discriminator is rescued
on deterministic t0022. If it stays 0 Hz down to 1 nS, the testbed is structurally
incompatible with primary DSI on morphology axes and the project must adopt Poisson rescue
(S-0030-02) or migrate the optimiser substrate to t0024 (S-0034-07). Distinct from S-0029-04
(3-12 nS at fixed length on t0029 code) - this extends below the 3 nS floor on the t0036
diameter-sweep code path. Recommended task types: experiment-run.

</details>
