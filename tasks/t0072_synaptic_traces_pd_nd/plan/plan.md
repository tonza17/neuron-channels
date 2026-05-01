---
spec_version: "2"
task_id: "t0072_synaptic_traces_pd_nd"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Synaptic Conductance and Current Traces (PD vs ND) on Both Model Beds

## Objective

Run one preferred-direction (PD) trial and one null-direction (ND) trial on each of two existing
DSGC compartmental models (Bed A: Poleg-Polsky 2016 deposited variant under the t0020 gabaMOD swap;
Bed B: de Rosenroll 2026 port under the t0066 bar-angle swap). Record the synaptic conductance state
variable `g(t)` and the local membrane voltage `v_local(t)` from every synapse instance of every
active synapse type on each bed. Compute population mean ± standard deviation across synapses for
each `(bed, direction, synapse_type)` combination, and the post-hoc current
`I(t) = g(t) · (v_local(t) − E_rev)`. Produce two multi-panel PNG figures showing g(t) and I(t)
for PD and ND overlaid per synapse type, embed them in a Typst-typeset PDF writeup. Done means: 12
raw `.npz` trace files exist in `data/`; both `bed_a_synaptic_traces.png` (4 rows × 2 cols) and
`bed_b_synaptic_traces.png` (2 rows × 2 cols) exist in `results/images/`; the rendered
`results_detailed.pdf` is at least 50 KB and embeds both figures with descriptive captions.

## Task Requirement Checklist

The operative task text from `task.json` (`short_description`) and `task_description.md`:

> Run one PD trial + one ND trial on each model bed (Bed A: t0008/t0020 deposited Poleg-Polsky; Bed
> B: t0024 de Rosenroll), record g(t) and I(t) traces from every synapse instance, plot the
> population mean ± SD per synapse type with PD and ND overlaid. Output: 2 multi-panel figures + a
> Typst-typeset PDF.

> Bed A — t0008 deposited Poleg-Polsky, with the t0020 gabaMOD-swap protocol applied (PD:
> `gabaMOD = 0.33`; ND: `gabaMOD = 0.99`). 282 ON dendrites, each carrying one BIPsyn (AMPA + NMDA),
> one SACinhibsyn (GABA), and one SACexcsyn (ACh). 4 synapse types to plot.

> Bed B — t0024 de Rosenroll port. Uses moving-bar angle for direction encoding, with per-event
> Bernoulli release sigmoid (PD: bar at preferred angle; ND: bar at null angle, i.e. rotated 180°).
> Active synapses on this bed are Exp2Syn ACh and Exp2Syn GABA. 2 synapse types to plot.

Concrete requirements extracted from the task text:

* **REQ-1** — Bed A: record `gAMPA(t)` and `gNMDA(t)` from every BIPsyn instance (282 instances),
  in PD and ND. Satisfied by Step 4. Evidence: `data/bed_a_pd_ampa.npz`, `data/bed_a_nd_ampa.npz`,
  `data/bed_a_pd_nmda.npz`, `data/bed_a_nd_nmda.npz` exist with shape `(282, n_samples)` for the
  `g_traces` array.

* **REQ-2** — Bed A: record `g(t)` from every SACinhibsyn (GABA, 282 instances) and SACexcsyn
  (ACh, 282 instances), PD and ND. Satisfied by Step 4. Evidence: `data/bed_a_pd_gaba.npz`,
  `data/bed_a_nd_gaba.npz`, `data/bed_a_pd_ach.npz`, `data/bed_a_nd_ach.npz` exist with shape
  `(282, n_samples)`.

* **REQ-3** — Bed B: record `g(t)` from every Exp2Syn ACh and Exp2Syn GABA instance (one of each
  per terminal dendrite, ~177 terminals), PD and ND. Satisfied by Step 5. Evidence:
  `data/bed_b_pd_ach.npz`, `data/bed_b_nd_ach.npz`, `data/bed_b_pd_gaba.npz`,
  `data/bed_b_nd_gaba.npz` exist with shape `(n_terminals, n_samples)`.

* **REQ-4** — Compute `I(t) = g(t) · (v_local(t) − E_rev)` post-hoc for every synapse, in pA,
  on both beds. Satisfied by Step 6 (aggregation). Evidence: aggregated `I_mean` and `I_std` arrays
  in `data/aggregated.npz` for every `(bed, direction, type)`.

* **REQ-5** — Aggregate to population mean ± SD per synapse type per direction. Satisfied by Step
  6\. Evidence: `data/aggregated.npz` contains `g_mean`, `g_std`, `I_mean`, `I_std`, `t_ms` arrays
  per `(bed, direction, type)` keyed prefix.

* **REQ-6** — Bed A figure: 4 rows (AMPA, NMDA, GABA, ACh) × 2 cols (g, I), with PD and ND
  overlaid in each panel as solid lines + ±1 SD shaded bands. Satisfied by Step 7. Evidence:
  `results/images/bed_a_synaptic_traces.png` exists, file size ≥ 50 KB.

* **REQ-7** — Bed B figure: 2 rows (ACh, GABA) × 2 cols (g, I), PD and ND overlaid in each panel
  as solid lines + ±1 SD shaded bands. Satisfied by Step 7. Evidence:
  `results/images/bed_b_synaptic_traces.png` exists, file size ≥ 50 KB.

* **REQ-8** — Both figures embedded in `results/results_detailed.md` with descriptive captions.
  Satisfied during the orchestrator's results-writing step (out of scope for this plan; the plan
  ends at chart generation per the planning skill specification).

* **REQ-9** — Typst-typeset PDF produced (consistent with t0071 pipeline). Satisfied by Step 8.
  Evidence: `results/results_detailed.pdf` exists with size ≥ 50 KB; the typst source
  `results/results_detailed.typ` includes both PNG figures via `#image(...)`.

* **REQ-10** — Discussion in the writeup highlighting which traces differ between PD and ND for
  each bed. Satisfied during the orchestrator's results-writing step (out of scope for this plan).

Note: REQ-8 and REQ-10 require prose in `results_detailed.md`, which the planning skill
specification places under the orchestrator's results-writing step (forbidden inside this plan's
Step by Step). They are listed here for traceability so the orchestrator can confirm coverage.

## Approach

The technical approach is recording-and-plotting: every cell-build, parameter-application, and
trial-runner primitive needed for both beds already exists in completed dependency tasks. The plan
imports those primitives, copies a small set of helpers that are not library-exposed, and adds one
extension over prior recording code (per-synapse local membrane voltage `v_local`).

**Bed A construction and trial setup**: import `build_dsgc()` and `apply_params()` from
`tasks.t0008_port_modeldb_189347.code.build_cell` (registered library `modeldb_189347_dsgc`). The
canonical PD/ND swap follows the order proven by
`tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py` (`run_one_trial_gabamod` body):
`apply_params(h, seed=seed) → h.gabaMOD = GABA_MOD_PD or GABA_MOD_ND → h("update()") → h("placeBIP()") → attach recorders → h.finitialize(V_INIT_MV) → h.continuerun(TSTOP_MS)`.
Constants: `GABA_MOD_PD = 0.33`, `GABA_MOD_ND = 0.99`, `TSTOP_MS = 1000.0`, `DT_MS = 0.1`,
`V_INIT_MV = -65.0`. The 282 ON dendrites each carry one `h.RGC.BIPsyn[i]` (AMPA + NMDA), one
`h.RGC.SACinhibsyn[i]` (GABA), and one `h.RGC.SACexcsyn[i]` (ACh).

**Bed A per-synapse recording**: copy the recorder pattern from
`tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py` (lines 100-150,
`attach_conductance_recorders` plus the `ConductanceRecorders` dataclass). For each `i` in
`range(h.RGC.numsyn)`, attach:

* `h.Vector().record(bip._ref_gAMPA, RECORD_DT_MS)` — AMPA conductance
* `h.Vector().record(bip._ref_gNMDA, RECORD_DT_MS)` — NMDA conductance
* `h.Vector().record(sacinhib._ref_g, RECORD_DT_MS)` — GABA conductance
* `h.Vector().record(sacexc._ref_g, RECORD_DT_MS)` — ACh conductance
* `h.Vector().record(bip.get_segment()._ref_v, RECORD_DT_MS)` — local membrane voltage at the
  midpoint of the ON dendrite section (shared by all 4 synapse types on that section)

The single extension over t0048's pattern is recording per-synapse `v_local` via
`pp.get_segment()._ref_v`. This is required because the same conductance produces different currents
at different dendritic compartments — and the task computes `I = g · (v_local − E_rev)`
post-hoc, so we need the voltage at the actual recording site, not soma voltage.
`RECORD_DT_MS = 1.0` (down from t0048's 0.25) bounds memory at ~22 MB raw across both Bed A
directions and satisfies the task description's Risk #1 mitigation preemptively.

**Bed B construction and synapse setup**: import `build_dsgc_cell()` from
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell` (registered library
`de_rosenroll_2026_dsgc`). The Bed B synapses (Exp2Syn ACh + Exp2Syn GABA, one of each per terminal
dendrite) are created by `_setup_synapses(*, cell, gaba_weight_scale)` in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py` (lines 189-226). Copy this helper
plus the `SynapseBundle` dataclass into the task code folder (private API, not library-exposed).
PD/ND for Bed B is encoded by bar angle: `DIRECTION_PD_DEG = 0.0`, `DIRECTION_ND_DEG = 180.0`, with
the angle entering through `_bar_arrival_times` and `_gaba_prob_for_direction` in the same file.
Copy the trial-runner body (`_run_one_trial`) from
`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py` (lines 205-298), stripping the
EPSP_PASSIVE / IPSP_PASSIVE mode logic — this task only needs the FULL mode. Use
`RHO_CORRELATED = 0.6` for the AR(2) noise (matches t0066 correlated condition).

**Bed B per-synapse recording**: same NEURON `Vector.record` idiom. For each `i` in
`range(len(bundle.syns_ach))`:

* `h.Vector().record(syn_ach._ref_g, RECORD_DT_MS)` — ACh conductance (microsiemens)
* `h.Vector().record(syn_gaba._ref_g, RECORD_DT_MS)` — GABA conductance (microsiemens)
* `h.Vector().record(syn_ach.get_segment()._ref_v, RECORD_DT_MS)` — local v at terminal section

Bed B's `Exp2Syn.g` is in microsiemens (µS) per NEURON convention, while Bed A's MOD-defined `g` is
in nanosiemens (nS). The aggregation step converts Bed B's `g` to nS (multiply by 1000) so the
post-hoc `I_pA = g_nS · (v_mV − E_mV)` formula applies uniformly across both beds and the plotted
units are consistent.

**Reversal potentials for current computation** (sourced from MOD files and dependency-task
constants):

* Bed A AMPA, Bed A NMDA, Bed A ACh: `E_rev = 0 mV`
* Bed A GABA: `E_rev = -60 mV` (from `e_SACinhib` GLOBAL set in t0008 `apply_params`)
* Bed B ACh: `E_rev = 0 mV` (`ACH_EREV_MV` in t0024 constants)
* Bed B GABA: `E_rev = -60 mV` (`GABA_EREV_MV` in t0024 constants)

**Aggregation**: load all 12 `.npz` files, stack per-synapse traces into a 2D array
`(n_synapses, n_samples)`, compute `g_mean = traces.mean(axis=0)`,
`g_std = traces.std(axis=0, ddof=1)`, then `I_per_synapse = g · (v_local − E_rev)` per synapse
and aggregate the same way. Save to a single `data/aggregated.npz` keyed by
`<bed>_<dir>_<type>_<g|I>_<mean|std>` plus a shared `t_ms`.

**Plotting**: matplotlib subplots. Bed A: `fig, axes = plt.subplots(4, 2, figsize=(12, 16))`. Rows:
AMPA, NMDA, GABA, ACh; cols: g(t), I(t). Each panel plots PD (blue, solid) and ND (red, solid) with
±1 SD shaded bands (`fill_between` with alpha 0.25). Axis labels: x = "Time (ms)"; y = "g (nS)" or
"I (pA)". Title each panel with the synapse type and column label. Legend in the top-left panel
only. Bed B: `fig, axes = plt.subplots(2, 2, figsize=(12, 8))`. Rows: ACh, GABA; cols: g, I. Same
overlay format. Save both PNGs to `results/images/` at 150 DPI.

**PDF rendering**: copy `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` verbatim (59 lines),
changing only the import path for `TYPST_SOURCE_PATH` and `PDF_OUTPUT_PATH` to point at this task's
`code/paths.py`. Write a short Typst source `results/results_detailed.typ` that includes both PNGs
via `#image("images/bed_a_synaptic_traces.png", width: 100%)` and the same for Bed B. The
orchestrator's results-writing step expands this into the full prose writeup.

**Alternatives considered**:

* *Record only somatic v as a v_local proxy* (matches t0048's exact pattern, no extension needed).
  Rejected because the task requires `I(t) = g · (v_local − E_rev)` per-synapse, and the same
  conductance produces wildly different currents at different dendritic compartments. Using soma
  voltage would systematically misestimate the local current in mid-dendritic regions.

* *Use Bed A MOD `local_v` RANGE variables* (`bip._ref_local_v`, `sacexc._ref_local_v`,
  `sacinhib._ref_local_v`) instead of `pp.get_segment()._ref_v`. Rejected because Bed B's Exp2Syn
  has no `local_v` exposure — using `pp.get_segment()._ref_v` uniformly across both beds is
  cleaner.

* *Record at the finer `DT_RECORD_MS = 0.25` used by t0048/t0047*. Rejected because synaptic
  rise/decay constants are all on the millisecond scale (AMPA τ = 2 ms, GABA decay 12-30 ms), so 1
  ms sampling captures the shape adequately and quarters the disk usage and per-trace memory. Bed
  B's ACh has a 0.1 ms rise but the peak and decay (the visualization-relevant features) are
  well-captured at 1 ms.

* *Recompute spikes / DSI / tuning curves*. Rejected because the task is explicitly trace
  visualization, not selectivity quantification — that was already done in t0020, t0024, t0048,
  t0065, t0066. No registered metric (DSI, HWHM, RMSE, reliability) applies.

**Recommended task type(s)**: this task is correctly tagged as `data-analysis` in `task.json`. The
data-analysis Planning Guidelines drove these design choices: defining the questions upfront (record
g and I per type, compare PD vs ND), listing all chart types upfront (4×2 Bed A figure plus 2×2
Bed B figure), and saving intermediate data (the 12 raw `.npz` trace files plus `aggregated.npz`) so
the analysis is reproducible from the simulator outputs.

## Cost Estimation

* External API calls: **$0** — no LLM, no third-party service. All computation is local NEURON
  simulation in Python.
* Remote compute: **$0** — runs on the local Windows workstation. Each bed simulation is 1-3
  seconds for the underlying solve; per-synapse recorder overhead may push wall-clock to 10-30
  seconds per trial. Four trials total (2 beds × 2 directions) — under 5 minutes wall-clock.
* Disk: ~50 MB raw `.npz` plus ~1 MB PDF — negligible.
* Project budget per task: $1.00 (`project/budget.json`). This task uses **$0**, well under budget.

## Step by Step

The Step by Step covers implementation work only. It ends at chart generation and PDF compilation
of the typst source. All orchestrator-managed steps (results writing, costs bookkeeping,
suggestions, literature comparison) are handled by `execute-task` and are explicitly excluded
here per the planning skill specification.

1. **Create `code/paths.py`.** Define output path constants:

   * `DATA_DIR: Path = Path("tasks/t0072_synaptic_traces_pd_nd/data")`
   * `RESULTS_DIR: Path = Path("tasks/t0072_synaptic_traces_pd_nd/results")`
   * `IMAGES_DIR: Path = RESULTS_DIR / "images"`
   * Per-file: `BED_A_PD_AMPA_NPZ`, `BED_A_ND_AMPA_NPZ`, ... (12 files total) — pattern
     `DATA_DIR / f"bed_{a|b}_{pd|nd}_{type}.npz"`
   * `AGGREGATED_NPZ: Path = DATA_DIR / "aggregated.npz"`
   * `BED_A_FIG_PNG: Path = IMAGES_DIR / "bed_a_synaptic_traces.png"`
   * `BED_B_FIG_PNG: Path = IMAGES_DIR / "bed_b_synaptic_traces.png"`
   * `TYPST_SOURCE_PATH: Path = RESULTS_DIR / "results_detailed.typ"`
   * `PDF_OUTPUT_PATH: Path = RESULTS_DIR / "results_detailed.pdf"`

   Expected output: file exists,
   `uv run python -c "from tasks.t0072_synaptic_traces_pd_nd.code import paths; print(paths.DATA_DIR)"`
   runs without error. Satisfies infrastructure for all REQs.

2. **Create `code/constants.py`.** Define recording, simulation, and per-bed PD/ND constants. All
   values are sourced from dependency-task constants (cited in research_code.md):

   * `RECORD_DT_MS: float = 1.0` (recording dt — see research finding "Recording dt: 1 ms gives
     ~1000 samples per trial, ~5 MB total")
   * `TSTOP_MS: float = 1000.0` — same for both beds (t0008 `code/constants.py` L18; t0024
     `code/constants.py` L22)
   * `DT_MS: float = 0.1` — simulator step (both beds)
   * `V_INIT_MV: float = -65.0`
   * `STEPS_PER_MS: int = 10` (Bed B, t0024 `code/constants.py` L23)
   * `CELSIUS_DEG_C: float = 35.0`
   * Bed A PD/ND: `GABA_MOD_PD: float = 0.33`, `GABA_MOD_ND: float = 0.99` (t0020
     `code/constants.py` L37-38)
   * Bed B PD/ND: `DIRECTION_PD_DEG: float = 0.0`, `DIRECTION_ND_DEG: float = 180.0` (t0066
     `code/constants.py` L19-20)
   * Bed B noise: `RHO_CORRELATED: float = 0.6` (matches t0066 correlated condition)
   * Bed B weight: `GABA_WEIGHT_SCALE: float = 1.0`
   * Reversal potentials in mV: `E_AMPA_MV = 0.0`, `E_NMDA_MV = 0.0`, `E_GABA_BED_A_MV = -60.0`,
     `E_ACH_BED_A_MV = 0.0`, `E_ACH_BED_B_MV = 0.0`, `E_GABA_BED_B_MV = -60.0`
   * Recorded quantity literal constants:
     `RECORDED_TYPES_BED_A: list[str] = ["ampa", "nmda", "gaba", "ach"]`,
     `RECORDED_TYPES_BED_B: list[str] = ["ach", "gaba"]`
   * Seed: `SEED: int = 0` (single seeded trial per (bed, direction))

   Expected output: file exists, all constants importable. Satisfies infrastructure for all REQs.

3. **(Skipped — merged into Steps 4 and 5.)** Originally a separate `record_synapses.py` helper
   was considered, but a per-bed runner is clearer. Each runner inlines the recorder-attachment loop
   adapted from `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py` lines 100-150.

4. **Create `code/run_bed_a.py`.** Implements the Bed A PD + ND trials with per-synapse recording.

   Imports:

   * `from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params` (Bed A
     library, registered)
   * `from tasks.t0072_synaptic_traces_pd_nd.code.constants import (RECORD_DT_MS, TSTOP_MS, V_INIT_MV, GABA_MOD_PD, GABA_MOD_ND, SEED, ...)`
   * `from tasks.t0072_synaptic_traces_pd_nd.code.paths import (BED_A_PD_AMPA_NPZ, ...)`
   * `import numpy as np`

   Logic:

   1. Call `build_dsgc()` once per process — returns `h` with `h.RGC` populated.

   2. For each direction in `[("pd", GABA_MOD_PD), ("nd", GABA_MOD_ND)]`:

      a. Call `apply_params(h, seed=SEED)` — writes canonical params (sets `h.gabaMOD = 0.33`). b.
      Override `h.gabaMOD = gabamod_value`. c. Run `h("update()")` then `h("placeBIP()")` —
      re-runs the HOC stimulus generator so inhibitory point processes pick up the new modulation
      envelope. d. Attach recorders: for each `i` in `range(int(h.RGC.numsyn))` (= 282), create five
      `h.Vector()` instances and call `.record(bip._ref_gAMPA, RECORD_DT_MS)`,
      `.record(bip._ref_gNMDA, RECORD_DT_MS)`, `.record(sacinhib._ref_g, RECORD_DT_MS)`,
      `.record(sacexc._ref_g, RECORD_DT_MS)`, and `.record(bip.get_segment()._ref_v, RECORD_DT_MS)`.
      Also attach a single `t_rec = h.Vector(); t_rec.record(h._ref_t, RECORD_DT_MS)`. e.
      `h.finitialize(V_INIT_MV)`; `h.continuerun(TSTOP_MS)`. f. Convert each per-synapse vector to
      numpy: `np.array(list(v_rec), dtype=np.float64)`. Stack across synapses to shape
      `(282, n_samples)`. Defensive assert: all per-synapse vectors have the same length (catches
      misordered finitialize). g. Save four `.npz` files per direction (`bed_a_<dir>_ampa.npz`,
      `bed_a_<dir>_nmda.npz`, `bed_a_<dir>_gaba.npz`, `bed_a_<dir>_ach.npz`). Each contains keys
      `g_traces` (shape `(282, n_samples)`), `v_local_traces` (shape `(282, n_samples)`), and `t_ms`
      (shape `(n_samples,)`). h. Drop the recorder list to release memory before the next
      direction's recorders are attached.

   Expected output: `data/bed_a_pd_*.npz` and `data/bed_a_nd_*.npz` exist (8 files). Each loaded
   with `np.load` reveals `g_traces.shape == (282, 1001)`, `v_local_traces.shape == (282, 1001)`,
   `t_ms.shape == (1001,)` (assuming `RECORD_DT_MS = 1.0`, `TSTOP_MS = 1000.0`).

   Satisfies REQ-1 (AMPA, NMDA recordings) and REQ-2 (GABA, ACh recordings).

5. **Create `code/run_bed_b.py`.** Implements the Bed B PD + ND trials with per-synapse recording.

   Imports:

   * `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`
     (Bed B library, registered)
   * `from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24` for terminal
     parameters (`ACH_TAU1_MS`, `ACH_TAU2_MS`, `ACH_EREV_MV`, `ACH_WEIGHT_US`, `GABA_TAU1_MS`,
     `GABA_TAU2_MS`, `GABA_EREV_MV`, `GABA_WEIGHT_US`, `BAR_START_TIME_MS`, `BAR_X_START_UM`,
     `BAR_VELOCITY_UM_PER_MS`, etc.)
   * `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise import generate_ar2_batch`
     (registered library entry point)
   * Helpers `_setup_synapses`, `SynapseBundle`, `_bar_arrival_times`, `_rates_with_ar2_noise`,
     `_gaba_prob_for_direction`, `_rates_to_events` — copied verbatim into this task's `code/`
     from `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py` (private API; ~40 lines
     for `_setup_synapses` + `SynapseBundle`, ~150 lines for the rest)
   * Trial runner body — adapted from
     `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py` `_run_one_trial` (lines
     205-298), with EPSP_PASSIVE / IPSP_PASSIVE mode-switching logic stripped (FULL mode only)
   * `from tasks.t0072_synaptic_traces_pd_nd.code.constants import (RECORD_DT_MS, TSTOP_MS, V_INIT_MV, DIRECTION_PD_DEG, DIRECTION_ND_DEG, RHO_CORRELATED, GABA_WEIGHT_SCALE, SEED, ...)`

   Logic:

   1. Call `build_dsgc_cell()` once — returns `DSGCCell` with `cell.h`, `cell.terminal_dends`,
      `cell.terminal_locs_xy`, `cell.origin_xy`, `cell.soma`.

   2. Call `bundle = _setup_synapses(cell=cell, gaba_weight_scale=GABA_WEIGHT_SCALE)`. Records
      `n_terminals = len(bundle.syns_ach)` (also equals `len(bundle.syns_gaba)`).

   3. For each direction in `[("pd", DIRECTION_PD_DEG), ("nd", DIRECTION_ND_DEG)]`:

      a. Set `h.celsius`, `h.dt`, `h.steps_per_ms`, `h.v_init`, `h.tstop` from constants. b. Compute
      bar arrival times via `_bar_arrival_times(cell=cell, direction_deg=direction_deg, ...)`.
      Compute AR(2) noise rates via `_rates_with_ar2_noise(...)`. Compute GABA release probability
      per direction via `_gaba_prob_for_direction(direction_deg=direction_deg)`. c. Sample Poisson
      event times via `_rates_to_events(...)` and queue them into NetCons via a
      `FInitializeHandler`. d. Attach recorders: for each `i` in `range(n_terminals)`, create three
      `h.Vector()` instances with `.record(syn_ach._ref_g, RECORD_DT_MS)`,
      `.record(syn_gaba._ref_g, RECORD_DT_MS)`, and
      `.record(syn_ach.get_segment()._ref_v, RECORD_DT_MS)`. Attach one
      `t_rec = h.Vector(); t_rec.record(h._ref_t, RECORD_DT_MS)`. e. `h.finitialize(V_INIT_MV)`;
      `h.run()` (or `h.continuerun(TSTOP_MS)`). f. Stack per-synapse vectors to numpy, shape
      `(n_terminals, n_samples)`. Defensive assert on length consistency. g. Save two `.npz` per
      direction (`bed_b_<dir>_ach.npz`, `bed_b_<dir>_gaba.npz`). Each contains keys `g_traces`
      (units: µS), `v_local_traces` (units: mV), `t_ms`. h. Drop recorder list.

   Expected output: `data/bed_b_pd_*.npz` and `data/bed_b_nd_*.npz` exist (4 files). Each loaded
   reveals `g_traces.shape == (n_terminals, 1001)` (n_terminals ~177),
   `v_local_traces.shape == (n_terminals, 1001)`, `t_ms.shape == (1001,)`.

   Satisfies REQ-3.

6. **Create `code/aggregate.py`.** Loads all 12 raw `.npz` files, computes per-synapse current
   `I = g · (v_local − E_rev)`, and aggregates to mean ± SD across synapses per
   `(bed, direction, type)`.

   Imports:

   * `import numpy as np`
   * `from tasks.t0072_synaptic_traces_pd_nd.code.paths import (BED_A_*, BED_B_*, AGGREGATED_NPZ)`
   * `from tasks.t0072_synaptic_traces_pd_nd.code.constants import (E_AMPA_MV, E_NMDA_MV, E_GABA_BED_A_MV, E_ACH_BED_A_MV, E_ACH_BED_B_MV, E_GABA_BED_B_MV)`

   Logic:

   1. Define a dataclass `AggregatedTraces` with fields `bed`, `direction`, `synapse_type`, `t_ms`,
      `g_mean_nS`, `g_std_nS`, `I_mean_pA`, `I_std_pA` (all `np.ndarray`).

   2. For each `(bed, direction, syn_type)` combination (8 Bed A + 4 Bed B = 12 total):

      a. Load `data/<bed>_<dir>_<type>.npz`. b. Read `g_traces` (shape `(n_synapses, n_samples)`)
      and `v_local_traces` (same shape). c. For Bed B: convert g from µS to nS by multiplying by
      1000\. d. Look up `E_rev` for this `(bed, syn_type)` — Bed A AMPA/NMDA/ACh = 0 mV; Bed A
      GABA = -60 mV; Bed B ACh = 0 mV; Bed B GABA = -60 mV. e. Per-synapse current:
      `I = g_nS * (v_local_mV - E_mV)` (units: pA, since 1 nS · 1 mV = 1 pA). f. Compute means and
      SDs along axis 0: `g_mean_nS`, `g_std_nS`, `I_mean_pA`, `I_std_pA`. g. Append an
      `AggregatedTraces` instance to the list.

   3. Save all to `data/aggregated.npz` keyed `<bed>_<dir>_<type>_g_mean`, `_g_std`, `_I_mean`,
      `_I_std`, plus a single shared `t_ms` (assert all 12 t_ms arrays are identical by
      value-equality).

   Expected output: `data/aggregated.npz` exists; `np.load` reveals 49 keys (12 × 4 + 1 t_ms). Each
   `<...>_mean` and `<...>_std` is a 1D array of shape `(1001,)`.

   Satisfies REQ-4 (post-hoc current computation) and REQ-5 (aggregation to mean ± SD).

7. **Create `code/plot_traces.py`.** Generates the two PNG figures.

   Imports:

   * `import numpy as np`
   * `import matplotlib.pyplot as plt`
   * `from tasks.t0072_synaptic_traces_pd_nd.code.paths import (AGGREGATED_NPZ, BED_A_FIG_PNG, BED_B_FIG_PNG)`

   Logic:

   1. Load `data/aggregated.npz`.

   2. Bed A figure (`fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 16), sharex=True)`):

      * Rows in order: AMPA (row 0), NMDA (row 1), GABA (row 2), ACh (row 3).
      * Col 0: g(t) in nS. Col 1: I(t) in pA.
      * Per panel: plot PD as solid blue line `ax.plot(t_ms, mean, color="C0", label="PD")`; ND as
        solid red `ax.plot(t_ms, mean, color="C3", label="ND")`. Add ±1 SD shaded bands via
        `ax.fill_between(t_ms, mean - std, mean + std, color="C0", alpha=0.25)` and same for ND with
        `color="C3"`.
      * Set per-panel title (e.g., "AMPA conductance", "AMPA current"). x-label "Time (ms)" on
        bottom row only. y-labels: "g (nS)" col 0, "I (pA)" col 1.
      * Legend on top-left panel only.
      * `plt.tight_layout()`; `fig.savefig(BED_A_FIG_PNG, dpi=150, bbox_inches="tight")`.

   3. Bed B figure (`fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), sharex=True)`):

      * Rows: ACh (row 0), GABA (row 1). Cols: g, I. Same overlay format as Bed A.
      * Save to `BED_B_FIG_PNG`.

   Expected output: both PNG files exist in `results/images/`, each ≥ 50 KB. Visual check: PD and
   ND are visibly different on at least the GABA panel for each bed.

   Satisfies REQ-6 (Bed A figure) and REQ-7 (Bed B figure).

8. **Create `code/render_pdf.py`.** Copy verbatim from
   `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` (59 lines), changing only the import path
   on line 11 from `tasks.t0071_t0070_synaptic_eqs_pdf.code.paths` to
   `tasks.t0072_synaptic_traces_pd_nd.code.paths`. The body (`compile_typst`, `CompileResult`,
   `MIN_PDF_SIZE_BYTES = 50_000`) is unchanged.

   Also write a minimal `results/results_detailed.typ` source that includes the two PNG figures via
   `#image("images/bed_a_synaptic_traces.png", width: 100%)` and the same for Bed B, plus
   placeholder section headings (`= Synaptic Traces (PD vs ND)`, `== Bed A`, `== Bed B`) so the
   typst source compiles. The orchestrator's results-writing step will replace these placeholders
   with the full prose writeup.

   Run:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0072_synaptic_traces_pd_nd -- uv run python -m tasks.t0072_synaptic_traces_pd_nd.code.render_pdf`.

   Expected output: `results/results_detailed.pdf` exists with size ≥ 50 KB.

   Satisfies REQ-9.

**No expensive operations**: no API calls, no remote compute, no model training, no large-scale data
processing (12 files, ~50 MB total). The standard validation gates (`--limit`, baseline comparison)
do not apply. Defensive checks instead: each runner asserts per-synapse vector lengths are
consistent before saving (catches misordered `finitialize`); the aggregator asserts all 12 `t_ms`
arrays are identical before reducing to one shared `t_ms`.

**Registered metrics applicability**: the four registered metrics in `meta/metrics/`
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) measure DSI and tuning-curve properties. This task records synaptic conductance
and current waveforms only — it does not compute spike-rate tuning curves across multiple bar
angles, and it runs only one PD trial and one ND trial (insufficient for tuning-curve fitting or
reliability across repeated noisy trials). Therefore the orchestrator should write `metrics.json` as
an empty object `{}` per the metrics specification's instruction that "tasks that do not measure any
registered metrics ... must write an empty object `{}`". This omission is deliberate and documented
here.

## Remote Machines

None required. All four trials (Bed A PD, Bed A ND, Bed B PD, Bed B ND) run on the local Windows
workstation in well under 5 minutes wall-clock total. The NEURON simulator is installed locally; no
GPU is needed for compartmental modeling at this scale.

## Assets Needed

* **`modeldb_189347_dsgc` library** (from `t0008_port_modeldb_189347`) — Bed A cell builder and
  parameter applicator. Imported, not copied. Registered library; entry points: `build_dsgc()`,
  `apply_params()`, `read_synapse_coords()`, `SynapseCoords`.
* **`de_rosenroll_2026_dsgc` library** (from `t0024_port_de_rosenroll_2026_dsgc`) — Bed B cell
  builder. Imported, not copied. Registered library; entry points: `build_dsgc_cell()`, `DSGCCell`
  dataclass, plus the `ar2_noise.generate_ar2_batch` function.
* **`tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py`** lines 100-150 — Bed A
  per-synapse recorder pattern. Copied (not library-registered).
* **`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`** lines 80-226 —
  `_setup_synapses`, `SynapseBundle`, `_bar_arrival_times`, `_rates_with_ar2_noise`,
  `_gaba_prob_for_direction`, `_rates_to_events`. Copied (private API).
* **`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py`** lines 205-298 — Bed B trial
  runner body. Copied (mode-switching logic stripped).
* **`tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py`** — Typst PDF compiler. Copied
  verbatim (only import path changes).
* External resources: none. No new datasets, papers, or downloads.

## Expected Assets

This task's `task.json` declares `expected_assets: {}` (no formal asset registrations expected). The
output is research-and-visualization artifacts, not registerable assets. Concretely the task
produces:

* **Raw trace data**: 12 compressed numpy archives in `tasks/t0072_synaptic_traces_pd_nd/data/`
  named `bed_a_{pd,nd}_{ampa,nmda,gaba,ach}.npz` (8 files) and `bed_b_{pd,nd}_{ach,gaba}.npz` (4
  files). Each contains `g_traces`, `v_local_traces`, `t_ms` arrays.
* **Aggregated trace data**: `tasks/t0072_synaptic_traces_pd_nd/data/aggregated.npz` with
  per-`(bed, direction, type)` `g_mean`, `g_std`, `I_mean`, `I_std` arrays plus shared `t_ms`.
* **Figures**: `tasks/t0072_synaptic_traces_pd_nd/results/images/bed_a_synaptic_traces.png` (4×2)
  and `tasks/t0072_synaptic_traces_pd_nd/results/images/bed_b_synaptic_traces.png` (2×2).
* **Writeup**: `tasks/t0072_synaptic_traces_pd_nd/results/results_detailed.typ` (Typst source) and
  `results_detailed.pdf` (compiled PDF). The `.md` version is written by the orchestrator during the
  results-writing step.

## Time Estimation

* Research stage (already done): ~1 hour (research_code.md exists).

* Planning stage (this stage): 30-45 minutes.

* Implementation:

  * Step 1 (`code/paths.py`): 5 minutes.
  * Step 2 (`code/constants.py`): 10 minutes.
  * Steps 4-5 (`code/run_bed_a.py`, `code/run_bed_b.py`): 60-90 minutes (bulk of the work — 80
    lines + 200 lines including copied helpers).
  * Step 6 (`code/aggregate.py`): 20 minutes.
  * Step 7 (`code/plot_traces.py`): 30 minutes.
  * Step 8 (`code/render_pdf.py` + Typst source): 15 minutes.
  * Total implementation: 2.5-3 hours.

* Validation runs: 5 minutes wall-clock for all 4 NEURON trials combined.

* Verificator runs: <1 minute.

* Orchestrator results-writing (out of plan scope): 30-60 minutes.

Total task wall-clock excluding orchestrator results stage: 3-4 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Recording vectors on 282 synapses × 5 traces × 2 directions exceed available RAM. | Low | Blocking | `RECORD_DT_MS = 1.0` keeps per-trace size at 8 KB → ~22 MB raw per Bed A direction. Drop recorder list between PD and ND runs to release Python references; NEURON also frees Vector buffers on next `finitialize`. If still OOM, raise `RECORD_DT_MS` to 2.0 (halves memory). |
| Bed B's Exp2Syn `g` is in µS (microsiemens), not nS. Mixing units in the post-hoc `I = g · (v − E_rev)` formula gives wrong currents on Bed B. | Medium | Wrong physics in Bed B I plot | The aggregator (Step 6) explicitly multiplies Bed B `g` by 1000 to convert µS → nS before computing I. Document the conversion in `code/aggregate.py` with a comment citing this risk. The unit assertion is `I_pA = g_nS · (v_mV − E_mV)`; check by computing peak |
| Bed B's PD/ND encoding requires correctly-set bar angle (`direction_deg = 0.0` vs `180.0`). Misconfiguration produces identical traces between PD and ND. | Low | Wrong direction encoding | Mirror t0066's PD/ND configuration exactly; verify by checking that `_gaba_prob_for_direction(0.0)` returns the lower (PD) sigmoid value (~0.05) and `_gaba_prob_for_direction(180.0)` returns the higher (ND) value (~0.80). After Step 5, eyeball one PD and one ND `bed_b_*_gaba.npz` mean trace — if they overlap, debug the angle wiring before proceeding. |
| Bed A's BIPsyn release model is stochastic; per-synapse traces are sparse spikes. | High | Visual noise in individual traces (but population average is the goal) | The plot shows population mean ± SD across all 282 synapses, which smooths out the per-synapse stochasticity. This is the intended behavior — not a bug. Document the smoothing rationale in the plotting module's docstring. |
| Typst PDF compilation fails because the Typst Python wrapper does not find a Typst CLI or the Typst source has syntax errors. | Low | Blocking for REQ-9 | The pure-Python `typst` pip package bundles its own compiler — no system-level Typst install required. Test with a minimal `.typ` that contains only `= Hello` first (validates the toolchain). If `#image` syntax errors out, fall back to the simplest `image("path")` form. The `MIN_PDF_SIZE_BYTES = 50_000` warning catches truncated outputs. If still failing, write an `intervention/typst_compile_failure.md` with the exact error. |
| Bed A's `h.RGC.numsyn` returns 0 because the cell was not built. | Very low | Blocking | `build_dsgc()` does `init_sim` + `init_active` + `update`; failure raises early. Defensive assert: `assert int(h.RGC.numsyn) == 282, f"expected 282 ON synapses, got {int(h.RGC.numsyn)}"` immediately after `build_dsgc()` in `run_bed_a.py`. |

## Verification Criteria

* **All 12 raw `.npz` trace files exist**:

  ```bash
  uv run python -c "from pathlib import Path; \
    files = ['bed_a_pd_ampa.npz','bed_a_nd_ampa.npz','bed_a_pd_nmda.npz','bed_a_nd_nmda.npz', \
             'bed_a_pd_gaba.npz','bed_a_nd_gaba.npz','bed_a_pd_ach.npz','bed_a_nd_ach.npz', \
             'bed_b_pd_ach.npz','bed_b_nd_ach.npz','bed_b_pd_gaba.npz','bed_b_nd_gaba.npz']; \
    p = Path('tasks/t0072_synaptic_traces_pd_nd/data'); \
    print('OK' if all((p/f).exists() for f in files) else 'MISSING')"
  ```

  Expected output: `OK`. This confirms REQ-1, REQ-2, REQ-3 outputs are present.

* **Bed A npz arrays have correct shape and the aggregator finds matching time axes**:

  ```bash
  uv run python -c "import numpy as np; \
    d = np.load('tasks/t0072_synaptic_traces_pd_nd/data/bed_a_pd_ampa.npz'); \
    print('g shape:', d['g_traces'].shape, 'v shape:', d['v_local_traces'].shape, \
          't shape:', d['t_ms'].shape); \
    assert d['g_traces'].shape == (282, 1001), 'wrong Bed A trace shape'; \
    print('Bed A AMPA shape OK')"
  ```

  Expected output:
  `g shape: (282, 1001) v shape: (282, 1001) t shape: (1001,)\nBed A AMPA shape OK`. This confirms
  REQ-1 evidence in detail.

* **Aggregated mean/SD arrays exist and have non-zero variance**:

  ```bash
  uv run python -c "import numpy as np; \
    d = np.load('tasks/t0072_synaptic_traces_pd_nd/data/aggregated.npz'); \
    keys_g_pd = [k for k in d.files if k.endswith('_g_mean') and '_pd_' in k]; \
    print('PD g_mean keys:', len(keys_g_pd)); \
    assert len(keys_g_pd) == 6, f'expected 6 PD g_mean keys (4 Bed A + 2 Bed B), got {len(keys_g_pd)}'; \
    a = d['bed_a_pd_gaba_g_mean']; \
    b = d['bed_a_nd_gaba_g_mean']; \
    diff = float(np.abs(a - b).max()); \
    print(f'Bed A GABA PD vs ND max abs diff in g_mean: {diff:.4f} nS'); \
    assert diff > 0.0, 'PD and ND GABA traces are identical (gabaMOD swap not applied)'"
  ```

  Expected output:
  `PD g_mean keys: 6\nBed A GABA PD vs ND max abs diff in g_mean: <some positive number> nS`. This
  confirms REQ-4, REQ-5, and that the gabaMOD swap actually changes the GABA trace (sanity check for
  REQ-1 / REQ-2 protocol).

* **Both PNG figures exist with size ≥ 50 KB**:

  ```bash
  uv run python -c "from pathlib import Path; \
    a = Path('tasks/t0072_synaptic_traces_pd_nd/results/images/bed_a_synaptic_traces.png'); \
    b = Path('tasks/t0072_synaptic_traces_pd_nd/results/images/bed_b_synaptic_traces.png'); \
    print(f'Bed A: {a.exists()}, {a.stat().st_size if a.exists() else 0} B'); \
    print(f'Bed B: {b.exists()}, {b.stat().st_size if b.exists() else 0} B'); \
    assert a.exists() and a.stat().st_size >= 50_000; \
    assert b.exists() and b.stat().st_size >= 50_000"
  ```

  Expected output: both files report `True` and size ≥ 50000. Confirms REQ-6 and REQ-7.

* **PDF compiles via render_pdf.py**:

  ```bash
  uv run python -m arf.scripts.utils.run_with_logs --task-id t0072_synaptic_traces_pd_nd -- \
    uv run python -m tasks.t0072_synaptic_traces_pd_nd.code.render_pdf
  ```

  Expected output: stdout shows `Compiled: ...results_detailed.typ`,
  `Output: ...results_detailed.pdf`, `Size: <bytes ≥ 50000>`. Process exit code 0. Confirms REQ-9.

* **All standard verificators pass on the produced artifacts**:

  ```bash
  uv run python -m arf.scripts.verificators.verify_plan t0072_synaptic_traces_pd_nd
  ```

  Expected output: zero errors. Plan structure check passes.

* **Requirement coverage check**: every `REQ-*` ID in this plan is referenced by at least one step
  in the Step by Step section. Run:

  ```bash
  uv run python -c "import re; \
    text = open('tasks/t0072_synaptic_traces_pd_nd/plan/plan.md', encoding='utf-8').read(); \
    reqs = set(re.findall(r'REQ-\d+', text)); \
    print(f'REQs found in plan: {sorted(reqs)}'); \
    expected = {f'REQ-{i}' for i in range(1, 11)}; \
    assert reqs >= expected, f'missing REQs: {expected - reqs}'"
  ```

  Expected output: `REQs found in plan: ['REQ-1', 'REQ-10', 'REQ-2', ..., 'REQ-9']`. Confirms all 10
  requirements are present.
