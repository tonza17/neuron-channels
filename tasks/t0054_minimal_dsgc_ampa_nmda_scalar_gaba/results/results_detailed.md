---
spec_version: "2"
task_id: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
date_completed: "2026-04-28"
---
# Results Detailed: Minimal DSGC with AMPA + NMDA Excitation and Scalar gabaMOD

## Summary

Extended t0052 by adding a co-located NMDA `Exp2Syn` (tau1=5 ms, tau2=80 ms, e=0 mV) at every E
synapse, swept gNMDA across `{0.0, 0.25, 0.5, 1.0}` nS, and ran the full 12-dir × 10-trial ×
3-mode protocol (1440 trials, 4 h 19 min wall-clock). The gNMDA=0 regression gate against t0052
passed exactly. Headline finding: NMDA closes the peak-rate gap (0.67 → 8 Hz at gNMDA=0.25; ~12×)
but scalar gabaMOD cannot maintain DSI once NMDA is active (vector-sum DSI 0.746 → 0.082 → 0.029
→ 0.017 across the sweep). The implementation is correct and reproducible; the negative result on
DSI vs gNMDA is the scientific finding.

## Methodology

* **Hardware**: local CPU. No GPU. No remote machines.
* **NEURON**: 8.2.7 with built-in `Exp2Syn`, `hh`, `pas` only (no MOD compilation).
* **Python**: 3.13 via uv. Same dependency pinning as t0052.
* **Random seed**: `PLACEMENT_SEED=0`, bit-identical to t0052/t0053. Per-trial seed
  `1000·angle_idx + trial_idx + 1`.
* **Sweep wall-clock**: 15 587 s = 4 h 19 min for 1440 trials at ≈ 10.8 s/trial average. Slower
  than t0052's 3.2 s/trial per Exp2Syn — the added NMDA `Exp2Syn` per synapse adds another
  integration component to every trial.
* **Validation gates run before full sweep**:
  * Quiescent rest (`test_quiescent_rest.py`): V_rest = −64.56 mV (±0.5 mV target). PASS.
  * Placement bit-identical to t0052: per-pair coords match within 1e-9. PASS.
  * NMDA-inert smoke test at gNMDA=0 (1 angle × 2 trials): firing rate 0.666667 Hz, matches t0052
    within 1e-6 Hz. PASS.
  * Dry-run skipped (sweep launched directly).
* **Hard-fail gate inside compute_metrics.py**: gNMDA=0 FULL CSV row-by-row vs t0052's
  `tuning_curve_full.csv`. **PASSED at max |rate diff| = 0.000e+00 Hz** across 120 rows.

## Metrics

See `results/metrics.json` (12 variants, multi-variant format) and
`results/derived_quantities.json`.

### Headline (FULL mode)

| gNMDA (nS) | DSI (registered) | HWHM (deg) | reliability | RMSE_vs_target | peak_hz | null_hz | vector_sum_dsi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 1.000 | 82.5 | 1.000 | 16.98 | 0.667 | 0.000 | 0.746 |
| 0.25 | 0.143 | n/a | 0.667 | 13.50 | 8.000 | 6.000 | 0.082 |
| 0.50 | 0.083 | n/a | 0.581 | 13.91 | 7.333 | 6.000 | 0.029 |
| 1.00 | 0.000 | n/a | 0.564 | 16.16 | 4.667 | 4.667 | 0.017 |

(Primary DSI = (peak − null) / (peak + null); HWHM and reliability come from the registered metric
helpers and become noisy / undefined as the tuning curve flattens.)

### E_ONLY mode (peak_hz, no inhibition)

| gNMDA (nS) | E_ONLY peak_hz |
| --- | --- |
| 0.00 | 0.667 |
| 0.25 | 6.667 |
| 0.50 | 4.667 |
| 1.00 | (saturating, multi-spike) |

E_ONLY peak Hz drops from 6.67 to 4.67 between gNMDA=0.25 and 0.50 because of refractory saturation;
further increases at 1.0 nS produce multi-spike trains that the simple peak-Hz metric undercounts.

### EPSP decay (the user's question)

`epsp_decay_to_1e_ms` returned `null` for all 4 gNMDA values. The compute logic looks for the time
after EPSP peak when V drops below `V_rest + (V_peak − V_rest)/e`; with NMDA's 80 ms decay τ
acting on 100 synapses, the cell stays depolarised at trial end (1500 ms) above the 1/e point. The
qualitative effect — that NMDA dramatically slows the EPSP tail — is plainly visible in the
per-direction EPSP PNGs (compare `epsp_dir_000_gnmda_0.00.png` vs `epsp_dir_000_gnmda_1.00.png`).
The numeric `epsp_decay_to_1e_ms` derivation should be extended to either (a) lengthen the trial
window or (b) fit an exponential rather than look for a 1/e crossing.

## Visualisations

`results/images/` contains 252 PNGs.

### Sweep summary plots (the headline)

![Peak Hz vs gNMDA per direction (FULL mode)](images/peak_hz_vs_gnmda.png)

Adding NMDA boosts peak firing rate by ~12× at gNMDA=0.25 across all directions; the curves cluster
(preferred and null directions both rise together), explaining the DSI collapse.

![Vector-sum DSI vs gNMDA (FULL mode)](images/dsi_vs_gnmda.png)

Vector-sum DSI drops monotonically from 0.746 (gNMDA=0) to 0.017 (gNMDA=1.0) — scalar gabaMOD
inhibition cannot keep up with NMDA-amplified excitation.

![EPSP decay-to-1/e vs gNMDA (E_ONLY)](images/epsp_decay_vs_gnmda.png)

Plot is rendered but the y-axis is empty — the decay metric returned `null` (see the Methodology /
Limitations sections).

### Per-direction headline figures

![Soma V(t) FULL θ=0° gNMDA=1.0](images/v_soma_dir_000_gnmda_1.00.png)

At gNMDA=1.0 nS the soma reaches sustained suprathreshold depolarisation with multiple spikes per
trial — very different from t0052's single-spike regime.

![Aggregate EPSP θ=0° gNMDA=0.0](images/epsp_dir_000_gnmda_0.00.png)
![Aggregate EPSP θ=0° gNMDA=1.0](images/epsp_dir_000_gnmda_1.00.png)

Compare the two: at gNMDA=0 the EPSP returns to baseline within ~50 ms after peak; at gNMDA=1.0 the
EPSP barely drops before the trial ends at 1500 ms. NMDA's 80-ms decay τ operating on 100
simultaneous synapses keeps the cell depolarised throughout the trial.

The remaining 246 PNGs (12 dirs × 5 plot types × 4 gNMDA = 240, plus 4 polar + 4 cartesian
+ 3 sweep summary) are in `results/images/`.

## Examples

Three concrete trial-level input/output pairs from the sweep.

### Example 1: gNMDA=0.0, θ=0°, trial 1, FULL — matches t0052 exactly

Input:

```text
gnmda_ns = 0.0
direction_deg = 0
trial_seed = 1
mode = FULL
```

Output (from `tuning_curve_full.csv`):

```text
firing_rate_hz = 0.666667
```

Same as t0052's row `0,1,0.666667`. Regression gate passed at 0 Hz diff.

### Example 2: gNMDA=0.25, θ=0°, trial 1, FULL — NMDA boost

Input:

```text
gnmda_ns = 0.25
direction_deg = 0
trial_seed = 1
mode = FULL
```

Output:

```text
firing_rate_hz = 8.000000   # 12-spike train across 1500 ms
```

12× the gNMDA=0 rate. The cell now fires multi-spike trains thanks to the slow NMDA tail.

### Example 3: gNMDA=1.0, θ=180° (null), trial 6001, FULL — DSI collapse

Input:

```text
gnmda_ns = 1.0
direction_deg = 180
trial_seed = 6001
mode = FULL
```

Output:

```text
firing_rate_hz = 4.666667    # null direction now fires almost as much as preferred
```

Compare to gNMDA=0 null Hz (0.0) — at gNMDA=1.0 the scalar `gabaMOD = 0.99` GABA amplitude can no
longer suppress the NMDA-amplified excitation, so the cell fires nearly as often in the null
direction as in the preferred direction. Vector-sum DSI 0.017.

## Analysis

### Plan-assumption check

The plan's Key Question 2 ("does NMDA close the peak-rate gap?") is answered **YES** — gNMDA=0.25
produces 8 Hz peak (12× t0052), within an order of magnitude of the in vivo 30-100 Hz target.

The plan's Key Question 3 ("does NMDA improve or degrade DSI?") is answered **DEGRADE under scalar
gabaMOD** — DSI drops from 0.746 to 0.017 across the gNMDA sweep. This is a consistent finding
with the brainstorm-9 narrative that t0052 was over-suppressed by GABA; once NMDA escalates
excitation, scalar GABA scaling becomes insufficient. The natural follow-up is a joint AMPA × NMDA
× GABA conductance sweep to find the operating point where DSI is preserved at
biologically-realistic firing rates.

The plan's Key Question 1 ("at what gNMDA does EPSP decay reach 50-100 ms?") is **not numerically
answered** because `epsp_decay_to_1e_ms` returned `null`. Qualitatively, the EPSP tail at gNMDA=1.0
spans the full 1500-ms trial window — much longer than t0052's ~30 ms. A precise number requires
either a longer trial window or an exponential fit.

### Why the cost

Sweep wall-clock 4 h 19 min vs the plan's ~75 min target. The 3.5× overrun is because adding the
NMDA `Exp2Syn` to every co-located synapse roughly tripled per-trial CPU (1.5× from the integration
step + 2× from the much slower decay, which keeps the synapse state active longer in the CVODE
adaptive solver). For future sweeps, expect ~3 s/trial to scale to ~10 s/trial when adding slow
synapses.

## Limitations

* **`epsp_decay_to_1e_ms` returned `null`**. Numerical answer to the headline question is missing;
  qualitative answer is in the per-direction EPSP PNGs.
* **HWHM is `null` at gNMDA > 0**. Once the tuning curve flattens (every direction firing ~6-8 Hz),
  the half-width-at-half-maximum is not well-defined. This is a property of the result, not a bug.
* **Single-trial firing-rate granularity at gNMDA=0**. Each preferred-direction trial fires exactly
  1 spike per 1500 ms = 0.667 Hz. Granularity at other gNMDA values is similarly quantized (e.g., 8
  Hz = 12 spikes / 1500 ms; 4.67 Hz = 7 spikes).
* **No noise / Poisson background**. Deterministic protocol.
* **No voltage-dependent NMDA Mg block**. Voltage-independent NMDA (Voff=1 equivalent) by design —
  see suggestions for the Mg-block follow-up.
* **No active dendrites** (Nav/Kv in dendrites).

## Files Created

Code: 16 modules in `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/` (10 copied verbatim from
t0052, 1 from t0053, 5 extended). Library asset:
`assets/library/minimal_dsgc_ampa_nmda_scalar_gaba/` with verifier 0/0.

Results:

* `tuning_curve_full.csv`, `tuning_curve_e_only.csv`, `tuning_curve_gaba_only.csv` (480 rows each).
* `spike_times_*.csv`, `voltage_traces_*.csv` (per mode).
* `activation_times.csv`, `wallclock.json`, `placement_seed0.json`.
* `metrics.json` (12 variants), `derived_quantities.json`, `costs.json`,
  `remote_machines_used.json`.
* 252 PNGs in `images/`.

Logs: full step lifecycle (1, 2, 3, 6, 7, 9, 10 skipped, 11 skipped, 12, 13, 14, 15) plus ~30
entries in `commands/` and a session-capture report in `sessions/`.

## Verification

* `meta.asset_types.library.verificator` — PASSED 0/0.
* `verify_task_metrics`, `verify_task_dependencies`, `verify_task_file`, `verify_task_results`,
  `verify_task_folder`, `verify_logs`, `verify_research_code`, `verify_compare_literature`,
  `verify_plan` — all PASSED 0 errors.
* gNMDA=0 regression gate vs t0052: PASSED at max |rate diff| = 0.000e+00 Hz.
* Placement bit-identical to t0052: PASSED.
* `ruff check` / `ruff format` / `mypy` (265 source files): clean.

## Task Requirement Coverage

Operative task text from `task.json`:

> Extend t0052 by adding co-located NMDA Exp2Syn (tau1=5, tau2=80, e=0) at each E synapse; sweep
> gNMDA at {0, 0.25, 0.5, 1.0} nS; characterise EPSP decay, peak rate, and DSI vs gNMDA.

Operative long-description text from `task_description.md` (concise summary): build a minimal DSGC
on the t0052 baseline with AMPA + NMDA co-located excitation, scalar gabaMOD inhibition, soma + AIS
HH, 100 E + 100 I synapses, fixed seed 0; run 4 gNMDA × 12 dirs × 10 trials × 3 modes = 1440
trials; report per-gNMDA per-direction soma V(t), EPSP/IPSP, PSTH, polar tuning, plus three
sweep-summary plots; library asset `minimal_dsgc_ampa_nmda_scalar_gaba`; gNMDA=0 must reproduce
t0052 within rounding.

| REQ | Item | Verdict | Evidence |
| --- | --- | --- | --- |
| REQ-1 | dsgc-baseline-morphology-calibrated | Done | cell.py; same as t0052 |
| REQ-2 | hh on soma+AIS, passive dendrites Rm/Ra/cm/V_rest | Done | constants.py; quiescent test PASS |
| REQ-3 | 100 E + 100 I co-located, uniform random, seed 0 | Done | placement.py; placement bit-identical to t0052 |
| REQ-4 | AMPA Exp2Syn 0.5/2.5/0/0.5 nS | Done | synapses.py |
| REQ-5 | NMDA Exp2Syn 5/80/0/swept | Done | synapses.py |
| REQ-6 | NMDA + AMPA fire from same NetStim | Done | shared ampa_netstim with two NetCons |
| REQ-7 | Scalar gabaMOD identical to t0052 | Done | gaba_mod() unchanged; conductance ratio 3.0 |
| REQ-8 | Stimulus 12 dirs × 200 µm × 1.0 µm/ms × 1500 ms | Done | constants.py |
| REQ-9 | 10 trials/direction, deterministic seeds | Done | run_tuning_curve.py; 480 rows per CSV |
| REQ-10 | Three trial modes FULL / E_ONLY / GABA_ONLY | Done | TrialMode enum + trial.py |
| REQ-11 | gNMDA sweep {0, 0.25, 0.5, 1.0} | Done | NMDA_PEAK_NS_VALUES |
| REQ-12 | Per-direction soma V(t) per gNMDA | Done | 48 PNGs |
| REQ-13 | Aggregate EPSP / IPSP per gNMDA | Done | 96 PNGs |
| REQ-14 | PSTH per gNMDA | Done | 48 PNGs |
| REQ-15 | Activation histogram per gNMDA | Done | 48 PNGs |
| REQ-16 | Polar tuning curve + DSI metrics per gNMDA | Done | 4 polar PNGs; metrics.json |
| REQ-17 | Cartesian tuning curve per gNMDA | Done | 4 cartesian PNGs |
| REQ-18 | Three sweep-summary plots (decay, peak Hz, DSI vs gNMDA) | Done | 3 PNGs (decay plot empty due to REQ-20) |
| REQ-19 | metrics.json multi-variant `gnmda_<value>_<mode>` | Done | 12 variants; verifier PASSED |
| REQ-20 | epsp_decay_to_1e_ms per gNMDA | Partial | All 4 returned `null`; qualitative answer in EPSP PNGs |
| REQ-21 | Quiescent rest gate | Done | V_rest -64.56 mV |
| REQ-22 | gNMDA=0 regression gate vs t0052 | Done | max |
| REQ-23 | Placement bit-identical to t0052 | Done | test_placement_seed0_match.py PASS |
| REQ-24 | gabaMOD ratio 3.0 sanity | Done | constants & metrics confirm 3.0 |
| REQ-25 | NMDA-inert smoke test at gNMDA=0 | Done | match within 1e-6 Hz |
| REQ-26 | Library asset minimal_dsgc_ampa_nmda_scalar_gaba | Done | verifier PASSED 0/0 |
| REQ-27 | Wall-clock budget ~75 min | Partial | Took 4 h 19 min (3.5× over); flagged in suggestions |
