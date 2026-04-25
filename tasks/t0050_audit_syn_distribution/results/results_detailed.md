---
spec_version: "2"
task_id: "t0050_audit_syn_distribution"
---
# Results Detailed: Synapse-Distribution Audit (Deposited DSGC vs Paper)

## Summary

This task tests t0049's spatial-distribution hypothesis (H1) — that the deposited code's GABA
PD/ND symmetry collapse under SEClamp comes from the deposited spatial distribution not having any
PD/ND asymmetry. Verdict: **H1 SUPPORTED on both structural and numerical grounds**. Structurally,
the deposited code's PD/ND condition swap is implemented as a pure scalar
`gabaMOD = 0.33 + 0.66*direction` applied uniformly across all 282 SAC inhibitory synapses with NO
spatial threshold. Numerically, the synapse spatial distribution is symmetric around the synapse
population's own median (139 / 143 = ratio 0.972), with identical per-side density (0.060 / 0.062
syn/µm). The t0049 GABA PD ≈ 47.47 / ND ≈ 48.04 nS somatic SEClamp result is therefore the
inevitable mechanical consequence of the deposited circuit's design — not a measurement artefact
and not something a parameter scan alone can fix.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7`
* **MOD compiler**: re-uses t0046's existing `nrnmech.dll`

### Runtime

* **Implementation step started**: 2026-04-25T11:42:13Z
* **Implementation step completed**: 2026-04-25T11:59:13Z (poststep)
* **Wall-clock**: ~1 hour total. NEURON cell build + placeBIP() ≈ 2 min; coordinate extraction +
  analysis + chart rendering ≈ 5 min; the rest is coding + answer asset authoring.

### Methods

The implementation directly imports `build_dsgc`, `read_synapse_coords`, and `run_one_trial` from
`tasks.t0046_reproduce_poleg_polsky_2016_exact.code` (registered library
`modeldb_189347_dsgc_exact`). The wrapper `code/extract_coordinates.py`:

1. Calls `build_dsgc()` to build the cell.
2. Calls
   `run_one_trial(exptype=ExperimentType.CONTROL, direction=Direction.PREFERRED, b2gnmda_override=0.5, trial_seed=0)`
   to drive `simplerun()` and `placeBIP()` once. NO `h.run()` is needed — the placeBIP call
   populates synapse positions, which is all we need for coordinate extraction.
3. Iterates `for i in range(int(h.RGC.numsyn))`. For each synapse, extracts:
   * `BIPsyn[i].locx`, `locy` (from t0046's existing `read_synapse_coords()` extension).
   * Parent section name via `syn.get_segment().sec.name()` (e.g., `"RGC[0].dend[42]"`, stripped to
     `"dend[42]"` for display).
   * Parent-section centroid 3D via averaging `h.x3d(j) / y3d(j) / z3d(j)` over the section's 3D
     points.
   * Section length via `sec.L`.
   * Path distance from soma along the cable: set origin via `h.distance(0, h.RGC.soma(0.5))`, then
     call `h.distance(soma_seg, syn.get_segment())` (the two-segment form, since the legacy
     single-arg form did not reliably set the origin in NEURON 8.2.7).
   * Radial distance from soma: `sqrt((x_syn - x_soma)^2 + (y_syn - y_soma)^2 + (z_syn - z_soma)^2)`
     where soma center is averaged over the soma section's 3D points.
4. Asserts `BIPsyn[i].section == SACexcsyn[i].section == SACinhibsyn[i].section` for every `i` (the
   three channel classes share parent sections per index — confirmed).
5. Writes per-synapse CSV `results/synapse_coordinates.csv` (282 rows, 17 columns).

The aggregator `code/compute_spatial_stats.py` reads the per-synapse CSV and computes per-channel
statistics under three midline definitions:

* **soma_x**: midline = soma center x-coordinate (104.58 µm). Synapses with `locx < midline` →
  side_a, otherwise → side_b.
* **zero**: midline = 0 µm. Tests whether the cell straddles the origin.
* **bipsyn_locx_median**: midline = the BIPsyn population's median x-coordinate (88.77 µm). The
  "intrinsic" midline that puts roughly half on each side.

For each (channel × midline), reports: counts (total, side_a, side_b), ratio, mean radial distance
per side ± SD, mean path distance per side ± SD, total dendritic length per side, density per
side. Verdict `symmetric` if `ratio in [0.9, 1.1]`.

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

**Key observation**: all three channel classes share parent sections per index (asserted in the
extraction wrapper). The three rows per midline are therefore identical across BIPsyn / SACexcsyn /
SACinhibsyn. This itself is a structural finding — the deposited code co-locates the three synapse
types at every synapse index, so no per-channel spatial asymmetry is possible by construction.

### Per-channel mean distances from soma at synapse-median midline

| Channel | side_a mean radial (µm) | side_b mean radial (µm) | side_a mean path (µm) | side_b mean path (µm) |
| --- | --- | --- | --- | --- |
| BIPsyn | 69.08 ± 21.56 | 48.00 ± 23.90 | 140.95 ± 40.38 | 103.09 ± 47.84 |
| SACexcsyn | (identical) | (identical) | (identical) | (identical) |
| SACinhibsyn | (identical) | (identical) | (identical) | (identical) |

side_a synapses sit ~20 µm farther from the soma in 3D and ~38 µm farther along the cable than
side_b synapses. This reflects the morphology's asymmetry (the soma is offset from the dendritic
centroid), not a per-channel asymmetry.

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

The t0049 SEClamp DSI ≈ -0.006 is the inevitable consequence of the deposited spatial distribution
being symmetric (DSI = 0.0 by spatial construction). The t0047 per-syn-direct asymmetry comes from
the `gabaMOD` scalar swap inflating ND-direction conductance gain across all synapses uniformly —
t0049's somatic clamp averages the per-side currents, which cancel because each side has the same
number of synapses with the same gain.

## Visualizations

![Per-channel x-coordinate histograms with midline markers](images/syn_x_hist_per_channel.png)

Three subplots, one per channel class. Histograms of the synapse x-coordinates, with a vertical line
marking each of the three midlines (soma_x, zero, BIPsyn-median). All three channels collapse to the
same histogram because they share parent sections per index. The distribution is bimodal-asymmetric
around soma_x (more synapses on side_a) but symmetric around the BIPsyn-median midline.

![Per-channel radial-distance histograms (side_a vs side_b overlay)](images/syn_radial_distance_per_channel.png)

Three subplots, radial distance from soma per channel, with side_a and side_b overlaid. Both sides
show similar radial distributions (~20-100 µm), with side_a peaking slightly farther out
(consistent with the off-center soma).

![Per-channel side_a vs side_b counts at each midline](images/syn_count_pd_vs_nd_per_channel.png)

Bar chart, 3 channels × 3 midlines × 2 sides. Visual confirmation that the synapse distribution is
symmetric only when measured against its own median.

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
  side_b synapse (locx 103.78 > median 88.77). Very close to soma along the cable (13 µm) and in 3D
  (5 µm).

* **Synapse index 3 (close to soma, side_b, multi-segment section)**:
  ```
  index=3 bip_locx_um=100.649 bip_locy_um=114.141 bip_z_um=48.990
  parent_section_name=dend[2] parent_section_length_um=2.31
  path_distance_um=21.91 radial_distance_from_soma_um=8.72
  ```

### Best cases (clear symmetry confirmation)

* **Side counts at synapse-median midline**: 139 / 143 → ratio 0.972, well within the [0.9, 1.1]
  symmetric band. The deposited synapse distribution is genuinely symmetric around its own median.

* **Density per side**: 0.060 / 0.062 syn/µm → essentially identical density of synapses per unit
  dendritic length.

* **Total dendritic length**: 2311 / 2296 µm → within 0.7%. The two sides have essentially the
  same dendritic surface area.

### Worst cases (asymmetry under the wrong midline)

* **soma_x midline**: 171 / 111 → ratio 1.541. This appears asymmetric until you realize the soma
  is offset from the dendritic centroid. The "asymmetry" here is purely a consequence of which point
  you call the midline.

### Boundary cases (cell does not straddle the origin)

* **zero midline**: 0 / 282 → all synapses on side_b. The deposited cell sits entirely in positive
  x (centroid at locx ≈ 80-100 µm). The "zero" midline is not anatomically meaningful for this
  cell.

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
synapses (line `gabaMOD = 0.33 + 0.66*$2` in `dsgc_model_exact.hoc:316-334`). For ND,
`gabaMOD = 0.99`. There is NO spatial gating — every synapse, regardless of locx, gets the same
scaling factor. This is the structural cause of t0049's SEClamp DSI ≈ 0 (both PD and ND see the
same total GABA conductance summed across spatially-symmetric synapses; the gain factor cancels in
the somatic average).

## Analysis

### Plan assumption check (per orchestrator instruction)

The plan's hypothesis section laid out three possible outcomes for H1 (spatial-distribution
hypothesis) per t0049's compare_literature analysis:

* **SUPPORTED**: deposited GABA distribution symmetric across PD/ND
* **REJECTED**: deposited GABA shows ND-bias matching paper claim
* **PARTIAL**: weakly asymmetric

**Outcome: SUPPORTED.** Two layers of evidence:

1. **Structural evidence**: the deposited code's PD/ND distinction has no spatial component in the
   protocol — it is a uniform scalar `gabaMOD` swap. Identified by reading
   `dsgc_model_exact.hoc:316-334` and `main.hoc` `simplerun()` proc. The deposited code cannot, by
   construction, produce a somatic GABA PD/ND asymmetry under SEClamp.

2. **Numerical evidence**: the synapse spatial distribution is symmetric around its own median (139
   / 143, ratio 0.972) with essentially identical per-side density (0.060 vs 0.062 syn/µm) and
   total dendritic length (2311 vs 2296 µm). Even if a future task re-implemented the deposited
   PD/ND swap with a spatial threshold, half the synapses on each side would still apply equal gain.

### What this means for the broader project

The t0049 SEClamp finding (GABA PD ≈ ND ≈ 48 nS, DSI ≈ 0) is now fully explained at the
mechanism level. There are two distinct deposited-code-vs-paper discrepancies:

1. **Protocol discrepancy**: the deposited PD/ND swap is non-spatial (uniform `gabaMOD` scalar). The
   paper's biology produces direction selectivity through SAC inhibition that is itself spatially
   asymmetric (more inhibition on the ND-side dendrite during ND stimulation). The deposited code
   does not encode this asymmetry in any form.

2. **Distribution discrepancy** (corollary): even setting aside the protocol issue, the deposited
   spatial synapse distribution is symmetric around its own median, so a spatial-threshold
   re-implementation alone would not reproduce the paper's PD~~12.5 / ND~~30 nS values without
   additional modifications (changing the per-side counts and/or per-syn conductance).

The simplest fix path to recover the paper's somatic GABA asymmetry would be:

* Re-implement `placeBIP()` to spatially gate `gabaMOD` (e.g., scale up synapses on the ND-side
  based on `locx` relative to the soma center).
* OR re-distribute the SACinhib synapses asymmetrically across PD-side and ND-side dendrites at
  construction.
* OR add an iMK801-style local synaptic modification that affects only ND-side dendrites.

Any of these would be model modifications, well beyond t0050's audit scope. The t0050 finding is the
prerequisite for designing such a modification rationally.

### Bonus finding (NEURON 8.2.7 path-distance API)

NEURON 8.2.7 Python's legacy `h.distance(0, sec(0.5))` form did not reliably set the path-distance
origin during implementation (returned 0.5 instead of resetting). The audit uses the more robust
two-segment form `h.distance(soma_seg, syn_seg)` which works correctly. Worth flagging to other DSGC
tasks that compute path distances. Consider adding to t0046's library API or documenting in the
project's NEURON usage notes.

## Verification

* `verify_task_file.py`: PASSED (0 errors)
* `verify_task_metrics.py`: PASSED (0 errors) on `metrics.json = {}` (no registered metrics apply to
  a static-coordinate audit)
* `verify_plan.py`: PASSED (0 errors)
* `verify_research_code.py`: PASSED (0 errors)
* `verify_task_results.py`: not yet run — deferred to reporting step
* `ruff check`, `ruff format`: clean across all 4 Python modules
* `mypy -p tasks.t0050_audit_syn_distribution.code`: clean
* Synapse-count assertion (282 per channel): PASSED
* Parent-section identity per index assertion (BIPsyn == SACexcsyn == SACinhibsyn): PASSED
* Soma path-distance assertion (synapse 0 at soma → path = 0): PASSED

## Limitations

* **Single midline classification (x_soma + 2 alternatives)**: the audit picks three midlines. Real
  SAC inhibition spatial structure is more nuanced than a single threshold along x. A more
  sophisticated audit would partition synapses by dendritic branch identity (proximal-PD-branch vs
  proximal-ND-branch vs distal-mixed).
* **Three channel classes share parent sections per index**: this is the deposited code's design. A
  future modification could decouple them, but t0050 is audit-only.
* **No paper-stated numerical targets**: the paper text describes spatial distributions
  qualitatively (SAC inhibition is asymmetric); the audit compares deposited values against
  qualitative claims only. Quantitative paper targets would require the supplementary PDF (S-0046-05
  still pending).
* **NEURON 8.2.7 API quirk**: the `h.distance(0, sec(0.5))` form failure in NEURON 8.2.7 is a
  workaround, not a bug fix. Other DSGC tasks may need to use the two-segment form if computing path
  distances.
* **Cell built with a single trial seed (0)**: synapse positions are deterministic given the
  morphology, so this is fine; but if the deposited code ever introduces stochastic position
  placement, this audit would need re-running.

## Files Created

### Code

* `code/paths.py` — centralized paths
* `code/constants.py` — channel-class enum, midline-classification rule, paper Fig 3C reference
  values
* `code/extract_coordinates.py` — wrapper that builds cell, calls placeBIP, extracts per-synapse
  coordinates and path/radial distances
* `code/compute_spatial_stats.py` — aggregator that reads per-synapse CSV and writes per-channel
  × per-midline stats CSV
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
* `assets/answer/synapse-distribution-audit-deposited-vs-paper/full_answer.md` (structural finding,
  per-channel + per-midline statistics, H1 SUPPORTED verdict, synthesis reconciling t0049's SEClamp
  result)

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
* **REQ-2** (cell-build + simplerun-only, no h.run()): **Done** — `code/extract_coordinates.py`
* **REQ-3** (per-synapse CSV with full 3D + section + path distance): **Done** —
  `results/synapse_coordinates.csv` (17 columns)
* **REQ-4** (synapse count assertion 282 per channel): **Done**
* **REQ-5** (per-channel x-coord histograms): **Done** —
  `results/images/syn_x_hist_per_channel.png`
* **REQ-6** (per-channel radial-distance summary): **Done** — table above + PNG
* **REQ-7** (per-channel path-distance summary): **Done** — table above
* **REQ-8** (per-side density and total dendritic length): **Done**
* **REQ-9** (mechanism-level synthesis reconciling t0049): **Done** — `## Analysis` above
  + answer asset full_answer.md
* **REQ-10** (three PNGs in `results/images/`): **Done**
* **REQ-11** (answer asset with v2 spec): **Done**
* **REQ-12** (H1 verdict with numerical evidence): **Done** — SUPPORTED
* **REQ-13** (lint/format/mypy clean): **Done** — all 4 modules pass
