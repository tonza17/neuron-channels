---
spec_version: "1"
task_id: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 8
libraries_found: 9
libraries_relevant: 3
date_completed: "2026-04-25"
status: "complete"
---
# Code Research: Minimal DSGC with AMPA + NMDA and Scalar gabaMOD (t0054)

## Task Objective

Extend the t0052 minimal DSGC by co-locating an NMDA `Exp2Syn` (`tau1=5 ms`, `tau2=80 ms`, `e=0 mV`,
voltage-independent) at every E synapse, sweep `gNMDA` over `{0.0, 0.25, 0.5, 1.0}` nS, and replace
the `AMPA_ONLY` trial mode with `E_ONLY` (AMPA + NMDA, GABA zeroed). The sweep produces 12 metric
variants (4 `gNMDA` × 3 modes × 12 directions × 10 trials = 1,440 trials), three sweep-summary
plots (EPSP decay-to-1/e vs `gNMDA`, peak Hz vs `gNMDA`, DSI vs `gNMDA`), and a new library asset
`minimal_dsgc_ampa_nmda_scalar_gaba`. The model must remain bit-identical to t0052 at `gNMDA = 0`
(validation gate) and reuse the t0052 placement (seed 0).

## Library Landscape

The project has nine registered library assets discovered by walking
`tasks/*/assets/library/*/details.json`. The library aggregator is not yet implemented in this fork
(`arf.scripts.aggregators.aggregate_libraries` raises `No module named ...`); raw asset inspection
was used as the substitute. None of the assets are flagged with corrections, so the metadata is the
effective state.

* `tuning_curve_viz` (created by [t0011], v0.1.0) — Matplotlib helpers for Cartesian / polar /
  multi-model overlay / raster+PSTH PNGs. Import path
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz`. **Relevant**: t0054 reuses
  `plot_polar_tuning_curve` and `plot_cartesian_tuning_curve` for one polar/Cartesian per-`gNMDA`
  panel (8 figures total).

* `tuning_curve_loss` (created by [t0012], v0.1.0) — Canonical scorer that returns `compute_dsi`,
  `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`,
  `load_tuning_curve`, and the `TuningCurve` dataclass. Import path
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`. **Relevant**: t0054
  computes the four registered metric keys per variant via the same six functions, exactly as t0052
  and t0053 do.

* `minimal_dsgc_scalar_gaba` (created by [t0052], v0.1.0) — The parent task's library: 12 source
  modules (`constants.py`, `paths.py`, `swc_io.py`, `cell.py`, `placement.py`,
  `neuron_bootstrap.py`, `synapses.py`, `trial.py`, `run_tuning_curve.py`, `compute_metrics.py`,
  `metrics_extra.py`, `render_figures.py`) plus two test modules (`test_quiescent_rest.py`,
  `test_gaba_mod.py`). **Relevant — but as a copy source, not as an importable dependency**.
  CLAUDE.md rule 3 forbids cross-task imports for non-library code, and although t0052's library
  asset is registered, the project pattern (validated by [t0053]) is to copy the modules into the
  new task's `code/` directory and rewrite the import paths to `tasks.t0054_*`. The library
  registration exists so verificators recognise the cross-task code-copy pattern, not so other tasks
  can `from tasks.t0052_*.code.synapses import ...` directly.

* `minimal_dsgc_spatial_gaba` (created by [t0053]) — Demonstrates the same code-copy pattern from
  t0052; not directly imported but its delta vs t0052 is the canonical reference for *how* to extend
  the t0052 codebase. **Relevant** as a structural template, especially
  `test_placement_seed0_match.py`.

* `modeldb_189347_dsgc_exact` (created by [t0046]), `modeldb_189347_dsgc` (created by [t0008]),
  `modeldb_189347_dsgc_gabamod` (created by t0020), `modeldb_189347_dsgc_dendritic` (created by
  t0022), `de_rosenroll_2026_dsgc` (created by t0024) — Five DSGC reproductions and ports. **Not
  relevant**: they all wrap the deposited Poleg-Polsky `bipolarNMDA.mod` (which compiles a custom
  voltage-dependent NMDA channel). t0054 explicitly avoids MOD compilation by using NEURON's
  built-in `Exp2Syn` for NMDA instead.

## Key Findings

### Code-copy pattern is universal across the t0052 lineage

[t0053] demonstrated the canonical pattern for extending [t0052] with a different inhibition
mechanism: every t0052 module is copied verbatim into the new task's `code/` directory, the imports
are rewritten from `tasks.t0052_minimal_dsgc_scalar_gaba.code.*` to
`tasks.t0053_minimal_dsgc_spatial_gaba.code.*`, and the `_T0052_NEURONHOME_BOOTSTRAPPED` sentinel
env var (defined in `constants.py:92`) is renamed to `_T0053_*`. Of t0053's 16 code files, 6 were
copied unchanged in spirit (only the import path rewrite), 4 were extended with a small
mechanism-specific delta, and 6 were rewritten. t0054 should follow exactly the same pattern.
[t0052] is the only direct source of non-library code; the t0046-line of NMDA-bearing code
[t0046][t0048] shares no architectural assumptions with t0052 and would be harder to fork.

### NMDA in this project so far has been MOD-compiled and voltage-dependent

[t0046] ports the deposited Poleg-Polsky `bipolarNMDA.mod`
(`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/sources/bipolarNMDA.mod`), which has
`tau1NMDA = 50 ms` (deactivation), `tau2NMDA = 2 ms` (activation), and a `Voff_bipNMDA` / `Vtau`
block that implements voltage-dependent Mg block. [t0048] turned the Mg block off
(`Voff_bipNMDA = 1`) and reported that DSI vs `gNMDA` flattens but does not collapse to the paper's
flat ~0.30 line — i.e., the voltage-independent NMDA used in t0054 is exactly the regime [t0048]
explored for the deposited cell, just with `Exp2Syn` in place of the MOD file. The t0054 spec's tau
choice (`tau1=5 ms` rise, `tau2=80 ms` decay) follows the standard `Exp2Syn` convention
(`tau1 < tau2`, both positive), giving an effective decay constant in the 50-200 ms biological range
— consistent with the literature surveys in [t0018].

### NEURON `Exp2Syn` semantics: rise tau is `tau1`, decay tau is `tau2`, weight is in microsiemens

[t0052]'s `synapses.py:93-101,115-117` constructs both AMPA and GABA `Exp2Syn` with `tau1 < tau2`,
`e` set to the reversal, and the `NetCon.weight[0]` carrying the conductance in microsiemens
(`AMPA_PEAK_NS * 1e-3`). The same convention applies to NMDA in t0054 (constants
`NMDA_TAU1_MS = 5.0`, `NMDA_TAU2_MS = 80.0`, `NMDA_E_MV = 0.0`, `gnmda_ns * 1e-3` for the NetCon
weight). Crucially, `Exp2Syn` is voltage-independent by construction — no Mg block, no `n`
exponent, no driving-force shaping beyond `i = g * (v - e)`. This is exactly what the t0054 spec
requires.

### Multi-variant `metrics.json` is a solved problem

[t0052]'s `compute_metrics.py` writes the explicit multi-variant metrics format
(`{"variants": [...]}` with each variant carrying `variant_id`, `label`, `dimensions`, `metrics`).
[t0046] and [t0048] extend this to multi-key dimensions (e.g., `(b2gnmda_ns, exptype)` in [t0048]).
t0054's 12 variants `(gnmda, mode)` follow the same pattern:
`dimensions = {"gnmda_ns": 0.5, "mode": "full"}`, `variant_id = "gnmda_0.50_full"`. The four
registered metric keys are already declared in `meta/metrics/`: `direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse` (used by [t0052]
`compute_metrics.py:36-44`).

### CVODE + dt = 0.025 ms gives ~3 s/trial on local CPU; 1,440 trials ≈ 75 min

[t0052] reported 19 min 13 s for 360 trials (3.2 s/trial), [t0053] reported 17 min 11 s (2.86
s/trial). Both used `enable_cvode(atol=1e-3)` from `neuron_bootstrap.py:70-83`. t0054's 1,440 trials
at the same per-trial cost is ~75 min — matches the task plan's wall-clock estimate. NMDA's slow
decay (`tau2 = 80 ms`) does not change per-trial cost meaningfully because CVODE adapts the time
step; the synaptic conductance state adds two state variables per synapse (200 extra ODE states for
100 NMDA synapses), which is negligible on top of the existing ~6,700 dendritic compartments and 200
AMPA + GABA synapses.

### Validation gates must include placement bit-identity and `gNMDA = 0` regression

[t0053]'s `test_placement_seed0_match.py:1-74` opens both placement JSONs, loads them as lists of
dicts, and asserts each pair's `(section_index, section_x, x_um, y_um, z_um)` matches within
`POSITION_TOLERANCE = 1e-9`. The same test, with `T0052_PLACEMENT_JSON` defined in t0054's
`paths.py`, is the placement gate for t0054. The new gate is `gNMDA = 0` regression: each row of
`tuning_curve_full.csv` at `gnmda_ns = 0.0` must match the corresponding row of
`tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv` within 1e-6 Hz. This catches
any accidental side-effect of the NMDA addition (e.g., a stale NetStim, a wrong `weight[0]` reset,
or shared state across modes).

### t0052's `_apply_mode_weights` must learn three new modes

[t0052]'s `trial.py:48-66` zeroes either AMPA or GABA NetCon weights depending on the mode. t0054
has co-located AMPA + NMDA + GABA, so `E_ONLY` (replacing `AMPA_ONLY`) must keep both AMPA and NMDA
active and zero GABA; `GABA_ONLY` must zero both AMPA and NMDA. The weight-restore block at
`trial.py:121-128` must symmetrically restore AMPA weight in `GABA_ONLY` mode and restore NMDA
weight in `GABA_ONLY` mode (both back to their `gnmda_ns * 1e-3` baseline).

## Reusable Code and Assets

### Import via library (cross-task, registered)

* **`tasks.t0011_response_visualization_library.code.tuning_curve_viz`** — used by t0054
  `render_figures.py` for the polar / Cartesian per-`gNMDA` panels. Functions:
  `plot_polar_tuning_curve(curve_csv: Path, out_path: Path, target_csv: Path | None) -> None` and
  `plot_cartesian_tuning_curve(...)`. **No adaptation needed**; t0052 `render_figures.py:198-209` is
  the exact usage pattern to copy.

* **`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`** — used by t0054
  `compute_metrics.py`. Functions: `load_tuning_curve(csv_path: Path) -> TuningCurve`,
  `compute_dsi(curve: TuningCurve) -> float`, `compute_peak_hz(curve: TuningCurve) -> float`,
  `compute_null_hz(curve: TuningCurve) -> float`, `compute_hwhm_deg(curve: TuningCurve) -> float`,
  `compute_reliability(curve: TuningCurve) -> float | None`. The `TuningCurve` dataclass exposes
  `angles_deg` and `firing_rates_hz`. **No adaptation needed**; the schema for t0054's per-mode CSVs
  is the same as t0052's, plus an extra `gnmda_ns` column that must be filtered out before passing
  to `load_tuning_curve` (or `load_tuning_curve` is invoked once per `(gnmda, mode)` group on a
  per-group temporary CSV — preferred for ergonomics).

### Copy into task (verbatim modules from [t0052])

For all of these, the only adaptation is
`s/t0052_minimal_dsgc_scalar_gaba/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/g` in import paths and
the bootstrap-sentinel rename `s/_T0052_NEURONHOME_BOOTSTRAPPED/_T0054_NEURONHOME_BOOTSTRAPPED/g`
(the sentinel value lives in `constants.py:92`, the consumers are in `neuron_bootstrap.py:38-45`).

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/__init__.py` (0 lines, empty marker).

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/swc_io.py` (180 lines) — SWC parser; pure I/O, no
  task-specific logic.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/cell.py` (215 lines) — `CellHandles`,
  `build_dsgc_from_swc`, AIS construction, channel insertion. No NMDA-related changes.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/placement.py` (87 lines) — `Location`,
  `sample_dendritic_locations`, `save_placement_json`. No changes; the task spec demands
  bit-identical placement to t0052.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/neuron_bootstrap.py` (82 lines) —
  `ensure_neuron_importable`, `load_stdrun`, `enable_cvode`. Sentinel rename only.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/metrics_extra.py` (44 lines) —
  `compute_vector_sum_dsi`, `compute_preferred_direction_deg`. No changes.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/test_quiescent_rest.py` (104 lines) — V_rest = -65 ±
  0.5 mV gate; only the import path changes.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/test_gaba_mod.py` (22 lines) — The scalar
  `gaba_mod(0)=0.33`, `gaba_mod(180)=0.99` unit test; only the import path changes (the formula in
  `synapses.py:54-73` is preserved unchanged).

* **Adopt verbatim from [t0053]**:
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_placement_seed0_match.py` (74 lines) —
  placement bit-identity test. Replace `t0053_*` import paths with `t0054_*` and add a
  `T0052_PLACEMENT_JSON` constant in t0054's `paths.py`. This is a verbatim copy of the [t0053]
  gate; no logic changes are needed because both tasks compare against the same
  `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json`.

### Copy into task and extend

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/constants.py` (125 lines → ~140 lines) — Add
  `NMDA_TAU1_MS = 5.0`, `NMDA_TAU2_MS = 80.0`, `NMDA_E_MV = 0.0`,
  `NMDA_PEAK_NS_VALUES: tuple[float, ...] = (0.0, 0.25, 0.5, 1.0)`,
  `COL_GNMDA_NS: str = "gnmda_ns"`, and replace the `TrialMode(StrEnum)` definition (lines 122-125)
  with members `FULL = "full"`, `E_ONLY = "e_only"`, `GABA_ONLY = "gaba_only"`. No legacy alias —
  the task description states that `E_ONLY` *replaces* `AMPA_ONLY`. Rename the bootstrap sentinel
  constant `NEURONHOME_SENTINEL_ENV` value to `_T0054_NEURONHOME_BOOTSTRAPPED`.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/paths.py` (78 lines → ~95 lines) — Update
  `TASK_ID = "t0054_..."` and `LIBRARY_ID = "minimal_dsgc_ampa_nmda_scalar_gaba"`. Rename per-mode
  CSVs from `*_ampa_only*` to `*_e_only*`. Add `T0052_PLACEMENT_JSON` (mirroring
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/paths.py:53-55`) and a single
  `tuning_curve_per_gnmda.csv` (with a `gnmda_ns` column) approach so downstream analysis can filter
  by `gnmda_ns` instead of opening four files. Add `EPSP_DECAY_PER_GNMDA_PNG`,
  `PEAK_HZ_VS_GNMDA_PNG`, `DSI_VS_GNMDA_PNG` for the three sweep-summary plots.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py` (181 lines → ~230 lines) — Extend
  `EiPair` with two new fields `nmda_syn: Any`, `nmda_netcon: Any` (no separate `nmda_netstim`; the
  AMPA NetStim drives both AMPA and NMDA — the task description specifies "the same NetStim
  event"). In `build_ei_pairs`, after constructing the AMPA `Exp2Syn`, build the NMDA `Exp2Syn` on
  the *same* `seg`, and a second `h.NetCon(ampa_netstim, nmda_syn)` with `weight[0] = 0.0` (set
  per-trial). Extend `schedule_ei_onsets` with a new `gnmda_ns: float` kwarg; the per-trial weight
  assignment becomes `pair.nmda_netcon.weight[0] = gnmda_ns * 1e-3`. Keep the scalar `gaba_mod`
  formula unchanged.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/trial.py` (140 lines → ~170 lines) — Add a
  `gnmda_ns: float` argument to `run_one_trial` and propagate it to `schedule_ei_onsets`. In
  `_apply_mode_weights`, replace `AMPA_ONLY` branch with `E_ONLY` (zero only GABA NetCons; AMPA and
  NMDA stay active). Add `nmda_netcon.weight[0] = 0.0` to the `GABA_ONLY` branch alongside the
  existing AMPA zeroing. In the post-run weight-restore block (lines 121-128), restore
  `nmda_netcon.weight[0] = gnmda_ns * 1e-3` in the `GABA_ONLY` arm. Add `gnmda_ns` to `TrialResult`
  so it can be propagated into the per-trial CSV row.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/run_tuning_curve.py` (390 lines → ~470 lines) —
  Wrap the existing dry-run + sweep loop in an outer `for gnmda_ns in NMDA_PEAK_NS_VALUES` loop. The
  per-mode CSVs gain a `gnmda_ns` column; rows for all four `gNMDA` values are appended to the same
  per-mode CSV (`tuning_curve_full.csv`, `tuning_curve_e_only.csv`, `tuning_curve_gaba_only.csv`)
  — the task description explicitly prefers this over per-`gNMDA` filename suffixes. The dry-run
  gate stays at `gnmda_ns = 0.0` to validate the zero-NMDA regression before doing real work.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/compute_metrics.py` (304 lines → ~360 lines) —
  Group the per-mode CSV by `gnmda_ns` to produce one variant per `(gnmda_ns, mode)` group. Add a
  `_compute_epsp_decay_to_1e_ms` function that reads the `E_ONLY` voltage trace at the preferred
  direction, locates the peak depolarisation, and finds the time at which the trace drops to
  `peak / e`. Drop the IPSP-conductance hard gate (it would still pass — t0054 keeps the same
  `gaba_mod` formula — but now lives inside the `gnmda = 0` mode-comparison validation rather than
  as the sole gate). Variant `id` is `f"gnmda_{gnmda:.2f}_{mode}"`.

* `tasks/t0052_minimal_dsgc_scalar_gaba/code/render_figures.py` (231 lines → ~390 lines) — Wrap
  the existing per-direction figure family in an outer `gnmda_ns` loop; the output filename becomes
  `f"{prefix}_gnmda_{gnmda:.2f}_dir_{angle_deg:03d}.png"`. Add three new top-level functions:
  `render_epsp_decay_vs_gnmda(out_path)` (line plot), `render_peak_hz_vs_gnmda` (line plot, one
  curve per direction), `render_dsi_vs_gnmda` (line plot of primary DSI and vector-sum DSI). Use
  `plot_polar_tuning_curve` from [t0011] for the per-`gNMDA` overview.

## Lessons Learned

* **Hard gates on conductance ratios catch bugs invisible to firing-rate gates** — [t0052]'s
  `compute_metrics.py:193-205` hard-fails when `gabaMOD(180)/gabaMOD(0)` is outside `[2.7, 3.3]`
  even though the firing rate is fine; this caught a sign-flip bug in pre-merge testing. t0054
  should keep this gate inside the `gnmda = 0` validation block.

* **Voltage-independent NMDA flattens but does not collapse DSI** — [t0048] reported that
  `Voff_bipNMDA = 1` (voltage-independent NMDA on the deposited cell) reduces the DSI vs gNMDA range
  from 0.174 to 0.066 but never reaches the paper's flat ~0.30 line. t0054's prediction: primary DSI
  will trend *downward* with `gNMDA` (more excitation overcoming the scalar GABA shunt), but more
  slowly than t0052's 1.0 → 0 transition because the slow NMDA decay sustains excitation across
  the IPSP window.

* **Driving-force saturation matters at 100-synapse density** — [t0052]'s IPSP voltage ratio
  (1.54) is much smaller than its conductance ratio (3.0) because local Vm approaches E_GABA when 99
  GABA synapses fire near-synchronously. t0054 should expect the same effect on the EPSP side as
  `gNMDA` rises: aggregate EPSP peak amplitude should *not* scale linearly with `gNMDA` because
  local Vm approaches `E_NMDA = 0 mV`.

* **CVODE atol = 1e-3 is the working-point** — [t0052]/[t0053]'s
  `neuron_bootstrap.py:enable_cvode(atol=1e-3)` gives ~3 s/trial. Tighter tolerances do not
  measurably change DSI but increase wall-clock substantially. Keep the t0052 setting.

* **t0048 cautionary note on NMDA flattening regimes** — DSI in [t0048] never went above 0.10 even
  at the highest `gNMDA = 3 nS` because absolute peak rates stayed in the noise. With t0052's 0.667
  Hz baseline (1 spike per 1500 ms trial), t0054 must watch for the regime where NMDA pushes the
  cell into multi-spike trains; multiple spikes per trial change DSI denominator scaling.

## Recommendations for This Task

1. **Adopt the [t0053] code-copy pattern verbatim**. Copy [t0052]'s `__init__.py`, `swc_io.py`,
   `cell.py`, `placement.py`, `neuron_bootstrap.py`, `metrics_extra.py`, `test_quiescent_rest.py`,
   `test_gaba_mod.py` with import-path rewrite and sentinel rename only. Copy [t0053]'s
   `test_placement_seed0_match.py` with the same path rewrite and add `T0052_PLACEMENT_JSON` to
   t0054's `paths.py`.

2. **Co-locate NMDA on the same `seg` and drive it from the *same* AMPA `NetStim`**. The task
   description is explicit: the NMDA NetCon is a second `h.NetCon(ampa_netstim, nmda_syn)`, no
   second NetStim. Setting `gnmda_ns = 0.0` simply zeroes the NMDA NetCon weight — the synapse is
   constructed but produces no current, which is the cleanest way to satisfy the
   `gnmda = 0 == t0052` regression gate without conditional construction logic.

3. **Use `Exp2Syn` for NMDA, not a MOD file**. The task specifies voltage-independent NMDA, which
   `Exp2Syn` (`tau1=5 ms` rise, `tau2=80 ms` decay, `e=0 mV`) implements without any MOD compilation
   step. Avoid the [t0046] / [t0048] `bipolarNMDA.mod` route entirely — it brings in `nrnivmodl`,
   custom HOC bootstrap, and Mg-block voltage dependence the spec excludes.

4. **Replace `AMPA_ONLY` with `E_ONLY` in the `TrialMode` enum**. Do not keep `AMPA_ONLY` as a
   legacy alias; the task explicitly designs the sweep so `E_ONLY` carries both AMPA and NMDA.
   Per-mode CSV filenames change from `*_ampa_only*` to `*_e_only*` (path constants only).

5. **Append all four `gNMDA` rows to a single per-mode CSV**. Add a `gnmda_ns` column so that
   downstream analysis can group by `(gnmda_ns, mode)` instead of opening four files. Three per-mode
   CSVs total, each with 4 × 12 × 10 = 480 rows.

6. **Hard-fail on the `gnmda = 0` regression gate**. After the sweep, re-load
   `tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv` and assert that the
   `gnmda_ns = 0.0` rows of t0054's `tuning_curve_full.csv` match within `1e-6 Hz`. Failure means
   either NMDA is not inert at zero conductance, NetCon weight reuse is leaking state between
   trials, or the placement seed drifted.

7. **Compute `epsp_decay_to_1e_ms` only for the preferred-direction `E_ONLY` trace**. Per the task
   description, this is *the* sweep-summary observable. Implementation: per `gNMDA`, average the 10
   preferred-direction `E_ONLY` voltage traces; find the peak depolarisation; find the first
   post-peak sample where `(v - v_init) <= peak_dep / math.e`; report `t_decay - t_peak`.

8. **Render three sweep-summary plots in addition to the per-`gNMDA` panels**. With only 4 `gNMDA`
   values, line plots are appropriate (no need for heatmaps). Use the [t0011] palette for
   cross-direction colour coding.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Original port of the deposited Poleg-Polsky cell with `bipolarNMDA.mod`. Used here
  as a negative example: t0054 deliberately avoids this code path.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library
* **Status**: completed
* **Relevance**: Provides `plot_polar_tuning_curve` and `plot_cartesian_tuning_curve`, imported into
  t0054 `render_figures.py` for the per-`gNMDA` overview plots.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Provides `load_tuning_curve`, `compute_dsi`, `compute_peak_hz`, `compute_null_hz`,
  `compute_hwhm_deg`, `compute_reliability`, `TuningCurve`. Imported into t0054 `compute_metrics.py`
  for all four registered metric keys per variant.

### [t0018]

* **Task ID**: `t0018_literature_survey_synaptic_integration`
* **Name**: Synaptic integration priors for DSGC modelling
* **Status**: completed
* **Relevance**: Literature support for the NMDA decay tau range (50-200 ms) chosen for the t0054
  `Exp2Syn` parameterisation.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347)
* **Status**: completed
* **Relevance**: Provides the `bipolarNMDA.mod` file used by [t0048] as the voltage-independent NMDA
  reference. t0054 confirms NMDA tau values are physiologically plausible without reusing the MOD
  file.

### [t0048]

* **Task ID**: `t0048_voff_nmda1_dsi_test`
* **Name**: Test Voff_bipNMDA = 1 (voltage-independent NMDA)
* **Status**: completed
* **Relevance**: The closest prior result for "voltage-independent NMDA on a DSGC". Establishes
  expectations for how DSI vs gNMDA should behave in t0054 (flatten but not collapse).

### [t0052]

* **Task ID**: `t0052_minimal_dsgc_scalar_gaba`
* **Name**: Minimal from-scratch DSGC with scalar gabaMOD inhibition
* **Status**: completed
* **Relevance**: Direct parent task; 12 of t0054's modules are copied verbatim from here, and five
  more are extended. The reference for the `gNMDA = 0` regression gate.

### [t0053]

* **Task ID**: `t0053_minimal_dsgc_spatial_gaba`
* **Name**: Minimal from-scratch DSGC with spatial PD/ND-asymmetric inhibition
* **Status**: completed
* **Relevance**: Sibling extension of [t0052] demonstrating the canonical code-copy pattern;
  `test_placement_seed0_match.py` is copied verbatim into t0054.
