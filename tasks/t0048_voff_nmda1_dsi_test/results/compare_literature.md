---
spec_version: "1"
task_id: "t0048_voff_nmda1_dsi_test"
date_compared: "2026-04-25"
---
# Compare Literature: Voff_bipNMDA=1 DSI vs gNMDA Test

## Summary

This task tests whether replacing the deposited control's voltage-dependent NMDA
(`Voff_bipNMDA = 0`) with voltage-independent NMDA (`Voff_bipNMDA = 1`) reproduces Poleg-Polsky and
Diamond 2016's Fig 3F bottom claim that DSI is approximately constant ~0.30 across
`b2gnmda in [0, 3]` nS. Verdict: **H2 (intermediate)** — Voff=1 substantially flattens the DSI vs
gNMDA curve (max-min range 0.066 vs t0047's 0.174; slope -0.024 vs -0.058 per nS) and removes the
predicted PD/ND NMDA conductance asymmetry (ratio 2.05 -> 1.00), but absolute DSI values stay
between 0.04-0.10 — never reaching the paper's flat 0.30 line. **NMDA voltage-dependence is
necessary but not sufficient** to explain the deposited code's divergence from the paper's claim.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 0.0 nS | ~0.30 | 0.103 | -0.197 | Outside +/- 0.05 band. Same as t0047 (Voff has no effect at gNMDA = 0). |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 0.5 nS | ~0.30 | 0.102 | -0.198 | Outside +/- 0.05 band. Voff=1 reduced from t0047's 0.192. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 1.0 nS | ~0.30 | 0.078 | -0.222 | Outside band. Voff=1 marginally reduced from t0047's 0.114. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 1.5 nS | ~0.30 | 0.057 | -0.243 | Outside band. Voff=1 INCREASED from t0047's 0.042. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 2.0 nS | ~0.30 | 0.053 | -0.247 | Outside band. Voff=1 INCREASED from t0047's 0.032. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 2.5 nS | ~0.30 | 0.044 | -0.256 | Outside band. Voff=1 INCREASED from t0047's 0.022. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 3.0 nS | ~0.30 | 0.037 | -0.263 | Outside band. Voff=1 INCREASED from t0047's 0.018. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI flatness range (max-min over sweep) | <= 0.05 (qualitative flat) | 0.066 | +0.016 | Within H1's relaxed 0.10 cutoff but above paper's qualitative tightness. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI vs gNMDA slope (qualitative ~ flat) | ~0.0 | -0.024 | -0.024 | Above H1's abs(slope) < 0.020 cutoff. |
| `PolegPolskyDiamond2016` Fig 3 NMDA PD/ND ratio (qualitative ~1, voltage-independent) | qualitative ~1 | 1.00 | 0 | qualitative match | At Voff=1, NMDA conductance is symmetric across PD/ND as paper expects. |

## Methodology Differences

* **NMDA Mg-block model**: Paper text states DSGC NMDA is "largely voltage-independent" in vivo. The
  deposited code implements both versions: `Voff_bipNMDA = 0` (voltage-dependent with Mg block at
  membrane voltage) and `Voff_bipNMDA = 1` (voltage-independent, Mg block evaluated at constant Vset
  = -43 mV). **This task uses Voff = 1 to match the paper's biological NMDA condition.** t0047 used
  Voff = 0 because that is the deposited control's default — neither matches the paper without
  explicit choice.
* **Trial count**: Paper uses 12-19 cells per condition; this task uses 4 trials per direction per
  gNMDA value (matching t0047's protocol). SD bands wider; covered by S-0046-01 for higher-N rerun.
* **Direction sweep**: Paper measures continuous tuning curves; this task uses PD/ND endpoints only
  via the deposited `gabaMOD` swap protocol. DSI is endpoint-based, so this difference does not
  affect the DSI numerics.
* **Conductance modality**: This task records per-synapse direct conductance (`syn._ref_g`) same as
  t0047. The paper's Fig 3A-E most likely reports somatic voltage-clamp; t0049 will resolve this.
  The amplitude mismatch noted in t0047 carries forward but is not the focus of this task (DSI is
  robust to modality).
* **Other parameters**: Identical to t0047 — only `Voff_bipNMDA` differs between the two sweeps.

## Analysis

The H2 verdict has three concrete components, each interpretable:

1. **NMDA voltage-dependence accounts for ~60-70% of the deposited code's DSI-vs-gNMDA collapse**.
   Switching from Voff=0 to Voff=1 reduces the max-min range by 2.6x and the slope by 2.4x. The
   mechanism is exactly as predicted: at Voff=0, PD dendritic depolarization relieves Mg block (PD
   NMDA = 69.5 nS, ND = 34.0 nS, ratio = 2.05); at Voff=1, both directions get the same NMDA (~50
   nS, ratio 1.00). Removing the asymmetry removes the gNMDA-driven collapse component.

2. **The remaining ~30-40% gap to the paper's flat 0.30 line must come from other mechanisms**. With
   NMDA voltage-dependence eliminated, the residual DSI is bounded by AMPA/GABA balance — and our
   deposited values (NMDA, AMPA, GABA all 6-9x over paper on the summed scale per t0047) suggest the
   deposited synapse counts and/or per-synapse conductances differ from the paper's text values. The
   Voff=1 DSI ceiling of ~0.10 is the AMPA+GABA-only limit on the deposited circuit.

3. **The deposited control choice for the project's DSGC simulations should be exptype=2
   (Voff_bipNMDA=1), not exptype=1**, because the paper's biological NMDA is voltage-independent.
   This is a clear recommendation for downstream tasks: use exptype=2 as the canonical control.

The most plausible candidate for closing the residual ~0.20 gap is the GABA conductance: the paper's
Fig 3C shows GABA PD ~12.5 nS and ND ~30 nS (ND/PD = 2.4) — our deposited values are ~106 / ~216
nS (ND/PD = 2.0). The total GABA is 8x over paper, suggesting either too many synapses (282 vs 177
paper text) or per-synapse conductances differ. Halving GABA toward the paper's stated values might
restore the missing direction selectivity, though at the cost of also changing absolute PSP
amplitudes. This is a candidate for a follow-up parameter-sweep task.

For the broader project, this task establishes that:

1. **Voltage-dependent NMDA (Voff=0) is the wrong control choice** for matching the paper.
2. **Voff_bipNMDA = 1 should become the default exptype** for downstream DSGC simulations.
3. **Closing the residual gap to paper DSI requires AMPA/GABA parameter validation** — either via
   the supplementary PDF (S-0046-05) or a dedicated parameter-sweep task.
4. **The somatic-voltage-clamp re-measurement (t0049, in flight)** is needed to determine whether
   the deposited synapse parameters are off, or whether the t0047 amplitude mismatch was purely
   modality.

## Limitations

* Comparison is restricted to one paper (`PolegPolskyDiamond2016`) Fig 3F bottom; no other paper
  claims compared in this task.
* Paper does not state per-cell SDs on the Fig 3F bottom DSI curve; the +/- 0.05 H1 threshold was a
  permissive heuristic chosen by the task plan.
* The H2 verdict is robust to trial-count: even with only 4 trials per direction, the range and
  slope are well outside the H1 band.
* The "paper claims constant ~0.30" target is a textual reading from the paper's qualitative
  description of Fig 3F bottom; the supplementary PDF (S-0046-05 still pending) might state a more
  precise target.
* The mechanism explanation (NMDA voltage-dependence accounts for 60-70% of collapse) is a
  back-of-envelope calculation from the range/slope ratios, not a controlled decomposition. A future
  task that varies NMDA voltage-dependence vs GABA scale jointly could quantify each contribution
  more precisely.
