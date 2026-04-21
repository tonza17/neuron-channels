---
spec_version: "2"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
date_completed: "2026-04-21"
status: "complete"
---
# Plan: Port de Rosenroll 2026 DSGC Model

## Objective

Port the NEURON-based direction-selective ganglion cell (DSGC) model from de Rosenroll,
Sethuramanujam, and Awatramani (2026, *Cell Reports*, DOI `10.1016/j.celrep.2025.116833`) into the
project as a standalone library asset `de_rosenroll_2026_dsgc`, exercise it with both the paper's
native 8-direction moving-bar protocol and the project-standard 12-angle sweep, and score both
outputs with `tuning_curve_loss`. Done means: (1) library asset compiled on Windows with
`nrnmech.dll`; (2) paper asset already on disk (registered in step 5); (3) `tuning_curves_8dir.csv`
and `tuning_curves_12ang.csv` under the canonical `(angle_deg, trial_seed, firing_rate_hz)` schema;
(4) `score_report.json` against the t0004 envelope for the 12-angle CSV; (5) DSI ~0.39 recovered for
the correlated-release condition and DSI ~0.25 recovered for the uncorrelated / AMB condition,
proving the subcellular-vs-global dissociation.

## Task Requirement Checklist

Task text verbatim from `task.json` and `task_description.md`:

> **Name**: Port de Rosenroll 2026 DSGC model
>
> **Short**: Port de Rosenroll et al. 2026 DSGC as a third NEURON implementation, incorporating
> modern channel mechanisms. DEFERRED pending t0022 outcomes.
>
> **Scope**: Port the de Rosenroll et al. 2026 DSGC model into the project as a new library asset
> (proposed slug `de_rosenroll_2026_dsgc`) following the HOC/MOD/morphology layout established by
> t0008. Fetch the paper as a paper asset if it is not already present. Run the standard 12-angle
> moving-bar tuning-curve protocol using the driver infrastructure from t0022 where compatible,
> producing `tuning_curves.csv` and a `score_report.json` against the target tuning curve from
> t0004. Compare results against the Poleg-Polsky lineage (t0008, t0020, t0022) and the Hanson port
> (t0023) in `results_detailed.md`.
>
> **Deliverables**: New library asset `de_rosenroll_2026_dsgc` with HOC, MOD, and morphology files,
> `details.json`, and `description.md`; paper asset for the source paper; 12-angle moving-bar tuning
> curve (`tuning_curves.csv` and `score_report.json`); cross-model comparison in
> `results_detailed.md` against t0008, t0020, t0022, t0023.

Requirements extracted from task text plus research clarifications (`research_internet.md`):

* **REQ-1** — Create library asset `assets/library/de_rosenroll_2026_dsgc/` with `sources/`
  (repository HOC/MOD files from [dsMicro-GH]), `code/` (NEURON bootstrap, driver, scoring glue), a
  `run_nrnivmodl.cmd` wrapper, `details.json`, and `description.md`. Evidence: step 3 produces a
  validated library passing `verify_library_asset`.
* **REQ-2** — Register the source paper as a paper asset (already done in step 5,
  `10.1016_j.celrep.2025.116833`). Evidence: paper asset verified by manual structural check against
  `meta/asset_types/paper/specification.md` v3.
* **REQ-3** — Produce a 12-angle moving-bar tuning curve CSV in the canonical schema
  `(angle_deg, trial_seed, firing_rate_hz)` and a `score_report.json` against the t0004 envelope via
  `tuning_curve_loss.score`. Evidence: step 6 outputs `data/tuning_curves_12ang.csv` and
  `data/score_report.json` with non-null DSI / peak / HWHM / RMSE fields.
* **REQ-4** — Produce the paper-match 8-direction tuning curve CSV in the same schema under a
  separate filename (`data/tuning_curves_8dir.csv`). Evidence: step 6 output file exists and
  8-direction DSI is reported in `results/metrics.json` alongside the 12-angle DSI.
* **REQ-5** — Recover the correlated-release DSI benchmark (DSI ~0.39 for correlated SAC ACh/GABA
  co-release) and the uncorrelated / AMB DSI benchmark (DSI ~0.25, ~36 percent drop) as the
  port-fidelity check. Evidence: step 7 validation gate reports both DSI values and the ratio; step
  10 documents any miss in `results_detailed.md`.
* **REQ-6** — Cross-model comparison in `results_detailed.md` against t0008 (DSI 0.316 / peak 18.1
  Hz), t0020 (DSI 0.7838 / peak 14.85 Hz), t0022 (DSI ~0.7 / peak ~15 Hz), and t0023 (Hanson port,
  outputs TBD). Evidence: `results_detailed.md` contains a comparison table with those four models
  plus the de Rosenroll port under all four registered metric keys.

Ambiguities flagged:

* **Direction count** — task says "standard 12-angle"; source uses 8. Resolved in favor of running
  both. 8-direction is the paper-match validation target (REQ-4, REQ-5); 12-angle is the
  project-comparison output for scoring against t0004 (REQ-3).
* **Parameter-set authority** — paper text and repository code disagree on Ra, eleak, and Na/K
  densities. Resolved in favor of the code values per `research_internet.md` Recommendations; text
  values are logged for a future sensitivity sweep, not used here.
* **AIS overlay** — `research_papers.md` recommended a Nav1.6 / Nav1.2 AIS split; the source model
  has no AIS. Resolved by dropping the overlay from this port (a follow-up suggestion is filed in
  step 14 of the overall task).

## Approach

Build the new library as a structural sibling of `modeldb_189347_dsgc`, following the t0008 layout
verbatim except for the model-specific HOC/MOD/morphology files. The de Rosenroll companion code
[dsMicro-GH] at `geoffder/ds-circuit-ei-microarchitecture` (MIT, Zenodo DOI
`10.5281/zenodo.17666158`) is the authoritative source: fork the relevant subset into
`assets/library/de_rosenroll_2026_dsgc/sources/` (HOC morphology `RGCmodelGD.hoc`, MOD mechanisms
`HHst_noiseless.mod`, `cadecay.mod`, `Exp2NMDA.mod`, plus the synaptic Exp2Syn config), strip any
`.git`, and compile with the existing `run_nrnivmodl.cmd` wrapper from t0008. The Python driver
`build_cell.py` mirrors t0008 function-for-function but points at the new HOC files, implements the
AR(2) release-rate noise process with `phi = [0.9, -0.1]` and cross-channel correlation `rho = 0.6`,
applies the code-authoritative parameter set (`Ra = 100 Ohm*cm`, `eleak = -60 mV`,
`gbar_Na = 150/200/30 mS/cm^2` across soma/primary/distal, `gbar_K = 35/40/25 mS/cm^2`,
`celsius = 36.9 C`, `dt = 0.1 ms`), and applies the Briggman 2011 connectome-placed SAC varicosities
with a 30 um minimum SAC-soma offset. The `run_tuning_curve.py` driver loops over both direction
sets (8 and 12) and over correlated and uncorrelated release conditions, writing the canonical CSV
schema. Scoring reuses `tuning_curve_loss.score` from t0012 verbatim.

**Alternatives considered**: (a) Reuse the `modeldb_189347_dsgc` HOC skeleton with parameter
overrides — rejected because the morphology (341 sections in `RGCmodelGD.hoc`) and channel
mechanisms (`HHst_noiseless` vs `HHst`) differ enough that a "parameter override" path would mask
structural differences. (b) Synthesize the driver from t0022's `schedule_ei_onsets` — rejected
because the paper specifies its own driver with AR(2) noise and correlated release, which t0022's
protocol does not model. (c) Add a Nav1.6 / Nav1.2 AIS overlay as originally recommended by
`research_papers.md` — rejected because the source has no AIS and adding one changes the published
biophysics.

**Task types**: `code-reproduction` (matches `task.json`). Per its planning guidance: preserve the
source's biophysical parameters verbatim, document every deviation, and validate against the paper's
headline quantitative result (DSI ~0.39 correlated, DSI ~0.25 uncorrelated) before claiming port
success.

## Cost Estimation

Total: **$0.00**. No paid external services are used. NEURON compilation and simulation run on the
local Windows workstation (same as t0008, t0020, t0022). No API calls, no remote compute. The
240-trial 12-angle sweep took ~9 minutes of wall time in t0008 on this machine; de Rosenroll's
AR(2)-noise driver is likely to be ~2-4x slower per trial, so budget ~20-35 minutes for the
correlated-condition 12-angle sweep and a similar amount for the 8-direction + uncorrelated
conditions. Project budget is untouched.

## Step by Step

### Milestone 1: Library scaffold and source import

1. **Create the library asset folder.** Create
   `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/` with
   subdirectories `sources/` and `code/`. Copy `run_nrnivmodl.cmd` from
   `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/run_nrnivmodl.cmd` into the
   new library root. Satisfies REQ-1 (scaffold).

2. **Clone the de Rosenroll repository into `sources/`.** Use
   `git clone https://github.com/geoffder/ds-circuit-ei-microarchitecture.git` into a temp dir, then
   copy `RGCmodelGD.hoc` and the `mechanisms/` subtree (containing `HHst_noiseless.mod`,
   `cadecay.mod`, `Exp2NMDA.mod`) into `sources/`. Do not include the upstream `.git` folder or
   `README.md` from the source repo (keep those in `sources/UPSTREAM_NOTES.md` as a short provenance
   file instead, including Zenodo DOI `10.5281/zenodo.17666158` and the commit hash that was
   imported). Satisfies REQ-1 (sources).

3. **Compile MOD files into `nrnmech.dll`.** From a Windows shell in `sources/`, run
   `cmd /c run_nrnivmodl.cmd`. Expected output: `nrnmech.dll` lives next to the `.mod` sources,
   `stderr.txt` is empty except for nrnivmodl banners. If the compile fails, log the error to
   `intervention/mod_compile_failure.md` and halt. Satisfies REQ-1 (compiled mechanism).

### Milestone 2: NEURON bootstrap and driver code

4. **Write `code/constants.py`.** Single flat module. Include all simulation and biophysical
   constants from [dsMicro-GH] code (authoritative, not paper-text): `CELSIUS_DEG_C = 36.9`,
   `DT_MS = 0.1`, `TSTOP_MS = 1000`, `V_INIT_MV = -65`, `AP_THRESHOLD_MV = -10`,
   `RA_OHM_CM = 100.0`, `CM_UF_CM2 = 1.0`, `GLEAK_S_CM2 = 5e-5`, `ELEAK_MV = -60.0`,
   `GBAR_NA_SOMA_MS_CM2 = 150`, `GBAR_NA_PRIMARY_MS_CM2 = 200`, `GBAR_NA_DISTAL_MS_CM2 = 30`,
   `GBAR_K_SOMA_MS_CM2 = 35`, `GBAR_K_PRIMARY_MS_CM2 = 40`, `GBAR_K_DISTAL_MS_CM2 = 25`,
   `ACH_TAU1_MS = 0.5`, `ACH_TAU2_MS = 6.0`, `ACH_EREV_MV = 0.0`, `ACH_GMAX_PS = 140.85`,
   `GABA_TAU1_MS = 0.5`, `GABA_TAU2_MS = 35.0`, `GABA_EREV_MV = -60.0`, `GABA_GMAX_PS = 450.72`,
   `GABA_SCALE = 1.8`, `NMDA_TAU1_MS = 2.0`, `NMDA_TAU2_MS = 80.0`, `NMDA_GMAX_PS = 140.85`,
   `CA_DECAY_TAU_MS = 10.0`, `AR2_PHI = (0.9, -0.1)`, `AR2_CROSS_CORR_RHO = 0.6`,
   `AMB_DECAY_TAU_UM = 27.0`, `SAC_SOMA_MIN_OFFSET_UM = 30.0`, `BAR_VELOCITY_UM_PER_MS = 1.0`,
   `BAR_WIDTH_UM = 250`, `ANGLES_8DIR_DEG = (0, 45, 90, 135, 180, 225, 270, 315)`,
   `ANGLES_12ANG_DEG = tuple(range(0, 360, 30))`, `N_TRIALS_PER_ANGLE = 20`. Also define paper-text
   alternatives (`RA_OHM_CM_PAPER_TEXT = 200.0`, etc.) as sensitivity-sweep constants but do not use
   them in the main driver. Satisfies REQ-1.

5. **Write `code/build_cell.py`.** Mirror the t0008 layout. Functions: `load_neuron()` (set
   `NEURONHOME`, `h.nrn_load_dll(<sources>/nrnmech.dll)`, source `stdrun.hoc`);
   `_sources_dir_hoc_safe()` (forward-slash path builder); `build_de_rosenroll_dsgc() -> h`
   (`h.chdir(_sources_dir_hoc_safe())`, `h.load_file("RGCmodelGD.hoc")`, fire the model's
   initialization); `apply_params(h, *, seed: int) -> None` (set `celsius`, `dt`, `tstop`, `v_init`,
   passive properties Ra/cm/gleak/eleak, active densities `gbar_Na`, `gbar_K` per compartment class,
   synaptic conductances); `@dataclass(frozen=True, slots=True) class SacVaricosity` with
   `soma_id: int`, `locx_um: float`, `locy_um: float`, `ach_gmax_ps: float`, `gaba_gmax_ps: float`;
   `read_varicosities(h) -> list[SacVaricosity]`; `get_cell_summary(h) -> CellSummary` with
   `n_sections: int`, `total_length_um: float`, `n_varicosities: int`. Satisfies REQ-1.

6. **Write `code/ar2_noise.py`.** Implements the AR(2) correlated release-rate noise process.
   Functions:
   `generate_ar2_process(*, n_samples: int, phi: tuple[float, float], rho: float, seed: int) -> np.ndarray`
   returns an `(n_samples, 2)` array of [ach_rate, gaba_rate] with AR(2) temporal structure and
   cross-channel correlation `rho`. Use `np.random.default_rng(seed)` for reproducibility. Include a
   self-test in `__main__` that validates the empirical auto-correlation matches `phi` and the
   cross-correlation peak matches `rho` to within 0.05. Satisfies REQ-1 (AR(2) noise model).

7. **Write `code/run_tuning_curve.py`.** Main driver. Signatures:
   `run_one_trial(*, h, pairs: list[SacVaricosity], angle_deg: float, trial_seed: int, correlated: bool) -> float`
   returns the somatic firing rate in Hz (threshold-crossings at -10 mV over the 1000 ms window);
   `sweep(*, h, angles: tuple[float, ...], n_trials: int, correlated: bool, output_csv: Path) -> None`
   writes the canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV. Conditions: correlated
   (normal `rho = 0.6`) and uncorrelated (`rho = 0.0`, matching the AMB / decorrelation
   intervention). A `main()` entry point runs four sweeps: (1) 8-direction correlated ->
   `data/tuning_curves_8dir_correlated.csv`; (2) 8-direction uncorrelated ->
   `data/tuning_curves_8dir_uncorrelated.csv`; (3) 12-angle correlated ->
   `data/tuning_curves_12ang_correlated.csv` (this is the primary project-comparison curve); (4)
   12-angle uncorrelated -> `data/tuning_curves_12ang_uncorrelated.csv`. Satisfies REQ-3, REQ-4.

8. **Copy the BIP-position guard pattern.** Not applicable — the de Rosenroll source does not use
   the Poleg-Polsky `placeBIP()` mechanism. Skip the copy-in from t0020. Noted for traceability.

### Milestone 3: Scoring and validation gates

9. **Write `code/score_envelope.py`.** Copy the pattern from
   `tasks/t0008_port_modeldb_189347/code/score_envelope.py` (approx. 100 lines). Adapt the input CSV
   constant to point to `data/tuning_curves_12ang_correlated.csv`. Import
   `score, METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY, METRIC_KEY_RMSE` from
   `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`. Serialize
   `data/score_report.json` (full 13-field debug dump) and `results/metrics.json` (four registered
   metric keys). Also compute a custom `de_rosenroll_dsi_correlated_8dir` and
   `de_rosenroll_dsi_uncorrelated_8dir` from the 8-direction CSVs (via `compute_dsi` from the same
   library) and include both in `results/metrics.json` under task-local keys for REQ-5 tracking.
   Satisfies REQ-3, REQ-4, REQ-5.

10. **[CRITICAL] Preflight validation gate (small-scale sanity run).** Before launching the full
    four-sweep run, run `run_tuning_curve.py --limit 3` (3 trials per angle, 8-direction correlated
    only) and inspect `data/tuning_curves_8dir_correlated_preflight.csv`. The trivial baseline for
    pass is DSI > 0.1 (clearly non-random); if DSI < 0.05, the pipeline is broken — halt, inspect
    individual-trial spike counts at each angle, and debug before proceeding. Expected preflight
    wall time: ~45 seconds. This step is **CRITICAL** because running the full ~30 minute sweep with
    a broken noise process or miswired driver wastes the whole implementation budget. Satisfies
    REQ-3 (preflight).

11. **[CRITICAL] Full four-condition sweep.** Run `code/run_tuning_curve.py` (no `--limit`) to
    execute all four sweeps (8-direction x {correlated, uncorrelated} and 12-angle x {correlated,
    uncorrelated}), writing the four CSVs under `data/`. Expected wall time: ~30-50 minutes total.
    Satisfies REQ-3, REQ-4.

12. **Run scoring.** Run `code/score_envelope.py` to generate `data/score_report.json` and
    `results/metrics.json`. Expected: `results/metrics.json` contains the four registered metric
    keys (DSI, HWHM, RELIABILITY, RMSE) from the 12-angle correlated CSV, plus task-local keys
    `de_rosenroll_dsi_correlated_8dir` and `de_rosenroll_dsi_uncorrelated_8dir`. Satisfies REQ-3,
    REQ-5.

13. **[CRITICAL] Port-fidelity validation gate.** Confirm the port recovers the paper's headline
    numbers. Pass: `de_rosenroll_dsi_correlated_8dir` in `[0.30, 0.50]` (paper target 0.39) and
    `de_rosenroll_dsi_uncorrelated_8dir` in `[0.18, 0.35]` (paper target 0.25), with the
    correlated-to-uncorrelated ratio showing a drop of at least 20 percent. If either fails, log the
    observed values into `intervention/port_fidelity_miss.md` with the hypothesized cause (noise
    process, synaptic scaling, parameter mismatch) and proceed to the results step anyway — report
    the miss as a first-class experimental finding. Satisfies REQ-5.

14. **Generate tuning-curve plots.** Run
    `uv run python -m tasks.t0011_tuning_curve_viz_library.code.tuning_curve_viz_cli --input data/tuning_curves_12ang_correlated.csv --output results/images/tuning_curve_12ang.png --kind polar`.
    Repeat for the 8-direction correlated CSV to `results/images/tuning_curve_8dir.png`. Expected:
    two PNG files in `results/images/`. Satisfies REQ-3, REQ-4 (visualization).

## Remote Machines

None required. NEURON compiles and simulates locally on the Windows workstation. No GPU, no vast.ai
provisioning. `setup-machines` and `teardown` steps are already marked `skipped` in
`step_tracker.json`.

## Assets Needed

* **`modeldb_189347_dsgc` library** (from t0008) — only for the `run_nrnivmodl.cmd` wrapper
  pattern and the Windows NEURON bootstrap template; not imported as Python.
* **`tuning_curve_loss` library** (from t0012) — imported as Python via
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`. No adaptation.
* **`tuning_curve_viz` library** (from t0011) — imported via CLI for plots.
* **`10.1016_j.celrep.2025.116833` paper asset** (registered in this task at step 5). Primary
  source.
* **[dsMicro-GH] external repository** `geoffder/ds-circuit-ei-microarchitecture` at Zenodo DOI
  `10.5281/zenodo.17666158`. MIT-licensed. Cloned into `sources/` at step 2.
* **t0004 target tuning curve** (via `tuning_curve_loss` default target resolution). Consumed by
  `score_envelope.py`.

## Expected Assets

Matches `task.json` `expected_assets: {"library": 1, "paper": 1}`:

* **Library**: `de_rosenroll_2026_dsgc` (v0.1.0) — NEURON-based DSGC port with 341-section
  morphology from `RGCmodelGD.hoc`, `HHst_noiseless` Na/K channels on soma and primary dendrites,
  Exp2Syn / Exp2NMDA synaptic inputs, AR(2) correlated release-rate noise. Includes `sources/*.hoc`,
  `sources/*.mod`, `sources/nrnmech.dll`, `code/*.py`, `details.json`, `description.md`,
  `run_nrnivmodl.cmd`.
* **Paper**: `10.1016_j.celrep.2025.116833` (already on disk, registered by step 5). Cell Reports,
  2026\.

## Time Estimation

* Research: already done (~45 minutes across steps 4-6).
* Implementation (steps 1-14 above): ~4-6 hours of active work.
  * Library scaffold + source import: ~20 minutes.
  * MOD compile: ~5 minutes.
  * Python code (constants, build_cell, ar2_noise, run_tuning_curve, score_envelope): ~2-3 hours.
  * Preflight validation run: ~1 minute.
  * Full four-condition sweep: ~30-50 minutes wall time.
  * Scoring + plots: ~10 minutes.
  * Library `details.json` + `description.md`: ~15 minutes.
  * Debugging buffer: ~60 minutes.
* Total wall time from implementation step start to step 14 completion: **~5-7 hours**.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| MOD compile fails on Windows (nrnivmodl path mangling) | Medium | Blocking | Reuse t0008's `run_nrnivmodl.cmd` exactly; if it still fails, fall back to compiling under WSL and copying `libnrnmech.so` + recompiling as DLL via MSYS, log to `intervention/mod_compile_failure.md` |
| AR(2) noise implementation mismatches paper (phi, rho, cross-correlation structure) | Medium | Undermines REQ-5 | Add a standalone unit test in `code/test_ar2_noise.py` that verifies empirical auto-correlation within 0.05 of `phi` and cross-correlation peak within 0.05 of `rho`; if the test fails, debug before using in the driver |
| DSI port-fidelity miss (correlated < 0.30 or uncorrelated > 0.35) | Medium | Does not block, but weakens the port | Record in `intervention/port_fidelity_miss.md` with hypothesized cause; still emit the results and document the gap in `results_detailed.md` as a first-class finding |
| Peak firing rate below t0004 envelope (40-80 Hz) | High | Expected; do not chase | Historically both t0020 (14.85 Hz) and t0022 (~15 Hz) missed the same envelope with correct DSI; frame as a known lineage-wide gap and report in `results_detailed.md` |
| 30+ minute sweep hangs or crashes mid-run | Low | Lose one run's work | Write CSVs incrementally (one row per trial), not at the end; resumption script can skip completed (angle, seed) pairs |
| Briggman 2011 connectome varicosity placement data is not ported into `RGCmodelGD.hoc` | Medium | Subcellular DSI signal may be weak | The `.hoc` file imported from [dsMicro-GH] already includes connectome-derived synapse coordinates; verify at step 5 by counting varicosities and confirming >= 200 unique `(locx, locy)` positions |
| Paper-code parameter disagreements confuse reviewers | Low | Documentation burden | Record both sets in `constants.py` with inline comments; `research_internet.md` already flags this; `results_detailed.md` will note the decision |

## Verification Criteria

* **Library structural check**:
  `uv run python -m arf.scripts.verificators.verify_library_asset t0024_port_de_rosenroll_2026_dsgc de_rosenroll_2026_dsgc`
  passes with zero errors. Confirms REQ-1.
* **Paper asset check**:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/` contains
  `details.json`, `summary.md`, and `files/`; all required fields populated per
  `meta/asset_types/paper/specification.md` v3. Confirms REQ-2 (already verified in step 5).
* **Tuning-curve CSV integrity**:
  `ls tasks/t0024_port_de_rosenroll_2026_dsgc/data/tuning_curves_*.csv` lists exactly four files;
  each has the columns `angle_deg, trial_seed, firing_rate_hz` and 240 rows (12 angles x 20 trials)
  for the 12-angle CSVs or 160 rows (8 directions x 20 trials) for the 8-direction CSVs. Confirms
  REQ-3, REQ-4.
* **Score report check**:
  `cat tasks/t0024_port_de_rosenroll_2026_dsgc/data/score_report.json | jq '.loss_scalar'` emits a
  non-null float; `.dsi`, `.hwhm_deg`, `.reliability`, `.rmse` are all populated. Confirms REQ-3.
* **Port-fidelity gate**:
  `cat tasks/t0024_port_de_rosenroll_2026_dsgc/results/metrics.json | jq '.de_rosenroll_dsi_correlated_8dir, .de_rosenroll_dsi_uncorrelated_8dir'`
  emits two floats; correlated value is in `[0.30, 0.50]`, uncorrelated value is in `[0.18, 0.35]`,
  and the fractional drop `(corr - uncorr) / corr` is at least 0.20. Confirms REQ-5.
* **Plots exist**: `ls tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_*.png`
  lists at least two PNG files. Confirms REQ-3, REQ-4.
* **Requirement coverage cross-check**: every `REQ-*` ID from the Task Requirement Checklist appears
  in at least one step of the Step by Step section (grep-able); the eventual
  `results/results_detailed.md` also references each `REQ-*` ID. Confirms full traceability.
