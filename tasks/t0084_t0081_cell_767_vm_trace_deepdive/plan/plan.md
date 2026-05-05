---
spec_version: "2"
task_id: "t0084_t0081_cell_767_vm_trace_deepdive"
date_completed: "2026-05-05"
status: "complete"
---
# Plan: Vm-Trace Deep-Dive of t0081 Cell 767 to Attribute DSI Mechanism

## Objective

Attribute the biophysical mechanism responsible for cell 767's joint-pass DSI result (DSI 0.494 / PD
11.39 Hz) — the first cell in the project lineage to satisfy `DSI >= 0.4 AND PD >= 10 Hz`
simultaneously — to one or a combination of three active dendritic mechanisms: (1) NMDA Mg-block
gain modulation, (2) distal Nav1.6 dendritic spikes, (3) NaP sustained depolarisation.

The task re-evaluates three cells from t0081's Pareto front (767, 637, 762) on the v3 substrate with
extended recording (per-section Vm, NMDA conductance, Nav1.6/NaP current, AIS spike onset). It
produces 12 figure assets (4 per cell) and one answer asset at
`assets/answer/cell-767-dendritic-spike-mechanism-attribution/`.

**Success criteria**:

* All 24 simulations complete with stable Vm traces (no NaN, no numerical instabilities).
* 12 PNG figures generated and saved to `results/images/`.
* One answer asset produced at `assets/answer/cell-767-dendritic-spike-mechanism-attribution/` with
  `details.json`, `short_answer.md`, `full_answer.md`.
* Fractional-channel-contribution metric computed for cells 767, 637, 762 and embedded in both the
  figure and the answer asset.
* Answer clearly identifies the dominant mechanism (or combination) with quantitative support.
* Pass criterion commentary for near-pass cells 637 and 762 consistent with cell 767, or discrepancy
  documented as "near-pass cluster heterogeneity."

## Task Requirement Checklist

Operative task text (from `task.json` name + `short_description` + `task_description.md`):

> "Per-direction Vm traces of t0081 cells 767 / 637 / 762 (proximal soma, mid dendrite, distal
> dendrite) to attribute cell 767's joint-pass DSI to NMDA Mg-block, distal Nav1.6, NaP, or
> combination."
>
> Detailed scope (from `task_description.md`):
>
> * Re-evaluate cells 767, 637, 762 on the v3 substrate in eval-mode (no NSGA-II loop).
> * For each cell and each of 8 directions (0, 45, 90, 135, 180, 225, 270, 315 deg), record: Vm at
>   proximal soma, mid-dendrite, distal dendrite; per-segment NMDA conductance trajectories;
>   per-segment Nav1.6 and NaP currents; per-direction AIS spike onset times.
> * Generate 4 figures per cell (12 total): (1) per-direction Vm traces 3-row × 8-col grid, (2)
>   NMDA conductance trajectories 8-line plot, (3) Nav1.6/NaP stacked current plot, (4) AIS spike
>   onset histogram.
> * Compute fractional-channel-contribution attribution metric per cell.
> * Produce one answer asset at `assets/answer/cell-767-dendritic-spike-mechanism-attribution/`.
> * Confidence must reflect single-cell-replicate nature; generalisation requires t0083.

Decomposed requirements:

* **REQ-1**: Run 8 simulations per cell (1 seed per direction) × 3 cells = 24 simulations total on
  the v3 substrate using cell 767, 637, 762 parameter vectors verbatim from t0081's
  `all_evaluations.json`. All simulations must complete without NaN Vm. Satisfied by Step 1–3.

* **REQ-2**: Record Vm at three locations per simulation: proximal soma (`cell.soma(0.5)`),
  mid-dendrite (first `non_terminal_dends` section midpoint), distal dendrite (first
  `terminal_dends` section midpoint). Satisfied by Step 3.

* **REQ-3**: Record per-synapse NMDA conductance trajectories (`Exp2NMDA._ref_g`, uS) at distal
  dendrite synapses. Satisfied by Step 3.

* **REQ-4**: Record Nav1.6 (`nav16t80._ref_i`, mA/cm²) and NaP (`napt80._ref_i`, mA/cm²) currents
  at each segment of the representative terminal dendrite. Satisfied by Step 3.

* **REQ-5**: Record AIS Vm at `cell.ais_distal(0.5)` and compute spike onset times by threshold
  crossing at AP_THRESHOLD_MV = -10.0 mV. Satisfied by Steps 3, 4.

* **REQ-6**: Generate Figure 1 per cell — per-direction Vm traces at soma/mid/distal (3 rows × 8
  columns grid PNG). Satisfied by Step 5.

* **REQ-7**: Generate Figure 2 per cell — NMDA conductance trajectories at distal dendrite per
  direction (8-line overlay plot PNG). Satisfied by Step 5.

* **REQ-8**: Generate Figure 3 per cell — Nav1.6/NaP current decomposition at distal dendrite per
  direction (8-direction stacked plot PNG). Satisfied by Step 5.

* **REQ-9**: Generate Figure 4 per cell — AIS spike onset histogram per direction (polar or 8-bin
  bar chart PNG). Satisfied by Step 5.

* **REQ-10**: Compute fractional-channel-contribution attribution metric for each cell: fractional
  contribution of each channel (NMDA, Nav1.6, NaP) to (PD-window integral minus ND-window integral)
  of channel current, normalised to the sum of absolute deltas. Integration window: [200, 1200] ms.
  Satisfied by Step 6.

* **REQ-11**: Produce answer asset `assets/answer/cell-767-dendritic-spike-mechanism-attribution/`
  containing `details.json` (spec_version "2"), `short_answer.md`, `full_answer.md` per answer-asset
  spec v2. Answer attributes cell 767's mechanism with quantitative evidence. Satisfied by Step 7.

* **REQ-12**: Mechanism attribution for cells 637 and 762 must be assessed for consistency with cell
  767's attribution. Discrepancies documented as "near-pass cluster heterogeneity." Satisfied by
  Steps 6–7.

* **REQ-13**: Answer asset confidence level must explicitly state single-cell-replicate limitation;
  generalisation to "all joint-pass cells in v3 substrate" requires t0083. Satisfied by Step 7.

* **REQ-14**: All 12 PNGs embedded in `results/results_detailed.md` (handled by the orchestrator's
  results step; the implementation step must save them to `results/images/`). Satisfied by Step 5.

## Approach

**Research findings informing the approach** (from `research_code.md`):

The v3 substrate library `de_rosenroll_2026_dsgc_ais_dendritic_spike` (t0080) provides all required
entry points:

* `build_dsgc_cell_with_ais()` → `DSGCCellWithAIS` with `soma`, `non_terminal_dends`,
  `terminal_dends`, `ais_proximal`, `ais_distal`.
* `apply_parameter_vector(cell, params)` writes the 54-d `ParameterVector` to all sections,
  including v3 overlay: `gbar_nav16t80` and `gbar_napt80` on `terminal_dends`.
* `setup_synapses_parametric(...)` creates `SynapseBundle.syns_nmda` (list of `Exp2NMDA` handles).
* `run_one_trial(cell, bundle, direction_deg, seed)` runs one simulation and returns spike count +
  peak Vm. The implementation will wrap this to attach recording vectors first.
* `max_workers=1` mode required for NEURON `h.Vector.record()` — vectors are not pickleable.

**NEURON recording variables** (confirmed from mod files):

* Vm: `section(x)._ref_v` (standard NEURON variable)
* NMDA conductance: `nmda_syn._ref_g` (uS; `Exp2NMDA.mod` RANGE variable `g`)
* Nav1.6 current: `seg.nav16t80._ref_i` (mA/cm²)
* NaP current: `seg.napt80._ref_i` (mA/cm²)

**Attribution metric** (integrated current approach):

For each channel `c` in {NMDA, Nav1.6, NaP}:

* Compute `I_c(t)` = channel current in nA (convert mA/cm² × section_area_cm² for density-based;
  for NMDA: `g_nmda(t) × (v_dend(t) - 0.0) × 1000` to get nA from uS × mV).
* Integrate `I_c(t)` from t=200 ms to t=1200 ms for PD direction (direction 0°) and ND direction
  (direction 180°).
* Fractional contribution: `|Δ_c| / Σ|Δ_c|` where `Δ_c = integral_PD_c - integral_ND_c`.

**Alternative approach considered**: Channel knockout (set one channel's gbar to 0, rerun, compare
DSI change). This would be more direct but requires 9 additional simulations per cell and modifies
the parameter vector, violating the "verbatim params" constraint. Rejected in favour of passive
current decomposition from a single verbatim evaluation per direction.

**Task types applied**: `experiment-run` (24 NEURON simulations), `data-analysis` (current
decomposition + figure generation), `answer-question` (mechanism attribution). Following the
experiment-run planning guidelines: fixed seed (SEED_BASE = 1000), cost cap = $0, reproducible
pipeline.

**Registered metrics applicable**: `direction_selectivity_index` — this task computes DSI per cell
from the 8-direction spike counts (PD-direction rate and ND-direction rate are measured). The other
registered metrics (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) are
not applicable because this task does not compare against a target tuning curve (it is a
mechanism-attribution deep-dive, not an optimisation evaluation).

## Cost Estimation

* Remote compute: **$0**. All simulations run locally on CPU (NEURON, sequential mode).
* API calls: **$0**. No LLM calls required.
* **Total: $0**.
* Project budget remaining: $11.87 / $20.00. Well within the $5.00 per-task default limit.

## Step by Step

### Milestone 1: Set Up Code Infrastructure

1. **[CRITICAL] Create `code/paths.py`** — centralise all `pathlib.Path` constants used across
   this task's modules. Define:

   ```python
   ALL_EVALUATIONS_JSON: Path = Path("tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json")
   RESULTS_DATA_DIR: Path = Path("tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data")
   RESULTS_IMAGES_DIR: Path = Path("tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images")
   ANSWER_DIR: Path = Path("tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution")
   ```

   Create `results/data/` directory (mkdir). Satisfies infrastructure for all REQs.

2. **[CRITICAL] Create `code/constants.py`** — task-local constants not in the t0080 library:

   ```python
   CELL_IDS: tuple[int, ...] = (767, 637, 762)
   RESPONSE_WINDOW_START_MS: float = 200.0
   RESPONSE_WINDOW_END_MS: float = 1200.0
   RECORD_DT_MS: float = 1.0          # matches t0080 RECORD_DT_MS
   NMDA_EREV_MV: float = 0.0          # Exp2NMDA e = 0.0 mV
   ```

### Milestone 2: Simulation and Recording

3. **[CRITICAL] Create `code/run_deepdive.py`** — main simulation driver. This is the core
   deliverable. Steps:

   a. Load parameter vectors: `json.load(ALL_EVALUATIONS_JSON)`, find entries with
   `cell_index in (767, 637, 762)`, construct `ParameterVector(values=np.array(entry["params"]))`
   for each. Imports:
   `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParameterVector`

   b. Build cell once: `cell = build_dsgc_cell_with_ais()`. Import:
   `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import build_dsgc_cell_with_ais, DSGCCellWithAIS`

   c. For each cell ID, call `apply_parameter_vector(cell=cell, params=pv)` and
   `setup_synapses_parametric(h=cell.h, cell=cell, n_ach=pv.n_ach, ..., gnmda_dend=pv.gnmda_dend, mg_conc_mm=pv.mg_conc_mm, voff_nmda=pv.voff_nmda)`
   to get `SynapseBundle`. Imports:
   `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import apply_parameter_vector`
   `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import setup_synapses_parametric, SynapseBundle, ...`

   d. Identify recording sections for this cell:
   * `sec_soma = cell.soma` (record at x=0.5)
   * `sec_mid = cell.non_terminal_dends[0]` (record at x=0.5)
   * `sec_distal = cell.terminal_dends[0]` (record at x=0.5; same section receiving v3 overlay)
   * `sec_ais = cell.ais_distal` (record at x=0.5 for AIS spike onset)

   e. For each direction in `ANGLES_8DIR_DEG = (0, 45, 90, 135, 180, 225, 270, 315)` (from t0080
   constants):

   Before `h.run()`, attach recording vectors:

   ```python
   h = cell.h
   t_vec = h.Vector(); t_vec.record(h._ref_t, RECORD_DT_MS)
   v_soma = h.Vector(); v_soma.record(cell.soma(0.5)._ref_v, RECORD_DT_MS)
   v_mid = h.Vector(); v_mid.record(sec_mid(0.5)._ref_v, RECORD_DT_MS)
   v_distal = h.Vector(); v_distal.record(sec_distal(0.5)._ref_v, RECORD_DT_MS)
   v_ais = h.Vector(); v_ais.record(cell.ais_distal(0.5)._ref_v, RECORD_DT_MS)
   g_nmda_vecs = [h.Vector() for _ in bundle.syns_nmda]
   for vec, syn in zip(g_nmda_vecs, bundle.syns_nmda):
       vec.record(syn._ref_g, RECORD_DT_MS)
   i_nav16_vecs = [h.Vector() for seg in sec_distal]
   i_nap_vecs = [h.Vector() for seg in sec_distal]
   for vec, seg in zip(i_nav16_vecs, sec_distal):
       vec.record(seg.nav16t80._ref_i, RECORD_DT_MS)
   for vec, seg in zip(i_nap_vecs, sec_distal):
       vec.record(seg.napt80._ref_i, RECORD_DT_MS)
   ```

   Use the existing `run_one_trial(cell=cell, bundle=bundle, direction_deg=direction, seed=seed)`
   where seed = SEED_BASE = 1000 for all directions (single replicate per direction). Import:
   `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import run_one_trial, _worker_prepare`

   After `h.run()`, harvest vectors to numpy arrays:

   * `v_soma_arr`, `v_mid_arr`, `v_distal_arr`, `v_ais_arr` — shape (n_timepoints,)
   * `g_nmda_arr` — shape (n_nmda_syns, n_timepoints)
   * `i_nav16_arr`, `i_nap_arr` — shape (n_segs_distal, n_timepoints)
   * `t_arr` — shape (n_timepoints,)

   Save to `.npz` per cell per direction:
   `RESULTS_DATA_DIR / f"cell{cell_id}_dir{int(direction)}_traces.npz"` Keys: `t_ms`, `v_soma_mv`,
   `v_mid_mv`, `v_distal_mv`, `v_ais_mv`, `g_nmda_us`, `i_nav16_ma_cm2`, `i_nap_ma_cm2`,
   `direction_deg`, `cell_id`.

   f. Also record spike count from `run_one_trial` return value to validate DSI.

   g. Save per-cell summary `RESULTS_DATA_DIR / f"cell{cell_id}_summary.json"` with keys: `cell_id`,
   `generation`, `dsi_original`, `pd_rate_hz_original`, `v3_params`, `recording_sections` (soma
   name, mid name, distal name).

   Satisfies REQ-1, REQ-2, REQ-3, REQ-4, REQ-5.

   **Validation gate**: After running cell 767 direction 0° (PD), check that spike_count >= 1 (PD
   direction should produce spikes). If spike_count == 0 for PD, STOP and inspect the Vm trace —
   the cell may have failed to load correctly. Expected: 10–20 spikes in 1400 ms at PD.

### Milestone 3: Figure Generation

4. **Create `code/attribution_metric.py`** — compute fractional channel contribution:

   Load all `.npz` files for a given cell. For PD (direction=0) and ND (direction=180):

   * NMDA current: `I_nmda(t) = np.sum(g_nmda_arr, axis=0) * (v_distal_mv - NMDA_EREV_MV) * 1e-3` (g
     in uS × voltage in mV → result in nA after ×1e-3 = × 1/1000 µS→nS scaling; actually
     g[uS] × ΔV[mV] = current[nA] directly since 1 uS × 1 mV = 1 nA). Sum over synapses.
   * Nav1.6 current: `I_nav16(t) = np.sum(i_nav16_arr * sec_area_cm2, axis=0) × 1e6` (mA/cm² ×
     cm² = mA → ×1e6 → nA). Sum over segments.
   * NaP current: same as Nav1.6 but using `i_nap_arr`.

   Get time mask: `mask = (t_ms >= 200) & (t_ms <= 1200)`.

   Integrals (trapezoid): `int_c = np.trapz(I_c[mask], t_ms[mask])` for each channel and direction.

   Delta: `delta_c = int_c_PD - int_c_ND`.

   Fractional contribution: `frac_c = |delta_c| / sum(|delta_c| for all channels)`.

   Return dataclass `AttributionResult` with fields: `cell_id`, `frac_nmda`, `frac_nav16`,
   `frac_nap`, `delta_nmda_nA_ms`, `delta_nav16_nA_ms`, `delta_nap_nA_ms`, `dominant_mechanism`.
   `dominant_mechanism` is the channel with the highest fractional contribution.

   Save to `RESULTS_DATA_DIR / f"cell{cell_id}_attribution.json"`.

   Satisfies REQ-10, REQ-12.

5. **Create `code/plot_figures.py`** — generate 4 figures per cell using `matplotlib`:

   For each cell in (767, 637, 762):

   * **Figure 1** (`cell{id}_fig1_vm_traces.png`): 3-row × 8-col subplot grid. Row 0 = soma Vm; Row
     1 = mid-dendrite Vm; Row 2 = distal-dendrite Vm. Each column = one direction. X-axis: t
     0–1400 ms; Y-axis: Vm (mV). Title: "Cell {id}: Per-direction Vm traces". Label each column
     with the direction angle. REQ-6.

   * **Figure 2** (`cell{id}_fig2_nmda_conductance.png`): 8-line overlay plot. X: t 0–1400 ms; Y:
     total NMDA g (uS, sum over synapses). One line per direction, colour-coded. Legend shows
     direction angles. REQ-7.

   * **Figure 3** (`cell{id}_fig3_nav16_nap_current.png`): 8-direction stacked subplots. X: t
     0–1400 ms; Y: total Nav1.6 current (nA, sum over segments) and NaP current (nA), shown as two
     overlaid lines per subplot. 8 subplots arranged 4×2 or 2×4. REQ-8.

   * **Figure 4** (`cell{id}_fig4_ais_spikes.png`): polar plot or 8-bin bar chart. Compute spike
     onset times from `v_ais_mv` threshold crossings at AP_THRESHOLD_MV = -10.0 mV. Plot spike count
     per direction. Colour PD (0°) in orange, ND (180°) in blue. REQ-9.

   Save all 12 PNGs to `RESULTS_IMAGES_DIR`. Include axis labels, titles, legends.

   Satisfies REQ-6, REQ-7, REQ-8, REQ-9, REQ-14.

### Milestone 4: Answer Asset Production

6. **[CRITICAL] Create `code/answer_writer.py`** — write the answer asset:

   a. Load attribution results for cells 767, 637, 762 from their JSON files. b. Create `ANSWER_DIR`
   and all required subdirectory structure. c. Write
   `assets/answer/cell-767-dendritic-spike-mechanism-attribution/details.json`:
   ```json
   {
     "spec_version": "2",
     "answer_id": "cell-767-dendritic-spike-mechanism-attribution",
     "question": "Which biophysical mechanism — NMDA Mg-block, distal Nav1.6, NaP, or a combination — is responsible for cell 767's joint-pass DSI improvement in the v3 Bed B substrate?",
     "short_title": "Cell 767 DSI mechanism attribution",
     "short_answer_path": "short_answer.md",
     "full_answer_path": "full_answer.md",
     "categories": ["active-dendrites", "dsi-mechanism"],
     "answer_methods": ["code-experiment"],
     "source_paper_ids": [],
     "source_urls": [],
     "source_task_ids": ["t0080_bedb_mobo_v3_dendritic_spike_nsga2", "t0081_bedb_v3_warmstart_nsga2"],
     "confidence": "medium",
     "created_by_task": "t0084_t0081_cell_767_vm_trace_deepdive",
     "date_created": "<ISO_DATE>"
   }
   ```
   Confidence is "medium" (single replicate per direction; no seed-to-seed variance quantified).

   d. Write `short_answer.md` with mandatory sections: `## Question`, `## Answer` (2–5 sentences,
   decisive, with dominant mechanism and fractional contributions), `## Sources`.

   e. Write `full_answer.md` with all 9 mandatory sections per answer-asset spec v2: `## Question`,
   `## Short Answer`, `## Research Process`, `## Evidence from Papers`,
   `## Evidence from Internet Sources`, `## Evidence from Code or Experiments`, `## Synthesis`,
   `## Limitations` (explicitly state single-replicate constraint), `## Sources`.

   f. Run
   `uv run python -m arf.scripts.verificators.verify_answer_asset --task-id t0084_t0081_cell_767_vm_trace_deepdive cell-767-dendritic-spike-mechanism-attribution`.
   Fix all errors before proceeding.

   Satisfies REQ-11, REQ-12, REQ-13.

### Milestone 5: Metrics and Quality Checks

7. **Compute `direction_selectivity_index`** (the one applicable registered metric) from the
   per-direction spike counts recorded in Step 3. DSI = (R_PD - R_ND) / (R_PD + R_ND). Record spike
   counts for PD (0°) and ND (180°) for each cell. Write to `results/metrics.json` using the
   explicit variant format — one variant per cell:

   ```json
   {
     "variants": [
       {
         "variant_id": "cell-767",
         "label": "Cell 767 (joint-pass)",
         "dimensions": {"cell_id": 767, "generation": 7},
         "metrics": {"direction_selectivity_index": <value>}
       },
       ...
     ]
   }
   ```

   Also write:
   * `results/costs.json`: `{"total_cost_usd": 0, "breakdown": {}}`
   * `results/remote_machines_used.json`: `[]`

8. **Run ruff and mypy on all new code**:
   ```
   uv run ruff check --fix tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/
   uv run ruff format tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/
   uv run mypy -p tasks.t0084_t0081_cell_767_vm_trace_deepdive.code
   ```
   Fix all errors.

9. **Run the full simulation pipeline end-to-end**:
   ```
   uv run python -m arf.scripts.utils.run_with_logs --task-id t0084_t0081_cell_767_vm_trace_deepdive -- uv run python -u tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py
   ```
   Expected: 24 `.npz` files and 3 `_summary.json` files in `results/data/`.

10. **Run figure generation and attribution**:
    ```
    uv run python -m arf.scripts.utils.run_with_logs --task-id t0084_t0081_cell_767_vm_trace_deepdive -- uv run python -u tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/plot_figures.py
    uv run python -m arf.scripts.utils.run_with_logs --task-id t0084_t0081_cell_767_vm_trace_deepdive -- uv run python -u tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/attribution_metric.py
    uv run python -m arf.scripts.utils.run_with_logs --task-id t0084_t0081_cell_767_vm_trace_deepdive -- uv run python -u tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/answer_writer.py
    ```
    Expected: 12 PNGs in `results/images/`, 3 `_attribution.json` files in `results/data/`, answer
    asset files at `assets/answer/cell-767-dendritic-spike-mechanism-attribution/`.

## Remote Machines

None required. All 24 simulations run locally on CPU using NEURON in sequential mode
(`max_workers=1`). Estimated total runtime: 15–30 minutes.

## Assets Needed

* **v3 substrate library** (`de_rosenroll_2026_dsgc_ais_dendritic_spike`): provided by dependency
  `t0080_bedb_mobo_v3_dendritic_spike_nsga2`. Import path:
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.*`.

* **NEURON mod files** (compiled `nrnmech` library): located at
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/x86_64/` (Linux) or equivalent compiled path.
  The `bootstrap.py` in t0080 handles DLL loading via `ensure_t80_dll_loaded(h)`.

* **Cell parameter vectors**:
  `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json`. Read at runtime; cells
  767, 637, 762 identified by `cell_index` field.

* **NEURON simulator**: installed in the Python environment via `uv sync`. Confirmed present as a
  dependency of the t0080 library.

## Expected Assets

* **Answer asset** (1): `assets/answer/cell-767-dendritic-spike-mechanism-attribution/` containing
  `details.json`, `short_answer.md`, `full_answer.md`. Answers the question: which biophysical
  mechanism is responsible for cell 767's joint-pass DSI? This matches `task.json`
  `expected_assets: {"answer": 1}`.

## Time Estimation

* Step 1–2 (code infrastructure): ~30 min
* Step 3 (simulation + recording, 24 simulations): ~15–30 min wall-clock
* Steps 4–5 (attribution + figures): ~20 min
* Step 6 (answer writer): ~20 min
* Steps 7–10 (metrics, lint, integration run): ~15 min
* **Total**: ~1.5–2 hours

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| NEURON DLL not compiled for local platform | Medium | Blocking | Run `nrnivmodl` from `tasks/t0080.../code/mods/`; the t0080 bootstrap.py calls `ensure_t80_dll_loaded` which should handle it; if not, rebuild manually with `cd tasks/t0080.../code/mods && nrnivmodl` |
| `_ref_g` attribute missing on `Exp2NMDA` (variable name differs from mod file) | Low | Blocking | Check with `dir(nmda_syn)` before first full run; if absent, inspect compiled mechanism attributes via `h.nrn_load_dll` output and adjust variable name |
| `_ref_i` attribute missing on `nav16t80` or `napt80` (compiled under different mechanism name) | Low | Blocking | Check `dir(seg.nav16t80)` before run; use `seg._ref_ina_nav16t80` if available; inspect mod file ASSIGNED block |
| NaN Vm in simulations (numerical instability with large gbar values) | Low | Partial | Add stability check: if `np.any(~np.isfinite(v_arr))` skip that direction and log; require at least PD and ND directions to be finite |
| Recording overhead causes simulation slowdown beyond 60 min | Low | Delay | Profile 1 direction first; if >5 min/direction, reduce `n_nmda_syns` recorded by selecting only those on `terminal_dends[0]` rather than all synapses |
| `terminal_dends[0]` has no Nav1.6/NaP inserted (wrong section identified) | Low | Partial | After `apply_parameter_vector`, assert `sec_distal.psection()['density_mechs']` contains `nav16t80` before recording; if not, iterate `terminal_dends` to find first section with the mechanism |

## Verification Criteria

* **24 `.npz` files exist** and are non-empty: run
  ```
  uv run python -c "from pathlib import Path; files=list(Path('tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data').glob('cell*_dir*_traces.npz')); print(len(files)); assert len(files)==24, files"
  ```
  Expected output: `24`.

* **12 PNG figures exist** in `results/images/`:
  ```
  uv run python -c "from pathlib import Path; pngs=list(Path('tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images').glob('cell*.png')); print(len(pngs)); assert len(pngs)==12, pngs"
  ```
  Expected: `12`.

* **Answer asset passes verificator**:
  ```
  uv run python -m arf.scripts.utils.run_with_logs --task-id t0084_t0081_cell_767_vm_trace_deepdive -- uv run python -m arf.scripts.verificators.verify_answer_asset --task-id t0084_t0081_cell_767_vm_trace_deepdive cell-767-dendritic-spike-mechanism-attribution
  ```
  Expected: PASSED with 0 errors.

* **Attribution results exist for all 3 cells**: run
  ```
  uv run python -c "import json; [json.load(open(f'tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell{c}_attribution.json')) for c in [767,637,762]]; print('OK')"
  ```
  Expected: `OK`.

* **metrics.json validates** with the task metrics verificator:
  ```
  uv run python -m arf.scripts.utils.run_with_logs --task-id t0084_t0081_cell_767_vm_trace_deepdive -- uv run python -m arf.scripts.verificators.verify_task_metrics t0084_t0081_cell_767_vm_trace_deepdive
  ```
  Expected: PASSED with 0 errors.

* **All simulations stable** (no NaN Vm): the `run_deepdive.py` script asserts stability. A
  successful run prints `[DONE] 24/24 stable simulations`.

* **REQ-11 coverage**: the answer asset `short_answer.md` `## Answer` section must name the dominant
  mechanism and state at least one fractional contribution percentage. Check manually that the
  answer is not empty or placeholder.
