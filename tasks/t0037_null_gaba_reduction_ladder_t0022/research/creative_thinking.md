# Creative Thinking: Interpreting the 4-nS Sweet Spot

## Objective

The GABA ladder produced a non-obvious result: null firing unpins at ALL tested levels (including 4
nS which was only 2 nS below t0036's failed 6 nS), yet DSI collapses at low GABA because preferred
direction randomises. This document enumerates what the 4 nS sweet spot reveals about the t0022
schedule and what follow-up experiments are highest leverage.

## Alternatives Considered

1. **The 6→4 nS transition is a hard threshold** — between 6 nS and 4 nS, null-direction membrane
   crosses Nav activation. Below 4 nS, null firing is guaranteed regardless of direction-specific
   modulation, which dilutes DSI. **Test**: fill in GABA = {4.5, 5.0, 5.5} nS to locate the
   transition precisely.

2. **Excess excitation at low GABA overwhelms directional asymmetry** — at ≤2 nS, both preferred and
   null directions reach ~20 Hz because the spatially-asymmetric E-I schedule loses its ability to
   differentiate when inhibition is too weak. The schedule needs SOME GABA to express DSGC
   directional selectivity. 4 nS is the minimum functional inhibition.

3. **4 nS corresponds to Schachter2010's compound GABA estimate** — originally considered "too weak"
   in t0036's compare_literature (6 nS was the target because 12 nS was estimated as 2×). Actually 6
   nS matches the AVERAGE, but 4 nS matches the LOW END of Schachter2010's range. The t0022
   testbed's E-I timing is sufficiently aggressive that the low-end value is the right match.

4. **Preferred-direction drift at low GABA is informative** — at 0 nS GABA, preferred direction is
   278° (anti-preferred!). This suggests the baseline E-I schedule's "null" direction actually has
   more spatial overlap with the preferred AMPA arrival pattern once inhibition is removed. The 10
   ms GABA lead was shaping the apparent null.

5. **DSI=0.429 at 4 nS matches Park2014 in vivo DSGC range (0.4-0.6)** — the sweet spot is
   biologically realistic. A follow-up diameter sweep at 4 nS should produce DSI values in the same
   range, not pinned at 1.0 or collapsed at 0.2.

6. **Vector-sum DSI tracks primary DSI at the sweet spot** — at 4 nS, vector-sum (0.259) is ~60% of
   primary DSI (0.429), consistent with the smoothing expected from non-zero null firing. This is
   the first testbed configuration where both metrics agree on the DSGC regime.

7. **The ladder inadvertently reveals the E-I schedule's operational range** — 4 nS is the ONLY GABA
   value in the tested range that simultaneously: (a) unpins null firing above the noise threshold,
   (b) preserves preferred-direction selectivity, (c) produces DSI in the biological range, (d)
   maintains preferred direction near the expected 40-50°.

## Recommendation

**Highest-leverage follow-up**: rerun t0030's 7-diameter sweep at GABA=4 nS (not 6 nS). This is the
first time primary DSI should be measurable across the diameter axis. Expected outcome: either
Schachter2010 (positive slope) or passive filtering (negative slope) should be detectable with
p<0.05. Cost: ~30 min local CPU. This becomes the definitive Schachter-vs-passive discriminator that
t0030, t0036 both failed to produce.

**Second-highest-leverage**: fill-in sweep at GABA ∈ {4.5, 5.0, 5.5} nS to precisely locate the
unpinning threshold and characterise the transition sharpness.

## Limitations

* The 4 nS result is at baseline diameter only — we don't know if the sweet spot shifts with distal
  morphology.
* 10 trials per angle may be insufficient at low GABA where firing is highly variable (peak 20-23 Hz
  range). Higher trial counts (30+) at 0-2 nS levels would clarify the regime.
* Schachter2010's compound null inhibition range wasn't precisely matched; the ladder brackets the
  rough "around 4 nS" target.
* The observed preferred direction drift at low GABA wasn't captured in voltage-trace detail; would
  need per-section membrane recordings to disambiguate.
