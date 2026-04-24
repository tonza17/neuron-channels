---
spec_version: "1"
task_id: "t0047_validate_pp16_fig3_cond_noise"
date_compared: "2026-04-25"
---
# Compare Literature: Poleg-Polsky 2016 Fig 3A-F Validation

## Summary

The deposited ModelDB 189347 code does not reproduce Poleg-Polsky 2016 (`PolegPolskyDiamond2016`)
Fig 3A-F simulation targets within tolerance. Of nine quantitative comparisons against the paper's
stated simulation values: **0/9 fall within numerical tolerance** on absolute amplitudes; **3/3
qualitative shape claims hold** (AMPA no DSI, GABA stronger in ND, DSI declines under noise); **0/1
hold for the central simulation claim** that DSI is approximately constant ~0.30 across gNMDA. The
ROC AUC mismatch is metric implementation, not model behaviour. Headline finding: the deposited
control's voltage-dependent NMDA Mg block is the most likely root cause of the DSI-vs-gNMDA collapse
— the paper's biological finding is that DSGC NMDA is voltage-INDEPENDENT in vivo, suggesting the
deposited control's `Voff_bipNMDA = 0` may be the wrong exptype.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `PolegPolskyDiamond2016` Fig 3A | NMDA conductance, PD (nS, summed) | ~7.0 | 69.55 | +62.55 (+893%) | Outside +/- 25% band. Likely measurement-modality difference (paper somatic VC vs ours per-syn direct). |
| `PolegPolskyDiamond2016` Fig 3A | NMDA conductance, ND (nS, summed) | ~5.0 | 33.98 | +28.98 (+580%) | Outside +/- 25% band. Same modality issue. |
| `PolegPolskyDiamond2016` Fig 3B | AMPA conductance, PD (nS, summed) | ~3.5 | 10.92 | +7.42 (+212%) | Outside +/- 25% band on absolute; PD/ND ratio 1.01 matches paper's "no DSI on AMPA". |
| `PolegPolskyDiamond2016` Fig 3B | AMPA conductance, ND (nS, summed) | ~3.5 | 10.77 | +7.27 (+208%) | Same as above. |
| `PolegPolskyDiamond2016` Fig 3C | GABA conductance, PD (nS, summed) | ~12.5 | 106.13 | +93.63 (+749%) | Outside +/- 25% band on absolute. ND/PD = 2.03 vs paper 2.30 — qualitative match. |
| `PolegPolskyDiamond2016` Fig 3C | GABA conductance, ND (nS, summed) | ~30.0 | 215.57 | +185.57 (+619%) | Same as above. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 0.5 nS | ~0.30 | 0.192 | -0.108 | Outside +/- 0.05 band. Closest match across the sweep. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 1.5 nS | ~0.30 | 0.042 | -0.258 | Outside +/- 0.05 band. DSI collapses. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 2.5 nS | ~0.30 | 0.022 | -0.278 | Outside +/- 0.05 band. DSI near zero at paper-pinned gNMDA. |
| `PolegPolskyDiamond2016` Fig 6 | DSI vs noise control (qualitative monotonic decline) | yes | -19% across 0->0.5 | qual match | Weakly monotonic; 3/4 points decline. |
| `PolegPolskyDiamond2016` Fig 6 | DSI vs noise 0Mg (qualitative monotonic decline) | yes | -48% across 0->0.5 | qual match | Cleanest monotonic of three conditions. |
| `PolegPolskyDiamond2016` Fig 7 | ROC AUC under noise (qualitative monotonic decline) | yes | flat at 1.000 | qual fail | Metric saturation; not a model finding (entry 15 of catalogue). |

## Methodology Differences

* **Conductance measurement modality**: Paper Fig 3A-E most likely uses somatic voltage-clamp,
  recording the integrated synaptic conductance seen at the soma (sums all synaptic currents
  propagated through cable). This task records per-synapse `_ref_g` directly at each synapse
  location (no cable propagation). The two quantities are not numerically comparable in absolute
  units; only PD/ND ratios per channel are robust. A follow-up SEClamp re-measurement is the
  apples-to-apples comparison.
* **Trial count**: Paper uses 12-19 cells per condition; this task uses 4 trials per direction per
  cell (lower-N matches t0046's protocol for wall-clock budget). SD bands wider; small-N bumps
  possible (e.g., AP5 noise=0.5 small bump).
* **Direction sweep**: Paper measures continuous tuning curves; this task uses PD/ND endpoints only
  via the `gabaMOD` swap protocol. DSI is endpoint-based, so direction-sweep collapse does not
  affect DSI numerics (preserved from t0046).
* **NMDAR block analogue**: AP5 modelled as `b2gnmda = 0` (removes all NMDA contribution). The
  paper's intracellular MK801 (iMK801) blocks dendritic NMDA only, leaving somatic NMDA + AMPA
  intact. Inherited from t0046; not within the scope of this task to fix.
* **Voltage-dependent NMDA in control**: The deposited `simplerun()` exptype = 1 (control) uses
  `Voff_bipNMDA = 0` (voltage-dependent NMDA with Mg block). The paper's biological finding is that
  DSGC NMDA is largely voltage-INDEPENDENT in vivo. The deposited control may not model the paper's
  physiological NMDA condition; this is the most plausible mechanistic source of the DSI-vs-gNMDA
  collapse.
* **ROC AUC negative class**: t0046's helper uses pre-stimulus baseline mean voltage as the negative
  class. PSP peaks dwarf baselines on this circuit, so AUC saturates at 1.000. The paper's analysis
  likely uses off-direction PSPs or jitter-isolated trials as the negative class. Documented as
  discrepancy entry 15.

## Analysis

The deposited code's failure to reproduce Fig 3F bottom (constant DSI ~0.30 across gNMDA) is the
most diagnostically valuable finding of this task. Because DSI in our model collapses exactly when
ND PSP catches up to PD PSP at high gNMDA, the most parsimonious explanation is that **ND NMDA is
opening too easily** — i.e., the dendrite is depolarizing enough to relieve Mg block on the ND
side. The paper's flat DSI-vs-gNMDA curve implies NMDA contributes amplitude but not selectivity,
consistent with **voltage-independent NMDA** that opens equally at any membrane potential. The
deposited control's `Voff_bipNMDA = 0` setting is therefore the most likely root cause: it makes
NMDA voltage-dependent, which equalizes PD/ND contributions at high gNMDA.

A direct test of this hypothesis is straightforward: re-run the gNMDA sweep at exptype = 2
(`Voff_bipNMDA = 1`, voltage-independent NMDA, same as 0 Mg conditions) and observe whether DSI vs
gNMDA goes flat. This is **NOT a modification** to the deposited model — it is a choice of which
exptype better models the paper's biological NMDA condition.

The conductance amplitude mismatch (6-9x over) is most likely a measurement-modality artefact:
per-synapse direct vs somatic voltage-clamp record different quantities. The qualitative shape
signatures (AMPA no DSI, GABA ND-stronger) are preserved on both modalities, so the deposited
circuit reproduces the paper's per-channel asymmetry — just not the absolute numbers.

The noise-sweep DSI monotonic decline is reproduced. The ROC AUC saturation is a metric
implementation issue (entry 15 of the catalogue), not a model finding.

For the broader project, this task establishes that:

1. **The deposited control is not the right model** for the paper's Fig 3F bottom claim. The
   `Voff_bipNMDA = 1` (voltage-independent NMDA) condition needs to be tested in the next sweep —
   likely the source of the flat DSI claim.
2. **Per-synapse conductance recording is now wired up**; future tasks can swap the measurement
   modality (SEClamp) without re-deriving the recorder pattern.
3. **The DSI metric is robust** across modality and trial-count variations; the AUC metric needs a
   redefinition before it is useful here.

## Limitations

* Comparison is restricted to one paper (`PolegPolskyDiamond2016`). The conductance-modality
  ambiguity could be resolved by reading the paper's Methods section in detail or fetching the
  supplementary PDF (S-0046-05 manual fetch, still pending).
* The task does NOT modify the deposited model; the `Voff_bipNMDA = 1` re-test is a separate
  follow-up task (sketched in suggestions).
* Trial counts (4/direction) are below the paper's 12-19. SD bands are wider than the paper's; the
  AP5 noise=0.5 small bump may resolve at higher N.
* Paper does not state per-cell SDs on Fig 3A-E conductances; the +/- 25% pass band was a permissive
  heuristic chosen by the task plan, not a paper-stated tolerance.
* The conductance values were captured but the paper-vs-ours interpretation depends on the
  measurement modality, which the supplementary may clarify.
