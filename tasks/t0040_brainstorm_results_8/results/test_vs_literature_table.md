# Cross-Task Test-vs-Literature Audit

This document consolidates every DSGC simulation test this project has run (through t0039) into a
master table and compares each test's quantitative outputs against published data drawn from the
`compare_literature.md` files of the contributing tasks. It is the primary audit deliverable of
brainstorm session 8 and the direct motivation for the four follow-up tasks (t0041–t0044) the
session approved.

* * *

## 1. Master Test Table

Every row is one simulation test. Columns are abbreviated so each row fits a single line per the
markdown style guide. "Pref dir" is preferred direction in degrees. "Peak" and "Null" are firing
rates in Hz. "—" means not reported.

| Task | Testbed | Swept | Range | N | Primary DSI | Vec-sum DSI | Pref dir | Peak Hz | Null Hz | Key finding |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t0008 | t0008 rotation-proxy | none | — | 240 | 0.316 | 0.366 | 0–120 | 18.1 | 9.4 | Spatial-rotation proxy understates DSI by ~0.48 vs Poleg-Polsky target |
| t0020 | t0008 gabaMOD-swap | none | — | 40 | 0.784 | — | 0 / 180 | 14.9 | 1.8 | Native gabaMOD protocol recovers DSI within 0.02 of paper target; peak remains depressed |
| t0022 | t0022 dendritic E-I | none | — | 120 | 1.000 | — | 120 | 15 | 0 | Deterministic per-dendrite 12 nS GABA pins null firing at 0 Hz |
| t0024 | t0024 AR(2) rho=0.6 | none | — | 800 | 0.776 | 0.776 | 0 | 5.15 | 0.74 | Correlation-drop signature not reproduced; DSI overshoots paper target |
| t0026 t0022 | t0022 | V_rest | -90 to -20 mV | 96 | 0.046–0.656 | — | stable 40 | 6–129 | 0 | DSI peaks at -60 mV; null stays pinned at 0 Hz |
| t0026 t0024 | t0024 | V_rest | -90 to -20 mV | 960 | 0.361–0.675 | — | unstable | 1.5–7.6 | 0.5–1.5 | U-shaped DSI profile; no firing-rate collapse |
| t0029 | t0022 | distal L x | 0.5–2.0 | 840 | 1.000 pinned | 0.643–0.664 | 120 | 14–15 | 0 | DSI pinned; Dan2018 and Sivyer2013 not falsifiable on this substrate |
| t0030 | t0022 | distal d x | 0.5–2.0 | 840 | 1.000 pinned | 0.635–0.665 | 116→84 | 13–15 | 0 | Vec-sum DSI flat p=0.177; both Schachter and passive-filtering unsupported |
| t0034 | t0024 | distal L x | 0.5–2.0 | 840 | 0.545–0.774 | 0.357–0.507 | 0 / 30 / 330 jumps | 3.4–5.7 | 0.7–1.0 | Slope -0.126 p=0.038; Dan2018 falsified on t0024 |
| t0035 | t0024 | distal d x | 0.5–2.0 | 840 | 0.680–0.808 | 0.417–0.463 | 0 stable | 4.2–5.4 | 0.5–0.8 | Flat p=0.88; cable-theory length/diameter asymmetry confirmed |
| t0036 | t0022 @ 6 nS | distal d x | 0.5–2.0 | 840 | 1.000 pinned | 0.579–0.590 | 116→59 | 13–15 | 0 | Halving GABA to 6 nS fails to unpin; rescue hypothesis falsified |
| t0037 | t0022 | null-GABA | 0, 0.5, 1, 2, 4 nS | 600 | 0.167–0.429 | 0.058–0.259 | stable at 4 nS only | 15 | 6 (at 4 nS) | Sweet spot 4 nS: DSI 0.429 matches Park2014 in vivo band |
| t0039 | t0022 @ 4 nS | distal d x | 0.5–2.0 | 840 | 0.368–0.429 | — | 37–41 stable | 13–15 | 6 | Slope -0.034 p=0.008; passive filtering, not Schachter active amplification |

* * *

## 2. Published-Data Comparison Table

Every quantitative claim from each task's `compare_literature.md` is one row. "Agreement" is MATCH /
PARTIAL / MISMATCH. "Gap" is the direction and approximate size of the discrepancy.

| Our task | Metric | Our value | Published source | Published value | Agreement | Gap |
| --- | --- | --- | --- | --- | --- | --- |
| t0008 | DSI | 0.316 | Poleg-Polsky 2016 paper median | ~0.80 | MISMATCH | -0.48 (protocol proxy) |
| t0008 | Peak Hz | 18.1 | t0004 envelope | 40–80 | MISMATCH | -22 Hz below floor |
| t0008 | Null Hz | 9.4 | t0004 envelope | <10 | MATCH | passes by 0.6 Hz |
| t0008 | HWHM deg | 82.8 | t0004 envelope | 60–90 | MATCH | in band |
| t0020 | DSI | 0.784 | Poleg-Polsky 2016 | ~0.80 | MATCH | -0.016 |
| t0020 | Peak Hz | 14.9 | t0004 envelope | 40–80 | MISMATCH | -25 Hz |
| t0022 | DSI | 1.000 | Park 2014 / Oesch 2005 | 0.65–0.85 | MISMATCH | +0.15 to +0.35 (schedule artefact) |
| t0022 | Peak Hz | 15 | Oesch 2005 | ~30–40 | MISMATCH | -15 to -25 Hz |
| t0022 | ND/PD GABA ratio | 4.0 | Park 2014 | 2–4x | MATCH | mid-range |
| t0024 | 8-dir DSI corr | 0.818 | de Rosenroll 2026 | 0.39 | MISMATCH | +0.43 overshoot |
| t0024 | 8-dir DSI uncorr | 0.835 | de Rosenroll 2026 | 0.25 | MISMATCH | +0.59 overshoot |
| t0024 | DSI drop corr to uncorr | 0.000 | de Rosenroll 2026 | 0.36 | MISMATCH | sign and magnitude fail |
| t0024 | Peak Hz | 5.15 | de Rosenroll 2026 / t0004 | ~30–40 | MISMATCH | -25 Hz |
| t0024 | HWHM deg | 68.6 | t0004 envelope | 66 | MATCH | within 3 deg |
| t0026 t0022 | DSI at -60 mV | 0.656 | Hanson 2019 / Hoshi 2011 / Sivyer 2010 | 0.33 / 0.66 / 0.45–0.50 | PARTIAL | exceeds Hanson, matches Hoshi, in Sivyer band |
| t0026 t0022 | Peak at -60 mV Hz | 15 | Oesch 2005 | 148 | MISMATCH | -133 Hz (10x gap) |
| t0026 t0024 | DSI at -60 mV | 0.446 | de Rosenroll 2026 / Hanson 2019 | 0.50 / 0.33 | PARTIAL | -0.054 below deR threshold; above Hanson |
| t0026 t0024 | Peak Hz at -30 mV | 129 | Chen 2009 | 166.4 | PARTIAL | 77% of target; requires non-physiological V_rest |
| t0029 | DSI slope vs length | 0.000 | Dan 2018 | +0.118 | MISMATCH | both Dan2018 and Sivyer2013 untestable (pinned) |
| t0030 | DSI slope vs diameter | +0.008 p=0.18 | Schachter 2010 | positive | MISMATCH | magnitude negligible |
| t0030 | DSI slope vs diameter | +0.008 p=0.18 | cable theory (Wu 2023) | negative | MISMATCH | sign opposite |
| t0034 | DSI slope vs length | -0.126 p=0.038 | Dan 2018 | +0.118 | MISMATCH | sign inverted |
| t0034 | DSI at 1.0x | 0.770 | Schachter 2010 baseline | 0.80 | MATCH | -0.030 |
| t0034 | Vec-sum DSI trend | 0.507 to 0.357 R2=0.91 | Tukker 2004 / Hausselt 2007 | cable-filter decline | PARTIAL | decline matches; no intermediate-peak optimum observed |
| t0034 | Preferred-angle jumps at 1.5x, 2.0x | 330 deg, 30 deg | Schachter 2010 | expected local-spike-failure | MATCH | fingerprint present |
| t0035 | DSI slope vs diameter | +0.004 p=0.88 | Schachter 2010 | positive | MISMATCH | no signal |
| t0035 | DSI slope vs diameter | +0.004 p=0.88 | cable theory (Z~1/d^1.5) | negative | MISMATCH | cable L/lambda asymmetry |
| t0036 | Null-GABA level | 6.0 nS | Schachter 2010 compound | 6.0 | MATCH | level matched; mechanism did not follow |
| t0036 | Primary DSI at 6 nS | 1.000 pinned | Schachter 2010 | 0.80 | MISMATCH | +0.20 overshoot; rescue failed |
| t0037 | DSI at 4 nS | 0.429 | Park 2014 / Schachter 2010 | 0.40–0.60 / ~0.50 | MATCH | in Park band; -0.07 vs Schachter |
| t0037 | Pref dir at 4 nS | 40.8 deg | Park 2014 / Hanson 2019 | polar | MATCH | axis stable |
| t0037 | DSI at 2 nS | 0.243 | Park 2014 | ~0.50 | MISMATCH | -0.26; cell over-excites |
| t0039 | DSI at 1.0x, GABA=4 | 0.429 | Park 2014 | 0.50 | MATCH | in band for first three multipliers |
| t0039 | DSI slope vs diameter | -0.034 p=0.008 | Schachter 2010 | concave-down interior peak | MISMATCH | wrong shape → passive filtering |
| t0039 | Peak Hz | 15 | Schachter 2010 / Sivyer 2013 | 40–80 | MISMATCH | -25 to -65 Hz |

* * *

## 3. Discrepancy Themes

1. **Peak firing rate is systematically 10x below published rates** across every port and every
   sweep (5–18 Hz vs 40–150 Hz in Oesch 2005, Sivyer 2013, Chen 2009). Root causes stack: lumped
   HHst lacks Nav1.6 and Kv3; NMDA is disabled in the t0022 schedule; AMPA-only drive; single-bar
   stimulus shorter than the multi-second drifting bars used experimentally.

2. **t0022's deterministic E-I schedule pins primary DSI at 1.000** for any GABA level >= 6 nS
   (t0029, t0030, t0036). Unpinning is possible only at GABA <= 4 nS (t0037, t0039), at which point
   the primary-DSI ceiling drops to 0.429 — still too tight for high-dynamic-range morphology
   sweeps.

3. **de Rosenroll correlation-drop signature not reproduced on t0024** (ours 0.000 vs paper 0.36).
   AR(2) is applied at individual Exp2Syn terminals, but the paper's effect arises from a
   spatially-distributed SAC release network with per-varicosity correlation. Our port lacks the
   connectome.

4. **Schachter 2010 active-amplification signature is absent on every diameter sweep** (t0030,
   t0035, t0039). Baseline DSI matches (0.770 vs 0.80) but the predicted concave-down interior-peak
   curvature never appears; we observe passive-filtering signatures instead.

5. **Length vs diameter asymmetry is ~25–30x** (length slope -0.126 p=0.038 on t0034; diameter
   slope +0.004 p=0.88 on t0035). Cable theory explains the asymmetry (L/lambda is linear in length
   but scales as 1/sqrt(d)). Implication: diameter is nearly a dead parameter for the t0033
   optimiser.

6. **Dan 2018 passive-TR prediction is falsified on t0024** (sign inverted, slope -0.126 vs
   predicted +0.118). No need to design further tasks around the Dan2018 hypothesis.

* * *

## 4. Correction Strategies Approved for Session 8

| # | Theme | Task created | Cost | Suggestion(s) covered |
| --- | --- | --- | --- | --- |
| C1 | Missing active channels and NMDA (theme 1, 4, 6) | t0043 | $0 local ~6 h | S-0019-03 partial, S-0018-03 partial, S-0022-02 |
| C4 | Length/diameter cable asymmetry (theme 5) | t0041 | $0 analysis ~1 h | S-0035-01 |
| C5 | GABA ceiling at 4 nS on t0022 (theme 2) | t0042 | $0 local ~1 h | new suggestion, self-covered |
| C6 | Schachter signature re-test post-C1 (theme 4) | t0044 | $0 local ~8 h | S-0002-02 |

## 5. Correction Strategies Deferred

| # | Theme | Why deferred |
| --- | --- | --- |
| C2 | Poisson background release on t0022 | Held behind C1 and C6; if t0044 shows Schachter recovery, this becomes secondary |
| C3 | SAC network port on t0024 | Needs dsMicro-GH access; high effort (~14 h) and Vast.ai cost; not immediately necessary |
| C7 | BIP burst-rate calibration | Held behind C1 diagnosis of peak-rate cause |
| Sheffield paper retrieval (Kim 2014, Sivyer 2013) | Researcher explicitly deferred this wave |  |

## 6. Published Sources Cited in This Audit

Poleg-Polsky & Diamond 2016, de Rosenroll et al. 2026, Park 2014, Schachter et al. 2010, Oesch et
al. 2005, Sivyer et al. 2010, Sivyer et al. 2013, Taylor et al. 2002, Hausselt et al. 2007, Tukker
et al. 2004, Dan et al. 2018, Barlow & Levick 1965, Chen et al. 2009, Hanson et al. 2019, Hoshi et
al. 2011, Wu et al. 2023, Poleg-Polsky 2026.

Full per-source summaries live in each task's `results/compare_literature.md`.
