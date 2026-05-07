# Diagnose why t0090 procedural cells produce no action potentials

## Motivation

Task t0090 delivered the 14-knob procedural DSGC morphology generator and ran it through a
60-morphology Phase D verification under the t0083 best-cell parameter vector. The result was that
**0 / 60 cells fired any spikes**: 51 / 60 collapsed to NaN voltage during the early stability
check, and the remaining 9 sat silent (peak Vm = -70 mV exactly for 6 of them, only -66 to -67 mV
for the other 3) across all 8 directions of the bar protocol. The Phase F Bed-B reproducibility
check, Phase G.2 NMDA calibration, and Phase G.3 NaP knockout all bottomed out on this silence: G.2
produced all-NaN per-spine recordings, G.3 had no non-zero baseline to knock down, and Phase F had
no measurable DSI to compare against the t0083 Pareto reference.

This silence is the gating blocker for **t0091**'s planned 68-d joint NSGA-II run. Warm-start
anchors do not exist; LHS bound tightening cannot be done meaningfully because the 9 STABLE cells
are also silent; any joint optimisation would burn its budget on infeasible morphologies. Before
t0091 can launch, the question "why does the procedural BedB-equivalent cell, under the exact t0083
best-cell channels, fail to spike?" has to be answered concretely, with a fix in hand.

This task is the focused diagnostic that answers that question. It does not attempt the full joint
optimisation; it does not retune the BedB base point exhaustively; it does not enlarge the
morphology bounds. It compares the procedural BedB-equivalent cell to the t0024 hand-coded Bed B
cell side-by-side under identical channels and identical synaptic input, isolates the structural
difference that causes silence, and lands a fix as a new generator-side library that t0091 can
adopt.

## Scope

### In Scope

* Build the procedural BedB-equivalent cell from `BEDB_BASE_POINT` via t0090's `generate_morphology`
  and the t0024 hand-coded Bed B cell via t0024's `de_rosenroll_2026_dsgc` library (or via t0080's
  `build_cell_ais.py` which wraps it for the trial driver).
* Apply the t0083 best-cell parameter vector to both cells via t0080's `apply_parameter_vector`.
* Run identical 8-direction bar trials (1400 ms each, the recorded researcher protocol's HH-on
  Vm/firing-rate mode, single seed) with bit-exact synapse placement seeds on both cells.
* Diagnose the difference. Specifically inspect: (a) `sec.L` after `pt3dadd` calls (does the
  procedural generator emit pt3d points whose Euclidean distance overrides `sec.L = node.length_um`
  silently?), (b) effective electrotonic length per-section (`L / lambda_f(100)`) compared to Bed
  B's, (c) `_section_midpoint_xy` outputs for placed synapses, (d) bar arrival times at each synapse
  vs the trial window `[0, 1400] ms`, (e) `cell.origin_xy` vs synapse XY centroid, (f) whether
  `apply_parameter_vector` actually sets channel densities on the procedural sections (no
  silent-skip on missing mechanism names).
* Implement the identified fix as a new generator helper in `tasks/t0092_.../code/` (NOT a
  modification to t0090's immutable code). The most likely shapes of the fix are: pt3dclear +
  explicit single pt3d-pair sized to L; or asymmetry transform that preserves cable length while
  only re-arranging xy; or a synapse-XY recomputation that uses the intended geometric layout rather
  than NEURON-stored pt3d midpoints.
* Re-run the 8-direction protocol on the patched procedural BedB-equivalent cell and 5 of the 9
  STABLE-but-silent cells from t0090 (different/morph_00, 13, 14, 15, 19, similar/morph_00). Pass
  criterion: at least the BedB-equivalent procedural cell, post-fix, fires under the t0083 best-cell
  channels with non-zero PD-rate AND DSI > 0.1.
* Produce one library asset (the fix module + any helper) and one answer asset (the diagnosis +
  recommended generator behaviour for t0091).

### Out of Scope

* Joint 68-d NSGA-II run (deferred to t0091).
* Retuning `BEDB_BASE_POINT` parameter values in any non-trivial way. If the diagnosis points at a
  mis-specified base point, that is recorded but the parameter retune happens in t0091's warm-up
  phase, not here.
* Repeating Phase D over the full 60-morphology sweep. The task validates fix on a small subset (1
  BedB-equivalent + 5 STABLE-from-t0090 cells); a full re-sweep belongs in t0091.
* Per-asset re-scoring of t0086 / t0088 cluster centroids.

## Approach

### Phase A — Two-cell side-by-side build

Build both cells inside the same NEURON process and dump their structural state to a single JSON
file:

* For each section: name, parent name, attach end (`PARENT_TIP_LOC`), `L` value as set in code, `L`
  value as NEURON reports it after `pt3dadd` (these may differ — that is the bug we are hunting),
  `nseg`, diameter, all `pt3dadd` x/y/z/diam tuples, computed Euclidean section length from the pt3d
  points, electrotonic length `L / lambda_f(100)`.
* For each cell: `origin_xy`, total dendritic length, soma-to-terminal max path length, soma-to-
  terminal max electrotonic distance.

Output: `data/structural_comparison.json` with two entries (`procedural_bedb`, `handcoded_bedb`).
Per-section dump with side-by-side comparable rows.

### Phase B — Synaptic-placement comparison

For both cells, run `setup_synapses_parametric(cell, n_ach=..., n_gaba=..., placer_seed=42)` with
the t0083 best-cell parameters. Record:

* For each placed synapse: section name, position-along-section, NEURON-reported (x, y) via
  `_section_midpoint_xy`, intended (x, y) from the procedural generator's `section_endpoints_xy`
  midpoint.
* Per-cell: synapse-XY centroid, synapse-XY bounding box, distribution of arrival times under the PD
  bar (direction = 0 deg) — minimum, maximum, mean, fraction of arrivals within `[0, 1400] ms`
  (the trial window).

Output: `data/synapse_comparison.json`.

### Phase C — Soma-Vm trace comparison under PD bar

For both cells, run a single PD-direction bar trial (1400 ms, HH on, single fixed seed) with
identical synapse placements (same `placer_seed`). Record the soma Vm trace at 0.1 ms resolution to
a `.npy` file per cell. Plot both traces overlaid; embed in `results_detailed.md`.

Compute and record per cell: peak Vm, time to peak, spike count using
`_count_spikes(threshold = -10 mV)`, total integrated EPSP area above -70 mV. The hand-coded Bed B
cell should produce a clear spike train under the t0083 best-cell channels (this was t0083's whole
point); if it does NOT, the bug is in `apply_parameter_vector` or the trial driver itself, not the
morphology — that flips the diagnosis to a t0080-side bug.

Output: `data/vm_trace_procedural.npy`, `data/vm_trace_handcoded.npy`,
`results/images/vm_trace_comparison.png`.

### Phase D — Diagnose and isolate root cause

From the structural and synaptic dumps, identify the structural difference(s) that explain the
soma-Vm difference. Document each candidate root cause and the evidence for/against it as a ranked
list. The 4 leading candidates from the t0090 post-mortem:

1. **pt3d-vs-L mismatch.** `pt3dadd(start, end)` with start-end Euclidean distance !=
   `node.length_um` silently overrides `sec.L`. If true, the procedural cell's effective cable
   lengths are determined by xy-coords rather than the intended `mean_segment_length_um`, breaking
   the d_lambda nseg sizing and electrotonic distance assumptions.
2. **Asymmetry transform double-stretch.** The asymmetry block applies `soma_offset` then
   `field_elongation_pd` to xy-coords. For the BedB-equivalent base point both knobs are neutral
   (`soma_offset_pd_um=0, field_elongation_pd=1.0`), so this should be a no-op — but the math at
   lines 350-355 of `generator.py` may have an off-by-something even in the neutral case that
   changes endpoint coordinates.
3. **Synapse XY mismatch with bar geometry.**
   `BAR_X_START_UM = -40, BAR_VELOCITY = 1 um/ms, TSTOP_MS = 1400` is calibrated to Bed B's ~300-um
   field. If procedural cell's synapse-XY bounding box extends well beyond [-40, +1360] in the PD
   direction, some synapses fire outside the trial window and the bar's spatiotemporal envelope
   mis-aligns with the cell.
4. **Channel application skip.** `apply_parameter_vector` may silently skip sections it does not
   recognise (e.g., expects sections named with a Bed-B-specific prefix). Procedural sections are
   named `*_t90` — verify each section receives the intended `gbar_nav16`, `gbar_kdr`, etc.

For each candidate, run a targeted check (read code + dump intermediate state). Mark each as
CONFIRMED, REFUTED, or PARTIAL.

Output: `data/root_cause_analysis.json` with the 4-candidate ranked list and per-candidate verdict +
supporting numbers.

### Phase E — Implement fix

Write the fix as a new helper library at `tasks/t0092_.../code/morphology_generator_fix.py` (plus
tests). The library exposes:

```python
def generate_fixed_morphology(
    params: MorphologyParams,
    morph_seed: int,
) -> MorphologyResult: ...
```

with the same signature as t0090's `generate_morphology` but with the bug fix(es) applied. The fix
is structured as a thin wrapper if possible (call t0090's `generate_morphology` then patch the
result), or as a forked builder if a deeper change is needed (e.g., `pt3dclear` + single `pt3dadd`
pair). Ship unit tests covering the original failure case (BedB-equivalent base point) plus
determinism and no-NaN.

### Phase F — Validation re-run

Run the 8-direction protocol on the patched cells:

* The procedural BedB-equivalent base point.
* The 5 STABLE-but-silent cells from t0090 (different/morph_00, 13, 14, 15, 19; similar/morph_00).

Pass criterion: at least the BedB-equivalent procedural cell post-fix has PD-rate > 0 Hz and DSI >
0.1. Stretch goal: at least 3 of the 5 STABLE-from-t0090 cells produce spikes after the fix (the
other 2 may still fail because of asymmetry-knob extreme values).

Output: `data/post_fix_verification.json` and a polar tuning panel
`results/images/post_fix_polar_tuning.png`.

### Phase G — Answer asset

Synthesise into the answer asset:

* What was the bug (or bugs)?
* How does the fix work, and what is its API?
* Does the fix recover the BedB-equivalent cell's spiking under t0083 channels?
* What does this imply for t0091 — does the joint NSGA-II run need any further preparation before
  it can be launched?

## Pass Criteria

* `data/structural_comparison.json` exists with side-by-side per-section data for both cells.
* `data/synapse_comparison.json` quantifies synapse-XY mismatch (or confirms there is none).
* `data/root_cause_analysis.json` identifies at least one CONFIRMED root cause with evidence.
* The fixed generator produces a procedural BedB-equivalent cell whose PD-rate > 0 Hz and DSI
  > 0.1 under the t0083 best-cell parameter vector.
* Library asset `procedural_dsgc_morphology_generator_fix` and answer asset
  `t0090-procedural-cell-silence-root-cause` both pass their schema verifiers.

**Acceptable negative**: if Phase D identifies that the hand-coded Bed B cell ALSO fails to spike
under the t0083 best-cell channels (i.e., the bug is in t0080's trial driver or in how the t0083
parameter vector was loaded), record that as the root cause and stop — Phase E and F become a
separate downstream task targeting `apply_parameter_vector` or `load_default_params.py` rather than
the generator.

## Compute and Budget

* **Local 64-core EPYC** for all phases. No remote machines required.
* **Total cost**: $0. Single-process NEURON simulations on the order of seconds-to-minutes per cell;
  comfortably fits in the local budget.
* Budget remaining after t0090: ~$4.45. This task does not move the project total.

## Time Estimation

* Phase A (structural dump): ~30 min.
* Phase B (synapse comparison): ~30 min.
* Phase C (Vm trace comparison): ~15 min.
* Phase D (root cause analysis): ~1-2 hours.
* Phase E (fix implementation): ~2-4 hours depending on whether a thin patch suffices or a builder
  rewrite is needed.
* Phase F (validation re-run): ~30 min.
* Phase G (answer asset): ~30 min.
* **Total wall-clock**: ~1 day.

## Expected Assets

* **Library asset (1)**: `assets/library/procedural_dsgc_morphology_generator_fix/` — the patched
  generator. Categories: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`.
* **Answer asset (1)**: `assets/answer/t0090-procedural-cell-silence-root-cause/` — the diagnosis
  synthesis. Question: "Why do t0090's procedural cells produce zero spikes under the t0083
  best-cell channel set, and what is the fix?". Categories: `compartmental-modeling`,
  `direction-selectivity`.

## Risks and Fallbacks

* **The hand-coded Bed B cell also fails to spike under t0083 best-cell channels.** Then the bug is
  in t0080's `apply_parameter_vector` or in the t0083 parameter-vector loader — not in the t0090
  generator. Record as the root cause, scope a follow-up task targeting t0080 / t0083.
* **The procedural cell's structural dump matches the hand-coded cell's section-for-section but the
  soma-Vm traces still diverge.** That points at a subtle NEURON-state bug (e.g., the procedural
  cell's sections are not in the same `h.SectionList` as the hand-coded cell's, so some background
  mechanism enumerator skips them). Investigate via `for sec in h.allsec(): print(sec.name())` and
  `h.distance(soma(0.5), terminal(0.5))`.
* **Fix changes the generator's API enough that t0091 needs a new wrapper.** Expose
  `generate_fixed_morphology` as a drop-in replacement so t0091's NSGA-II loop just swaps the import
  path; no signature changes.
* **More than one root cause is involved.** Apply each fix incrementally and document which one was
  load-bearing.

## Verification Criteria

* `verify_task_file.py t0092_diagnose_morphology_generator_silence` passes.
* `verify_logs.py t0092_diagnose_morphology_generator_silence` passes.
* `verify_plan.py`, `verify_task_results.py`, `verify_suggestions.py` all pass.
* The library asset and answer asset both pass their respective verifiers.
* `data/post_fix_verification.json` shows PD-rate > 0 and DSI > 0.1 for the BedB-equivalent cell.

## Cross-References

* **t0024_port_de_rosenroll_2026_dsgc** — hand-coded Bed B cell (the "ground truth" comparison).
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** — `apply_parameter_vector`,
  `setup_synapses_parametric`, `run_one_trial`, `_section_midpoint_xy`, `_bar_arrival_times`. The
  trial-driver harness consumed by both cells in this task.
* **t0083_bedb_v3_extend_nsga2_gen8plus** — source of the best-cell parameter vector.
* **t0090_morphology_generator_diversity_test** — the task whose silence finding motivates this
  diagnostic. Uses its committed `BEDB_BASE_POINT` and `generate_morphology`. The fix in this task
  does NOT modify t0090; it adds a new sibling library.
* Source suggestion: **S-0090-01** (Retune BEDB_BASE_POINT to elicit spikes under the t0083 channel
  set). This task generalises the suggestion: rather than retuning parameter values, it diagnoses
  the structural cause of silence and patches the generator.
