# Audit Deposited GABA/NMDA/AMPA Synapse Spatial Distribution vs Poleg-Polsky 2016 Text

## Motivation

Task t0049 measured per-channel synaptic conductance under a somatic SEClamp on the deposited DSGC
(gNMDA = 0.5 nS, exptype = control) and found that the GABA PD/ND symmetry collapses entirely (PD =
47.47 nS, ND = 48.04 nS, DSI ≈ -0.006), contradicting Poleg-Polsky 2016's stated PD ~12.5 / ND ~30
nS (DSI ≈ -0.41). The compare_literature analysis identified three candidate mechanisms for this
discrepancy:

1. **Spatial-distribution hypothesis**: deposited GABA synapses are distributed roughly equally
   across PD-side and ND-side dendrites, so the somatic measurement sees no asymmetry. The paper's
   actual GABA distribution may put more synapses on ND-side dendrites.
2. **Cable-filtering hypothesis**: deposited cable filtering averages out local asymmetry by the
   time the current reaches the soma; paper's morphology may preserve the asymmetry better.
3. **Modality-of-paper-measurement hypothesis**: paper's PD ~12.5 / ND ~30 nS may reflect a sublocal
   dendritic measurement, not a true somatic SEClamp.

Hypothesis (1) is the most directly testable from the deposited code alone — by extracting the (x,
y, z) coordinates of every BIP (NMDA + AMPA), SACexc, and SACinhib synapse instance and computing
per-direction spatial densities. If the deposited distribution is symmetric, the
spatial-distribution hypothesis is supported and the deposited code is missing the paper's PD/ND
asymmetry by construction. If the deposited distribution is asymmetric, the hypothesis is rejected
and (2) or (3) becomes more likely.

This task does not modify the model — it is a measurement and audit of what is already in the
deposited code, plus a side-by-side comparison with the paper's text.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or fork.
* Build the cell once via
  `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell. build_dsgc()`, then call
  `placeBIP()` (control condition, gNMDA = 0.5 nS, exptype = 1). Extract for every synapse the (x,
  y, z) center coordinate of its parent section, plus the section name and section length.
* Compute per-channel-class spatial statistics:
  * **Per-channel synapse counts**: total, PD-side, ND-side. (Reproduce/confirm the 282 count from
    t0046's audit.)
  * **Per-channel x-position histograms**: PD-side dendrites are at one extreme of the x-axis (or
    whichever axis the deposited code uses for the wave-stimulus direction); ND- side at the other.
    The `placeBIP()` `gabaMOD` swap protocol uses x-position to determine PD vs ND. Compute the
    bimodal histogram per channel.
  * **Per-channel mean radial distance from soma**: distance in 3D from soma center to each synapse,
    summarized as mean ± SD. Also broken down by PD-side vs ND-side.
  * **Per-channel mean dendritic-tree distance from soma** (path length along the cable): using
    `h.distance(0, sec(0.5))` from the soma. Mean ± SD per channel × side.
  * **PD-side vs ND-side density**: number of synapses per unit dendritic length on each side, per
    channel.
* Compare these statistics against the paper's text descriptions:
  * Paper text states 177 BIP synapses; deposited code has 282 (already catalogued as discrepancy
    entry 4 in t0046's audit).
  * Paper text describes the spatial distribution of GABA synapses (likely SAC-derived, asymmetric
    across PD/ND).
  * Paper text describes the AMPA + NMDA distribution (BIP synapses, likely symmetric).
* Identify the synapse-distribution discrepancies that explain the t0049 GABA symmetry collapse.

### Out of Scope

* Any modification to the model (synapse positions, counts, or kinetics). This task is audit and
  measurement only.
* Re-running the SEClamp protocol (already done in t0049).
* Higher-N reruns or new sweeps (covered by S-0046-01 / S-0048-04).
* Reading the supplementary PDF for paper protocol details (covered by S-0046-05; if the PDF is
  fetched manually before this task starts, use it; otherwise rely on paper main text and t0046's
  research_papers.md notes).
* Implementing iMK801 or any other model modification.

## Reproduction Targets

There are no quantitative reproduction targets per se; this task produces measurements that the
paper does not state numerically. The audit compares the extracted spatial statistics against the
paper's qualitative claims:

| Paper claim | Expected if H1 (spatial-distribution discrepancy) |
| --- | --- |
| GABA stronger on ND side | Deposited GABA density should NOT be ND-biased |
| BIP (AMPA+NMDA) symmetric | Deposited BIP density should be symmetric |
| 177 BIP synapses | Deposited has 282 (already known) |

If H1 is supported, the deposited GABA spatial distribution is symmetric across PD/ND, with PD-side
count ≈ ND-side count. The paper's GABA ND-bias is then inherent to the ND-side distribution
itself, and the deposited code's `gabaMOD` swap protocol cannot reproduce it because it scales gain
symmetrically without changing positions.

## Approach

The implementation extracts synapse coordinates via:

1. Build cell via `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell.build_dsgc()`.
2. Call `simplerun(exptype=1, direction=0)` to populate `placeBIP()` with the control conditions.
3. Iterate over `h.RGC.BIPsyn[i]`, `h.RGC.SACexcsyn[i]`, `h.RGC.SACinhibsyn[i]` for
   `i in range(int(h.RGC.numsyn))`. For each synapse, extract:
   * Parent section name (via `syn.get_segment().sec.name()`).
   * Center segment (x, y, z) via `h.x3d`, `h.y3d`, `h.z3d` on the parent section's center.
   * Section path-distance from soma via `h.distance(0, syn.get_segment())` (after setting
     `h.distance(0, h.RGC.soma(0.5))` as the origin).
   * Section length via `sec.L`.
4. Build a per-synapse DataFrame and compute per-channel spatial statistics.

The deposited `placeBIP()` (per t0049's research_code.md) uses the x-coordinate of the synapse to
determine PD vs ND-side: synapses with x > 0 are on one side, x < 0 on the other. Confirm this
convention by inspecting `placeBIP()` source code in `main.hoc` / `dsgc_model_exact.hoc`.

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
* Per-channel PD-side vs ND-side count ratio reported numerically with verdict (symmetric if ratio
  in [0.9, 1.1]; asymmetric otherwise).
* H1 (spatial-distribution hypothesis) verdict: SUPPORTED, REJECTED, or PARTIAL with numerical
  evidence. SUPPORTED if GABA is symmetric (count_pd / count_nd in [0.9, 1.1]) AND paper claims
  ND-bias. REJECTED if GABA shows ND-bias matching paper claim. PARTIAL if weakly asymmetric.
* Spatial-distribution discrepancy catalogue updated: any per-channel × per-side asymmetry or
  symmetry that differs from paper text is logged.

## Deliverables

### Answer asset (1)

`assets/answer/synapse-distribution-audit-deposited-vs-paper/` per
`meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
`full_answer.md`. The `full_answer.md` must contain:

* Question framing: "Does the deposited DSGC's spatial distribution of NMDA/AMPA/GABA synapses match
  Poleg-Polsky 2016's text descriptions, and does it explain the t0049 GABA PD/ND symmetry collapse
  under SEClamp?"
* Per-channel synapse-count and spatial-statistics table (counts, PD/ND ratio, mean radial distance,
  mean path distance, density per side).
* Per-channel x-coordinate histogram with PD/ND-side annotation.
* H1 verdict (spatial-distribution hypothesis) with numerical evidence.
* Synthesis paragraph: which of the three t0049-flagged candidate mechanisms is supported by the
  spatial audit; what the next test should be.

### Per-figure PNGs (under `results/images/`)

* `syn_x_hist_per_channel.png` — three subplots (NMDA, AMPA, GABA), each an x-coordinate histogram
  with a PD/ND median line.
* `syn_radial_distance_per_channel.png` — three subplots, radial-distance histograms PD vs ND
  overlay.
* `syn_count_pd_vs_nd_per_channel.png` — bar chart, 3 channels × 2 sides, per-channel PD vs ND
  counts side-by-side.

## Execution Guidance

* **Task type**: `data-analysis`. Optional steps to include: research-code (review t0046's
  `placeBIP()` to identify x-coordinate convention and `read_synapse_coords()` pattern), planning,
  implementation, results, suggestions, reporting. Skip research-papers / research-internet (paper
  text already covered by t0046's research_papers.md), skip compare-literature (this task IS the
  literature comparison; compare-literature would duplicate it). Skip creative-thinking.
* **Local CPU only**. No Vast.ai. The task requires a single NEURON cell build + one simplerun call
  to populate placeBIP coordinates; ~1 minute wall-clock for the measurement phase. Total task
  estimate: 1-2 hours including coding + analysis + answer asset writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **x-coordinate axis convention**: confirmed in t0049's research that `placeBIP()` uses x-position
  to determine PD vs ND. If the convention is actually y-coordinate or some other axis, the audit
  must use the correct axis. Mitigation: read `placeBIP()` source carefully before writing the
  analysis script.
* **Path-distance computation**: `h.distance()` in NEURON requires setting an origin first via
  `h.distance(0, soma(0.5))`. Forgetting to set the origin gives wrong distances. Mitigation:
  explicit assertion in the wrapper that `h.distance(0, ...)` was called before measuring synapse
  distances.
* **Section name parsing**: synapse positions returned via `syn.get_segment().sec.name()` may
  include the template prefix (e.g., `RGC[0].dend[5]`). Strip the prefix consistently.
* **Paper text descriptions may be vague**: the paper may not state the spatial distribution
  numerically. The audit will then compare deposited values against the qualitative claims only.
  Mitigation: also report what the paper does NOT state, so future tasks know what to fetch from the
  supplementary.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset + `read_synapse_coords()` pattern), t0049
  (provides the SEClamp evidence that motivates this audit).
* **Source suggestion**: S-0049-01 (HIGH priority evaluation).
* **Complements**: t0049's compare_literature analysis. This task is the direct test of hypothesis
  (1) (spatial-distribution discrepancy).
* **Precedes**: any future synapse-redistribution modification task (would adjust the deposited
  code's `placeBIP()` to better match paper text, after this audit identifies the exact
  discrepancies).

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection) passes for the answer asset.
* Per-channel synapse-count table is populated for NMDA / AMPA / GABA × PD-side / ND-side.
* Per-channel x-coordinate histograms exist as PNGs and are embedded in `results_detailed.md`.
* H1 verdict (SUPPORTED / REJECTED / PARTIAL) is stated with numerical evidence.
* `metrics.json` is `{}` (this task does not measure registered metrics; spatial counts and ratios
  are task-specific operational data, reported in `results_detailed.md` and `full_answer.md`).
