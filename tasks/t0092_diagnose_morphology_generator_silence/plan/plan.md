---
spec_version: "2"
task_id: "t0092_diagnose_morphology_generator_silence"
date_completed: "2026-05-07"
status: "complete"
---
# Plan: Diagnose t0090 Procedural Morphology Generator Silence

## Objective

Diagnose why t0090's procedural DSGC morphology generator produces zero spikes (0 / 60 cells) under
the t0083 best-cell channel parameter vector, and ship a fix as a new sibling library that t0091's
planned 68-d joint NSGA-II run can swap in as a drop-in replacement for `generate_morphology`.

The diagnosis uses a side-by-side comparison between the procedural BedB-equivalent cell built by
`tasks.t0090_morphology_generator_diversity_test.code.generator.generate_morphology` (call it
`procedural_bedb`) and the hand-coded Bed B cell built by
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.build_dsgc_cell` (call it
`handcoded_bedb`). Both cells receive the identical t0083 best-cell 54-d parameter vector via
`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params.apply_parameter_vector` and the
same synapse placer seed via
`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers.setup_synapses_parametric`. The
hand-coded cell is the "ground truth": under the t0083 vector it must spike (this is what t0083
optimised against). If the procedural cell with the same channels and the same synaptic input fails
to spike, the difference must be structural, and the structural dump from Phase A makes the cause
visible.

The leading hypothesis (from `research/research_code.md`) is a **soma area mismatch**. The
procedural soma is a single 15 µm × 15 µm cylinder with an ~706 µm² surface area, while the
t0024 hand-coded soma is a 7-pt3d frustum stack with a roughly 220 µm² surface area. A 3.2x larger
soma sinks ~3.2x more synaptic charge before reaching AP threshold, and the t0083 channel densities
were optimised against the smaller hand-coded soma. Phase A's structural dump confirms or refutes
this quantitatively; Phase E's fix is most likely a soma-pt3d patch that brings the procedural
soma's surface area into agreement with the hand-coded reference while preserving the existing
`generate_morphology` API.

**Done** means: (1) `data/structural_comparison.json` exists with side-by-side per-section data
including `sec.area()`, (2) `data/synapse_comparison.json` quantifies the synapse-XY mismatch (or
confirms there is none), (3) `data/root_cause_analysis.json` ranks the four candidate causes with
CONFIRMED / REFUTED / PARTIAL verdicts and supporting numbers, (4) the fix library
`procedural_dsgc_morphology_generator_fix` ships with at least one passing unit test, (5)
`data/post_fix_verification.json` records that the patched procedural BedB-equivalent cell has
PD-rate > 0 Hz and DSI > 0.1 under the t0083 best-cell vector, and (6) the answer asset
`t0090-procedural-cell-silence-root-cause` synthesises the diagnosis and recommends generator
behaviour for t0091.

## Task Requirement Checklist

The operative task text (from
`tasks/t0092_diagnose_morphology_generator_silence/task_description.md`):

> Build the procedural BedB-equivalent cell from `BEDB_BASE_POINT` via t0090's `generate_morphology`
> and the t0024 hand-coded Bed B cell via t0024's `de_rosenroll_2026_dsgc` library. Apply the t0083
> best-cell parameter vector to both cells via t0080's `apply_parameter_vector`. Run identical
> 8-direction bar trials (1400 ms each, the recorded researcher protocol's HH-on Vm/firing-rate
> mode, single seed) with bit-exact synapse placement seeds on both cells. Diagnose the difference.
> Implement the identified fix as a new generator helper in `tasks/t0092_.../code/` (NOT a
> modification to t0090's immutable code). Re-run the 8-direction protocol on the patched procedural
> BedB-equivalent cell and 5 of the 9 STABLE-but-silent cells from t0090. Pass criterion: at least
> the BedB-equivalent procedural cell, post-fix, fires under the t0083 best-cell channels with
> non-zero PD-rate AND DSI > 0.1. Produce one library asset (the fix module + any helper) and one
> answer asset (the diagnosis + recommended generator behaviour for t0091).

Concrete requirements derived from the task text:

* **REQ-1** — Phase A: Build both `procedural_bedb` and `handcoded_bedb` in the same NEURON
  process and dump per-section structural state (`sec.L` as written, `sec.L` as NEURON reports it
  after `pt3dadd`, `sec.nseg`, `sec.diam`, `sec.area()`, all pt3d points, computed Euclidean section
  length, electrotonic length `L / lambda_f(100)`, parent name, attach end). Per-cell totals:
  `origin_xy`, total dendritic length, soma-to-terminal max path length, soma-to-terminal max
  electrotonic distance, soma surface area. Output:
  `tasks/t0092_.../data/structural_comparison.json`. Satisfied by Step 3.

* **REQ-2** — Phase B: Place synapses with
  `setup_synapses_parametric(cell, n_ach=..., n_gaba=..., placer_seed=42)` using the t0083 best-cell
  `n_ach`, `n_gaba`, `rho0_*`, `lambda_*` parameters. For each synapse, record: section name,
  position-along-section, NEURON-reported `(x, y)` via `_section_midpoint_xy`, intended `(x, y)`
  from `section_endpoints_xy`. Per cell: synapse-XY centroid, bounding box, distribution of arrival
  times under the PD-direction bar (min, max, mean, fraction within `[0, 1400] ms`). Output:
  `tasks/t0092_.../data/synapse_comparison.json`. Satisfied by Step 4.

* **REQ-3** — Phase C: Run a single PD-direction (`direction_deg=0.0`) bar trial of length 1400 ms
  with HH on, single fixed seed `SEED_BASE`, identical synapse placements (same `placer_seed=42`).
  Record soma Vm trace at `dt=0.1 ms` to `.npy` files; compute peak Vm, time to peak, spike count
  via `_count_spikes(threshold_mv=-10)`, and integrated EPSP area above -70 mV. Outputs:
  `data/vm_trace_procedural.npy`, `data/vm_trace_handcoded.npy`,
  `results/images/vm_trace_comparison.png`. Satisfied by Step 5.

* **REQ-4** — Phase D: From the structural and synaptic dumps, rank the four leading candidate
  root causes and assign each a CONFIRMED / REFUTED / PARTIAL verdict with supporting numbers. The
  candidates are: (a) soma-area mismatch, (b) pt3d-vs-L override, (c) synapse-XY mismatch with bar
  geometry, (d) channel-application skip. Output: `tasks/t0092_.../data/root_cause_analysis.json`.
  Satisfied by Step 6.

* **REQ-5** — Phase D acceptable-negative branch: If `handcoded_bedb` ALSO fails to spike under
  the t0083 best-cell vector (i.e., the bug is in `apply_parameter_vector` or in
  `load_t0083_best_cell_param_vector`, not in t0090), record this as the root cause, write the
  answer asset accordingly, and stop before Phase E. Satisfied by Step 6.

* **REQ-6** — Phase E: Implement the identified fix as a new helper library at
  `tasks/t0092_.../code/morphology_generator_fix.py`. Expose
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int) -> MorphologyResult` with
  the same signature as t0090's `generate_morphology` so t0091 swaps the import path with no other
  code changes. The fix is a thin wrapper over `generate_morphology` (call it, then patch the
  result) where possible. Satisfied by Step 7.

* **REQ-7** — Phase E: Ship unit tests for the fix library at `tasks/t0092_.../code/test_*.py`
  covering at minimum: (a) determinism (same seed + same params → same output), (b) no-NaN
  invariant on the BedB base point, and (c) the "before fix" failure mode is now resolved (the
  specific structural property that was broken is now within tolerance of the hand-coded reference).
  Satisfied by Step 7.

* **REQ-8** — Phase F: Re-run the 8-direction bar protocol on the patched procedural
  BedB-equivalent cell. Pass criterion: PD-rate > 0 Hz **AND** DSI > 0.1. Output:
  `tasks/t0092_.../data/post_fix_verification.json` (BedB-equivalent block) and
  `tasks/t0092_.../results/images/post_fix_polar_tuning.png`. Satisfied by Step 8.

* **REQ-9** — Phase F stretch goal: Re-run the 8-direction bar protocol on 5 of the 9 STABLE-but-
  silent cells from t0090 (cell selection: `different/morph_00`, `different/morph_13`,
  `different/morph_14`, `different/morph_15`, `different/morph_19`). Stretch criterion: at least 3
  of the 5 cells produce non-zero PD-rate post-fix. Output: same file as REQ-8, with five extra
  blocks. Satisfied by Step 8.

* **REQ-10** — Library asset: Create
  `tasks/t0092_.../assets/library/procedural_dsgc_morphology_ generator_fix/` with `details.json`
  and `description.md` per `meta/asset_types/library/specification.md`. Categories:
  `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`. Satisfied by Step 9.

* **REQ-11** — Answer asset: Create
  `tasks/t0092_.../assets/answer/t0090-procedural-cell-silence- root-cause/` with `details.json`,
  `short_answer.md`, and `full_answer.md` per `meta/asset_types/answer/specification.md`. Question:
  "Why do t0090's procedural cells produce zero spikes under the t0083 best-cell channel set, and
  what is the fix?". Categories: `compartmental-modeling`, `direction-selectivity`. Satisfied by
  Step 10.

* **REQ-12** — Compute the registered metric `direction_selectivity_index` for both the pre-fix
  procedural BedB cell (expected 0.0 / undefined) and the post-fix procedural BedB cell, and write
  to `tasks/t0092_.../results/metrics.json` using the explicit multi-variant format. Satisfied by
  Step 8.

* **REQ-13** — All unit tests must pass under `uv run pytest tasks/t0092_.../code/ -v`. The fix
  library code must pass `uv run ruff check` and `uv run mypy`. Satisfied by Step 11.

## Approach

### Recommended task types

The task carries `task_types: ["data-analysis", "experiment-run", "write-library"]` in `task.json`.
All three apply: the structural and synapse dumps plus root-cause-analysis JSON are data analysis;
the pre-fix and post-fix 8-direction bar trials are experiment runs; the fix module shipped as a
sibling library is a write-library. The data-analysis Planning Guidelines drive the requirement that
`results/metrics.json` use registered keys only and that intermediate data is saved as JSON. The
experiment-run guidelines drive the requirement to record seeds, save raw Vm traces, and produce at
least 2 charts. The write-library guidelines drive the requirement that the fix module ships with
unit tests, mypy-clean type annotations, and a thorough description document.

### Why this approach over alternatives

Three alternatives were considered and rejected:

* **Alternative 1 — Retune `BEDB_BASE_POINT` parameter values until cells spike.** Rejected
  because the task description explicitly excludes parameter retuning from scope: "If the diagnosis
  points at a mis-specified base point, that is recorded but the parameter retune happens in t0091's
  warm-up phase, not here." Retuning would also mask a structural bug rather than fix it; t0091
  would inherit the bug and re-encounter it under different parameter combinations.

* **Alternative 2 — Modify t0090's `generate_morphology` directly.** Rejected because of the
  framework rule that completed tasks are immutable (`CLAUDE.md` rule 5). The fix must be a sibling
  library so t0090's verifier output and library asset remain unchanged.

* **Alternative 3 — Replace t0090's procedural builder wholesale with a pt3d-only builder modeled
  on t0024's `RGCmodelGD.hoc`.** Rejected because the task scope explicitly says the fix should be a
  "thin wrapper or shim over t0090's `generate_morphology` if possible, NOT a full rewrite". A full
  rewrite would break the 14-knob procedural API that t0091 depends on. The thin-wrapper approach
  preserves all of t0090's tested geometry generation (asymmetry transforms, branch recursion,
  terminal classification) and only patches the specific structural element the diagnosis
  identifies.

### Embedded research findings

Five facts from `research/research_code.md` ground the approach:

1. **Soma area mismatch is the leading hypothesis.** The procedural soma is built as
   `sec.L = sec.diam = 15 µm` plus a single `pt3dadd(0,0,0,15)` and `pt3dadd(0,0,15,15)` pair,
   yielding a cylinder of surface area `π · 15 · 15 ≈ 706.86 µm²`. The t0024 hand-coded soma
   uses 7 pt3d points with diameters varying from 0.88 to 10.62 µm, yielding a frustum-stack
   surface area of roughly 220 µm². A 3.2x larger soma sinks ~3.2x more synaptic charge before
   reaching AP threshold; the t0083 channel densities were optimised against the smaller hand-coded
   soma.

2. **The pt3d-vs-L override is irrelevant for the BedB base point.** For
   `soma_offset_pd_um=0, field_elongation_pd=1.0, branch_length_cv=0.1` the asymmetry transform is a
   no-op and the Euclidean distance between `node.start_xy` and `node.end_xy` equals
   `node.length_um` exactly. This removes pt3d-override as the smoking gun for BedB silence (it
   remains a concern for non-BedB asymmetry knobs, but those are out of scope for the BedB
   diagnostic).

3. **The section-list contract `all_dends == terminal_dends + non_terminal_dends` is satisfied** by
   t0090's `_materialise_neuron_sections`. `apply_parameter_vector` writes via list membership, not
   by name, so the procedural cell's `*_t90`-named sections receive the same channel densities as
   the hand-coded cell's sections.

4. **Channel insertion is correct.** t0090's `verification.py:_insert_baseline_channels` inserts
   `HHst` and `cad` on every soma + dendrite + AIS section before `apply_parameter_vector` is
   called. This rules out missing-channel-insertion as a candidate.

5. **Synapse XY readout is correct in both cells.** `_section_midpoint_xy` returns
   `(start + end) / 2` for the procedural cell's 2-pt3d sections and the geometric midpoint for the
   hand-coded cell's multi-pt3d sections; both are semantically correct.

These findings narrow Phase D from "search broadly" to "test the soma-area hypothesis first; if
confirmed, the pt3d-override is irrelevant for BedB; the synapse-XY mismatch reduces effective drive
by ~50% but does not zero it out."

### Architecture and library reuse

The diagnostic builds both cells inside the same NEURON process using the t0090 `_get_neuron_h()`
singleton, which is idempotent across both DLLs. Sections are kept alive via a module-level
`_LIVE_CELLS` list to defend against the `id()` reuse bug documented in t0090's `verification.py`.
All cross-task imports go through the registered libraries:

* `procedural_dsgc_morphology_generator` (from t0090): `generate_morphology`, `MorphologyParams`,
  `MorphologyResult`, `BEDB_BASE_POINT`, `_insert_baseline_channels`,
  `load_t0083_best_cell_param_vector`, `MorphologyParams.from_bedb_base_point()`.
* `de_rosenroll_2026_dsgc_ais_dendritic_spike` (from t0080): `apply_parameter_vector`,
  `setup_synapses_parametric`, `_section_midpoint_xy`, `_bar_arrival_times`, `_count_spikes`,
  `run_one_trial`, `build_dsgc_cell_with_ais`, `DSGCCellWithAIS`, `ParameterVector`, `ParamIndex`,
  `Tier`, `N_PARAMS=54`, `TSTOP_MS=1400`, `SEED_BASE`, `PD_DIRECTION_DEG=0`, `AP_THRESHOLD_MV`.
* `de_rosenroll_2026_dsgc` (from t0024): `build_dsgc_cell`, `BAR_X_START_UM=-40`,
  `BAR_VELOCITY_UM_PER_MS=1.0`.

Non-library helper code (`_insert_baseline_channels`) is **copied** into
`tasks/t0092_.../code/baseline_channels.py` per the framework rule that only registered libraries
may be imported across tasks; t0090's `verification.py` is not a library entry point.

### Fix shape

If Phase D confirms the soma-area hypothesis, the fix in `code/morphology_generator_fix.py`:

1. Calls `generate_morphology(params, morph_seed)` to get the standard `MorphologyResult`.
2. Inside the soma section, calls `h.pt3dclear()` then emits a 7-point pt3d stack scaled to deliver
   ~220 µm² surface area (matching the t0024 reference). The simplest implementation rescales
   either `sec.L` and `sec.diam` so the resulting cylinder has the target area, or emits a multi-
   pt3d frustum stack mirroring the t0024 ratios at scale `params.soma_diameter_um / 15`.
3. Re-runs `_compute_nseg` on the soma if necessary.
4. Returns the patched `MorphologyResult` (the dataclass is `frozen=True`, so the patch returns a
   new instance via `dataclasses.replace`; the underlying NEURON section objects are mutated in
   place).

If Phase D rejects the soma-area hypothesis and confirms a different cause (e.g., synapse-XY bar
mismatch), the fix targets that cause specifically. The wrapper-vs-fork decision is made in Step 7
based on the Phase D verdict.

## Cost Estimation

* **API calls**: $0. No LLM calls, no external services, no paid endpoints.
* **Remote compute**: $0. All NEURON simulations run on the local 64-core EPYC workstation. Each
  cell's 8-direction protocol takes seconds to a few minutes; no GPU required.
* **Other paid resources**: $0.
* **Total**: $0.

Project budget remaining after t0090: ~$4.45 of the $20.00 total (project budget per
`project/budget.json`; per-task default limit $5.00). This task does not move the project total. The
full $4.45 remains available for any follow-up tasks.

## Step by Step

### Milestone 1: Two-cell side-by-side build (REQ-1, REQ-2, REQ-3)

1. **Set up paths and constants.** Create `tasks/t0092_.../code/paths.py` with constants
   `STRUCTURAL_COMPARISON_JSON = Path("tasks/t0092_diagnose_morphology_generator_silence/data/ structural_comparison.json")`,
   `SYNAPSE_COMPARISON_JSON`, `VM_TRACE_PROCEDURAL_NPY`, `VM_TRACE_HANDCODED_NPY`,
   `ROOT_CAUSE_ANALYSIS_JSON`, `POST_FIX_VERIFICATION_JSON`,
   `IMAGES_DIR = Path("tasks/t0092_diagnose_morphology_generator_silence/results/images")`. Create
   `tasks/t0092_.../code/constants.py` with `MORPH_SEED = 1234`, `PLACER_SEED = 42`,
   `STABLE_T0090_CELLS = ["different/morph_00", "different/morph_13", "different/morph_14", "different/morph_15", "different/morph_19"]`,
   `BEDB_AREA_TARGET_UM2 = 220.0` (the t0024 reference soma surface area). Create
   `tasks/t0092_.../data/.gitkeep` so the data folder commits. Inputs: none. Outputs:
   `code/paths.py`, `code/constants.py`. Expected observable:
   `uv run python -c "from tasks.t0092_diagnose_morphology_generator_silence.code import paths, constants"`
   runs without ImportError. Satisfies setup for REQ-1 through REQ-13.

2. **Copy `_insert_baseline_channels`.** Copy the helper from
   `tasks/t0090_morphology_generator_diversity_test/code/verification.py:125-137` into
   `tasks/t0092_.../code/baseline_channels.py` as
   `def insert_baseline_channels(*, h: Any, cell: Any) -> None`. Reason: this helper is
   task-internal in t0090 and is not a library entry point; the framework forbids cross-task imports
   of non-library code. Inputs: `tasks/t0090_.../code/verification.py`. Outputs:
   `tasks/t0092_.../code/baseline_channels.py`. Expected observable:
   `uv run mypy tasks/t0092_.../code/baseline_channels.py` reports no errors. Satisfies setup for
   REQ-1.

3. **[CRITICAL] Phase A — Structural dump.** Create `tasks/t0092_.../code/structural_dump.py` with
   a `main()` that: (a) calls `_get_neuron_h()` from
   `tasks.t0090_morphology_generator_diversity_test.code.generator`; (b) builds
   `procedural_bedb = generate_morphology(params=MorphologyParams.from_bedb_base_point(), morph_seed=MORPH_SEED)`;
   (c) builds `handcoded_bedb_raw = build_dsgc_cell()` from
   `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell` and wraps it as
   `handcoded_bedb = build_dsgc_cell_with_ais(ais_length_um=31.0, ais_diameter_um=0.8)` from
   `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais`; (d) appends both cells to a
   module-level `_LIVE_CELLS: list[Any]` list to defend against `id()` reuse; (e) for each cell and
   each section, records: name, parent name, attach end (`PARENT_TIP_LOC`), `sec.L` as set in code,
   `sec.L` as NEURON reports it after `pt3dadd`, `sec.nseg`, `sec.diam`, `sec.area()`, all
   `(x3d, y3d, z3d, diam3d)` tuples, computed Euclidean section length from the pt3d points, and
   electrotonic length `sec.L / lambda_f(100)`; (f) for each cell records `origin_xy`, total
   dendritic length, soma-to-terminal max path length via `h.distance(soma(0.5), terminal(0.5))`,
   soma-to-terminal max electrotonic distance, and soma surface area; (g) writes a Pydantic model
   `StructuralComparison` to `STRUCTURAL_COMPARISON_JSON` with two entries `procedural_bedb` and
   `handcoded_bedb`. Run with
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0092_diagnose_morphology_generator_silence -- python -m tasks.t0092_diagnose_morphology_generator_silence.code.structural_dump`.
   Inputs: t0090 + t0080 + t0024 libraries. Outputs: `data/structural_comparison.json`. Expected
   observable: the JSON contains `procedural_bedb.soma.area_um2 ≈ 706` and
   `handcoded_bedb.soma.area_um2 ≈ 220` (the soma-area hypothesis would be confirmed by an ~3.2x
   ratio). Satisfies REQ-1.

4. **[CRITICAL] Phase B — Synapse-placement comparison.** Create
   `tasks/t0092_.../code/synapse_dump.py` with a `main()` that: (a) reuses the two cells built in
   Step 3 (in the same Python process via a shared cell-builder module); (b) loads the t0083
   best-cell vector via `load_t0083_best_cell_param_vector()` from t0090; (c) extracts `n_ach`,
   `n_gaba`, `rho0_ach`, `rho0_gaba`, `lambda_ach_um`, `lambda_gaba_um`, `w_ach_us`, `w_gaba_us`
   from the vector via `ParamIndex` constants in t0080; (d) calls
   `setup_synapses_parametric(cell=procedural_bedb, n_ach=..., n_gaba=..., placer_seed=PLACER_SEED, ...)`
   and the same for `handcoded_bedb`; (e) for each placed synapse records: section name,
   position-along-section, NEURON-reported `(x, y)` via `_section_midpoint_xy(h=h, section=sec)`,
   and the procedural cell's intended `(x, y)` from `result.section_endpoints_xy` midpoint (when
   applicable); (f) per cell computes synapse-XY centroid, bounding box, and the distribution of
   arrival times under the PD bar (`direction_deg=0.0`) via
   `_bar_arrival_times(syn_xy=arr, origin_xy=cell.origin_xy, direction_deg=0.0)` with the t0024
   constants `BAR_X_START_UM=-40`, `BAR_VELOCITY_UM_PER_MS=1.0`, `BAR_START_TIME_MS=0.0`,
   `TSTOP_MS=1400`; reports min, max, mean, and fraction of arrivals within `[0, 1400]` ms. Run with
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0092_diagnose_morphology_generator_silence -- python -m tasks.t0092_diagnose_morphology_generator_silence.code.synapse_dump`.
   Outputs: `data/synapse_comparison.json`. Expected observable: the procedural cell's PD-direction
   arrival distribution shows roughly 50% of synapses arriving within `[0, 1400] ms` (consistent
   with the research-code finding that ~half of symmetric procedural synapses fall outside the bar
   window). Satisfies REQ-2.

5. **[CRITICAL] Phase C — Vm trace comparison.** Create `tasks/t0092_.../code/vm_trace_dump.py`
   with a `main()` that: (a) reuses the two cells from Step 4 with synapses placed; (b) calls
   `apply_parameter_vector(cell=procedural_bedb, params=t0083_vector)` and the same for
   `handcoded_bedb`; (c) calls `insert_baseline_channels(h=h, cell=cell)` on each before
   `apply_parameter_vector`; (d) runs
   `run_one_trial(cell=cell, bundle=bundle, direction_deg=PD_DIRECTION_DEG, seed=SEED_BASE)` from
   `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver`; (e) records the soma Vm trace
   at `dt=0.1 ms` to `data/vm_trace_procedural.npy` and `data/vm_trace_handcoded.npy`; (f) computes
   peak Vm, time to peak, spike count via
   `_count_spikes(v_trace=trace, threshold_mv=AP_THRESHOLD_MV)` (typically -10 mV), integrated EPSP
   area above -70 mV; (g) plots both traces overlaid with `matplotlib` to
   `results/images/vm_trace_comparison.png` (title, x-axis "Time (ms)", y-axis "Soma Vm (mV)",
   legend `procedural_bedb` / `handcoded_bedb`). Run with
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0092_diagnose_morphology_generator_silence -- python -m tasks.t0092_diagnose_morphology_generator_silence.code.vm_trace_dump`.
   Outputs: `data/vm_trace_procedural.npy`, `data/vm_trace_handcoded.npy`,
   `results/images/vm_trace_comparison.png`. Expected observable: `handcoded_bedb` shows a clear
   spike train (this was t0083's whole point), while `procedural_bedb` shows a sub-threshold EPSP
   trace peaking around -66 mV (consistent with the t0090 finding of 0 / 60 spiking cells).
   **Validation gate**: if `handcoded_bedb` does NOT spike, halt and route into the REQ-5
   acceptable-negative branch — the bug is in `apply_parameter_vector` or
   `load_t0083_best_cell_param_vector`, not in t0090; do not proceed past Step 6. Satisfies REQ-3.

### Milestone 2: Root cause diagnosis (REQ-4, REQ-5)

6. **[CRITICAL] Phase D — Root cause analysis.** Create
   `tasks/t0092_.../code/root_cause_analysis.py` with a `main()` that loads the three JSON dumps
   (`structural_comparison.json`, `synapse_comparison.json`, derived numbers from the Vm traces) and
   produces a Pydantic `RootCauseAnalysis` ranking the four candidates. For each candidate:

   * **Candidate A — soma-area mismatch.** Test: ratio
     `procedural_bedb.soma.area_um2 / handcoded_bedb.soma.area_um2`. CONFIRMED if ratio > 2.0;
     PARTIAL if 1.5 - 2.0; REFUTED if < 1.5.

   * **Candidate B — pt3d-vs-L override.** Test: per-section
     `abs(sec.L_after_pt3d - node.length_um) / node.length_um`. CONFIRMED if any non-soma section in
     `procedural_bedb` exceeds 1% relative drift; REFUTED if all sections within 1%; PARTIAL
     otherwise. Expected REFUTED for the BedB base point per research-code.

   * **Candidate C — synapse-XY mismatch with bar geometry.** Test: fraction of `procedural_bedb`
     synapses with PD-direction arrival time outside `[0, 1400] ms`. CONFIRMED if
     > 75%; PARTIAL if 25 - 75%; REFUTED if < 25%. Expected PARTIAL (~50%) per research-code.

   * **Candidate D — channel-application skip.** Test: for each section in `procedural_bedb`'s
     `primary_dends`, `non_terminal_dends`, `terminal_dends`, soma, AIS, sample `seg.gbar_nav16` (or
     whichever channel name is exposed by the t0080 mod files) and confirm it is non-zero. CONFIRMED
     if any expected section has all-zero channel densities; REFUTED if all sections have non-zero
     densities. Expected REFUTED per research-code's verification of `apply_parameter_vector`'s
     list-membership-based dispatch.

   Each candidate's verdict block contains: `verdict` (CONFIRMED / REFUTED / PARTIAL), `evidence`
   (the supporting numbers), `explanation` (a 1-2 sentence reason). The top-level
   `RootCauseAnalysis` also names a single primary root cause (the highest-ranked CONFIRMED) and a
   recommendation for the fix shape. Run with
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0092_diagnose_morphology_generator_silence -- python -m tasks.t0092_diagnose_morphology_generator_silence.code.root_cause_analysis`.
   Output: `data/root_cause_analysis.json`. Expected observable: the JSON identifies one CONFIRMED
   primary cause (likely Candidate A — soma-area mismatch — with ratio ≈ 3.2x). If Step 5 hit
   the acceptable-negative branch (handcoded_bedb does not spike), this step records "primary cause:
   t0080-side bug in apply_parameter_vector or load_default_params" and stops there. Satisfies REQ-4
   and REQ-5.

### Milestone 3: Fix implementation and validation (REQ-6, REQ-7, REQ-8, REQ-9, REQ-12, REQ-13)

7. **[CRITICAL] Phase E — Fix implementation.** Create
   `tasks/t0092_.../code/morphology_generator_fix.py` exposing
   `def generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int) -> MorphologyResult`.
   Implementation strategy (specialised based on Step 6's verdict):

   * **If Candidate A is the confirmed primary cause** (most likely): the function calls
     `generate_morphology(params=params, morph_seed=morph_seed)`, then with the result's `soma`
     section pushed (`sec.push() / h.pop_section()`) calls `h.pt3dclear()` and emits a soma geometry
     that yields surface area ≈ `BEDB_AREA_TARGET_UM2 = 220.0` µm². The simplest patch is to set
     `sec.L = params.soma_diameter_um` and
     `sec.diam = params.soma_diameter_um * (BEDB_AREA_TARGET_UM2 / (PI * params.soma_diameter_um * params.soma_diameter_um))`
     so the cylinder area matches the target. A pt3d-equivalent patch emits two pt3d points
     `pt3dadd(0, 0, 0, new_diam)` and `pt3dadd(0, 0, params.soma_diameter_um, new_diam)`.

   * **If Candidate B or C is confirmed primary**: the wrapper instead patches the offending
     dendrite or synapse-XY logic. For B, the wrapper calls `pt3dclear()` on each non-BedB-base-
     point dendrite and re-emits a single pt3d-pair sized to `node.length_um`. For C, the wrapper
     re-computes synapse-XY using `result.section_endpoints_xy` midpoints rather than NEURON-stored
     pt3d midpoints (this requires a sibling helper `setup_synapses_with_intended_xy` in
     `code/morphology_generator_fix.py`).

   The function returns a `MorphologyResult` constructed via `dataclasses.replace(result, ...)` if
   any field needs updating (e.g., `morphometric_summary` if soma area changed). `_LIVE_CELLS`
   defense is the caller's responsibility, mirroring t0090's pattern.

   Also create `tasks/t0092_.../code/test_morphology_generator_fix.py` with at minimum: (a)
   `test_determinism` — same `params` and `morph_seed` produce structurally identical outputs
   across two calls; (b) `test_no_nan_on_bedb_base_point` — the patched cell's soma Vm under
   `apply_parameter_vector + insert_baseline_channels + 50 ms unstimulated` has no NaN samples; (c)
   `test_soma_area_within_tolerance` — `procedural_bedb_fixed.soma.area_um2` is within ±5% of
   `BEDB_AREA_TARGET_UM2`.

   Inputs: `data/root_cause_analysis.json` (drives the fix shape decision). Outputs:
   `code/morphology_generator_fix.py`, `code/test_morphology_generator_fix.py`. Expected observable:
   `uv run pytest tasks/t0092_.../code/test_morphology_generator_fix.py -v` shows 3+ passing tests.
   Satisfies REQ-6 and REQ-7.

8. **[CRITICAL] Phase F — Post-fix validation re-run.** Create
   `tasks/t0092_.../code/post_fix_verification.py` with a `main()` that runs the 8-direction bar
   protocol on the patched cells:

   * **Required block (REQ-8)**:
     `procedural_bedb_fixed = generate_fixed_morphology(params= MorphologyParams.from_bedb_base_point(), morph_seed=MORPH_SEED)`.
     For each of 8 directions `[0, 45, 90, 135, 180, 225, 270, 315]` deg, run
     `run_one_trial(cell=..., bundle=..., direction_deg=d, seed=SEED_BASE)` and record spike count,
     peak Vm, AP rate. Compute `dsi = (R_pref - R_null) / (R_pref + R_null)` where `R_pref` is the
     rate at PD=0° and `R_null` is the rate at ND=180°.

   * **Stretch block (REQ-9)**: For each cell ID in `STABLE_T0090_CELLS`, load the corresponding
     `MorphologyParams` from `tasks/t0090_.../results/data/` (or reconstruct from the t0090
     diversity-grid params), call `generate_fixed_morphology` with the matching seed, and run the
     same 8-direction protocol. Record per-cell spike counts and DSI.

   Plot the 6 polar tuning curves (1 BedB-equivalent + 5 STABLE) to
   `results/images/post_fix_polar_tuning.png` using `matplotlib.projections.polar`. Write
   `data/post_fix_verification.json` with one block per cell. Also update
   `tasks/t0092_.../results/metrics.json` using the explicit multi-variant format with two variants
   `pre_fix_procedural_bedb` (DSI: 0.0 or null if no spikes) and `post_fix_procedural_bedb` (DSI:
   actual computed value). Use the registered metric key `direction_selectivity_index` from
   `meta/metrics/`.

   **Validation gate**: this step processes ~6 cells × 8 directions = 48 trials. If after the first
   3 cells the patched BedB-equivalent shows DSI ≤ 0.0 or PD-rate = 0 Hz, halt and inspect: print
   the patched soma's `area_um2` (must be within tolerance of 220 µm²); print 5 individual Vm
   traces from PD trials; verify `apply_parameter_vector` was called with the t0083 vector. Do not
   proceed to the STABLE-from-t0090 cells until BedB-equivalent passes its criterion.

   Run with
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0092_diagnose_morphology_generator_silence -- python -m tasks.t0092_diagnose_morphology_generator_silence.code.post_fix_verification`.
   Outputs: `data/post_fix_verification.json`, `results/images/post_fix_polar_tuning.png`,
   `results/metrics.json`. Expected observable: BedB-equivalent block shows `pd_rate_hz > 0.0` AND
   `dsi > 0.1`. Stretch: at least 3 of 5 STABLE cells have `pd_rate_hz > 0.0`. Satisfies REQ-8,
   REQ-9, REQ-12.

### Milestone 4: Asset creation (REQ-10, REQ-11)

9. **Create the library asset.** Create
   `tasks/t0092_.../assets/library/procedural_dsgc_morphology_generator_fix/details.json` per
   `meta/asset_types/library/specification.md` v2 with:
   `library_id = "procedural_dsgc_morphology_generator_fix"`,
   `name = "Procedural DSGC Morphology Generator Fix"`, `version = "0.1.0"`,
   `short_description = "Drop-in replacement for t0090's generate_morphology that patches the structural bug causing zero spikes under the t0083 best-cell channel set"`,
   `description_path = "description.md"`,
   `module_paths = ["code/morphology_generator_fix.py", "code/baseline_channels.py", "code/paths.py", "code/constants.py"]`,
   `entry_points` with `generate_fixed_morphology` (function), `dependencies = ["neuron", "numpy"]`,
   `test_paths = ["code/test_morphology_generator_fix.py"]`,
   `categories = ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell"]`,
   `created_by_task = "t0092_diagnose_morphology_generator_silence"`, `date_created = "2026-05-07"`.
   Create `tasks/t0092_.../assets/library/procedural_dsgc_morphology_generator_fix/description.md`
   with YAML frontmatter and the 7 mandatory sections (`## Metadata`, `## Overview`,
   `## API Reference`, `## Usage Examples`, `## Dependencies`, `## Testing`, `## Main Ideas`,
   `## Summary`). The Overview must explain the bug, the fix shape, and the drop-in compatibility
   guarantee. The API Reference must document `generate_fixed_morphology`'s full signature and
   contract. Usage Examples must include t0091's expected import-swap line:
   `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
   Outputs: the library asset folder with both files. Expected observable:
   `uv run python -m arf.scripts.verificators.verify_assets t0092_diagnose_morphology_generator_silence`
   reports zero LA-E*** errors. Satisfies REQ-10.

10. **Create the answer asset.** Create
    `tasks/t0092_.../assets/answer/t0090-procedural-cell-silence-root-cause/details.json` per
    `meta/asset_types/answer/specification.md` v2 with:
    `answer_id = "t0090-procedural-cell-silence- root-cause"`,
    `question = "Why do t0090's procedural cells produce zero spikes under the t0083 best-cell channel set, and what is the fix?"`,
    `short_title = "t0090 procedural cell silence root cause"`,
    `short_answer_path = "short_answer.md"`, `full_answer_path = "full_answer.md"`,
    `categories = ["compartmental-modeling", "direction-selectivity"]`,
    `answer_methods = ["code-experiment"]`, `source_paper_ids = []`, `source_urls = []`,
    `source_task_ids = ["t0024_port_de_rosenroll_2026_dsgc", "t0080_bedb_mobo_v3_dendritic_spike_nsga2", "t0083_bedb_v3_extend_nsga2_gen8plus", "t0090_morphology_generator_diversity_test"]`,
    `confidence = "high"` (with the validation re-run as the supporting code experiment).
    `short_answer.md`: 2-5 sentences naming the primary root cause, citing no inline references.
    `full_answer.md`: the 9 mandatory sections (`## Question`, `## Short Answer`,
    `## Research Process`, `## Evidence from Papers`, `## Evidence from Internet Sources`,
    `## Evidence from Code or Experiments`, `## Synthesis`, `## Limitations`, `## Sources`). The
    "Evidence from Code or Experiments" section walks through Phases A through F with the supporting
    numbers from the JSON dumps. The "Synthesis" recommends the generator behaviour for t0091 (use
    `generate_fixed_morphology` instead of `generate_morphology`; verify any further deviation from
    BedB base point still preserves soma area within the 220 µm² target). Outputs: the answer
    asset folder with all three files. Expected observable:
    `uv run python -m arf.scripts.verificators.verify_assets t0092_diagnose_morphology_generator_silence`
    reports zero AA-E*** errors. Satisfies REQ-11.

### Milestone 5: Quality checks (REQ-13)

11. **Run quality gates.** Run `uv run ruff check --fix tasks/t0092_.../code/`,
    `uv run ruff format tasks/t0092_.../code/`, `uv run mypy tasks/t0092_.../code/`,
    `uv run pytest tasks/t0092_.../code/ -v`. Run
    `uv run flowmark --inplace --nobackup tasks/t0092_diagnose_morphology_generator_silence/plan/plan.md`
    and on every other task-folder markdown file edited during this task. Inputs: all task code +
    assets. Outputs: clean code, passing tests, formatted markdown. Expected observable: ruff
    reports 0 issues, mypy reports 0 issues, pytest reports 0 failures, all *.md files
    Flowmark-clean. Satisfies REQ-13.

## Remote Machines

None required. All NEURON simulations run inline on the local 64-core EPYC workstation. Each
8-direction protocol completes in seconds to minutes; the structural and synapse dumps are
sub-second. No GPU is needed. The framework rule is honoured: there is no setup-machines step in the
workflow.

## Assets Needed

* **Library asset** `procedural_dsgc_morphology_generator` (from t0090, source:
  `tasks/t0090_morphology_generator_diversity_test/`): provides `generate_morphology`,
  `MorphologyParams`, `MorphologyResult`, `BEDB_BASE_POINT`, and
  `load_t0083_best_cell_param_vector`.
* **Library asset** `de_rosenroll_2026_dsgc_ais_dendritic_spike` (from t0080, source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/`): provides `apply_parameter_vector`,
  `setup_synapses_parametric`, `_section_midpoint_xy`, `_bar_arrival_times`, `_count_spikes`,
  `run_one_trial`, `build_dsgc_cell_with_ais`, `DSGCCellWithAIS`, `ParameterVector`, `ParamIndex`,
  `Tier`, `N_PARAMS`, `TSTOP_MS`, `SEED_BASE`, `PD_DIRECTION_DEG`, `AP_THRESHOLD_MV`.
* **Library asset** `de_rosenroll_2026_dsgc` (from t0024, source:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/`): provides `build_dsgc_cell`, `BAR_X_START_UM`,
  `BAR_VELOCITY_UM_PER_MS`.
* **Data file** `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json` (loaded
  via `load_t0083_best_cell_param_vector`): provides the 54-d best-cell parameter vector.
* **Code helper (copied)** `tasks/t0090_.../code/verification.py:_insert_baseline_channels`: copied
  into `tasks/t0092_.../code/baseline_channels.py` because it is task-internal in t0090, not a
  library entry point.
* **Reference data** `tasks/t0024_.../assets/library/de_rosenroll_2026_dsgc/sources/RGCmodelGD.hoc`:
  source of the 7-pt3d soma frustum stack used to compute the 220 µm² target surface area.

## Expected Assets

* **Library asset (1)** —
  `tasks/t0092_.../assets/library/procedural_dsgc_morphology_generator_fix/`. The fix module plus
  its task-internal helpers (`baseline_channels.py`, `paths.py`, `constants.py`). Categories:
  `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`. Public entry point:
  `generate_fixed_morphology` — drop-in replacement for t0090's `generate_morphology` with the
  identified bug fixed.

* **Answer asset (1)** —
  `tasks/t0092_.../assets/answer/t0090-procedural-cell-silence-root-cause/`. Question: "Why do
  t0090's procedural cells produce zero spikes under the t0083 best-cell channel set, and what is
  the fix?". Categories: `compartmental-modeling`, `direction-selectivity`. Confidence: `high`,
  supported by the structural dump, synapse comparison, Vm trace comparison, ranked candidate
  analysis, and post-fix validation re-run.

The expected counts match `task.json` `expected_assets`: `{"answer": 1, "library": 1}`.

## Time Estimation

* Phase A (structural dump, Step 3): ~30 min — single-process build of two cells, per-section data
  dump, JSON write.
* Phase B (synapse comparison, Step 4): ~30 min — synapse placement on both cells, per-synapse XY
  + arrival-time computation, JSON write.
* Phase C (Vm trace comparison, Step 5): ~15 min — two single-direction trials, .npy + .png write.
* Phase D (root cause analysis, Step 6): ~1-2 hours — load all dumps, code the four candidate
  tests, write the verdict JSON, manual inspection of borderline numbers.
* Phase E (fix implementation, Step 7): ~2-4 hours — depends on whether the verdict points at a
  thin soma-pt3d patch (closer to 2 hours) or a deeper re-emit-pt3d-per-section change (closer to 4
  hours). Includes unit-test authoring.
* Phase F (validation re-run, Step 8): ~30 min — 6 cells × 8 directions = 48 trials, plus polar
  plot rendering and metrics.json writing.
* Asset creation (Steps 9-10): ~30 min — library `details.json` + description, answer
  `details.json`
  + short + full answer.
* Quality gates (Step 11): ~15 min — ruff, mypy, pytest, flowmark.
* **Total wall-clock**: ~1 day. Comfortably within local capacity; no remote scheduling.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Hand-coded Bed B cell ALSO fails to spike under the t0083 best-cell vector — bug is in `apply_parameter_vector` or `load_t0083_best_cell_param_vector`, not in t0090 | Low | Blocking: invalidates Phase E and F, redirects fix to a different task | Step 5 includes an explicit validation gate. If `handcoded_bedb` does not spike, halt, write the answer asset documenting this as the root cause, and create an intervention file recommending a follow-up task targeting `tasks/t0080_.../code/apply_params.py`. The fix library is then deferred. |
| Structural dump matches between cells but soma-Vm traces still diverge — points at a NEURON-state bug (e.g., `h.allsec()` enumeration order, GC `id()` reuse despite `_LIVE_CELLS` defense) | Low | Slows diagnosis: Phase D has no clear primary cause | Step 3's structural dump includes `for sec in h.allsec(): ...` as a sanity output. Step 6's analysis adds a fifth fallback candidate "NEURON-state asymmetry" if the primary four are all REFUTED. Recovery: run both cells in *separate* processes (one Python subprocess per cell) and compare results. |
| Soma-area patch fixes BedB-equivalent but breaks for non-trivial asymmetry knobs (the 5 STABLE-from-t0090 cells) | Medium | Stretch goal (REQ-9) misses; required goal (REQ-8) still passes | The fix's unit test `test_soma_area_within_tolerance` runs on the BedB base point only; non-BedB cells are validated in Step 8's stretch block. If a stretch cell still fails, document the residual issue in the answer asset's Limitations section as a t0091 follow-up; the BedB-equivalent pass is sufficient to unblock t0091's warm-start anchor. |
| Multiple simultaneous root causes (e.g., soma area + synapse-XY together) — fixing one alone does not restore spiking | Medium | Phase E iterates: first fix does not pass Step 8's validation gate | Step 8's validation gate explicitly halts after 3 cells if BedB-equivalent does not pass. Recovery: return to Step 7 and stack a second patch (e.g., soma area patch + intended-XY synapse placement). The wrapper architecture supports compositional patches without rewriting `generate_morphology`. |
| Fix changes the generator's output dataclass shape enough that t0091 needs a new wrapper | Low | Slight slowdown for t0091 | The fix's contract is documented in the library description: same `MorphologyResult` shape, same `MorphologyParams` signature, same return-by-value semantics. Steps 9-10 emphasise the drop-in guarantee. If a contract-breaking change is unavoidable, document it as a Major Limitation in the answer asset. |
| `uv run pytest` fails for a reason unrelated to the fix (e.g., NEURON DLL version mismatch, mypy strictness on t0090 imports) | Low | Step 11 fails repeatedly | Step 11 runs the gates last so other progress is preserved. Recovery: scope fixes to `tasks/t0092_.../code/`-only — never modify t0090 or t0080 in response. If a gate failure is in imported library code, log as an intervention. |

## Verification Criteria

The implementation is complete when ALL the following criteria pass:

* **File existence** — Run `ls tasks/t0092_diagnose_morphology_generator_silence/data/`. Expected
  to list at minimum: `structural_comparison.json`, `synapse_comparison.json`,
  `vm_trace_procedural.npy`, `vm_trace_handcoded.npy`, `root_cause_analysis.json`,
  `post_fix_verification.json`. Run `ls tasks/t0092_.../results/images/`. Expected:
  `vm_trace_comparison.png`, `post_fix_polar_tuning.png`.

* **Pass criterion** — Run
  `uv run python -c "import json; d = json.load(open('tasks/t0092_diagnose_morphology_generator_silence/data/post_fix_verification.json')); bedb = d['procedural_bedb_fixed']; assert bedb['pd_rate_hz'] > 0.0; assert bedb['dsi'] > 0.1; print('PASS:', bedb['pd_rate_hz'], bedb['dsi'])"`.
  Expected output: `PASS: <pd_rate> <dsi>` with both numbers strictly positive and DSI > 0.1. This
  satisfies REQ-8.

* **Unit tests** — Run
  `uv run pytest tasks/t0092_diagnose_morphology_generator_silence/code/test_morphology_generator_fix.py -v`.
  Expected output: at least 3 tests collected, 0 failures, 0 errors. This satisfies REQ-7 and
  REQ-13.

* **Style and types** — Run
  `uv run ruff check tasks/t0092_diagnose_morphology_generator_silence/code/` and
  `uv run mypy tasks/t0092_diagnose_morphology_generator_silence/code/`. Expected output: 0 issues
  from ruff, 0 errors from mypy. This satisfies REQ-13.

* **Library asset verifier** — Run
  `uv run python -m arf.scripts.verificators.verify_assets t0092_diagnose_morphology_generator_silence`.
  Expected output: 0 errors (LA-E***), warnings acceptable.

* **Answer asset verifier** — Same command as above also covers the answer asset (AA-E***).
  Expected: 0 errors.

* **Plan verifier** — Run
  `uv run python -m arf.scripts.verificators.verify_plan t0092_diagnose_morphology_generator_silence`.
  Expected output: 0 errors. (This criterion is checked at planning time; the implementation step
  inherits the validated plan.)

* **Metrics file** — Run
  `uv run python -c "import json; m = json.load(open('tasks/t0092_diagnose_ morphology_generator_silence/results/metrics.json')); print(list(m.keys()))"`.
  Expected output includes a top-level structure with the registered key
  `direction_selectivity_index` for at least the `post_fix_procedural_bedb` variant. This satisfies
  REQ-12.

* **Requirement coverage** — Run
  `uv run python -c "import re, pathlib; text = pathlib.Path('tasks/t0092_diagnose_morphology_generator_silence/plan/plan.md').read_text(); reqs = sorted(set(re.findall(r'REQ-\d+', text))); print(len(reqs), reqs)"`.
  Expected output: count is 13 and IDs are `REQ-1` through `REQ-13` exactly once each. Confirms the
  plan-level requirement traceability. The implementation step's completion notes (in
  `logs/steps/<step>/step_log.md`) must tick off each `REQ-*` ID with a one-line evidence pointer.
