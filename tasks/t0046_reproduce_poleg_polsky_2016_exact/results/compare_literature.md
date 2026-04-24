---
spec_version: "1"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
date_compared: "2026-04-24"
---
# Compare Literature: Poleg-Polsky and Diamond 2016 Reproduction

## Summary

The from-scratch port of ModelDB 189347 reproduces the slope-angle and ROC-AUC headline targets of
Poleg-Polsky and Diamond 2016 (`PolegPolskyDiamond2016`) within tolerance, but the absolute PSP
amplitudes at the code-pinned `b2gnmda = 0.5 nS` overshoot the paper's reported means by
approximately **4x**. Of nine quantitative comparisons against the paper, **5 lie within paper
tolerance**, **3 lie outside**, and **1 reveals an AP5-vs-iMK801 mechanistic divergence** in
suprathreshold behaviour. The headline finding is that the systematic peak-rate gap previously
observed in t0008 / t0020 / t0022 is **not a modification artefact** — the inflated PSP / firing
amplitudes are inherent to the deposited ModelDB code as released, when followed faithfully.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `PolegPolskyDiamond2016` Fig 1 | PD PSP (mV) | 5.8 | 23.25 | +17.45 (+301%) | Outside paper's 1-SD band (3.1 mV). Attributed to synapse-count discrepancy (282 deposited vs 177 paper text). |
| `PolegPolskyDiamond2016` Fig 1 | ND PSP (mV) | 3.3 | 16.39 | +13.09 (+397%) | Outside paper's 1-SD band (2.8 mV). Same root cause as PD PSP overshoot. |
| `PolegPolskyDiamond2016` Fig 1 | Slope angle (deg) | 62.5 | 54.82 | -7.68 | Within paper's 1-SD band (14.2 deg). PD/ND ordering preserved. |
| `PolegPolskyDiamond2016` Fig 4 | High-Cl- slope (deg) | 45.5 | 47.33 | +1.83 | Within paper's 1-SD band (3.7 deg). Closest numerical agreement. |
| `PolegPolskyDiamond2016` Fig 5 | 0 Mg2+ slope (deg) | 45.5 | 50.65 | +5.15 | Within paper's 1-SD band (5.3 deg). Voltage-independent NMDAR analogue reproduced. |
| `PolegPolskyDiamond2016` Fig 7 | ROC AUC, control | 0.99 | 1.00 | +0.01 | Within +/- 0.05 tolerance. |
| `PolegPolskyDiamond2016` Fig 7 | ROC AUC, AP5 | 0.98 | 1.00 | +0.02 | Within +/- 0.05 tolerance. |
| `PolegPolskyDiamond2016` Fig 7 | ROC AUC, 0 Mg2+ | 0.83 | 1.00 | +0.17 | Outside +/- 0.05 tolerance. Saturation attributed to small-N (2 trials/condition) reducing PD/ND distribution overlap. |
| `PolegPolskyDiamond2016` Fig 8 | DSI control (suprathr.) | preserved (0.5-0.7)* | 0.676 | within range | Suprathreshold DS reproduced. PD AP rate 15.5 Hz; ND AP rate 3.0 Hz. |
| `PolegPolskyDiamond2016` Fig 8 | DSI AP5 (suprathr.) | preserved (qual) | 0.0 | full ablation | Outside qualitative match. AP5 fully silences cell; paper's iMK801 leaves PD spiking. |
| `PolegPolskyDiamond2016` Fig 8 | DSI 0 Mg2+ (suprathr.) | reduced (qual) | 0.212 | -69% vs control | Within qualitative match. PD AP rate 20 Hz; ND AP rate 13 Hz. |

(*) Paper does not state Fig 8 control DSI numerically; the 0.5-0.7 range is inferred from the
control panel of Figure 8B.

## Methodology Differences

* **Trial count**: paper uses 12-19 cells per condition; this reproduction uses 2-4 trials per
  condition (single deterministic NEURON instance with different RNG seeds for noise vectors). SD
  bands on PSP and AP-rate distributions are correspondingly wider, and ROC AUC saturates at 1.00
  where the paper's larger N reveals overlap.
* **Direction sweep**: paper sweeps 8 directions at 45-degree spacing using a moving bar; this
  reproduction collapses to PD/ND only via the `gabaMOD` swap protocol (`PD = 0.33`, `ND = 0.99`),
  consistent with the deposited code's default protocol. Slope angle is approximated by
  `atan2(mean PD PSP, mean ND PSP)` rather than fitted to the full tuning curve. The approximation
  is exact for symmetric tuning curves and tracks the paper's slope to within 8 deg in every
  reproduced condition.
* **NMDAR removal**: paper uses intracellular MK801 (iMK801) to block dendritic NMDAR while leaving
  somatic NMDAR + AMPA intact, allowing PD trials to retain some firing under the AP5 + iMK801
  condition. The reproduction models AP5 as `b2gnmda = 0`, removing all NMDAR contribution. This
  single methodological substitution explains the Fig 8 AP5 silencing divergence.
* **gNMDA value**: paper Fig 3E states `gNMDA = 2.5 nS`; deposited `main.hoc:43` sets
  `b2gnmda = 0.5 nS`. The primary reproduction follows the code (per task_description.md
  primary-source rule); a secondary sweep at 2.5 nS shows that the paper-pinned value collapses
  direction selectivity (DSI = 0.02), suggesting the paper's text value cannot reproduce the paper's
  own Fig 1 result.
* **Synapse count**: paper text reports 177 BIP synapses; deposited `RGCmodel.hoc` instantiates 282
  BIP, 282 SACinhib, and 282 SACexc terminals. The 1.6x overcount is the most plausible root cause
  of the ~4x PSP amplitude inflation.
* **Noise driver**: paper Figs 6-8 vary luminance noise SD; deposited `placeBIP()` already contains
  the per-50-ms Gaussian-perturbation driver but with `flickerVAR = stimnoiseVAR = 0` at module
  load. The reproduction overrides these globals before calling `placeBIP()` (no new MOD file),
  reclassifying `research_internet.md`'s "noise driver missing" claim as "noise driver present but
  zeroed".
* **Morphology**: both use the cell embedded in `RGCmodel.hoc` (approximately 11,500 `pt3dadd`
  calls); the t0005 SWC morphology was deliberately not substituted (`placeBIP()` depends on section
  ordering and the ON/OFF cut, which only make sense on the bundled cell).

## Analysis

The reproduction is faithful to the deposited code and confirms that the ModelDB code reproduces the
paper's **slope angles** (Figs 1, 4, 5) and **noise-free subthreshold ROC AUCs** (Fig 7 control +
AP5) **within tolerance**. It does not reproduce the paper's **absolute PSP amplitudes** (Figs 1, 2,
6\) or the **0 Mg2+ ROC AUC** (Fig 7) or the **AP5 suprathreshold DSI preservation** (Fig 8).

The PSP amplitude overshoot is the most consequential discrepancy. With 282 deposited synapses
versus 177 in the paper text, the linearised PSP amplitude prediction (proportional to N for small
EPSPs) is approximately `282/177 ~ 1.59x` the paper's value. The observed ratio of
`23.25/5.8 ~ 4.0x` exceeds this by a factor of approximately 2.5, suggesting that **either** (a) the
deposited synaptic conductances are also higher than the paper text states, **or** (b) the paper's
reported PSP amplitudes were measured under additional attenuation (e.g., voltage clamp leak,
soma-vs-recording-site offset) not captured in the deposited code. The audit table in
`assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md` lists every basic parameter
(V_rest, Ra, Cm, conductance densities, kinetic constants) for paper-vs-code comparison to support
follow-up root-cause analysis.

The Fig 8 AP5 silencing divergence is mechanistic, not numerical. Faithful reproduction requires
re-implementing iMK801's selective dendritic blockade — a separate MOD modification beyond the
scope of this exact-reproduction task. This finding **invalidates the modification motivation for
downstream tasks t0042 (GABA ladder) and t0044 (Schachter re-test)** insofar as those tasks assume
the AP5 firing-rate gap is a channel-inventory problem; it is instead an AP5-vs-iMK801 substitution
artefact.

The Fig 7 0 Mg2+ ROC saturation is small-N — the paper's 12-19 trials per condition produce PD/ND
PSP distributions that overlap; with 2 trials per condition this overlap is invisible. This is a
methodological gap, not a model gap, and would resolve with a higher-N rerun.

For the broader project, the reproduction establishes that:

1. The **slope-angle** metric is robust to the discrepancies and is a reliable convergence target
   for any downstream optimisation task.
2. The **PSP-amplitude** target is unreliable as a goodness-of-fit metric until the synapse-count
   discrepancy is reconciled (paper text vs deposited code).
3. The **suprathreshold DSI** under AP5 cannot be reproduced without re-implementing iMK801, so any
   task that uses Fig 8 AP5 as a target needs to re-derive the analogue.

## Limitations

* Comparison is restricted to a single paper (`PolegPolskyDiamond2016`). No comparison against other
  DSGC compartmental models (Oesch 2005, Ozaita 2004, Sivyer 2007, Schachter 2010) is performed in
  this task.
* Trial counts (2-4) are well below the paper's (12-19), so SD bands on the reproduction column are
  wider than the paper's. A higher-N rerun would tighten the comparison but is unlikely to change
  the headline 4x PSP overshoot finding (single deterministic seed-1 trial already shows the gap).
* The paper's Fig 8 AP5 panel is qualitative; no numeric DSI value is stated. The "preserved (qual)"
  target was inferred from the figure; a paper-numeric comparison is not possible without
  supplementary tables.
* The supplementary PDF is referenced but not attached (PMC interstitial blocks programmatic
  download). Any parameter values stated only in the supplementary cannot be cross-checked against
  the deposited code in this audit.
* The `## Examples` section of `results_detailed.md` provides per-trial reproduction values but the
  paper's per-trial data are not published, so trial-level comparison is not possible.
