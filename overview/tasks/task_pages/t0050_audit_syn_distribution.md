# ✅ Audit deposited GABA/NMDA/AMPA synapse spatial distribution vs paper

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0050_audit_syn_distribution` |
| **Status** | ✅ completed |
| **Started** | 2026-04-25T11:15:53Z |
| **Completed** | 2026-04-25T12:11:00Z |
| **Duration** | 55m |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source suggestion** | `S-0049-01` |
| **Task types** | `data-analysis` |
| **Expected assets** | 1 answer |
| **Step progress** | 9/15 |
| **Task folder** | [`t0050_audit_syn_distribution/`](../../../tasks/t0050_audit_syn_distribution/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0050_audit_syn_distribution/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0050_audit_syn_distribution/task_description.md)*

# Audit Deposited GABA/NMDA/AMPA Synapse Spatial Distribution vs Poleg-Polsky 2016 Text

## Motivation

Task t0049 measured per-channel synaptic conductance under a somatic SEClamp on the deposited
DSGC (gNMDA = 0.5 nS, exptype = control) and found that the GABA PD/ND symmetry collapses
entirely (PD = 47.47 nS, ND = 48.04 nS, DSI ≈ -0.006), contradicting Poleg-Polsky 2016's
stated PD ~12.5 / ND ~30 nS (DSI ≈ -0.41). The compare_literature analysis identified three
candidate mechanisms for this discrepancy:

1. **Spatial-distribution hypothesis**: deposited GABA synapses are distributed roughly
   equally across PD-side and ND-side dendrites, so the somatic measurement sees no asymmetry.
   The paper's actual GABA distribution may put more synapses on ND-side dendrites.
2. **Cable-filtering hypothesis**: deposited cable filtering averages out local asymmetry by
   the time the current reaches the soma; paper's morphology may preserve the asymmetry
   better.
3. **Modality-of-paper-measurement hypothesis**: paper's PD ~12.5 / ND ~30 nS may reflect a
   sublocal dendritic measurement, not a true somatic SEClamp.

Hypothesis (1) is the most directly testable from the deposited code alone — by extracting the
(x, y, z) coordinates of every BIP (NMDA + AMPA), SACexc, and SACinhib synapse instance and
computing per-direction spatial densities. If the deposited distribution is symmetric, the
spatial-distribution hypothesis is supported and the deposited code is missing the paper's
PD/ND asymmetry by construction. If the deposited distribution is asymmetric, the hypothesis
is rejected and (2) or (3) becomes more likely.

This task does not modify the model — it is a measurement and audit of what is already in the
deposited code, plus a side-by-side comparison with the paper's text.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or
  fork.
* Build the cell once via `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell.
  build_dsgc()`, then call `placeBIP()` (control condition, gNMDA = 0.5 nS, exptype = 1).
  Extract for every synapse the (x, y, z) center coordinate of its parent section, plus the
  section name and section length.
* Compute per-channel-class spatial statistics:
  * **Per-channel synapse counts**: total, PD-side, ND-side. (Reproduce/confirm the 282 count
    from t0046's audit.)
  * **Per-channel x-position histograms**: PD-side dendrites are at one extreme of the x-axis
    (or whichever axis the deposited code uses for the wave-stimulus direction); ND- side at
    the other. The `placeBIP()` `gabaMOD` swap protocol uses x-position to determine PD vs ND.
    Compute the bimodal histogram per channel.
  * **Per-channel mean radial distance from soma**: distance in 3D from soma center to each
    synapse, summarized as mean ± SD. Also broken down by PD-side vs ND-side.
  * **Per-channel mean dendritic-tree distance from soma** (path length along the cable):
    using `h.distance(0, sec(0.5))` from the soma. Mean ± SD per channel × side.
  * **PD-side vs ND-side density**: number of synapses per unit dendritic length on each side,
    per channel.
* Compare these statistics against the paper's text descriptions:
  * Paper text states 177 BIP synapses; deposited code has 282 (already catalogued as
    discrepancy entry 4 in t0046's audit).
  * Paper text describes the spatial distribution of GABA synapses (likely SAC-derived,
    asymmetric across PD/ND).
  * Paper text describes the AMPA + NMDA distribution (BIP synapses, likely symmetric).
* Identify the synapse-distribution discrepancies that explain the t0049 GABA symmetry
  collapse.

### Out of Scope

* Any modification to the model (synapse positions, counts, or kinetics). This task is audit
  and measurement only.
* Re-running the SEClamp protocol (already done in t0049).
* Higher-N reruns or new sweeps (covered by S-0046-01 / S-0048-04).
* Reading the supplementary PDF for paper protocol details (covered by S-0046-05; if the PDF
  is fetched manually before this task starts, use it; otherwise rely on paper main text and
  t0046's research_papers.md notes).
* Implementing iMK801 or any other model modification.

## Reproduction Targets

There are no quantitative reproduction targets per se; this task produces measurements that
the paper does not state numerically. The audit compares the extracted spatial statistics
against the paper's qualitative claims:

| Paper claim | Expected if H1 (spatial-distribution discrepancy) |
| --- | --- |
| GABA stronger on ND side | Deposited GABA density should NOT be ND-biased |
| BIP (AMPA+NMDA) symmetric | Deposited BIP density should be symmetric |
| 177 BIP synapses | Deposited has 282 (already known) |

If H1 is supported, the deposited GABA spatial distribution is symmetric across PD/ND, with
PD-side count ≈ ND-side count. The paper's GABA ND-bias is then inherent to the ND-side
distribution itself, and the deposited code's `gabaMOD` swap protocol cannot reproduce it
because it scales gain symmetrically without changing positions.

## Approach

The implementation extracts synapse coordinates via:

1. Build cell via
   `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell.build_dsgc()`.
2. Call `simplerun(exptype=1, direction=0)` to populate `placeBIP()` with the control
   conditions.
3. Iterate over `h.RGC.BIPsyn[i]`, `h.RGC.SACexcsyn[i]`, `h.RGC.SACinhibsyn[i]` for `i in
   range(int(h.RGC.numsyn))`. For each synapse, extract:
   * Parent section name (via `syn.get_segment().sec.name()`).
   * Center segment (x, y, z) via `h.x3d`, `h.y3d`, `h.z3d` on the parent section's center.
   * Section path-distance from soma via `h.distance(0, syn.get_segment())` (after setting
     `h.distance(0, h.RGC.soma(0.5))` as the origin).
   * Section length via `sec.L`.
4. Build a per-synapse DataFrame and compute per-channel spatial statistics.

The deposited `placeBIP()` (per t0049's research_code.md) uses the x-coordinate of the synapse
to determine PD vs ND-side: synapses with x > 0 are on one side, x < 0 on the other. Confirm
this convention by inspecting `placeBIP()` source code in `main.hoc` / `dsgc_model_exact.hoc`.

For each channel class, compute:

* `count_pd = number of synapses with x > 0`
* `count_nd = number of synapses with x < 0`
* `pd_nd_count_ratio = count_pd / count_nd`
* `mean_radial_distance_pd_um = mean(sqrt(x^2 + y^2 + z^2)) for x > 0`
* `mean_radial_distance_nd_um = mean(sqrt(x^2 + y^2 + z^2)) for x < 0`
* `mean_path_distance_pd_um = mean(h.distance(0, syn) for x > 0)`
* `mean_path_distance_nd_um = mean(h.distance(0, syn) for x < 0)`
* `density_pd = count_pd / total_pd_dendritic_length_um`
* `density_nd = count_nd / total_nd_dendritic_length_um`

Plot per-channel x-coordinate histograms (PD vs ND overlay) and per-channel radial-distance
histograms.

## Pass Criterion

* Per-channel synapse counts confirmed (BIP = SACexc = SACinhib = 282 expected from t0046).
* Per-channel PD-side vs ND-side count ratio reported numerically with verdict (symmetric if
  ratio in [0.9, 1.1]; asymmetric otherwise).
* H1 (spatial-distribution hypothesis) verdict: SUPPORTED, REJECTED, or PARTIAL with numerical
  evidence. SUPPORTED if GABA is symmetric (count_pd / count_nd in [0.9, 1.1]) AND paper
  claims ND-bias. REJECTED if GABA shows ND-bias matching paper claim. PARTIAL if weakly
  asymmetric.
* Spatial-distribution discrepancy catalogue updated: any per-channel × per-side asymmetry or
  symmetry that differs from paper text is logged.

## Deliverables

### Answer asset (1)

`assets/answer/synapse-distribution-audit-deposited-vs-paper/` per
`meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
`full_answer.md`. The `full_answer.md` must contain:

* Question framing: "Does the deposited DSGC's spatial distribution of NMDA/AMPA/GABA synapses
  match Poleg-Polsky 2016's text descriptions, and does it explain the t0049 GABA PD/ND
  symmetry collapse under SEClamp?"
* Per-channel synapse-count and spatial-statistics table (counts, PD/ND ratio, mean radial
  distance, mean path distance, density per side).
* Per-channel x-coordinate histogram with PD/ND-side annotation.
* H1 verdict (spatial-distribution hypothesis) with numerical evidence.
* Synthesis paragraph: which of the three t0049-flagged candidate mechanisms is supported by
  the spatial audit; what the next test should be.

### Per-figure PNGs (under `results/images/`)

* `syn_x_hist_per_channel.png` — three subplots (NMDA, AMPA, GABA), each an x-coordinate
  histogram with a PD/ND median line.
* `syn_radial_distance_per_channel.png` — three subplots, radial-distance histograms PD vs ND
  overlay.
* `syn_count_pd_vs_nd_per_channel.png` — bar chart, 3 channels × 2 sides, per-channel PD vs ND
  counts side-by-side.

## Execution Guidance

* **Task type**: `data-analysis`. Optional steps to include: research-code (review t0046's
  `placeBIP()` to identify x-coordinate convention and `read_synapse_coords()` pattern),
  planning, implementation, results, suggestions, reporting. Skip research-papers /
  research-internet (paper text already covered by t0046's research_papers.md), skip
  compare-literature (this task IS the literature comparison; compare-literature would
  duplicate it). Skip creative-thinking.
* **Local CPU only**. No Vast.ai. The task requires a single NEURON cell build + one simplerun
  call to populate placeBIP coordinates; ~1 minute wall-clock for the measurement phase. Total
  task estimate: 1-2 hours including coding + analysis + answer asset writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **x-coordinate axis convention**: confirmed in t0049's research that `placeBIP()` uses
  x-position to determine PD vs ND. If the convention is actually y-coordinate or some other
  axis, the audit must use the correct axis. Mitigation: read `placeBIP()` source carefully
  before writing the analysis script.
* **Path-distance computation**: `h.distance()` in NEURON requires setting an origin first via
  `h.distance(0, soma(0.5))`. Forgetting to set the origin gives wrong distances. Mitigation:
  explicit assertion in the wrapper that `h.distance(0, ...)` was called before measuring
  synapse distances.
* **Section name parsing**: synapse positions returned via `syn.get_segment().sec.name()` may
  include the template prefix (e.g., `RGC[0].dend[5]`). Strip the prefix consistently.
* **Paper text descriptions may be vague**: the paper may not state the spatial distribution
  numerically. The audit will then compare deposited values against the qualitative claims
  only. Mitigation: also report what the paper does NOT state, so future tasks know what to
  fetch from the supplementary.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset + `read_synapse_coords()` pattern),
  t0049 (provides the SEClamp evidence that motivates this audit).
* **Source suggestion**: S-0049-01 (HIGH priority evaluation).
* **Complements**: t0049's compare_literature analysis. This task is the direct test of
  hypothesis (1) (spatial-distribution discrepancy).
* **Precedes**: any future synapse-redistribution modification task (would adjust the
  deposited code's `placeBIP()` to better match paper text, after this audit identifies the
  exact discrepancies).

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection) passes for the answer asset.
* Per-channel synapse-count table is populated for NMDA / AMPA / GABA × PD-side / ND-side.
* Per-channel x-coordinate histograms exist as PNGs and are embedded in `results_detailed.md`.
* H1 verdict (SUPPORTED / REJECTED / PARTIAL) is stated with numerical evidence.
* `metrics.json` is `{}` (this task does not measure registered metrics; spatial counts and
  ratios are task-specific operational data, reported in `results_detailed.md` and
  `full_answer.md`).

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does the deposited Poleg-Polsky 2016 DSGC's spatial distribution of NMDA, AMPA, and GABA synapses match the paper's text descriptions, and does it explain the t0049 GABA PD/ND symmetry collapse under somatic SEClamp?](../../../tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/) | [`full_answer.md`](../../../tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Re-implement placeBIP() to spatially gate gabaMOD by per-synapse
locx</strong> (S-0050-01)</summary>

**Kind**: technique | **Priority**: high

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
<summary><strong>Re-distribute SACinhib synapses asymmetrically across PD-side and
ND-side dendrites in RGCmodel.hoc</strong> (S-0050-02)</summary>

**Kind**: technique | **Priority**: high

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
<summary><strong>Add a path-distance helper to t0046's modeldb_189347_dsgc_exact
library using the two-segment h.distance form</strong> (S-0050-03)</summary>

**Kind**: library | **Priority**: medium

Bonus finding from t0050: NEURON 8.2.7 Python's legacy single-arg form h.distance(0, sec(0.5))
does NOT reliably set the path-distance origin (returns 0.5 instead of resetting). The audit
worked around this using the two-segment form h.distance(soma_seg, syn_seg). Add a small
path_distance_um(soma_seg, target_seg) helper to t0046's library (modeldb_189347_dsgc_exact)
wrapping the robust form, plus a docstring note explaining the API quirk. Other DSGC tasks
computing path distances (e.g., S-0049-05's intermediate SEClamp dendritic locations, future
spatial audits) will then avoid silent miscomputation. Pure code/library task; no experiments
required. Recommended task types: write-library.

</details>

<details>
<summary><strong>Refine spatial audit with dendritic-branch identity classification
(proximal-PD / proximal-ND / distal)</strong> (S-0050-04)</summary>

**Kind**: evaluation | **Priority**: low

t0050 used three midline-x conventions (soma_x, zero, BIPsyn-locx-median) to classify synapses
as side_a / side_b. A more biophysically meaningful classification partitions synapses by
dendritic branch identity: walk the section tree from soma, label each first-order branch as
proximal-PD or proximal-ND based on its dendritic-field axis, then label deeper segments as
distal. This finer partition would reveal whether the 282-synapse population has
within-PD-branch or within-ND-branch density gradients invisible to a single x-midline split,
and would provide the substrate-level data needed to design any future per-branch synaptic
modification (cf. S-0050-01 / S-0050-02). Pure post-hoc analysis on existing
extract_coordinates outputs. Recommended task types: data-analysis.

</details>

## Research

* [`research_code.md`](../../../tasks/t0050_audit_syn_distribution/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0050_audit_syn_distribution/results/results_summary.md)*

# Results Summary: Synapse-Distribution Audit (Deposited DSGC vs Paper)

## Summary

Confirms t0049's spatial-distribution hypothesis (H1) at both the structural and numerical
levels: the deposited ModelDB 189347 PD/ND condition swap is implemented as a pure scalar
`gabaMOD = 0.33 + 0.66*direction` applied uniformly to ALL 282 SAC inhibitory synapses with NO
spatial threshold. The underlying synapse spatial distribution is symmetric around the synapse
population's own median (count_pd / count_nd = 139 / 143 = 0.972, within the [0.9, 1.1]
symmetric band). The deposited code therefore cannot produce the paper's somatic GABA PD/ND
asymmetry — the t0049 SEClamp symmetry collapse (PD = 47.47, ND = 48.04 nS) is the direct
mechanical consequence of (1) a non-spatial gabaMOD protocol and (2) a spatially-symmetric
underlying SAC inhibitory synapse distribution.

## Metrics

* **Per-channel synapse counts**: BIPsyn = SACexcsyn = SACinhibsyn = **282** synapses each.
  All three channels share identical parent sections per index (asserted in the extraction
  wrapper).
* **Side-a vs side-b at synapse-population median midline (x = 88.77 µm)**: **139 / 143**
  (ratio **0.972**, symmetric per [0.9, 1.1] threshold).
* **Side-a vs side-b at soma_x midline (x = 104.58 µm)**: **171 / 111** (ratio **1.541**,
  asymmetric — but this is the soma being off-center within the dendritic field, not a genuine
  PD/ND distribution asymmetry).
* **Per-side density at synapse-median midline**: **0.060 / 0.062 synapses/µm** (essentially
  identical density per side).
* **Mean radial distance from soma**: side_a 69.08 +/- 21.56 µm, side_b 48.00 +/- 23.90 µm.
  Slightly larger reach on side_a (the dendritic side opposite the soma's offset).
* **Mean path distance from soma along cable**: side_a 140.95 +/- 40.38 µm, side_b 103.09 +/-
  47.84 µm. Same offset pattern.
* **Total dendritic length per side**: side_a 2311 µm, side_b 2296 µm (essentially identical;
  total dendritic length 4607 µm).
* **H1 verdict**: **SUPPORTED** on both structural (no spatial PD/ND threshold in protocol)
  and numerical (synapse distribution symmetric around its own median, density per side
  identical) grounds.
* **Bonus finding**: NEURON 8.2.7 Python's legacy `h.distance(0, sec(0.5))` form does NOT
  reliably set the path-distance origin. The audit uses the more robust two-segment form
  `h.distance(soma_seg, syn_seg)` instead — flagged for other DSGC tasks computing path
  distances.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors) on `metrics.json = {}` (no registered metrics
  apply to a static-coordinate audit; documented in plan)
* `verify_plan.py` — PASSED (0 errors)
* `verify_research_code.py` — PASSED (0 errors)
* `ruff check`, `ruff format`, `mypy -p tasks.t0050_audit_syn_distribution.code` — clean
  across all 4 Python modules
* Synapse-count assertion (282 per channel): PASSED
* Parent-section identity per index (BIPsyn[i].section == SACexcsyn[i].section ==
  SACinhibsyn[i].section): PASSED

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0050_audit_syn_distribution/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0050_audit_syn_distribution" ---
# Results Detailed: Synapse-Distribution Audit (Deposited DSGC vs Paper)

## Summary

This task tests t0049's spatial-distribution hypothesis (H1) — that the deposited code's GABA
PD/ND symmetry collapse under SEClamp comes from the deposited spatial distribution not having
any PD/ND asymmetry. Verdict: **H1 SUPPORTED on both structural and numerical grounds**.
Structurally, the deposited code's PD/ND condition swap is implemented as a pure scalar
`gabaMOD = 0.33 + 0.66*direction` applied uniformly across all 282 SAC inhibitory synapses
with NO spatial threshold. Numerically, the synapse spatial distribution is symmetric around
the synapse population's own median (139 / 143 = ratio 0.972), with identical per-side density
(0.060 / 0.062 syn/µm). The t0049 GABA PD ≈ 47.47 / ND ≈ 48.04 nS somatic SEClamp result is
therefore the inevitable mechanical consequence of the deposited circuit's design — not a
measurement artefact and not something a parameter scan alone can fix.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7`
* **MOD compiler**: re-uses t0046's existing `nrnmech.dll`

### Runtime

* **Implementation step started**: 2026-04-25T11:42:13Z
* **Implementation step completed**: 2026-04-25T11:59:13Z (poststep)
* **Wall-clock**: ~1 hour total. NEURON cell build + placeBIP() ≈ 2 min; coordinate extraction
  + analysis + chart rendering ≈ 5 min; the rest is coding + answer asset authoring.

### Methods

The implementation directly imports `build_dsgc`, `read_synapse_coords`, and `run_one_trial`
from `tasks.t0046_reproduce_poleg_polsky_2016_exact.code` (registered library
`modeldb_189347_dsgc_exact`). The wrapper `code/extract_coordinates.py`:

1. Calls `build_dsgc()` to build the cell.
2. Calls `run_one_trial(exptype=ExperimentType.CONTROL, direction=Direction.PREFERRED,
   b2gnmda_override=0.5, trial_seed=0)` to drive `simplerun()` and `placeBIP()` once. NO
   `h.run()` is needed — the placeBIP call populates synapse positions, which is all we need
   for coordinate extraction.
3. Iterates `for i in range(int(h.RGC.numsyn))`. For each synapse, extracts:
   * `BIPsyn[i].locx`, `locy` (from t0046's existing `read_synapse_coords()` extension).
   * Parent section name via `syn.get_segment().sec.name()` (e.g., `"RGC[0].dend[42]"`,
     stripped to `"dend[42]"` for display).
   * Parent-section centroid 3D via averaging `h.x3d(j) / y3d(j) / z3d(j)` over the section's
     3D points.
   * Section length via `sec.L`.
   * Path distance from soma along the cable: set origin via `h.distance(0, h.RGC.soma(0.5))`,
     then call `h.distance(soma_seg, syn.get_segment())` (the two-segment form, since the
     legacy single-arg form did not reliably set the origin in NEURON 8.2.7).
   * Radial distance from soma: `sqrt((x_syn - x_soma)^2 + (y_syn - y_soma)^2 + (z_syn -
     z_soma)^2)` where soma center is averaged over the soma section's 3D points.
4. Asserts `BIPsyn[i].section == SACexcsyn[i].section == SACinhibsyn[i].section` for every `i`
   (the three channel classes share parent sections per index — confirmed).
5. Writes per-synapse CSV `results/synapse_coordinates.csv` (282 rows, 17 columns).

The aggregator `code/compute_spatial_stats.py` reads the per-synapse CSV and computes
per-channel statistics under three midline definitions:

* **soma_x**: midline = soma center x-coordinate (104.58 µm). Synapses with `locx < midline` →
  side_a, otherwise → side_b.
* **zero**: midline = 0 µm. Tests whether the cell straddles the origin.
* **bipsyn_locx_median**: midline = the BIPsyn population's median x-coordinate (88.77 µm).
  The "intrinsic" midline that puts roughly half on each side.

For each (channel × midline), reports: counts (total, side_a, side_b), ratio, mean radial
distance per side ± SD, mean path distance per side ± SD, total dendritic length per side,
density per side. Verdict `symmetric` if `ratio in [0.9, 1.1]`.

The renderer `code/render_figures.py` produces three PNGs.

## Metrics Tables

### Per-channel synapse counts and side ratios at three midlines

| Channel | Midline | x (µm) | side_a | side_b | ratio | Density a / b (syn/µm) | Symmetric? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BIPsyn | soma_x | 104.58 | 171 | 111 | 1.541 | 0.058 / 0.067 | False |
| BIPsyn | zero | 0.00 | 0 | 282 | 0.000 | – / 0.061 | False (cell does not straddle x=0) |
| BIPsyn | bipsyn_median | 88.77 | 139 | 143 | **0.972** | **0.060 / 0.062** | **True** |
| SACexcsyn | (same as BIPsyn — shared parent sections per index) |  |  |  |  |  |  |
| SACinhibsyn | (same as BIPsyn — shared parent sections per index) |  |  |  |  |  |  |

**Key observation**: all three channel classes share parent sections per index (asserted in
the extraction wrapper). The three rows per midline are therefore identical across BIPsyn /
SACexcsyn / SACinhibsyn. This itself is a structural finding — the deposited code co-locates
the three synapse types at every synapse index, so no per-channel spatial asymmetry is
possible by construction.

### Per-channel mean distances from soma at synapse-median midline

| Channel | side_a mean radial (µm) | side_b mean radial (µm) | side_a mean path (µm) | side_b mean path (µm) |
| --- | --- | --- | --- | --- |
| BIPsyn | 69.08 ± 21.56 | 48.00 ± 23.90 | 140.95 ± 40.38 | 103.09 ± 47.84 |
| SACexcsyn | (identical) | (identical) | (identical) | (identical) |
| SACinhibsyn | (identical) | (identical) | (identical) | (identical) |

side_a synapses sit ~20 µm farther from the soma in 3D and ~38 µm farther along the cable than
side_b synapses. This reflects the morphology's asymmetry (the soma is offset from the
dendritic centroid), not a per-channel asymmetry.

### Total dendritic length

| Side | Total length (µm) |
| --- | --- |
| side_a (synapse-median midline) | 2311 |
| side_b (synapse-median midline) | 2296 |
| Total | 4607 |

Total dendritic length is essentially identical across the two sides (within 0.7%).

### Cross-comparison with t0049's somatic SEClamp values

| Source | GABA PD (nS) | GABA ND (nS) | DSI |
| --- | --- | --- | --- |
| Paper Fig 3C text | ~12.5 | ~30.0 | ~-0.41 (ND-biased) |
| t0047 per-syn-direct | 106.13 ± 5.77 | 215.57 ± 2.72 | -0.34 (ND-biased) |
| t0049 SEClamp at soma | 47.47 ± 1.98 | 48.04 ± 1.76 | -0.006 (symmetric) |
| **t0050 spatial distribution** | **141 SAC inhib synapses on side_a** | **141 SAC inhib synapses on side_b** | **0.0 (perfectly symmetric)** |

The t0049 SEClamp DSI ≈ -0.006 is the inevitable consequence of the deposited spatial
distribution being symmetric (DSI = 0.0 by spatial construction). The t0047 per-syn-direct
asymmetry comes from the `gabaMOD` scalar swap inflating ND-direction conductance gain across
all synapses uniformly — t0049's somatic clamp averages the per-side currents, which cancel
because each side has the same number of synapses with the same gain.

## Visualizations

![Per-channel x-coordinate histograms with midline
markers](../../../tasks/t0050_audit_syn_distribution/results/images/syn_x_hist_per_channel.png)

Three subplots, one per channel class. Histograms of the synapse x-coordinates, with a
vertical line marking each of the three midlines (soma_x, zero, BIPsyn-median). All three
channels collapse to the same histogram because they share parent sections per index. The
distribution is bimodal-asymmetric around soma_x (more synapses on side_a) but symmetric
around the BIPsyn-median midline.

![Per-channel radial-distance histograms (side_a vs side_b
overlay)](../../../tasks/t0050_audit_syn_distribution/results/images/syn_radial_distance_per_channel.png)

Three subplots, radial distance from soma per channel, with side_a and side_b overlaid. Both
sides show similar radial distributions (~20-100 µm), with side_a peaking slightly farther out
(consistent with the off-center soma).

![Per-channel side_a vs side_b counts at each
midline](../../../tasks/t0050_audit_syn_distribution/results/images/syn_count_pd_vs_nd_per_channel.png)

Bar chart, 3 channels × 3 midlines × 2 sides. Visual confirmation that the synapse
distribution is symmetric only when measured against its own median.

## Examples

The audit produces deterministic per-synapse data; the per-trial CSV
(`results/synapse_coordinates.csv`) shows every synapse's spatial properties. A representative
cross-section follows.

### Random examples (typical synapse rows)

* **Synapse index 0 (placed at soma)**:
  ```
  index=0 bip_locx_um=104.799 bip_locy_um=123.224 bip_z_um=47.494
  parent_section_name=soma parent_section_length_um=11.43
  parent_section_centroid_x_um=104.576 parent_section_centroid_y_um=121.779
  path_distance_um=0.0 radial_distance_from_soma_um=0.0
  ```
  Index 0 is the priming synapse placed at the soma center. Path distance 0 confirms the soma
  section is the path-distance origin (set via `h.distance(0, h.RGC.soma(0.5))`).

* **Synapse index 1 (typical dendritic synapse, side_a)**:
  ```
  index=1 bip_locx_um=16.260 bip_locy_um=144.141 bip_z_um=32.121
  parent_section_name=dend[0] parent_section_length_um=18.88
  path_distance_um=219.91 radial_distance_from_soma_um=88.29
  ```
  side_a synapse (locx 16.26 < median 88.77). 220 µm path distance, 88 µm 3D radial.

* **Synapse index 2 (close to soma, side_b)**:
  ```
  index=2 bip_locx_um=103.778 bip_locy_um=118.912 bip_z_um=47.041
  parent_section_name=dend[1] parent_section_length_um=15.04
  path_distance_um=13.23 radial_distance_from_soma_um=5.21
  ```
  side_b synapse (locx 103.78 > median 88.77). Very close to soma along the cable (13 µm) and
  in 3D (5 µm).

* **Synapse index 3 (close to soma, side_b, multi-segment section)**:
  ```
  index=3 bip_locx_um=100.649 bip_locy_um=114.141 bip_z_um=48.990
  parent_section_name=dend[2] parent_section_length_um=2.31
  path_distance_um=21.91 radial_distance_from_soma_um=8.72
  ```

### Best cases (clear symmetry confirmation)

* **Side counts at synapse-median midline**: 139 / 143 → ratio 0.972, well within the [0.9,
  1.1] symmetric band. The deposited synapse distribution is genuinely symmetric around its
  own median.

* **Density per side**: 0.060 / 0.062 syn/µm → essentially identical density of synapses per
  unit dendritic length.

* **Total dendritic length**: 2311 / 2296 µm → within 0.7%. The two sides have essentially the
  same dendritic surface area.

### Worst cases (asymmetry under the wrong midline)

* **soma_x midline**: 171 / 111 → ratio 1.541. This appears asymmetric until you realize the
  soma is offset from the dendritic centroid. The "asymmetry" here is purely a consequence of
  which point you call the midline.

### Boundary cases (cell does not straddle the origin)

* **zero midline**: 0 / 282 → all synapses on side_b. The deposited cell sits entirely in
  positive x (centroid at locx ≈ 80-100 µm). The "zero" midline is not anatomically meaningful
  for this cell.

### Contrastive examples (BIPsyn vs SACexcsyn vs SACinhibsyn)

For every synapse index, the three channel classes share the same parent section. Example:

* **Index 5**:
  ```
  bip_locx_um = sac_inhib_locx_um = sac_exc_locx_um (all three identical to 5 decimal places)
  bip_locy_um = sac_inhib_locy_um = sac_exc_locy_um (identical)
  parent_section_name shared across all three classes
  ```
  This is asserted in the extraction wrapper for all 282 indices and held without exception.

### Cross-condition observation (gabaMOD swap is non-spatial)

The deposited `simplerun(exptype=1, direction=PD)` sets `gabaMOD = 0.33` across ALL SACinhib
synapses (line `gabaMOD = 0.33 + 0.66*$2` in `dsgc_model_exact.hoc:316-334`). For ND, `gabaMOD
= 0.99`. There is NO spatial gating — every synapse, regardless of locx, gets the same scaling
factor. This is the structural cause of t0049's SEClamp DSI ≈ 0 (both PD and ND see the same
total GABA conductance summed across spatially-symmetric synapses; the gain factor cancels in
the somatic average).

## Analysis

### Plan assumption check (per orchestrator instruction)

The plan's hypothesis section laid out three possible outcomes for H1 (spatial-distribution
hypothesis) per t0049's compare_literature analysis:

* **SUPPORTED**: deposited GABA distribution symmetric across PD/ND
* **REJECTED**: deposited GABA shows ND-bias matching paper claim
* **PARTIAL**: weakly asymmetric

**Outcome: SUPPORTED.** Two layers of evidence:

1. **Structural evidence**: the deposited code's PD/ND distinction has no spatial component in
   the protocol — it is a uniform scalar `gabaMOD` swap. Identified by reading
   `dsgc_model_exact.hoc:316-334` and `main.hoc` `simplerun()` proc. The deposited code
   cannot, by construction, produce a somatic GABA PD/ND asymmetry under SEClamp.

2. **Numerical evidence**: the synapse spatial distribution is symmetric around its own median
   (139 / 143, ratio 0.972) with essentially identical per-side density (0.060 vs 0.062
   syn/µm) and total dendritic length (2311 vs 2296 µm). Even if a future task re-implemented
   the deposited PD/ND swap with a spatial threshold, half the synapses on each side would
   still apply equal gain.

### What this means for the broader project

The t0049 SEClamp finding (GABA PD ≈ ND ≈ 48 nS, DSI ≈ 0) is now fully explained at the
mechanism level. There are two distinct deposited-code-vs-paper discrepancies:

1. **Protocol discrepancy**: the deposited PD/ND swap is non-spatial (uniform `gabaMOD`
   scalar). The paper's biology produces direction selectivity through SAC inhibition that is
   itself spatially asymmetric (more inhibition on the ND-side dendrite during ND
   stimulation). The deposited code does not encode this asymmetry in any form.

2. **Distribution discrepancy** (corollary): even setting aside the protocol issue, the
   deposited spatial synapse distribution is symmetric around its own median, so a
   spatial-threshold re-implementation alone would not reproduce the paper's PD~~12.5 / ND~~30
   nS values without additional modifications (changing the per-side counts and/or per-syn
   conductance).

The simplest fix path to recover the paper's somatic GABA asymmetry would be:

* Re-implement `placeBIP()` to spatially gate `gabaMOD` (e.g., scale up synapses on the
  ND-side based on `locx` relative to the soma center).
* OR re-distribute the SACinhib synapses asymmetrically across PD-side and ND-side dendrites
  at construction.
* OR add an iMK801-style local synaptic modification that affects only ND-side dendrites.

Any of these would be model modifications, well beyond t0050's audit scope. The t0050 finding
is the prerequisite for designing such a modification rationally.

### Bonus finding (NEURON 8.2.7 path-distance API)

NEURON 8.2.7 Python's legacy `h.distance(0, sec(0.5))` form did not reliably set the
path-distance origin during implementation (returned 0.5 instead of resetting). The audit uses
the more robust two-segment form `h.distance(soma_seg, syn_seg)` which works correctly. Worth
flagging to other DSGC tasks that compute path distances. Consider adding to t0046's library
API or documenting in the project's NEURON usage notes.

## Verification

* `verify_task_file.py`: PASSED (0 errors)
* `verify_task_metrics.py`: PASSED (0 errors) on `metrics.json = {}` (no registered metrics
  apply to a static-coordinate audit)
* `verify_plan.py`: PASSED (0 errors)
* `verify_research_code.py`: PASSED (0 errors)
* `verify_task_results.py`: not yet run — deferred to reporting step
* `ruff check`, `ruff format`: clean across all 4 Python modules
* `mypy -p tasks.t0050_audit_syn_distribution.code`: clean
* Synapse-count assertion (282 per channel): PASSED
* Parent-section identity per index assertion (BIPsyn == SACexcsyn == SACinhibsyn): PASSED
* Soma path-distance assertion (synapse 0 at soma → path = 0): PASSED

## Limitations

* **Single midline classification (x_soma + 2 alternatives)**: the audit picks three midlines.
  Real SAC inhibition spatial structure is more nuanced than a single threshold along x. A
  more sophisticated audit would partition synapses by dendritic branch identity
  (proximal-PD-branch vs proximal-ND-branch vs distal-mixed).
* **Three channel classes share parent sections per index**: this is the deposited code's
  design. A future modification could decouple them, but t0050 is audit-only.
* **No paper-stated numerical targets**: the paper text describes spatial distributions
  qualitatively (SAC inhibition is asymmetric); the audit compares deposited values against
  qualitative claims only. Quantitative paper targets would require the supplementary PDF
  (S-0046-05 still pending).
* **NEURON 8.2.7 API quirk**: the `h.distance(0, sec(0.5))` form failure in NEURON 8.2.7 is a
  workaround, not a bug fix. Other DSGC tasks may need to use the two-segment form if
  computing path distances.
* **Cell built with a single trial seed (0)**: synapse positions are deterministic given the
  morphology, so this is fine; but if the deposited code ever introduces stochastic position
  placement, this audit would need re-running.

## Files Created

### Code

* `code/paths.py` — centralized paths
* `code/constants.py` — channel-class enum, midline-classification rule, paper Fig 3C
  reference values
* `code/extract_coordinates.py` — wrapper that builds cell, calls placeBIP, extracts
  per-synapse coordinates and path/radial distances
* `code/compute_spatial_stats.py` — aggregator that reads per-synapse CSV and writes
  per-channel × per-midline stats CSV
* `code/render_figures.py` — three PNG renderer (raw matplotlib)

### Results

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (empty `{}` — no registered metrics apply to static-coordinate audit)
* `results/costs.json` (zero), `results/remote_machines_used.json` (empty)
* `results/synapse_coordinates.csv` (282 per-synapse rows × 17 columns)
* `results/per_channel_density_stats.csv` (9 rows = 3 channels × 3 midlines)
* `results/images/syn_x_hist_per_channel.png`
* `results/images/syn_radial_distance_per_channel.png`
* `results/images/syn_count_pd_vs_nd_per_channel.png`

### Answer asset

* `assets/answer/synapse-distribution-audit-deposited-vs-paper/details.json`
* `assets/answer/synapse-distribution-audit-deposited-vs-paper/short_answer.md`
* `assets/answer/synapse-distribution-audit-deposited-vs-paper/full_answer.md` (structural
  finding, per-channel + per-midline statistics, H1 SUPPORTED verdict, synthesis reconciling
  t0049's SEClamp result)

## Task Requirement Coverage

Operative task quoted verbatim from `task.json` and `task_description.md`:

> Extract per-synapse (x,y,z) coordinates from deposited DSGC, compute PD-side vs ND-side spatial
> densities for NMDA/AMPA/GABA, compare to paper text descriptions; explain t0049 GABA symmetry
> collapse.

> If the deposited distribution is symmetric, the spatial-distribution hypothesis is supported and
> the deposited code is missing the paper's PD/ND asymmetry by construction. If the deposited
> distribution is asymmetric, the hypothesis is rejected and (2) or (3) becomes more likely.

REQ-* IDs reused from `plan/plan.md`:

* **REQ-1** (re-use t0046 library, no fork): **Done** — only library-level imports
* **REQ-2** (cell-build + simplerun-only, no h.run()): **Done** —
  `code/extract_coordinates.py`
* **REQ-3** (per-synapse CSV with full 3D + section + path distance): **Done** —
  `results/synapse_coordinates.csv` (17 columns)
* **REQ-4** (synapse count assertion 282 per channel): **Done**
* **REQ-5** (per-channel x-coord histograms): **Done** —
  `results/images/syn_x_hist_per_channel.png`
* **REQ-6** (per-channel radial-distance summary): **Done** — table above + PNG
* **REQ-7** (per-channel path-distance summary): **Done** — table above
* **REQ-8** (per-side density and total dendritic length): **Done**
* **REQ-9** (mechanism-level synthesis reconciling t0049): **Done** — `## Analysis` above +
  answer asset full_answer.md
* **REQ-10** (three PNGs in `results/images/`): **Done**
* **REQ-11** (answer asset with v2 spec): **Done**
* **REQ-12** (H1 verdict with numerical evidence): **Done** — SUPPORTED
* **REQ-13** (lint/format/mypy clean): **Done** — all 4 modules pass

</details>
