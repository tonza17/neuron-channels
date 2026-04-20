# ✅ Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0020_port_modeldb_189347_gabamod` |
| **Status** | ✅ completed |
| **Started** | 2026-04-20T19:13:31Z |
| **Completed** | 2026-04-20T20:35:00Z |
| **Duration** | 1h 21m |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source suggestion** | `S-0008-02` |
| **Task types** | `code-reproduction` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 1 library |
| **Step progress** | 10/15 |
| **Task folder** | [`t0020_port_modeldb_189347_gabamod/`](../../../tasks/t0020_port_modeldb_189347_gabamod/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0020_port_modeldb_189347_gabamod/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0020_port_modeldb_189347_gabamod/task_description.md)*

# Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Motivation

This task implements suggestion **S-0008-02** raised by t0008. The existing port
(`modeldb_189347_dsgc`, library asset produced by t0008) reaches **DSI 0.316 / peak 18.1 Hz**,
well below the Poleg-Polsky & Diamond 2016 envelope (**DSI 0.70-0.85, peak 40-80 Hz**). The
shortfall is not a bug in the port — it comes from t0008's choice to substitute a
spatial-rotation proxy for the paper's native direction-selectivity protocol.

In the original ModelDB 189347 driver the direction-selectivity test does not rotate a
stimulus. Instead it runs the *same* synaptic input pattern under two different parameter
settings of the inhibitory `gabaMOD` scalar:

* **Preferred direction (PD)**: `gabaMOD = 0.33` — weak inhibition, strong spike output.
* **Null direction (ND)**: `gabaMOD = 0.99` — strong inhibition, suppressed spike output.

The DSI emerges from the PD/ND firing-rate ratio. t0008's `run_one_trial` implementation kept
`gabaMOD` fixed and instead rotated BIP synapse coordinates around the soma, which
approximates direction tuning geometrically but does not exercise the inhibition-modulation
mechanism the paper relies on. This task adds a **second** library asset that runs the paper's
native protocol so the project can quote a fair reproduction number against the published
envelope, and so subsequent sensitivity-analysis tasks can manipulate `gabaMOD` directly.

The rotation-proxy port from t0008 stays unchanged and remains valid for direction-tuning
curves that need an explicit angle axis (e.g. tuning-curve fitting, HWHM measurement). The two
protocols are kept side by side so future tasks can pick whichever matches their question.

## Scope

Produce a **new sibling library asset** with proposed id `modeldb_189347_dsgc_gabamod`. The
new asset shares the MOD files and `RGCmodel.hoc` skeleton with `modeldb_189347_dsgc` (do not
vendor a second copy of the source HOC/MOD — load them via the path conventions established in
t0008) and replaces only the per-angle BIP rotation in `run_one_trial` with a two-condition
`gabaMOD` sweep.

In scope:

* New driver script (e.g. `code/run_gabamod_sweep.py`) that runs N PD trials and N ND trials,
  varying only the `gabaMOD` scalar between the two conditions.
* New tuning-curve CSV with schema `(condition, trial_seed, firing_rate_hz)` instead of
  t0008's `(angle_deg, trial_seed, firing_rate_hz)`. `condition` takes values `PD` and `ND`.
* Two-point envelope gate that scores the run against the published envelope using DSI from
  the PD/ND ratio and peak from the PD condition (HWHM and null are read from the
  rotation-proxy port in the comparison note — they have no analogue in the two-point
  protocol).
* Library asset metadata (`details.json`, `description.md`) registering the new asset under
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/`.

Out of scope:

* Re-deriving the underlying NEURON model. The HOC/MOD files used by t0008 are reused
  unchanged.
* Sensitivity sweeps over `gabaMOD` values other than the canonical 0.33 / 0.99 pair (proposed
  as follow-up suggestions).
* Re-fitting tuning curves with a Gaussian or von Mises function — the two-point protocol does
  not produce an angle axis.

## Approach

The work is a single implementation step plus a comparison note:

1. Initialise the new library asset folder and copy the t0008 driver as the starting point.
2. Refactor `run_one_trial` to accept a `gabaMOD` value as a keyword argument and remove the
   BIP `locx` rotation. The BIP synapse stays at its canonical position; only the inhibitory
   scalar changes between conditions.
3. Wire a new top-level driver that loops over `(condition, trial_seed)` pairs:
   * `condition = "PD"` → set `gabaMOD = 0.33` on every inhibitory point process before the
     run.
   * `condition = "ND"` → set `gabaMOD = 0.99` similarly.
   * `trial_seed` varies the RNG seed used for synaptic-release noise so each repeat is
     independent.
4. Write `tuning_curves.csv` with one row per `(condition, trial_seed)`. Default sweep: **2
   conditions × 20 trials = 40 trials per run**. Total runtime estimate: ~1.5 minutes on the
   local Windows workstation (240-trial t0008 run took ~9 minutes; 40 trials scales linearly).
5. Score the CSV with the t0012 `tuning_curve_loss` scorer using a **two-point envelope
   gate**:
   * Compute mean firing rate for PD and ND across trials.
   * `DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)`.
   * `peak = mean_PD`.
   * Pass = DSI in [0.70, 0.85] AND peak in [40, 80] Hz; fail otherwise.
6. Write `score_report.json` and a comparison table in `results/results_detailed.md` showing:
   * Rotation-proxy port (t0008): DSI / peak / null / HWHM / reliability.
   * gabaMOD-swap port (t0020): DSI / peak (null and HWHM marked N/A — no angle axis).

## Deliverables

* **New library asset**:
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/` with
  `details.json`, `description.md`, and the gabaMOD-swap driver code under
  `assets/library/modeldb_189347_dsgc_gabamod/code/`.
* **Tuning curves CSV**: `data/tuning_curves.csv` with columns `(condition, trial_seed,
  firing_rate_hz)`.
* **Score report**: `results/score_report.json` produced by the t0012 scorer with the
  two-point envelope gate, including DSI, peak, pass/fail, and the envelope used.
* **Comparison note**: a section in `results/results_detailed.md` quantifying how the
  gabaMOD-swap port differs from the t0008 rotation-proxy port on DSI, peak, null, and HWHM.
  The note must be embedded in `results_detailed.md`, not a separate file, so it shows up in
  the materialized overview.
* **Charts**: bar chart of mean firing rate by condition (PD vs ND, with per-trial scatter)
  saved to `results/images/` and embedded in `results_detailed.md`.

## Dependencies

* `t0008_port_modeldb_189347` — provides the source HOC/MOD layout, `run_one_trial` template,
  and the rotation-proxy baseline numbers used in the comparison note.
* `t0012_tuning_curve_scoring_loss_library` — provides the scorer library used to compute DSI,
  apply the envelope gate, and write `score_report.json`.

## Compute and Budget

* No remote machines. Runs locally on the Windows workstation that t0008 used. NEURON 8.2.7 +
  NetPyNE 1.1.1 are already installed.
* Estimated wall-clock: **~1.5 minutes** for the canonical 40-trial sweep (2 conditions × 20
  trials). t0008's 240-trial sweep took ~9 minutes; this sweep is 6× smaller.
* Estimated cost: **$0** (local compute, no paid API calls).

## Output Specification

CSV schema (`data/tuning_curves.csv`):

| Column | Type | Description |
| --- | --- | --- |
| `condition` | string | `PD` or `ND` |
| `trial_seed` | int | RNG seed for synaptic-release noise on this trial |
| `firing_rate_hz` | float | Mean spike rate over the stimulus window for this trial |

Score report schema (`results/score_report.json`):

* `protocol`: `"gabamod_swap"`
* `dsi`: float (PD/ND ratio)
* `peak_hz`: float (mean PD firing rate)
* `gate`: object with `dsi_min`, `dsi_max`, `peak_min`, `peak_max`, `passed` (bool)
* `n_trials_per_condition`: int

Comparison table (`results/results_detailed.md`):

| Metric | Rotation proxy (t0008) | gabaMOD swap (t0020) | Envelope |
| --- | --- | --- | --- |
| DSI | 0.316 | <measured> | 0.70-0.85 |
| Peak (Hz) | 18.1 | <measured> | 40-80 |
| Null (Hz) | 9.4 | N/A | <10 |
| HWHM (deg) | 82.81 | N/A | 60-90 |
| Reliability | 0.991 | <measured> | high |

## Verification

* `data/tuning_curves.csv` has exactly `2 * n_trials_per_condition` rows with the canonical
  schema.
* `results/score_report.json` validates against the t0012 scorer's schema.
* Library asset folder passes the library-asset verificator (mirroring the layout used by
  `modeldb_189347_dsgc` in t0008).
* Comparison table in `results_detailed.md` quotes the t0008 numbers verbatim from
  `tasks/t0008_port_modeldb_189347/results/results_summary.md` (no rounding drift).

## Risks and Fallbacks

* **gabaMOD scalar not exposed at the Python level**: if the t0008 port wraps `gabaMOD` inside
  a HOC-only context that is not directly settable from Python, the implementation may need to
  set it via `h.gabaMOD = value` as a global before instantiating the inhibitory point
  processes, or reach into each `inh_syn` object after instantiation. Either path is
  straightforward; flag in the implementation step log if a HOC patch is needed.
* **Two-point gate too permissive**: if the run produces a DSI inside the envelope but spike
  counts are unrealistically low (e.g. peak < 5 Hz), record this in the limitations section.
  The envelope is necessary but not sufficient — a follow-up suggestion can add a per-trial
  spike-count floor.
* **Driver divergence from rotation-proxy port**: the new driver must not silently
  re-introduce the `locx` rotation. The implementation step must include an assertion that BIP
  `locx` stays at its canonical value across all trials.

## Cross-references

* Source suggestion: **S-0008-02** (active, high priority, raised by t0008).
* Source paper: Poleg-Polsky & Diamond 2016, ModelDB 189347 (DOI
  `10.1016/j.neuron.2016.02.013`).
* Sibling library asset: `modeldb_189347_dsgc` from t0008 (rotation-proxy port).
* Scorer dependency: `tuning_curve_loss` library from t0012.

</details>

## Metrics

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.7837837837837838** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [ModelDB 189347 DSGC Port -- gabaMOD-swap protocol](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/) | [`description.md`](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/description.md) |

## Suggestions Generated

<details>
<summary><strong>Excitation-side sensitivity sweep under gabaMOD-swap to close the
25 Hz peak-firing-rate gap</strong> (S-0020-01)</summary>

**Kind**: experiment | **Priority**: high

Under the native gabaMOD-swap protocol, DSI (0.7838) sits inside the [0.70, 0.85] envelope but
PD peak (14.85 Hz) is 25.15 Hz below the 40 Hz floor. Protocol is now ruled out, so the
shortfall must live on the excitation side. Run a factorial sweep over (a) BIP synapse count
{88, 177, 354}, (b) excMOD on AMPA+NMDA in {0.5, 1.0, 1.5, 2.0, 3.0}, (c) stimulus drive
{baseline, +50%, +100%}, holding gabaMOD at the 0.33/0.99 PD/ND pair. Report the smallest
config shift that moves peak into [40, 80] Hz without dragging DSI outside [0.70, 0.85].
Distinct from S-0008-04 (sweeps all parameters including GABA side under the rotation-proxy
protocol); this is excitation-only under the native driver, addressable only now that t0020
localised the gap. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Reproduce Poleg-Polsky 2016 Fig 1D/H subthreshold validation
targets (PSP amplitude, NMDAR slope angle)</strong> (S-0020-02)</summary>

**Kind**: evaluation | **Priority**: high

compare_literature.md flags that the paper reports concrete subthreshold validation targets
that this task did not measure: PD NMDAR-mediated PSP component 5.8 +/- 3.1 mV and ND 3.3 +/-
2.8 mV (Fig 1D, n=19), and NMDAR multiplicative scaling slope angle 62.5 +/- 14.2 deg (Fig 1H,
additive baseline 45 deg). Extend the gabaMOD-swap driver to record somatic whole-cell voltage
traces (v_soma, not just spike count) across the 40-trial sweep, compute (1) the peak PSP
amplitude in a 0-200 ms post-stimulus window per condition and (2) the slope-angle regression
over a scan of AMPA vs NMDA drive ratios, then gate each against the paper's n=19 mean +/- SD
intervals. This turns a single spike-output check into a multi-level subthreshold validation
that exercises the cell's passive and NMDA-block biophysics independently of spike
thresholding. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Intermediate-gabaMOD sensitivity sweep to map the PD-ND transition
curve</strong> (S-0020-03)</summary>

**Kind**: experiment | **Priority**: medium

The canonical protocol uses only the two endpoints gabaMOD = 0.33 (PD) and 0.99 (ND).
Task_description Scope explicitly deferred intermediate values as follow-up work. Run 20
trials per condition at gabaMOD in {0.20, 0.33, 0.50, 0.66, 0.83, 0.99} and plot firing rate
vs gabaMOD plus DSI computed as (rate_at_0.33 - rate_at_X)/(rate_at_0.33 + rate_at_X).
Outputs: (1) a firing-rate-vs-gabaMOD curve that shows whether the 0.33 -> 0.99 transition is
sigmoidal, threshold-like, or linear; (2) the critical gabaMOD value at which DSI crosses 0.5
(useful for later calibration); (3) a CSV with schema (gabamod, trial_seed, firing_rate_hz).
Probes whether the paper's two-point choice lies on a plateau or a steep-response region of
the inhibition axis, directly informing the inhibition-strength free parameter for later
optimisation. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Extend tuning_curve_loss with a two-point (PD/ND) scoring API to
make t0012 usable under the native protocol</strong> (S-0020-04)</summary>

**Kind**: library | **Priority**: medium

research_code.md records that t0012's high-level score() entry point rejects the two-condition
CSV because its loader's _validate_angle_grid requires exactly 12 angles on a 30-degree
spacing. t0020 worked around this by re-implementing the DSI formula inline in
score_envelope.py. Every future gabaMOD-swap task (including S-0020-01 and S-0020-03 above)
will hit the same wall. Add a score_two_point(pd_rates: np.ndarray, nd_rates: np.ndarray, *,
dsi_envelope, peak_envelope) -> TwoPointScore API to tuning_curve_loss that returns DSI, mean
PD, mean ND, per-condition stderr, gate.passed, plus optional per-trial CIs via bootstrap.
Keep the 12-angle score() untouched; the new API is an additional entry point. Register it in
the tuning_curve_loss library details.json entry_points. Recommended task types:
write-library.

</details>

<details>
<summary><strong>Add a per-trial spike-count floor to the two-point envelope gate to
catch biologically implausible passes</strong> (S-0020-05)</summary>

**Kind**: evaluation | **Priority**: medium

Plan Risks & Fallbacks explicitly anticipated this scenario: DSI can land inside the envelope
while absolute firing rates stay unrealistically low (t0020 recorded DSI 0.7838 / peak 14.85
Hz exactly here). The current gate checks (mean_PD in [40, 80] Hz, DSI in [0.70, 0.85]) but
does not enforce biological plausibility at the trial level: the gate could pass with, say,
one trial firing 80 Hz and nineteen firing 0 Hz. Extend the envelope gate (in
tuning_curve_loss or the t0020 scorer) to add a trial-level floor: require that at least
N_pd_pass PD trials fire above a biological minimum threshold (e.g., 5 Hz). Report the
per-trial floor result alongside the mean-based envelope. Rerun scoring over t0020's existing
40-trial CSV to verify the new gate flags the current run as failed on the floor (baseline
expectation). Recommended task types: write-library, experiment-run.

</details>

<details>
<summary><strong>Trial-count power analysis for the PD/ND DSI estimator (bootstrap
CI vs N_trials)</strong> (S-0020-06)</summary>

**Kind**: evaluation | **Priority**: medium

t0020 reports DSI 0.7838 from 20 trials per condition but quotes no confidence interval.
Before launching sensitivity sweeps (S-0020-01, S-0020-03), future tasks need to know how many
trials per condition are needed to resolve, say, a 0.05-DSI difference at 95% CI. Compute
bootstrap 95% CIs on DSI for N_trials per condition in {5, 10, 20, 40, 80} by resampling with
replacement (10,000 resamples) from a single long run (80 trials per condition, reusing
run_gabamod_sweep.py with --n-trials 80). Output: (1) a CSV
trial_count,dsi_mean,dsi_ci_low,dsi_ci_high,peak_mean,peak_ci_low,peak_ci_high; (2) a plot of
DSI CI width vs trial count; (3) a recommended N_trials for each sensitivity-analysis budget
tier. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Extend t0011 response-visualisation library with a condition-based
(PD/ND) raster+PSTH plot</strong> (S-0020-07)</summary>

**Kind**: library | **Priority**: low

t0011's tuning_curve_viz library supports angle-based rasters (one column per angle) but the
two-condition CSV produced by t0020 has no angle axis; only the bar chart (plot_pd_vs_nd.py,
t0020 local code) currently visualises it. Extend t0011 with
plot_condition_raster_psth(spike_times_df, *, conditions=('PD','ND'), out_png) that draws a
two-column raster (one per condition) above a PSTH panel. Requires t0020 (or a follow-up) to
first record per-trial spike times (not just rates) from run_gabamod_sweep.py. Complements
S-0011-01 (angle-based raster on the rotation-proxy port); this is the condition-based
analogue for the native-protocol port. Once merged, back-apply to t0020's existing sweep to
produce a publication-quality raster. Recommended task types: write-library, experiment-run.

</details>

## Research

* [`research_code.md`](../../../tasks/t0020_port_modeldb_189347_gabamod/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0020_port_modeldb_189347_gabamod/results/results_summary.md)*

# Results Summary: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Summary

Built a new sibling library asset `modeldb_189347_dsgc_gabamod` that drives the Poleg-Polsky &
Diamond 2016 DSGC under the paper's native two-condition `gabaMOD` swap protocol (PD = 0.33,
ND = 0.99) instead of t0008's spatial-rotation proxy. The canonical 2 × 20 = 40-trial sweep
reproduces the direction-selectivity contrast (**DSI 0.7838** inside the literature envelope
**[0.70, 0.85]**) but the absolute firing rates remain depressed (**peak 14.85 Hz** vs
envelope **[40, 80] Hz**), so the combined two-point gate fails. This matches the Risk-3
scenario anticipated in the plan and is recorded as a genuine experimental finding, not an
implementation defect.

## Metrics

* **Direction Selectivity Index (DSI)**: **0.7838** — inside envelope [0.70, 0.85] ✓
* **Peak firing rate (mean PD)**: **14.85 Hz** — below envelope [40, 80] Hz ✗
* **Null firing rate (mean ND)**: **1.80 Hz**
* **PD firing rate stddev**: **1.59 Hz** across 20 trials
* **ND firing rate stddev**: **1.03 Hz** across 20 trials
* **Two-point envelope gate**: **failed** (DSI passes, peak fails)
* **vs t0008 rotation-proxy DSI (0.316)**: gabaMOD-swap DSI is **+0.468** higher — 2.48× the
  rotation-proxy value
* **Trials run**: 40 (20 PD + 20 ND), local runtime ~1.5 minutes on the Windows workstation

## Verification

* `verify_task_file.py` — PASSED (0 errors) at init-folders step
* `verify_task_dependencies.py` — PASSED (both t0008 and t0012 completed) at check-deps step
* `verify_library_asset.py` — N/A (script not present in `arf/scripts/verificators/`);
  structural validity confirmed manually: `details.json` has `spec_version "2"` and all
  required fields; `description.md` has YAML frontmatter, exceeds the 500-word minimum, and is
  flowmark-normalized
* Per-trial BIP-position assertion (REQ-3 critical guard) — PASSED across all 40 trials; BIP
  synapses stayed at baseline coordinates throughout, confirming the rotation logic was not
  silently re-engaged

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0020_port_modeldb_189347_gabamod/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0020_port_modeldb_189347_gabamod" ---
# Results Detailed: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Summary

Implemented a new sibling library asset `modeldb_189347_dsgc_gabamod` that drives the
Poleg-Polsky & Diamond 2016 DSGC cell under the paper's native two-condition `gabaMOD` swap
protocol: PD trials set `h.gabaMOD = 0.33` (weak inhibition) and ND trials set `h.gabaMOD =
0.99` (strong inhibition), keeping every BIP synapse at its canonical spatial position. The
canonical 2 × 20 = 40-trial sweep yielded **DSI 0.7838** (inside the literature envelope
[0.70, 0.85]) with **peak 14.85 Hz** (below the envelope [40, 80] Hz), so the combined
envelope gate fails. This is a genuine experimental finding consistent with Risk-3 in the plan
— the gabaMOD swap mechanism is clearly reproducing the direction-selectivity *contrast* seen
in the paper, but the absolute firing rates remain depressed, the same shortfall that
motivated this task in the first place. The rotation-proxy port from t0008 is unchanged and
remains valid for tuning-curve fitting.

## Methodology

### Machine specs

* Windows 11 Education (build 10.0.22631) workstation, the same machine t0008 used.
* Python 3.12 via `uv`, NEURON 8.2.7 + NetPyNE 1.1.1 (already installed from t0008).
* No remote compute, no GPU, no paid API calls.

### Runtime

* Implementation step started: 2026-04-20T19:37:29Z (prestep).
* Implementation step completed: 2026-04-20T20:05:00Z.
* Full sweep wall clock: ~85 seconds for 40 trials (well within the ~1.5 minute estimate; 6×
  faster than t0008's 240-trial sweep as expected).
* Full task (worktree creation through implementation completion): ~52 minutes.

### Protocol

1. **Cell build**: `build_dsgc()` imported from
   `tasks.t0008_port_modeldb_189347.code.build_cell` (registered via the t0008 library asset)
   — reuses the unchanged HOC/MOD skeleton and `apply_params()` canonical parameter block.
2. **Per-trial driver** (`run_one_trial_gabamod` in
   `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py`):
   * Apply canonical parameters via `apply_params(h)`.
   * **Override** `h.gabaMOD` to the condition-specific scalar (0.33 for PD, 0.99 for ND)
     *after* `apply_params` (which otherwise writes the canonical 0.33).
   * Assert each BIP synapse stays at its baseline `locx` — the per-trial rotation guard
     (REQ-3).
   * Seed the NEURON RNG with `trial_seed` for synaptic-release noise.
   * Run `h.finitialize(-65 mV)` + `h.continuerun(1000 ms)` and count threshold-crossings at
     the soma.
3. **Sweep** (`main` in `run_gabamod_sweep.py`): iterate over `(condition, trial_seed) ∈ {PD,
   ND} × range(1, 21)`; write one row per trial to `data/tuning_curves.csv` with schema
   `(condition, trial_seed, firing_rate_hz)`.
4. **Scoring** (`main` in `code/score_envelope.py`): read the CSV, compute `DSI = (mean_PD -
   mean_ND) / (mean_PD + mean_ND)` and `peak = mean_PD` inline (t0012's high-level `score()`
   rejects non-12-angle inputs; the formula is the same one t0012's `compute_dsi` uses
   internally). Gate against unwidened literature envelope (DSI ∈ [0.70, 0.85], peak ∈ [40,
   80] Hz) and write `results/score_report.json` + `results/metrics.json`.
5. **Chart** (`code/plot_pd_vs_nd.py`): bar chart of mean PD vs ND firing rate with per-trial
   scatter overlay, saved to `results/images/pd_vs_nd_firing_rate.png` at 200 DPI.
6. **Validation gate**: before the full sweep, ran `run_gabamod_sweep.py --limit 2 --n-trials
   1` (PD = 15 Hz, ND = 1 Hz, DSI ≈ 0.875), confirming the gabaMOD swap took effect before
   committing to the 40-trial sweep.

All CLI invocations wrapped via `uv run python -m arf.scripts.utils.run_with_logs`; command
logs live in `logs/commands/008..013_*.{json,stdout.txt,stderr.txt}`.

## Metrics Tables

### Headline metrics (two-point protocol)

| Metric | Value | Envelope | Inside? |
| --- | --- | --- | --- |
| Direction Selectivity Index | 0.7838 | [0.70, 0.85] | ✓ |
| Peak firing rate (mean PD, Hz) | 14.85 | [40, 80] | ✗ |
| Mean ND firing rate (Hz) | 1.80 | — | — |
| PD stddev (Hz, n=20) | 1.59 | — | — |
| ND stddev (Hz, n=20) | 1.03 | — | — |
| Gate passed | false | — | — |

### Comparison vs t0008 rotation-proxy (REQ-6)

| Metric | Rotation proxy (t0008) | gabaMOD swap (t0020) | Envelope | Notes |
| --- | --- | --- | --- | --- |
| DSI | 0.316 | **0.7838** | 0.70-0.85 | gabaMOD swap matches literature; rotation does not |
| Peak (Hz) | 18.1 | 14.85 | 40-80 | Both protocols depressed below envelope |
| Null (Hz) | 9.4 | N/A | < 10 | Two-point protocol has no angle axis |
| HWHM (deg) | 82.81 | N/A | 60-90 | No angle axis |
| Reliability | 0.991 | N/A | high | Not comparable across protocols |

The t0008 numbers are quoted verbatim from
`tasks/t0008_port_modeldb_189347/results/results_summary.md` with no rounding drift.

## Visualizations

![PD vs ND mean firing rate with per-trial
scatter](../../../tasks/t0020_port_modeldb_189347_gabamod/results/images/pd_vs_nd_firing_rate.png)

The bar chart shows mean PD vs ND firing rates (bars) with per-trial scatter overlay (dots).
PD trials cluster between 11-18 Hz; ND trials cluster between 0-4 Hz. The large, clean
separation of the two distributions is the direct visual evidence for the high DSI.

## Analysis

The headline result has two parts that must not be conflated:

1. **The gabaMOD swap mechanism works.** DSI 0.7838 from 40 trials is not a marginal pass — it
   sits squarely inside the literature envelope and is **2.48× t0008's rotation-proxy DSI
   (0.316)**. The PD vs ND contrast is large (~8× firing-rate ratio), reproducible across
   seeds (PD stddev 1.59 Hz on a mean of 14.85 Hz = 10.7% CV; ND stddev 1.03 Hz on a mean of
   1.80 Hz), and consistent with what the paper reports qualitatively.

2. **Absolute firing rates remain depressed.** Peak 14.85 Hz is well below the envelope [40,
   80] Hz. This is *not* the rotation-proxy shortfall — the gabaMOD swap is exactly the
   paper's native protocol. It means the depressed firing rate is intrinsic to the current
   port (same excitation gain, mechanism densities, synapse counts, or stimulus strength as
   t0008), *independent* of whether direction selectivity is induced by rotation or by gabaMOD
   swap.

This cleanly localises the gap: the two-point protocol rules out the rotation proxy as the
cause of the peak-rate shortfall, so any follow-up sensitivity sweep should target the
*excitation* side (BIP synapse count, `excMOD`, stimulus strength) rather than the inhibition
side.

## Examples

Examples are verbatim rows from `data/tuning_curves.csv` (schema
`condition,trial_seed,firing_rate_hz`). The dataset has 40 rows (20 PD + 20 ND). Each code
block below is the actual input/output of one or two trials: the *input* is the `(condition,
trial_seed)` pair that drives `run_one_trial_gabamod`, which sets `h.gabaMOD` to 0.33 (PD) or
0.99 (ND) and seeds the NEURON RNG with `trial_seed`; the *output* is the `firing_rate_hz`
column written to the CSV at the end of the 1-second stimulus window.

### Contrastive examples (same seed, both conditions)

These five pairs isolate the gabaMOD effect: the only thing that differs between the two rows
of each pair is `h.gabaMOD` (0.33 vs 0.99). Same cell, same BIP positions, same noise RNG
seed.

Example 1 — seed 1, trial-level DSI = (15-1)/(15+1) = **0.875**:

```csv
condition,trial_seed,firing_rate_hz
PD,1,15.000000
ND,1,1.000000
```

Example 2 — seed 5, trial-level DSI = (16-1)/(16+1) = **0.882**:

```csv
condition,trial_seed,firing_rate_hz
PD,5,16.000000
ND,5,1.000000
```

Example 3 — seed 8, trial-level DSI = (18-1)/(18+1) = **0.895** (strongest PD in the sweep):

```csv
condition,trial_seed,firing_rate_hz
PD,8,18.000000
ND,8,1.000000
```

Example 4 — seed 11, trial-level DSI = (16-1)/(16+1) = **0.882**:

```csv
condition,trial_seed,firing_rate_hz
PD,11,16.000000
ND,11,1.000000
```

Example 5 — seed 14, trial-level DSI = (15-0)/(15+0) = **1.000** (complete ND suppression,
ideal direction-selective trial):

```csv
condition,trial_seed,firing_rate_hz
PD,14,15.000000
ND,14,0.000000
```

Every contrastive pair independently shows direction selectivity. The effect is not an
artefact of trial averaging — it holds at the single-trial level too.

### Random examples (unbiased sample)

Example 6 — random sample from the middle of the sweep (seeds 2, 6, 12, 17, 20 picked before
inspecting values):

```csv
condition,trial_seed,firing_rate_hz
PD,2,11.000000
ND,6,3.000000
PD,12,14.000000
ND,17,1.000000
PD,20,14.000000
```

### Best PD trials (strongest peak firing)

Example 7 — the three highest PD trials in the sweep. Even the best (18 Hz) stays well below
the envelope floor of 40 Hz, reinforcing the peak-rate diagnosis in the Analysis section:

```csv
condition,trial_seed,firing_rate_hz
PD,8,18.000000
PD,16,17.000000
PD,5,16.000000
```

### Worst PD trials (where the depression is most pronounced)

Example 8 — the three lowest PD trials. Seed 2 at 11 Hz is the weakest PD in the sweep, yet is
still ~10× higher than the same-seed ND trial (1 Hz):

```csv
condition,trial_seed,firing_rate_hz
PD,2,11.000000
PD,7,12.000000
PD,10,13.000000
```

### Best ND trials (weakest null suppression)

Example 9 — the highest ND trial in the sweep. `gabaMOD = 0.99` still suppresses the matching
PD trial (seed 4, 14 Hz) down to 4 Hz; the 3.5× ratio is preserved even at the worst ND seed:

```csv
condition,trial_seed,firing_rate_hz
ND,4,4.000000
PD,4,14.000000
```

### ND cluster around mode

Example 10 — three clustered ND trials showing the typical null-direction firing rate of 1-3
Hz:

```csv
condition,trial_seed,firing_rate_hz
ND,6,3.000000
ND,9,3.000000
ND,13,3.000000
```

### Boundary case — complete null suppression

Example 11 — the only trial with zero spikes. Seed 14 shows that `gabaMOD = 0.99` is strong
enough to completely silence the cell under some noise realisations. The same-seed PD trial
fires 15 Hz, making this the ideal DSI = 1.0 pair used in Example 5:

```csv
condition,trial_seed,firing_rate_hz
ND,14,0.000000
```

### Validation-gate example (pre-sweep sanity check)

Example 12 — the `--limit 2 --n-trials 1` validation gate run before the full sweep. The log
lines below are extracted verbatim from
`logs/commands/010_run_gabamod_sweep_validation_gate.stdout.txt` and show the PD >> ND
contrast that confirmed the gabaMOD swap took effect before the 40-trial commit:

```text
[validation_gate] condition=PD trial_seed=1 firing_rate_hz=15.0
[validation_gate] condition=ND trial_seed=1 firing_rate_hz=1.0
[validation_gate] DSI = (15 - 1) / (15 + 1) = 0.875
[validation_gate] PASS: PD >> ND, proceeding to full sweep
```

## Verification

* `verify_task_file.py` — PASSED (0 errors) at init-folders step (log in
  `logs/steps/003_init-folders/verify_task_file.json`).
* `verify_task_dependencies.py` — PASSED at check-deps step; both `t0008_port_modeldb_189347`
  and `t0012_tuning_curve_scoring_loss_library` completed.
* `verify_library_asset.py` — N/A (script referenced by the plan's Verification Criteria does
  not exist in `arf/scripts/verificators/`). Structural validity was confirmed manually:
  `details.json` has `spec_version "2"` and all required fields (library_id, name, version,
  short_description, description_path, module_paths, entry_points, dependencies, categories,
  created_by_task, date_created); `description.md` has YAML frontmatter with `spec_version
  "2"`, exceeds the 500-word minimum (1541 words), and is flowmark-normalised.
* **Per-trial BIP-position assertion (REQ-3 critical guard)** — PASSED across all 40 trials.
  The driver asserts `h.RGC.BIPsyn[i].locx == baseline[i].bip_locx_um` for all `i` immediately
  before each `h.continuerun` call, guaranteeing the rotation logic was not silently
  re-engaged.
* **CSV schema check (REQ-4)** — PASSED. `data/tuning_curves.csv` has exactly 40 rows with
  header `condition,trial_seed,firing_rate_hz` and values in the expected ranges.
* **Validation gate** — PASSED. The `--limit 2 --n-trials 1` run produced PD = 15 Hz, ND = 1
  Hz (DSI ≈ 0.875), confirming the gabaMOD swap took effect before the full sweep.
* **Lint / type** — `ruff check --fix .`, `ruff format .`, and `mypy -p
  tasks.t0020_port_modeldb_189347_gabamod.code` all clean from the worktree root.

## Limitations

* **Peak firing rate below envelope** — the combined two-point envelope gate fails because
  `peak = 14.85 Hz` < 40 Hz. As anticipated by Risk-3 in the plan, this is a genuine finding:
  the gabaMOD swap reproduces the *contrast* but not the *absolute level*. The shortfall is
  now localised to the excitation side of the model rather than to the direction-selectivity
  protocol.
* **No angle axis** — the two-point protocol has no notion of angle, so `HWHM (deg)` and `Null
  (Hz)` are marked N/A in the comparison table. The t0008 rotation-proxy port remains the
  correct tool for tuning-curve fitting.
* **t0012 scorer not used at the API boundary** — the high-level `score()` entry point in the
  t0012 library enforces a 12-angle / 30-degree grid on input CSVs, which the two-point
  protocol cannot satisfy. The DSI formula is therefore computed inline in `score_envelope.py`
  using the same arithmetic `compute_dsi()` uses internally in t0012; the t0012 library is
  referenced in the description and is available for the envelope-widening approach if a
  future task wants it.
* **Single gabaMOD value per condition** — the sweep uses only the canonical 0.33 / 0.99 pair.
  Sensitivity over intermediate gabaMOD values is explicitly out of scope (proposed as a
  follow-up suggestion).
* **Per-trial stochasticity controlled only by seed** — noise realisations depend on the
  NEURON RNG; reproducibility is seed-controlled but sensitive to NEURON / numpy / OS version
  changes. The exact firing rates may drift between environments even with identical seeds.

## Files Created

* `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/details.json`
* `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/description.md`
* `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/code/.gitkeep`
* `tasks/t0020_port_modeldb_189347_gabamod/code/constants.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/paths.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/score_envelope.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/plot_pd_vs_nd.py`
* `tasks/t0020_port_modeldb_189347_gabamod/data/tuning_curves.csv` (40 rows + header, 2
  conditions × 20 trial seeds)
* `tasks/t0020_port_modeldb_189347_gabamod/results/score_report.json` (full two-point gate
  report)
* `tasks/t0020_port_modeldb_189347_gabamod/results/metrics.json` (registered metric key
  `direction_selectivity_index` only; other keys moved to `results_detailed.md` per
  task-results spec v8)
* `tasks/t0020_port_modeldb_189347_gabamod/results/costs.json` (zero-cost local-only task)
* `tasks/t0020_port_modeldb_189347_gabamod/results/remote_machines_used.json` (empty array)
* `tasks/t0020_port_modeldb_189347_gabamod/results/results_summary.md`
* `tasks/t0020_port_modeldb_189347_gabamod/results/results_detailed.md` (this file)
* `tasks/t0020_port_modeldb_189347_gabamod/results/images/pd_vs_nd_firing_rate.png` (200 DPI
  bar chart with per-trial scatter)
* `tasks/t0020_port_modeldb_189347_gabamod/logs/commands/008..013_*.{json,stdout.txt,stderr.txt}`
  (run_with_logs output for validation gate, full sweep, scorer, chart generator, and
  verification commands)
* Step logs under `tasks/t0020_port_modeldb_189347_gabamod/logs/steps/`

## Task Requirement Coverage

Task request (quoted from `task.json` and `task_description.md`):

> **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol.
>
> **Short description**: Reproduce Poleg-Polsky & Diamond 2016 DSGC direction selectivity using the
> paper's native gabaMOD scalar swap (PD=0.33, ND=0.99) instead of the spatial-rotation proxy used
> in t0008.
>
> **Long description (scope)**: Produce a new sibling library asset with proposed id
> `modeldb_189347_dsgc_gabamod`. The new asset shares the MOD files and RGCmodel.hoc skeleton with
> `modeldb_189347_dsgc` and replaces only the per-angle BIP rotation in `run_one_trial` with a
> two-condition gabaMOD sweep. Deliverables: (1) new library asset with gabaMOD-swap driver; (2)
> `tuning_curves.csv` under the new protocol; (3) `score_report.json` against the envelope; (4) a
> short comparison note in `results_detailed.md` quantifying how the gabaMOD-swap port differs from
> the rotation-proxy port on DSI/peak/null/HWHM.

Requirements from `plan/plan.md`:

* **REQ-1** — **Done**. Registered new library asset
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/` with
  `details.json` (spec_version "2", all required fields) and `description.md` (spec_version
  "2", YAML frontmatter, 1541 words). Evidence: files exist; manual structural validity check
  in the Verification section of this file (the planned `verify_library_asset.py` does not
  exist, which is recorded as an Issue in the implementation step log).

* **REQ-2** — **Done**. The new driver imports `build_dsgc`, `read_synapse_coords`,
  `apply_params`, and `get_cell_summary` from
  `tasks.t0008_port_modeldb_189347.code.build_cell` via the t0008 library asset. No `sources/`
  directory exists under the new asset; the HOC/MOD files are not vendored a second time.
  Evidence: `run_gabamod_sweep.py` import block; filesystem check that
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/sources/`
  does not exist.

* **REQ-3** — **Done**. `run_one_trial_gabamod` sets `h.gabaMOD = 0.33` for PD and 0.99 for
  ND, keeps BIP positions at baseline, and asserts per-trial that `h.RGC.BIPsyn[i].locx ==
  baseline[i].bip_locx_um` for all `i`. Evidence: assertion survived the full 40-trial sweep
  (no AssertionError in any of the `logs/commands/010_*.stderr.txt` or
  `logs/commands/011_*.stderr.txt` files).

* **REQ-4** — **Done**. `data/tuning_curves.csv` has exactly 40 rows with header
  `condition,trial_seed,firing_rate_hz`. Evidence: the file exists; `wc -l` shows 41 lines (1
  header \+ 40 data rows); the Examples section in this file quotes 20+ individual rows.

* **REQ-5** — **Done**. `results/score_report.json` contains `protocol: "gabamod_swap"`,
  `n_trials_per_condition: 20`, `dsi: 0.7838`, `peak_hz: 14.85`, `gate` object with `dsi_min`,
  `dsi_max`, `peak_min_hz`, `peak_max_hz`, `dsi_in_range: true`, `peak_in_range: false`,
  `passed: false`. Gate thresholds are the unwidened literature values [0.70, 0.85] and [40,
  80] Hz. Evidence: file exists at the expected path.

* **REQ-6** — **Done**. The `## Metrics Tables` section in this file includes the mandated
  comparison table with rows DSI / Peak / Null / HWHM / Reliability, quoting the t0008
  rotation-proxy numbers verbatim from
  `tasks/t0008_port_modeldb_189347/results/results_summary.md` (DSI 0.316, Peak 18.1 Hz, Null
  9.4 Hz, HWHM 82.81 deg, Reliability 0.991) and marking `N/A` for metrics without an angle
  analogue. Evidence: the table is embedded above.

* **REQ-7** — **Done**. Bar chart `results/images/pd_vs_nd_firing_rate.png` (200 DPI, 5 × 4
  inches) was produced by `plot_pd_vs_nd.py` and is embedded in the `## Visualizations`
  section of this file via `![PD vs ND mean firing rate with per-trial
  scatter](../../../tasks/t0020_port_modeldb_189347_gabamod/results/images/pd_vs_nd_firing_rate.png)`.

* **REQ-8** — **Done**. The canonical 2 × 20 = 40-trial sweep ran on the local Windows
  workstation, wrapped via `run_with_logs.py`. Evidence: command logs
  `logs/commands/010_run_gabamod_sweep_validation_gate.{json,stdout.txt,stderr.txt}` and
  `logs/commands/011_run_gabamod_sweep_full.{json,stdout.txt,stderr.txt}`; the
  `remote_machines_used.json` file is an empty array.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0020_port_modeldb_189347_gabamod/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0020_port_modeldb_189347_gabamod" date_compared: "2026-04-20"
---
# Comparison with Published Results

## Summary

This reproduction of the Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC under the paper's native
two-condition `gabaMOD` parameter-swap protocol (PD = 0.33, ND = 0.99) achieves **DSI 0.7838**
— squarely inside the literature envelope **[0.70, 0.85]** and **+0.468** above the t0008
rotation-proxy DSI of 0.316 — but the **peak firing rate (14.85 Hz)** remains well below the
envelope **[40, 80] Hz**, so the combined two-point envelope gate fails. The split is
informative: the gabaMOD mechanism cleanly recovers the direction-selectivity *contrast*
reported by `[PolegPolsky2016]`, while the peak-rate shortfall — previously entangled with the
rotation-proxy protocol mismatch in t0008 — is now unambiguously localised to the excitation
side of the port.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Poleg-Polsky 2016 [PolegPolsky2016, Figs 1G/4F/5G/6G/8E boxplot median] | DSI (median, noise-free control, spike output) | **0.80** | **0.7838** | -0.0162 | Paper reports DSI as median+/-quartile boxplots without a single aggregate number; qualitative headline **~0.8** taken from figure medians. Our protocol is the paper's native `gabaMOD` swap (PD=0.33, ND=0.99), matching the paper's direction-selectivity driver. |
| Poleg-Polsky 2016 [PolegPolsky2016, p. 1281 Exp Procedures] | Preferred-direction peak firing rate (Hz) | **40-80** (project-literature envelope; not numerically reported in the paper) | **14.85** | -25.15 (vs envelope floor 40) | `[PolegPolsky2016]` does not report a numeric peak firing rate anywhere in text or figures. The 40-80 Hz envelope floor is the project target drawn from broader DSGC literature consensus; comparison is to the envelope floor, not to a paper-verbatim number. |
| Poleg-Polsky 2016 [PolegPolsky2016, Fig 1D, n = 19] | PD NMDAR-mediated PSP component (mV) | **5.8 +/- 3.1** | not measured | — | Subthreshold validation target from patch-clamp recordings; this task measures spike output only. Listed to document a quantitative hook we did not reproduce. |
| Poleg-Polsky 2016 [PolegPolsky2016, Fig 1H, n = 19] | NMDAR multiplicative scaling slope (deg) | **62.5 +/- 14.2** | not measured | — | Multiplicativity test (additive baseline = 45 deg). Subthreshold only; not extracted in this task. |
| Poleg-Polsky 2016 [PolegPolsky2016, main.hoc stim() proc, PD setting] | Inhibitory gabaMOD scalar (PD) | **0.33** | **0.33** | +0.00 | Exact match to the paper's native protocol driver (sourced from the ModelDB 189347 `main.hoc`). |
| Poleg-Polsky 2016 [PolegPolsky2016, main.hoc stim() proc, ND setting] | Inhibitory gabaMOD scalar (ND) | **0.99** | **0.99** | +0.00 | Exact match to the paper's native protocol driver. |
| Prior task t0008 rotation-proxy port [t0008, results_summary.md] | DSI | **0.316** | **0.7838** | +0.468 | Rotation-proxy port held `gabaMOD` fixed and rotated BIP synapse coordinates. gabaMOD-swap port is 2.48x higher — reproducing the literature envelope on the DSI axis. |
| Prior task t0008 rotation-proxy port [t0008, results_summary.md] | Peak firing rate (Hz) | **18.1** | **14.85** | -3.25 | Both ports under-fire relative to envelope. gabaMOD-swap is slightly lower because PD-only firing (no rotation-based averaging) is compared against the rotation-proxy peak at the single best angle. |

## Methodology Differences

* **Direction-selectivity driver** — `[PolegPolsky2016]` implements DS via a per-condition
  `gabaMOD` parameter swap (`0.33` in PD, `0.99` in ND) inside `main.hoc`'s `stim()`
  procedure. This task uses the *same* driver verbatim (sourced from ModelDB 189347 `main.hoc`
  via t0008's library asset) — this is the protocol fix raised as suggestion **S-0008-02**
  after t0008 used a spatial-rotation proxy.
* **Stimulus structure** — `[PolegPolsky2016]` uses a moving bar in **8 directions at 45 deg
  spacing**; this task runs **no bar rotation**, using only two parameter-swapped conditions
  (PD and ND) to isolate the gabaMOD mechanism. There is therefore no angle axis, which is why
  `Null (Hz)`, `HWHM (deg)`, and trial reliability are marked N/A in the `results_detailed.md`
  comparison table.
* **Bar speed and stimulus window** — identical to the t0008 baseline: `tstop = 1000 ms`, `dt
  = 0.1 ms`, matching `main.hoc` verbatim.
* **Synaptic architecture** — identical to the paper: **177 AMPA + 177 NMDA + 177 GABA_A**
  synapses on ON dendrites, passive dendrites, Jahr-Stevens NMDAR Mg2+ block (all read from
  the unchanged HOC/MOD files sourced via the t0008 library asset).
* **Trial count** — `[PolegPolsky2016]` uses n = **25 / 21 / 34** cells as biological
  replicates; this task uses **20 seeded trials per condition** as computational replicates.
  Not directly comparable at the cell level but exceeds the 10-trial floor implied by the DSGC
  modelling literature.
* **Output metric reporting** — paper reports DSI as **median+/-quartile boxplots** across
  cells. This task reports DSI as the aggregate `(mean_PD - mean_ND) / (mean_PD + mean_ND)`
  ratio over 20 trials per condition — the same formula the t0012 scorer's `compute_dsi()`
  evaluates internally.
* **Subthreshold traces not extracted** — the paper's n = 19 patch-clamp validation targets
  (PSP amplitudes, slope-angle multiplicativity) require whole-cell voltage traces; this task
  records only somatic threshold-crossings for spike counting.

## Analysis

**The native protocol recovers DSI within 0.02 of the paper's headline figure-median value.**
DSI **0.7838** sits inside the **[0.70, 0.85]** envelope and only **-0.0162** below the
~**0.80** qualitative median that `[PolegPolsky2016]` reports via box-and-whisker plots in
Figures 1G/4F/5G/6G/8E. The 40-trial sweep confirms this is not a marginal pass: PD mean 14.85
Hz vs ND mean 1.80 Hz yields an ~8x firing-rate ratio with per-condition CVs of 10.7% (PD) and
57% (ND, on a small-integer spike count). The direction-selective *contrast* the paper reports
is reproduced faithfully under the paper's native driver.

**The peak-rate gap is real and now unambiguously localised.** PD peak of **14.85 Hz** falls
**25.15 Hz below** the **40 Hz** envelope floor. Because the `gabaMOD` swap is the paper's
exact native protocol, this shortfall cannot be attributed to a protocol mismatch in the way
t0008's rotation-proxy DSI gap could. The depression is intrinsic to the port — most likely in
excitation gain (BIP synapse count, `excMOD` scalar, stimulus strength) — and is independent
of whether direction selectivity is induced by rotation or by gabaMOD swap. The gap is
recorded as a genuine experimental finding consistent with Risk-3 in the plan.

**What the comparison does NOT tell us.** `[PolegPolsky2016]` does not report a numeric peak
firing rate in text or figures (see `research_papers.md` Gaps section in t0008), so the "fails
the envelope" verdict is relative to the project envelope **[40, 80] Hz** drawn from broader
DSGC literature, not to a paper-verbatim number. A direct peak-rate reproduction of this paper
is therefore not possible from the published material alone — only envelope-compliance checks
are.

### Prior Task Comparison

The plan explicitly cites t0008's rotation-proxy numbers
(`tasks/t0008_port_modeldb_189347/results/results_summary.md`) as the baseline to contrast
with, so a head-to-head comparison is mandatory per spec phase 19.

| Metric | Rotation proxy (t0008) | gabaMOD swap (t0020) | Delta | Envelope | Verdict |
| --- | --- | --- | --- | --- | --- |
| DSI | 0.316 | **0.7838** | **+0.468** (2.48x) | [0.70, 0.85] | t0020 inside envelope; t0008 below floor |
| Peak (Hz) | 18.1 | 14.85 | -3.25 | [40, 80] | Both below floor; gabaMOD-swap slightly lower |
| Null (Hz) | 9.4 | 1.80 | -7.60 | < 10 | Both pass ceiling; gabaMOD-swap much lower (ND firing is strongly suppressed by gabaMOD = 0.99) |
| HWHM (deg) | 82.81 | N/A | — | 60-90 | Two-point protocol has no angle axis |
| Reliability | 0.991 | N/A | — | > 0.9 | Two-point protocol has no per-angle trial variance |

**The DSI gap between the two ports refutes the interpretation that t0008's low DSI was caused
by port fidelity issues** (HOC sourcing, mechanism density, parameter mismatch). Every element
of the cell — HOC skeleton, MOD files, `apply_params`, synapse placement — is shared between
the two ports; only the driver changes. The fact that DSI jumps from 0.316 to 0.7838 when only
the driver is swapped confirms the hypothesis recorded in suggestion **S-0008-02**: t0008's
DSI shortfall was a protocol mismatch, not a port bug.

**The peak-rate deltas also narrow the search.** Both ports produce PD firing rates in the
14.85-18.1 Hz band (t0020 sits 3.25 Hz *below* t0008; t0008 aggregates over 12 angles whereas
t0020 uses only the PD condition). Because the driver changed but the firing rate did not
meaningfully shift, the depressed peak is localised to the *excitation* side of the port — the
same conclusion reached in the `results_detailed.md` analysis. Any follow-up should target BIP
synapse count, `excMOD`, or stimulus strength rather than anything on the inhibition side.

## Limitations

* **No single published numeric DSI or peak firing rate for `[PolegPolsky2016]` control**.
  Every DSI reference in the paper is a median+/-quartile boxplot; no numeric peak firing rate
  is reported in text or figures. The comparison therefore uses figure-median readings
  (~**0.80** for DSI) and project-envelope bounds (**[40, 80] Hz** for peak) rather than
  paper-verbatim numbers.
* **Two-point protocol has no angle axis**. HWHM, null rate per angle, and per-angle trial
  reliability are not measurable under this protocol and are marked N/A in the prior-task
  comparison table. The t0008 rotation-proxy port remains the correct tool for tuning-curve
  fitting.
* **Subthreshold validation targets not extracted**. `[PolegPolsky2016, Fig 1D-H]` provides
  concrete numeric subthreshold targets (PD NMDAR PSP component **5.8 +/- 3.1 mV**, ND **3.3
  +/- 2.8 mV**, slope **62.5 +/- 14.2 deg**) that this task does not reproduce — it records
  only somatic spike counts. A subthreshold validation sweep is a natural follow-up.
* **Single `gabaMOD` pair**. The sweep uses only the canonical **0.33 / 0.99** scalar pair
  from `main.hoc`. Sensitivity over intermediate `gabaMOD` values (e.g. 0.5, 0.7) is
  explicitly out of scope and proposed as a follow-up suggestion.
* **Mechanism-context comparisons are not attempted**. Sibling DSGC models with different
  architectures (Schachter 2010, Hanson 2019, Jain 2020, Oesch 2005) would require porting
  their weight sets and would not constitute like-for-like comparisons on the
  `[PolegPolsky2016]` baseline. Their relevance to future work is documented in t0008's
  `compare_literature.md`, not repeated here.
* **Trial-level noise controlled only by RNG seed**. Per-trial stochasticity depends on the
  NEURON RNG and may drift between NEURON/numpy/OS versions even with identical seeds; the
  comparison is stable at the aggregate (DSI, mean PD/ND) level but individual trial firing
  rates may not reproduce bit-exactly across environments.

</details>
