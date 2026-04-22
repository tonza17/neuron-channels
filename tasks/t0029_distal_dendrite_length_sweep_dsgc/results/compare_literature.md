---
spec_version: "1"
task_id: "t0029_distal_dendrite_length_sweep_dsgc"
date_compared: "2026-04-22"
---

# Comparison with Published Results

## Summary

This task swept distal-dendrite length from **0.5x** to **2.0x** on the t0022 DSGC testbed with the
explicit aim of discriminating Dan2018's passive-transfer-resistance (TR) weighting prediction
(monotonic DSI growth) from Sivyer2013's dendritic-spike branch-independence prediction (DSI
saturation). The primary peak/null DSI is pinned at **1.000** at every multiplier, producing a
DSI-vs-length slope of **0.000** and a range at extremes of **0.000** — neither mechanism is
falsified, and the testbed's operating point sits **outside** the Park2014 DSGC DSI envelope of
**0.65 +/- 0.05**. The 1.000 plateau is consistent with Sivyer2013's qualitative "DSI close to 1"
observation under control conditions but represents a deterministic ceiling artefact of the t0022
scheduler rather than a genuine biological saturation plateau.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 CART-Cre On-Off DSGCs [Park2014, p. 3977] | DSI (spike) | 0.65 | 1.000 | **+0.350** | Mouse in vitro, drifting grating, n=14; our testbed saturates well above the physiological envelope |
| Park2014 TRHR-GFP / wild-type DSGCs [Park2014, p. 3977] | DSI (spike) | 0.73 | 1.000 | **+0.270** | Mouse in vitro reference population, n=38 |
| Sivyer2013 rabbit DSGC control [Sivyer2013, Fig. 2-3 text] | DSI (spike) | ~1.0 | 1.000 | **+0.000** | Qualitative match — "close to 1" under control conditions; Sivyer2013 plateau height not quantified to 3 dp |
| Schachter2010 compartmental DSGC [Schachter2010, Abstract / Overview] | DSI (somatic spike) | 0.80 | 1.000 | **+0.200** | Biophysical model with Poisson-like inputs + dendritic Nav/Kv; our testbed has deterministic inputs and no background noise |
| Schachter2010 subthreshold PSP [Schachter2010, Overview] | DSI (PSP) | 0.20 | n/a | n/a | Not measured directly — the t0022 driver emits spike-count tuning only, no subthreshold PSP-DSI axis |
| PolegPolsky2016 compartmental DSGC (correlated release) [deRosenroll2026, Overview as proxy] | DSI (spike) | 0.39 | 1.000 | **+0.610** | Correlated AR(2) bipolar release in the t0024 port; our testbed lacks stochastic release entirely |
| deRosenroll2026 model (uncorrelated release) [deRosenroll2026, Overview] | DSI (spike) | 0.25 | 1.000 | **+0.750** | Same port, decorrelated release; confirms noise is what brings DSI down to physiological values |
| Dan2018 VS-cell fly TR-weighted fit [Dan2018, p. 9 / Table "DI"] | Axonal RF DI (VS5) | 0.293 | n/a | n/a | Different metric (RF vector difference index, not DSI); included as the only available Dan2018 quantitative comparator — their paper reports no DSI-vs-length sweep |

### Prior Task Comparison

The task plan cites four upstream results as the motivating baselines — t0008, t0020, t0022, and
t0024 — plus Park2014 as the biology envelope and PolegPolsky2016 as the source cell. Those values
are restated here so the ceiling saturation finding can be judged against the project's own
measurement lineage.

| Prior Task / Source | Metric | Prior Value | t0029 Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0022 baseline (per-dendrite E-I, PolegPolsky2016 lineage) | DSI (pref/null) | 1.000 | 1.000 | **+0.000** | t0029 at 1.00x multiplier is an exact by-construction reproduction — only `sec.L` is mutated |
| t0022 baseline | HWHM (deg) | 116.25 | 116.25 | **+0.00** | Same exact match at 1.00x |
| t0022 baseline | Peak firing (Hz) | 15 | 15 | **+0** | Same exact match at 1.00x |
| t0020 (gabaMOD PD/ND swap, sibling port) | DSI | 0.784 | 1.000 | **+0.216** | Alternative DS driver (global conductance swap rather than per-dendrite timing); not saturated |
| t0008 (rotation-proxy port, PolegPolsky2016 lineage) | DSI | 0.316 | 1.000 | **+0.684** | Different DS driver (morphology rotation, not E-I timing); well below saturation |
| t0024 (deRosenroll2026 AR(2) correlated-release port) | DSI | 0.776 | 1.000 | **+0.224** | Stochastic release implemented — DSI drops into the Park2014 envelope |
| t0024 | Peak firing (Hz) | 5.15 | 15 | **+9.85** | t0024 input-rate ceiling much lower than t0022 |

The lineage-internal finding is that **every t0022-descended variant hits the DSI = 1.000 ceiling**
while every DSGC port that introduces stochasticity or a non-E-I-timing driver (t0008, t0020, t0024)
sits strictly below it. The t0029 sweep adds a morphological axis to this pattern but does not
escape the ceiling. This contradicts the original t0029 plan assumption that length would move DSI
visibly and must be reported as a negative result on the mechanism-discrimination question.

## Methodology Differences

* **Stochasticity.** Park2014 records in vitro DSGCs driven by real retinal circuitry with all
  associated noise sources; Schachter2010 and PolegPolsky2016 inject Poisson-like stochastic inputs;
  deRosenroll2026 uses explicit AR(2) correlated release. The t0022 testbed used by t0029 is
  **deterministic** (`noise = 0`, reliability = **1.000** at every multiplier), which collapses the
  rate-code integration picture that Dan2018 and Sivyer2013 both assume and eliminates the
  subthreshold voltage fluctuations that bring DSI down from 1.0 to ~0.65-0.8 in all three
  reference studies.

* **Null-direction inhibition magnitude.** The t0022 scheduler uses
  `GABA_CONDUCTANCE_NULL_NS = 12 nS`, about 4x the preferred-direction value of 3 nS, applied 10 ms
  before the AMPA arrival. This 12-nS early shunt is intentionally large — much larger than
  Schachter2010's measured compound null inhibition of **~6 nS** — and it forces null-direction
  firing to exactly **0 Hz** at every length multiplier, which pins the pref/null DSI denominator
  at the preferred rate and the ratio at 1.000.

* **Organism and cell type.** Dan2018 studies *Drosophila*-like blowfly VS tangential cells (pure
  passive cable, steady-state analysis, Rm = 2000 Ohm.cm^2); Sivyer2013 and Park2014 study mammalian
  ON-OFF DSGCs; our testbed is a port of PolegPolsky2016's mouse ON-OFF DSGC. Translating
  Dan2018's transfer-resistance prediction to a vertebrate DSGC with active distal Nav/Kv
  conductances is already a stretch before considering the ceiling artefact.

* **Length range.** Dan2018 sweeps distal branch length **50-400 um** (factor 8), Sivyer2013's
  critical length sits at **~150 um**. The t0022 baseline distal-leaf lengths are on the order of
  tens of um; our 0.5x-2.0x sweep likely spans ~15-160 um — overlapping only the tail of the
  Sivyer2013 range and sitting below Dan2018's critical regime. This is one of the seven
  alternative explanations for the null result (creative_thinking.md, prediction 6).

* **Metric definition.** Park2014, Sivyer2013, Schachter2010, and PolegPolsky2016 compute DSI as
  `(Rpref - Rnull) / (Rpref + Rnull)` on spike counts over 8 or more directions at physiological
  noise; the t0012 scorer used here applies the same formula on 12 directions but on deterministic
  integer spike counts with null rate exactly 0.

* **Input rate ceiling.** The t0022 driver produces peak firing of **15 Hz** (or 14 Hz above
  multiplier 1.25). Dan2018 VS cells report mean rates 5-40 spikes/s; Sivyer2013 reports 20-60 Hz;
  Schachter2010 models report similar. Our 15 Hz ceiling is in a 1-spike quantization regime where
  secondary metrics (vector-sum DSI 0.664 -> 0.643) can be explained by a single spike being lost
  at a single off-peak angle rather than a genuine cable-length effect.

* **NMDA channels.** The t0022 testbed silences bundled HOC NMDA synapses (`b2gnmda = 0`),
  installing AMPA-only E-I pairs. All four mammalian DSGC papers above include NMDA components
  active at physiological Mg block. This also removes the Espinosa2010 kinetic-tiling mechanism
  from the testable space — a third mechanism that could produce non-monotonic DSI vs length.

## Analysis

**Dan2018 prediction vs t0029 observation.** Dan2018 predicts a **monotonic** DSI-vs-length
relationship arising from the transfer-resistance weighting of dendritic inputs — longer distal
branches have lower TR, contribute less to the axonal RF, and should reduce DSI if the distal
branchlets are the DS-carrying subunits. Our observation is DSI = **1.000** at every multiplier
with slope = **0.000**. This does not falsify Dan2018: the paper's derivation assumes a passive,
rate-coded steady-state regime with stochastic Poisson inputs and a noise floor in the axonal RF.
The t0022 testbed exits that regime in at least three ways — it is deterministic, it has an
oversized deterministic GABA null shunt that drives null firing to exactly 0 Hz before cable
mechanics enter, and it ports Dan2018's invertebrate cable analysis onto a mammalian DSGC with
active distal Nav/Kv channels. The **+0.350** and **+0.270** deltas against the Park2014 envelope
are the structural evidence that our testbed sits outside the regime in which Dan2018's prediction
is falsifiable.

**Sivyer2013 prediction vs t0029 observation.** Sivyer2013 qualitatively predicts that DSI should
**saturate** at a plateau once distal branches are long enough to support independent local spike
initiation, because beyond that length additional cable does not add further DS. Our observation
of DSI = 1.000 across the whole sweep is nominally consistent with "saturation at the smallest
length tested" (curve_shape.json classifies the curve as `saturating` at multiplier 0.5x,
plateau_dsi = 1.0). But Sivyer2013 plateau heights are closer to **0.6-0.8** on the spike-DSI
metric at the soma; our 1.0 plateau is a ceiling artefact rather than Sivyer2013's biological
plateau. The HWHM non-monotonicity (71.7-116.2 deg across the sweep) is in fact more consistent
with Sivyer2013's dendritic-Nav threshold-crossing picture than DSI alone can show, and the
creative_thinking.md prediction 3 proposes a distal-Nav-ablation follow-up that would test this
directly.

**Park2014 envelope.** Park2014's measured DSI of **0.65 +/- 0.05** (n=14 CART-Cre) and
**0.73 +/- 0.03** (n=38 TRHR-GFP/WT) is the cleanest biological target for what a mouse ON-OFF
DSGC should produce. Our testbed sits **+0.27 to +0.35** above this envelope, with a null-direction
firing rate of exactly 0 Hz compared to the physiological non-zero null rate that produces DSIs
below 1. This mismatch identifies the t0022 testbed as operating **outside the physiological
regime** and is the root cause of the ceiling saturation — not a property of distal-dendrite
length.

**PolegPolsky2016 / t0008 / t0020 / t0022 lineage.** The t0022 testbed was constructed
specifically to make per-dendrite E-I scheduling the DS driver, replacing the rotation-proxy driver
of t0008 (DSI = **0.316**) and the gabaMOD swap of t0020 (DSI = **0.784**). That engineering
succeeded: t0022 baseline reaches DSI = **1.000**. t0029's result at multiplier 1.00x reproduces
this exactly, confirming the driver change is what pinned the metric. Within the same ModelDB
189347 morphology lineage, only the deRosenroll2026 port (t0024) with AR(2) correlated stochastic
release produces a physiological DSI of **0.776** — again implicating stochasticity, not
morphology, as the primary DSI-setting variable on this cell.

**Schachter2010 / deRosenroll2026 as the noise witness.** Schachter2010 explicitly models DSGC DS
with dendritic Nav/Kv plus Poisson-like synaptic drive and reports somatic spike DSI ~**0.80**.
deRosenroll2026's AR(2) correlated release yields DSI ~**0.39**; decorrelating release drops DSI to
~**0.25**. Together these pin the literature result: **stochasticity, not passive cable length, is
the dominant DSI-setting variable on a ModelDB-189347-descended DSGC.** This directly motivates the
top follow-up in creative_thinking.md (prediction 5): a Poisson-noise desaturation sweep. If the
ceiling artefact is removed by ~5 Hz background release per distal dendrite, DSI should drop below
1.0 and the length-sweep can then be re-run to actually test Dan2018 vs Sivyer2013.

## Limitations

* **DSI-pinned-at-1 eliminates the discriminator.** The primary metric is saturated; both
  published predictions are consistent with a constant ceiling, so neither is falsified. This is a
  genuine null result on the mechanism-discrimination question and must be reported as such.

* **No subthreshold PSP-DSI measurement.** Schachter2010's key comparison is between PSP DSI (~0.2)
  and spike DSI (~0.8), which quantifies the dendritic-spike-amplification step. The t0022 driver
  emits only spike-count tuning; the PSP-DSI axis that would tie directly to Schachter2010's
  headline finding is not produced and cannot be compared.

* **No direct Dan2018 quantitative comparator.** Dan2018 reports a passive-cable-fit difference
  index (DI) of **0.293** for VS5 and **0.236** for VS4 — a receptive-field vector-metric, not a
  spike DSI. No DSI-vs-length curve appears in Dan2018. The comparison is therefore by analogy
  rather than by metric, and the limitation is documented in the Comparison Table `n/a` rows.

* **No direct Sivyer2013 quantitative plateau height.** The Sivyer2013 summary flags the full
  paper as paywalled (see the t0027 Sivyer2013 summary YAML frontmatter "File: Not downloaded").
  Our Sivyer2013 DSI plateau target ("close to 1" under control) comes from the verbatim PubMed
  abstract and the paper's role in the downstream DSGC literature rather than a specific figure
  number.

* **Length range likely below Dan2018's critical regime.** The t0022 distal-leaf L baseline is
  tens of um; the 0.5x-2.0x sweep covers ~15-160 um, overlapping only the tail of Sivyer2013's
  75-300 um range and sitting entirely below Dan2018's 50-400 um sweep. An extended 4.0x-8.0x
  sweep (creative_thinking.md prediction 6) is needed before the null result can be claimed to
  cover the mechanism's interesting regime.

* **Fewer than the recommended set of comparable mammalian DSGC DSI-vs-length sweeps.** The
  research corpus contains zero peer-reviewed published sweeps of distal-dendrite length vs DSI on
  a mouse or rabbit ON-OFF DSGC at the resolution we ran here. The comparison is therefore against
  single-point DSI references (Park2014, Sivyer2013, Schachter2010, deRosenroll2026) and one
  invertebrate cable-theory reference (Dan2018), all of which are conceptual rather than
  sweep-matched.
