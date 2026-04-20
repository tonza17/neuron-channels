---
spec_version: "2"
task_id: "t0020_port_modeldb_189347_gabamod"
date_completed: "2026-04-20"
status: "complete"
---
# Plan: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Objective

Build a new sibling library asset `modeldb_189347_dsgc_gabamod` that drives the same NEURON DSGC
cell as t0008's `modeldb_189347_dsgc` but uses the Poleg-Polsky & Diamond 2016 native
direction-selectivity protocol — swapping the inhibitory `gabaMOD` scalar between PD (0.33) and ND
(0.99) — instead of t0008's spatial-rotation proxy. Done means: a registered library asset under
`assets/library/modeldb_189347_dsgc_gabamod/`, a `data/tuning_curves.csv` with
`(condition, trial_seed, firing_rate_hz)` rows for 2 conditions × 20 trials, a
`results/score_report.json` evaluating the run against the literature envelope (DSI 0.70-0.85, peak
40-80 Hz), and a comparison table in `results/results_detailed.md` quantifying how the gabaMOD-swap
port differs from the rotation-proxy port on DSI/peak/null/HWHM.

## Task Requirement Checklist

Verbatim task request from `tasks/t0020_port_modeldb_189347_gabamod/task_description.md`:

> Reproduce the Poleg-Polsky & Diamond 2016 DSGC direction-selectivity result under the paper's
> native gabaMOD parameter-swap protocol. Produce a new sibling library asset (proposed id
> `modeldb_189347_dsgc_gabamod`) that shares the MOD files and `RGCmodel.hoc` skeleton with
> `modeldb_189347_dsgc` but replaces the per-angle BIP rotation in `run_one_trial` with a
> two-condition gabaMOD sweep: PD trials run `gabaMOD=0.33`, ND trials run `gabaMOD=0.99`, and the
> tuning-curve CSV columns become `(condition, trial_seed, firing_rate_hz)` instead of
> `(angle_deg, ...)`. Reuse the t0012 `tuning_curve_loss` scoring library with a two-point envelope
> gate (DSI via PD/ND ratio, peak from PD). Deliverables: (1) new library asset with gabaMOD-swap
> driver; (2) `tuning_curves.csv` under the new protocol; (3) `score_report.json` against the
> envelope; (4) a short comparison note in `results_detailed.md` quantifying how the gabaMOD-swap
> port differs from the rotation-proxy port on DSI/peak/null/HWHM.

* **REQ-1**: Register a new library asset
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/` with
  `details.json` and `description.md` mirroring the t0008 asset's spec_version 2 layout. Evidence:
  `verify_library_asset` passes with 0 errors.
* **REQ-2**: Reuse t0008's HOC/MOD files via the registered library path; do not vendor a second
  copy of the source HOC/MOD. Evidence: the new driver imports `build_dsgc` from
  `tasks.t0008_port_modeldb_189347.code.build_cell` and the new asset's `sources/` directory does
  not exist.
* **REQ-3**: Replace per-angle BIP rotation with a two-condition gabaMOD sweep — set `h.gabaMOD`
  to `0.33` for PD trials and `0.99` for ND trials. Evidence: per-trial assertion that
  `h.RGC.BIPsyn[i].locx == baseline[i].bip_locx_um` for all `i` survives the full run.
* **REQ-4**: Emit `data/tuning_curves.csv` with columns `(condition, trial_seed, firing_rate_hz)`
  and exactly `2 * n_trials_per_condition` rows. Evidence: CSV header check + row count = 40 for the
  canonical sweep.
* **REQ-5**: Score the run with a two-point envelope gate using
  `DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)` and `peak = mean_PD` against literature
  thresholds DSI in [0.70, 0.85] and peak in [40, 80] Hz; write `results/score_report.json`.
  Evidence: file exists with `protocol`, `dsi`, `peak_hz`, `gate`, `n_trials_per_condition` fields.
* **REQ-6**: Add a comparison table in `results/results_detailed.md` quoting the t0008
  rotation-proxy numbers verbatim from `tasks/t0008_port_modeldb_189347/results/results_summary.md`
  alongside the new gabaMOD-swap numbers, with `null` and `HWHM` marked `N/A` for the two-point
  protocol. Evidence: table present with rows DSI / Peak / Null / HWHM / Reliability.
* **REQ-7**: Produce a bar chart of mean firing rate by condition (PD vs ND, with per-trial scatter)
  in `results/images/` and embed it in `results_detailed.md`. Evidence: PNG file exists and is
  referenced by the markdown.
* **REQ-8**: Run the canonical 2 × 20 = 40-trial sweep on the local Windows workstation. Evidence:
  command logs from `run_with_logs.py` for the driver invocation.

## Approach

The work is a single implementation step plus a comparison note. The cell, mechanisms, parameters,
and HOC/MOD files are reused unchanged from t0008's library asset; only the per-trial driver
changes. From the research-code findings: t0008's `build_cell.py:apply_params()` already writes
`h.gabaMOD = GABA_MOD` (= 0.33) on every trial, which means the new driver can override `h.gabaMOD`
per condition simply by mutating the global between trials — no HOC patch is needed, contrary to
the Risks & Fallbacks concern from the task description. The HOC point processes read the global on
every `placeBIP()` call. The new driver imports `build_dsgc`, `read_synapse_coords`, `apply_params`,
and `get_cell_summary` from `tasks.t0008_port_modeldb_189347.code.build_cell` via the registered
library, and inlines the spike-counting tail of `run_one_trial` (vector recording, `finitialize` +
`continuerun`, threshold-crossing count) — explicitly omitting the
`rotate_synapse_coords_in_place()` / `reset_synapse_coords()` calls that the rotation-proxy port
wraps around the spike-counting body.

For scoring, the t0012 high-level `score()` entry point cannot be invoked because its loader's
`_validate_angle_grid` requires 12 angles on a 30-degree grid (research-code finding); the new
two-condition CSV has only 2 means. Instead the new scorer reads the CSV with `pandas.read_csv`
directly and computes `DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)` and `peak = mean_PD` inline
(5 lines, same formula t0012's `compute_dsi` uses internally). The envelope thresholds DSI in
[0.70, 0.85] and peak in [40, 80] Hz are taken from the unwidened literature values quoted in
Poleg-Polsky 2016, not from t0012's widened test-conformant envelope (DSI in [0.7, 0.9], peak in
[30, 80]) — t0012 widened its envelope only so the identity test
`score(target, target).passes_envelope is True` would hold on the canonical t0004 target.

**Alternative considered**: write a thin t0012-compatible adapter that fakes a 12-angle grid by
duplicating PD/ND firing rates across 6 angles each. Rejected because it would corrupt the HWHM/null
computations that the t0012 scorer otherwise produces — those metrics are inherently ill-defined
for a two-point protocol and should be reported as `N/A`, not as artifacts of a faked grid.
Computing DSI inline by formula is the honest path.

**Task type**: `code-reproduction` (already set in `task.json`). The task type's planning guideline
calls for explicit envelope thresholds, an upstream baseline number to compare against, and a
per-trial reproducibility check — all addressed by REQ-3, REQ-5, and REQ-6.

## Cost Estimation

* Local NEURON simulation on the Windows workstation t0008 used: **$0** (no remote compute, no paid
  API calls).
* No third-party API calls during implementation. Total: **$0**, well under the project budget.

## Step by Step

1. **Bootstrap the new library asset folder.** Create
   `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/` with an
   empty `code/.gitkeep`. Write the asset's `details.json` (spec_version 2, library_id
   `modeldb_189347_dsgc_gabamod`, version `0.1.0`, name "ModelDB 189347 DSGC Port — gabaMOD-swap
   protocol", description_path `description.md`, module_paths listing the new task code files,
   entry_points listing the driver and scorer, dependencies `["neuron", "pandas", "tqdm"]`,
   categories matching t0008's plus `dsi-protocol`, created_by_task
   `t0020_port_modeldb_189347_gabamod`). Write `description.md` (≥500 words) explaining the
   gabaMOD-swap protocol, the divergence from t0008's rotation proxy, the two-point CSV schema, and
   why HWHM/null are N/A. Satisfies **REQ-1**.

2. **Create `code/constants.py` and `code/paths.py`.** `constants.py` re-exports `TSTOP_MS`,
   `V_INIT_MV`, `AP_THRESHOLD_MV`, `GABA_MOD`, and other canonical values from
   `tasks.t0008_port_modeldb_189347.code.constants` and adds `GABA_MOD_PD = 0.33`,
   `GABA_MOD_ND = 0.99`, `N_TRIALS_PER_CONDITION = 20`, `DSI_ENVELOPE = (0.70, 0.85)`,
   `PEAK_ENVELOPE_HZ = (40.0, 80.0)`, and a `Condition` string enum-like namespace with `"PD"` and
   `"ND"`. `paths.py` defines `Path` constants `DATA_DIR = Path("data")`,
   `TUNING_CURVES_CSV = DATA_DIR / "tuning_curves.csv"`, `RESULTS_DIR = Path("results")`,
   `SCORE_REPORT_JSON = RESULTS_DIR / "score_report.json"`, and
   `IMAGES_DIR = RESULTS_DIR / "images"`. Satisfies **REQ-2**.

3. **Create `code/run_gabamod_sweep.py`.** Imports `build_dsgc`, `read_synapse_coords`,
   `apply_params`, `get_cell_summary` from `tasks.t0008_port_modeldb_189347.code.build_cell` via the
   registered library path (no copy). Defines
   `run_one_trial_gabamod(*, h, gabamod_value: float, seed: int, baseline_coords: list[SynapseCoords]) -> float`:
   calls `apply_params(h, seed=seed)`, sets `h.gabaMOD = gabamod_value`, asserts
   `h.RGC.BIPsyn[i].locx == baseline_coords[i].bip_locx_um` for all `i`, records the soma `vec` with
   `h.Vector().record(h.RGC.soma(0.5)._ref_v)`, runs `h.finitialize(h.v_init)` then
   `h.continuerun(h.tstop)`, counts threshold crossings with
   `numpy.diff(numpy.signbit(soma - AP_THRESHOLD_MV)).sum() // 2`, returns spike count divided by
   stimulus window in seconds. Defines `main()` that builds the cell once, reads baseline coords,
   loops over the 40 trial pairs `[("PD", seed), ("ND", seed)]` for
   `seed in range(N_TRIALS_PER_CONDITION)`, writes `data/tuning_curves.csv` with header
   `condition,trial_seed,firing_rate_hz`. Uses `argparse` with `--n-trials` (default 20) and
   `--limit` (default `None`) for validation. Wraps the trial loop in `tqdm`. Satisfies **REQ-3**
   and **REQ-4**.

4. **[CRITICAL] Run the validation gate first.** Execute
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0020_port_modeldb_189347_gabamod -- uv run python -m tasks.t0020_port_modeldb_189347_gabamod.code.run_gabamod_sweep --limit 2 --n-trials 1`.
   Expected output: 2 rows in `data/tuning_curves.csv` (one PD, one ND), PD firing rate clearly
   higher than ND firing rate (PD ~30-80 Hz, ND ~0-15 Hz) — these are sanity bounds, not envelope
   thresholds. **Failure condition**: if PD ≤ ND or both rates are 0, halt and inspect per-trial
   soma traces with `report_morphology.py`-style instrumentation before launching the full sweep.
   The trivial baseline is "two random spike trains have DSI ≈ 0"; if our run is at or below that,
   the gabaMOD swap did not take effect and the run is broken. Satisfies the validation-gate
   requirement for REQ-3.

5. **[CRITICAL] Run the full canonical sweep.** Execute
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0020_port_modeldb_189347_gabamod -- uv run python -m tasks.t0020_port_modeldb_189347_gabamod.code.run_gabamod_sweep --n-trials 20`.
   Expected wall-clock: ~1.5 minutes (40 trials × ~2 s/trial). Expected output: 40 rows in
   `data/tuning_curves.csv`. Satisfies **REQ-4** and **REQ-8**.

6. **Create `code/score_envelope.py`.** Reads `data/tuning_curves.csv` with `pandas.read_csv` using
   the explicit dtype map
   `{"condition": pd.StringDtype(), "trial_seed": pd.UInt32Dtype(), "firing_rate_hz": "float64"}`.
   Computes `mean_PD = df[df.condition == "PD"].firing_rate_hz.mean()`,
   `mean_ND = df[df.condition == "ND"].firing_rate_hz.mean()`,
   `dsi = (mean_PD - mean_ND) / (mean_PD + mean_ND)`, `peak_hz = mean_PD`. Builds a frozen dataclass
   `ScoreReport(protocol="gabamod_swap", dsi: float, peak_hz: float, gate: GateResult, n_trials_per_condition: int)`
   where `GateResult` holds `dsi_min, dsi_max, peak_min, peak_max, passed`. Writes
   `results/score_report.json` via `pydantic.BaseModel.model_dump_json(indent=2)`. Satisfies
   **REQ-5**.

7. **Run the scorer.** Execute
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0020_port_modeldb_189347_gabamod -- uv run python -m tasks.t0020_port_modeldb_189347_gabamod.code.score_envelope`.
   Expected output: file `results/score_report.json` exists with non-null `dsi` and `peak_hz` and a
   `gate.passed` boolean. Satisfies **REQ-5**.

8. **Generate the comparison chart.** Create `code/plot_pd_vs_nd.py` that reads
   `data/tuning_curves.csv`, builds a matplotlib bar chart with two bars (PD mean, ND mean), error
   bars (per-condition std), and a per-trial scatter overlay. Saves the PNG to
   `results/images/pd_vs_nd_firing_rate.png` at 200 DPI, 5×4 inches. Run via `run_with_logs`.
   Produces the chart asset that the orchestrator-managed `results` step will later reference;
   satisfies the chart-generation half of **REQ-7**. The narrative comparison table (**REQ-6**) and
   the chart embed (the embed half of **REQ-7**) are written by the orchestrator's `results` step
   and are out of scope for this implementation step.

## Remote Machines

None required. The full 40-trial sweep runs locally on the Windows workstation that t0008 used —
NEURON 8.2.7 + NetPyNE 1.1.1 are already installed.

## Assets Needed

* **Library asset `modeldb_189347_dsgc`** from `tasks/t0008_port_modeldb_189347` — provides
  `build_dsgc`, `apply_params`, `read_synapse_coords`, `get_cell_summary`, the canonical paper
  parameters, and the source HOC/MOD files in
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/`.
* **Library asset `tuning_curve_loss`** from `tasks/t0012_tuning_curve_scoring_loss_library` —
  imported only as a formula reference for `compute_dsi`; the high-level `score()` entry point
  cannot be used because its loader requires 12 angles.
* **Rotation-proxy results** in `tasks/t0008_port_modeldb_189347/results/results_summary.md` —
  quoted verbatim in the comparison table for DSI / Peak / Null / HWHM / Reliability values.

## Expected Assets

* **1 library asset** of type `library`, id `modeldb_189347_dsgc_gabamod`, registered at
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/`. Contains:
  `details.json` (spec_version 2), `description.md` (≥500 words explaining the gabaMOD-swap
  protocol, the divergence from t0008, the two-point CSV schema, and the unwidened literature
  envelope), and the `code/.gitkeep` placeholder. The driver and scorer source files live in the
  task's main `code/` directory and are referenced from `details.json` `module_paths`. Matches
  `task.json` `expected_assets: {"library": 1}`.

## Time Estimation

* Implementation (code + library asset metadata): ~30 minutes.
* Validation gate (2-trial run): ~10 seconds.
* Full sweep (40 trials): ~1.5 minutes.
* Scoring + chart generation: ~30 seconds.
* Results writing: ~15 minutes.
* **Total wall-clock**: ~50 minutes from prestep of `implementation` to commit of `reporting`.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `h.gabaMOD` global is shadowed by per-synapse parameter, mutation has no effect | Low | High — gate fails with DSI ≈ 0 | Research-code finding shows `apply_params` already writes `h.gabaMOD` on every trial; if the validation gate fails, set `inh_syn.gMOD` directly on each `h.RGC.SACinhibsyn[i]` instead |
| BIP `locx` rotation re-engages silently (e.g. via leftover state from a prior call) | Low | High — port silently regresses to rotation proxy | Per-trial assertion `h.RGC.BIPsyn[i].locx == baseline[i].bip_locx_um` for all `i`; halt + intervention if assertion fires |
| DSI inside envelope but PD spike rate unrealistically low (< 5 Hz) | Medium | Medium — passes gate but is biologically implausible | Record in Limitations section; recommend per-trial spike-count floor as a follow-up suggestion |
| t0008 module import path breaks if t0008 library asset gets renamed or relocated | Low | Medium — driver fails to import | Pin the library version `0.1.0` in `details.json` `dependencies` (informally — verificator does not enforce inter-task lib pins yet); if the import breaks, copy `build_cell.py` into the new task's `code/` and accept the duplication |
| Local NEURON `.dll` not loaded (compiled mech missing) | Medium | High — driver fails on `build_dsgc` | Run `nrnivmodl` on `assets/library/modeldb_189347_dsgc/sources/` if needed; t0008's |
| `run_nrnivmodl.cmd` is the canonical recipe |  |  |  |

## Verification Criteria

* **Library asset structurally valid**: run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0020_port_modeldb_189347_gabamod -- uv run python -m arf.scripts.verificators.verify_library_asset t0020_port_modeldb_189347_gabamod modeldb_189347_dsgc_gabamod`.
  Expected: 0 errors, 0 warnings. Confirms **REQ-1** and **REQ-2**.
* **CSV schema and row count**: `data/tuning_curves.csv` has header
  `condition,trial_seed,firing_rate_hz` and exactly 40 data rows (20 PD + 20 ND). Check via
  `wc -l data/tuning_curves.csv` (expect 41) and `head -1 data/tuning_curves.csv`. Confirms
  **REQ-4**.
* **Score report present and well-formed**: `results/score_report.json` exists, parses as JSON, has
  fields `protocol == "gabamod_swap"`, `dsi`, `peak_hz`, `gate.passed`,
  `n_trials_per_condition == 20`. Confirms **REQ-5**.
* **BIP positions unchanged**: `code/run_gabamod_sweep.py` per-trial assertion did not fire during
  the full sweep — check the run's `stdout.txt` log for the absence of `AssertionError`. Confirms
  **REQ-3**.
* **Comparison table present in results**: after the orchestrator's `results` step writes
  `results/results_detailed.md`, it must contain a markdown table with rows `DSI`, `Peak (Hz)`,
  `Null (Hz)`, `HWHM (deg)`, `Reliability` and columns `Rotation proxy (t0008)`,
  `gabaMOD swap (t0020)`, `Envelope`. The t0008 numbers must match
  `tasks/t0008_port_modeldb_189347/results/results_summary.md` exactly (no rounding). Confirms
  **REQ-6**.
* **Chart asset exists and is embedded**: `results/images/pd_vs_nd_firing_rate.png` exists after the
  implementation step (chart-generation half of REQ-7) and is referenced in
  `results/results_detailed.md` after the `results` step via a `![](images/...)` tag (embed half of
  REQ-7).
* **Sweep ran via wrapped CLI**: at least two log entries under `logs/commands/` reference
  `run_gabamod_sweep.py` (validation gate + full sweep). Confirms **REQ-8**.
