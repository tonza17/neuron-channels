---
spec_version: "1"
task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
---
# Creative Thinking: Interpreting a Passive Filtering Signature at 4 nS

## Context

The sweep delivered a clean, statistically significant result: DSI decreases monotonically with
distal dendrite diameter (slope=-0.0336 per log2(multiplier), p=0.008). On the
Schachter2010-vs-passive classifier thresholds inherited from t0030, this is labelled
**passive_filtering**: thicker distal dendrites → lower input resistance → stronger soma-ward
current sink at the pref-direction E-I pairs → weaker DSI. Thinner dendrites invert the pattern
and produce higher DSI.

This is the first time t0022 has produced a discriminator with dynamic range, and the answer came
out clean. That's worth thinking about carefully.

## Hypotheses and Alternative Interpretations

### 1. The pref_direction stays pinned near 40° across the full diameter range (37-41°)

The preferred direction does NOT randomise as diameter changes — it hovers within 4° of the t0037
baseline value (40.8°). This means the mechanism behind direction selectivity is robust to diameter
manipulation within [0.5x, 2.0x]. What changes is the **gain** of the discriminator (DSI magnitude),
not its **axis** (pref direction).

**Implication**: t0022's DS is encoded in the E-I arrival-time schedule, not in morphology. The
morphology just attenuates or amplifies the differential soma depolarization.

### 2. Schachter2010 active amplification should live in a specific diameter regime

Schachter2010 predicts active dendritic calcium/sodium spikes that preferentially boost
pref-direction responses at intermediate diameters. If t0022 had channels sufficient for this
mechanism, we should see DSI peaking at an intermediate multiplier (concave-down).

Instead, DSI is maximal at the thinnest tested diameter (0.5x) and falls monotonically. This
suggests t0022's distal dendrites **lack the active amplification machinery** — either the channel
densities are too low, or the local Ra/Cm balance doesn't support regenerative events.

**Implication**: If the project wants to test the active-amplification hypothesis, t0022 is the
wrong testbed; t0024 (de_rosenroll_2026_dsgc with richer channel inventory) is the likely candidate.

### 3. DSI saturation at the thin end (0.5x and 0.75x both = 0.429)

The two thinnest points hit the ceiling at exactly 0.429 — the same value as t0037's 4 nS sweet
spot. This is not coincidence: at 4 nS GABA, t0022's discriminator ceiling is set by the stimulus
schedule, not by morphology. Making dendrites even thinner won't raise DSI further.

**Implication**: Any morphological optimisation at 4 nS GABA on t0022 will produce diminishing
returns below D≈0.5x. A more informative sweep would bracket D ∈ [0.75, 3.0] to catch both the
plateau and the decay.

### 4. Peak firing rate decreases with diameter (15 → 13 Hz)

Peak firing also drops as diameter increases (15 Hz at 0.5-1.0x → 13 Hz at 1.75-2.0x). This
co-tracks the DSI decrease: both soma-ward current-sink losses and pref-direction excitation
attenuate with larger dendrites. The effect is small (~2 Hz) but directionally consistent.

**Alternative**: the 2 Hz peak drop could also reflect more spike-failures at 2.0x than at 0.5x
(more charge leaking into the thick dendrite before the soma reaches threshold). The per-trial
spike-count distribution would distinguish these; worth checking.

### 5. Null firing is invariant across the sweep (6 Hz at every diameter)

This is the cleanest signal in the dataset. Null firing doesn't move — the inhibitory schedule
dominates the null direction regardless of diameter. The 6 Hz baseline is set entirely by the 4 nS
GABA level and the stimulus timing.

**Implication**: Any future intervention aimed at raising null firing (e.g., further reducing GABA)
will be orthogonal to diameter — they can be swept independently.

### 6. The t0037 operational window (~4-5 nS) interacts with morphology

At 6 nS (t0036), DSI was pinned. At 4 nS (t0037 baseline D=1.0), DSI=0.429. On t0039, thinning to
D=0.5x gives the same 0.429 — not higher. This suggests the GABA-morphology interaction is
**multiplicative, not additive**: the morphology can't rescue more DSI than the GABA level permits.

**Implication**: The right way to look for Schachter2010 amplification is probably a joint sweep of
(GABA, diameter) with GABA ladder below 4 nS and diameter below 0.5x, where the ceiling lifts.

## Recommended Follow-ups

1. **Rerun the same sweep on t0024** to test whether the richer channel inventory produces a
   Schachter2010 (concave-down) signature. Direct apples-to-apples test.
2. **Fine-grained sweep D ∈ {0.3, 0.4, 0.5, 0.6, 0.7} at GABA=4** to locate the DSI plateau edge.
3. **Joint (GABA, D) sweep** with GABA ∈ {5, 4.5, 4, 3.5, 3} and D ∈ {0.5, 1.0, 2.0} to test the
   multiplicative-ceiling hypothesis.
4. **Diagnose the 15 Hz peak-firing cap** — it blocks quantitative comparison to Schachter2010's
   40-80 Hz. Likely an AMPA-only drive issue (carried from t0030).

## Most Interesting Follow-up

**Run the same 7-diameter sweep on t0024 at its equivalent operational GABA level.** This is the
definitive test of whether t0022 lacks active amplification or whether the whole 4 nS regime is
inherently passive. If t0024 shows a concave-down pattern and t0022 doesn't, we have a clean
testbed-level discrimination between the two mechanisms — and t0024 becomes the preferred
substrate for the t0033 Vast.ai optimisation.
