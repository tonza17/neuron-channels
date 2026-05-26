# Reproduce t0126 with signed DSI and real per-cell firing rates

## Motivation

t0126 (`bedb_dsi_atp_per_spike_nsga2_60gen`) ran an NSGA-II optimisation of the Bed B DSGC over a
68-d morphology + electrophysiology parameter vector with objective
`F = [-dsi_vector_sum, +atp_per_spike_molecules]`. Two design choices in that task limit the
downstream interpretability of its Pareto front and are corrected here:

1. **Vector-sum DSI** (`_vector_sum_dsi` in `tasks/t0126_*/code/evaluator.py:356`) collapses the
   antipodal pair `[0°, 180°]` to a non-negative scalar `|PD - ND| / (PD + ND)`. The sign is
   discarded, so cells that fire *more* to ND than PD (anti-preferred response) look identical to
   cells with a true preferred-direction bias of the same magnitude. The standard
   direction-selective ganglion cell (DS-RGC) literature uses the **signed** ratio
   `DSI = (R_PD - R_ND) / (R_PD + R_ND)`, range `[-1, 1]`, so direction reversals are detectable.

2. **`pd_rate_hz` placeholder**: per project memory `project_t0126_cell_trace_synthesised.md`, the
   `cell_trace` artefact in t0126 was hand-synthesised after the run, with `pd_rate_hz = 40` used as
   a hard-coded placeholder for every cell. The per-direction firing rates that downstream analyses
   (factor analysis, cluster reports, Pareto plots) consume are therefore unreliable for t0126. This
   task computes `pd_rate_hz` and `nd_rate_hz` directly from the actual per-direction spike counts
   that the evaluator already records.

Together, these two corrections let us re-examine the DSI-vs-ATP-per-spike Pareto on a fresh seed
with metrics that match the literature definition and reflect what each cell actually does.

## Scope

* **Single fresh seed** (3517) — not in the t0124 / t0126 / t0128 lineage. This is a first-pass
  replication; multi-seed scaling is left to a follow-up if results warrant.
* Fork of t0126's evaluator and NSGA-II driver into `tasks/t0129_*/code/`. **No changes to t0126
  itself** — the framework rule of completed-task immutability applies.
* All other t0126 protocol parameters preserved verbatim: 68-d parameter vector, Bed B substrate,
  antipodal direction pair `[0°, 180°]`, `N_EVAL_SEEDS`, `TSTOP_MS = 1400`, smoke-gate, silence
  guard at `pd_spikes_sum < 3`, 60 generations, population restart cadence
  (`_POOL_RESTART_EVERY = 10`), HV-plateau auto-stop **disabled** (per
  `feedback_disable_hv_plateau_autostop`).
* **t0127 and t0128 are out of scope.** t0127's cell_trace JSONL recording fix is not adopted; this
  task does not record per-spike `cell_trace` data. Instead, the full electrophysiology + morphology
  parameter vector for every evaluated cell is persisted to a per-cell parameter dump (see Outputs).

## Changes to the t0126 Evaluator

All edits live in `tasks/t0129_*/code/evaluator.py` (forked copy). t0126 is not touched.

### Change 1: Signed antipodal DSI

Replace the call to `_vector_sum_dsi` with a new helper:

```python
def _signed_antipodal_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float:
    """Signed antipodal DSI = (R_PD - R_ND) / (R_PD + R_ND), range [-1, 1].

    Assumes exactly two antipodal directions (PD at PD_DIRECTION_DEG and ND
    at PD_DIRECTION_DEG + 180 deg). Returns -1.0 (WORST_CASE_DSI) when the
    denominator is zero.
    """
```

The objective `F` is rewritten as `F = [-dsi_signed, +atp_per_spike_molecules]` so NSGA-II still
maximises DSI. The silence sentinel `WORST_CASE_DSI = -1.0` is reused — already at the lower bound
of the signed range. The `CellEvalResult` dataclass field is renamed `dsi_vector_sum` →
`dsi_signed` to make the metric switch obvious in downstream code; both the metric registration in
`meta/metrics/` and the comparator scripts must be updated accordingly.

### Change 2: Real per-direction firing rates

The evaluator already populates `firing_hz_per_dir: dict[str, float]` from actual spike counts
(`tasks/t0126_*/code/evaluator.py:467-470`). This task formalises two named scalar fields on
`CellEvalResult` derived from that same data:

* `pd_rate_hz = mean(pd_spikes) / (TSTOP_MS / 1000.0)`
* `nd_rate_hz = mean(nd_spikes) / (TSTOP_MS / 1000.0)`

These replace the synthesised placeholders downstream. They are the actual numbers used by the
signed-DSI computation, so the two corrections are arithmetically consistent.

### Change 3: Per-cell parameter persistence

For every cell evaluated during the run (Phase A random-init population + every NSGA-II generation),
persist a JSONL row containing:

* `gen` (int) — generation index, `-1` for Phase A random init
* `cell_idx` (int) — index within the generation
* `param_vector` (list[float]) — full 68-d morphology + electrophysiology vector
* `dsi_signed` (float)
* `atp_per_spike_molecules` (float)
* `pd_rate_hz` (float)
* `nd_rate_hz` (float)
* `silence_failed` (bool)
* `n_errors` (int)

File: `results/cell_params.jsonl`. This replaces the dropped `cell_trace.jsonl` for diagnostic
purposes — it loses the per-spike timing detail but keeps everything needed to reconstruct
parameter-vs-objective scatter plots and per-cell factor analysis.

## Approach

1. **Bootstrap & smoke gate.** Compile mod files, re-run the smoke gate from t0126 verbatim to
   confirm the forked evaluator behaves identically on a fixed test cell before changing the DSI
   formula. (The smoke gate currently asserts on `dsi_vector_sum`; relax its assertion to compare
   against the new `dsi_signed` on the same fixed cell.)
2. **Phase A: random init.** Generate the seed-3517 random initial population using the t0126
   protocol. Persist parameters + metrics per cell.
3. **Phase B: 60-generation NSGA-II.** Launch via the canonical `run_seed3517.sh` wrapper (per
   `feedback_nsga2_launch_via_run_script`). Auto-stop disabled, `_POOL_RESTART_EVERY = 10`, budget
   cap + generation ceiling are the only stop conditions.
4. **Post-run analysis.** Build Pareto plot of `dsi_signed` vs `atp_per_spike_molecules`,
   distribution of `dsi_signed` (with negative tail visible), and PD-vs-ND rate scatter coloured by
   `dsi_signed`. Compare cross-front overlap and Pareto-dominance against t0126's vector-sum front.
5. **Comparison vs t0126.** Quantify how many t0126-Pareto cells would still be Pareto-optimal under
   signed DSI; flag cells whose `dsi_vector_sum > 0.5` but `dsi_signed < 0` (reversed preference
   masked by magnitude).

## Outputs and Expected Assets

* **Predictions asset** — Pareto front of cells under (`dsi_signed`, `atp_per_spike_molecules`)
  with full parameter vectors. Mirrors t0126's predictions asset format.
* **Answer asset** — one-pager: "Does the signed-DSI re-evaluation of t0126's protocol change the
  Pareto structure, or is the vector-sum / signed distinction immaterial on the antipodal pair?"
  with supporting numbers.
* `results/cell_params.jsonl` — per-cell parameter dump (see Change 3).
* `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
  `results/suggestions.json`, `results/costs.json`, `results/remove_machines_used.json`.
* `results/images/` — Pareto front, DSI distribution (showing negative tail), PD-vs-ND scatter,
  t0126-vs-t0129 front overlay.

## Dependencies

* `t0126_bedb_dsi_atp_per_spike_nsga2_60gen` — code template, comparison baseline, parameter
  bounds, smoke-gate fixture.

t0127 and t0128 are explicitly **not** dependencies and are not read.

## Compute, Budget, and Time

Single seed × 60 generations × NSGA-II population × NEURON simulation per cell. Target compute
profile mirrors t0126's one-seed cost envelope (t0126 ran 1 seed in ~9h elapsed on the local
machine). Budget cap inherited from t0126's run script.

* **GPU**: none. NSGA-II + NEURON is CPU-bound.
* **Machine**: local (CPU). Remote provisioning not required for one seed.
* **Estimated wall-clock**: ~8-12h (single seed, 60 gen). Hard ceiling 24h via budget cap.

## Risks & Fallbacks

* **Smoke gate fails after DSI swap.** Likely cause: an unrelated regression in the fork.
  Mitigation: diff `evaluator.py` against t0126 line-by-line; only the DSI helper, the field rename,
  and the rate-field additions should differ.
* **All Phase A cells trip the silence guard** (`dsi_signed = -1.0`). Same risk as t0126 — fall
  back to wider random init bounds is *not* permitted (would break parameter-vector comparability
  with t0126). Document and stop.
* **Run script drops the per-cell JSONL** (per memory `feedback_nsga2_launch_via_run_script`).
  Mitigation: verify the wrapper sets the env var that the evaluator reads for `cell_params.jsonl`
  before launching; assert the file exists and is non-empty after Phase A.

## Verification Criteria

* `evaluator.py` exports a `_signed_antipodal_dsi` helper with a unit test in
  `tasks/t0129_*/code/test_evaluator_dsi_guard.py` covering: (a) PD>ND positive case, (b)
  PD<ND negative case, (c) PD=ND=0 silence sentinel, (d) PD=ND>0 zero case.
* The smoke gate passes for a fixed cell after the DSI change.
* `results/cell_params.jsonl` exists, has one row per evaluated cell, and contains all required
  fields.
* `metrics.json` reports `dsi_signed_max`, `dsi_signed_pareto_median`, `atp_per_spike_pareto_min`,
  `pd_rate_hz_pareto_median`, and the count of t0126-Pareto cells with `dsi_vector_sum > 0.5` but
  `dsi_signed < 0`.
* Pareto plot embedded in `results_detailed.md` with negative-DSI region visible on the axis.
