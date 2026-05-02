---
spec_version: "2"
task_id: "t0076_bedb_dsi_firing_rate_mobo"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Multi-Objective Bayesian Optimisation of Channels + Synapses on Bed B

## Objective

Run a 25-parameter multi-objective Bayesian optimisation (BoTorch qNEHVI) on the Bed B (de Rosenroll
2026\) DSGC compartmental model in NEURON, jointly maximising direction selectivity index (DSI) and
preferred-direction (PD) firing rate. The cell morphology is fixed; the search space covers 12
voltage-gated channel densities, 3 passive parameters, 2 calcium dynamics parameters, 2 synapse
counts, 4 spatial-rule synapse-placement parameters, and 2 synapse weights. Each candidate cell is
evaluated by 8 directions × 20 seeds = 160 NEURON trials in parallel on a Vast.ai 64-core CPU node.
The optimiser produces a Pareto front of (DSI, firing rate) trade-offs with at least 5 distinct
configurations after 200 iterations and a monotonically increasing hypervolume metric. Done means a
Pareto-front PNG, a hypervolume-trajectory PNG, 3-5 representative-cell deep-dive figures, a Typst
PDF writeup, and `results/metrics.json` populated with the registered DSI metric for each Pareto
cell — produced under a hard $5.00 Vast.ai cap.

## Task Requirement Checklist

The operative task text from `task.json` `short_description` and `task_description.md`:

> Fix Bed B (de Rosenroll) morphology; optimise 25 free parameters (12 channel densities, 3 passive,
> 2 calcium, 2 synapse counts, 4 spatial-rule synapse placement params, 2 synapse weights) over the
> joint Pareto front of DSI and PD firing rate via BoTorch qNEHVI. ~300-500 iterations, 8 directions
> x 20 seeds per iteration.

The verbatim REQ list from `task_description.md` is preserved here so each line is bound to a step
in `## Step by Step`.

* **REQ-1** — 12 voltage-gated channel mechanisms vendored or implemented. Satisfied by Steps 2-3 (4
  new MODs: Kdr, HCN, CaL, CaT vendored from Hay 2011 + Mainen 1996; 5 SUFFIX-renamed copies of
  Nav1.6/NaP/NaR/Kv3/Kv4 from t0067; 3 SUFFIX-renamed copies of BK/SK/Kv7 from t0074; total 12;
  `cad` already provided by t0024). Evidence: `code/mods/` contains 12 `.mod` files plus the
  compiled `nrnmech.dll`/`libnrnmech.so` after `nrnivmodl`.
* **REQ-2** — Parametric synapse placer takes (N, ρ_0, λ) and produces a valid synapse placement
  with the requested density pattern. Satisfied by Step 4 (`code/parametric_placer.py`). Evidence:
  unit-style smoke test in Step 7 visualises 4 (ρ_0, λ) configurations; placement returns the
  requested N positions with empirical density ∝ exp(-d/λ).
* **REQ-3** — Trial driver runs 8 directions × 20 seeds for any 25-d parameter vector and returns
  (DSI, PD firing rate); handles NaN errors gracefully. Satisfied by Step 6 (`code/trial_driver.py`)
  using `ProcessPoolExecutor` over directions × seeds. Evidence: the Step 7 local smoke-test runs
  one full 160-trial evaluation in ≤300 s on a single workstation core (~3 s × 160 / parallelism)
  and returns finite (DSI, rate). NaN handling tested by injecting `gbar=0.5 S/cm²` extreme.
* **REQ-4** — BoTorch qNEHVI optimiser wired up and runs ≥ 300 iterations. Satisfied by Step 8
  (`code/mobo_loop.py`) with 30 Sobol DoE + ≤500 acquisition steps; remote run in setup-machines /
  implementation / teardown chain. Evidence: `data/trial_history.parquet` contains ≥ 330 rows.
* **REQ-5** — Pareto front + hypervolume trajectory plotted; saved to `results/images/`. Satisfied
  by Step 10 (`code/plot_pareto.py`). Evidence: `results/images/pareto_front.png` and
  `results/images/hypervolume_trajectory.png` exist after the remote run + teardown.
* **REQ-6** — At least 3 representative Pareto cells documented in detail (parameter values, tuning
  curves, spike traces). Satisfied by Step 10's deep-dive section (uses t0072's
  `_attach_bed_b_recorders` recorder). Evidence: `results/images/deepdive_cell_<i>_*.png` for
  i=1..5; `results/data/deepdive_cell_<i>.npz` per cell.
* **REQ-7** — `results/results_summary.md` + `results_detailed.md` (mandatory sections per the
  results spec) + Typst PDF. Owned by the orchestrator's results step (NOT in this plan's Step by
  Step), but the Typst PDF render script (`code/render_pdf.py`) is created in Step 11 so the
  orchestrator can call it. Evidence: `code/render_pdf.py` exists and runs successfully on a stub
  `results/results_detailed.typ`.
* **REQ-8** — All standard verificators pass. Owned by the orchestrator's reporting step. The plan
  ensures every produced asset matches the spec it claims to satisfy. Evidence: `verify_plan` and
  `verify_results` exit 0 in the reporting step.
* **REQ-9** — `pyproject.toml` updated with `botorch`, `gpytorch`, `torch` (and any related deps)
  cleanly. Satisfied by Step 1 (adds `botorch>=0.12 gpytorch>=1.13 torch>=2.4 pyarrow>=15.0` to
  `pyproject.toml` and runs `uv sync`). Evidence: `uv.lock` updated; `python -c "import botorch"`
  succeeds.
* **REQ-10** — A documented "next steps" suggestion: tier-stratify the channel densities of the best
  3 Pareto cells and re-optimise locally (extends the search to ~40 dim). Satisfied by the
  orchestrator's suggestions step (NOT in this plan's Step by Step), but the relevant data
  (best-Pareto cell parameters from `results/data/pareto_front.json`) is produced in Step 10 so the
  suggestions step has the input it needs. Evidence: orchestrator's `results/suggestions.json`
  contains a suggestion citing the best 3 Pareto-cell IDs.
* **REQ-11** — All compute (cell builds, NEURON sims, BoTorch acquisition steps) runs on the Vast.ai
  64-core node, NOT on the local workstation. The local workstation only orchestrates the SSH
  session, holds the task folder, and pulls results back during teardown. Owned by the
  orchestrator's setup-machines / implementation / teardown chain. The plan specifies the exact
  remote setup script and image; see `## Remote Machines` and `## Step by Step` Step 12.
* **REQ-12** — `results/costs.json` records the actual Vast.ai bill (≤ $5.00) and
  `results/remote_machines_used.json` records the instance ID, GPU/CPU specs (no GPU expected),
  hourly rate, total billed time, and provisioning + teardown timestamps. Owned by the
  orchestrator's teardown step. The plan specifies the budget cap and warn threshold; see
  `## Cost Estimation`.

## Approach

The task is an `experiment-run` (per `meta/task_types/experiment-run/instruction.md`): a defined
hypothesis test ("there exists a Pareto front of DSI vs PD firing rate over a 25-d channel + synapse
parameter space, and the best operating point is more selective AND fires faster than the de
Rosenroll defaults") with explicit independent variables (the 25 parameters) and dependent variables
(DSI, firing rate). The experiment-run guidelines drive the structure: explicit cost cap, seed
logging, per-Pareto-cell raw data saved (`.npz` per cell + per direction), at least 2 charts (Pareto
front + hypervolume trajectory + 3-5 deep-dive panels = 5+ charts), baseline comparison (de
Rosenroll default cell as the "no optimisation" reference point), and an error-analysis section
covering NaN/divergent trials.

**Optimiser choice**: BoTorch qNEHVI (q-noisy expected hypervolume improvement) with a multi-output
Gaussian Process surrogate. qNEHVI is the current state-of-the-art for noisy multi-objective black-
box optimisation (Daulton et al. 2021), handles per-trial seed noise natively, and converges faster
per evaluation than NSGA-II in moderate dimensions (≤ 30). Reference point fixed at (DSI=0, rate=0).

**Alternatives considered**:

* *NSGA-II via DEAP/pymoo* — population-based evolutionary algorithm; needs ≥ 5000 trials at
  population × generation = 50 × 100 to converge in 25 d; rejected because the ~30 s/iter cost on
  the Vast.ai node makes this 40+ hours, exceeding the $5 budget cap. NSGA-II remains the Risk-3
  fallback if qNEHVI fails to converge in 500 iterations.
* *scikit-optimize* — single-objective only; would require scalarising DSI + rate via a fixed
  weight, defeating the Pareto-front objective. Rejected.
* *Ax (Facebook's BoTorch wrapper)* — lighter API but obscures the qNEHVI internals. Rejected; raw
  BoTorch is preferred for transparency in the writeup.
* *Optimising on the local workstation only* — would take ~40 hours single-threaded (160 trials ×
  500 iters × 3 s); rejected per task description's REQ-11 (mandatory remote compute).

**Vendoring strategy** (informed by `research_internet.md` and `research_code.md`): the t0076 12-
channel set is the union of {t0067 5 channels: Nav1.6, NaP, NaR, Kv3, Kv4} ∪ {t0074 3 channels: BK,
SK, Kv7=KM} ∪ {4 truly new MODs: Kdr, HCN, CaL, CaT}. The 4 new MODs are vendored as: Kdr ←
Mainen-Sejnowski 1996 ModelDB 2488 `kv.mod`; HCN ← Hay 2011 ModelDB 139653 `mod/Ih.mod`; CaL ← Hay
2011 ModelDB 139653 `mod/Ca_HVA.mod`; CaT ← Hay 2011 ModelDB 139653 `mod/Ca_LVAst.mod`. All 12 MODs
get the t0067-convention 4-line citation header and a `t76` SUFFIX namespace marker (`kdrt76`,
`iht76`, `calt76`, `catt76` for new files; `nav16t76`/`napt76`/`nart76`/`kv3t76`/`kv4t76` SUFFIX-
renamed from t0067; `bkt76`/`skt76`/`kv7t76` SUFFIX-renamed from t0074). The `cad` mechanism comes
from t0024's already-loaded library DLL — t0076 must NOT include `cadecay.mod` in `code/mods/` or it
will collide with the existing `cad` SUFFIX. Channel densities are Single (one number per channel,
not tier-stratified per soma/dendrite/AIS) — tier-stratification is deferred to the follow-up
suggestion (REQ-10).

**Cell builder reuse**: import `build_dsgc_cell` from
`tasks.t0024_port_de_rosenroll_2026_dsgc.code .build_cell` as a registered library entry point. NO
copy of the cell builder is needed.

**Trial driver reuse**: copy 180 lines of private helpers (`_setup_synapses`, `SynapseBundle`,
`_bar_arrival_times`, `_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events`,
`_count_spikes`, `BASE_ACH_PROB`, `RATE_DT_MS`, `BAR_SIGMA_MS`) from
`tasks/t0024_port_de_rosenroll_ 2026_dsgc/code/run_tuning_curve.py:52-232` into
`code/trial_helpers.py`, with a "COPIED verbatim" header comment per the t0072 precedent.
`_setup_synapses` is the only helper that needs adapting: it must accept
`(N_ACh, N_GABA, ρ_0_ACh, λ_ACh, ρ_0_GABA, λ_GABA)` and call the new parametric placer instead of
the fixed `for dend in cell.terminal_dends` loop.

**Parameter-override pattern**: copy ~80 lines of `CanonicalState` snapshot/restore +
`_apply_mode_overrides` from `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py:117-194`
into `code/apply_params.py`. Adapt to write the 25-d vector to per-segment `gnabar_<suffix>`
attributes for all 12 SUFFIXes plus passive (`Ra`, `cm`, `g_pas`), `cad.depth`, `cad.taur`, and per-
NetCon weight.

**Per-synapse recorder for deep-dives**: copy `_attach_bed_b_recorders`, `BedBRecorders`,
`_save_one_type`, `_save_bed_b_direction` (~125 lines) from
`tasks/t0072_synaptic_traces_pd_nd/code/ run_bed_b.py:203-327`. Used only on the 3-5 best Pareto
cells (NOT on every BO iteration).

**Typst PDF render**: copy `tasks/t0072_synaptic_traces_pd_nd/code/render_pdf.py` (64 lines)
verbatim with `paths` import retargeted. The orchestrator calls this after writing
`results/results_detailed.typ`.

**Single-density (not tier-stratified) channels**: each channel has one optimised density across the
cell. Tier-stratification (different densities for soma / order-1 dendrite / mid dendrite / terminal
/ AIS) would expand the parameter space to ~40 d and is deferred per REQ-10.

**Synapse count rounding**: parameters 18 and 19 (N_ACh, N_GABA) are integers in [50, 350], but
BoTorch operates on continuous variables. The driver rounds to the nearest int before calling the
placer; the GP sees the original continuous value. This is the standard BoTorch pattern for mixed
integer-continuous spaces.

**No predictions asset**: the experiment-run instruction recommends a `predictions` asset for
classification-style experiments. t0076 produces NO per-instance predictions; it produces 25-d → 2-d
function evaluations. The `data/trial_history.parquet` (one row per BoTorch evaluation: 25 input
columns + DSI + PD_rate) IS the analogous artefact and is saved to `results/data/`. No
`assets/predictions/` folder is created.

## Cost Estimation

Hard cap: **$5.00**. Project total budget: $10.00 (per `project/budget.json`); per-task default:
$5.00; this task uses the per-task default cap. The user has authorised the spend explicitly.

Itemised:

* **Vast.ai 64-core CPU node** typical pricing: $0.30/hr (range $0.20-$0.60/hr per
  `research_code.md`). Soft warning if spend reaches $4.00; hard halt + intervention file at $5.00.
* **Provisioning** (Vast.ai instance create +
  `apt update + apt install build-essential gcc + curl install uv + git clone + uv sync + cd code/mods && nrnivmodl . + smoke test`):
  ~20 min × $0.30 = **$0.10**.
* **30-trial Sobol DoE** (initial design-of-experiments): 30 cells × ~30 s/cell = 15 min × $0.30 =
  **$0.075**.
* **300 acquisition steps** (minimum per REQ-4): 300 × ~30 s = 2.5 h × $0.30 = **$0.75**.
* **Up to 500 acquisition steps if budget allows**: 500 × ~30 s = ~4.2 h × $0.30 = **$1.25**.
* **Teardown + result rsync** (~5 min): negligible (≤ $0.03).
* **Expected total: $0.85 - $1.50** for the planned 300-iteration run.
* **Maximum total at 500 iterations + worst-case $0.60/hr pricing**: ~$3.10 — still under the $5.00
  cap.
* **API calls**: $0 (no LLM/API costs in this task; only NEURON simulations).

If the actual spend exceeds $4.00 mid-run, the implementation step should checkpoint the BoTorch
state (save GP + observation history to `data/checkpoint.pt`), terminate gracefully, and write an
intervention file noting the budget proximity. The orchestrator decides whether to authorise
continuation.

## Step by Step

The Step by Step covers ONLY implementation work (per the planning skill's forbidden list — no
results-summary, no cost recording, no suggestion generation). The orchestrator owns setup-machines
(Step 12 below describes what it provisions, but the actual provisioning command is in the
orchestrator's step), implementation orchestration of the remote run, teardown, results,
suggestions, and reporting.

**Milestones**:

* M1 (Steps 1-3): Dependencies + MOD vendoring complete; `nrnivmodl` succeeds locally.
* M2 (Steps 4-7): Driver code complete; local smoke test of one full 160-trial cell evaluation
  succeeds in ≤ 300 s and returns finite (DSI, rate).
* M3 (Steps 8-9): BoTorch loop complete; local smoke test of 5-Sobol + 3-acquisition with reduced
  trial count (4 dirs × 5 seeds = 20 trials/cell) succeeds in ≤ 15 min and produces a Pareto- front
  parquet with ≥ 5 rows.
* M4 (Steps 10-11): Plotting + PDF render code complete and tested on synthetic Pareto data.
* M5 (Step 12): Real run executes on Vast.ai under the orchestrator's setup-machines /
  implementation / teardown chain.

1. **Add Python dependencies to `pyproject.toml`.** Edit `pyproject.toml` to add `botorch>=0.12`,
   `gpytorch>=1.13`, `torch>=2.4`, `pyarrow>=15.0` to the `dependencies` list. Run `uv sync` (no
   wrapper needed — this is a tooling change). Expected: `uv.lock` updated;
   `uv run python -c "import botorch, gpytorch, torch, pyarrow; print('ok')"` prints `ok`. Total
   install footprint ~2 GB (per Risk #7). **Satisfies REQ-9.**

2. **Vendor 4 new MOD files into `code/mods/`.** Source paths and SUFFIX-renamed targets:

| Channel | Source | New file | New SUFFIX | Original cite |
| --- | --- | --- | --- | --- |
| Kdr | ModelDB 2488 `kv.mod` | `code/mods/kdrt76.mod` | `kdrt76` | Mainen-Sejnowski 1996 |
| HCN | ModelDB 139653 `mod/Ih.mod` | `code/mods/iht76.mod` | `iht76` | Kole 2006 / Hay 2011 |
| CaL | ModelDB 139653 `mod/Ca_HVA.mod` | `code/mods/calt76.mod` | `calt76` | Hay 2011 |
| CaT | ModelDB 139653 `mod/Ca_LVAst.mod` | `code/mods/catt76.mod` | `catt76` | Hay 2011 |

   Each file gets the t0067-convention 4-line citation header naming the source ModelDB ID, original
   publication DOI, kinetic parameters (V_half, slope, time constant), and the renamed SUFFIX. Use
   raw-GitHub fetch from `https://raw.githubusercontent.com/ModelDBRepository/<id>/ master/<path>`
   to download cleanly. **Partially satisfies REQ-1** (4 of 12).

3. **Copy 5 t0067 MODs + 3 t0074 MODs into `code/mods/` with SUFFIX rename.** Copy the files
   verbatim and rename SUFFIXes:

   * `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/{nav16t67, napt67, nart67, kv3t67, kv4t67}.mod`
     → `code/mods/{nav16t76, napt76, nart76, kv3t76, kv4t76}.mod` (rename `t67` → `t76` in the
     SUFFIX line and in any internal references).
   * `tasks/t0074_channel_tuning_width_bed_a/code/mods/{bk74, sk74, kv7t74}.mod` →
     `code/mods/{bkt76, skt76, kv7t76}.mod` (rename `t74` → `t76`; for `bk74`/`sk74` also normalise
     the file basename to `bkt76`/`skt76` for consistency with the other `t76` files).

   Then run `nrnivmodl code/mods/` (Linux equivalent of the t0067/t0074 `run_nrnivmodl.cmd` — on the
   local workstation, use `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat code\mods` invoked via a
   `code/run_nrnivmodl.cmd` wrapper copied from t0074). Expected: 12 `.mod` files compile into
   `code/build/nrnmech.dll` (Windows) or `code/mods/x86_64/.libs/libnrnmech.so` (Linux); no SUFFIX
   collisions. **CRITICAL** — without all 12 channels compiled the BoTorch loop cannot apply the
   parameter vector. Idempotent: rerunning `nrnivmodl` overwrites the build folder. **Completes
   REQ-1** (12 of 12).

4. **Write `code/paths.py`, `code/constants.py`, `code/parametric_placer.py`.**

   * `code/paths.py`: per-task path constants. `TASK_ROOT = Path(__file__).parent.parent`,
     `MODS_DIR = TASK_ROOT / "code" / "mods"`, `BUILD_DIR = MODS_DIR / "build"` (Windows) /
     `MODS_DIR / "x86_64" / ".libs"` (Linux), `RESULTS_DIR = TASK_ROOT / "results"`,
     `IMAGES_DIR = RESULTS_DIR / "images"`, `DATA_DIR = RESULTS_DIR / "data"`,
     `TRIAL_HISTORY_PARQUET = DATA_DIR / "trial_history.parquet"`,
     `PARETO_FRONT_PNG = IMAGES_DIR / "pareto_front.png"`,
     `HYPERVOLUME_PNG = IMAGES_DIR / "hypervolume_trajectory.png"`,
     `RESULTS_TYPST = RESULTS_DIR / "results_detailed.typ"`,
     `RESULTS_PDF = RESULTS_DIR / "results_detailed.pdf"`.

   * `code/constants.py`: 25-d parameter bounds as a frozen dataclass per the python style guide.
     `RECORD_DT_MS: float = 0.1`, `TSTOP_MS: float = 1400.0`, `THRESHOLD_MV: float = -10.0`.
     `CHANNEL_SUFFIXES: tuple[str, ...] = ("nav16t76", "napt76", "nart76", "kdrt76", "kv3t76", "kv4t76", "kv7t76", "iht76", "calt76", "catt76", "bkt76", "skt76")`
     (order MUST match parameter indices 1-12).
     `ANGLES_8DIR_DEG: tuple[int, ...] = (0, 45, 90, 135, 180, 225, 270, 315)` (copied from
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:87`). `N_SEEDS: int = 20`,
     `N_DIRECTIONS: int = 8`. `ParameterBounds` dataclass with `lower: ndarray[(25,)]` and
     `upper: ndarray[(25,)]` per the table in `task_description.md` lines 38-55.

   * `code/parametric_placer.py`: walks `cell.all_dends` (350 sections), calls
     `h.distance(cell.soma(0.5), sec(0.5))` per section midpoint to get path distance `d` (µm) per
     the t0050 precedent, computes per-section weights `w_i = ρ_0 · exp(-d_i / λ) · L_i`,
     normalises, samples `N` positions without replacement weighted by `w` using
     `numpy.random. Generator(PCG64(seed)).choice(...)`, returns `list[tuple[Section, float]]`
     (section + position in [0, 1]). 90 LOC. **Satisfies REQ-2.**

5. **Write `code/apply_params.py`.** Copy `CanonicalState` snapshot/restore from
   `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py:117-194` (~80 lines) into
   `code/apply_params.py` with a "COPIED verbatim from t0066 lines 117-194" header comment per the
   t0072 precedent. Then write a new
   `apply_parameter_vector(*, cell: DSGCCell, bundle: SynapseBundle, params: ParameterVector) -> None`
   function that: (a) Inserts the 12 `t76` SUFFIX mechanisms into every section if not already
   present. (b) Writes `setattr(seg, f"gnabar_{suffix}", params.channel_densities[i])` per segment
   per channel for all 12 channels. (c) Writes `sec.Ra = params.Ra`; `seg.cm = params.cm`;
   `seg.g_pas = params.gleak`. (d) Writes `seg.depth_cad = params.cad_depth`;
   `seg.taur_cad = params.cad_taur`. (e) Writes `nc.weight[0] = params.w_ach` for all ACh NetCons;
   `nc.weight[0] = params.w_gaba` for all GABA NetCons. For (a), use `_ensure_t76_dll_loaded()`
   (copied 14 lines from `tasks/t0067_t0065_soma_channel_ addition_sweep/code/run_sweep.py:107-120`)
   to ensure the DLL is loaded once per process before the first `insert()` call. Total ~120 LOC
   including the copied state snapshot.

6. **Write `code/trial_driver.py`.** Copy 180 lines of private helpers (`_setup_synapses`,
   `SynapseBundle`, `_bar_arrival_times`, `_rates_with_ar2_noise`, `_gaba_prob_for_direction`,
   `_rates_to_events`, `_count_spikes`, `BASE_ACH_PROB`, `RATE_DT_MS`, `BAR_SIGMA_MS`) from
   `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:52-232` into
   `code/trial_helpers.py` with a "COPIED verbatim from t0024 lines 52-232" header. Adapt
   `_setup_synapses` to accept (N_ACh, N_GABA, ρ_0_ACh, λ_ACh, ρ_0_GABA, λ_GABA, w_ACh, w_GABA) and
   call the new parametric placer (Step 4) instead of the fixed `for dend in cell.terminal_dends`
   loop.

   Then write `code/trial_driver.py` with two top-level functions:

   * `run_one_trial(*, cell: DSGCCell, bundle: SynapseBundle, direction_deg: int, seed: int, rho: float) -> TrialResult`
     — wraps
     `tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_ curve._run_single_trial`-style logic
     with try/except around `h.run()` returning
     `TrialResult(spike_count=0, peak_mv=-100.0, error="NaN")` on `RuntimeError` per Risk #4.

   * `evaluate_parameter_vector(*, params: ParameterVector, n_seeds: int, n_directions: int) -> EvalResult`
     — uses `concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()-1)` to dispatch
     `n_directions × n_seeds = 160` trials in parallel. Workers receive (params, direction, seed);
     each worker calls `build_dsgc_cell()` once on first invocation (cached in a process-local
     global), then `apply_parameter_vector`, then `run_one_trial`. Returns
     `EvalResult(dsi=..., pd_rate_hz=..., n_nan=...)` where DSI is computed across the 20 seeds at
     each PD/ND direction and the firing rate is the PD spike count divided by 1.0 s.

   ~80 LOC for the trial_driver.py layer above the copied helpers. **Satisfies REQ-3.**

7. **Local smoke test of one full 160-trial cell evaluation.** Run:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0076_bedb_dsi_firing_rate_mobo -- uv run python -u -c "from tasks.t0076_bedb_dsi_firing_rate_mobo.code.trial_driver import evaluate_parameter_vector; from tasks.t0076_bedb_dsi_firing_rate_mobo.code.constants import ParameterVector; r = evaluate_parameter_vector(params=ParameterVector.default(), n_seeds=20, n_directions=8); print(r)"`.
   **Validation gate**: baseline DSI for a default de Rosenroll cell from t0066 is approximately
   0.40-0.55 (per the t0066 protocol results, `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/`). Expected:
   DSI in [0.30, 0.70], PD rate in [10, 80] Hz, no NaN trials. **If DSI < 0.20 or PD rate < 5 Hz or
   n_nan > 5: HALT and debug** — read 5 individual trial results from the worker logs and verify (a)
   `apply_parameter_vector` is writing to the right per-segment attributes, (b) the placer returned
   ~177 ACh + ~177 GABA synapses (defaults), (c) the 12 SUFFIX mechanisms compiled cleanly. Do not
   proceed to BoTorch wiring with broken trials. This catches HOC errors before remote provisioning.
   Wall time should be ≤ 300 s on a single workstation with default 7-core ProcessPoolExecutor.

8. **Write `code/mobo_loop.py`.** BoTorch qNEHVI loop. Imports:
   `from botorch.acquisition. multi_objective.monte_carlo import qNoisyExpectedHypervolumeImprovement`,
   `from botorch.models import SingleTaskGP, ModelListGP`,
   `from botorch.utils.multi_objective.box_decompositions. non_dominated import FastNondominatedPartitioning`,
   `from botorch.optim import optimize_acqf`,
   `from botorch.utils.sampling import draw_sobol_samples`, `import torch`. Structure: (a) Parse CLI
   args: `--n-iterations 400` (default), `--workers 64`, `--checkpoint-every 50`. (b) Initial Sobol
   DoE: 30 candidates from `draw_sobol_samples(bounds=bounds, n=30, q=1)`, evaluate each via
   `evaluate_parameter_vector`, append to `train_X` and `train_Y`. (c) For each acquisition step
   (1..n_iterations): (i) Fit `ModelListGP` of 2 `SingleTaskGP`s (one per objective) to (train_X,
   train_Y). (ii) Build `qNEHVI` with `ref_point=torch.tensor([0.0, 0.0])`,
   `partitioning=FastNondominatedPartitioning(ref_point=ref_point, Y=train_Y)`. (iii)
   `optimize_acqf(acq_func=qnehvi, bounds=bounds, q=1, num_restarts=10, raw_samples=512)` →
   `candidate_X`. (iv) Evaluate the candidate via `evaluate_parameter_vector`, append to (train_X,
   train_Y). (v) Every `checkpoint_every` iterations: write `data/trial_history.parquet` (one row
   per evaluation: 25 input cols + dsi + pd_rate_hz + n_nan + iteration + sobol_or_acq) plus
   `data/checkpoint.pt` (torch save of train_X, train_Y, GP state). Compute current hypervolume via
   `botorch.utils.multi_objective.hypervolume.Hypervolume(ref_point= ref_point).compute(pareto_Y)`
   and append to `data/hypervolume_trajectory.csv`. (d) After all iterations: compute final Pareto
   front from train_Y, save to `data/pareto_front.json` (list of {iteration, params (25 floats),
   dsi, pd_rate_hz}). ~280 LOC. **Satisfies REQ-4.**

9. **Local smoke test of BoTorch loop with reduced trial count.** Run:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0076_bedb_dsi_firing_rate_mobo -- uv run python -u -m tasks.t0076_bedb_dsi_firing_rate_mobo.code.mobo_loop --n-iterations 3 --n-sobol 5 --n-seeds 5 --n-directions 4 --workers 4`.
   **Validation gate**: this is 8 evaluations × 20 trials/eval = 160 trials total. Baseline trivial
   expectation: at least one evaluation should produce DSI > 0 (most cells DO show some directional
   preference; only pathological gbar combinations fail). Expected: 5 + 3 = 8 rows in
   `data/trial_history.parquet`, non-empty Pareto front (at least 1 entry), monotonic hypervolume.
   Wall time ≤ 15 min on a 7-core workstation. **If hypervolume is 0 throughout: HALT and inspect**
   — read the 8 individual evaluations from the parquet file and check whether any DSI > 0; if all
   DSI ≤ 0, the trial driver is broken (Step 6/7 issue). Do NOT launch on Vast.ai with a broken
   loop.

10. **Write `code/plot_pareto.py`.** Reads `data/trial_history.parquet`,
    `data/hypervolume_trajectory.csv`, `data/pareto_front.json`. Produces:

    * `results/images/pareto_front.png` — scatter of all evaluations (small grey dots) + Pareto
      front (large coloured dots), x = DSI, y = PD firing rate (Hz), with reference de Rosenroll
      default cell as a star marker (DSI ≈ 0.45, rate ≈ 30 Hz from t0066 baseline).
    * `results/images/hypervolume_trajectory.png` — line plot of hypervolume vs iteration; should be
      monotonic.
    * For 3-5 representative Pareto cells (selected as: highest DSI, highest rate, knee point per
      `botorch.utils.multi_objective.utils.find_pareto_optimal_points`-style), launch a deep-dive
      trial via `evaluate_parameter_vector` with `n_directions=8, n_seeds=20` and the t0072 per-
      synapse recorder attached. Save:
      * `results/data/deepdive_cell_<i>.npz` — t_rec, v_soma, g_ACh per synapse, g_GABA per synapse,
        v_local per synapse, per direction (PD + ND).
      * `results/images/deepdive_cell_<i>_tuning_curve.png` — 8-direction tuning curve (mean ± SEM
        across 20 seeds).
      * `results/images/deepdive_cell_<i>_traces.png` — 4-panel: PD soma Vm, ND soma Vm, PD g_ACh
        sum, PD g_GABA sum.

    Copy `_attach_bed_b_recorders`, `BedBRecorders`, `_save_one_type`, `_save_bed_b_direction` (~125
    lines) from `tasks/t0072_synaptic_traces_pd_nd/code/run_bed_b.py:203-327` into
    `code/recorder.py` with a "COPIED verbatim from t0072" header. ~250 LOC for plot_pareto.py.
    **Satisfies REQ-5 + REQ-6.**

11. **Write `code/render_pdf.py`.** Copy `tasks/t0072_synaptic_traces_pd_nd/code/render_pdf.py` (64
    lines) verbatim with `paths` import retargeted from
    `tasks.t0072_synaptic_traces_pd_nd. code.paths` to
    `tasks.t0076_bedb_dsi_firing_rate_mobo.code.paths`. The orchestrator calls
    `uv run python -u -m tasks.t0076_bedb_dsi_firing_rate_mobo.code.render_pdf` after writing
    `results/results_detailed.typ`. The script asserts that the produced PDF is at least 50 KB.
    **Supports REQ-7** (the orchestrator's results step uses this).

12. **Write `code/run_remote.sh` (Linux remote setup script).** This is the script the
    orchestrator's setup-machines step uploads to and runs on the Vast.ai instance. Contents:

    ```bash
    #!/usr/bin/env bash
    set -euo pipefail
    apt-get update
    apt-get install -y --no-install-recommends \
      git curl build-essential gcc libncurses5-dev libreadline-dev \
      libxext-dev libxt-dev libxmu-dev mpich
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    cd /root
    git clone <REPO_URL> neuron-channels
    cd neuron-channels
    git checkout task/t0076_bedb_dsi_firing_rate_mobo
    uv sync
    cd tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods
    nrnivmodl .
    cd /root/neuron-channels
    # Smoke test: import + 1 trial
    uv run python -u -c "from tasks.t0076_bedb_dsi_firing_rate_mobo.code.trial_driver import \
      evaluate_parameter_vector; from tasks.t0076_bedb_dsi_firing_rate_mobo.code.constants \
      import ParameterVector; r = evaluate_parameter_vector(params=ParameterVector.default(), \
      n_seeds=2, n_directions=2); print('SMOKE:', r)"
    # Real run (the orchestrator may invoke this separately):
    # uv run python -u -m tasks.t0076_bedb_dsi_firing_rate_mobo.code.mobo_loop \
    #   --n-iterations 400 --workers 64 > /root/output.log 2>&1
    ```

    The orchestrator's setup-machines step provisions the Vast.ai instance per `## Remote Machines`
    below and runs this script. The orchestrator's implementation step then runs the BoTorch loop
    via
    `tmux new-session -d -s work "uv run python -u -m tasks.t0076_bedb_dsi_firing_rate_mobo. code.mobo_loop --n-iterations 400 --workers 64 2>&1 | tee /root/output.log; echo DONE >> /root/output.log"`.
    The orchestrator's teardown step rsyncs `tasks/t0076_bedb_dsi_firing_rate_ mobo/data/` and
    `results/` back to the local workstation, then `vastai destroy instance`. **Supports REQ-11 +
    REQ-12** (this script is the contract; the orchestrator wraps it).

13. **Compute Pareto front + hypervolume + 3-5 deep-dive figures.** This step runs ON THE REMOTE,
    triggered by the orchestrator's implementation step. After `mobo_loop.py` finishes (Step 8 on
    remote), run `uv run python -u -m tasks.t0076_bedb_dsi_firing_rate_mobo.code.plot_pareto` on the
    remote. Outputs land in `tasks/t0076_bedb_dsi_firing_rate_mobo/results/{images,data}/` on the
    remote and are rsynced to the local workstation by the teardown step. Record per-cell DSI values
    for `results/metrics.json` registered metric `direction_selectivity_index` (multi-variant format
    with one variant per representative Pareto cell). ~30-60 min wall time on the remote (3-5
    deep-dive trials × 160 trials each × ~3 s / 64-core parallelism = ~15 min
    + plotting). **Completes the on-remote computation; the orchestrator's teardown handles the
      instance destruction. Satisfies REQ-5 + REQ-6 (remote-side completion).**

**Registered metric measurement**: of the 4 registered metrics in `meta/metrics/`, only
`direction_selectivity_index` (DSI) is measurable from this experiment — it is the primary
objective. `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, and `tuning_curve_rmse` could in
principle be computed from the 8-direction tuning curves of the 3-5 deep-dive cells but are
secondary to the headline (DSI, PD firing rate) Pareto and add no new information beyond the deep-
dive figures. The plan computes ONLY `direction_selectivity_index` per Pareto cell into
`results/metrics.json` (multi-variant format, one variant per representative Pareto cell). The other
3 metrics are deliberately omitted because the headline objective IS DSI; computing tuning-curve
descriptors per cell would be redundant with the deep-dive PNGs and inflate the metrics file without
scientific gain. This is a deliberate, documented omission per the planning skill's rule.

## Remote Machines

**Required**: yes — Vast.ai 64-core CPU instance. **Per REQ-11 the optimisation MUST run on the
Vast.ai instance**, not on the local workstation; the local workstation's role is limited to (a)
holding the task folder, (b) the orchestrator's SSH session for setup-machines / implementation /
teardown, and (c) receiving the rsync'd results.

**Vast.ai search query** (CPU-only, derived from `arf/skills/setup-remote-machine/SKILL.md` adapted
per `research_code.md`'s "NEURON Deployment on Vast.ai" subsection):

```bash
vastai search offers \
  'num_gpus=0 cpu_cores>=64 cpu_ram>=64 disk_space>=20 \
  reliability>0.98 rentable=true verified=true dph<1.0' \
  --order 'dph' --limit 20 --raw
```

Bid pricing < $1.00/hr (target ~$0.30/hr per `research_code.md`).

**Image**: `python:3.12-bookworm` (~1.2 GB, includes pip and gcc; the Linux NEURON wheel is cp312).
NOT a pytorch image (those are GPU-oriented and ~5 GB; we want CPU-only). NOT `python:3.12-slim`
(missing the gcc that `nrnivmodl` needs).

**Smoke test on the freshly provisioned instance** (from `research_code.md`):

```bash
python -c "from neuron import h; h.load_file('stdrun.hoc'); s = h.Section(); s.insert('hh'); print('OK', s.gnabar_hh)"
```

Expected: `OK 0.12`. Then second smoke test confirms the t0076 MOD library:

```bash
cd /root/neuron-channels/tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods && \
  python -c "from neuron import h; h.nrn_load_dll('./x86_64/.libs/libnrnmech.so'); s = h.Section(); s.insert('nav16t76'); print('OK')"
```

**Estimated billed runtime**: 2.5-4 hours wall on the 64-core node (300-500 acquisition steps × 30
s/iter) + 20 min provisioning + 5 min teardown. Total billable: ~3-5 hours × ~$0.30/hr = $0.85 -
$1.50 expected; $5.00 hard cap. The setup-machines / implementation / teardown chain is owned by the
orchestrator (NOT in this plan's Step by Step), but `code/run_remote.sh` (Step 12 above) is the
contract.

**Teardown**: orchestrator rsyncs `data/` and `results/` back, then
`vastai destroy instance <INSTANCE_ID>`. Records actual billed amount in `results/costs.json` and
instance specs in `results/remote_machines_used.json` per REQ-12.

## Assets Needed

* **`de_rosenroll_2026_dsgc` library v0.1.0** (registered) — from
  `t0024_port_de_rosenroll_2026_dsgc`. Imported via
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`.
  Provides the Bed B cell builder + the already-loaded `cad` SUFFIX from `cadecay.mod`.
* **`dsgc_active_channel_pack` library v0.1.0** (registered) — from
  `t0074_channel_tuning_width_bed_a`. 3 MOD source files (`bk74.mod`, `sk74.mod`, `kv7t74.mod`) at
  `tasks/t0074_channel_tuning_width_ bed_a/code/mods/` are copied (NOT imported) into `code/mods/`
  with SUFFIX rename.
* **t0067 5-MOD pack** (NOT a registered library, but copied per project convention) — from
  `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/`. 5 MOD source files copied with SUFFIX
  rename `t67` → `t76`.
* **t0066 trial-driver helpers** (NOT a library) — copied 80 lines from
  `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py:117-194`.
* **t0024 trial-driver helpers** (NOT a library) — copied 180 lines from
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:52-232`.
* **t0072 per-synapse recorder + Typst PDF render** (NOT libraries) — copied ~190 lines from
  `tasks/t0072_synaptic_traces_pd_nd/code/{run_bed_b.py, render_pdf.py}`.
* **External: ModelDB 139653 + 2488** — 4 raw `.mod` files downloaded via raw-GitHub fetch from the
  ModelDBRepository GitHub mirror; no API key required.
* **Vast.ai account credit** — $10 user credit; this task's cap is $5.

## Expected Assets

`task.json` `expected_assets` is `{}` (empty). The plan does NOT create new asset entries (no
papers, datasets, libraries, models, predictions, or answers). The compute outputs land in:

* `results/images/` — Pareto-front PNG, hypervolume-trajectory PNG, 3-5 deep-dive cell PNGs (≥ 5
  files).
* `results/data/` — `trial_history.parquet`, `pareto_front.json`, `hypervolume_trajectory.csv`,
  `deepdive_cell_<i>.npz` × 3-5.
* `results/metrics.json` — multi-variant format with one variant per representative Pareto cell;
  each variant records the registered metric `direction_selectivity_index`.

These are task results, not assets — they live in `results/` and are produced by the implementation
\+ orchestrator steps. The orchestrator's results / suggestions / reporting steps write
`results_summary.md`, `results_detailed.md`, `costs.json`, `suggestions.json`, and
`remote_machines_used.json`.

## Time Estimation

| Phase | Estimated wall time | Owner |
| --- | --- | --- |
| Research (papers + internet + code) | 0 h (already completed) | n/a |
| Step 1: pyproject.toml + uv sync | 5-15 min (botorch+torch download is ~2 GB) | implementation agent |
| Step 2: vendor 4 new MODs | 30-60 min (raw-GitHub fetch + citation header + SUFFIX rename) | implementation agent |
| Step 3: copy 8 MODs from t0067/t0074 + nrnivmodl | 15-30 min | implementation agent |
| Step 4: paths.py, constants.py, parametric_placer.py | 1-2 h | implementation agent |
| Step 5: apply_params.py | 1-2 h (the trickiest mapping step) | implementation agent |
| Step 6: trial_driver.py + trial_helpers.py | 1-2 h | implementation agent |
| Step 7: local smoke test of 1 cell × 160 trials | ~10 min run + debug headroom | implementation agent |
| Step 8: mobo_loop.py | 2-3 h | implementation agent |
| Step 9: local BoTorch smoke test (5 Sobol + 3 acq) | ~30 min run + debug headroom | implementation agent |
| Step 10: plot_pareto.py + recorder.py | 1-2 h | implementation agent |
| Step 11: render_pdf.py | 15 min (copy + retarget) | implementation agent |
| Step 12: run_remote.sh | 30 min | implementation agent |
| Step 13: remote run (300-500 iters × 30 s + plotting) | 2.5-4 h wall on Vast.ai | orchestrator's setup-machines + implementation + teardown |
| Orchestrator: results / suggestions / reporting | 2-3 h | orchestrator |
| **Total local code time** | **~10-15 h** | implementation agent |
| **Total remote billed time** | **~3-5 h** | orchestrator |

## Risks & Fallbacks

| # | Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| 1 | One or more of the 4 newly-vendored MODs (Kdr, HCN, CaL, CaT) fails to compile under modern NEURON 8.x. | Low | Blocks Step 3; cascades to all later steps. | Per `research_internet.md` Methodology Insights: drop in priority order BK first (already vendored from t0074, low risk), then CaT, then CaL. The 8-channel reduced set is `(Nav1.6, NaP, NaR, Kdr, Kv3, Kv4, KM, HCN, SK)` if BK/CaL/CaT fail. The BoTorch dimension shrinks from 25 → 22-24; framework unaffected. Document the drop in the writeup. |
| 2 | Vast.ai has no 64-core CPU node available within the $1/hr ceiling at provisioning time. | Medium | Blocks Step 13. | Try adjacent regions; relax the price cap up to $1/hr; or accept a 32-core node (run wall doubles to ~5-8 h, still under the $5 cap at $0.30/hr). Do NOT fall back to local-workstation execution per REQ-11. If no remote node is available within the $5 cap, write `intervention/no_vast_node_available.md` and stop. |
| 3 | BoTorch qNEHVI fails to converge in 500 iterations (Pareto front still expanding, hypervolume not plateauing). | Medium | Suboptimal Pareto front; REQ-4 minimum 300 iters still satisfied. | Manually inspect the front at iter 100, 200, 400; check the hypervolume metric for monotonic increase. If still expanding at iter 500, switch to NSGA-II via `pymoo` for the next attempt (cap at 5000 trials = $4.50 at $0.30/hr × 5 h). Document the under-convergence in results. |
| 4 | Calcium dynamics make the cell numerically unstable at extreme channel-density combinations (e.g., gbar = 0.5 S/cm² for both Nav1.6 and NaP). | Medium | Trial errors out; BoTorch sees NaN. | `trial_driver.run_one_trial` catches the `RuntimeError` from `h.run()` and returns the worst-case score (DSI = -1.0, rate = 0.0). The optimiser learns to avoid that region. Track `n_nan` per evaluation in the parquet; if > 50% of trials NaN at iter 50, halt and inspect the parameter range. |
| 5 | Stochastic per-trial noise on DSI is large enough that the GP can't learn (DSI estimates have SE > 0.1). | Low | GP residual variance dominates; Pareto front is noisy. | High GP residual variance after 50 iterations triggers fallback: increase seeds per direction from 20 to 40 (doubles per-iter time but halves DSI SE). Or use a noise-aware GP kernel (BoTorch's `HeteroskedasticSingleTaskGP`). |
| 6 | The parametric synapse placer (exponential decay) is too restrictive; the optimal cell needs a non-monotonic spatial pattern. | Low | Best-Pareto cells cluster at parameter-bound extremes (ρ_0 ≈ 0.1 or λ ≈ 500 µm). | Add a quadratic term to the spatial rule (`ρ(d) = ρ_0 · exp(-d/λ) · (1 + α · d²)`) — adds 2 params per type, total dim = 29. Defer to a follow-up task per REQ-10. |
| 7 | `botorch + gpytorch + torch` install footprint is ~2 GB; uv sync slow / disk concern on Vast.ai instance. | Medium | Adds 5-10 min to provisioning; may exceed disk quota on a small instance. | Provision with `disk_space>=20 GB`. The `torch>=2.4` default install pulls CUDA libraries even though they're unused on CPU; this is acceptable per Risk #9 below. Document install size in writeup. |
| 8 | Linux NEURON wheel version mismatch with project's pinned local `nrn-8.2.7` (Windows build). | Low | Different kinetic constants between local smoke test and remote run. | The `pip install neuron==8.2.7` Linux cp312 wheel exists on PyPI. If 8.2.7 is unavailable, install latest 8.x and document the divergence in the writeup. The HHst kinetics are stable across NEURON 8.x; no behavioural drift expected. |
| 9 | BoTorch CPU-only torch wheel install (`torch>=2.4+cpu`) fails on Vast.ai. | Low | Falls back to default `torch>=2.4` GPU+CPU build (~2 GB extra disk). | Default `torch>=2.4` works fine on CPU even on a no-GPU node — it just pulls the CUDA libraries that go unused. Acceptable cost. |

## Verification Criteria

* **PL-VC1 (REQ-1, REQ-3 coverage)**: After Steps 2-3 complete, run
  `uv run python -u -c "from pathlib import Path; mods = sorted(p.stem for p in Path('tasks/t0076_bedb_dsi_firing_rate_mobo/ code/mods').glob('*.mod')); print(len(mods), mods)"`.
  Expected output:
  `12 ['bkt76', 'calt76', 'catt76', 'iht76', 'kdrt76', 'kv3t76', 'kv4t76', 'kv7t76', 'nart76', 'nav16t76', 'napt76', 'skt76']`
  (alphabetical; 12 files; all `t76` SUFFIX namespace).

* **PL-VC2 (REQ-1 compilation)**: After Step 3, run
  `uv run python -u -c "from neuron import h; h.nrn_load_dll('tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods/build/nrnmech.dll'); s = h.Section(); [s.insert(suf) for suf in ('nav16t76','napt76','nart76','kdrt76','kv3t76','kv4t76','kv7t76', 'iht76','calt76','catt76','bkt76','skt76')]; print('OK')"`.
  Expected: prints `OK` (all 12 SUFFIX mechanisms resolve).

* **PL-VC3 (REQ-2, REQ-3 driver works)**: After Step 7, the local smoke test must print a
  `EvalResult` with `dsi` in [0.30, 0.70], `pd_rate_hz` in [10, 80], `n_nan == 0`, in ≤ 300 s wall.

* **PL-VC4 (REQ-4 BoTorch loop works locally)**: After Step 9, the BoTorch smoke test produces
  `tasks/t0076_bedb_dsi_firing_rate_mobo/data/trial_history.parquet` with ≥ 8 rows and a non-empty
  Pareto front (at least 1 entry).

* **PL-VC5 (REQ-4, REQ-5, REQ-6 remote run completes)**: After Step 13 + orchestrator's teardown,
  `tasks/t0076_bedb_dsi_firing_rate_mobo/data/trial_history.parquet` exists with ≥ 330 rows and
  `tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lists ≥ 5 distinct
  configurations after iteration 200. `tasks/t0076_bedb_dsi_firing_rate_mobo/results/images/`
  contains `pareto_front.png`, `hypervolume_trajectory.png`, and at least 3 × 2 = 6 deep-dive PNGs.
  Run
  `uv run python -u -c "import json; d = json.loads(open('tasks/t0076_bedb_dsi_firing_ rate_mobo/results/data/pareto_front.json').read()); print(len(d), 'pareto cells')"`.

* **PL-VC6 (REQ-12 cost recorded)**: After orchestrator's teardown,
  `tasks/t0076_bedb_dsi_firing_ rate_mobo/results/costs.json` exists and `total_usd` is ≤ $5.00 and
  \> 0.

* **PL-VC7 (plan verificator passes)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs -- task-id t0076_bedb_dsi_firing_rate_mobo -- uv run python -m arf.scripts.verificators.verify_plan t0076_bedb_dsi_firing_rate_mobo`.
  Expected: exit 0, no errors.

* **PL-VC8 (REQ coverage check)**: All REQ items REQ-1 through REQ-12 are referenced in at least one
  Step or in the orchestrator's responsibilities documented in this plan. Verify by running
  `uv run python -u -c "import re; t = open('tasks/t0076_bedb_dsi_firing_rate_mobo/plan/plan.md'). read(); reqs = set(re.findall(r'REQ-\d+', t)); print(sorted(reqs)); assert reqs >= {f'REQ-{i}' for i in range(1, 13)}, reqs"`.
  Expected: prints REQ-1 through REQ-12 and asserts pass.
