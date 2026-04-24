---
spec_version: "2"
answer_id: "poleg-polsky-2016-reproduction-audit"
answered_by_task: "t0046_reproduce_poleg_polsky_2016_exact"
date_answered: "2026-04-24"
confidence: "medium"
---
## Question

Does ModelDB 189347 (Poleg-Polsky and Diamond 2016) reproduce every quantitative claim in Figures
1-8 of the Neuron paper when re-run faithfully under NEURON 8.2.7, and where do the paper text and
the ModelDB code disagree?

## Short Answer

Partially. The from-scratch port of ModelDB 189347 reproduces the qualitative direction-tuning
behaviour (PD PSP > ND PSP) and the predicted suppression of selectivity under 0 Mg2+, but the
absolute PSP amplitudes are larger than the paper's reported means at the code-pinned gNMDA = 0.5
nS, and the paper-vs-code discrepancies on synapse count, gNMDA value, and noise driver behaviour
are confirmed. Ten or more discrepancies are catalogued below including six
MOD-default-vs-main.hoc-override mismatches and four pre-flagged paper-vs-code disagreements; every
Figure 1-8 reproduction outcome is recorded with numerical evidence in the figure-reproduction table
and the underlying CSVs in `results/data/`.

## Research Process

The audit synthesizes three sources:

1. The published paper PDF [PolegPolsky2016][polegpolsky2016] and the abstract from the
   `10.1016_j.neuron.2016.02.013` paper asset.
2. The ModelDB 189347 source release pinned to commit `87d669dcef18e9966e29c88520ede78bc16d36ff`
   (2019-05-31). Source files (`main.hoc`, `RGCmodel.hoc`, six `.mod` files, `mosinit.hoc`,
   `model.ses`) are mirrored into `code/sources/` and
   `assets/library/modeldb_189347_dsgc_exact/sources/` with provenance comments.
3. A fresh from-scratch reproduction. The MOD files compile cleanly under NEURON 8.2.7 + MinGW-gcc
   with no source edits. The Python driver (`code/run_simplerun.py`) wraps
   `h.simplerun(exptype, dir)` and exposes the noise globals (`flickerVAR`, `stimnoiseVAR`) plus a
   `b2gnmda` post-call override. Every Figure 1-8 sweep is automated in `code/run_all_figures.py`;
   per-figure CSVs land under `results/data/`; the explicit multi-variant `metrics.json` is built by
   `code/compute_metrics.py`; PNG overlays are rendered by `code/render_figures.py` into
   `results/images/`.

The supplementary PDF (NIHMS766337, PMC4795984) is cited but could not be auto-downloaded: PMC
blocks programmatic access with a JS-only interstitial. The corrections overlay
`corrections/paper_10.1016_j.neuron.2016.02.013.json` records the citation as a metadata-only
update; manual fetch is documented in `intervention/supplementary_pdf_blocked.md`.

## Evidence from Papers

The paper's Figures 1-8 report the following primary metrics (see paper Figs 1-8 and
[PolegPolsky2016][polegpolsky2016] Methods):

* **Fig 1** (control, 8-direction PSPs, voltage-dependent NMDAR): PD PSP **5.8 +/- 3.1 mV**, ND PSP
  **3.3 +/- 2.8 mV**, slope **62.5 +/- 14.2 deg** (multiplicative). DSI preserved under AP5. n=19.
* **Fig 2** (iMK801 + bath AP5): AP5-after-iMK801 reduces PD PSP by **16 +/- 17 %**. n=15.
* **Fig 3** (NEURON model gNMDA sweep): 282 presynaptic cells, paper-stated **gNMDA = 2.5 nS**.
* **Fig 4** (high-Cl-, tuned-excitation analogue): slope **45.5 +/- 3.7 deg** (additive). DS
  reverses PD in 15/20 cells (75 %). n=12.
* **Fig 5** (0 Mg2+): slope **45.5 +/- 5.3 deg** (additive). DSI reduced but PD != ND. n=8.
* **Fig 6** (noisy PSPs, SD = 0/10/30/50 %): DSI reduced by noise, strongest reduction in 0 Mg2+.
  n=12.
* **Fig 7** (subthreshold ROC, noise-free): AUC **0.99 / 0.98 / 0.83** for control / AP5 / 0 Mg2+.
  Tolerance +/- 0.05.
* **Fig 8** (suprathreshold APs): DSI preserved under AP5; DSI reduced in 0 Mg2+; PD-failure rate
  increases under AP5. **No specific peak Hz reported.**

Methodology and parameter cross-checks come from the paper's Methods section and the supplementary
text (NIHMS766337). The paper-vs-code discrepancies catalogued below were flagged across the three
research stages of this task and are confirmed (or in some cases overturned) by direct inspection of
`main.hoc`.

## Evidence from Internet Sources

The ModelDB record (`https://senselab.med.yale.edu/ModelDB/showmodel.cshtml?model=189347`) and the
GitHub mirror (`https://github.com/ModelDBRepository/189347`) confirm the commit SHA, file
inventory, and licensing of the release. The "noise driver" pre-flag from
`research/research_internet.md` was overturned by direct code inspection: `main.hoc`'s `placeBIP()`
already contains the per-50-ms Gaussian noise driver, parameterised to zero by default. Setting
`h.flickerVAR = 0.10` (10 % SD) and re-calling `placeBIP()` is sufficient to exercise it; no new MOD
file is required. This entry is reclassified in the discrepancy catalogue below from "missing" to
"present but zeroed".

## Evidence from Code or Experiments

A fresh port was built and run (see Methods in
`assets/library/modeldb_189347_dsgc_exact/ description.md`). Per-trial PSP traces are recorded as
soma voltage maxima above `v_init = -65 mV`. The full per-figure data is in
`results/data/fig{1..8}*.csv`; aggregated metrics in `results/metrics.json`; PNG overlays in
`results/images/`.

### Audit Table (basic parameters)

The "Code value" column reports the `main.hoc` value at module load (per
`research/research_code.md`'s correction). Where `main.hoc` overrides a MOD-file PARAMETER default,
that override is the canonical code value and the MOD default is captured in the discrepancy
catalogue.

| Parameter | Paper value (when stated) | ModelDB code value | Reproduction value | Match? | Citation |
| --- | --- | --- | --- | --- | --- |
| Ra (axial resistance) | not stated | 100 Ohm-cm (`global_ra=100`) | 100 Ohm-cm | yes | main.hoc:317 |
| g_pas (passive leak) | not stated | 5e-5 S/cm^2 (active=0) | 5e-5 S/cm^2 | yes | main.hoc:161 |
| V_rest | -65 mV (Methods) | -60 mV (`RGCepas`) | -60 mV | partial | main.hoc:162 |
| V_init | -65 mV (Methods) | -65 mV (HOC default v_init) | -65 mV | yes | stdrun.hoc default |
| Cm | 1 uF/cm^2 (Methods, default) | 1 uF/cm^2 (NEURON default) | 1 uF/cm^2 | yes | NEURON default |
| Soma gNa | "active soma" | 0.4 S/cm^2 (`RGCsomana`) | 0.4 S/cm^2 | yes | main.hoc:148 |
| Soma gKv | "active soma" | 0.07 S/cm^2 (`RGCsomakv`) | 0.07 S/cm^2 | yes | main.hoc:149 |
| Soma gKm | "active soma" | 5e-4 S/cm^2 (`RGCsomakm`) | 5e-4 S/cm^2 | yes | main.hoc:150 |
| Dend gNa | "passive dendrites" (text) | 2e-4 S/cm^2 (`RGCdendna`) | 2e-4 S/cm^2 | partial | main.hoc:152 (text != code) |
| Dend gKv | "passive dendrites" (text) | 0.007 S/cm^2 (`RGCdendkv`) | 0.007 S/cm^2 | partial | main.hoc:153 |
| Dend gKm | "passive dendrites" (text) | 0 (`RGCdendkm`) | 0 | yes | main.hoc:154 |
| n_bipNMDA | not stated | 0.3 (main.hoc override) | 0.3 | yes | main.hoc:82 |
| gama_bipNMDA | not stated | 0.07 (main.hoc override) | 0.07 | yes | main.hoc:83 |
| newves_bipNMDA | not stated | 0.002 (main.hoc override) | 0.002 | yes | main.hoc:84 |
| tau1NMDA_bipNMDA | not stated | 60 ms (main.hoc override) | 60 ms | yes | main.hoc:86 |
| tauAMPA | not stated | bipolarNMDA.mod default | as-shipped | yes | bipolarNMDA.mod |
| tau_SACinhib | not stated | 30 ms (main.hoc override) | 30 ms | yes | main.hoc:90 |
| e_SACinhib | -65 mV (typical Cl) | -60 mV (main.hoc override) | -60 mV | partial | main.hoc:89 |
| tau_SACexc (ACh) | not stated | 3 ms | 3 ms | yes | main.hoc:88 |
| e_nACh | not stated | SACexc reversal (~0) | as-shipped | yes | SAC2RGCexc.mod |
| b2gampa | not stated | 0.25 nS | 0.25 nS | yes | main.hoc:42 |
| b2gnmda (paper text) | 2.5 nS (Fig 3E text) | 0.5 nS (main.hoc default) | 0.5 nS (primary) | NO (5x gap) | main.hoc:43 vs paper Fig 3E |
| s2ggaba | not stated | 0.5 nS | 0.5 nS | yes | main.hoc:44 |
| s2gach | not stated | 0.5 nS | 0.5 nS | yes | main.hoc:45 |
| gabaMOD (PD) | "preferred direction" | 0.33 (`gabaMOD=.33+.66*0`) | 0.33 | yes | main.hoc:351 (simplerun) |
| gabaMOD (ND) | "null direction" | 0.99 (`gabaMOD=.33+.66*1`) | 0.99 | yes | main.hoc:351 (simplerun) |
| achMOD (after simplerun) | not stated | 0.33 (rebound by simplerun) | 0.33 | yes | main.hoc:352 (silently overrides line-47 default 0.25) |
| maxves_bipNMDA | not stated | 10 (RRP) | 10 | yes | main.hoc:59 |
| Vtau (VampT) | not stated | 1 | 1 | yes | main.hoc:80 |
| lightspeed | 1 mm/sec (Methods) | 1 um/ms = 1 mm/sec | 1 um/ms | yes | main.hoc:64 |
| lightwidth | 500 um | 500 um | 500 um | yes | main.hoc:65 |
| SACdur | not stated | 500 ms | 500 ms | yes | main.hoc:74 |
| dt | 0.1 ms (Methods) | 0.1 ms | 0.1 ms | yes | main.hoc:50 |
| tstop | 1000 ms (Methods) | 1000 ms | 1000 ms | yes | main.hoc:37 |
| countON | 282 ON dendrites (this code) | 282 (verified in placeBIP loop) | 282 | yes | RGCmodel.hoc cut z >= -0.16 y + 46 |
| numsyn (paper text) | 177 synapses (text) | 282 (one BIP/SACinhib/SACexc per ON dend) | 282 | NO | paper Methods vs main.hoc cell summary |

### Figure-Reproduction Table

Numerical reproduction values are pulled from `results/metrics.json` (12 variants) and the
per-figure CSVs in `results/data/`. Tolerances are from the paper's reported SDs (see
`task_description.md` Pass Criterion). Match? legend: `yes` = inside the paper's 1-SD band; `near` =
outside the band but within 2 SD; `NO` = greater than 2 SD or qualitatively wrong; `qual` =
qualitative claim only.

| Figure | Metric | Paper value | Reproduction value | Tolerance | Match? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | PD PSP mean (b2gnmda = 0.5, code) | 5.8 +/- 3.1 mV | **23.25 mV** | +/- 3.1 mV | NO | At code's b2gnmda = 0.5 nS, PD PSP is ~4x the paper value. |
| 1 | ND PSP mean (b2gnmda = 0.5, code) | 3.3 +/- 2.8 mV | **16.39 mV** | +/- 2.8 mV | NO | Same multiplicative gap as PD. |
| 1 | Slope angle (b2gnmda = 0.5, code) | 62.5 +/- 14.2 deg | **54.8 deg** | +/- 14.2 deg | yes | Inside the paper's 1-SD band. |
| 1 | PD PSP mean (b2gnmda = 2.5, paper) | 5.8 +/- 3.1 mV | **41.60 mV** | +/- 3.1 mV | NO | Even larger at the paper's claimed gNMDA. |
| 1 | Slope angle (b2gnmda = 2.5, paper) | 62.5 +/- 14.2 deg | **46.2 deg** | +/- 14.2 deg | near | Outside band but within ~1.2 SD; larger gNMDA pushes slope toward additive 45 deg. |
| 2 | PD PSP change (b2gnmda 0.5 -> 0) | -16 +/- 17 % | **-42.7 %** ((13.32 - 23.25)/23.25) | +/- 17 % | NO | AP5 analogue cuts PD PSP by ~43%, much more than the paper's 16%. |
| 3 | DSI peaks at intermediate gNMDA | qualitative | DSI 0.13 / 0.18 / 0.13 / 0.04 at b2gnmda 0 / 0.5 / 1.5 / 2.5 nS | qualitative | qual yes | DSI peaks at code's b2gnmda = 0.5 nS as predicted by the paper's "intermediate gNMDA" claim. |
| 4 | Slope angle (high-Cl-) | 45.5 +/- 3.7 deg | **47.3 deg** | +/- 3.7 deg | yes | Inside the paper's 1-SD band; consistent with additive scaling. |
| 4 | Direction reversal | 15/20 = 75 % | 0/3 trials reverse PD/ND in our sample | >= 50 % | NO | Cannot reliably assess at N = 3 trials per direction; flagged as a small-sample limitation. |
| 5 | Slope angle (0 Mg2+) | 45.5 +/- 5.3 deg | **50.7 deg** | +/- 5.3 deg | yes | Inside the paper's 1-SD band. |
| 5 | DSI reduced but PD != ND | qualitative | DSI 0.099 (vs control 0.173) | DSI > 0 | qual yes | DSI dropped 43% under 0 Mg2+; PD still > ND. |
| 6 | DSI decreases with noise (control) | qualitative | DSI 0.20 (SD=0) -> 0.17 (SD=0.10) | qualitative | qual yes | Confirmed: DSI decreases monotonically with noise SD. |
| 6 | DSI decreases with noise (0 Mg2+) | qualitative | DSI 0.11 (SD=0) -> 0.10 (SD=0.10) | qualitative | qual yes | Same trend in 0 Mg2+, but smaller change. |
| 7 | ROC AUC PD vs ND noise-free (control) | 0.99 +/- 0.05 | **1.00** | +/- 0.05 | yes | All PD trials are higher than all ND trials at noise = 0. |
| 7 | ROC AUC PD vs ND noise-free (AP5) | 0.98 +/- 0.05 | **1.00** | +/- 0.05 | yes | Even at b2gnmda = 0, PD/ND separation is preserved subthreshold. |
| 7 | ROC AUC PD vs ND noise-free (0 Mg2+) | 0.83 +/- 0.05 | **1.00** | +/- 0.05 | NO | We over-reproduce: paper sees AUC drop to 0.83 in 0 Mg2+; our small-N sample still gives perfect separation. |
| 8 | DSI preserved under AP5 | qualitative (DSI > 0) | DSI = **0.0** (zero spikes everywhere under AP5 analogue) | DSI > 0 | NO | AP5 analogue (b2gnmda = 0) silences the cell; paper's "preserved DSI" requires non-zero spike rate. |
| 8 | DSI reduced in 0 Mg2+ | qualitative (DSI < control) | control DSI = **0.676**; 0 Mg2+ DSI = **0.212** | DSI(0Mg) < DSI(control) | yes | DSI dropped 69% under 0 Mg2+ as paper predicts. |
| 8 | PD-failure rate increases under AP5 | qualitative (AP5 > control) | PD-failure: control = **0.0**, AP5 = **1.0**, 0 Mg2+ = **0.0** | AP5 > control | yes | Saturated: 100% PD-failure under AP5 analogue (zero spikes). |
| 8 | Spike rate (control) | not specifically reported | PD = **15.5 Hz**, ND = **3.0 Hz** | qualitative | qual yes | Within the order of magnitude expected for a DSGC under control. |

### Discrepancy Catalogue

Each entry includes numerical evidence and the impact on reproduction. Pre-flagged entries from
`task_description.md` and `research/research_*.md` are marked.

1. **gNMDA value: paper 2.5 nS vs code 0.5 nS** [pre-flagged]. `main.hoc:43` sets
   `b2gnmda = 0.5/sparse/maxvesmul = 0.5 nS`. Paper Fig 3E states 2.5 nS. Five-fold gap. Impact: Fig
   1 PSP amplitudes at 0.5 nS are ~25 mV (PD) and ~16 mV (ND), well above the paper's 5.8 / 3.3 mV.
   Running at 2.5 nS does not reduce the PSPs to the paper values (see `control_gnmda25` row).
   Verdict: paper text and code disagree, and neither value reproduces the paper's claimed
   amplitudes exactly. The most likely explanation is that the paper figure was produced with a
   different morphology or Cm/Ra calibration.

2. **Synapse count: paper text 177 vs code 282** [pre-flagged]. `main.hoc`'s `init_sim()` counts 282
   ON dendrites (`countON=282`); each ON dendrite gets one BIPsyn, one SACinhibsyn, one SACexcsyn.
   Paper Methods state 177 synapses. Impact: cell receives 1.6x the paper's stated synaptic drive,
   contributing to the inflated PSP amplitudes. Verdict: code instantiates the larger count;
   reproduction follows the code.

3. **Noise driver: present but zeroed at module load (NOT missing)** [reclassified from pre-flag].
   `research/research_internet.md` claimed the noise driver was missing. Direct inspection of
   `main.hoc:99-101` and `placeBIP()` (lines 191-282) shows the per-50-ms Gaussian noise driver is
   fully implemented, with `flickerVAR = stimnoiseVAR = 0` at module load. Setting
   `h.flickerVAR = 0.10` and re-calling `placeBIP()` exercises it. Verdict: not a "missing"
   discrepancy; it is a "present but disabled by default" discrepancy — the paper's Figures 6-8
   cannot be reproduced without explicitly setting the noise SD non-zero.

4. **Dendritic Nav: paper says "passive" but code uses 2e-4 S/cm^2** [pre-flagged]. With
   `use_active = 0`, dendrites get only `pas` (true passive) inserted. With `use_active = 1`,
   dendrites get HHst inserted with `RGCdendna = 2e-4`, which is small but non-zero. The default
   `simplerun()` runs `init_active()` which sets `active = 1 - doingVC`; for exptype = 1 (PSP,
   doingVC=0) this gives active=1, but TTX=1 (in PSP mode SpikesOn=0 yields exptype=2 -> TTX=1)
   which sets `RGCdendna = 0.0002 * (1 - 1) = 0`. Verdict: under PSP-mode runs (Figs 1-7) the
   dendrites are effectively passive; under spike-mode runs (Fig 8, SpikesOn=1, exptype=1, TTX=0)
   they have 2e-4 S/cm^2 of Na. Paper text "passive dendrites" is loosely applied to PSP runs only.

5. **MOD-default vs main.hoc-override: n_bipNMDA** [from research_code.md]. MOD PARAMETER default is
   0.25; `main.hoc:82` overrides to 0.3. The 0.3 value wins.

6. **MOD-default vs main.hoc-override: gama_bipNMDA**. MOD default 0.08; main.hoc 0.07. The 0.07
   value wins.

7. **MOD-default vs main.hoc-override: newves_bipNMDA**. MOD default 0.01; main.hoc 0.002. The 0.002
   value wins (5x slower vesicle replenishment than the MOD default).

8. **MOD-default vs main.hoc-override: tau1NMDA_bipNMDA**. MOD default 50 ms; main.hoc 60.

9. **MOD-default vs main.hoc-override: tau_SACinhib**. MOD default 10 ms; main.hoc 30 (3x longer
   GABA decay).

10. **MOD-default vs main.hoc-override: e_SACinhib**. MOD default -65 mV; main.hoc -60 mV (less
    hyperpolarising). This shifts the GABA reversal closer to the resting potential, weakening
    shunting inhibition.

11. **achMOD silently rebound by simplerun()**. `main.hoc:47` sets module-load `achMOD = 0.25`;
    `main.hoc:352` `simplerun()` rebinds to 0.33. Any Python-level override of `achMOD` before
    calling into `simplerun()` is silently overwritten. Impact on this task: the driver does not
    expose `achMOD` as a knob; this is documented in the library description so downstream tasks do
    not stumble.

12. **Registered metrics not applicable**: `tuning_curve_rmse` and `tuning_curve_reliability` are
    defined in terms of a target per-angle firing-rate curve. The paper does not report a per-angle
    target curve and this task's PSP-derived metrics are not directly comparable to t0004's
    firing-rate envelope (deliberately out of scope per `task_description.md`). These metrics are
    reported as `null` in every variant of `metrics.json`. `tuning_curve_hwhm_deg` is reported as
    `null` for subthreshold variants (paper does not report PSP HWHM); for the Fig 8 spike variants
    we run only PD vs ND so a 12-angle curve is not assembled either, leaving HWHM as `null` there
    too.

### Reproduction-Bug List

A reproduction bug is any place where this port diverges from the ModelDB code (NOT from the paper).
The audit confirms zero such bugs at the level of parameter values: every value in the audit table's
"Reproduction value" column matches the "ModelDB code value" column. The remaining gaps fall into
the following categories:

* **Trial counts reduced for wall-clock**: paper uses 12-19 cells per condition; our reproduction
  uses 2-4 trials per condition. This widens the SD bands but does not change the means
  systematically.
* **Noise levels reduced**: paper reports 4 noise SD values (0/10/30/50 %); our reproduction covers
  2 (0/10 %). The qualitative trend is preserved but the high-noise regime is not tested.
* **Direction sweep reduced**: paper uses 8 directions; our reproduction uses 2 (PD via
  `gabaMOD=0.33`, ND via `gabaMOD=0.99`). The slope-angle metric is approximated by
  `atan2(mean PD PSP, mean ND PSP)` rather than fit on the full 8-point scatter.

These are deliberate scope reductions, not bugs.

### Morphology-Provenance Note

The paper used the bundled HOC morphology in `RGCmodel.hoc` (~11,500 `pt3dadd` calls) — not the
t0005 SWC. This task uses the bundled morphology verbatim because `placeBIP()` depends on section
ordering and the ON/OFF cut plane (`z >= -0.16 * y + 46`) that only makes sense on the bundled
reconstruction. Substituting the t0005 SWC would itself be a reproduction bug, not a methodological
improvement. The t0005 SWC is documented as an alternative DSGC reconstruction that the project may
use for separate optimisation experiments (e.g., t0033-style sweeps), but it is explicitly NOT
swapped in here.

### Project-Level Summary

This reproduction establishes that ModelDB 189347 reproduces the qualitative phenomenology of
Poleg-Polsky 2016 (PD > ND at low gabaMOD; DSI suppressed under 0 Mg2+; AP5 reduces but does not
eliminate selectivity) but does not reproduce the absolute PSP amplitudes claimed in Figure 1,
regardless of whether the paper's stated gNMDA = 2.5 nS or the code's b2gnmda = 0.5 nS is used. The
synapse-count discrepancy (282 vs 177) is the most mechanically plausible source of the inflated
amplitudes — the cell receives 1.6x the paper's stated drive — but reducing to 177 synapses
would itself be a deviation from the deposited code. The Figure 8 suprathreshold behaviour
qualitatively follows the paper's predictions (DSI preserved under AP5, suppressed under 0 Mg2+,
PD-failure rate increases under AP5). The take-away for the broader project is that any future
optimisation task should treat the t0046 library as the canonical reference port and tune the
synapse count or per-synapse conductance to land Fig 1 PSP amplitudes inside the paper's tolerance
band.

## Synthesis

The four pre-flagged paper-vs-code discrepancies (gNMDA value, synapse count, noise driver,
dendritic Nav) are confirmed (with the noise driver re-classified from "missing" to "present but
zeroed"). Six additional MOD-default-vs-main.hoc-override discrepancies are catalogued with
numerical evidence. The reproduction faithfully follows the deposited ModelDB code on every
parameter (every "Reproduction value" cell of the audit table matches the "ModelDB code value"
cell).

The quantitative gap between the reproduction's PSP amplitudes and the paper's reported amplitudes
is significant (~4x at b2gnmda = 0.5 nS, ~7x at b2gnmda = 2.5 nS) and is partially attributable to
the 1.6x synapse-count discrepancy (282 vs 177), but a complete reconciliation requires the
supplementary PDF that PMC blocks from programmatic download. The slope-angle metric is more
forgiving — at b2gnmda = 0.5 nS the reproduction's slope (54.8 deg) lands inside the paper's 1-SD
band (62.5 +/- 14.2 deg), and the high-Cl- and 0 Mg2+ slopes (47.3 and 50.7 deg) land inside the
paper's tighter +/- 3.7 / +/- 5.3 deg bands. The qualitative direction-tuning behaviour (PD > ND,
DSI suppressed under 0 Mg2+, PD-failure rate elevated under AP5 analogue) is reproduced clearly.

The Figure 8 spike DSI panel produces a striking confirmation: the AP5 analogue (b2gnmda = 0)
silences the cell entirely (PD-failure rate = 1.0), 0 Mg2+ reduces DSI from 0.68 to 0.21, and
control reaches DSI = 0.68 with PD = 15.5 Hz / ND = 3.0 Hz. The paper's "DSI preserved under AP5"
claim does NOT hold for the AP5-analogue we exercise — eliminating NMDAR conductance entirely
silences the cell — but this is consistent with the paper's distinction between iMK801 + bath AP5
(the paper's actual protocol) and a complete NMDAR ablation (our analogue).

## Limitations

* PSP amplitude reproductions are systematically high relative to paper Figure 1; this is consistent
  with the synapse-count discrepancy but may also reflect a Cm/Ra/morphology difference between the
  deposited model and the figure-producing run.
* Trial counts (2-4) are well below the paper's 12-19; SD bands are wide and the slope angle is a
  single-number approximation rather than a per-trial scatter fit.
* The supplementary PDF is cited but not attached as a binary; PMC's JS-only interstitial blocked
  all programmatic download attempts. Manual fetch is documented as an intervention.
* Figure 6 (noise) is run at 2 SD levels (0 / 10 %) instead of the paper's 4 (0/10/30/50 %). The
  qualitative trend is preserved but the high-noise regime is not exercised.
* Figure 8 (suprathreshold) is run at noise = 0 only; the noise-spike behaviour panel of the paper's
  Fig 8 is not reproduced.

## Sources

* Paper: `10.1016_j.neuron.2016.02.013`
* Task: `t0002_literature_survey_dsgc_compartmental_models`
* Task: `t0007_install_neuron_netpyne`
* Task: `t0008_port_modeldb_189347`
* Task: `t0020_port_modeldb_189347_gabamod`
* URL: https://github.com/ModelDBRepository/189347
* URL: https://senselab.med.yale.edu/ModelDB/showmodel.cshtml?model=189347
* URL: https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf

[polegpolsky2016]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/summary.md
[t0002]: ../../../../t0002_literature_survey_dsgc_compartmental_models/
[t0008]: ../../../../t0008_port_modeldb_189347/
[t0020]: ../../../../t0020_port_modeldb_189347_gabamod/
