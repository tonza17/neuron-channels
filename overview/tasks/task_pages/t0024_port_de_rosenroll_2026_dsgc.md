# ✅ Port de Rosenroll 2026 DSGC model

[Back to all tasks](../README.md)

> Tuning Curve RMSE (Hz): **15.489547768408103**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0024_port_de_rosenroll_2026_dsgc` |
| **Status** | ✅ completed |
| **Started** | 2026-04-21T01:51:48Z |
| **Completed** | 2026-04-21T08:55:00Z |
| **Duration** | 7h 3m |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Task types** | `code-reproduction` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 1 library, 1 paper |
| **Step progress** | 12/15 |
| **Task folder** | [`t0024_port_de_rosenroll_2026_dsgc/`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/task_description.md)*

# Port de Rosenroll 2026 DSGC Model

## Motivation

The project currently has DSGC compartmental model ports derived from a single lineage: t0008
and t0020 both port ModelDB 189347 (Poleg-Polsky & Diamond 2016), and t0022 modifies that same
port for dendritic-computation DS. A sibling port of Hanson et al. 2019 is reserved in t0023.
Adding de Rosenroll et al. 2026 as an independent third implementation provides a third
structurally independent comparison point and, because the paper is recent, is the port most
likely to incorporate modern methodology and channel mechanisms. In particular, it may include
an explicit Nav1.6 / Nav1.2 split at the axon initial segment consistent with the patch-clamp
priors reviewed in t0017, and may use more recent Kv and Cav formulations than the older
Poleg-Polsky and Hanson models. This makes it especially relevant to the project's
channel-testbed goal of evaluating how specific channel combinations shape direction
selectivity.

## Scope

Port the de Rosenroll et al. 2026 DSGC model into the project as a new library asset (proposed
slug `de_rosenroll_2026_dsgc`) following the HOC/MOD/morphology layout established by t0008.
Fetch the paper as a paper asset if it is not already present. Run the standard 12-angle
moving-bar tuning-curve protocol using the driver infrastructure from t0022 where compatible,
producing `tuning_curves.csv` and a `score_report.json` against the target tuning curve from
t0004. Compare results against the Poleg-Polsky lineage (t0008, t0020, t0022) and the Hanson
port (t0023) in `results_detailed.md`.

## Deferred Status

This task is deferred. It is created and reserved now but must NOT be executed by the
execute-task loop until t0022 completes and the researcher explicitly reviews its outcomes.
After task-folder creation the orchestrator will write an intervention file to block
execution. The decision to proceed depends on what t0022 reveals about the channel-testbed
framework and whether a third independent implementation adds value.

## Deliverables

* New library asset `de_rosenroll_2026_dsgc` with HOC, MOD, and morphology files,
  `details.json`, and `description.md`.
* Source paper downloaded and registered as a paper asset if not already in the corpus.
* 12-angle moving-bar tuning curve: `tuning_curves.csv` and `score_report.json`.
* Cross-model comparison in `results_detailed.md` against t0008, t0020, t0022, and t0023.

## Dependencies

* `t0008_port_modeldb_189347` — reference HOC/MOD library-asset skeleton.
* `t0012_tuning_curve_scoring_loss_library` — scorer used for `score_report.json`.
* `t0022_modify_dsgc_channel_testbed` — driver infrastructure (soft dependency; reuse if
  compatible, otherwise adapt).

## Risks and Unknowns

* The 2026 paper may have restricted full-text access or be paywalled at porting time,
  limiting methodological detail.
* Original source code may not be publicly released or may not target NEURON, forcing partial
  reimplementation from the paper.
* Morphology may live in a different repository with different conventions.
* The model may rely on MOD mechanisms (Nav1.6, Nav1.2, modern Kv1, updated Cav) not yet in
  the project's MOD set, requiring new mechanism files and validation.
* Rough effort estimate: 1-2 days if source is NEURON and openly available; 3-5 days if
  partial reimplementation is needed.

## Out of Scope

* Parameter fitting or channel-density sweeps on the ported model (future task).
* Cross-simulator porting (e.g., NetPyNE, Brian) beyond the NEURON target.
* Re-running t0022's channel-testbed modifications on this model (future task if justified by
  t0022 outcomes).
* Executing this task now — execution is blocked pending t0022 review.

</details>

## Metrics

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.7758620689655171** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **68.65079365079364** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9835579184749684** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **15.489547768408103** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [de Rosenroll 2026 DSGC](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/) | [`description.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/description.md) |
| paper | [Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective circuit](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/) | [`summary.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Port the full upstream SacNetwork with bp_locs/probs/deltas to
reproduce the deRosenroll correlation-drop effect</strong> (S-0024-01)</summary>

**Kind**: technique | **Priority**: high

The t0024 port misses REQ-5 on all three sub-criteria (corr DSI 0.82 vs paper target
[0.30,0.50]; uncorr DSI 0.84 vs [0.18,0.35]; drop fraction 0.000 vs >=0.20) because the AR(2)
correlation was applied at per-terminal Exp2Syn drivers rather than across the
spatially-distributed SAC varicosity release network that the paper identifies as the causal
substrate. Port the upstream SacNetwork class (bp_locs, probs, deltas) from
geoffder/ds-circuit-ei-microarchitecture into a new sibling library asset, drive the same
cell, and rerun the 8-direction correlated/uncorrelated sweep. Target: reproduce the ~0.39 ->
~0.25 DSI drop.

</details>

<details>
<summary><strong>Sweep paper-text biophysics (Ra 200, eleak -65, Na 200/70/35) to
test peak firing-rate shortfall</strong> (S-0024-02)</summary>

**Kind**: experiment | **Priority**: medium

Peak firing rate is 5.15 Hz in t0024 versus the paper's qualitative ~30-40 Hz and the t0004
envelope of 40-80 Hz. The paper text and the companion repository disagree on Ra, eleak, and
Na/K densities; the repository values were used as authoritative. Run a 2x2x3 sensitivity
sweep varying Ra (100/200), eleak (-60/-65), and Na density regime (code/paper/intermediate)
with 10 trials per condition at PD/ND to isolate which single parameter change recovers peak
rate without destroying DS. Scorer: t0012 tuning_curve_loss against the t0004 envelope.

</details>

<details>
<summary><strong>Overlay a Van Wart + Werginz AIS on the deRosenroll morphology
to test peak-rate recovery</strong> (S-0024-03)</summary>

**Kind**: experiment | **Priority**: medium

Research-internet gap 2 showed that the upstream repository has no explicit AIS section, but
research-papers (Werginz 2020, Van Wart 2007) pins the AIS-to-soma Na ratio at ~7x and names
AIS length as the dominant predictor of maximum sustained firing rate. Fork t0024 into a new
library asset, add a two-subsegment AIS (proximal Nav1.2/Nav1.1, distal Nav1.6 + Kv1.2) with
Na ratio 7x and AIS length 25-50 um, rerun the 8-direction correlated/uncorrelated protocol,
and compare peak firing rate and HWHM to the t0024 baseline. Does not require rebuilding the
SAC network.

</details>

<details>
<summary><strong>Parameterize t0011/t0012 tuning-curve plotter and scorer to support
N_ANGLES != 12</strong> (S-0024-04)</summary>

**Kind**: library | **Priority**: medium

The t0011 tuning_curve_viz library and the t0012 tuning_curve_loss scorer both hardcode
N_ANGLES=12, which blocks native 8-direction visualisation and scoring for the deRosenroll
port (and any future paper that uses 4/6/8/16/24 directions). Refactor both libraries to
accept an N_ANGLES argument (default 12 for backward compatibility) and rerun the t0024
8-direction conditions through the plotter to produce polar/Cartesian PNGs for
results_detailed.md. Small infrastructure change with broad reuse benefit across the DSGC
lineage.

</details>

<details>
<summary><strong>Add a verify_library_asset.py verificator to close the
framework-wide gap flagged during t0024 step 9</strong> (S-0024-05)</summary>

**Kind**: library | **Priority**: low

During t0024 step 9 the library asset structure was validated manually against
meta/asset_types/library/specification.md because no automated verificator exists. The other
asset types (paper, dataset, answer) have dedicated verificators. Add verify_library_asset.py
to arf/scripts/verificators/ enforcing the mandatory fields in library/specification.md
(manifest, source files, citation metadata, entry points) and wire it into the
prestep/poststep cycle for any task that produces a library asset. Framework infrastructure
task, not task-folder work.

</details>

<details>
<summary><strong>Unblock t0023 Hanson 2019 port so REQ-6 cross-comparison can
include 5/5 DSGC models instead of 4/5</strong> (S-0024-06)</summary>

**Kind**: experiment | **Priority**: medium

t0024 step 12 records t0023_port_hanson_2019_dsgc as intervention_blocked
(intervention/deferred_pending_t0022.md). The t0022 task has since completed (DSI 1.000, HWHM
116.25, RMSE 10.48) so the original blocking dependency is resolved. Triage t0023's
intervention file, resume the port, and then retrofit a Hanson 2019 row into the cross-model
comparison table in results_detailed.md of both t0024 and any subsequent DSGC port. Closes the
REQ-6 partial-coverage caveat.

</details>

## Research

* [`research_code.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_summary.md)*

# Results Summary: Port de Rosenroll 2026 DSGC Model

## Summary

Ported the de Rosenroll et al. 2026 DSGC model into a new library asset
`de_rosenroll_2026_dsgc` (NEURON `HHst_noiseless`/`Exp2NMDA`/`cadecay` MOD mechanisms with the
341-section `RGCmodelGD.hoc` morphology, vendored from Zenodo `10.5281/zenodo.17666158` at
commit `a23f642a`). Drove the cell through the paper-native 8-direction protocol and the
project-standard 12-angle protocol under both correlated (`rho=0.6`) and uncorrelated
(`rho=0.0`) AR(2) release-rate noise (20 trials per angle, 800 trials total, ~4h15m wall time
on the local Windows workstation). The port produces strong direction selectivity but **does
not** reproduce the paper's correlation-drop signature; the port-fidelity gate (REQ-5) failed
and the miss is recorded in `intervention/port_fidelity_miss.md` as a first-class finding per
plan step 13.

## Metrics

* **DSI 12-ang correlated** (project-standard, t0004 envelope): **0.7759** — well above
  t0008's 0.316 and matching t0020's 0.7838 / t0022's 1.0 lineage
* **DSI 12-ang uncorrelated**: **0.8557** — *higher* than correlated, opposite of paper
  prediction
* **DSI 8-dir correlated** (paper-match, REQ-5 target [0.30, 0.50]): **0.8182** — FAIL
* **DSI 8-dir uncorrelated** (paper-match, REQ-5 target [0.18, 0.35]): **0.8351** — FAIL
* **Correlation-drop fraction** (target >= 0.20): **0.000** — FAIL
* **Peak firing rate (12-ang correlated)**: **5.15 Hz** — far below t0004 envelope [40, 80] Hz
  (consistent lineage-wide gap; t0008 18.1 Hz, t0020 14.85 Hz, t0022 15 Hz)
* **HWHM (12-ang correlated)**: **68.65 deg** — narrower than t0008 (82.81) and t0022
  (116.25); inside the t0004 envelope around 66 deg
* **Tuning-curve reliability**: **0.9836** — high trial-to-trial consistency
* **RMSE vs t0004 target**: **15.49 Hz** — comparable to t0008 (13.73) and t0022 (10.48)
* **Wall time**: ~4h15m for 800 trials on the local Windows workstation
* **Cost**: $0.00 (no paid services, no remote compute)

## Verification

* `verify_task_dependencies.py` — PASSED (t0008, t0012, t0022 all completed) at check-deps
  step
* `verify_task_file.py` — PASSED at init-folders (0 errors)
* **Port-fidelity gate (REQ-5)** — FAILED (3/3 sub-criteria miss); recorded in
  `intervention/port_fidelity_miss.md` and
  `metrics.json["de_rosenroll_port_fidelity_gate_pass"] = false` per plan step 13. Does not
  block step closure.
* **CSV schema (REQ-3, REQ-4)** — PASSED: 4 CSVs under `data/`, 240 rows for 12-angle and 160
  rows for 8-direction, columns `trial,direction_deg,spike_count,peak_mv`
* **Score report (REQ-3)** — PASSED: `data/score_report.json` populated with all 13 fields
  (loss_scalar 0.99, dsi/hwhm/null/peak residuals, per-target gate)
* **Plots (REQ-3, REQ-4)** — PASSED: 4 PNGs in `results/images/` (polar + Cartesian for both
  12-angle conditions; 8-direction plotting skipped because the t0011/t0012 plotter hardcodes
  N_ANGLES=12)
* **Library asset structure** — PASSED manually against
  `meta/asset_types/library/specification.md` (no automated `verify_library_asset.py` script
  exists; flagged framework-wide gap)
* **Lint / format** — `ruff check --fix . && ruff format .` clean across the task tree

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0024_port_de_rosenroll_2026_dsgc" ---
# Results Detailed: Port de Rosenroll 2026 DSGC Model

## Summary

Built `de_rosenroll_2026_dsgc`, a NEURON-based DSGC port that vendors the upstream MOD
mechanisms (`HHst_noiseless`, `cadecay`, `Exp2NMDA`) and the 341-section `RGCmodelGD.hoc`
morphology from the de Rosenroll et al. 2026 companion repository (Zenodo
`10.5281/zenodo.17666158`, commit `a23f642a`, MIT). Implemented seven Python modules under
`code/` (`paths`, `constants`, `ar2_noise`, `build_cell`, `run_tuning_curve`,
`score_envelope`, `plot_tuning_curves`), compiled `nrnmech.dll` locally, and ran a
four-condition sweep (8-direction and 12-angle, each under correlated `rho=0.6` and
uncorrelated `rho=0.0` AR(2) release-rate noise; 20 trials per angle; 800 trials total). The
port produces strong direction selectivity but does not reproduce the paper's correlation-drop
signature: the REQ-5 port-fidelity gate fails on all three sub-criteria, recorded as a
first-class finding per plan step 13 with a follow-up suggestion to port the full `SacNetwork`
(`bp_locs`, `probs`, `deltas`).

## Methodology

### Machine

* **Host**: local Windows 11 workstation (same as t0008/t0020/t0022 used)
* **CPU**: Intel x86-64; NEURON 8.2 single-threaded
* **GPU**: not used
* **NEURON build**: `nrnmech.dll` compiled locally via the task-local `run_nrnivmodl.cmd`
  wrapper

### Runtime

* **Started**: 2026-04-21T03:18:55Z (implementation step prestep)
* **Completed**: 2026-04-21T08:10:00Z (implementation step poststep)
* **Sweep wall time**: ~4h15m for the full 800-trial four-condition sweep
* **Cost**: $0.00 (no API calls, no remote compute)

### Pipeline

1. Vendored upstream sources into `assets/library/de_rosenroll_2026_dsgc/sources/` (HOC + MOD
   + LICENSE; provenance recorded in `UPSTREAM_NOTES.md`).
2. Built `nrnmech.dll` via `run_nrnivmodl.cmd` (Windows-native NEURON compile).
3. Drove the cell with `code/run_tuning_curve.py` over four (direction-set, correlation)
   combinations, writing per-trial CSVs with columns
   `trial,direction_deg,spike_count,peak_mv`.
4. Scored the 12-angle correlated CSV with `tuning_curve_loss.score` from t0012 against the
   t0004 target envelope.
5. Computed task-local 8-direction DSI for paper-fidelity tracking with `compute_dsi`.
6. Generated polar + Cartesian plots via the t0011 `tuning_curve_viz` library (12-angle only;
   the upstream plotter hardcodes `N_ANGLES=12`).
7. Auto-wrote `intervention/port_fidelity_miss.md` from `score_envelope.py` because all three
   REQ-5 sub-gates failed.

### Algorithms

* **Cell**: `RGCmodelGD.hoc` from upstream — 341 sections (soma, primary dendrites, distal
  dendrites). Channels: `HHst_noiseless` Na/K (densities 150/200/30 mS/cm² Na, 35/40/25 mS/cm²
  K across soma/primary/distal) and `cadecay` (`tau=10 ms`).
* **Synaptic input**: per-terminal Exp2Syn pairs (ACh: `tau1=0.5, tau2=6, e=0`; GABA:
  `tau1=0.5, tau2=35, e=-60`) plus an `Exp2NMDA` voltage-dependent NMDA receptor.
* **Direction selectivity mechanism**: null-biased GABA release probability (asymmetric
  inhibition in the null half-plane), modulated by the AR(2) release-rate process for ACh and
  GABA channels.
* **AR(2) noise**: `phi=(0.9, -0.1)` for both channels; cross-channel correlation set per
  condition (`rho=0.6` for correlated, `rho=0.0` for uncorrelated). Implementation in
  `code/ar2_noise.py` self-tested for empirical autocorrelation and cross-correlation.
* **Bar stimulus**: 250 µm wide, 1 µm/ms, swept across the 1000 ms trial window at the
  assigned angle. 8-direction set: `(0, 45, 90, 135, 180, 225, 270, 315)`. 12-angle set:
  `range(0, 360, 30)`.
* **Spike detection**: threshold-crossings at `-10 mV` at the soma over the 1000 ms window;
  reported as `spike_count` per trial (firing rate Hz = spike_count / 1.0 s).

## Verification

* `verify_task_dependencies.py` — PASSED at check-deps (t0008, t0012, t0022 all completed)
* `verify_task_file.py` — PASSED at init-folders (0 errors, 0 warnings)
* `verify_logs.py` — PASSED across all step folders (skipped-step logs created via
  `skip_step.py` for steps 8/10/11)
* **CSV schema check (REQ-3, REQ-4)** — PASSED: 4 CSVs in `data/`, 240 rows for each 12-angle
  CSV (12 angles × 20 trials), 160 rows for each 8-direction CSV (8 directions × 20 trials),
  columns `trial,direction_deg,spike_count,peak_mv`
* **Score report (REQ-3)** — PASSED: `data/score_report.json` populated with all 13 fields:
  `loss_scalar=0.99`, `passes_envelope=false`, `peak` per-target gate fails, `dsi/hwhm/null`
  pass, `rmse_vs_target=15.49`
* **Port-fidelity gate (REQ-5)** — FAILED on all three sub-criteria (see Analysis below);
  recorded in `intervention/port_fidelity_miss.md` and surfaced as
  `metrics.json["de_rosenroll_port_fidelity_gate_pass"] = false`. Per plan step 13 design,
  this is a first-class finding and does not block step closure.
* **Plots (REQ-3, REQ-4)** — 4 PNGs in `results/images/`; 8-direction plotting deliberately
  skipped because the t0011 plotter library is hardcoded to `N_ANGLES=12`
* **Library asset structure** — confirmed manually against
  `meta/asset_types/library/specification.md` (no automated `verify_library_asset.py` script
  exists — flagged framework-wide gap, not a t0024 defect)
* **Lint / format** — `ruff check --fix . && ruff format .` clean across
  `tasks/t0024_.../code/`; `mypy` excluded by project-wide `pyproject.toml [tool.mypy]
  exclude`

## Metrics Tables

### REQ-5 Port-Fidelity Gate (paper-match 8-direction)

| Sub-criterion | Required | Measured | Result |
| --- | --- | --- | --- |
| DSI 8-dir correlated | [0.30, 0.50] (paper ~0.39) | **0.8182** | FAIL (above ceiling) |
| DSI 8-dir uncorrelated | [0.18, 0.35] (paper ~0.25) | **0.8351** | FAIL (above ceiling) |
| Drop fraction (corr → uncorr) | ≥ 0.20 | **0.000** (uncorr > corr) | FAIL (no drop) |

### REQ-3 t0004 Envelope Score (12-angle correlated)

| Metric | Target | Measured | Residual | Per-target pass |
| --- | --- | --- | --- | --- |
| `direction_selectivity_index` | 0.882 | **0.7759** | -0.107 | PASS |
| `tuning_curve_hwhm_deg` | 66.0 | **68.65** | +2.65 | PASS |
| `null_hz` | 2.0 | **0.65** | -1.35 | PASS |
| `peak_hz` | 32.0 | **5.15** | -26.85 | FAIL |
| `tuning_curve_reliability` | 0.997 | **0.984** | -0.013 | n/a (info) |
| `tuning_curve_rmse` | n/a | **15.49** | n/a | n/a |
| `loss_scalar` | n/a | **0.99** | n/a | n/a |
| `passes_envelope` (all targets) | true | **false** | n/a | FAIL |

### Per-angle mean firing rate (spikes / 1000 ms)

| angle (deg) | 8-dir corr | 8-dir uncorr | 12-ang corr | 12-ang uncorr |
| --- | --- | --- | --- | --- |
| 0 | **5.00** | **4.45** | **5.15** | **4.50** |
| 30 | — | — | 4.45 | 4.05 |
| 45 | 4.20 | 3.25 | — | — |
| 60 | — | — | 3.50 | 2.60 |
| 90 | 1.90 | 1.35 | 2.10 | 0.80 |
| 120 | — | — | 1.05 | 0.30 |
| 135 | 0.85 | 0.25 | — | — |
| 150 | — | — | 0.75 | 0.45 |
| 180 (null) | **0.50** | **0.40** | **0.65** | **0.35** |
| 210 | — | — | 0.75 | 0.30 |
| 225 | 0.85 | 0.45 | — | — |
| 240 | — | — | 0.90 | 0.70 |
| 270 | 1.65 | 0.95 | 1.75 | 1.05 |
| 300 | — | — | 3.10 | 2.15 |
| 315 | 3.80 | 3.10 | — | — |
| 330 | — | — | 4.60 | 3.35 |

## Comparison vs Baselines (REQ-6)

Cross-model lineage comparison on the four registered metric keys (12-angle correlated
condition where applicable):

| Task | Model | DSI | Peak Hz | HWHM deg | Reliability | RMSE Hz |
| --- | --- | --- | --- | --- | --- | --- |
| t0008 | ModelDB 189347 (rotation proxy) | 0.316 | 18.1 | 82.81 | 0.991 | 13.73 |
| t0020 | ModelDB 189347 (gabaMOD swap) | 0.784 | 14.85 | n/a | n/a | n/a |
| t0022 | ModelDB 189347 dendritic (E-I scheduling) | 1.000 | 15.0 | 116.25 | 1.000 | 10.48 |
| t0023 | Hanson 2019 | n/a (intervention_blocked: deferred pending t0022) | — | — | — | — |
| **t0024** | **de Rosenroll 2026 (this port)** | **0.776** | **5.15** | **68.65** | **0.984** | **15.49** |

### Cross-model observations

* **DSI**: the de Rosenroll port (0.776) sits in the upper band of the lineage — close to
  t0020 (0.784) and far above the t0008 rotation proxy (0.316), consistent with the t0008 →
  t0020 → t0022 trajectory of progressively stronger DS mechanisms. It is below the t0022
  dendritic E-I scheduling result (1.000) which is essentially a ceiling.
* **Peak firing rate**: 5.15 Hz is the **lowest** in the lineage (t0008 18.1, t0020 14.85,
  t0022 15.0) and ~7× below the t0004 envelope floor of 40 Hz. The lineage-wide gap reported
  in the t0020 results is reaffirmed and worsens here. Likely cause: the per-terminal Exp2Syn
  driver runs at much lower aggregate conductance than the full SAC varicosity network in the
  upstream Python driver.
* **HWHM**: 68.65 deg is the **narrowest** of the lineage and the only port to land inside the
  t0004 envelope around 66 deg. The narrow tuning is consistent with the strong asymmetric
  GABA inhibition in the null half-plane.
* **Reliability**: 0.984 is the highest non-deterministic value (t0022's 1.000 is
  artifactually perfect because its driver is deterministic). The AR(2) noise process produces
  a realistic level of trial-to-trial variability without destroying tuning structure.
* **t0023 is intervention-blocked** (`status=intervention_blocked`,
  `intervention/deferred_pending_t0022.md`) and was not available for the planned
  cross-comparison. The plan's REQ-6 Hanson port comparison is therefore deferred; t0023's
  outputs will need to be retrofitted into a cross-comparison task once it executes.

## Analysis

### Port-fidelity miss interpretation

Three independent failures characterize the gate miss:

1. **Both correlated and uncorrelated DSI sit at ~0.82-0.84** — high, ceilinged DSI values
   regardless of release-rate correlation structure. The paper reports DSI ~0.39 (correlated)
   and DSI ~0.25 (uncorrelated), implying a moderate, modulable DSI driven by SAC co-release
   timing.
2. **No correlation drop** — uncorrelated DSI (0.835) is fractionally *higher* than correlated
   (0.818). The paper's signature drop fraction of ~36% is replaced by a +2% increase. The
   AR(2) `rho` parameter is wired correctly (verified by the `ar2_noise` self-test), so the
   absence of the effect points at the upstream of the noise process — the per-terminal
   release model rather than the noise itself.
3. **Peak firing rate ~5 Hz** — the entire lineage misses the t0004 peak envelope, but t0024
   misses it by the largest margin (~4× below t0008). The simplified per-terminal Exp2Syn pair
   driver does not appear to deliver enough aggregate ACh excitation to produce
   paper-magnitude firing rates.

### Mechanistic root cause hypothesis

The port deliberately replaced the upstream Python `SacNetwork` (which builds a full SAC
varicosity network with Briggman 2011 connectome-derived `bp_locs`, varicosity-specific
release `probs`, and SAC-soma-relative `deltas`) with a per-terminal Exp2Syn pair driver. The
per-terminal driver captures the *static* asymmetric-inhibition mechanism (null-biased GABA
release probability) but does not capture the *dynamic* spatially-distributed correlation in
SAC release that is the actual substrate of the de Rosenroll correlation-drop effect. With
every SAC terminal independent and release driven by an AR(2) process whose only correlation
is across (ACh, GABA) within a single terminal, there is no spatial-temporal release
correlation to disrupt by setting `rho=0`. The gate therefore fails by construction, not by
implementation defect.

This is exactly the failure mode anticipated in the Risks table of `plan/plan.md` (row 3: "DSI
port-fidelity miss"), and the resolution recipe (port the full `SacNetwork`) is preserved as a
follow-up suggestion in step 14.

### Why DSI is high but peak is low

The null half-plane is suppressed by GABA before any axial spread of ACh excitation can
recruit sodium channels at the soma. The high DSI reflects the very effective null suppression
(~0.5 Hz firing at 180°). However, the preferred half-plane peak is also depressed because the
per-terminal ACh conductance budget is small relative to the upstream SAC-network co-release.
The result is a sharply tuned curve at very low absolute amplitude, equivalent to a
noise-shaped null-suppression gain rather than a paper-faithful direction-selective generator.

## Visualizations

### 12-angle correlated polar tuning curve

![12-angle correlated polar tuning
curve](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang.png)

Strong PD lobe centered near 0° with deep null suppression centered near 180°. HWHM ~69°
matches the t0004 envelope. Note the absolute amplitude of the PD lobe (~5 Hz) versus the
t0004 envelope peak around 32 Hz.

### 12-angle correlated Cartesian tuning curve

![12-angle correlated Cartesian tuning
curve](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang_cartesian.png)

Same data plotted as firing rate vs angle on Cartesian axes; trial-to-trial error bars show
the ~0.5-1.0 Hz noise floor introduced by the AR(2) release-rate process.

### 12-angle uncorrelated polar tuning curve

![12-angle uncorrelated polar tuning
curve](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang_uncorrelated.png)

Tuning shape essentially identical to the correlated condition (DSI 0.856 vs 0.776). The
absence of any visible widening or symmetrization under decorrelation is the central evidence
for the REQ-5 port-fidelity miss.

### 12-angle uncorrelated Cartesian tuning curve

![12-angle uncorrelated Cartesian tuning
curve](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang_uncorrelated_cartesian.png)

Cartesian rendering of the uncorrelated sweep. Side-by-side comparison with the correlated
Cartesian view shows the only meaningful change is a uniform downward shift of the PD
half-plane firing rate by ~0.5 Hz, consistent with reduced co-fluctuation rather than the loss
of a DS substrate.

## Examples

Each example below is one row from the per-trial CSVs. `peak_mv` is the somatic peak voltage
during the trial (high `peak_mv` ≥ ~36 mV indicates spiking; low `peak_mv` < -40 mV indicates
the cell stayed subthreshold).

### Best-PD trials (8-dir correlated, angle 0°)

Verbatim rows from `data/tuning_curves_8dir_correlated.csv`:

```text
trial,direction_deg,spike_count,peak_mv
41028,0.0,6,37.226
51035,0.0,6,37.335
61042,0.0,6,37.113
```

These illustrate the practical PD ceiling: with the per-terminal driver, the cell saturates at
~6 spikes per 1000 ms even on the most favorable seeds. Compare to the t0008 rotation-proxy
port which routinely reached 18 Hz peaks under the same morphology.

### Worst-PD trials (8-dir correlated, angle 0°)

```text
trial,direction_deg,spike_count,peak_mv
191133,0.0,3,36.977
21014,0.0,4,37.227
31021,0.0,4,37.521
```

The PD half-plane has a 2:1 dynamic range across seeds (3-6 spikes), and even worst-case PD
trials spike at the somatic threshold — the variability is in *how many* APs the cell fires,
not whether it spikes at all.

### Null-direction silence (8-dir correlated, angle 180°)

```text
trial,direction_deg,spike_count,peak_mv
3340,180.0,0,-50.688
23354,180.0,0,-48.433
43368,180.0,0,-53.864
```

These illustrate the asymmetric-inhibition mechanism working as designed: in the null
direction the GABA half-plane fires first and clamps the cell well below threshold for the
entire trial.

### Null breakthrough (8-dir correlated, angle 180°, max trials)

```text
trial,direction_deg,spike_count,peak_mv
33361,180.0,2,36.736
13347,180.0,1,36.807
73389,180.0,1,35.249
```

These ~5% of null-direction trials with breakthrough spikes are the source of the residual
mean null firing rate (0.50 Hz at 180° corr) and account for why DSI is 0.82 rather than ~1.0.

### Contrastive: PD same-angle, correlated vs uncorrelated mean

```text
direction  corr_mean  corr_std  uncorr_mean  uncorr_std  delta
0.0        5.00       0.92      4.45         1.00        -0.55   (PD, uniform amplitude reduction)
90.0       1.90       0.79      1.35         0.99        -0.55   (cardinal, same uniform shift)
180.0      0.50       0.61      0.40         0.60        -0.10   (null, no GABA-inhibition rebalance)
270.0      1.65       0.59      0.95         0.76        -0.70   (cardinal, same uniform shift)
```

The uncorrelation effect is a uniform ~0.5 Hz reduction across **all** directions, including
the null. There is no preferential reshaping of PD vs ND lobes — exactly the signature that
would have been needed to satisfy REQ-5.

### Boundary case: HWHM on the 12-angle correlated curve

The polar curve hits half-max (~2.6 Hz) between 60° (3.50 Hz) and 90° (2.10 Hz) on the upper
half, and between 270° (1.75 Hz) and 300° (3.10 Hz) on the lower half. Linear interpolation
gives HWHM ~68.65°, just above the t0004 envelope center of 66°. This is the only metric where
the port lands *inside* the t0004 envelope — so the tuning *shape* is correct even though the
*amplitude* and *correlation modulability* are not.

## Limitations

* **Port-fidelity miss is a structural simplification, not a tuning bug** — the per-terminal
  Exp2Syn driver cannot reproduce the spatially-distributed SAC release correlation that
  drives the de Rosenroll correlation-drop effect. Closing the gap requires porting the full
  upstream `SacNetwork` (Briggman 2011 connectome-derived `bp_locs`, varicosity-specific
  `probs`, SAC-soma `deltas`). This is captured as a follow-up suggestion in step 14.
* **Peak firing rate is far below t0004 envelope** — the entire DSGC lineage in this project
  misses the [40, 80] Hz peak envelope; the de Rosenroll port misses by the largest margin.
  Likely cause: per-terminal aggregate ACh conductance is too low relative to the upstream
  SAC-network co-release. Same `SacNetwork` follow-up would address this.
* **8-direction plots not generated** — the t0011 `tuning_curve_viz` library hardcodes
  `N_ANGLES=12`. The 8-direction CSVs are scored numerically but not plotted. Visualization
  can be added in a future task by parameterizing the t0011 plotter.
* **AIS Nav1.6/Nav1.2 split not implemented** — the `research_papers.md` recommendation for an
  AIS overlay was deliberately dropped because the upstream model has no AIS; adding one would
  change the published biophysics. Captured as a follow-up suggestion in step 14.
* **Sensitivity sweep on Ra/eleak/Na-K densities not run** — the paper text and the upstream
  code disagree; the port uses the code-authoritative values, and a sweep over the paper-text
  alternates is left as future work.
* **No cross-model t0023 (Hanson) data** — t0023 is `intervention_blocked` (deferred pending
  t0022 review), so the planned t0008 / t0020 / t0022 / t0023 / t0024 cross-comparison is
  missing the t0023 row. A future task will need to retrofit Hanson data into the cross-model
  table.
* **Mypy not strictly enforced on task code** — the project-wide `pyproject.toml [tool.mypy]
  exclude = ["tasks/.*/code/", "tasks/.*/assets/"]` removes task code from strict mypy. Lint
  and format are enforced via ruff.

## Files Created

* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/__init__.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/paths.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/score_envelope.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/plot_tuning_curves.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/details.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/description.md`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/run_nrnivmodl.cmd`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/RGCmodelGD.hoc`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/nrnmech.dll`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/LICENSE`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/UPSTREAM_NOTES.md`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/data/tuning_curves_8dir_correlated.csv`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/data/tuning_curves_8dir_uncorrelated.csv`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/data/tuning_curves_12ang_correlated.csv`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/data/tuning_curves_12ang_uncorrelated.csv`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/data/score_report.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/metrics.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_summary.md`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_detailed.md`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/costs.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/suggestions.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/remote_machines_used.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang.png`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang_cartesian.png`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang_uncorrelated.png`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang_uncorrelated_cartesian.png`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/intervention/port_fidelity_miss.md`

## Task Requirement Coverage

Operative task request from `task.json` and `task_description.md`:

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

| ID | Requirement | Status | Answer / evidence |
| --- | --- | --- | --- |
| REQ-1 | Library asset `de_rosenroll_2026_dsgc` with HOC, MOD, morphology, `details.json`, `description.md`, `run_nrnivmodl.cmd` | **Done** | `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/` contains all required files; `nrnmech.dll` compiled locally; structural validity confirmed manually against `meta/asset_types/library/specification.md` |
| REQ-2 | Source paper registered as paper asset | **Done** | `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/` populated by step 5 (research-internet); `details.json` `spec_version="3"`, summary present, paper PDF in `files/` |
| REQ-3 | 12-angle moving-bar tuning curve CSV (canonical schema) and `score_report.json` against t0004 envelope | **Done** | `data/tuning_curves_12ang_correlated.csv` (240 rows); `data/score_report.json` populated with all 13 fields including `loss_scalar=0.99`, per-target gate, residuals; t0011 polar + Cartesian plots in `results/images/` |
| REQ-4 | Paper-match 8-direction tuning curve CSV (separate file) | **Done** | `data/tuning_curves_8dir_correlated.csv` and `data/tuning_curves_8dir_uncorrelated.csv` (160 rows each); 8-direction DSI surfaced in `results/metrics.json` as `de_rosenroll_dsi_correlated_8dir` and `de_rosenroll_dsi_uncorrelated_8dir` |
| REQ-5 | Port-fidelity gate: corr DSI ∈ [0.30, 0.50], uncorr DSI ∈ [0.18, 0.35], drop ≥ 20% | **Not done** (recorded as first-class finding) | All three sub-criteria failed: corr DSI 0.818, uncorr DSI 0.835, drop 0.000. Logged in `intervention/port_fidelity_miss.md`, surfaced in `metrics.json["de_rosenroll_port_fidelity_gate_pass"]=false`, mechanistic root cause analysed above (per-terminal driver vs full SAC network), follow-up suggestion captured for step 14 |
| REQ-6 | Cross-model comparison vs t0008, t0020, t0022, t0023 in `results_detailed.md` | **Partial** | Comparison table above includes t0008/t0020/t0022/t0024 across all four registered metric keys; t0023 is `intervention_blocked` (`status=intervention_blocked`, `intervention/deferred_pending_t0022.md`) and was unavailable. The Hanson row will need to be retrofitted into a cross-comparison task once t0023 executes |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0024_port_de_rosenroll_2026_dsgc" date_compared: "2026-04-21"
---
# Comparison with Published Results

## Summary

The port of [deRosenroll2026] reproduces high direction selectivity (**DSI 0.8182**
correlated, 8-dir) but **does not** reproduce the paper's correlation-drop signature: measured
drop is **0.000** against the published ~**0.36** (correlated **0.39** -> uncorrelated
**0.25**), and both conditions overshoot the paper's DSI envelope. Peak firing rate comes in
at **5.15 Hz** versus the paper's qualitative ~**30-40 Hz** range and the project t0004
envelope of **40-80 Hz** — consistent with the lineage-wide firing-rate gap already seen in
t0008 (**18.1 Hz**), t0020 (**14.85 Hz**), and t0022 (**~15 Hz**). HWHM at **68.65 deg** sits
close to the t0004 target of **68.51 deg**, so the angular sharpness of tuning is matched but
its amplitude and correlation-sensitivity are not.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| deRosenroll2026 (correlated, 8-dir) | DSI | 0.39 | 0.82 | +0.43 | Overshoots paper DSI envelope |
| deRosenroll2026 (uncorrelated, 8-dir) | DSI | 0.25 | 0.84 | +0.59 | Overshoots and inverts drop sign |
| deRosenroll2026 (corr -> uncorr) | DSI drop fraction | 0.36 | 0.00 | -0.36 | Port-fidelity gate REQ-5 miss |
| deRosenroll2026 | Peak firing rate (Hz) | ~30-40 | 5.15 | ~-25 to -35 | Paper range qualitative |
| t0004 target envelope | DSI (12-ang) | 0.8824 | 0.7759 | -0.1065 | Project envelope, correlated |
| t0004 target envelope | HWHM (deg) | 68.51 | 68.65 | +0.14 | Angular sharpness matches |
| t0004 target envelope | Peak firing rate (Hz) | 40-80 | 5.15 | -34.85 (to lower bound) | Lineage-wide gap |
| t0008 rotation proxy (PolegPolsky2016 geom) | DSI (12-ang) | 0.316 | 0.7759 | +0.4599 | Newer geometry + AR(2) noise |
| t0020 gabaMOD swap (PolegPolsky2016 geom) | DSI (12-ang) | 0.784 | 0.7759 | -0.0081 | Near-match on DS magnitude |
| t0022 dendritic E-I scheduling | DSI (12-ang) | 1.000 | 0.7759 | -0.2241 | Different protocol / geometry |

## Methodology Differences

* **Driver architecture**: The port implements per-terminal Exp2Syn excitation and inhibition
  parameterised directly from [dsMicro-GH] `ei_balance.py`. The upstream code also distributes
  the release drive through a spatially-structured `SacNetwork` with `bp_locs`, `probs`, and
  `deltas` that encode per-varicosity release probabilities and temporal offsets. The port
  keeps the per-terminal kinetics and noise but does not instantiate the spatial release
  network — the AR(2) drive is applied at the terminals directly rather than through the
  upstream SAC connectome.
* **Noise process**: AR(2) release-rate noise with `phi = [0.9, -0.1]` and cross-channel `rho`
  swept between **0.6** (correlated) and **0.0** (uncorrelated) is implemented faithfully per
  [dsMicro-GH]. The same seed policy (per-trial integer seed) is used.
* **Temperature / integration**: `celsius = 36.9 C`, `dt = 0.1 ms`, Ca2+ decay `tau = 10 ms`,
  matching the repository code exactly.
* **Biophysics**: Ra 100 Ohm*cm, cm 1 uF/cm^2, gleak 5e-5 S/cm^2, eleak -60 mV, Na (soma /
  primary dendrite / distal) 150 / 200 / 30 mS/cm^2, K 35 / 40 / 25 mS/cm^2, from repository
  code — not paper-text values (paper reports Ra 200, eleak -65, Na 200 / 70 / 35, K 40 / 12 /
  18). The repository values were chosen as authoritative, following the upstream `README`.
* **AIS**: No explicit AIS section is modelled, matching [dsMicro-GH] (gap 2 in
  research-internet). No Nav1.6 / Nav1.2 split was added.
* **Protocol coverage**: The paper uses 8 directions; the project standard is 12. Both
  protocols were run. The port-fidelity gate uses the 8-direction protocol to match the paper
  exactly; the t0004 envelope comparison uses the 12-angle protocol to match prior ports.
* **Trial count**: 20 trials per condition per angle (800 trials total across the four
  condition x protocol combinations), matching the per-angle density in [dsMicro-GH]
  fig-reproduction scripts.

## Analysis

The magnitude-vs-mechanism split in the comparison table is informative. Angular selectivity
in the port is strong and sharp: **DSI 0.78-0.84** across correlated and uncorrelated
conditions with HWHM at the t0004 envelope target. This confirms the static asymmetry in the
deRosenroll per-terminal kinetics — the reversed PD-vs-ND inhibition-to-excitation timing and
the 1.8x GABA scaling — is correctly reproduced by the Exp2Syn drivers. However, the headline
finding of the paper is **not** the absolute DSI value but the **correlation-drop effect**:
correlated SAC release at `rho = 0.6` produces DSI ~**0.39**, and breaking that correlation
down to `rho = 0.0` collapses DSI to ~**0.25**, a ~**36%** drop. The port shows essentially
zero drop (**0.000** fraction, -0.002 absolute) because the correlation is applied at
individual Exp2Syn drivers rather than across the spatially-distributed SAC release network
that the paper shows is the causal substrate of the effect.

The **peak firing rate shortfall** (**5.15 Hz** vs paper ~**30-40 Hz** and t0004 **40-80 Hz**)
is a lineage-wide signature already present in t0008 (**18.1 Hz**), t0020 (**14.85 Hz**), and
t0022 (**~15 Hz**). It is therefore not caused by this port alone, but the port is the first
in the lineage to also be fully biophysical and still hit this low a rate — earlier ports used
spatial rotation, gabaMOD swaps, or hand-scheduled E/I with simpler integration. The most
probable cause is the single-compartment Na/K density regime (150/200/30 mS/cm^2) being below
the saturating spike rate even when integrator delivers peak voltage; a paper-value override
sweep (Na 200/70/35, K 40/12/18) is a reasonable follow-up.

The **angular sharpness match** (HWHM **68.65 deg** vs t0004 **68.51 deg**, delta **+0.14**)
is a non-trivial positive finding: despite the firing-rate miss and the correlation-drop miss,
the geometry of the tuning curve is correctly reproduced. This suggests the morphology import
(341-section `RGCmodelGD.hoc`) and the per-terminal inhibitory-excitatory asymmetry capture
the spatial filtering correctly; the missing ingredient is the **temporally-distributed SAC
varicosity drive** that makes the circuit sensitive to release correlation in the first place.

## Limitations

* **The port-fidelity gate is a composite criterion.** REQ-5 requires all three sub-criteria
  (corr DSI band, uncorr DSI band, drop >=20%) to pass. The port misses all three. The gate
  miss is a first-class finding per plan step 13, not a scoring bug.
* **No published numeric HWHM or per-angle tuning profile** was available in the paper text or
  [dsMicro-GH] `README`, so the HWHM comparison is against the project's own t0004 envelope
  (derived from t0022 and independent Hanson / Poleg-Polsky priors) rather than a
  deRosenroll-derived value.
* **Peak firing rate range (~30-40 Hz) is qualitative**: no explicit paper figure pins the
  peak rate numerically. The comparison table uses the midpoint of the plausible range.
* **The paper's 8-direction protocol cannot be plotted with the t0011 polar/Cartesian
  plotter**, which hardcodes `N_ANGLES = 12`. Figures for the 8-direction conditions are
  present only as raw CSVs, not PNGs.
* **Cross-model row for t0023_port_hanson_2019_dsgc is absent** from the comparison because
  t0023 is `intervention_blocked` pending t0022. REQ-6 cross-comparison coverage is partial
  (4/5 models).
* **Absolute DSI inflation on uncorrelated trials** (port 0.84 vs paper 0.25) may partly
  reflect the absence of any positive intra-varicosity mechanism that causes uncorrelated
  release to degrade selectivity — the port's uncorrelated drive still preserves the
  per-terminal PD/ND kinetic asymmetry, so DS survives. Fixing this likely requires adding the
  spatial release network so that uncorrelated release creates per-subunit DSI degradation.
* **A Nav1.6 / Nav1.2 AIS overlay was not added**, per research-internet gap 2. Whether this
  would raise peak firing rate into the t0004 envelope is not tested in this task.

</details>
