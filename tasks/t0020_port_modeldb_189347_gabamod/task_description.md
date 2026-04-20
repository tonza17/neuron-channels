# Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Motivation

This task implements suggestion **S-0008-02** raised by t0008. The existing port
(`modeldb_189347_dsgc`, library asset produced by t0008) reaches **DSI 0.316 / peak 18.1 Hz**, well
below the Poleg-Polsky & Diamond 2016 envelope (**DSI 0.70-0.85, peak 40-80 Hz**). The shortfall is
not a bug in the port — it comes from t0008's choice to substitute a spatial-rotation proxy for
the paper's native direction-selectivity protocol.

In the original ModelDB 189347 driver the direction-selectivity test does not rotate a stimulus.
Instead it runs the *same* synaptic input pattern under two different parameter settings of the
inhibitory `gabaMOD` scalar:

* **Preferred direction (PD)**: `gabaMOD = 0.33` — weak inhibition, strong spike output.
* **Null direction (ND)**: `gabaMOD = 0.99` — strong inhibition, suppressed spike output.

The DSI emerges from the PD/ND firing-rate ratio. t0008's `run_one_trial` implementation kept
`gabaMOD` fixed and instead rotated BIP synapse coordinates around the soma, which approximates
direction tuning geometrically but does not exercise the inhibition-modulation mechanism the paper
relies on. This task adds a **second** library asset that runs the paper's native protocol so the
project can quote a fair reproduction number against the published envelope, and so subsequent
sensitivity-analysis tasks can manipulate `gabaMOD` directly.

The rotation-proxy port from t0008 stays unchanged and remains valid for direction-tuning curves
that need an explicit angle axis (e.g. tuning-curve fitting, HWHM measurement). The two protocols
are kept side by side so future tasks can pick whichever matches their question.

## Scope

Produce a **new sibling library asset** with proposed id `modeldb_189347_dsgc_gabamod`. The new
asset shares the MOD files and `RGCmodel.hoc` skeleton with `modeldb_189347_dsgc` (do not vendor a
second copy of the source HOC/MOD — load them via the path conventions established in t0008) and
replaces only the per-angle BIP rotation in `run_one_trial` with a two-condition `gabaMOD` sweep.

In scope:

* New driver script (e.g. `code/run_gabamod_sweep.py`) that runs N PD trials and N ND trials,
  varying only the `gabaMOD` scalar between the two conditions.
* New tuning-curve CSV with schema `(condition, trial_seed, firing_rate_hz)` instead of t0008's
  `(angle_deg, trial_seed, firing_rate_hz)`. `condition` takes values `PD` and `ND`.
* Two-point envelope gate that scores the run against the published envelope using DSI from the
  PD/ND ratio and peak from the PD condition (HWHM and null are read from the rotation-proxy port in
  the comparison note — they have no analogue in the two-point protocol).
* Library asset metadata (`details.json`, `description.md`) registering the new asset under
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/`.

Out of scope:

* Re-deriving the underlying NEURON model. The HOC/MOD files used by t0008 are reused unchanged.
* Sensitivity sweeps over `gabaMOD` values other than the canonical 0.33 / 0.99 pair (proposed as
  follow-up suggestions).
* Re-fitting tuning curves with a Gaussian or von Mises function — the two-point protocol does not
  produce an angle axis.

## Approach

The work is a single implementation step plus a comparison note:

1. Initialise the new library asset folder and copy the t0008 driver as the starting point.
2. Refactor `run_one_trial` to accept a `gabaMOD` value as a keyword argument and remove the BIP
   `locx` rotation. The BIP synapse stays at its canonical position; only the inhibitory scalar
   changes between conditions.
3. Wire a new top-level driver that loops over `(condition, trial_seed)` pairs:
   * `condition = "PD"` → set `gabaMOD = 0.33` on every inhibitory point process before the run.
   * `condition = "ND"` → set `gabaMOD = 0.99` similarly.
   * `trial_seed` varies the RNG seed used for synaptic-release noise so each repeat is independent.
4. Write `tuning_curves.csv` with one row per `(condition, trial_seed)`. Default sweep: **2
   conditions × 20 trials = 40 trials per run**. Total runtime estimate: ~1.5 minutes on the local
   Windows workstation (240-trial t0008 run took ~9 minutes; 40 trials scales linearly).
5. Score the CSV with the t0012 `tuning_curve_loss` scorer using a **two-point envelope gate**:
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
* **Tuning curves CSV**: `data/tuning_curves.csv` with columns
  `(condition, trial_seed, firing_rate_hz)`.
* **Score report**: `results/score_report.json` produced by the t0012 scorer with the two-point
  envelope gate, including DSI, peak, pass/fail, and the envelope used.
* **Comparison note**: a section in `results/results_detailed.md` quantifying how the gabaMOD-swap
  port differs from the t0008 rotation-proxy port on DSI, peak, null, and HWHM. The note must be
  embedded in `results_detailed.md`, not a separate file, so it shows up in the materialized
  overview.
* **Charts**: bar chart of mean firing rate by condition (PD vs ND, with per-trial scatter) saved to
  `results/images/` and embedded in `results_detailed.md`.

## Dependencies

* `t0008_port_modeldb_189347` — provides the source HOC/MOD layout, `run_one_trial` template, and
  the rotation-proxy baseline numbers used in the comparison note.
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

* `data/tuning_curves.csv` has exactly `2 * n_trials_per_condition` rows with the canonical schema.
* `results/score_report.json` validates against the t0012 scorer's schema.
* Library asset folder passes the library-asset verificator (mirroring the layout used by
  `modeldb_189347_dsgc` in t0008).
* Comparison table in `results_detailed.md` quotes the t0008 numbers verbatim from
  `tasks/t0008_port_modeldb_189347/results/results_summary.md` (no rounding drift).

## Risks and Fallbacks

* **gabaMOD scalar not exposed at the Python level**: if the t0008 port wraps `gabaMOD` inside a
  HOC-only context that is not directly settable from Python, the implementation may need to set it
  via `h.gabaMOD = value` as a global before instantiating the inhibitory point processes, or reach
  into each `inh_syn` object after instantiation. Either path is straightforward; flag in the
  implementation step log if a HOC patch is needed.
* **Two-point gate too permissive**: if the run produces a DSI inside the envelope but spike counts
  are unrealistically low (e.g. peak < 5 Hz), record this in the limitations section. The envelope
  is necessary but not sufficient — a follow-up suggestion can add a per-trial spike-count floor.
* **Driver divergence from rotation-proxy port**: the new driver must not silently re-introduce the
  `locx` rotation. The implementation step must include an assertion that BIP `locx` stays at its
  canonical value across all trials.

## Cross-references

* Source suggestion: **S-0008-02** (active, high priority, raised by t0008).
* Source paper: Poleg-Polsky & Diamond 2016, ModelDB 189347 (DOI `10.1016/j.neuron.2016.02.013`).
* Sibling library asset: `modeldb_189347_dsgc` from t0008 (rotation-proxy port).
* Scorer dependency: `tuning_curve_loss` library from t0012.
