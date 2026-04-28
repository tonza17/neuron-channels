---
spec_version: "1"
task_id: "t0055_nmda_mg_block_dsi_recovery"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 9
libraries_found: 10
libraries_relevant: 4
date_completed: "2026-04-28"
status: "complete"
---
# Code Research: Add Mg-Block NMDA to Recover DSI in t0054 Minimal Architecture

## Task Objective

This task forks the t0054 minimal DSGC codebase and replaces its voltage-independent NMDA `Exp2Syn`
with a custom `NMDA_MgBlock` point process implementing the Jahr-Stevens Boltzmann Mg block. Every
other parameter — morphology, AMPA, GABA, HH soma+AIS, placement seed, stimulus protocol — is
bit-identical to t0054. The task re-runs the same `gNMDA = {0, 0.25, 0.5, 1.0} nS` sweep and tests
whether Mg block restores the vector-sum DSI (target: > 0.50 at gNMDA = 0.25 nS, FULL mode, with
peak Hz >= 5 Hz). The primary engineering challenge is introducing the first custom MOD compilation
step into the minimal-architecture lineage (t0052 -> t0053 -> t0054 used only NEURON built-ins;
t0055 adds `nrnivmodl` to the bootstrap).

## Library Landscape

The aggregator scripts for libraries do not yet exist in this worktree
(`arf/scripts/aggregators/aggregate_libraries.py` is absent), so the survey below was assembled by
walking `tasks/*/assets/library/*/details.json` directly.

Ten libraries exist project-wide. Four are relevant to t0055.

| Library ID | Created by | Relevance |
| --- | --- | --- |
| `tuning_curve_loss` | t0012 | RELEVANT — `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`, `load_tuning_curve`, `TuningCurve`, used by `compute_metrics.py`. |
| `tuning_curve_viz` | t0011 | RELEVANT — `plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`, used by `render_figures.py`. |
| `minimal_dsgc_ampa_nmda_scalar_gaba` | t0054 | RELEVANT (as REFERENCE) — the immediate parent codebase being forked. Cannot be imported (cross-task `code/` imports forbidden by the project rule); the 13 modules described in `details.json` will be COPIED into t0055's `code/` with the standard import-path rewrite. |
| `modeldb_189347_dsgc_exact` | t0046 | RELEVANT (as PROVENANCE) — its `sources/bipolarNMDA.mod` is the source of the Mg-block formula and parameter values. The whole library is HOC-driven and cannot be imported; only the formula/parameters from one MOD file are reused, and a new bespoke MOD file is written for t0055. |
| `modeldb_189347_dsgc` | t0008 | NOT relevant — superseded by `modeldb_189347_dsgc_exact` for any audit; t0055 does not need the t0008 driver. |
| `modeldb_189347_dsgc_gabamod` | t0020 | NOT relevant — sibling port using a different protocol; not needed for the t0055 minimal-architecture extension. |
| `modeldb_189347_dsgc_dendritic` | t0022 | NOT relevant — driver for a different model substrate. |
| `de_rosenroll_2026_dsgc` | t0024 | NOT relevant — different DSGC port. |
| `minimal_dsgc_scalar_gaba` | t0052 | NOT relevant directly — t0054 already supersedes it; placement-match comparison is done against t0054's placement_seed0.json instead. |
| `minimal_dsgc_spatial_gaba` | t0053 | NOT relevant — sibling spatial-gating variant; out of scope per the t0055 task description. |

For the two libraries that t0055 will import-via-library:

* `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`
* `tasks.t0011_response_visualization_library.code.tuning_curve_viz`

These imports are inherited from t0054 verbatim; no API surface changes.

## Key Findings

### Fork pattern: copy t0054 verbatim with single-line import-path rewrite

The minimal-DSGC lineage [t0052] -> [t0053] -> [t0054] consistently uses the verbatim-copy pattern
where every Python module is duplicated into the next task's `code/` folder with a global
search-and-replace from `tasks.tNNNN_oldslug.code.*` to `tasks.tMMMM_newslug.code.*`. The [t0054]
plan documents this for 10 modules from [t0052] plus `test_placement_seed0_match.py` from [t0053].
t0055 inherits the same pattern: 13 modules will be copied verbatim from
`C:/Users/md1avn/Documents/GitHub/neuron-channels-worktrees/t0055_nmda_mg_block_dsi_recovery/tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/`
with the global rewrite `tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code` ->
`tasks.t0055_nmda_mg_block_dsi_recovery.code`. Each file currently imports only from its own task
plus the t0011 / t0012 libraries; no other cross-task imports exist (verified by
`grep -rn "from tasks.t00"` over the t0054 code/).

### NEURON bootstrap currently has no MOD compilation in the minimal-architecture lineage

The t0054 `neuron_bootstrap.py` (82 lines) only handles three Windows-specific concerns: (i) re-exec
to set `NEURONHOME` before C-level NEURON imports, (ii) inserting `<NEURONHOME>/lib/python` into
`sys.path`, (iii) `os.add_dll_directory(<NEURONHOME>/bin)`. There is no `h.nrn_load_dll`, no
`nrnivmodl` invocation, and no MOD-file scaffolding. [t0052], [t0053], and [t0054] all use NEURON
built-ins (`Exp2Syn`, `NetStim`, `NetCon`, `hh`) exclusively, so no custom DLL has been needed.
t0055 is the first task in this lineage to require `nrnivmodl`, which means `neuron_bootstrap.py`
must be EXTENDED (not just re-imported) and a `code/mod/` subfolder plus a build script must be
introduced. The reference pattern lives in [t0046].

### t0046 establishes the MOD compilation pattern reused by t0055

[t0046]'s `code/run_nrnivmodl.cmd` is a 13-line .cmd shim that pushd's into `code/sources/`, calls
`C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat .`, and pops back. The build is idempotent (safe to
re-run) because `nrnivmodl` handles incremental rebuilds. The DLL is loaded at NEURON startup via
`h.nrn_load_dll(str(NRNMECH_DLL))` in
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/build_cell.py:76`, gated by a
`NRNMECH_DLL.exists()` check in `_nrnmech_dll_path()`. [t0046] keeps two copies of every MOD: the
canonical copy under `assets/library/modeldb_189347_dsgc_exact/sources/`, and a working copy under
`code/sources/` that nrnivmodl writes the compiled DLL into. t0055 should follow the same
two-location approach: `tasks/t0055_*/assets/library/minimal_dsgc_mg_block_nmda/sources/` for the
canonical artefact, and `tasks/t0055_*/code/mod/` for the build directory (with the dll output).

### Jahr-Stevens Mg-block formula provenance and parameter values

The exact formula and parameter values come from
`tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod`
(the [t0046]-deposited verbatim copy of ModelDB 189347 commit
`87d669dcef18e9966e29c88520ede78bc16d36ff`).

Lines 47-54 of `bipolarNMDA.mod`:

```
n=0.25         (/mM)        :NMDA VOLTAGE DEPENDENCE
gama=0.08      (/mV)        :NMDA VOLTAGE DEPENDENCE
e = 0          (mV)         :REVERSAL POTENTIAL
...
Voff=0                      :0 - voltage dependent 1- voltage independent
Vset=-60                    :set voltage when voltage independent
```

Lines 108-109 are the actual gating expression (the BREAKPOINT block):

```
local_v = v*(1-Voff) + Vset*Voff       :VOLTAGE DEPENDENCE
gNMDA   = (A-B) / (1 + n * exp(-gama * local_v))
```

Where `A` and `B` are dual-exponential gating states (`A' = -A/tau1NMDA`, `B' = -B/tau2NMDA`) so
`A - B` is the standard Exp2Syn waveform. `[Mg2+]` is folded into `n`. With `Voff = 0` the gating is
fully voltage-dependent (Mg block on); with `Voff = 1` the gating is voltage-independent and clamps
`local_v` to `Vset = -60 mV` (Mg block off, used by [t0048] for the H1/H2 DSI flatness test).

The new `NMDA_MgBlock.mod` strips the t0046 bundling (presynaptic vesicle release, AMPA block,
calcium fraction) and keeps only the NMDA Mg-block point process with Exp2Syn-style NetStim drive.
Constants:

| Constant | Value | Units |
| --- | --- | --- |
| `n` | 0.25 | /mM (Mg2+ folded in) |
| `gama` | 0.08 | /mV |
| `Voff` | 0 | dimensionless (0 = voltage-dependent) |
| `Vset` | -60 | mV (used only when Voff = 1) |
| `tau1` | 5 | ms (rise — same as t0054) |
| `tau2` | 80 | ms (decay — same as t0054) |
| `e` | 0 | mV |

[t0046]'s line 109 expression `(A-B)/(1+n*exp(-gama*local_v))` divided by the NMDA dual-exponential
profile is the canonical Jahr-Stevens form. With `n = 0.25` and `gama = 0.08`, the Boltzmann factor
`1/(1 + 0.25 * exp(-0.08 * v))` is ~0.20 at `v = -80 mV` (heavy block), ~0.45 at `v = -40 mV`, ~0.83
at `v = 0 mV`, and ~0.95 at `v = +20 mV`. The expected single-synapse sanity test pattern (peak
gNMDA at -80 mV ~5x smaller than at -20 mV) is consistent with this curve.

### t0048 already validated the converse (Voff=1 -> partial DSI flatness)

[t0048] re-ran the t0046 gNMDA sweep at `Voff_bipNMDA = 1` (voltage-INDEPENDENT NMDA — the
deposited 0 Mg2+ condition) on the [t0046] DSGC substrate. The H1 verdict failed (slope -0.024/nS,
above the 0.02/nS cutoff), but the range collapse was real: DSI swept from 0.174 (Voff=0 baseline)
to 0.066 (Voff=1) over `gNMDA in [0, 3] nS`. This is direct evidence that NMDA voltage dependence is
*part* of the answer to DSI maintenance under varying gNMDA, but on the [t0046] substrate it does
not by itself recover paper-level DSI. t0055 tests the inverse hypothesis on a *different substrate*
— the from-scratch minimal architecture — where t0054 collapsed DSI from 0.746 to 0.082 by
adding voltage-INDEPENDENT NMDA. Symmetry expectation: re-introducing voltage dependence on the
minimal architecture should recover most of the lost DSI.

### t0054 places NMDA via a second NetCon on the SAME shared NetStim, not a second NetStim

t0054's `synapses.py` lines 92-171 build one `Exp2Syn` per synapse for AMPA and a SECOND `Exp2Syn`
for NMDA on the SAME `seg(location.section_x)`. Both are driven by the SAME single `ampa_netstim`
via two separate NetCons (`ampa_netcon` and `nmda_netcon`). This guarantees AMPA and NMDA fire at
byte-identical times. t0055 keeps this pattern verbatim: just substitute `h.NMDA_MgBlock(seg)` for
the NMDA `Exp2Syn(seg)` and keep the second-NetCon-on-the-same-NetStim wiring. The NMDA NetCon
weight is set per-trial by `schedule_ei_onsets` to `gnmda_ns * 1e-3` (microsiemens). With
`gnmda_ns = 0` the Mg-block factor multiplies a zero conductance, so the result must be
bit-identical to t0054 at gNMDA=0 (which itself was bit-identical to t0052).

### Validation gate inheritance: 4 gates carry over from t0054 with one new addition

t0054 has three numeric gates wired into `compute_metrics.py` and `test_*.py`:

1. Quiescent rest gate: `V_rest = -65 +/- 0.5 mV` after a 200 ms continuerun with no synapses
   (`test_quiescent_rest.py:31` — `QUIESCENT_DURATION_MS = 200.0`, `V_REST_TOLERANCE_MV = 0.5`).
2. Placement bit-identical gate: t0054's `test_placement_seed0_match.py` compares against t0052's
   `placement_seed0.json` at `POSITION_TOLERANCE = 1e-9`.
3. gNMDA = 0 cross-task regression gate inside `compute_metrics.py`:
   `GNMDA0_REGRESSION_TOL_HZ = 1e-6` (line 79). t0054 enforces this against t0052's
   `tuning_curve_full.csv`.

t0055 inherits all three with two updates:

* The placement-match reference points to **t0054's** `placement_seed0.json` instead of t0052's. The
  constant in `paths.py` becomes `T0054_PLACEMENT_JSON` and the `T0052_PLACEMENT_JSON` import is
  dropped from `test_placement_seed0_match.py`. Per the task description the per-synapse coordinates
  must match t0054's exactly.
* The gNMDA = 0 regression points to **t0054's** `tuning_curve_full.csv` instead of t0052's.

A NEW gate is added: NMDA voltage-dependence sanity test (single NMDA_MgBlock under SEClamp at
`v in {-80, -60, -40, -20, 0, +20} mV`, drive a single NetCon event, record peak gNMDA, assert the
curve is monotonic and that peak gNMDA at -80 mV is ~5x smaller than at -20 mV). This is
implementable as a new `code/test_nmda_mg_block_voltage_dep.py` (no clear analogue in [t0054] or
[t0046], so it is a fresh test).

### CVODE acceleration is critical for wall-clock budget

t0054's `enable_cvode` (lines 70-82 of `neuron_bootstrap.py`) sets `atol = 1e-3` and reduces
per-trial wall-clock from ~75 s (fixed-step) to ~3-8 s. The 1440-trial sweep took 4 h 19 min in
t0054 (per `results_summary.md`). t0055 inherits this verbatim. The plan budget of ~75 minutes is
optimistic given t0054's actual run; if wall-clock exceeds 4 hours the task description says abort
and create a parallelisation task.

## Reusable Code and Assets

The vast majority of t0055's Python is a verbatim copy from t0054 with import-path rewrite. The
custom MOD file and the bootstrap extension are the only new code.

### Modules to COPY INTO TASK from t0054 (verbatim with import-path rewrite)

All paths below are absolute under
`C:/Users/md1avn/Documents/GitHub/neuron-channels-worktrees/t0055_nmda_mg_block_dsi_recovery/tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/`.
Reuse method: **copy into task** (cross-task `code/` imports are forbidden by project rule). Single
search-and-replace per file: `tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code` ->
`tasks.t0055_nmda_mg_block_dsi_recovery.code`. Bootstrap sentinel `_T0054_NEURONHOME_BOOTSTRAPPED`
-> `_T0055_NEURONHOME_BOOTSTRAPPED`.

| File | Lines | Purpose | Adaptation |
| --- | --- | --- | --- |
| `__init__.py` | 0 | Package marker | None |
| `swc_io.py` | 180 | Stdlib SWC reader | Import-path rewrite only |
| `cell.py` | 218 | Cell builder (`build_dsgc_from_swc`, `summarize_cell`, `CellHandles`) | Import-path rewrite only |
| `placement.py` | 90 | `Location` dataclass, `sample_dendritic_locations`, `save_placement_json` | Import-path rewrite only |
| `paths.py` | 99 | All file path constants | Rewrite TASK_ID, LIBRARY_ID; replace `T0052_PLACEMENT_JSON`/`T0052_TUNING_CURVE_FULL_CSV` with `T0054_*`; add `NMDA_MOD_DIR`, `NRNMECH_DLL`, `RUN_NRNIVMODL_CMD` |
| `metrics_extra.py` | 44 | `compute_vector_sum_dsi`, `compute_preferred_direction_deg` | None (only depends on t0012 library) |
| `test_quiescent_rest.py` | 104 | V_rest gate | Import-path rewrite only |
| `test_gaba_mod.py` | 22 | gabaMOD scalar tests | Import-path rewrite only |
| `test_placement_seed0_match.py` | 78 | Placement-match gate | Rewrite imports; rebind reference to `T0054_PLACEMENT_JSON` |
| `compute_metrics.py` | 445 | 12-variant metrics + IPSP gate + regression gate | Rewrite imports; rebind regression reference to `T0054_TUNING_CURVE_FULL_CSV` |
| `render_figures.py` | 391 | Per-direction PNGs + 11 sweep-summary plots | Import-path rewrite; add Mg-block g(v) sanity-curve plot in addition to t0054's three sweep-summary plots |
| `run_tuning_curve.py` | 484 | Outer-loop sweep driver, FULL/E_ONLY/GABA_ONLY modes | Import-path rewrite; add `nrnivmodl` build step + DLL load before NEURON-touch |

Total verbatim copy: ~2,155 lines.

### Modules to COPY INTO TASK with material modification

| File | Source | New count est. | Modification |
| --- | --- | --- | --- |
| `constants.py` | `t0054/code/constants.py` (138 lines) | ~145 lines | Rewrite `NEURONHOME_SENTINEL_ENV` to `_T0055_NEURONHOME_BOOTSTRAPPED`. Add `MG_BLOCK_N: float = 0.25`, `MG_BLOCK_GAMMA: float = 0.08`, `MG_BLOCK_VOFF: float = 0.0`, `MG_BLOCK_VSET_MV: float = -60.0`. Documentation comment block referencing bipolarNMDA.mod lines 47-54 / 108-109. |
| `synapses.py` | `t0054/code/synapses.py` (222 lines) | ~225 lines | Replace `nmda_syn: Any = h.Exp2Syn(seg)` with `nmda_syn: Any = h.NMDA_MgBlock(seg)`. Set `nmda_syn.tau1`, `tau2`, `e` from existing constants; add `nmda_syn.n = MG_BLOCK_N`, `nmda_syn.gama = MG_BLOCK_GAMMA`, `nmda_syn.Voff = MG_BLOCK_VOFF`, `nmda_syn.Vset = MG_BLOCK_VSET_MV`. Everything else (NetCon wiring, `gaba_mod`, `_onset_time_ms`, `schedule_ei_onsets`) is unchanged. |
| `neuron_bootstrap.py` | `t0054/code/neuron_bootstrap.py` (82 lines) | ~115 lines | Add a new `ensure_nmda_mg_block_compiled()` function that (i) checks if `NRNMECH_DLL.exists()`, (ii) if not, runs `RUN_NRNIVMODL_CMD` via `subprocess.run` (idempotent), (iii) calls `h.nrn_load_dll(str(NRNMECH_DLL))` after `ensure_neuron_importable` and BEFORE `load_stdrun`. Add new constant import `NRNMECH_DLL`, `RUN_NRNIVMODL_CMD` from paths. Sentinel rename. |
| `trial.py` | `t0054/code/trial.py` (161 lines) | 161 lines (no logic change) | Import-path rewrite only. The trial-mode weight-restore block already uses `nmda_netcon.weight[0]`, which works the same with `NMDA_MgBlock` because the dual-exponential gating fires from NetCon events identically to `Exp2Syn`. |

### New files

| File | Lines (est.) | Purpose |
| --- | --- | --- |
| `code/mod/NMDA_MgBlock.mod` | ~80 | Custom POINT_PROCESS with `tau1`, `tau2`, `e`, `n`, `gama`, `Voff`, `Vset`, NetCon-driven dual-exponential gating multiplied by `1/(1+n*exp(-gama*local_v))`. Provenance header citing `bipolarNMDA.mod` lines 47-54 (parameters) and 108-109 (BREAKPOINT). |
| `code/run_nrnivmodl.cmd` | ~13 | .cmd build shim mirroring `t0046/code/run_nrnivmodl.cmd`, but pointing at `code/mod/` instead of `code/sources/`. |
| `code/test_nmda_mg_block_voltage_dep.py` | ~80 | NEW gate. Single `NMDA_MgBlock` under SEClamp at `v in {-80, -60, -40, -20, 0, +20} mV`; drive one NetCon event at t = 100 ms; record peak gNMDA. Assert monotonic increase with depolarisation; assert peak(-80 mV) <= 0.25 * peak(-20 mV). |

### Library imports (cross-task — IMPORT VIA LIBRARY)

These two imports are inherited verbatim from t0054.

| Import | Module | Used by |
| --- | --- | --- |
| `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_cartesian_tuning_curve, plot_polar_tuning_curve` | `tuning_curve_viz` library | `render_figures.py` |
| `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import TuningCurve, compute_dsi, compute_hwhm_deg, compute_null_hz, compute_peak_hz, compute_reliability, load_tuning_curve` | `tuning_curve_loss` library | `compute_metrics.py`, `metrics_extra.py` |

### Dataset asset (cross-task reference — copy by Path constant, not import)

| Asset | Path | Used by |
| --- | --- | --- |
| `dsgc-baseline-morphology-calibrated` | `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc` | `paths.MORPHOLOGY_SWC_PATH` (referenced verbatim from t0054) |
| t0054 placement reference | `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/placement_seed0.json` | `test_placement_seed0_match.py` |
| t0054 tuning_curve regression reference | `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv` | `compute_metrics.py` regression gate |

### Reference MOD file

| Asset | Path | Reuse method |
| --- | --- | --- |
| `bipolarNMDA.mod` | `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod` | DO NOT copy. Extract only the formula (lines 108-109) and parameter values (lines 47-54) into the new `NMDA_MgBlock.mod`. The bipolarNMDA bundle includes presynaptic vesicle release, AMPA, and `ica` write that t0055 explicitly does not want. |

## Lessons Learned

### From t0054: scalar gabaMOD cannot maintain DSI under voltage-independent NMDA

t0054's headline finding (`results_summary.md`) is that adding voltage-independent NMDA collapses
vector-sum DSI from 0.746 (gNMDA=0) to 0.082 (gNMDA=0.25 nS) — a ~9x collapse — while peak Hz
RISES from 0.667 to 8.0 Hz. The interpretation in t0054's `results_summary.md` is that "scalar
`gabaMOD` inhibition is too weak to maintain direction selectivity once NMDA is active" once the
long-tail NMDA depolarisation (tau2 = 80 ms) keeps the cell above threshold across both PD and ND
trials. Mg block is the canonical fix: it suppresses NMDA conductance at hyperpolarised voltages and
unblocks it once AMPA has depolarised the cell, restoring multiplicative gain. t0055's pass
criterion (DSI > 0.50 at gNMDA = 0.25 nS) directly tests this hypothesis.

### From t0048: voltage-dependence is necessary but not sufficient on a different substrate

[t0048]'s answer asset confirmed that toggling `Voff_bipNMDA = 1` on the [t0046] DSGC substrate
flattened the DSI-vs-gNMDA range (0.174 -> 0.066) but did not produce a flat curve at the paper's
claimed 0.30. This is direct evidence that the relationship between NMDA voltage dependence and DSI
is substrate-specific — what works on the [t0046] code-pinned substrate may differ quantitatively
from the minimal-architecture substrate. t0055 must be evaluated on its own merits: "DSI > 0.50 at
gNMDA = 0.25 nS" is the only gate that matters.

### From t0054: EPSP decay-to-1/e metric is null when NMDA tau2 = 80 ms

t0054 reported `null` for `epsp_decay_to_1e_ms` across all four gNMDA values — the windowed E_ONLY
trace doesn't return below 1/e of peak within the 1500 ms trial because stacked NMDA keeps the cell
depolarised at trial end. t0055 will inherit this limitation (same NMDA tau2); the rendered
`epsp_decay_vs_gnmda.png` will show an empty/null y-axis. This is acceptable per the task
description (suggestion S-0054-03 covers an improved EPSP-decay metric).

### From t0046: nrnivmodl on Windows writes nrnmech.dll INTO the source dir

The `run_nrnivmodl.cmd` in [t0046] is structured around the Windows MinGW toolchain quirk that
`nrnivmodl.bat` outputs `nrnmech.dll` directly into the source directory (mknrndll style), NOT into
a `x86_64/` subdirectory as on Linux. The `paths.py` must reflect this:
`NRNMECH_DLL = MOD_DIR / "nrnmech.dll"`, not `MOD_DIR / "x86_64" / "nrnmech.dll"`. Same toolchain
applies to t0055.

### From t0054: per-trial seed formula does NOT depend on gnmda_ns

t0054's `run_tuning_curve.py` documents the per-trial seed as `1000 * angle_idx + trial_idx + 1`
with no `gnmda_ns` term. This is intentional: it guarantees that at `gnmda_ns = 0` the per-trial
NetStim event timings (and therefore the FULL-mode firing rates) are identical to [t0052]'s by
construction. The same property carries over to t0055: at `gnmda_ns = 0` the Mg-block factor
multiplies a zero conductance, yielding zero NMDA current at every voltage, so t0055's gnmda=0 rows
must be bit-identical to t0054's gnmda=0 rows (which were bit-identical to t0052's).

## Recommendations for This Task

1. **Treat t0054's `code/` as a known-good baseline; copy and rewrite mechanically.** The
   minimal-architecture lineage has used this pattern three times consecutively
   ([t0052]->[t0053]->[t0054]) without regressions. Do not refactor on the way in.
2. **Lift the MOD compilation pattern from [t0046] verbatim.** Place `NMDA_MgBlock.mod` in
   `code/mod/` (not `code/sources/`, to avoid implying it's a verbatim ModelDB copy), write a
   13-line `code/run_nrnivmodl.cmd` shim pointing at `code/mod/`, and load the resulting
   `nrnmech.dll` via `h.nrn_load_dll(str(NRNMECH_DLL))` inside an extended `neuron_bootstrap.py`
   step that runs BEFORE `load_stdrun()`.
3. **Write a minimal NMDA_MgBlock.mod with only the Mg-block + dual-exponential gating.** Strip
   bipolarNMDA's presynaptic vesicle release, AMPA bundling, calcium fraction, and unused stimulus
   parameters. Keep `tau1`/`tau2` (using t0054's 5/80 ms naming, not the bipolarNMDA tau1NMDA /
   tau2NMDA), `e`, `n = 0.25`, `gama = 0.08`, `Voff = 0`, `Vset = -60`. Drive via NET_RECEIVE so it
   works as a drop-in replacement for the t0054 NMDA `Exp2Syn`. Header comment must cite
   `bipolarNMDA.mod` lines 47-54 / 108-109 with the [t0046] library asset path for traceability.
4. **Keep the second-NetCon-on-the-same-NetStim wiring from t0054.** AMPA and NMDA must fire at
   byte-identical times; this is what makes the gnmda_ns=0 regression bit-identical to t0054.
5. **Add a single new validation gate: the NMDA voltage-dependence sanity test.** Single
   `NMDA_MgBlock` under `h.SEClamp`, six clamp voltages, single NetCon event, record peak gNMDA. Two
   assertions: (i) monotonic in voltage, (ii) peak(-80 mV) <= 0.25 * peak(-20 mV). Order this gate
   AFTER `nrnivmodl` build but BEFORE the full sweep so a misconfigured MOD fails fast.
6. **Inherit t0054's three existing gates with the reference rebound from t0052 to t0054.**
   `paths.T0052_*` becomes `paths.T0054_*` in `paths.py`, and the imports in
   `test_placement_seed0_match.py` and `compute_metrics.py` are updated accordingly.
7. **Plan ~75-260 min wall-clock; trigger the parallelisation fallback at 4 hours.** t0054 actually
   took 4 h 19 min for the same 1440-trial budget. CVODE with `atol = 1e-3` is already on; further
   speed-up requires a separate parallelisation task (S-0054-06).
8. **Register the library asset `tasks/t0055_*/assets/library/minimal_dsgc_mg_block_nmda/`.** Mirror
   t0054's `details.json` structure exactly, swapping the NMDA point-process entry-point description
   and adding the new `NMDA_MgBlock.mod` to a `sources/` subfolder (the canonical artefact). The
   library spec_version stays at "2".
9. **Build a Mg-block g(v) sanity figure as a sweep-summary PNG.** Plot the Boltzmann factor
   `1 / (1 + 0.25 * exp(-0.08 * v))` at `v in [-80, +20] mV` and the empirical peak gNMDA from the
   voltage-clamp gate on the same axes — if they agree to within numerical precision the MOD is
   correctly compiled.

## Task Index

### [t0009]

* **Task ID**: t0009_calibrate_dendritic_diameters
* **Name**: Calibrate dendritic diameters of DSGC morphology
* **Status**: completed (dependency)
* **Relevance**: Provides the `dsgc-baseline-morphology-calibrated` SWC asset that t0055 reuses
  verbatim via `paths.MORPHOLOGY_SWC_PATH`. No code is copied from t0009.

### [t0011]

* **Task ID**: t0011_response_visualization_library
* **Name**: Response visualization library
* **Status**: completed (dependency)
* **Relevance**: Source of the `tuning_curve_viz` library (`plot_cartesian_tuning_curve`,
  `plot_polar_tuning_curve`). t0055 imports these via library, inherited from t0054.

### [t0012]

* **Task ID**: t0012_tuning_curve_scoring_loss_library
* **Name**: Tuning curve scoring loss library
* **Status**: completed (dependency)
* **Relevance**: Source of the `tuning_curve_loss` library (`TuningCurve`, `compute_dsi`,
  `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`,
  `load_tuning_curve`). t0055 imports these via library, inherited from t0054.

### [t0046]

* **Task ID**: t0046_reproduce_poleg_polsky_2016_exact
* **Name**: Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347)
* **Status**: completed (dependency)
* **Relevance**: Provides the canonical Mg-block formula and parameter values via
  `assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod` lines 47-54 (parameters) and
  108-109 (BREAKPOINT). Also establishes the MOD compilation pattern (`run_nrnivmodl.cmd` +
  `h.nrn_load_dll`) that t0055 lifts.

### [t0048]

* **Task ID**: t0048_voff_nmda1_dsi_test
* **Name**: Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA flatness
* **Status**: completed
* **Relevance**: Direct prior work on the same hypothesis (NMDA voltage dependence affects DSI vs
  gNMDA shape). Verdict on the [t0046] substrate was H2 (partial flattening, not paper-level
  flatness). t0055 tests the inverse on the minimal-architecture substrate.

### [t0052]

* **Task ID**: t0052_minimal_dsgc_scalar_gaba
* **Name**: Minimal from-scratch DSGC with scalar gabaMOD inhibition
* **Status**: completed
* **Relevance**: Original from-scratch minimal DSGC that established the file layout
  (`constants.py`, `paths.py`, `cell.py`, `placement.py`, `synapses.py`, `trial.py`,
  `run_tuning_curve.py`, `compute_metrics.py`, `render_figures.py`, three test files). t0055
  inherits this layout via t0054.

### [t0053]

* **Task ID**: t0053_minimal_dsgc_spatial_gaba
* **Name**: Minimal from-scratch DSGC with spatial PD/ND-asymmetric inhibition
* **Status**: completed
* **Relevance**: Sibling of t0052 that introduced the placement-match validation gate
  (`test_placement_seed0_match.py`). t0055 inherits this test via t0054 with the reference rebound
  from t0052 to t0054.

### [t0054]

* **Task ID**: t0054_minimal_dsgc_ampa_nmda_scalar_gaba
* **Name**: Minimal DSGC with AMPA + NMDA (voltage-independent) excitation and scalar gabaMOD
* **Status**: completed (parent task)
* **Relevance**: The codebase being forked. Every Python module in t0055 starts as a verbatim copy
  of the equivalent t0054 module with import-path rewrite. t0054's `placement_seed0.json` and
  `tuning_curve_full.csv` are the regression references for two of t0055's validation gates. t0054's
  headline DSI collapse from 0.746 to 0.082 at gNMDA=0.25 nS is the failure case t0055 is engineered
  to reverse.

### [t0008]

* **Task ID**: t0008_port_modeldb_189347
* **Name**: Initial port of ModelDB 189347
* **Status**: completed
* **Relevance**: Reviewed and judged NOT relevant — superseded by [t0046] for any audit purpose.
  Cited here for provenance completeness because the bipolarNMDA.mod was first deposited in this
  task before being re-deposited in [t0046]'s exact-reproduction asset.
