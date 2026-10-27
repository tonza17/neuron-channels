---
spec_version: "2"
task_id: "t0131_rd1_na_k_remodelling_dsgc_dsi"
date_completed: "2026-10-27"
status: "complete"
---
# Plan: rd1-like Na/K Remodelling of the DSGC Model and Its Effect on DSI

## Objective

Test, with local NEURON simulations of the project's Bed B compartmental direction-selective
ganglion cell (DSGC, 68-d parameter vector), whether scaling the soma and axon-initial-segment (AIS)
voltage-gated Na and K conductances reproduces the researcher's FVB/N rd1 versus mature wild-type
(WT) phenotype (`research/inputs/SomeResults.pdf`, panels A-C), and what that remodelling does to
signed antipodal direction-selectivity index, DSI = (PD - ND) / (PD + ND). Also reproduce or refute
the researcher's panel D toy model (saturating input-output curve and temporally smeared output of
rd1-like cells) first as a minimal rate model and then in the NEURON model.

Success means: (1) per-cell rd1-like (s_Na, s_K) scalings fitted from voltage-clamp data only; (2)
an out-of-sample report of +60 pA evoked firing and a tonic-bias spontaneous-firing result for
WT-like and rd1-like cells; (3) signed DSI, PD rate and ND rate for WT-like and rd1-like (with and
without bias) on 8 reference cells plus a DSI-versus-(s_Na, s_K) heatmap; (4) a verdict (reproduced,
partly reproduced, disproved) for each panel D prediction; (5) one answer asset answering the five
Key Questions; (6) all required charts in `results/images/`; (7) the registered metric
`direction_selectivity_index` in `results/metrics.json` as explicit variants.

Calibration targets (read by eye from the PDF, approximate; replace if the researcher supplies exact
traces and record the change):

| Panel | WT | rd1 |
| --- | --- | --- |
| A: spontaneous, 2 s | near silent | about 14 spikes in 2 s (about 7 Hz), irregular or bursty, about 60 mV tall |
| B: +60 pA step, 500 ms | about 4 adapting spikes (about 8 Hz), peaks about 90, 70, 65 mV | almost no spiking, small blips at onset |
| C: +100 mV voltage step, about 340 ms | sustained outward about 2 nA, early inward Na transient | sustained outward about 3.5 nA (about 1.7x), much smaller inward transient |

The PDF panel C trace begins at 0 nA before the step, so its y axis is a baseline-subtracted current
and its x axis is "time from voltage step onset (ms)". The step lasts about 340 ms.

## Task Requirement Checklist

Operative task text (task name, short description and the long description file
`tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/task_description.md`), quoted:

```text
Task: rd1-like Na/K remodelling of the DSGC model and its effect on DSI
Short description: Calibrate soma/AIS gNa and gK scaling to rd1 vs WT clamp data, test if it
predicts rd1 firing, measure signed DSI, and reproduce or refute the panel-D toy model.

Reference cells: 5-10 LEGIT high-DSI cells drawn with a fixed seed from the t0121 pooled parquet.
List the chosen cell IDs. Evaluator: reuse the signed antipodal DSI evaluator and cell_params.jsonl
per-cell parameter dump from t0129. Conditions: WT-like (scale 1.0 on gNa and gK) and rd1-like
(scaling from Part 1) for every reference cell.

Part 1: 1. Replicate the +100 mV voltage step at the soma on each reference cell. 2. Sweep soma plus
AIS gNa scale (0.25-1.0x) against gK scale (1-3x) on a grid of at least 6 x 6. 3. Choose the
rd1-like scaling that matches the sustained-current ratio (~1.7x) and the reduced inward transient.
Set the scaling from clamp data only; do not use any firing data. 4. Report the fitted scalings per
cell and their spread across cells.

Part 2: 1. With the Part 1 scalings, run the +60 pA, 500 ms step for WT-like and rd1-like cells
(out-of-sample test: report whether evoked firing collapses). 2. For panel A, add a weak tonic bias
current or noise at rest (exploratory; state exactly what was used and how it was tuned). Check
whether rd1-like cells fire irregularly at ~7 Hz while WT-like cells stay near silent. 3. Report
f-I curves, spike amplitude, adaptation index and spontaneous rate for both conditions. 4. If soma
and AIS scaling alone does not reproduce the phenotype, add a second arm that also scales dendritic
channels and rerun Parts 1-2 for that arm.

Part 3: 1. Run the standard protocol for WT-like and rd1-like cells: HH on, 8 directions, fixed
1400 ms trials. Use the EPSP_PASSIVE / IPSP_PASSIVE / FULL mode trio only where the existing
protocol calls for it. 2. Report signed antipodal DSI, PD rate and ND rate per cell and condition,
with and without the tonic bias from Part 2. 3. Produce a DSI-versus-scaling heatmap over the Part 1
gNa x gK grid.

Part 4: Panel D toy model. Same input (three Gaussian pulses at about 180, 430 and 680 ms over 1000
ms) drives WT-like and rd1-like cells. Predictions: WT output grows gradually with input strength
(0-100, reaching ~15); rd1 output flat and saturated (~23) at all but the lowest strengths. WT output
cleaner and stimulus-locked; rd1 elevated baseline (~0.35), broader, less distinct peaks. Steps: 1.
Build the simple toy model and check it reproduces panel D; if not reproducible from the description,
say so and list what is missing. 2. Test both predictions in the NEURON model: sweep PD synaptic
drive strength and compare WT-like and rd1-like output curves; drive both with the three-pulse input
and compare baseline, stimulus-locking and peak distinctness. 3. State for each prediction whether
it is reproduced, partly reproduced or disproved.

Key Questions: 1. Does Part 1 yield rd1-like scalings that reproduce the panel C current ratio on
all reference cells? 2. Do those scalings, with no firing data in the fit, collapse evoked firing at
+60 pA? 3. Can a tonic bias give ~7 Hz irregular spontaneous firing in rd1-like but not WT-like
cells? 4. Does rd1-like remodelling raise, lower or leave unchanged signed DSI, and does the answer
depend on the tonic bias? 5. Does the compartmental model reproduce the panel D saturation and
temporal-smearing predictions?

Expected outputs: charts in results/images/ embedded in results_detailed.md (panel C replication,
gNa x gK calibration grid, current-clamp traces and f-I curves, signed DSI / PD / ND by condition and
DSI heatmap, panel D toy and NEURON); one answer asset covering questions 1-5; per-cell parameter
dump and results tables in data/; registered metric direction_selectivity_index (signed) reported per
condition as variants. Local CPU only, $0.
```

Requirements:

* **REQ-1**: Choose 5-10 LEGIT reference cells with a fixed seed from the t0121 pooled parquet, list
  the cell IDs. Satisfied by Steps 2-3; evidence `data/reference_cells.jsonl` and the cell ID table
  in `results_detailed.md`. Ambiguity: the parquet has no parameter vectors, so vectors are rebuilt
  from the source dumps (Step 2).
* **REQ-2**: Reuse the signed antipodal DSI evaluator and the `cell_params.jsonl` dump protocol of
  t0129 (Steps 5, 10); evidence `data/cell_params.jsonl` and `code/evaluator.py`.
* **REQ-3**: WT-like (1.0, 1.0) and rd1-like (Part 1 scaling) conditions for every reference cell
  (Steps 8, 9, 10, 11).
* **REQ-4**: Part 1.1, replicate the +100 mV step at the soma on each cell (Step 7); evidence
  `data/clamp_traces.npz` and chart `images/panel_c_clamp_traces.png`.
* **REQ-5**: Part 1.2, gNa (0.25-1.0) x gK (1-3) grid of at least 6 x 6 (Step 8); evidence
  `data/clamp_grid.csv` and `images/calibration_grid.png`.
* **REQ-6**: Part 1.3, choose rd1-like scaling matching the sustained ratio about 1.7 and the
  reduced transient, from clamp data only (Step 8); evidence `data/fitted_scalings.json` plus a
  code-level assertion that no firing quantity is read in `code/calibration.py`.
* **REQ-7**: Part 1.4, fitted scalings per cell and spread (Step 8); evidence table in
  `results_detailed.md` and `images/fitted_scalings.png`.
* **REQ-8**: Part 2.1, +60 pA, 500 ms step, WT-like vs rd1-like, out-of-sample (Step 9); evidence
  `images/current_clamp_traces.png`, `data/cc_step_summary.csv`.
* **REQ-9**: Part 2.2, tonic bias or noise at rest, tuned and described exactly (Step 10); evidence
  `data/bias_tuning.csv`, `images/spontaneous_traces.png`.
* **REQ-10**: Part 2.3, f-I curves, spike amplitude, adaptation index, spontaneous rate for both
  conditions (Steps 9, 10); evidence `data/fi_curves.csv`, `images/fi_curves.png`.
* **REQ-11**: Part 2.4, dendritic-scaling second arm, run if the soma+AIS arm fails the pre-defined
  phenotype criteria (Step 12); evidence `data/arm_decision.json` stating whether the arm was
  triggered and why, and arm outputs when triggered.
* **REQ-12**: Part 3.1-3.2, standard protocol, 8 directions, 1400 ms, signed antipodal DSI, PD and
  ND rate per cell and condition, with and without bias (Step 11); evidence `data/dsi_results.csv`,
  `images/dsi_by_condition.png`. Ambiguity: the EPSP/IPSP/FULL trio is not in the existing Bed B
  evaluator; the plan runs the FULL mode only (see Approach).
* **REQ-13**: Part 3.3, DSI-versus-scaling heatmap over the Part 1 grid (Step 11); evidence
  `data/dsi_heatmap.csv`, `images/dsi_heatmap.png`.
* **REQ-14**: Part 4.1, toy model reproducing panel D or a statement of what is missing (Step 13);
  evidence `images/panel_d_toy_model.png`, `data/toy_params.json`.
* **REQ-15**: Part 4.2, NEURON input-strength sweep and three-pulse drive comparison (Step 14);
  evidence `images/panel_d_neuron_sweep.png`, `images/panel_d_neuron_pulses.png`.
* **REQ-16**: Part 4.3, verdict per prediction (Step 14); evidence `data/panel_d_verdicts.json`.
* **REQ-17**: Key Questions 1-5 answered in one answer asset (Step 16); evidence
  `assets/answer/<answer_id>/`.
* **REQ-18**: Registered metric `direction_selectivity_index` as explicit variants in
  `results/metrics.json` (Step 15).
* **REQ-19**: All required charts in `results/images/` (Step 15) and per-cell parameter dump and
  tables in `data/` (Steps 2-14).
* **REQ-20**: Local CPU only, no remote machines, $0 (all steps; Cost Estimation).

## Approach

**Model and what is scaled.** Bed B cell = 68-d vector: 54-d electrophysiology plus 14-d morphology.
The cell is built by (a) `split_68d_vector` and `morphology_params_from_vector`, (b)
`generate_fixed_morphology` and `insert_baseline_channels` from the t0092 library (mandatory: the
unpatched t0090 generator gives a zero-area soma and NaN voltage), (c) `apply_parameter_vector` from
the t0080 library, (d) `setup_synapses_parametric` for DSI runs only. Sections: soma `soma_t90`, AIS
`ais_proximal_t90` and `ais_distal_t90`, dendrites. Na/K mechanisms (S/cm2, all `*t80` are
NONSPECIFIC_CURRENT with erev Na 50 mV, K -85 mV, so they do not enter the `ina`/`ik` pools;
per-channel current = sum of the range variable `i_<suffix>`, plus `ina`/`ik` for `HHst`):
`nav16t80` (soma, AIS, dendrites; median soma 0.85, AIS 2.5 in LEGIT cells), `napt80` (persistent
Na, soma and dendrites), `nart80` (resurgent Na, uniform), `HHst` gnabar 0.12 / gkbar 0.036 at MOD
defaults everywhere including the AIS and NOT in the 68-d vector, `kdrt80` (uniform on soma and
dendrites, median 0.36), `kv4t80` (A-type, uniform, 0.47), `kv3t80` (soma 0.22, AIS 0.11), `kv7t80`
(M-type), and Ca-activated K (`bkt80`, `skt80`, `skahpt80`).

**Scaling definition (base arm "soma+AIS").** Applied after `apply_parameter_vector`, to sections
`soma_t90`, `ais_proximal_t90`, `ais_distal_t90` only: `gbar_nav16t80` and `HHst.gnabar` are
multiplied by `s_Na`; `gbar_kdrt80`, `gbar_kv3t80`, `gbar_kv4t80` and `HHst.gkbar` are multiplied by
`s_K` (only the mechanisms inserted on a given section are touched). Decision, documented in the
results: `HHst` IS scaled (research recommends it because it is a fixed Na/K background that would
otherwise blunt the scale); `napt80`, `nart80`, `kv7t80`, Ca-activated K and all dendrite channels
stay fixed in the base arm. The AIS term dominates the Na scaling because AIS Na density is several
times the soma density (literature: AIS about 7x soma). **Dendritic arm** (fallback, Step 12): the
same factors are additionally applied to all dendrite sections (`nav16t80`, `HHst`, `kdrt80`,
`kv4t80`, `kv3t80`) and `napt80`.

**Part 1 (voltage clamp, fitted without firing data).** `h.SEClamp` at `soma(0.5)` with series
resistance 0.001 MOhm (pattern from t0063 `run_step.py`), no synapses. Protocol: 50 ms hold at
`V_HOLD = -65 mV` (the model resting potential is about -60 to -65 mV), then 340 ms at
`V_STEP = V_HOLD + 100 = +35 mV`, then 60 ms back at hold. Documented assumption: the panel C axis
says "delta V +100 mV", so the step is an increment of 100 mV above holding; a sensitivity check
repeats the clamp with an absolute step to +40 mV for two cells. Observables on the baseline-
subtracted (pre-step hold current) membrane current, sign positive outward (verify the sign of
`seclamp.i` in a unit test: K current at +35 mV must come out positive): sustained current = mean
over the last 50 ms of the step; transient inward = minimum current in the first 5 ms after step
onset (negative number; amplitude = its absolute value). Also logged per channel: Na (sum of
`i_nav16t80`, `i_napt80`, `i_nart80`, `HHst ina`) and K sums, for soma versus AIS segments
separately. Targets: sustained ratio S(s_Na,s_K)/S(1,1) = 1.7 and transient ratio T(s_Na,s_K)/T(1,1)
= 0.25 (the PDF shows rd1 transient at roughly a quarter or less of WT; "much smaller" is not
numerically defined, so 0.25 is an explicit assumption, with a sensitivity band 0.15-0.35 reported).
Loss = ((S_ratio - 1.7)/0.1)^2 + ((T_ratio - 0.25)/0.1)^2 on the grid
`s_Na in {0.25, 0.40, 0.55, 0.70, 0.85, 1.00}` x `s_K in {1.0, 1.4, 1.8, 2.2, 2.6, 3.0}` (36 points
plus the (1,1) reference, which lies in the grid), followed by a refinement: bilinear interpolation
of the log ratios on the grid and `scipy.optimize.minimize` inside the grid box, then one direct
verification clamp run at the refined point. Absolute currents (WT about 2 nA in the PDF) are
reported but not fitted (soma-only space clamp; the model's absolute amplitude depends on cell
size); the SEClamp controls only the soma, so AIS and dendritic Na escapes clamp control: this
limitation is documented and mirrors the recorded whole-cell data. The fit code must not read any
spike or firing quantity (enforced by structure: `code/calibration.py` imports nothing from the
current-clamp module, and a unit test checks that).

**Part 2 (current clamp, out of sample).** `h.IClamp` at `soma(0.5)`, no synapses, 100 ms delay, 500
ms duration, amplitudes 0, 20, 40, 60, 100, 200, 400, 800 pA (the +60 pA step is the out-of-sample
test; the larger amplitudes distinguish Na-loss collapse from depolarisation block, break currents
in the literature are 369-792 pA). Spike threshold -10 mV upward crossing (`AP_THRESHOLD_MV`).
Outputs: spike count, first-100 ms and last-200 ms rates, adaptation index = 1 - (last-200-ms rate /
first-100-ms rate), spike peak amplitude (mV), spike FWHM (ms), rheobase (smallest tested amplitude
giving at least 1 spike), break current (amplitude at which rate falls). Collapse criterion declared
up front: evoked firing "collapses" in rd1-like when spike count at +60 pA is at most 1 and at least
3 fewer than WT-like (WT-like should give about 4; if WT-like itself gives under 2 spikes at +60 pA
the comparison is reported as uninformative). Spontaneous activity: 2 s at rest with no synapses;
tonic bias = DC `IClamp` of `I_bias` plus Gaussian white noise current of standard deviation
`sigma_noise` (a second IClamp whose `amp` is driven by an `h.Vector` through `Vector.play(..., dt)`
at dt 0.1 ms, noise seed fixed per cell). Tuning rule (rd1-like only, WT never used to tune): grid
`I_bias in {0, 5, 10, 15, 20, 30, 40, 50} pA` x `sigma_noise in {0, 5, 10} pA` on 3 rd1-like cells;
choose the combination whose mean rate is closest to 7 Hz with ISI coefficient of variation above
0.5 (irregular); then apply the SAME (`I_bias`, `sigma_noise`) to WT-like cells of all reference
cells and report the WT-like rate (prediction: below 1 Hz). If no combination meets both criteria it
is reported honestly; the "any form that works" freedom is used only if this rule fails
(alternatives: Ornstein-Uhlenbeck noise with tau 20 ms; per-cell bias; a negative result is a valid
answer to Key Question 3).

**Part 3 (DSI).** Copy and trim the t0129 evaluator (`_run_one_trial`, `_summarise_trials`,
`evaluate_68d_vector`; drop pymoo, MI and ATP code) to `code/evaluator.py`; add (a) scale factors
(`s_Na`, `s_K`, arm) applied after `apply_parameter_vector` (and the worker cell cache keyed on
scales), (b) optional bias IClamp for the whole 1400 ms trial, (c) the silence rule change below.
Protocol facts to preserve: `TSTOP_MS = 1400`, `DT_MS = 0.1`, `V_INIT_MV = -60`,
`CELSIUS_DEG_C = 36.9`, `AP_THRESHOLD_MV = -10`, moving-bar synaptic drive with AR(2) noise
(`RHO_CORRELATED = 0.6`), `PD_DIRECTION_DEG = 0`, ND = 180; directions `angle = d*360/8`. Signed
antipodal DSI uses only 0 and 180 deg; the 8 directions give the polar tuning curves (preferred
direction rate, polar plot). The Bed B evaluator has no HH-off mode and the existing protocol has no
EPSP_PASSIVE/IPSP_PASSIVE trio, so only FULL (all channels on) is run, as the task allows. Silence
rule: the t0129 evaluator returns DSI = -1.0 when summed PD spikes are below 3; this plan changes
it: DSI = `None` when PD + ND spikes sum to 0, otherwise DSI is computed from the counts and a
boolean `low_count` (PD spikes below 3 over seeds) and the raw PD/ND spike counts are always stored;
in aggregates, `None` DSIs are excluded from means and counted separately ("n_undefined").

**Part 4.** (a) Toy model: because the PDF gives only output curves, not equations, the
"reproduction" is by construction of a minimal model whose parameters are fitted to numbers read
from panel D; what it tests is whether a simple mechanism (rd1: raised baseline, higher gain, early
saturation, slower smoothing; WT: low baseline, low gain, gradual) can produce both panel D facts,
not whether the paper's authors used that model. Concrete model: static nonlinearity
`f(u) = b + R_max * u^n / (u^n + K^n)` (Naka-Rushton) with WT-like `b = 0`, `R_max` about 30, `K`
about 100, `n = 1` (gives about 15 at u = 100, gradual), rd1-like `b` about 10 (the PDF rd1 curve
starts at about 10 at u = 0 and reaches 23 by u about 5), `R_max` about 13, `K` about 1, `n = 1`;
temporal stage: leaky rate integrator `tau dr/dt = -r + f(g * s(t))`, where `s(t)` = sum of three
Gaussians of sigma 20 ms centred at 180, 430 and 680 ms over 0-1000 ms normalised to peak 1,
`tau_WT` about 12 ms, `tau_rd1` about 40 ms, rd1 output normalised so the elevated baseline is about
0.35 and WT about 0 (the PDF plots "relative signal"). Parameters are fitted with
`scipy.optimize.least_squares` to the by-eye anchor points listed in `code/constants.py` (WT: 0 at
0, about 15 at 100, about 10 at 50; rd1: about 23 for u >= 5; baseline 0.35; peak heights about 0.9,
0.85, 0.8). If the fit cannot hit all anchors (for example, if peak distinctness of rd1, defined
below, cannot be matched together with baseline 0.35), the plan records exactly which anchors failed
and which missing information (equation, normalisation, units of "RGC spike output") prevented it.
(b) NEURON test: PD synaptic drive strength u in {0, 5, 10, 20, 30, 50, 75, 100} where 100 equals
the standard drive: event weights of the excitatory (ACh) synapses in the synapse bundle are
multiplied by u/100 (documented; alternative parameterisation by release probability checked on one
cell if the first shows ambiguity); output = mean PD-direction spike rate (Hz), 3 seeds, 3 cells,
WT-like and rd1-like with the tuned bias (and without as a second series). Three-pulse test: replace
the moving-bar event rate by `rate(t) = r_peak * s(t)` (r_peak = peak excitatory rate in the
standard PD bar trial, no inhibitory change) over 1000 ms, 10 repetitions per condition with
different noise seeds, PSTH in 10 ms bins smoothed with a 20-ms Gaussian, normalised to the input
peak. Metrics, defined before looking at results: saturation index = rate(u = 20)/rate(u = 100)
(prediction: rd1 at least 0.9, WT at most 0.6), baseline = mean normalised PSTH in the windows 0-100
and 900-1000 ms (prediction: rd1 about 0.35, WT about 0), peak distinctness = (mean peak height -
mean minimum between peaks)/mean peak height (prediction: rd1 clearly lower than WT), peak FWHM (rd1
broader), stimulus-locking = Pearson correlation of PSTH with the input. Verdict rule: "reproduced"
if both the direction and at least half the predicted magnitude hold in the median of cells,
"partly" if direction holds only, or holds in some cells; "disproved" if opposite or absent.

**Alternatives considered.** (1) Fit gNa and gK directly to firing (rejected: would use the very
data the out-of-sample test needs). (2) Voltage-clamp-based scaling of all channels including
dendrites first (rejected as default: task prescribes soma+AIS first; kept as the Step 12 fallback).
(3) A full 8 x 36-direction DSI heatmap (about 7 core-hours, rejected; reduced to 5 cells x 2
directions x 2 seeds). (4) Recompiling MOD files to add scaling (rejected: scaling through existing
`gbar_*` parameters needs no recompilation; recompilation failed on this workstation in t0129). (5)
A literature-grounded pacemaker (HCN, T-type Ca) for spontaneous firing (rejected: not in the model;
bias is an explicit network surrogate).

**Task types.** `experiment-run`, `data-analysis`, `comparative-analysis` (as in `task.json`). The
experiment-run guidelines drove an explicit hypothesis list (H1: s_Na about 0.4-0.6 with s_K about
1.5-2 gives the 1.7x ratio; H2: the same scalings collapse +60 pA firing with no firing data in the
fit; H3: a bias gives about 7 Hz irregular firing in rd1-like but not WT-like cells only if rd1-like
threshold or input resistance differs; H4: rd1-like signed DSI is lower than WT-like, mostly with
bias; H5: panel D saturation appears in the compartmental model only with bias), named independent
variables (`s_Na`, `s_K`, bias, arm, direction) and dependent variables (currents, rates, DSI), and
the metric-variants decision. The comparative-analysis guidelines drove a paired design (the same
cells under WT-like and rd1-like), tests declared up front (Wilcoxon signed-rank on per-cell DSI,
two-sided, alpha 0.05, plus bootstrap 95% CI of the median paired difference with 10,000 resamples;
reference-cell n is 8 so results are described as exploratory), and the metrics-variants format.
`efficiency_*` metrics are not measured: no training or per-item inference benchmark is part of this
task (deliberate omission).

**Reference cells (REQ-1).** The t0121 parquet
`tasks/t0121_5seed_substrate_rate_canonical_report/results/data/pooled_legit_jointpass_cells.parquet`
has 675 rows and only the columns `seed`, `source_task_id`, `generation`, `dsi`, `pd_rate_hz`,
`cell_id` (counts: `t0114_seed7755` 484, `t0106_seed44` 121, `t0115_seed9354` 63, `t0112_seed77` 7).
The 68-d vectors are in the source dumps (top-level key `evaluations`, per record `vector_68d`,
`generation`, `dsi_vector_sum`, `pd_rate_hz`):
`tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`,
`tasks/t0112_t0106_seed77_replicate/results/data/all_evaluations_seed77.json.gz`,
`tasks/t0114_seed7755_no_autostop/results/data/all_evaluations_seed7755.json`,
`tasks/t0115_seed9354_no_autostop/results/data/all_evaluations_seed9354.json`. LEGIT rule:
`0.5 <= dsi_vector_sum < 0.9999` and `pd_rate_hz >= 30.0`; de-duplicate per seed on the exact 68-d
tuple in file order; `cell_id = f"{seed_label}_{seq:04d}"` with `seq` counting kept records from 0
(copy `is_legit_joint_pass`, `cell_vector_key`, `load_evaluations` from t0121 `code/loaders.py` and
the logic of `csv_writers.py::build_pooled_legit_cells`). Assert the rebuilt 675 `cell_id`s equal
the parquet `cell_id`s and each record's `dsi_vector_sum` equals the parquet `dsi`. Do NOT use the
t0129 `cell_params.jsonl` as a LEGIT source (it has zero cells with PD rate at or above 30 Hz).
Sampling: 8 cells, stratified by seed with `numpy.random.default_rng(131)`: 3 from `t0114_seed7755`,
2 from `t0106_seed44`, 2 from `t0115_seed9354`, 1 from `t0112_seed77` (LEGIT cells cluster in one
basin, 72% from seed 7755, so equal weighting avoids a redundant draw). If a sampled cell crashes or
is unstable, replace it by the next draw from the same stratum and log it. The parquet `dsi` is a
vector-sum DSI (2 directions, 3 seeds); the WT-like condition is therefore re-evaluated with the
signed antipodal evaluator rather than trusting it.

**MOD library loading (no writes outside the task folder).** `nrnmech.dll` under
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/` is gitignored and absent in the
worktree. A byte-identical tracked copy exists at
`tasks/t0107_t0106_polar_8dir_recheck/code/mods/nrnmech.dll`. Step 1 copies it to
`tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/code/build/nrnmech.dll` (the `build/` folder is
gitignored so the copy is not committed; the loader re-copies it if missing). `code/mech_loader.py`
loads, in this order, the t0024 vendored DLL
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/nrnmech.dll`
(`HHst`, `cad`, `Exp2NMDA`) and then the t0131 `code/build/nrnmech.dll` (13 `*t80` channels) with
`h.nrn_load_dll(str(path))`, asserting the return code is 1.0 and that `h.nav16t80` style mechanism
names exist. Do not import `ensure_t80_dll_loaded` from the t0080 library (it uses the t0080 path);
do not modify any other task folder.

**Parallelism and compute design.** `os.cpu_count()` is 8; use
`MAX_WORKERS = max(1, cpu_count - 1) = 7` with `concurrent.futures.ProcessPoolExecutor` and an
initializer that loads the DLLs once per worker process (one NEURON instance per process). Cache
keys include the scales, so each job rebuilds the cell (0.22 s). A 1400 ms DSI trial takes about 9 s
(measured in research on a LEGIT cell with Na recorders; set `record_ina_for_atp=False`/drop
recorders to speed it up). Budget (core-seconds): DSI main run = 8 cells x 4 conditions x 8
directions x 3 seeds = 768 trials x 9 s about 6,900 core-s (about 16 min at 7 workers); heatmap = 36
grid points x 5 cells x 2 directions (0, 180) x 2 seeds = 720 trials about 6,500 core-s (about 16
min); this subsampling replaces the full 7.2 core-hour version. Clamp and current-clamp runs have no
synapses and are short (assumed 2-5 s each, to be measured in the Step 7 timing gate).

**Code conventions.** Follow `arf/styleguide/python_styleguide.md`: all paths in `code/paths.py`,
constants in `code/constants.py`, frozen slots dataclasses (no tuples), keyword arguments for 2+
heterogeneous parameters, absolute imports
`from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.<module> import ...`, `None` for missing data,
Pydantic at JSON edges, tqdm for long loops, argparse for scripts. Tasks must not import other
tasks' code; only the registered libraries t0024, t0080, t0090, t0092 may be imported (via
`tasks.<id>.code.<module>`); everything else is copied.

## Cost Estimation

Total **$0.00**. All runs are local CPU NEURON simulations on this Windows workstation (8 cores,
NEURON 8.2.7 in the project venv). No Vast.ai machines, no paid APIs, no LLM-judge calls. Project
budget `project/budget.json`: total $100, per-task default limit $8; about $32.84 remains; this task
uses none of it. No cost cap is needed beyond the invariant that the plan never provisions a remote
machine; if wall-clock exceeds 8 hours the implementation agent stops and subsamples further rather
than renting compute.

## Step by Step

**Milestone A: infrastructure and reference cells (Steps 1-4).**

1. **Create `code/paths.py` and `code/constants.py`, copy the MOD library and write
   `code/mech_loader.py`.** `paths.py` defines `TASK_ROOT`, `REPO_ROOT`, `DATA_DIR`
   (`tasks/t0131.../data`), `RESULTS_DIR`, `IMAGES_DIR`, `BUILD_DIR` (`code/build`), the four
   source-dump paths, the t0121 parquet path, the t0107 DLL path and the t0024 DLL path.
   `constants.py` holds protocol constants (`TSTOP_MS = 1400.0`, `DT_MS = 0.1`, `V_INIT_MV = -60.0`,
   `CELSIUS_DEG_C = 36.9`, `AP_THRESHOLD_MV = -10.0`, `V_HOLD_MV = -65.0`,
   `V_STEP_DELTA_MV = 100.0`, `CLAMP_*_MS`, grids, target ratios 1.7 and 0.25, `RNG_SEED = 131`),
   copied slices of t0129 `constants_electrophys.py` / `constants_morphology.py` (`ParamIndex` is
   imported from the t0080 library, not copied), and string constants for section names. Copy the
   t0107 DLL to `code/build/nrnmech.dll`. `mech_loader.py::load_mechanisms()` loads t0024 then t0131
   DLLs and asserts rc 1.0. Run
   `uv run python -X utf8 -c "from ... import load_mechanisms; load_mechanisms()"` wrapped in
   `run_with_logs`. Expected: no exception, `h.nrnversion()` prints 8.2.7. Satisfies REQ-20 (and
   prerequisites of all others).

2. **Rebuild the cell-to-vector table: `code/reference_cells.py`.** Copy `load_evaluations`,
   `is_legit_joint_pass`, `cell_vector_key` from t0121 `code/loaders.py` and the dedup/id logic from
   `csv_writers.py::build_pooled_legit_cells`. Read the four dumps, apply the LEGIT rule,
   de-duplicate, assign `cell_id`. Assert the 675 ids and DSI values match the t0121 parquet
   (`pandas.read_parquet` with explicit dtype checks). Output `data/legit_vectors_675.jsonl` is NOT
   written (size); keep the table in memory. Expected: stratum counts 484/121/63/7 and zero
   mismatches. Satisfies REQ-1.

3. **Draw and persist the 8 reference cells (`code/draw_reference_cells.py`).** Stratified draw with
   `numpy.random.default_rng(131)` as in Approach; write `data/reference_cells.jsonl` with one JSON
   line per cell: `cell_id`, `seed_label`, `source_task_id`, `param_vector` (68 floats),
   `dsi_vector_sum`, `pd_rate_hz`. Print the 8 IDs. Satisfies REQ-1, REQ-2 (dump protocol keys).

4. **Copy and trim the cell builder and evaluator.** Create `code/generator_wrapper.py` (copy of
   t0129 `generator_wrapper.py`: `split_68d_vector`, `morphology_params_from_vector`,
   `hash_morphology_vector`, `build_cell`, `_LIVE_CELLS`; imports from the t0092 and t0090
   libraries), `code/trial_helpers_private.py` (copy of `_bar_arrival_times`,
   `_rates_with_ar2_noise`, `_rates_to_events`, `_gaba_prob_for_direction`, `_count_spikes` and the
   constants they need, from t0080/t0129 `trial_helpers.py`), and `code/evaluator.py` (copy of t0129
   `evaluator.py` keeping `TrialResult`, `CellEvalResult`, `_run_one_trial`, `_summarise_trials`,
   `evaluate_68d_vector`, `_ensure_worker_cell`, `_ensure_synapse_bundle`; drop
   `BedBV3MorphProblem`, pymoo, MI/ATP). Import `apply_parameter_vector`, `ParameterVector`,
   `setup_synapses_parametric`, `SynapseBundle` from
   `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code...`. Modify: add
   `scales: ChannelScales | None` and `bias: BiasSpec | None` parameters, cache key includes scales,
   DSI is `float | None`, add `low_count`, raw `pd_spikes`/`nd_spikes`. Identity gate: with scales
   (1.0, 1.0) `gbar_*` values on every section equal those from `apply_parameter_vector` exactly
   (unit test, Step 6). Satisfies REQ-2.

**Milestone B: scaling and clamp code, tests (Steps 5-6).**

5. **`code/scaling.py`.** Define
   `@dataclass(frozen=True, slots=True) class ChannelScales: s_na: float; s_k: float; arm: ScalingArm`
   (enum `SOMA_AIS`, `SOMA_AIS_DENDRITE`) and
   `apply_channel_scales(*, cell, scales) -> ScalingReport` that multiplies, per section group, the
   mechanisms listed in Approach (`setattr(seg, f"gbar_{suffix}", old * s)` per segment, and
   `seg.gnabar_HHst` / `seg.gkbar_HHst`, only if the mechanism is inserted) and returns a report
   (dataclass listing section, mechanism, old and new totals) for the per-cell parameter dump.
   Satisfies REQ-3, REQ-6.

6. **`code/clamp.py`, `code/test_scaling.py`, `code/test_clamp.py`, `code/test_dsi_rules.py`.**
   `clamp.py`: `run_voltage_clamp(*, cell, v_hold_mv, v_step_mv, scales) -> ClampResult` with
   `SEClamp` at `soma(0.5)` (rs 0.001), 50 ms hold, 340 ms step, 60 ms hold, recorders for
   `seclamp._ref_i`, `soma(0.5)._ref_v`, `t`, and per-channel current sums split by soma vs AIS;
   `run_current_clamp(*, cell, amp_na, delay_ms, dur_ms, tstop_ms, bias) -> CcResult` with the
   IClamp and spike detection; spike metrics helpers (`count_spikes`, `spike_peak_mv`,
   `spike_fwhm_ms`, `adaptation_index`, `isi_cv`). Tests (run with
   `uv run pytest tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/code -v`): scaling identity at (1,1);
   scaling at (0.5, 2.0) halves soma/AIS `gbar_nav16t80` and doubles `gbar_kdrt80` while leaving
   dendrite densities unchanged in the base arm; current-sign check (outward K current at +35 mV
   positive); DSI rule (silent condition returns `None`, never -1.0; `low_count` flag); a structural
   test that `calibration.py` does not import `clamp.run_current_clamp` or read spike fields; spike
   metric helpers on synthetic traces. Expected: all tests pass. Satisfies REQ-4, REQ-6, REQ-12.

**Milestone C: Part 1 calibration (Steps 7-8).**

7. **[CRITICAL] Replicate the +100 mV clamp on every reference cell
   (`code/run_clamp_baseline.py`).** For each of the 8 cells run WT-like (1,1) and the +100 mV step
   (V_HOLD -65 to +35 mV). Save `data/clamp_traces.npz` (time, current, per-channel sums, per cell)
   and a per-cell row in `data/clamp_baseline.csv` (sustained nA, transient nA, rest Vm). Timing
   gate: print seconds per run; if above 10 s, reduce recorders or use CVode with `dt = 0.025`
   before Step 8. Validation gate: baseline comparison is the zero-current trivial baseline and the
   panel C WT shape; for each cell confirm (i) transient is negative (inward) and larger in
   magnitude than 0.2 nA, (ii) sustained is positive; if either fails for a cell STOP and inspect
   that cell's trace and per- channel currents before the grid. Inspect 3 cell traces as images.
   Also run the sensitivity check (absolute step to +40 mV) on 2 cells. Satisfies REQ-4.

8. **[CRITICAL] 6 x 6 gNa x gK clamp grid, fit and per-cell scalings (`code/calibration.py`,
   `code/run_clamp_grid.py`).** For each of 8 cells x 36 grid points run the clamp (a `--limit 1`
   cell dry run first; expect about 36 x 3 s about 2 min), write `data/clamp_grid.csv` (`cell_id`,
   `s_na`, `s_k`, `sustained_na`, `transient_na`, `sustained_ratio`, `transient_ratio`). Fit as in
   Approach (loss on ratios, grid argmin, bilinear refinement in log space, verification run).
   Record per cell `s_na_fit`, `s_k_fit`, achieved sustained and transient ratios, loss, and whether
   the achieved sustained ratio is within +/-0.15 of 1.7 (Key Question 1: "all reference cells"
   means all 8 pass this tolerance). Report spread (mean, SD, min, max, IQR) and note the
   transient-ratio band sensitivity (0.15 and 0.35). Write `data/fitted_scalings.json`. Failure
   condition: if the grid cannot reach a sustained ratio of 1.7 within the s_K range 1-3 for any
   cell (maximum achievable sustained ratio below 1.55), do not proceed silently: record the cell as
   failed and trigger the dendritic arm (Step 12) for Part 1. Chart: `images/calibration_grid.png`
   (two heatmap panels per example cell plus the median over cells: sustained ratio and transient
   ratio over s_Na x s_K, fitted point marked), `images/panel_c_clamp_traces.png` (WT-like vs
   rd1-like traces for 3 cells, nA versus ms), `images/fitted_scalings.png` (per-cell fitted s_Na
   and s_K). Satisfies REQ-5, REQ-6, REQ-7, REQ-3.

**Milestone D: Part 2 current clamp (Steps 9-10).**

9. **[CRITICAL] Out-of-sample current clamp (`code/run_current_clamp.py`).** For each cell run
   WT-like and rd1-like (per-cell fitted scalings from `data/fitted_scalings.json`) at amplitudes 0,
   20, 40, 60, 100, 200, 400, 800 pA, 500 ms step with 100 ms delay and 100 ms tail (tstop 700 ms;
   no synapses). Write `data/cc_step_summary.csv` (`cell_id`, `condition`, `amp_pa`, spike count,
   rates, adaptation, peak mV, FWHM) and `data/fi_curves.csv`. Gate: `--limit 1` cell first; the
   trivial reference is the 0 pA run (must give 0 spikes; if WT-like at 0 pA fires, STOP and
   inspect: the cell is spontaneously active without drive); read 5 individual traces (WT-like +60,
   rd1-like +60, WT-like 800, rd1-like 800, 0 pA) and confirm the spike detection counts match the
   visual peaks. Apply the collapse criterion from Approach and write the verdict per cell
   (collapsed / not collapsed / uninformative) in `data/cc_collapse_verdict.json`. Charts:
   `images/current_clamp_traces.png` (+60 pA, 3 cells, WT-like vs rd1-like, mV versus ms) and
   `images/fi_curves.png` (mean +/- SD across cells, both conditions). Satisfies REQ-8, REQ-10,
   REQ-3.

10. **Spontaneous activity and bias tuning (`code/run_spontaneous.py`).** Run (a) 2 s at rest, no
    bias, WT-like and rd1-like for all 8 cells (3 noise seeds); (b) bias tuning grid on 3 rd1-like
    cells, 18 combinations, tuning rule from Approach; (c) apply the chosen common bias and noise to
    all 8 cells, both conditions, 3 noise seeds each; report rate, ISI CV and spike amplitude. Write
    `data/bias_tuning.csv`, `data/spontaneous_summary.csv`, `data/chosen_bias.json` (including the
    exact `I_bias`, `sigma_noise`, noise seed and tuning criterion). Gate: no-bias rd1-like rate
    below 0.5 Hz is a legitimate result (and expected); inspect 2 voltage traces of the tuned
    rd1-like condition to check that the spikes are real (peak above 0 mV) and not noise crossings.
    Chart: `images/spontaneous_traces.png` (2 s traces WT-like vs rd1-like at the chosen bias, 2
    cells, and a rate-versus-bias curve for both conditions). Satisfies REQ-9, REQ-10.

**Milestone E: Part 3 DSI (Step 11) and arm decision (Step 12).**

11. **[CRITICAL] Signed DSI runs and heatmap (`code/run_dsi.py`, `code/run_dsi_heatmap.py`).** Gate
    first (`--limit 1`): WT-like of cell index 0, 8 directions, 1 seed; the trivial baseline is DSI
    = 0 (no preference); WT-like PD rate must be within 25% of the recorded `pd_rate_hz` of that
    cell and signed DSI must exceed 0.3 (the LEGIT rule guarantees vector-sum DSI >= 0.5; t0129 saw
    lower signed DSI for non-LEGIT cells); if either fails, STOP, read the per-trial spike counts
    for 0 and 180 deg and the synapse bundle construction and debug before any batch. Read 5 trial
    spike counts individually and verify the direction mapping (PD = 0 deg gets the larger count).
    Main run: conditions `wt_like`, `rd1_like`, `wt_like_with_bias`, `rd1_like_with_bias` (bias =
    chosen common bias, applied as whole-trial IClamp), 8 cells, 8 directions, 3 seeds (eval seeds
    from `SEED_BASE`), 7 workers, about 16 min. Per cell and condition write to
    `data/dsi_results.csv` and `data/cell_params.jsonl` (t0129-compatible keys plus `condition`,
    `s_na`, `s_k`, `pd_spikes`, `nd_spikes`, `pd_rate_hz`, `nd_rate_hz`, `dsi_signed` or null,
    `low_count`, `n_errors`; `cell_idx` is NOT used as a key because it was always 0 in t0129; use
    `cell_id` plus `condition`). Statistics: per-cell paired differences rd1_like minus wt_like (and
    with-bias), Wilcoxon signed-rank (two-sided, alpha 0.05, undefined DSI pairs dropped and
    counted), bootstrap CI of the median difference (10,000 resamples, seed 131). Heatmap: 36 grid
    points (the Part 1 grid) x 5 cells (first 5 of the reference list covering all strata) x
    directions 0 and 180 x 2 seeds, written to `data/dsi_heatmap.csv` with signed DSI and PD rate
    (None where undefined) and plotted as `images/dsi_heatmap.png` (median over cells, plus the
    PD-rate heatmap beside it, fitted points overplotted). Charts: `images/dsi_by_condition.png`
    (per-cell paired lines for DSI, PD rate and ND rate, 4 conditions), `images/polar_tuning.png`
    (8-direction spike counts, WT-like vs rd1-like, 3 cells). Satisfies REQ-12, REQ-13, REQ-2,
    REQ-3.

12. **Arm decision and dendritic arm (`code/run_arm_decision.py`).** Write `data/arm_decision.json`.
    The dendritic arm is triggered if ANY of: (a) Step 8 failure condition; (b) the base arm does
    not collapse +60 pA firing on at least 6 of 8 cells under the collapse criterion; (c) the tuned
    bias cannot give rd1-like 4-10 Hz with ISI CV above 0.5 while WT-like stays below 1 Hz. If
    triggered, rerun Steps 7-10 for the `SOMA_AIS_DENDRITE` arm (clamp grid, fit, current clamp,
    spontaneous) on all 8 cells with the same code (arm flag) and Step 11 main run (not the heatmap)
    on 5 cells, writing outputs with an `_dendritic` suffix, and report the two arms side by side
    (`images/arm_comparison.png`). If not triggered, the file records the three tests with values
    and "not triggered". Satisfies REQ-11.

**Milestone F: Part 4 panel D (Steps 13-14).**

13. **Toy model (`code/toy_model.py`, `code/run_toy_model.py`, `code/test_toy_model.py`).**
    Implement the Naka-Rushton plus leaky-integrator toy model of Approach as pure functions
    (`rate_static(*, u, params)`, `simulate_pulses(*, params, tstop_ms, dt_ms)`), fit parameters to
    the by-eye anchors in `constants.py` with `scipy.optimize.least_squares`, write
    `data/toy_params.json`, and report which anchors are matched within 20% and which are not
    (`data/toy_anchor_check.json`) together with a short list of missing information (equations,
    units of "RGC spike output", normalisation of "relative signal"). Tests: WT saturation index
    below 0.6 and rd1 at least 0.9 on the fitted parameters; rd1 baseline between 0.25 and 0.45; WT
    baseline below 0.05. Chart `images/panel_d_toy_model.png` (three panels mimicking panel D:
    input, input-output curve, pulse responses). Satisfies REQ-14.

14. **[CRITICAL] NEURON test of the panel D predictions (`code/run_panel_d_neuron.py`).** On 3 cells
    (one per major stratum: seeds 7755, 44, 9354), conditions `wt_like` and `rd1_like`, each with
    and without the tuned bias: (a) PD input-strength sweep u in {0, 5, 10, 20, 30, 50, 75, 100}
    with excitatory synaptic weight scaled by u/100, 3 seeds, PD direction only, 1400 ms trials (8 x
    3 x 4 x 3 = 288 trials, 288 x 9 s = 2,600 core-s, about 6 min at 7 workers); validate first with
    `--limit` one cell, u = 100 and u = 0, 1 seed: u = 100 must reproduce the WT-like PD rate of
    Step 11 within 10% (baseline comparison) before running the sweep; (b) three-pulse drive with 10
    repetitions of 1000 ms trials per condition per cell (3 x 4 x 10 = 120 trials). Compute
    saturation index, baseline, peak distinctness, FWHM and stimulus-locking correlation as defined
    in Approach, write `data/panel_d_neuron_sweep.csv`, `data/panel_d_neuron_pulses.csv`,
    `data/panel_d_verdicts.json` (one verdict per prediction: saturation/flatness, WT gradual
    growth, elevated baseline, temporal smearing; each reproduced, partly reproduced or disproved,
    with the numbers and the rule that gave it). Individual-output inspection: look at 3 PSTH plots
    and 5 raw trial spike lists before accepting the verdict. Charts
    `images/panel_d_neuron_sweep.png` and `images/panel_d_neuron_pulses.png`. Satisfies REQ-15,
    REQ-16.

**Milestone G: outputs (Steps 15-16).**

15. **Metrics and charts (`code/build_metrics.py`, `code/build_charts.py`).** Write
    `results/metrics.json` in the explicit variant format (read
    `arf/specifications/metrics_specification.md` and
    `arf/specifications/task_results_specification.md` first): variants `wt-like`, `rd1-like`,
    `wt-like-with-bias`, `rd1-like-with-bias` (plus `rd1-like-dendritic` and `wt-like-dendritic`
    only if the arm ran), each with `dimensions`
    `{"scaling": ..., "tonic_bias": true|false, "arm": "soma_ais"|"soma_ais_dendrite"}` and
    `metrics`
    `{"direction_selectivity_index": <median over cells of signed DSI, or null if undefined for all>}`.
    Cell-level undefined DSIs are excluded and the count reported in `data/dsi_results.csv` (column
    `n_undefined`). Other registered metrics (`tuning_curve_*`) are not measured (no tuning curve
    fit; deliberate omission); `efficiency_*` omitted as stated. Ensure every chart named in Steps
    8-14 exists in `results/images/` (copy from the IMAGES_DIR constant if charts were written
    elsewhere), at 150 dpi minimum, axes labelled with units. Satisfies REQ-18, REQ-19.

16. **Answer asset (`code/build_answer.py`).** Create
    `assets/answer/does-rd1-like-na-k-remodelling-of-the-dsgc-model-reproduce-the-rd1-phenotype-and-change-dsi/`
    (ID matches `^[a-z0-9]+(-[a-z0-9]+)*$`; shorten if needed) with `details.json` (spec_version
    "2", `answer_methods` `["code-experiment", "papers"]`, `source_task_ids`
    `["t0121_5seed_substrate_rate_canonical_report", "t0129_t0126_signed_dsi_real_rates_1seed"]`,
    `source_paper_ids` the DOI-slug IDs of Werginz2024 `10.1523_JNEUROSCI.1592-24.2024`,
    Goethals2020 `10.1101_2020.09.15.297937`, Dhingra2004 `10.1523_jneurosci.5346-03.2004`,
    Oesch2005 `10.1016_j.neuron.2005.06.036`, Schachter2010 `10.1371_journal.pcbi.1000899`,
    MargolisDetwiler2007 `10.1523_jneurosci.0130-07.2007`, categories from `meta/categories/`,
    `confidence` set from the evidence), `short_answer.md` (sections `## Question`, `## Answer` 2-5
    sentences, `## Sources`) and `full_answer.md`, following
    `meta/asset_types/answer/specification.md` v2 exactly (read it; run its verificator). The full
    answer has one subsection per Key Question 1-5 with numbers from `data/` and an explicit
    evidence list, and states limitations: soma-only space clamp; by-eye targets; single-cell model
    has no presynaptic network so the bias is a surrogate; no rd1/rd10 Na/K remodelling data in the
    corpus except rd10 alpha RGCs where the spike generator is largely preserved; exploratory n = 8.
    No answer-specific verificator exists in `arf/scripts/verificators/`; check the folder against
    the specification by hand and run `verify_task_folder` (Verification Criteria). Satisfies
    REQ-17.

## Remote Machines

None required. All simulations run locally on the 8-core Windows workstation with NEURON 8.2.7; the
heaviest job (DSI main run, about 768 trials of about 9 s) takes about 16 minutes on 7 workers. No
GPU is used. No Vast.ai machine is provisioned, so no setup or teardown stage is needed.

## Assets Needed

* Library `de_rosenroll_2026_dsgc_ais_dendritic_spike` (task t0080): `apply_parameter_vector`,
  `ParameterVector`, `ParamIndex`, `setup_synapses_parametric`, `SynapseBundle`; import via
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.<module>`.
* Library `procedural_dsgc_morphology_generator` (t0090): `MorphologyParams`, `MorphologyResult`.
* Library `procedural_dsgc_morphology_generator_fix` (t0092): `generate_fixed_morphology`,
  `insert_baseline_channels`.
* Library `de_rosenroll_2026_dsgc` (t0024): vendored `nrnmech.dll` (`HHst`, `cad`, `Exp2NMDA`) and
  `ar2_noise` for the AR(2) synaptic noise.
* t0121 parquet (675 LEGIT cells) and the four source dumps from t0106, t0112, t0114, t0115 (68-d
  vectors); read in place.
* t0129 `evaluator.py`, `generator_wrapper.py`, constants (copied into this task) and, as a sanity
  reference only, `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/cell_params.jsonl`.
* t0063 `run_step.py` (SEClamp) and t0064 `run_step.py` (IClamp) as copy-the-pattern templates.
* The tracked DLL `tasks/t0107_t0106_polar_8dir_recheck/code/mods/nrnmech.dll`.
* Paper summaries (read for the answer, no downloads needed): Werginz2024, Goethals2020,
  Dhingra2004, Oesch2005, Schachter2010, MargolisDetwiler2007, FohlmeisterMiller1997,
  Fohlmeister2010. The aggregators `aggregate_papers`, `aggregate_answers` and `aggregate_libraries`
  do not exist in this repo, so these assets were located from tracked asset folders directly.
* `tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/research/inputs/SomeResults.pdf` for calibration
  targets.

## Expected Assets

One asset of type `answer` (matches `expected_assets` `{"answer": 1}` in `task.json`): an answer
asset in `assets/answer/<answer_id>/` that answers Key Questions 1-5 (current-ratio reproduction on
all cells, out-of-sample collapse at +60 pA, tonic-bias spontaneous firing, DSI direction with and
without bias, panel D saturation and temporal smearing) with `details.json`, `short_answer.md` and
`full_answer.md`. Non-asset outputs: `data/*.csv|json|jsonl`, `results/metrics.json`, charts under
`results/images/`, and task-local tests in `code/test_*.py`.

## Time Estimation

* Research: already done (about 1 hour before this step).
* Implementation, code writing and unit tests (Steps 1-6): about 2.5-3.5 hours.
* Clamp baseline and grid including timing gate (Steps 7-8): coding 1 hour; compute about 10-25
  minutes wall-clock (about 300 runs at 3-10 s on 7 workers).
* Current clamp and spontaneous/bias tuning (Steps 9-10): coding 1 hour; compute about 10-20
  minutes.
* DSI main run and heatmap (Step 11): coding 1 hour; compute about 35-45 minutes (two batches of
  about 16 minutes each; add 50% margin, so allow 1 hour).
* Arm decision (Step 12): 15 minutes if not triggered; about 2 hours if the dendritic arm is
  triggered (clamp grid, current clamp, spontaneous, 5-cell DSI).
* Panel D toy and NEURON (Steps 13-14): coding 1.5 hours; compute about 15 minutes.
* Metrics, charts, answer asset (Steps 15-16): about 1.5 hours.
* Total: about 10-12 hours of agent time with about 2-2.5 hours of compute (about 4.5 hours if the
  dendritic arm is needed). Compute estimates assume 9 s per 1400 ms DSI trial measured in research;
  underestimating NEURON runtime by up to 10x is the usual failure mode in this project, so run the
  Step 7 and Step 11 timing gates before launching batches, and subsample further if a gate predicts
  more than 4 hours for any one batch.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Soma+AIS scaling cannot reach sustained ratio 1.7 or transient ratio 0.25 (grid extremes) | Medium | Part 1 fails for some cells | Report failure honestly; trigger dendritic arm (Step 12); the sustained current is set by `kdr`, `kv3`, `kv4` on soma and dendrites, so the dendritic K scale is the natural fallback; record maximum achievable ratio |
| Space clamp: SEClamp controls the soma only, AIS/dendritic Na escapes, so the transient is mostly AIS | High | Transient fit is not a clean gNa measure | Document; log soma and AIS currents separately; fit only ratios; same limit exists in the researcher's whole-cell data |
| "+100 mV step" is a delta from holding vs absolute potential | Medium | Different driving force and activation | Use hold -65 to +35 mV; sensitivity check to +40 mV absolute on 2 cells; state in results; no escalation needed (not a critical blocker) |
| Transient-ratio target 0.25 and sustained 1.7x are by-eye values | High | Fitted scalings shift | Report sensitivity band (transient 0.15-0.35) and the resulting scaling ranges; replace targets if the researcher provides data |
| Evoked firing in WT-like model does not look like panel B (about 4 spikes, adapting) because the model has no calibration to a real WT cell | Medium | Collapse test uninformative | Collapse criterion defined up front with an "uninformative" outcome; amplitude sweep up to 800 pA; report f-I regardless |
| rd1-like cells are silent at rest even with bias, or bias also drives WT-like cells | Medium | Key Question 3 negative | Tuning rule and honest reporting of a negative result; alternatives (OU noise, per-cell bias) tried only after the common-bias rule fails; trigger (c) of Step 12 |
| NEURON runtime much longer than 9 s per trial (more recorders, scaled channels, bias noise) | Medium | Wall-clock blowup | Timing gates in Steps 7, 11 and 14; subsample heatmap to 3 cells or 1 seed; 7 workers; never rent compute |
| MOD DLL missing or fails to load (gitignored build, t0129 failed to recompile) | Low | Blocks everything | Load tracked t0107 DLL copy with rc assertion; if load fails, create an intervention file in `intervention/` rather than recompiling or substituting a different model; do not edit other task folders |
| Evaluator patch needs MOD recompilation (for example to expose a new mechanism parameter) | Low | Blocks Step 4-5 | Not needed: scaling only multiplies existing `gbar_*t80` and `HHst` parameters; if a parameter turns out to be unavailable, scale through existing parameters only and document |
| Reference cells are near-duplicates (one basin), giving false unanimity | Medium | Overstated generality | Seed-stratified draw (3/2/2/1); report spread and per-stratum medians |
| rd1-like cells collapse: DSI undefined | High | Misreading sentinel -1 as reversed preference | `None` DSI with spike counts and `low_count`; undefined pairs dropped and counted; metric variant value `null` if undefined for all |
| Panel D toy model cannot match all anchors (no equations given) | Medium | Reproduction partial | Record failed anchors and missing information; verdict "partly reproduced" or "not reproducible from description" is acceptable (REQ-14) |
| Tonic bias is a network surrogate and not an intrinsic mechanism | High | Interpretation limit | State in answer; report DSI with and without bias; do not claim intrinsic pacemaking |

## Verification Criteria

* Plan and structure checks:
  `uv run python -u -m arf.scripts.verificators.verify_plan t0131_rd1_na_k_remodelling_dsgc_dsi`
  reports 0 errors (this plan); at the end of implementation
  `uv run python -u -m arf.scripts.verificators.verify_task_file t0131_rd1_na_k_remodelling_dsgc_dsi`
  and `verify_task_results` report 0 errors.
* Unit tests: `uv run pytest tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/code -v` shows 0 failures
  (scaling identity at (1, 1), scaling at (0.5, 2.0), current sign, DSI-rule `None` and `low_count`,
  calibration module independence from firing code, toy-model anchor checks).
* Reference cells:
  `uv run python -X utf8 -c "import json;r=[json.loads(l) for l in open('tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/data/reference_cells.jsonl')];print(len(r), [x['cell_id'] for x in r])"`
  prints 8 and the 8 cell IDs, and the Step 2 assertion confirmed 675 rebuilt IDs equal the t0121
  parquet IDs (REQ-1).
* Calibration coverage: `data/clamp_grid.csv` has at least 8 x 36 = 288 rows;
  `data/fitted_scalings.json` has 8 per-cell entries each with `s_na_fit`, `s_k_fit`, achieved
  sustained and transient ratios; command
  `uv run python -X utf8 -c "import pandas as pd;d=pd.read_csv('tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/data/clamp_grid.csv');print(len(d), d.cell_id.nunique())"`
  prints `288 8` or more (REQ-4 to REQ-7).
* DSI outputs: `data/dsi_results.csv` has 8 cells x 4 conditions = 32 rows with columns
  `pd_rate_hz`, `nd_rate_hz`, `dsi_signed`, and no `dsi_signed` equal to -1.0:
  `uv run python -X utf8 -c "import pandas as pd;d=pd.read_csv('tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/data/dsi_results.csv');print(len(d), (d.dsi_signed==-1.0).sum())"`
  prints `32 0` (REQ-12); `data/dsi_heatmap.csv` covers 36 grid points (REQ-13).
* Metrics and charts: `results/metrics.json` parses with an explicit `variants` array containing at
  least the four variants and only the key `direction_selectivity_index`:
  `uv run python -u -m arf.scripts.verificators.verify_task_metrics t0131_rd1_na_k_remodelling_dsgc_dsi`
  reports 0 errors; `ls tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/results/images` lists at least
  `panel_c_clamp_traces.png`, `calibration_grid.png`, `current_clamp_traces.png`, `fi_curves.png`,
  `spontaneous_traces.png`, `dsi_by_condition.png`, `dsi_heatmap.png`, `panel_d_toy_model.png`,
  `panel_d_neuron_sweep.png`, `panel_d_neuron_pulses.png` (REQ-19).
* Panel D verdicts: `data/panel_d_verdicts.json` contains four predictions each with a verdict in
  {reproduced, partly reproduced, disproved} (REQ-16).
* Answer asset: `ls tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/assets/answer/*/` lists
  `details.json`, `short_answer.md`, `full_answer.md`; `verify_task_folder` reports 0 errors; and
  `full_answer.md` has headed subsections for each of Key Questions 1-5 (REQ-17).
* Requirement coverage: every `REQ-1` ... `REQ-20` appears in the implementation completion notes
  and in `results/results_detailed.md`; confirm with `grep -c "REQ-" results/results_detailed.md` at
  least 20 matches; `git status` shows no files changed outside
  `tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/` and
  `uv run python -u -m arf.scripts.verificators.verify_task_folder t0131_rd1_na_k_remodelling_dsgc_dsi`
  reports 0 errors (REQ-20, rule 3).
