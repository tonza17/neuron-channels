# Suggestions: `retinal-ganglion-cell`

16 suggestion(s) in category
[`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) **13 open** (5
high, 7 medium, 1 low), **3 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>🔧 <strong>Calibrate active Nav / Kv / Ih densities to match Poleg-Polsky
2016 spike shape and distal Ih sag</strong> (S-0009-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-03` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Geometry alone does not recover the Schachter Rin targets; the residual gap needs active and
passive membrane parameters. On dsgc-baseline-morphology-calibrated, install Fohlmeister-like
Nav, delayed-rectifier Kv, and Ih channels and fit their densities (somatic vs dendritic) so
that (1) the somatic action-potential shape (halfwidth, peak, afterhyperpolarisation) matches
Poleg-Polsky 2016 Figure 2, and (2) the voltage-sag response to hyperpolarising current at
distal tips matches the Ih-driven sag amplitude reported in Schachter 2010. This is distinct
from S-0002-01 (DSI-maximising g_Na/g_K grid) and S-0002-02 (passive-vs-active DSI ablation):
it tunes channel densities against single-cell electrophysiological waveforms, not tuning
curves. Output: a library asset exposing the fitted mechanism list for reuse in the DSI
experiments. Recommended task types: experiment-run, feature-engineering.

</details>

<details>
<summary>🧪 <strong>Factorial morphology sweep (branch orders, segment length,
segment diameter) at fixed synapse count</strong> (S-0002-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1523_ENEURO.0261-21.2021`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

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
<summary>🔧 <strong>Interpolate soma pt3dadd diameters along the principal axis to
replace the uniform 4.118 um soma radius</strong> (S-0009-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-02` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

All 19 CNG soma rows currently receive the same averaged 4.118 um radius, flattening the
bell-shaped taper (~3.07 um to 5.31 um) visible in the five central Poleg-Polsky pt3dadd soma
contour points. Run PCA on the 19 soma xyz coordinates, project each row onto the first
principal component, and assign a radius by linear interpolation over the 7 Poleg-Polsky
pt3dadd values mapped onto the same axis. Emit a corrections file that overrides the 19
soma-row radii in dsgc-baseline-morphology-calibrated. Fixes the on-soma current-density
distribution for downstream spike-initiation simulations without changing the mean soma radius
or any dendritic row. Creative_thinking.md section F4. Recommended task types:
feature-engineering, correction.

</details>

<details>
<summary>🔧 <strong>Inverse-fit three-bin dendritic radii against the Schachter 2010
proximal/distal input-resistance gradient</strong> (S-0009-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-01` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The calibrated proximal Rin (0.52 MOhm) and distal Rin (54 MOhm) are far below Schachter
2010's 150-200 MOhm proximal and >1 GOhm distal targets because the pure-literature
Poleg-Polsky three-bin radii are not tuned to our cell. Keep the three-bin (primary / mid /
terminal) structure but treat the three radii as free parameters; fit them in a NEURON
passive-properties simulation (Ra=100 Ohm-cm, Rm fit jointly) so that soma Rin lands in
150-200 MOhm and distal-tip Rin >= 1 GOhm. Seed the optimiser with the Poleg-Polsky means
(3.694/1.653/0.439 um) and emit a corrections file that overrides
dsgc-baseline-morphology-calibrated with the fitted radii. Blocks downstream DSI reproductions
against Schachter's tree. Recommended task types: feature-engineering, experiment-run.

</details>

<details>
<summary>📚 <strong>Port the Poleg-Polsky & Diamond 2016 DSGC ModelDB 189347 into
the project as a library asset</strong> (S-0003-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-02` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Download ModelDB 189347 (the only public DSGC NEURON model), re-run its included demo, and
register the resulting Python package as a library asset under `assets/library/`. This makes
the DSGC reference implementation available to every downstream simulation task without
re-download.

</details>

## Medium Priority

<details>
<summary>🧪 <strong>Benchmark NEURON vs Arbor on the project's actual DSGC
morphology</strong> (S-0003-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Once a DSGC model runs in NEURON (via S-0003-02), port the same morphology and channel set to
Arbor 0.12.0 and measure single-cell simulation wall-clock on the project's workstation.
Third-party benchmarks claim Arbor is 7-12x faster; this task validates that claim on our
actual use case and records the real cost of the NMODL `modcc` translation that t0003 flagged
as the main Arbor adoption risk.

</details>

<details>
<summary>📚 <strong>Build a reusable SWC -> NEURON/NetPyNE/Arbor section-translator
library for dsgc-baseline-morphology</strong> (S-0005-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-04` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Every downstream compartmental-modelling task in this project will need to load the
dsgc-baseline-morphology SWC into a simulator and produce a section/segment graph indexed by
SWC compartment id, soma reference, and per-section parent links. NEURON's built-in Import3d
handling of CNG SWCs is fragile (soma-3point convention, branch-point splitting, axon stubs)
and other simulators have their own quirks (NetPyNE's netParams.cellParams, Arbor's morphology
builder). Write a small library asset that exposes a pure-function
load_dsgc_morphology(simulator: str) -> SimulatorMorphology API with verified-equivalent
loaders for NEURON, NetPyNE, and Arbor, plus a smoke test that compares total path length and
compartment count across loaders against validate_swc.py. This eliminates per-task SWC-loading
bugs and keeps morphology choice swappable when S-0005-03 lands. Recommended task types:
write-library.

</details>

<details>
<summary>📂 <strong>Download additional Feller-archive DSGC reconstructions to enable
cross-cell variability sensitivity analysis</strong> (S-0005-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-03` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The current dsgc-baseline-morphology commits the project to a single reconstructed cell
(141009_Pair1DSGC). Cell-to-cell variability in branching pattern, total path length, and
arbor extent is a known source of variance in DSGC tuning curves (RQ2), and the Feller archive
on NeuroMorpho hosts several sibling ON-OFF DSGC reconstructions from the same lab (e.g.,
141009_Pair2DSGC and other 2014 Pair* records). Download 3-5 additional Feller-archive ON-OFF
DSGC SWCs as separate dataset assets (each with its own NeuroMorpho neuron_id and provenance),
validate each with the existing validate_swc.py parser, and tabulate per-cell compartment
count, branch points, and total dendritic path length so a downstream morphology-sweep task
can quantify cross-cell variability without committing a priori to a specific morphology.
Recommended task types: download-dataset.

</details>

<details>
<summary>🔧 <strong>Re-calibrate using a Poleg-Polsky xyz-registered 1:1 per-section
diameter lookup to drop Strahler binning entirely</strong> (S-0009-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-04` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Our three-bin heuristic collapses 170 Poleg-Polsky mid-role sections into one 1.653 um radius
(section F1 of creative_thinking.md). A lossless alternative is to Procrustes-align the CNG
xyz points with the Poleg-Polsky RGCmodel.hoc pt3dadd points, then for each CNG compartment
copy the diameter of the nearest registered source section. Preserves all 350 source diameters
and eliminates both the tie-break-induced primary bin boundary (section F3) and the
bin-collapse interior variability. Deliverable: a sibling dataset asset
dsgc-baseline-morphology-registered with a registration-quality report (residual xyz distance
per compartment). Emit corrections if registration succeeds with sub-micron residuals.
Recommended task types: feature-engineering, data-analysis.

</details>

<details>
<summary>📂 <strong>Re-type SWC by section role (soma / primary / mid / terminal)
as a sibling dataset asset</strong> (S-0009-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-06` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The calibrated SWC uses only SWC type codes 1 (soma) and 3 (dendrite); downstream NEURON tasks
that set section-specific conductance densities (e.g., Na 150/150/30 mS/cm^2, K 70/70/35) must
re-derive Strahler order every time. Produce a sibling dataset asset
dsgc-baseline-morphology-calibrated-typed that re-types each row to 1 (soma), 5 (primary), 3
(mid), or 6 (terminal) using the calibration's bin labels. Topology, xyz, and parent_id are
preserved; only type_code changes. Add a conversion script and a smoke test that confirms
NEURON's Import3d loader accepts the extended type codes. Cuts duplicated Strahler
recomputation from every downstream channel-placement task. Creative_thinking.md section A3.
Recommended task types: feature-engineering.

</details>

<details>
<summary>📊 <strong>Render and QA-check 2D/3D visualisations of
dsgc-baseline-morphology for documentation and synapse placement</strong>
(S-0005-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

The dsgc-baseline-morphology asset is currently described only by tabulated statistics (6,736
compartments, 129 branch points, 1,536.25 um path length). Downstream tasks that place
AMPA/GABA synapses by spatial rule (e.g., Park2014 3-5x null/preferred IPSC asymmetry,
S-0002-05 GABA/AMPA density scan) need a visual reference for the dendritic arbor,
branch-order map, and soma orientation; reviewers also need a figure for any project paper.
Render three QA visualisations (2D top-down dendrogram coloured by Strahler order, 2D xy
projection coloured by path distance from soma, 3D rotating xyz scatter) using neurom +
matplotlib (or NEURON's PlotShape) and register the figures plus the rendering script as an
answer asset describing what was checked. Flag any visible reconstruction artefacts (dangling
branches, axon stubs, soma asymmetry) for downstream tasks. Recommended task types:
data-analysis, answer-question.

</details>

<details>
<summary>📂 <strong>Reproduce the Park2014 mouse ON-OFF DSGC tuning-curve dataset
as a validation benchmark</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1523_JNEUROSCI.5017-13.2014`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Park2014 (paper 10.1523_JNEUROSCI.5017-13.2014) and Chen2009 (paper
10.1113_jphysiol.2008.161240) are the two papers that set the mouse ON-OFF DSGC RQ5 targets
(DSI 0.6-0.9, peak 40-80 Hz, HWHM 60-90 deg). Park2014 is available open-access. Digitise the
published tuning-curve figure(s) into a reusable dataset asset (angle in degrees, spike rate
in Hz, error bars, cell counts) so the model can be scored against measured data rather than
only against the analytic target in t0004. This gives the project a literature-grounded
validation benchmark distinct from the canonical analytic target. Recommended task types:
download-dataset, data-analysis.

</details>

## Low Priority

<details>
<summary>📂 <strong>Per-cell ex-vivo two-photon image segmentation of
141009_Pair1DSGC to produce a cell-specific diameter ground truth</strong>
(S-0009-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-07` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The calibration imposes a nearby cell's diameters on our topology; a cell-specific ground
truth would validate or refute the transfer. The 141009_Pair1DSGC reconstruction came from the
Murphy-Baum / Feller two-photon rig; contact the original authors to obtain the raw image
stack and run a segmentation + radius-estimation pipeline (e.g., Vaa3D or neuTube) to recover
per-compartment diameters. Register the result as dsgc-baseline-morphology-imaged and use it
as the authoritative reference for sensitivity analyses like S-0009-05. Depends on external
data availability; likely requires an intervention for author contact. Recommended task types:
download-dataset, data-analysis.

</details>

## Closed

<details>
<summary>✅ <s>Calibrate realistic dendritic diameters for dsgc-baseline-morphology
to replace the 0.125 um placeholder radii</s> — covered by <a
href="../../../tasks/t0009_calibrate_dendritic_diameters/"><code>t0009_calibrate_dendritic_diameters</code></a>
(S-0005-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-02` |
| **Kind** | technique |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Every compartment in the downloaded CNG SWC carries the placeholder radius 0.125 um because
the original Simple Neurite Tracer reconstruction did not record diameters. Cable-theory
predicts segment diameter is the single most influential local-electrotonic knob (see
S-0002-04), so leaving the uniform placeholder in place will silently bias every downstream
biophysical simulation (axial resistance, attenuation, spike initiation threshold). Build a
diameter-calibration pipeline that applies a literature-derived order-dependent diameter taper
(e.g., Vaney/Sivyer/Taylor 2012 mouse ON-OFF DSGC profile, or the Poleg-Polsky 2016
distribution) keyed on Strahler order or path distance from the soma, write the calibrated SWC
as a new dataset asset (e.g., dsgc-baseline-morphology-calibrated), and report the per-order
diameter distribution against the original placeholder. Recommended task types:
feature-engineering, data-analysis.

</details>

<details>
<summary>✅ <s>Download both candidate Feller-lab 2018 source papers to resolve the
dsgc-baseline-morphology provenance ambiguity</s> — covered by <a
href="../../../tasks/t0013_resolve_morphology_provenance/"><code>t0013_resolve_morphology_provenance</code></a>
(S-0005-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The dsgc-baseline-morphology asset (NeuroMorpho neuron 102976, 141009_Pair1DSGC) currently has
source_paper_id=null because two Feller-lab papers from 2018 are plausibly the source: the
plan-nominated Morrie & Feller 2018 Neuron (DOI 10.1016/j.neuron.2018.05.028) and the
NeuroMorpho-reported Murphy-Baum & Feller 2018 Current Biology (DOI
10.1016/j.cub.2018.03.001). Run /add-paper for both DOIs in a dedicated download-paper task,
read each paper's Methods to confirm which one introduced the 141009_Pair1DSGC reconstruction,
then file a corrections asset that updates dsgc-baseline-morphology source_paper_id to the
correct paper_id slug. This unblocks correct citation of the morphology in every downstream
paper-comparison task. Recommended task types: download-paper.

</details>

<details>
<summary>✅ <s>Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain on the
local workstation</s> — covered by <a
href="../../../tasks/t0007_install_neuron_netpyne/"><code>t0007_install_neuron_netpyne</code></a>
(S-0003-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-01` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Create a task that `uv pip install neuron==8.2.7 netpyne==1.1.1` into the project's
virtualenv, compiles the bundled Hodgkin-Huxley MOD files with `nrnivmodl`, runs a
1-compartment sanity simulation, and records the installed versions, install-time warnings,
and simulation wall-clock in a task asset. Rationale: the t0003 survey selected this toolchain
but did not install it; the next simulation task needs a validated environment.

</details>
