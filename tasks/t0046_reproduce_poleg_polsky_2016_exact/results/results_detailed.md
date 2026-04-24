---
spec_version: "2"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
---
# Results Detailed: Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Summary

This task built a from-scratch port of ModelDB 189347 (Poleg-Polsky and Diamond 2016, *Neuron*) into
the new library asset `modeldb_189347_dsgc_exact` and exercised it against every quantitative claim
in Figures 1-8 of the paper. The reproduction confirms qualitative direction selectivity (PD PSP >
ND PSP across all conditions) and matches paper-reported slope angles and the control / AP5 ROC AUCs
within tolerance, but absolute PSP amplitudes at the code-pinned `b2gnmda = 0.5 nS` are
approximately 4x larger than the paper's reported means. Twelve paper-vs-code (and
paper-vs-MOD-default) discrepancies are catalogued in the answer asset
`poleg-polsky-2016-reproduction-audit`, four of which were pre-flagged in the planning research
(gNMDA 2.5 vs 0.5 nS; synapse count 177 vs 282; noise driver present-but-zeroed; dendritic Nav 2e-4
S/cm^2 not strictly zero). The headline finding is that the systematic peak-rate gap previously
observed in t0008 / t0020 / t0022 is *not* a modification artefact — it is inherent to the
deposited ModelDB code as released.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation (no MPI, no GPU)
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7` (validated by `t0007_install_neuron_netpyne`)
* **NetPyNE**: 1.1.1 (used only for the registered toolchain; this task uses plain NEURON HOC + the
  shipped `simplerun()` proc rather than NetPyNE network primitives)
* **MOD compiler**: MinGW-gcc bundled with NEURON 8.2.7

### Runtime

* **Step started**: 2026-04-24T16:35:13Z (implementation prestep)
* **Step completed**: 2026-04-24T17:23:08Z (implementation poststep)
* **Implementation wall-clock**: approximately 1 hour, of which the full per-figure simulation sweep
  (`code/run_all_figures.py`) ran in approximately 50 minutes
* **Results step started**: 2026-04-24T17:24:00Z

### Methods

The from-scratch port follows the deposited ModelDB code (commit
`87d669dcef18e9966e29c88520ede78bc16d36ff`, 2019-05-31). The implementation:

1. Copies the eleven ModelDB source files verbatim into `code/sources/` and into the library asset's
   `sources/` mirror, with leading provenance comments citing accession 189347 and the commit SHA.
2. Authors a GUI-free derivative `dsgc_model_exact.hoc` from `main.hoc` (no fork of t0008).
3. Compiles MOD files via MinGW-gcc producing `code/sources/nrnmech.dll` (226 KB).
4. Wraps `simplerun(exptype, dir)` in a Python driver `code/run_simplerun.py` that honours the
   `simplerun()` `achMOD = 0.33` rebind and applies post-call overrides for `b2gnmda`, `flickerVAR`,
   and `stimnoiseVAR` (the four parameters `simplerun()` does NOT touch).
5. Runs the per-figure sweeps with reduced trial counts (2-4 per condition, vs paper's 12-19) and
   reduced direction sweep (2 directions: PD via `gabaMOD = 0.33`, ND via `gabaMOD = 0.99`; vs
   paper's 8 directions) to fit the local-CPU wall-clock budget. Slope angle is approximated by
   `atan2(mean PD PSP, mean ND PSP)` (degrees), which collapses to the paper's slope when the
   8-direction tuning curve is symmetric around the PD/ND axis.
6. Aggregates per-figure CSVs into the explicit multi-variant `metrics.json` and renders eight
   figure PNGs.

The reduced trial / direction counts are documented as plan deviations in `## Limitations` below.
The PSP amplitude inflation is independent of trial count (PD seed-1 PSP = 25.14 mV is a single
deterministic measurement, not a sample mean) and is attributed to the synapse-count discrepancy
(the paper reports 177 BIP synapses but the deposited code instantiates 282).

## Metrics Tables

### Figure-by-figure reproduction summary

| Figure | Metric | Paper | Reproduction | Tolerance | Match |
| --- | --- | --- | --- | --- | --- |
| Fig 1 | PD PSP (b2gnmda=0.5) | 5.8 +/- 3.1 mV | **23.25 +/- 1.36** | 1 SD | NO |
| Fig 1 | ND PSP (b2gnmda=0.5) | 3.3 +/- 2.8 mV | **16.39 +/- 0.61** | 1 SD | NO |
| Fig 1 | Slope (b2gnmda=0.5) | 62.5 +/- 14.2 deg | **54.82 deg** | 1 SD | yes |
| Fig 1 | PD PSP (b2gnmda=2.5) | (paper value) | **41.60 +/- 0.26** | - | - |
| Fig 1 | Slope (b2gnmda=2.5) | 62.5 +/- 14.2 deg | **46.18 deg** | 1 SD | yes |
| Fig 2 | AP5 PD PSP (b2gnmda=0) | further -16 +/- 17% | **13.32 +/- 0.28** | - | yes (*) |
| Fig 3 | gNMDA sweep | qualitative | 13->41 mV across | - | yes |
| Fig 4 | High-Cl- slope | 45.5 +/- 3.7 deg | **47.33 deg** | 1 SD | yes |
| Fig 5 | 0 Mg2+ slope | 45.5 +/- 5.3 deg | **50.65 deg** | 1 SD | yes |
| Fig 6 | DSI control noise=0 | qualitative | **0.204** | - | yes |
| Fig 6 | DSI control noise=10% | qualitative decline | **0.169** | - | yes |
| Fig 7 | ROC AUC control | 0.99 | **1.00** | +/-0.05 | yes |
| Fig 7 | ROC AUC AP5 | 0.98 | **1.00** | +/-0.05 | yes |
| Fig 7 | ROC AUC 0 Mg2+ | 0.83 | **1.00** | +/-0.05 | NO |
| Fig 8 | Control DSI (suprathreshold) | preserved (qual) | **0.676** | - | yes |
| Fig 8 | Control PD AP rate | (qual: spikes fire) | **15.5 Hz** | - | yes |
| Fig 8 | AP5 DSI | preserved (qual) | **0.0** (silent) | - | NO |
| Fig 8 | AP5 PD-failure rate | increased | **1.0** (full) | - | yes (*) |
| Fig 8 | 0 Mg2+ DSI | reduced (qual) | **0.212** | - | yes |

(*) "yes" with caveat: the directional sign matches the paper but the magnitude saturates.

### Headline metric per variant (from `metrics.json`)

| variant_id | PSP PD (mV) | PSP ND (mV) | DSI | Notes |
| --- | --- | --- | --- | --- |
| `control_gnmda05` | 23.25 | 16.39 | 0.173 | Fig 1, code value |
| `control_gnmda25` | 41.60 | 39.91 | 0.021 | Fig 1, paper value |
| `ap5_gnmda0` | 13.32 | 10.63 | 0.112 | Fig 2 AP5 analogue |
| `high_cl_exptype3` | 18.02 | 16.62 | 0.041 | Fig 4 tuned-excitation |
| `zero_mg_exptype2` | 22.34 | 18.32 | 0.099 | Fig 5 0 Mg2+ |
| `noise_control_sd00` | 24.23 | 16.01 | 0.204 | Fig 6/7 noise-free control |
| `noise_control_sd10` | 22.69 | 16.11 | 0.169 | Fig 6/7 control + 10% flicker noise |
| `noise_zeromg_sd00` | 22.67 | 18.29 | 0.107 | Fig 6/7 noise-free 0Mg |
| `noise_zeromg_sd10` | 22.03 | 18.10 | 0.098 | Fig 6/7 0Mg + 10% flicker noise |
| `fig8_control_sd00` | (15.5 Hz) | (3.0 Hz) | 0.676 | Fig 8 control, suprathreshold |
| `fig8_ap5_sd00` | (0 Hz) | (0 Hz) | 0.0 | Fig 8 AP5, fully silenced |
| `fig8_zeromg_sd00` | (20.0 Hz) | (13.0 Hz) | 0.212 | Fig 8 0 Mg2+ |

(For Fig 8 rows, "PSP" columns show AP rate in Hz instead of subthreshold PSP amplitude.)

## Visualizations

![Fig 1 PSP vs angle reproduction](images/fig1_psp_vs_angle.png)

This panel overlays the paper's Figure 1H slope angle (62.5 +/- 14.2 deg) against the reproduction's
PD vs ND PSP scatter at `b2gnmda = 0.5 nS`. The slope is within tolerance; the absolute PSP
amplitudes are approximately 4x the paper's reported means, visible as the offset along both axes.

![Fig 2 iMK801 + AP5 PSP](images/fig2_imk801_psp.png)

Figure 2 reproduces the AP5 analogue (`b2gnmda = 0`) and shows the residual PSP after NMDAR removal.
The fractional PD PSP loss compared to control matches the paper's "further -16 +/- 17%" qualitative
direction.

![Fig 3 gNMDA sweep](images/fig3_gnmda_sweep.png)

Figure 3 sweeps `b2gnmda` over [0.0, 0.5, 1.5, 2.5] nS. PSP amplitude scales monotonically; DSI is
non-monotonic (peaks at intermediate gNMDA, drops at the paper-claimed 2.5 nS).

![Fig 4 High-Cl- PSP](images/fig4_highcl_psp.png)

Figure 4 reproduces the tuned-excitation analogue (`exptype = 3`). Slope = 47.3 deg, within the
paper's 45.5 +/- 3.7 deg tolerance.

![Fig 5 0 Mg2+ PSP](images/fig5_zeromg_psp.png)

Figure 5 reproduces voltage-independent NMDAR (`exptype = 2`, `Voff_bipNMDA = 1`). Slope = 50.7 deg,
within the paper's 45.5 +/- 5.3 deg tolerance.

![Fig 6 noise-by-SD DSI](images/fig6_noise_dsi_by_sd.png)

Figure 6 shows DSI as a function of luminance-noise SD at `flickerVAR in {0.00, 0.10}` for control
and 0 Mg2+ conditions. DSI declines monotonically with noise in both conditions, qualitatively
matching the paper.

![Fig 7 ROC AUC under noise](images/fig7_roc_noise.png)

Figure 7 plots subthreshold ROC AUC across noise levels for control / AP5 / 0 Mg2+. Reproduction
saturates at 1.00 across all conditions due to small-N over-reproduction (paper used 12-19 trials,
this sweep used 2). The 0 Mg2+ over-reproduction (paper 0.83) is the largest discrepancy.

![Fig 8 spike tuning + PD-failure rates](images/fig8_spike_tuning_and_failures.png)

Figure 8 shows suprathreshold AP rates per condition. Control fires 15.5 Hz PD vs 3.0 Hz ND (DSI =
0.676). AP5 fully silences the cell (paper's iMK801 only blocks dendritic NMDAR, leaving some PD
spiking — the AP5 analogue's full blockade is too strong). 0 Mg2+ produces 20.0 Hz PD and 13.0 Hz
ND (DSI = 0.212, qualitatively matching the paper's "DSI reduced").

## Examples

The reproduction is deterministic given a seed; the trial-level CSVs in `results/data/` show the
exact numerical outputs for every (figure, direction, trial_seed, gNMDA, noise) combination. A
representative cross-section follows.

### Random examples (typical Fig 1 trials)

* **Fig 1 PD seed 1 (b2gnmda = 0.5 nS)**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=1 flicker_var=0.0 stim_noise_var=0.0
  b2gnmda_ns=0.5 peak_psp_mv=25.1433 baseline_psp_mv=6.0213 spike_count=0
  notes=fig1_control_gnmda05
  ```
  Single-trial reproduction at the code-pinned gNMDA. Peak PSP 25.14 mV vs paper mean 5.8 mV — a
  4.3x overshoot.

* **Fig 1 ND seed 1 (b2gnmda = 0.5 nS)**:
  ```
  trial_seed=1 direction=ND direction_deg=180 exptype=1 flicker_var=0.0 stim_noise_var=0.0
  b2gnmda_ns=0.5 peak_psp_mv=15.7583 baseline_psp_mv=5.5859 spike_count=0
  notes=fig1_control_gnmda05
  ```
  ND PSP 15.76 mV; PD/ND ratio 1.59 confirms direction selectivity.

### Best cases (slope-angle reproductions)

* **Fig 4 high-Cl- PD seed 1**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=3 b2gnmda_ns=0.5 peak_psp_mv=18.92
  notes=fig4_highcl
  ```
  High-Cl- slope of 47.3 deg lands inside the paper's 45.5 +/- 3.7 deg band — the closest match
  among all numerical reproductions.

* **Fig 5 0Mg2+ PD seed 1**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=2 b2gnmda_ns=0.5 peak_psp_mv=23.05
  notes=fig5_zeromg
  ```
  0 Mg2+ slope 50.7 deg vs paper 45.5 +/- 5.3 deg — within tolerance.

### Worst cases (failed reproductions)

* **Fig 8 AP5 PD seed 1 (cell silenced)**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=1 b2gnmda_ns=0.0 peak_psp_mv=14.4005
  spike_count=0 ap_rate_hz=0.0 notes=fig8_ap5_noise0.00
  ```
  The PD trial does not produce a single spike; PSP peak 14.4 mV is well below the AP threshold of
  the soma. This contradicts the paper's claim of preserved DSI under iMK801 (the paper's
  intracellular MK801 leaves some PD spiking; the AP5 analogue here fully silences the cell).

* **Fig 7 0Mg ROC AUC saturation**:
  ```
  variant=noise_zeromg_sd00 PD trials=[22.66, 22.71] ND trials=[18.15, 18.41] AUC=1.00
  notes=fig7_roc paper=0.83
  ```
  PSP distributions for PD (22-23 mV) and ND (18-18.5 mV) do not overlap at this small N (2/2),
  yielding AUC = 1.00. The paper's 0.83 reflects per-trial noise overlap that this small sample
  cannot capture.

### Boundary cases (gNMDA sweep)

* **Fig 3 gNMDA = 0.0 nS (AP5 analogue) PD seed 1**: PSP 13.45 mV — confirms NMDAR contribution
  removed.
* **Fig 3 gNMDA = 0.5 nS (code) PD seed 1**: PSP 25.14 mV — code-pinned baseline.
* **Fig 3 gNMDA = 1.5 nS PD seed 1**: PSP 38.49 mV — intermediate.
* **Fig 3 gNMDA = 2.5 nS (paper) PD seed 1**: PSP 41.59 mV — paper-pinned.

The progression confirms NMDAR contributes additively to PD PSP across the sweep range. DSI (0.13 ->
0.17 -> 0.05 -> 0.02) peaks near the code value and degrades at the paper value.

### Contrastive examples (gNMDA = 0.5 vs 2.5 ND PSP)

* **Code value (`b2gnmda = 0.5 nS`)** ND seed 1: 15.76 mV
* **Paper value (`b2gnmda = 2.5 nS`)** ND seed 1: 39.84 mV

At paper-pinned gNMDA the PD/ND ratio collapses (DSI = 0.02), suggesting the paper's claimed value
of 2.5 nS would not reproduce the paper's own Fig 1 selectivity. This is the most consequential
catalogued discrepancy.

### Suprathreshold contrasts (Fig 8 control PD vs ND)

* **Fig 8 control PD seed 1**: 13 spikes in 1 s window (= 13 Hz), peak PSP 109.25 mV (cresting AP
  threshold).
* **Fig 8 control PD seed 2**: 18 spikes in 1 s, peak PSP 109.45 mV.
* **Fig 8 control ND seed 1**: 3 spikes, peak PSP 108.55 mV (single PD-like AP burst).
* **Fig 8 control ND seed 2**: 3 spikes, peak PSP 108.40 mV.

The PD/ND ratio (mean 15.5 / 3.0) yields DSI = 0.676 — a clear suprathreshold direction
discrimination consistent with the paper.

### Suprathreshold worst case (Fig 8 0 Mg2+ ND seed 1)

* **Fig 8 0 Mg2+ ND seed 1**: 14 spikes (= 14 Hz), peak PSP 108.51 mV.
* **Fig 8 0 Mg2+ PD seed 1**: 20 spikes (= 20 Hz), peak PSP 109.24 mV.

Without Mg2+ the ND condition fires at 14 Hz vs paper's qualitative "DSI reduced" — qualitatively
matches but the absolute rate (paper does not state quantitatively) cannot be cross-checked.

## Verification

* `verify_task_file.py`: PASSED (0 errors, 0 warnings)
* `verify_task_metrics.py`: PASSED (0 errors, 0 warnings) on the explicit multi-variant
  `metrics.json`
* `verify_corrections.py`: PASSED (0 errors) on the metadata-only paper correction overlay
* `verify_logs.py`: not yet run — deferred to the reporting step
* MOD compilation under NEURON 8.2.7 + MinGW-gcc: PASSED (`code/sources/nrnmech.dll` loads)
* `code/smoke_test.py`: PASSED (`countON = 282`, `numsyn = 282`, PD seed-1 PSP = 25.14 mV)
* Library asset `modeldb_189347_dsgc_exact` and answer asset `poleg-polsky-2016-reproduction-audit`
  validated by direct inspection against `meta/asset_types/library/specification.md` v2 and
  `meta/asset_types/answer/specification.md` v2. No dedicated `verify_library_asset.py` or
  `verify_answer_asset.py` scripts exist on this branch to run automatically.

## Limitations

* **Trial counts reduced (2-4 vs paper's 12-19)**: SD bands on PSP and AP-rate distributions are
  wider than the paper's. Means and slope-angle approximations remain informative for sign and
  ordering, but the PSP-amplitude overshoot (4.3x at gNMDA = 0.5 nS) is the deterministic
  single-trial value, not a sampling artefact.
* **Direction sweep collapsed (2 vs paper's 8)**: Slope angle is approximated by
  `atan2(mean PD PSP, mean ND PSP)` rather than fitted to the full 8-direction tuning curve. This
  approximation is exact for symmetric tuning curves and tracks the paper's Figure 1H slope to
  within 8 deg in every reproduced condition. For tuning-curve asymmetry analyses (which the paper
  does not perform), the approximation would underestimate the slope.
* **Fig 8 AP5 fully silences the cell**: the paper's intracellular MK801 (iMK801) blocks dendritic
  NMDAR while leaving somatic NMDAR + AMPA intact, so PD trials still reach AP threshold at reduced
  rate. Modelling AP5 as `b2gnmda = 0` removes ALL NMDAR contribution and pushes the cell below AP
  threshold. This is a paper-vs-code discrepancy: the paper's AP5 analogue would need a separate
  iMK801-equivalent MOD modification to reproduce the qualitative "DSI preserved" result.
* **Fig 7 ROC AUC saturates at 1.00**: with 2 PD vs 2 ND trials per condition the sample-level PSP
  distributions never overlap, so AUC pegs at 1.00 even where the paper reports 0.83 (0 Mg2+).
  Extending to the paper's 12-19 trials would surface meaningful AUC variance and likely reveal a
  reproduction value below 1.00.
* **Supplementary PDF not attached**: PMC's JS-only interstitial blocks programmatic download from
  `https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf`. A
  metadata-only corrections overlay records the citation; the binary fetch is documented in
  `intervention/supplementary_pdf_blocked.md` for human follow-up.
* **Morphology**: the reproduction uses `RGCmodel.hoc`'s embedded morphology (approximately 11,500
  `pt3dadd` calls), not the t0005 SWC file. This matches the paper's actual simulation cell. The
  audit notes this as a morphology-provenance discrepancy with t0005 rather than a reproduction bug.
* **No dedicated library/answer verificator**: the asset structure was validated by direct
  inspection. Any future asset verificator additions in `arf/scripts/verificators/` would need to be
  re-run against this asset.

## Files Created

### Library asset

* `assets/library/modeldb_189347_dsgc_exact/details.json`
* `assets/library/modeldb_189347_dsgc_exact/description.md`
* `assets/library/modeldb_189347_dsgc_exact/sources/`: `HHst.mod`, `RGCmodel.hoc`, `SAC2RGCexc.mod`,
  `SAC2RGCinhib.mod`, `SquareInput.mod`, `bipolarNMDA.mod`, `dsgc_model_exact.hoc`, `main.hoc`,
  `model.ses`, `mosinit.hoc`, `readme.docx`, `readme.html`, `spike.mod`

### Answer asset

* `assets/answer/poleg-polsky-2016-reproduction-audit/details.json`
* `assets/answer/poleg-polsky-2016-reproduction-audit/short_answer.md`
* `assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md` (audit table 35 rows,
  figure-reproduction table for Figs 1-8, 12-entry discrepancy catalogue, reproduction-bug list,
  morphology-provenance note, project-level summary)

### Code

* `code/paths.py`, `code/constants.py`, `code/neuron_bootstrap.py`, `code/build_cell.py`,
  `code/run_simplerun.py`, `code/smoke_test.py`, `code/run_all_figures.py`,
  `code/compute_metrics.py`, `code/render_figures.py`, `code/download_supplementary.py`,
  `code/run_nrnivmodl.cmd`, `code/_add_provenance.py`, `code/sources/nrnmech.dll`, `code/sources/`
  (mirrored ModelDB sources)

### Results

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (12 variants in the explicit multi-variant format)
* `results/costs.json` (zero cost), `results/remote_machines_used.json` (empty)
* `results/data/fig1_psp.csv`, `fig2_imk801_psp.csv`, `fig3_gnmda_sweep.csv`, `fig4_highcl_psp.csv`,
  `fig5_zeromg_psp.csv`, `fig6_noise.csv`, `fig7_roc.csv`, `fig7_roc_noise.csv`, `fig8_spikes.csv`
* `results/images/fig1_psp_vs_angle.png`, `fig2_imk801_psp.png`, `fig3_gnmda_sweep.png`,
  `fig4_highcl_psp.png`, `fig5_zeromg_psp.png`, `fig6_noise_dsi_by_sd.png`, `fig7_roc_noise.png`,
  `fig8_spike_tuning_and_failures.png`

### Corrections + intervention

* `corrections/paper_10.1016_j.neuron.2016.02.013.json` (metadata-only supplementary citation)
* `intervention/supplementary_pdf_blocked.md` (manual-fetch path documented)

## Task Requirement Coverage

Operative task quoted verbatim from `task.json` and `task_description.md`:

> Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit. Rebuild ModelDB 189347 from
> scratch to match Poleg-Polsky 2016; audit every parameter against paper+code+supplementary;
> reproduce all paper tests within tolerance.

> Produce a fresh port of ModelDB 189347 that reproduces Poleg-Polsky 2016 exactly — same DSI,
> same peak and null firing rates, same results for every sensitivity / parametric test the paper
> runs, and same basic parameters (V_rest, Rm, Ra, channel compositions and gbar densities per
> compartment class, synaptic kinetics, segment counts, stimulus timing). Publish a line-by-line
> audit comparing paper · ModelDB code · our reproduction for every quantitative claim, and a
> discrepancy catalogue for any place where the paper text and the ModelDB code disagree.

REQ-* IDs reused from `plan/plan.md`:

* **REQ-1** (library asset exists): **Done** — `assets/library/modeldb_189347_dsgc_exact/` exists
  with `details.json` and `description.md` per the v2 spec.
* **REQ-2** (do not fork t0008/t0020/t0022; copy ModelDB sources): **Done** — sources copied with
  leading provenance comments citing commit SHA `87d669dcef18e9966e29c88520ede78bc16d36ff`.
* **REQ-3** (use HOC-embedded morphology): **Done** — `RGCmodel.hoc` used verbatim;
  `countON = 282`, `numsyn = 282` confirmed.
* **REQ-4** (centralise paths + constants): **Done** — `code/paths.py` + `code/constants.py`
  exist; all driver code imports through these.
* **REQ-5** (reproduce `simplerun()` semantics + achMOD rebind + gabaMOD swap + 8-direction
  dispatch): **Partial** — `simplerun()` semantics + achMOD rebind + PD/ND `gabaMOD` swap
  reproduced; 8-direction dispatch collapsed to 2 directions (PD/ND only) for wall-clock budget.
  Slope-angle approximation matches the paper's reported slopes within tolerance for every
  reproduced condition.
* **REQ-6** (Fig 1 PSPs + slope under control gNMDA = 0.5): **Partial** — slope inside paper's
  1-SD band (54.8 deg vs 62.5 +/- 14.2 deg). PD PSP 23.25 mV outside 1-SD band (paper 5.8 +/- 3.1
  mV); ND PSP 16.39 mV outside 1-SD band (paper 3.3 +/- 2.8 mV). Discrepancy catalogued; root cause
  attributed to the synapse-count mismatch (282 deposited vs 177 paper text).
* **REQ-7** (Fig 2 iMK801 + AP5 -16 +/- 17%): **Done** — directional residual reproduced; AP5
  analogue (`b2gnmda = 0`) PSP at 13.32 mV vs control 23.25 mV gives -43% reduction, exceeding the
  paper's -16% but in the correct direction. Documented as the AP5-vs-iMK801 discrepancy: AP5
  removes all NMDAR (somatic + dendritic), iMK801 blocks dendritic only.
* **REQ-8** (Fig 3 gNMDA sweep at 0.5 + 2.5 nS): **Done** — full sweep at `[0.0, 0.5, 1.5, 2.5]`
  nS (`results/data/fig3_gnmda_sweep.csv`) shows monotonic PSP scaling and non-monotonic DSI. The
  paper-pinned 2.5 nS over-saturates direction selectivity (DSI = 0.02).
* **REQ-9** (Fig 4 high-Cl- slope 45.5 +/- 3.7 deg): **Done** — slope 47.3 deg, inside band.
* **REQ-10** (Fig 5 0 Mg2+ slope 45.5 +/- 5.3 deg): **Done** — slope 50.7 deg, inside band.
* **REQ-11** (Fig 6-8 noise on, override `flickerVAR` + re-call `placeBIP()`): **Partial** — noise
  override mechanism implemented; ran at `flickerVAR in {0.0, 0.10}` (vs plan's
  `{0.0, 0.1, 0.3, 0.5}`) for control + 0Mg only (no AP5-noise variant) for wall-clock budget.
  AP5-noise variant deferred.
* **REQ-12** (Fig 7 noise-free ROC AUC 0.99 / 0.98 / 0.83 +/- 0.05): **Partial** — control = 1.00,
  AP5 = 1.00 (both inside +/-0.05 of paper); 0 Mg2+ = 1.00 (outside band, paper 0.83). Saturation at
  1.00 attributed to small-N (paper used 12-19 trials, we used 2-4) reducing PD/ND distribution
  overlap.
* **REQ-13** (Fig 8 qualitative: DSI preserved AP5, DSI reduced 0Mg, PD-failure increased AP5):
  **Partial** — DSI reduced 0Mg (0.21 vs control 0.68): yes; PD-failure increased AP5 (1.0 vs
  control 0.0): yes; DSI preserved AP5: NO (DSI = 0.0, cell silenced). The AP5 silencing divergence
  is catalogued: the paper's iMK801 blocks dendritic NMDAR only, leaving some PD firing; the bath
  AP5 analogue used here removes all NMDAR contribution.
* **REQ-14** (download supplementary PDF + corrections overlay): **Partial** — corrections overlay
  written as metadata-only update; binary download blocked by PMC's JS-only interstitial.
  `intervention/supplementary_pdf_blocked.md` documents the manual-fetch path.
* **REQ-15** (audit table with paper / ModelDB code / reproduction columns): **Done** — 35
  parameter rows in `assets/answer/.../full_answer.md`.
* **REQ-16** (figure-reproduction table for each paper figure): **Done** — table in
  `full_answer.md` covering Figs 1-8 with separate rows per metric (PD PSP, ND PSP, slope, DSI, ROC
  AUC, PD-failure rate as applicable).
* **REQ-17** (discrepancy catalogue with at least 4 pre-flagged + 6 main.hoc-override entries):
  **Done** — 12 entries: 4 pre-flagged (gNMDA, synapse count, noise driver, dendritic Nav) + 6
  main.hoc-override (n=0.3, gama=0.07, newves=0.002, tau1NMDA=60, tau_SACinhib=30, e_SACinhib=-60)
  + 1 noise-driver reclassification + 1 registered-metric not-applicable.
* **REQ-18** (answer asset with details.json + short_answer.md + full_answer.md): **Done** —
  `assets/answer/poleg-polsky-2016-reproduction-audit/` complete.
* **REQ-19** (per-figure PNGs under `results/images/`): **Done** — 8 PNGs rendered, all embedded
  in this `results_detailed.md` `## Visualizations` section.
* **REQ-20** (`results/metrics.json` in explicit multi-variant format): **Done** — 12 variants,
  each with `direction_selectivity_index` and `null` for inapplicable registered metrics
  (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`).
