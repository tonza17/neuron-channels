---
spec_version: "3"
task_id: "t0022_modify_dsgc_channel_testbed"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-21T01:00:00Z"
completed_at: "2026-04-21T00:19:17Z"
---
## Summary

Executed the 13-step plan: built the channel-modular AIS partition HOC (5 `forsec` regions), wrote
the per-dendrite E-I driver on top of the ModelDB 189347 cell build, calibrated synaptic drive to
match the t0008 baseline, and ran the full 12-angle x 10-trial sweep. Emitted canonical
`curve_modeldb_189347_dendritic.csv` (120 rows), scored it with the t0012 `tuning_curve_loss` to
produce `results/metrics.json` (DSI = 1.0, peak = 15 Hz, HWHM = 116.25 deg, RMSE = 10.48), generated
the polar + Cartesian PNG chart, and authored the library description with the Nav1.1 correction and
the 5-region partition table. All acceptance gates for REQ-1 through REQ-6 pass; REQ-7 is deferred
to orchestrator post-implementation work as declared in the plan.

## Actions Taken

1. **Local NEURON setup (Steps 1-2).** Verified `NEURONHOME=C:\Users\md1avn\nrn-8.2.7`, built the
   ModelDB 189347 MOD library under `tasks/t0022_modify_dsgc_channel_testbed/build/modeldb_189347/`
   via `nrnivmodl`, and bootstrapped `h.load_file` with the resulting `nrnmech.dll`. Set the t0008
   `load_neuron._loaded = True` sentinel to bypass its upstream DLL lookup without importing from
   t0008's `code/`.
2. **Channel-modular AIS partition (Steps 3, 9).** Authored `code/dsgc_channel_partition.hoc`
   declaring five `SectionList` objects (`SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`,
   `AIS_DISTAL`, `THIN_AXON`) with one `forsec <region> { ... }` block each. The bundled morphology
   has no axon sections, so the three AIS / axon lists are empty in the baseline; downstream
   channel-swap tasks `append()` to them before inserting. Satisfies REQ-5.
3. **Per-dendrite E-I driver (Steps 4-7).** Wrote `code/run_tuning_curve.py`. For every section in
   `h.RGC.ON` the driver creates one AMPA `Exp2Syn` at seg 0.9 (distal) and one GABA_A `Exp2Syn` at
   seg 0.3 (proximal), each gated by a `NetStim` burst driver (`number=N_SYN_EVENTS=6`,
   `interval=SYN_EVENT_INTERVAL_MS=30`, `noise=0`). Upstream baseline synapses are silenced by
   zeroing `h.b2gampa`, `h.b2gnmada`, `h.s2ggaba`, and `h.s2gach` then re-running `h("update()")`
   and `h("placeBIP()")`. Satisfies REQ-1 and REQ-3.
4. **Direction-dependent scheduling (Step 7).** `schedule_ei_onsets` sets per-pair NetStim `start`
   times: inhibition leads excitation by `EI_OFFSET_NULL_MS = -10` in the null direction and lags by
   `EI_OFFSET_PREFERRED_MS = +10` in the preferred direction, computed from the dendrite angle vs
   bar direction. GABA conductance follows the Park 2014 ratio (`GABA_CONDUCTANCE_NULL_NS = 12`,
   `GABA_CONDUCTANCE_PREFERRED_NS = 3`). Satisfies REQ-1.
5. **Conductance calibration (Step 10 preflight gate).** Iterated `AMPA_CONDUCTANCE_NS` through
   preflight runs (4 angles x 2 trials, ~30 s each) to land the preferred-direction firing rate near
   the t0008 baseline (~15 Hz). Settled on `AMPA_CONDUCTANCE_NS = 6.0` giving ~14 Hz preferred vs 0
   Hz null, clearing the >=5 Hz preferred-direction gate and giving a clean sign for the DSI.
6. **Full 12-angle sweep (Step 11 [CRITICAL]).** Ran the default non-preflight path of
   `run_tuning_curve.py` (12 angles x 10 trials = 120 trials) wrapped with `run_with_logs.py`. Wall
   time 9 min 22 s. Emitted `data/tuning_curves/curve_modeldb_189347_dendritic.csv` with 120 rows
   and canonical schema `(angle_deg, trial_seed, firing_rate_hz)`. Satisfies REQ-2.
7. **Scoring (Step 12).** Ran `code/score_envelope.py` to apply the t0012 `tuning_curve_loss`
   scorer. Emitted `results/metrics.json` with all four registered keys:
   `direction_selectivity_index = 1.0`, `tuning_curve_hwhm_deg = 116.25`,
   `tuning_curve_reliability = 1.0`, `tuning_curve_rmse = 10.48`. Peak firing rate is 15 Hz at angle
   120 deg. DSI gate (>= 0.5) and peak gate (>= 10 Hz) both pass. Satisfies REQ-4 and REQ-6.
   `passes_envelope=False` is expected per plan - the task only requires DSI + peak gates, not a
   full envelope match against t0004.
8. **Chart generation.** Added `code/plot_tuning_curve.py` producing a polar + Cartesian PNG with
   per-angle mean and std error bars plus a 10 Hz peak-gate reference line. Output at
   `results/images/tuning_curve_dendritic.png`.
9. **Library description (Step 13 [CRITICAL]).** Authored
   `assets/library/modeldb_189347_dsgc_dendritic/description.md` (spec-v2) covering purpose, entry
   points, dependencies, constants table, outputs, the REQ-4 acceptance gate, and design decisions.
   Includes the mandatory **Channel-Modular Partition** section with a 5-row region table (region ->
   membership -> baseline -> channel-swap target -> default gbar -> literature source) and the
   **"Correction: Nav1.1 in the Proximal AIS (NOT Nav1.2)"** subsection citing VanWart 2006 and
   RGC-AIS-Review-2022. `details.json` (spec-v2) lists all seven `module_paths`, six entry points
   (three functions + three scripts), five dependencies, and four categories. Satisfies REQ-5
   (description side) and REQ-6 traceability.
10. **Quality checks.** Applied `flowmark` to `description.md`, ran `ruff check --fix`,
    `ruff format`, and `mypy .` on the whole tree - all clean (ruff: all checks passed, mypy:
    Success, no issues found in 240 source files).

## Outputs

* `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc` (5 SectionLists, 5
  `forsec` insertion blocks, empty AIS lists populated by downstream tasks)
* `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (per-dendrite E-I driver,
  NetStim burst mode, baseline-synapse silencing)
* `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py` (calibrated values:
  `AMPA_CONDUCTANCE_NS=6.0`, `N_SYN_EVENTS=6`, `SYN_EVENT_INTERVAL_MS=30.0`,
  `EI_OFFSET_PREFERRED_MS=10.0`, `EI_OFFSET_NULL_MS=-10.0`)
* `tasks/t0022_modify_dsgc_channel_testbed/code/score_envelope.py` (t0012 scorer wrapper)
* `tasks/t0022_modify_dsgc_channel_testbed/code/plot_tuning_curve.py` (polar + Cartesian plotter)
* `tasks/t0022_modify_dsgc_channel_testbed/data/tuning_curves/curve_modeldb_189347_dendritic.csv`
  (120 rows, schema `angle_deg,trial_seed,firing_rate_hz`)
* `tasks/t0022_modify_dsgc_channel_testbed/results/metrics.json` (DSI=1.0, peak=15 Hz, HWHM=116.25
  deg, RMSE=10.48)
* `tasks/t0022_modify_dsgc_channel_testbed/results/images/tuning_curve_dendritic.png`
* `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/details.json`
  (spec-v2, 7 module_paths, 6 entry_points, 5 deps, 4 categories)
* `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/description.md`
  (purpose, entry points, 5-region partition table, Nav1.1 correction, constants, outputs,
  acceptance gate, design decisions)

## Issues

1. **No framework verificator for library assets.** The plan's Step 9 references
   `verify_library_asset.py`, but `arf/scripts/verificators/` contains only 24 other `verify_*.py`
   scripts and no library-specific verificator. Verified structural correctness manually against
   `meta/asset_types/library/specification.md` instead: spec_version "2", `description_path` field
   declared, `module_paths` all existing, `dependencies` listed, `categories` all present in
   `meta/categories/`. This is a framework gap worth flagging in a follow-up suggestion.

2. **Baseline synapse silencing depends on mutating module globals on `h`.** The upstream
   RGCmodel.hoc installs `b2gampa`, `b2gnmada`, `s2ggaba`, `s2gach` as NEURON global conductances
   and provides an `update()` procedure that rebuilds the synapses from those globals. Setting them
   to 0 and re-running `update()` + `placeBIP()` is the documented reset path but is fragile against
   upstream HOC changes. Documented in `description.md` under "Design Decisions".

3. **Conductance calibration required ~6 iterations.** Initial AMPA conductance (0.3 nS, single
   event) gave 0 Hz everywhere after silencing the baseline synapses; scaling up produced saturation
   near the cell's Na/K-limited ceiling (~60 Hz) before landing at 14 Hz preferred with 6 nS + 6
   events at 30 ms spacing. Preflight (4x2 = 8 trials) was invaluable here; the full 120-trial sweep
   would have been wasted on any of the early conductance settings.

4. **passes_envelope=False is expected, not a failure.** The `score_envelope` output reports
   `passes_envelope=False` because the dendritic driver's tuning curve shape does not match the
   t0004 canonical envelope's exact values. This is acceptable per the plan (REQ-4 specifies DSI +
   peak gates only, not envelope shape match).
