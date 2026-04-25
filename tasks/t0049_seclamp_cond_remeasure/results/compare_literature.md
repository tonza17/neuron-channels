---
spec_version: "1"
task_id: "t0049_seclamp_cond_remeasure"
date_compared: "2026-04-25"
---
# Compare Literature: SEClamp Conductance Re-Measurement vs Poleg-Polsky 2016 Fig 3A-E

## Summary

Measuring per-channel synaptic conductance under a somatic SEClamp on the deposited DSGC yields
values that lie **between** Poleg-Polsky 2016 (`PolegPolskyDiamond2016`) Fig 3A-E targets and
t0047's per-synapse-direct measurements. **Verdict: H2 (intermediate) for all 6 channel x direction
cells**: SEClamp is 5-10x smaller than per-syn-direct (modality reduction CONFIRMED) but still
1.7-5x over paper. Most diagnostic: GABA PD/ND symmetry under SEClamp (PD = 47.47 nS, ND = 48.04 nS)
**contradicts** the paper's reported PD ~12.5 / ND ~30 nS — the deposited code's GABA distribution
does not produce the paper's somatic ND-bias. Modality alone does not reconcile the deposited code
with paper Fig 3A-E.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `PolegPolskyDiamond2016` Fig 3A | NMDA conductance, PD (nS) | ~7.0 | 13.89 | +6.89 (+98%) | SEClamp; 9.1x closer to paper than t0047's per-syn (893% over). Outside +/- 25%. |
| `PolegPolskyDiamond2016` Fig 3A | NMDA conductance, ND (nS) | ~5.0 | 13.71 | +8.71 (+174%) | SEClamp; 3.3x closer to paper than t0047's per-syn (580% over). Outside +/- 25%. |
| `PolegPolskyDiamond2016` Fig 3B | AMPA conductance, PD (nS) | ~3.5 | 5.93 | +2.43 (+69%) | SEClamp; 3.1x closer than t0047 per-syn (212% over). Within tolerance for AMPA-no-DSI claim (PD/ND ratio 1.02 vs paper 1.0). |
| `PolegPolskyDiamond2016` Fig 3B | AMPA conductance, ND (nS) | ~3.5 | 5.79 | +2.29 (+65%) | SEClamp; 3.2x closer than t0047 per-syn (208% over). |
| `PolegPolskyDiamond2016` Fig 3C | GABA conductance, PD (nS) | ~12.5 | 47.47 | +34.97 (+280%) | SEClamp; 2.7x closer than t0047 per-syn (749% over). Outside +/- 25%. |
| `PolegPolskyDiamond2016` Fig 3C | GABA conductance, ND (nS) | ~30.0 | 48.04 | +18.04 (+60%) | SEClamp; 10.3x closer than t0047 per-syn (619% over). Closest to paper of all 6 cells. |
| `PolegPolskyDiamond2016` Fig 3 | NMDA PD/ND ratio | ~1.4 (PD-biased) | 1.01 | -0.39 | SEClamp removes asymmetry. t0047 had +0.34 DSI; SEClamp +0.006. |
| `PolegPolskyDiamond2016` Fig 3 | AMPA PD/ND ratio | ~1.0 (no DSI) | 1.02 | +0.02 | Within tolerance. AMPA's no-DSI signature preserved across modalities. |
| `PolegPolskyDiamond2016` Fig 3 | GABA PD/ND ratio | ~0.42 (ND-biased) | 0.99 | +0.57 | Outside tolerance. SEClamp completely removes the paper's ND-bias. Major discrepancy. |
| `PolegPolskyDiamond2016` Fig 3 | NMDA conductance DSI | ~+0.17 | +0.006 | -0.16 | SEClamp removes the PD-bias. |
| `PolegPolskyDiamond2016` Fig 3 | GABA conductance DSI | ~-0.41 | -0.006 | +0.40 | SEClamp removes the ND-bias entirely. |

## Methodology Differences

* **Measurement modality**: Paper Fig 3A-E most likely reports somatic voltage-clamp recordings in
  vitro. This task uses NEURON's `SEClamp` at the soma center segment with
  `dur1 = h.tstop, amp1 = -65 mV, rs = 0.001 MOhm` — effectively a perfect voltage source. The
  clamp voltage SD across all 32 trials is 1-3e-4 mV, well below tolerance. This is the
  apples-to-apples comparison with the paper.
* **Channel isolation protocol**: This task isolates channels via Python overrides to
  `h.b2gampa = 0`, `h.b2gnmda = 0`, `h.gabaMOD = 0` after `simplerun()` returns, then re-calls
  `placeBIP()` and re-runs the simulation. The paper presumably isolates channels pharmacologically
  (NBQX for AMPA, AP5 for NMDA, picrotoxin/bicuculline for GABA-A). The effect on the postsynaptic
  conductance is identical (the channel's conductance is set to zero), but the cellular state during
  isolation might differ subtly from a pharmacological block.
* **Trial count**: Paper uses 12-19 cells per condition; this task uses 4 trials per direction per
  channel-isolation. SD bands wider; covered by S-0046-01 / S-0048-04 for higher-N reruns.
* **Single condition**: This task measures only at gNMDA = 0.5 nS, exptype = control. The paper's
  Fig 3A-E may include multiple conditions. Future tasks may want to repeat this measurement at
  exptype = 2 (Voff_bipNMDA = 1, per t0048's recommendation).
* **Direction sweep**: Paper measures continuous tuning curves; this task uses PD/ND endpoints only
  via the deposited `gabaMOD` swap protocol. PD/ND is sufficient for Fig 3A-E channel-isolation
  comparison.
* **bipolarNMDA.mod AMPA/NMDA independence**: confirmed at the MOD source level (per
  research_code.md). `b2gampa = 0` zeros only AMPA leaving NMDA active and vice versa, so channel
  isolation works cleanly on the dual-component bipolar synapse.
* **Reversal potentials**: NMDA = AMPA = 0 mV, SACinhib = -60 mV (per main.hoc override, not the MOD
  default of -65 mV). This was already catalogued in t0046's audit.

## Analysis

### Diagnostic finding 1: modality reduction confirmed

SEClamp values are 5-10x smaller than t0047's per-synapse-direct sums. This explains a major
fraction of the t0047 amplitude mismatch with paper — t0047's per-synapse-direct measurement was
over-counting by aggregating local conductance values that don't sum linearly at the soma due to
cable attenuation and driving-force interactions. The somatic SEClamp is the right modality for the
paper Fig 3A-E comparison.

### Diagnostic finding 2: residual amplitude mismatch is NOT modality

Even after modality correction, all 6 channel x direction cells are 1.7-5x over the paper's stated
values:

* NMDA PD: 13.89 nS vs paper 7.0 (98% over)
* NMDA ND: 13.71 vs 5.0 (174% over)
* AMPA PD/ND: ~5.9 vs 3.5 (~67% over both)
* GABA PD: 47.47 vs 12.5 (280% over)
* GABA ND: 48.04 vs 30.0 (60% over)

The residual mismatch is consistent with the 282-vs-177 synapse-count discrepancy from t0046's audit
(282/177 = 1.59x). For NMDA and GABA PD, the over-counting factor exceeds 1.59x, suggesting
per-synapse conductances may also differ from paper's text values (or that the spatial distribution
puts more synapses electrically close to the soma than paper's distribution).

### Diagnostic finding 3: direction asymmetries collapse under SEClamp

Three concrete asymmetries that t0047's per-syn-direct measurement showed DISAPPEAR under SEClamp:

* NMDA: t0047 PD/ND DSI +0.34 (PD-biased); SEClamp +0.006 (symmetric).
* GABA: t0047 PD/ND DSI -0.34 (ND-biased); SEClamp -0.006 (symmetric).
* Paper claims: NMDA DSI ~+0.17, GABA DSI ~-0.41. Both expected at the soma.

The SEClamp gives both PD and ND directions essentially the same conductance. This means the
deposited code's spatial synapse distribution, when integrated through cable filtering, does NOT
produce a somatic PD/ND asymmetry — even though local-synapse measurements (per t0047) do show
asymmetry. The paper's Fig 3A-E SHOULD show the somatic asymmetry by their own measurement modality.

Possible mechanisms for this discrepancy:

1. The deposited code's GABA synapses are spatially distributed roughly equally across PD-side and
   ND-side dendrites (the `gabaMOD` swap simply scales their gain symmetrically across both sides),
   so the somatic measurement sees no asymmetry. The paper's actual synapse distribution may put
   more GABA on the ND-side dendrites.
2. The deposited code's cable filtering averages out the local asymmetry by the time the current
   reaches the soma. The paper's morphology may have different cable properties that preserve local
   asymmetry better at the soma.
3. The paper's stated values for PD ~12.5 and ND ~30 nS may reflect a sublocal measurement at a
   specific dendritic site, not a true somatic SEClamp.

### Implication for the broader project

This task plus t0048 together establish:

1. **t0048 finding**: NMDA voltage-dependence accounts for ~60-70% of the DSI-vs-gNMDA collapse in
   the deposited code. Voff_bipNMDA = 1 should be the canonical control choice.
2. **t0049 finding (this task)**: per-synapse direct conductances are 5-10x over the somatic
   measurement; SEClamp modality correction is necessary. After modality correction, the deposited
   code is still 1.7-5x over paper amplitudes and ~0 PD/ND asymmetry vs paper's claimed strong
   asymmetry.
3. **Combined**: the residual 30-40% gap to paper DSI noted in t0048 is consistent with this task's
   GABA symmetry collapse — if the deposited GABA had the paper's PD-biased asymmetry, DSI would
   presumably increase. The next step is a synapse-distribution audit comparing deposited spatial
   coordinates against paper text, or a parameter scan reducing GABA toward paper's stated values to
   test whether DSI then approaches 0.30.

## Limitations

* Comparison is restricted to `PolegPolskyDiamond2016` Fig 3A-E only.
* The paper's exact Fig 3A-E protocol (clamp potential, holding solution, channel isolation method)
  is not stated in the text we have access to. The supplementary PDF (S-0046-05 still pending) might
  clarify these details.
* Single condition tested (gNMDA = 0.5 nS, exptype = control). t0048's recommended exptype = 2 is
  not tested here.
* Trial counts (4 per direction per channel-isolation) are below paper's 12-19. SD bands are wider
  than paper's; reported in every comparison.
* Channel isolation via global overrides may not perfectly match the cellular state under
  pharmacological block. The MOD-level conductances are zeroed identically, but the cellular
  environment (ion concentrations, local potentials) might differ subtly.
* The paper does not state per-cell SDs on Fig 3A-E; H2 verdict was based on the task plan's
  permissive +/- 25% heuristic.
* GABA driving force is small (-5 mV at V_clamp = -65 mV vs E_GABA = -60 mV). Small driving force
  amplifies noise in conductance estimation. The +/- 1.98 nS GABA SD already accounts for this; a
  more sensitive measurement would use a different V_clamp.
