# Suggestions: `cable-theory`

5 suggestion(s) in category [`cable-theory`](../../../meta/categories/cable-theory/) **3
open** (1 high, 2 medium), **2 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

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

## Medium Priority

<details>
<summary>📚 <strong>Port the TREES-toolbox Rall 3/2 quaddiameter rule to a
pure-Python calibrator and compare against the Strahler bins</strong>
(S-0009-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-08` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Rall's 3/2 power rule (r_parent^(3/2) = sum r_child^(3/2)) is the only biophysically
principled way to match impedance across a binary tree; our max-child Strahler bins have no
such guarantee. Implement TREES-toolbox's quaddiameter algorithm as ~80 lines of pure Python,
solve the system bottom-up from the 131 terminals with the Poleg-Polsky terminal mean fixed,
and produce a sibling asset dsgc-baseline-morphology-rall. Compare against the
Strahler-calibrated asset by per-branch axial resistance, total surface area, and
per-compartment radius deltas. Expected primary-radius shift ~15% (3.69 to ~3.1 um) at the
measured 2-way branching ratio. Creative_thinking.md section A2. Recommended task types:
write-library, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Sensitivity analysis: re-run DSGC simulations under alternative
Strahler tie-break rules and bin boundaries</strong> (S-0009-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

The primary bin (33 compartments) is set by max_strahler_order = 5 under a max-child
tie-break; a min-child or NeuroM section-based convention can push max_order to 6 and
reclassify the current 33 primary compartments as mid, jumping proximal Rin by ~15%
(creative_thinking.md section F3, E1). Produce 3-4 sibling calibrated SWCs under alternative
tie-break rules (max-child, min-child, NeuroM section_strahler_orders, two-bin collapse) and
run the downstream DSGC passive simulation from S-0009-01 on each. Report DSI, preferred peak,
HWHM, and proximal/distal Rin per variant; quantify the sensitivity of downstream metrics to
the heuristic choice. This makes the tie-break choice reviewable rather than arbitrary.
Recommended task types: experiment-run, comparative-analysis.

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
<summary>✅ <s>Literature survey: cable theory and dendritic filtering (target ~25
papers)</s> — covered by <a
href="../../../tasks/t0015_literature_survey_cable_theory/"><code>t0015_literature_survey_cable_theory</code></a>
(S-0014-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/) |

Systematically survey cable-theory and passive dendritic-filtering literature relevant to
direction-selective retinal ganglion cells. Target ~25 category-relevant papers spanning
Rall-era foundations, modern compartmental treatments, impedance / space-constant analyses,
and segment-discretisation guidelines. Exclude the 20 DOIs already in the t0002 corpus.
Output: paper assets + synthesis document organised by theme (classical cable theory, segment
discretisation, branched-tree impedance, frequency-domain analyses, transmission in thin
dendrites).

</details>
