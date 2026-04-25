---
spec_version: "2"
answer_id: "dsi-flatness-test-voltage-independent-nmda"
answered_by_task: "t0048_voff_nmda1_dsi_test"
date_answered: "2026-04-25"
confidence: "medium"
---
## Question

Does setting Voff_bipNMDA = 1 (voltage-independent NMDA, the deposited 0 Mg2+ condition) reproduce
Poleg-Polsky and Diamond 2016's claim that DSI vs gNMDA is approximately constant ~0.30 across 0-3
nS?

## Short Answer

No. Voltage-independent NMDA partially flattens the DSI-vs-gNMDA curve — the 0-3 nS range
collapses from 0.174 (Voff_bipNMDA = 0 baseline) to 0.066, satisfying the H1 range threshold of 0.10
— but the slope test still trends downward at -0.024 per nS, above the 0.02 H1 cutoff and never
within +/- 0.05 of the paper's claimed 0.30. The combined verdict is therefore H2 (flatter than the
deposited control but still not flat at 0.30): the Voff = 1 curve runs at 0.04-0.10 across the
entire range, not at 0.30. The Voff_bipNMDA = 1 swap by itself does not reproduce the paper's DSI vs
gNMDA claim.

## Research Process

This task is the direct mechanistic follow-up to [t0047], which documented that the deposited
ModelDB 189347 control (`exptype = 1`, `Voff_bipNMDA = 0`, voltage-dependent NMDA with Mg block)
produces a DSI-vs-gNMDA curve that peaks at 0.19 near gNMDA = 0.5 nS and decays monotonically to
0.018 at gNMDA = 3.0 nS, never matching the paper's claimed flat ~0.30 line. [t0047]'s
compare_literature analysis identified the deposited control's voltage-dependent NMDA as the most
plausible mechanistic source of the collapse: at high gNMDA, the ND dendrite depolarizes enough to
relieve Mg block, ND NMDA opens, and the PD/ND distinction collapses.

Poleg-Polsky and Diamond 2016 [polegpolsky2016] state in the in vivo text that DSGC NMDA is largely
voltage-independent. The deposited code already provides a voltage-independent NMDA setting via
`exptype = 2` (`Voff_bipNMDA = 1`), used in the deposited 0 Mg2+ condition. **This task is not a
model modification** — it is a choice of which deposited exptype best matches the paper's
biological NMDA condition.

Steps:

1. The 56-trial gNMDA sweep (7 grid values x 2 directions x 4 trials) was re-run at
   `exptype = ExperimentType.ZERO_MG` (= 2, sets `Voff_bipNMDA = 1`) using the same
   `_trial_seed_for(gnmda_idx, dir_idx, trial) = 1000 * gnmda_idx + 100 * dir_idx + trial` formula
   as t0047. PD/ND noise realizations therefore match t0047 trial-by-trial, isolating the Voff
   effect.
2. The library asset `modeldb_189347_dsgc_exact` from [t0046] was reused unchanged via cross-task
   package import
   (`from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`).
   The recorder helper (`run_with_conductances.py`) and DSI helper (`dsi.py`) were COPIED with
   attribution from [t0047] because t0047 is not a registered library asset.
3. DSI per gNMDA was computed from the freshly written CSV via the same
   `compute_dsi_pd_nd(*, pd_values, nd_values)` helper used by t0047. Voff = 0 DSI was recomputed
   from t0047's `gnmda_sweep_trials.csv` via the same helper to ensure both curves are evaluated
   identically.
4. Two numerical tests classify the H0 / H1 / H2 verdict (REQ-12): the **range test** takes the
   max-min DSI across the 7 grid points (H1 if <= 0.10, H2 if < t0047's reference 0.174, H0
   otherwise), and the **slope test** takes the linear-regression slope of DSI vs `b2gnmda_ns` (H1
   if `|slope| < 0.02` per nS, H2 if `|slope| < |t0047 reference -0.058|`, H0 otherwise).
5. Per-class summed peak conductances at gNMDA = 0.5 nS were extracted from both CSVs and compared
   in a bar chart to characterize what changed mechanistically.

## Evidence from Papers

The paper [polegpolsky2016] reports that DSGC NMDA conductance in vivo is largely
voltage-independent and that DSI is approximately preserved across a wide range of total synaptic
NMDA conductance (Fig 3F bottom panel, ~0.30 across the same 0-3 nS range tested here). The
deposited ModelDB 189347 mirror of the paper's code is the only implementation publicly available;
[t0046] audited it and confirmed that `exptype = 2`'s only effect (versus `exptype = 1`) is to set
`Voff_bipNMDA = 1`, with every other condition global (`b2gampa`, `b2gnmda`, `s2ggaba`, `s2gach`,
`gabaMOD`, `achMOD`, `Vset_bipNMDA`, channel and cable parameters) unchanged. This is the cleanest
single-variable swap available without forking the model.

The paper's text statement and Fig 3F together claim two things at once: that NMDA is
voltage-independent **and** that DSI stays near 0.30 across the gNMDA range. This task tests the
implication that the first should suffice to produce the second. The result below is that it does
not.

## Evidence from Internet Sources

The `internet` method was not used; [t0046] and [t0047] already exhausted the relevant external
corpus on the deposited model and the paper's claim.

## Evidence from Code or Experiments

### DSI vs gNMDA: Voff = 0 (t0047) vs Voff = 1 (this task) vs paper

| gNMDA (nS) | Voff = 0 DSI (t0047) | Voff = 1 DSI (this task) | Paper target |
| --- | --- | --- | --- |
| 0.0 | 0.103 | 0.103 | ~0.30 |
| 0.5 | 0.192 | 0.102 | ~0.30 |
| 1.0 | 0.114 | 0.078 | ~0.30 |
| 1.5 | 0.042 | 0.057 | ~0.30 |
| 2.0 | 0.032 | 0.053 | ~0.30 |
| 2.5 | 0.022 | 0.044 | ~0.30 |
| 3.0 | 0.018 | 0.037 | ~0.30 |

Source: `results/data/dsi_by_gnmda_voff1.json` and
`results/data/dsi_by_gnmda_voff0_from_t0047.json`, computed from
`results/data/gnmda_sweep_trials_voff1.csv` (this task, 56 rows) and
`tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` (t0047 baseline, 56
rows) using identical `compute_dsi_pd_nd` calls.

The two values at gNMDA = 0.0 are identical (0.103) because Voff has no effect when NMDA conductance
is zero and the per-trial seeds are matched. From gNMDA = 0.5 nS up, the two curves diverge: Voff =
0 peaks then collapses, while Voff = 1 starts lower and stays lower across the entire range.

### H0 / H1 / H2 verdict with numerical evidence

| Test | Voff = 1 value | H1 threshold | t0047 reference | Verdict |
| --- | --- | --- | --- | --- |
| max-min DSI range across 7 grid points | 0.066 | range <= 0.10 | 0.174 | H1 (passes flat-range threshold) |
| absolute linear slope of DSI vs b2gnmda_ns (deg=1 polyfit) | 0.024 per nS | abs slope < 0.02 per nS | 0.058 per nS | H2 (above H1 cutoff but flatter than t0047) |

**Combined verdict: H2.** The Voff = 1 curve is roughly **2.6x flatter** than the Voff = 0 baseline
by both range (0.066 vs 0.174) and slope (-0.024 vs -0.058) measures, but it is not flat in absolute
terms (it still trends downward) and it never approaches the paper's claimed ~0.30 line — every
Voff = 1 grid value sits in the 0.04-0.10 band, 0.20-0.26 below the paper target. Source:
`results/data/verdict_voff1.json`.

![DSI overlay: Voff = 0 vs Voff = 1 vs paper](../../../results/images/dsi_vs_gnmda_voff0_vs_voff1.png)

### Per-direction PSP amplitude comparison

| gNMDA (nS) | Voff = 0 PD (mV) | Voff = 0 ND (mV) | Voff = 1 PD (mV) | Voff = 1 ND (mV) |
| --- | --- | --- | --- | --- |
| 0.5 | 24.27 +/- 1.02 | 16.47 +/- 0.24 | 22.76 +/- 0.44 | 18.55 +/- 0.16 |
| 1.5 | 38.69 +/- 0.19 | 35.60 +/- 0.35 | 31.07 +/- 0.30 | 27.74 +/- 0.26 |
| 2.5 | 41.98 +/- 0.34 | 40.16 +/- 0.29 | 34.51 +/- 0.38 | 31.62 +/- 0.43 |

Means +/- standard deviation across 4 trials, drawn from `peak_psp_mv` in both per-trial CSVs. Voff
= 1 PSPs are systematically lower than Voff = 0 PSPs at gNMDA >= 1.0 nS — voltage-independent NMDA
does not amplify at depolarized voltages, so the runaway Mg-block-relief feedback that swells Voff =
0 PSPs to ~42 mV at gNMDA = 2.5 nS is absent in Voff = 1.

### Per-class summed peak conductance comparison at gNMDA = 0.5 nS

| Synapse class | Voff = 0 PD (nS) | Voff = 0 ND (nS) | Voff = 1 PD (nS) | Voff = 1 ND (nS) |
| --- | --- | --- | --- | --- |
| NMDA | 69.55 | 33.98 | 50.16 | 50.08 |
| AMPA | 10.92 | 10.77 | 10.92 | 10.77 |
| GABA | 106.13 | 215.57 | 106.13 | 215.57 |

Means across 4 trials. AMPA and GABA values are identical between Voff = 0 and Voff = 1 because
Voff_bipNMDA only affects NMDA channel kinetics in `bipolarNMDA.mod`. The NMDA column carries the
entire mechanistic story: under Voff = 0, PD NMDA opens 2.05x more than ND NMDA (69.55 vs 33.98 nS)
because the depolarized PD dendrite relieves Mg block. Under Voff = 1, PD and ND NMDA are
essentially equal (50.16 vs 50.08 nS, ratio 1.00). The voltage-driven asymmetry that gave Voff = 0
its DSI peak is gone, and the remaining DSI is driven only by AMPA-vs-GABA balance (which is itself
PD/ND asymmetric: ND has 2.03x more GABA than PD).

![Conductance comparison at gNMDA = 0.5](../../../results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png)

## Synthesis

The Voff_bipNMDA = 1 swap delivers exactly what the mechanistic prediction in [t0047]'s
research_code.md said it would on the conductance side: it removes the voltage-driven PD/ND
asymmetry from NMDA. At gNMDA = 0.5 nS the PD-vs-ND NMDA conductance ratio collapses from 2.05 (Voff
= 0) to 1.00 (Voff = 1), and PSP amplitudes no longer balloon as gNMDA increases. The combined
verdict (H2) reflects the two-sided nature of this result: the curve does flatten substantially
(range halves, slope more than halves), but it does not flatten at the paper's claimed 0.30 line —
it flattens at roughly 0.05-0.10 instead.

The interpretation is that the deposited code's two control choices — `exptype = 1`
(voltage-dependent NMDA, the published "control" in main.hoc) and `exptype = 2` (the deposited "0
Mg2+" / voltage-independent setting) — both fall short of the paper's Fig 3F flat-0.30 claim, but
for opposite reasons. `exptype = 1` produces a peaked curve that crosses 0.19 once and drops, driven
by the runaway Mg-block-relief feedback at high gNMDA. `exptype = 2` produces a much flatter curve
that never crosses 0.10, because removing the NMDA voltage dependence eliminates the very PD/ND
asymmetry that would have produced a high baseline DSI in the first place. Neither setting alone
reproduces both the paper's qualitative shape (flat) and absolute level (0.30); a secondary
mechanism — likely the AMPA / GABA balance, the SAC inhibition kinetics, or the b2gampa value
relative to gNMDA — must be co-tuned to explain the published result.

For the project's deposited-control choice, the Voff = 1 result strengthens [t0047]'s position that
the deposited code does not faithfully reproduce Fig 3F under either exptype = 1 or exptype = 2.
Future tasks should investigate the ampa-gaba balance, an explicit SEClamp re-measurement of
conductances under both Voff settings, and the sensitivity to `gabaMOD` swing (`PD = 0.33`,
`ND = 0.99`, the asymmetry that drives the remaining Voff = 1 DSI).

## Limitations

* **Small N per condition** (4 trials per direction per gNMDA value, 56 trials total). Standard
  deviations on `peak_psp_mv` are 0.16-1.02 mV, well below the trial-to-trial PD/ND difference, so
  the means are not noise-limited; the verdict labels are robust to the chosen sample size.
* **Single sweep dimension.** Only `b2gnmda` was swept; `b2gampa` (= 0.25 nS), `s2ggaba` (= 0.5 nS),
  `gabaMOD` swing (PD = 0.33, ND = 0.99), and `Vset_bipNMDA` (= -43 mV) were left at the deposited
  canonical values. A two-dimensional sweep over (gNMDA, X) for each of these would be needed to
  identify which co-tuning recovers the paper's 0.30 baseline.
* **No AP5 cross-control.** The paper uses pharmacological AP5 to ablate NMDA; we emulated this in
  `exptype = 1` by setting `b2gnmda_override = 0.0`. The data point at gNMDA = 0.0 is therefore the
  de-facto AP5 condition and shows DSI = 0.103 — so even with NMDA fully ablated, the deposited
  cell does not reach the paper's 0.30 baseline. This is independent evidence that the gap between
  this task's Voff = 1 result and the paper's claim is not localized to NMDA voltage-dependence.
* **No SEClamp re-measurement.** The conductance measurements are forward-mode peaks of the synaptic
  state variables under the soma's natural voltage trace, not a voltage-clamp re-measurement that
  would isolate driving force from gating. Task [S-0047-02][s-0047-02] is queued to address this.
* **No noise sweep under Voff = 1.** This task focused on the DSI-vs-gNMDA flatness hypothesis only;
  the noise extension (Fig 6/7 of the paper) was not re-run under Voff = 1.
* **Verdict thresholds are subjective.** The H1 range threshold (0.10) and slope threshold (0.02 per
  nS) were set in the plan from the task description's "+/- 0.05 of some constant" criterion. The H2
  reference values (0.174 range, -0.058 slope per nS) were taken from t0047's empirical numbers. A
  tighter or looser choice would not change the qualitative finding (Voff = 1 is flatter but not
  flat at 0.30).

## Sources

* Paper: `10.1016_j.neuron.2016.02.013` (Poleg-Polsky and Diamond 2016, Neuron Fig 3F)
* Task: `t0046_reproduce_poleg_polsky_2016_exact` (library asset, deposited code audit)
* Task: `t0047_validate_pp16_fig3_cond_noise` (Voff = 0 baseline DSI sweep, recorder pattern, DSI
  helper)

[polegpolsky2016]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/summary.md
[t0046]: ../../../../t0046_reproduce_poleg_polsky_2016_exact/
[t0047]: ../../../../t0047_validate_pp16_fig3_cond_noise/
[s-0047-02]: ../../../../t0047_validate_pp16_fig3_cond_noise/results/suggestions.json
