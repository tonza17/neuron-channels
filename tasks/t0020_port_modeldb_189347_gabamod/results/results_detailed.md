---
spec_version: "2"
task_id: "t0020_port_modeldb_189347_gabamod"
---
# Results Detailed: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Summary

Implemented a new sibling library asset `modeldb_189347_dsgc_gabamod` that drives the Poleg-Polsky &
Diamond 2016 DSGC cell under the paper's native two-condition `gabaMOD` swap protocol: PD trials set
`h.gabaMOD = 0.33` (weak inhibition) and ND trials set `h.gabaMOD = 0.99` (strong inhibition),
keeping every BIP synapse at its canonical spatial position. The canonical 2 × 20 = 40-trial sweep
yielded **DSI 0.7838** (inside the literature envelope [0.70, 0.85]) with **peak 14.85 Hz** (below
the envelope [40, 80] Hz), so the combined envelope gate fails. This is a genuine experimental
finding consistent with Risk-3 in the plan — the gabaMOD swap mechanism is clearly reproducing the
direction-selectivity *contrast* seen in the paper, but the absolute firing rates remain depressed,
the same shortfall that motivated this task in the first place. The rotation-proxy port from t0008
is unchanged and remains valid for tuning-curve fitting.

## Methodology

### Machine specs

* Windows 11 Education (build 10.0.22631) workstation, the same machine t0008 used.
* Python 3.12 via `uv`, NEURON 8.2.7 + NetPyNE 1.1.1 (already installed from t0008).
* No remote compute, no GPU, no paid API calls.

### Runtime

* Implementation step started: 2026-04-20T19:37:29Z (prestep).
* Implementation step completed: 2026-04-20T20:05:00Z.
* Full sweep wall clock: ~85 seconds for 40 trials (well within the ~1.5 minute estimate; 6× faster
  than t0008's 240-trial sweep as expected).
* Full task (worktree creation through implementation completion): ~52 minutes.

### Protocol

1. **Cell build**: `build_dsgc()` imported from `tasks.t0008_port_modeldb_189347.code.build_cell`
   (registered via the t0008 library asset) — reuses the unchanged HOC/MOD skeleton and
   `apply_params()` canonical parameter block.
2. **Per-trial driver** (`run_one_trial_gabamod` in
   `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py`):
   * Apply canonical parameters via `apply_params(h)`.
   * **Override** `h.gabaMOD` to the condition-specific scalar (0.33 for PD, 0.99 for ND) *after*
     `apply_params` (which otherwise writes the canonical 0.33).
   * Assert each BIP synapse stays at its baseline `locx` — the per-trial rotation guard (REQ-3).
   * Seed the NEURON RNG with `trial_seed` for synaptic-release noise.
   * Run `h.finitialize(-65 mV)` + `h.continuerun(1000 ms)` and count threshold-crossings at the
     soma.
3. **Sweep** (`main` in `run_gabamod_sweep.py`): iterate over
   `(condition, trial_seed) ∈ {PD, ND} × range(1, 21)`; write one row per trial to
   `data/tuning_curves.csv` with schema `(condition, trial_seed, firing_rate_hz)`.
4. **Scoring** (`main` in `code/score_envelope.py`): read the CSV, compute
   `DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)` and `peak = mean_PD` inline (t0012's high-level
   `score()` rejects non-12-angle inputs; the formula is the same one t0012's `compute_dsi` uses
   internally). Gate against unwidened literature envelope (DSI ∈ [0.70, 0.85], peak ∈ [40, 80]
   Hz) and write `results/score_report.json` + `results/metrics.json`.
5. **Chart** (`code/plot_pd_vs_nd.py`): bar chart of mean PD vs ND firing rate with per-trial
   scatter overlay, saved to `results/images/pd_vs_nd_firing_rate.png` at 200 DPI.
6. **Validation gate**: before the full sweep, ran `run_gabamod_sweep.py --limit 2 --n-trials 1` (PD
   = 15 Hz, ND = 1 Hz, DSI ≈ 0.875), confirming the gabaMOD swap took effect before committing to
   the 40-trial sweep.

All CLI invocations wrapped via `uv run python -m arf.scripts.utils.run_with_logs`; command logs
live in `logs/commands/008..013_*.{json,stdout.txt,stderr.txt}`.

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

![PD vs ND mean firing rate with per-trial scatter](images/pd_vs_nd_firing_rate.png)

The bar chart shows mean PD vs ND firing rates (bars) with per-trial scatter overlay (dots). PD
trials cluster between 11-18 Hz; ND trials cluster between 0-4 Hz. The large, clean separation of
the two distributions is the direct visual evidence for the high DSI.

## Analysis

The headline result has two parts that must not be conflated:

1. **The gabaMOD swap mechanism works.** DSI 0.7838 from 40 trials is not a marginal pass — it
   sits squarely inside the literature envelope and is **2.48× t0008's rotation-proxy DSI
   (0.316)**. The PD vs ND contrast is large (~8× firing-rate ratio), reproducible across seeds (PD
   stddev 1.59 Hz on a mean of 14.85 Hz = 10.7% CV; ND stddev 1.03 Hz on a mean of 1.80 Hz), and
   consistent with what the paper reports qualitatively.

2. **Absolute firing rates remain depressed.** Peak 14.85 Hz is well below the envelope [40, 80] Hz.
   This is *not* the rotation-proxy shortfall — the gabaMOD swap is exactly the paper's native
   protocol. It means the depressed firing rate is intrinsic to the current port (same excitation
   gain, mechanism densities, synapse counts, or stimulus strength as t0008), *independent* of
   whether direction selectivity is induced by rotation or by gabaMOD swap.

This cleanly localises the gap: the two-point protocol rules out the rotation proxy as the cause of
the peak-rate shortfall, so any follow-up sensitivity sweep should target the *excitation* side (BIP
synapse count, `excMOD`, stimulus strength) rather than the inhibition side.

## Examples

Examples are verbatim rows from `data/tuning_curves.csv` (schema
`condition,trial_seed,firing_rate_hz`). The dataset has 40 rows (20 PD + 20 ND). Each code block
below is the actual input/output of one or two trials: the *input* is the `(condition, trial_seed)`
pair that drives `run_one_trial_gabamod`, which sets `h.gabaMOD` to 0.33 (PD) or 0.99 (ND) and seeds
the NEURON RNG with `trial_seed`; the *output* is the `firing_rate_hz` column written to the CSV at
the end of the 1-second stimulus window.

### Contrastive examples (same seed, both conditions)

These five pairs isolate the gabaMOD effect: the only thing that differs between the two rows of
each pair is `h.gabaMOD` (0.33 vs 0.99). Same cell, same BIP positions, same noise RNG seed.

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

Example 5 — seed 14, trial-level DSI = (15-0)/(15+0) = **1.000** (complete ND suppression, ideal
direction-selective trial):

```csv
condition,trial_seed,firing_rate_hz
PD,14,15.000000
ND,14,0.000000
```

Every contrastive pair independently shows direction selectivity. The effect is not an artefact of
trial averaging — it holds at the single-trial level too.

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

Example 7 — the three highest PD trials in the sweep. Even the best (18 Hz) stays well below the
envelope floor of 40 Hz, reinforcing the peak-rate diagnosis in the Analysis section:

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

Example 9 — the highest ND trial in the sweep. `gabaMOD = 0.99` still suppresses the matching PD
trial (seed 4, 14 Hz) down to 4 Hz; the 3.5× ratio is preserved even at the worst ND seed:

```csv
condition,trial_seed,firing_rate_hz
ND,4,4.000000
PD,4,14.000000
```

### ND cluster around mode

Example 10 — three clustered ND trials showing the typical null-direction firing rate of 1-3 Hz:

```csv
condition,trial_seed,firing_rate_hz
ND,6,3.000000
ND,9,3.000000
ND,13,3.000000
```

### Boundary case — complete null suppression

Example 11 — the only trial with zero spikes. Seed 14 shows that `gabaMOD = 0.99` is strong enough
to completely silence the cell under some noise realisations. The same-seed PD trial fires 15 Hz,
making this the ideal DSI = 1.0 pair used in Example 5:

```csv
condition,trial_seed,firing_rate_hz
ND,14,0.000000
```

### Validation-gate example (pre-sweep sanity check)

Example 12 — the `--limit 2 --n-trials 1` validation gate run before the full sweep. The log lines
below are extracted verbatim from `logs/commands/010_run_gabamod_sweep_validation_gate.stdout.txt`
and show the PD >> ND contrast that confirmed the gabaMOD swap took effect before the 40-trial
commit:

```text
[validation_gate] condition=PD trial_seed=1 firing_rate_hz=15.0
[validation_gate] condition=ND trial_seed=1 firing_rate_hz=1.0
[validation_gate] DSI = (15 - 1) / (15 + 1) = 0.875
[validation_gate] PASS: PD >> ND, proceeding to full sweep
```

## Verification

* `verify_task_file.py` — PASSED (0 errors) at init-folders step (log in
  `logs/steps/003_init-folders/verify_task_file.json`).
* `verify_task_dependencies.py` — PASSED at check-deps step; both `t0008_port_modeldb_189347` and
  `t0012_tuning_curve_scoring_loss_library` completed.
* `verify_library_asset.py` — N/A (script referenced by the plan's Verification Criteria does not
  exist in `arf/scripts/verificators/`). Structural validity was confirmed manually: `details.json`
  has `spec_version "2"` and all required fields (library_id, name, version, short_description,
  description_path, module_paths, entry_points, dependencies, categories, created_by_task,
  date_created); `description.md` has YAML frontmatter with `spec_version "2"`, exceeds the 500-word
  minimum (1541 words), and is flowmark-normalised.
* **Per-trial BIP-position assertion (REQ-3 critical guard)** — PASSED across all 40 trials. The
  driver asserts `h.RGC.BIPsyn[i].locx == baseline[i].bip_locx_um` for all `i` immediately before
  each `h.continuerun` call, guaranteeing the rotation logic was not silently re-engaged.
* **CSV schema check (REQ-4)** — PASSED. `data/tuning_curves.csv` has exactly 40 rows with header
  `condition,trial_seed,firing_rate_hz` and values in the expected ranges.
* **Validation gate** — PASSED. The `--limit 2 --n-trials 1` run produced PD = 15 Hz, ND = 1 Hz
  (DSI ≈ 0.875), confirming the gabaMOD swap took effect before the full sweep.
* **Lint / type** — `ruff check --fix .`, `ruff format .`, and
  `mypy -p tasks.t0020_port_modeldb_189347_gabamod.code` all clean from the worktree root.

## Limitations

* **Peak firing rate below envelope** — the combined two-point envelope gate fails because
  `peak = 14.85 Hz` < 40 Hz. As anticipated by Risk-3 in the plan, this is a genuine finding: the
  gabaMOD swap reproduces the *contrast* but not the *absolute level*. The shortfall is now
  localised to the excitation side of the model rather than to the direction-selectivity protocol.
* **No angle axis** — the two-point protocol has no notion of angle, so `HWHM (deg)` and
  `Null (Hz)` are marked N/A in the comparison table. The t0008 rotation-proxy port remains the
  correct tool for tuning-curve fitting.
* **t0012 scorer not used at the API boundary** — the high-level `score()` entry point in the
  t0012 library enforces a 12-angle / 30-degree grid on input CSVs, which the two-point protocol
  cannot satisfy. The DSI formula is therefore computed inline in `score_envelope.py` using the same
  arithmetic `compute_dsi()` uses internally in t0012; the t0012 library is referenced in the
  description and is available for the envelope-widening approach if a future task wants it.
* **Single gabaMOD value per condition** — the sweep uses only the canonical 0.33 / 0.99 pair.
  Sensitivity over intermediate gabaMOD values is explicitly out of scope (proposed as a follow-up
  suggestion).
* **Per-trial stochasticity controlled only by seed** — noise realisations depend on the NEURON
  RNG; reproducibility is seed-controlled but sensitive to NEURON / numpy / OS version changes. The
  exact firing rates may drift between environments even with identical seeds.

## Files Created

* `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/details.json`
* `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/description.md`
* `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/code/.gitkeep`
* `tasks/t0020_port_modeldb_189347_gabamod/code/constants.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/paths.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/score_envelope.py`
* `tasks/t0020_port_modeldb_189347_gabamod/code/plot_pd_vs_nd.py`
* `tasks/t0020_port_modeldb_189347_gabamod/data/tuning_curves.csv` (40 rows + header, 2 conditions
  × 20 trial seeds)
* `tasks/t0020_port_modeldb_189347_gabamod/results/score_report.json` (full two-point gate report)
* `tasks/t0020_port_modeldb_189347_gabamod/results/metrics.json` (registered metric key
  `direction_selectivity_index` only; other keys moved to `results_detailed.md` per task-results
  spec v8)
* `tasks/t0020_port_modeldb_189347_gabamod/results/costs.json` (zero-cost local-only task)
* `tasks/t0020_port_modeldb_189347_gabamod/results/remote_machines_used.json` (empty array)
* `tasks/t0020_port_modeldb_189347_gabamod/results/results_summary.md`
* `tasks/t0020_port_modeldb_189347_gabamod/results/results_detailed.md` (this file)
* `tasks/t0020_port_modeldb_189347_gabamod/results/images/pd_vs_nd_firing_rate.png` (200 DPI bar
  chart with per-trial scatter)
* `tasks/t0020_port_modeldb_189347_gabamod/logs/commands/008..013_*.{json,stdout.txt,stderr.txt}`
  (run_with_logs output for validation gate, full sweep, scorer, chart generator, and verification
  commands)
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
  `details.json` (spec_version "2", all required fields) and `description.md` (spec_version "2",
  YAML frontmatter, 1541 words). Evidence: files exist; manual structural validity check in the
  Verification section of this file (the planned `verify_library_asset.py` does not exist, which is
  recorded as an Issue in the implementation step log).

* **REQ-2** — **Done**. The new driver imports `build_dsgc`, `read_synapse_coords`,
  `apply_params`, and `get_cell_summary` from `tasks.t0008_port_modeldb_189347.code.build_cell` via
  the t0008 library asset. No `sources/` directory exists under the new asset; the HOC/MOD files are
  not vendored a second time. Evidence: `run_gabamod_sweep.py` import block; filesystem check that
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/sources/` does
  not exist.

* **REQ-3** — **Done**. `run_one_trial_gabamod` sets `h.gabaMOD = 0.33` for PD and 0.99 for ND,
  keeps BIP positions at baseline, and asserts per-trial that
  `h.RGC.BIPsyn[i].locx == baseline[i].bip_locx_um` for all `i`. Evidence: assertion survived the
  full 40-trial sweep (no AssertionError in any of the `logs/commands/010_*.stderr.txt` or
  `logs/commands/011_*.stderr.txt` files).

* **REQ-4** — **Done**. `data/tuning_curves.csv` has exactly 40 rows with header
  `condition,trial_seed,firing_rate_hz`. Evidence: the file exists; `wc -l` shows 41 lines (1 header
  \+ 40 data rows); the Examples section in this file quotes 20+ individual rows.

* **REQ-5** — **Done**. `results/score_report.json` contains `protocol: "gabamod_swap"`,
  `n_trials_per_condition: 20`, `dsi: 0.7838`, `peak_hz: 14.85`, `gate` object with `dsi_min`,
  `dsi_max`, `peak_min_hz`, `peak_max_hz`, `dsi_in_range: true`, `peak_in_range: false`,
  `passed: false`. Gate thresholds are the unwidened literature values [0.70, 0.85] and [40, 80] Hz.
  Evidence: file exists at the expected path.

* **REQ-6** — **Done**. The `## Metrics Tables` section in this file includes the mandated
  comparison table with rows DSI / Peak / Null / HWHM / Reliability, quoting the t0008
  rotation-proxy numbers verbatim from `tasks/t0008_port_modeldb_189347/results/results_summary.md`
  (DSI 0.316, Peak 18.1 Hz, Null 9.4 Hz, HWHM 82.81 deg, Reliability 0.991) and marking `N/A` for
  metrics without an angle analogue. Evidence: the table is embedded above.

* **REQ-7** — **Done**. Bar chart `results/images/pd_vs_nd_firing_rate.png` (200 DPI, 5 × 4
  inches) was produced by `plot_pd_vs_nd.py` and is embedded in the `## Visualizations` section of
  this file via
  `![PD vs ND mean firing rate with per-trial scatter](images/pd_vs_nd_firing_rate.png)`.

* **REQ-8** — **Done**. The canonical 2 × 20 = 40-trial sweep ran on the local Windows
  workstation, wrapped via `run_with_logs.py`. Evidence: command logs
  `logs/commands/010_run_gabamod_sweep_validation_gate.{json,stdout.txt,stderr.txt}` and
  `logs/commands/011_run_gabamod_sweep_full.{json,stdout.txt,stderr.txt}`; the
  `remote_machines_used.json` file is an empty array.
