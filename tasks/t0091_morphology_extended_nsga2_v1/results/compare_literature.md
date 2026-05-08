---
spec_version: "1"
task_id: "t0091_morphology_extended_nsga2_v1"
date_compared: "2026-05-08"
---
# Compare Literature -- t0091_morphology_extended_nsga2_v1

## Summary

Compared the 57-cell Pareto front from the joint 68-d NSGA-II (54-d v3 electrophys + 14-d
morphology) against published DSGC firing rates, channel-density priors, dendritic-asymmetry
findings, and multi-objective optimisation precedents. The headline finding is that the
morphology-extended optimiser **cannot rescue biological plausibility**: 0/57 Pareto cells pass the
13-prior worst-case scorecard, and the single strict joint-pass cell reaches **35.1 Hz PD** (vs
[Trenholm2013] **198 Hz** measured peak; delta **-162.9 Hz**). The PD vs ND asymmetric anchor counts
**12 vs 9** are far below the [Briggman2011] **12.8x** structural-asymmetry effect-size threshold (p
= 0.331; ratio **1.33x**), so the soma-displacement-toward-PD prediction from
[Schachter2010, Briggman2011, Trenholm2013] is not confirmed at gen 2. A length-vs-DSI Spearman
**rho = -0.07** directly refutes the [Hausselt2007] monotonic length-DSI scaling under joint
optimisation.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Trenholm2013, Fig 1B / Table 1] (mouse Hb9+ DSGC) | Peak PD firing rate (Hz, control) | 198 | 35.1 | -162.9 | Best of 57 Pareto cells; wide-field bar stimulus in published vs 16-direction synthetic stimulus here |
| [Trenholm2013, Fig 1B / Table 1] (mouse Hb9+ DSGC) | Peak ND firing rate (Hz, control) | 27 | 0 | -27 | Best joint-pass cell has near-zero null firing; published cell shows residual null firing |
| [Trenholm2013, Fig 1B] (peak PD/ND ratio) | PD:ND firing ratio | 7.33 | inf | n/a | Our best cell has ND ~= 0 Hz which mechanically gives DSI 1 with low absolute spike count (artefact pattern from t0093) |
| [Briggman2011, Fig 4 / p. 184] (SAC-DSGC structural asymmetry) | Null:preferred soma-side synapse ratio | 12.8 | 1.33 | -11.47 | Pareto-anchor count 12 PD-asym vs 9 ND-asym; functional rather than structural; t0091 ratio is 0.087x of published structural ratio |
| [Briggman2011, p. 184] structural asymmetry threshold | One-sided permutation p-value | < 0.001 (implied) | 0.331 | n/a | Our test is on Pareto-anchor counts not synapse counts; not significant at alpha = 0.05 |
| [Schachter2010, Fig 2C / p. 4] PSP-vs-spike DSI amplification | Spike DSI / PSP DSI ratio | 4.0 | n/a | n/a | Our DSI is computed at firing-rate level (vector-sum across 16 directions); PSP-level DSI not measured per cell here |
| [Schachter2010, p. 5] dendritic Na density baseline | Dendritic gNa (mS/cm^2) | 40 | varies (per cell) | n/a | Pareto cells exceed Schachter baseline; biological scorecard NaP prior flagged exotic on all 57 cells |
| [Sivyer2013, Fig 2 / p. 1612] NMDA per-spine conductance | Per-spine NMDA gmax (nS) | 0.1 | up to ~10 (1e-2 uS bound) | +9.9 | Plan upper bound 1e-2 uS implies up to 100x [Sivyer2013] per-spine prior; bound not lowered in t0091; flagged exotic on Pareto cells |
| [Hausselt2007, Fig 4 / p. 8] dendritic-length-vs-DSI scaling | Spearman rho (length vs DSI) | positive monotonic (DSI 0.35 at 150 um vs 0.12 at 50 um) | -0.07 | n/a | Not confirmed; length and DSI are independent in joint Pareto under our 16-direction stimulus protocol |
| [Tukker2004, Fig 8] artificial-morphology DSI amplification | DSI uplift from distal-branch concentration | up to 2x | n/a | n/a | Our optimiser does not stratify by distal-branch concentration; alt_topology anchor (Pareto count 16, mean DSI 0.263) carries the analogous mechanism |
| [Ezra-Tsur2021, Fig 3 / Table 1] NSGA-II Pareto-population size | Pareto cells found | 100s (multi-seed pop 100 x 20-45 gens, d=8) | 57 | n/a | Their d=8 vs our d=68; we ran 2 of 8 planned generations; REQ-10 threshold of 8 cells exceeded 7x |
| [Hay2011, Fig 1 / Table 2] multi-objective biophysical pop size | Pareto-family size | hundreds | 57 | n/a | Their pop 1000+, d~30; ours pop 96, d=68. Direct size comparison non-comparable; Hay's family-of-models pattern reproduced |
| [Schachter2010, Fig 6 / p. 7] soma-displacement toward PD | Functional PD-asymmetry direction effect | yes (intrinsic-DS opposes desired tuning at preferred side, DSI -0.1 to -0.2) | counts 12 vs 9 (p=0.331) | n/a | Refuted at gen 2: optimiser direction-blind |
| [Trenholm2013, p. 5] DSGC ceiling under disinhibition (picrotoxin) | Peak PD firing rate (Hz) | 244 | 35.1 (max in 57-cell Pareto) | -208.9 | Peak ceiling 244 Hz; bio scorecard flags >250 Hz hyperbolic; our cells nowhere near ceiling |

### Prior Task Comparison

The t0091 plan cites two prior project tasks as direct baselines:

* **[t0083] 54-d electrophys-only NSGA-II Pareto**: t0086/t0088 evaluated the t0083 Pareto's joint-
  pass cells against 9 priors. Result: all flagged exotic (NMDA +85 to +116 sigma, distal NaP +9 to
  +34 sigma, GABA spatial-gradient violations). **t0091's morphology-extended 68-d Pareto reproduces
  the same outcome**: 0 of 57 cells biologically plausible. The morphology axis does not raise the
  ceiling.

* **[t0093] patched-generator validation under fixed t0083 channels**: 21 of 60 LHS morphologies
  achieved DSI > 0.5 with the single best-cell electrophys vector (no optimisation). t0091's joint-
  search finds **1 of 57 strict joint-pass** at (DSI 0.51, PD 35 Hz, robust 0.79). The optimiser
  does locate higher-quality individual cells than random sampling, but at the cost of all 57 Pareto
  cells violating biological priors -- consistent with the "ceiling not raised by morphology"
  conclusion.

* **[t0086, k=2 clustering]** found NMDA at +85 / +122 sigma above [Sivyer2013];
  **[t0088, k=4 clustering]** found NMDA +86 to +116 sigma. **t0091's biological scorecard
  confirms** all 57 Pareto cells violate the NMDA per-spine prior at upper-bound saturation (1e-2
  uS, ~100x [Sivyer2013]). The contradiction with prior-task hopes (that morphology would shift the
  centroid toward [Sivyer2013]) is a finding: the bound was not narrowed in t0091, and the optimiser
  remains pinned at the upper rail.

## Methodology Differences

* **Stimulus protocol (vs [Trenholm2013])**: published peak firing rates use a 600 um/s wide-field
  bar at preferred / null directions; our protocol uses 16-direction synthetic bar rotation with
  vector-sum DSI. Peak rates measured under different temporal kinetics; our 35.1 Hz is the per-cell
  PD-rate at the preferred direction averaged over 5 seeds, not a peak instantaneous rate.

* **Asymmetry test (vs [Briggman2011])**: published 12.8:1 ratio is over 565 SAC-to-DSGC synapses
  (524 null-side soma vs 41 preferred-side soma); our 12 vs 9 ratio is over 21 Pareto-anchor cells
  drawn from 57 total. Sample size, unit of analysis (synapses vs cells), and null model (random vs
  uniform anchor distribution) all differ.

* **DSI metric (vs [Schachter2010])**: published 4x amplification is PSP DSI vs spike DSI on the
  same cell; we report only spike-level DSI vector-sum, so the PSP-vs-spike amplification cannot be
  measured per Pareto cell.

* **Channel-density baselines (vs [Schachter2010, Sivyer2013])**: their values come from rabbit DSGC
  (Schachter) and rabbit DSGC dendritic patch (Sivyer); our v3 substrate inherits cortical-
  pyramidal NaP priors (Stuart 1999) and applies them to mouse-DSGC simulations. Cross-species and
  cross-cell-type prior application is documented in the scorecard (and inherited unchanged from
  t0086 / t0088).

* **Length-vs-DSI test (vs [Hausselt2007])**: their length sweep was 50-200 um *with fixed
  electrophys*; our test is across the joint 14-d morphology + 54-d electrophys Pareto. Joint
  optimisation lets electrophys compensate for any morphology; this can mask the length-DSI
  relationship that fixed-channel sweeps reveal.

* **NSGA-II population scale (vs [Ezra-Tsur2021], [Hay2011])**: theirs were pop 100 x 20-45 gens at
  d=8 ([Ezra-Tsur2021]) or pop 1000+ at d~30 ([Hay2011]); ours is pop 96 x 2 gens at d=68. Our
  Pareto is partially-converged (HV +68% gen 1 to gen 2, plateau not reached).

* **Anchor design (novel, vs [Briggman2011])**: t0091's PD-asymmetric vs ND-asymmetric anchors apply
  structural asymmetry to *DSGC* morphology; [Briggman2011]'s 12.8:1 ratio describes *SAC* dendrite
  orientation. The mirror-pair test is a project-novel construct and has no direct experimental
  analogue in DSGC literature.

* **MOBO algorithm choice (vs [Ament2023])**: GP-based qLogNEHVI was tested in t0078 at d=40+ and
  hit O(N^3) scaling cost. t0091's NSGA-II via pymoo avoids this scaling, consistent with the
  project memo standing default for d > 40.

## Analysis

The optimiser's behaviour is consistent with [Hay2011]'s Pareto-as-family pattern but with the
ceiling-not-raised limitation predicted by t0086's NMDA + NaP prior violations. Three findings are
most informative:

1. **Direction-blind morphology selection**: counts 12 vs 9 (p=0.331), 0.087x of [Briggman2011]'s
   12.8x structural ratio. The substrate prefers asymmetric over symmetric morphology (symmetric
   anchor count = 0 of 57 Pareto cells) but is indifferent to asymmetry polarity. This refutes the
   [Schachter2010, Briggman2011, Trenholm2013] soma-displacement-toward-PD prediction at the current
   generation depth. Possible explanations: (a) gen 2 is too early to converge on the
   biologically-correct asymmetry; (b) the symmetric-direction 16-direction stimulus grid washes out
   direction-specific selection because vector-sum DSI is direction-blind; (c) the anchor
   construction does not capture the SAC dendrite-orientation feature that [Briggman2011] identifies
   as the wiring unit.

2. **Length-DSI decoupling**: rho = -0.07 directly contradicts [Hausselt2007]'s monotonic positive
   relationship. Under joint optimisation, electrophys compensates: any cell with short dendrites
   can recover DSI by raising channel densities, and any cell with long dendrites can saturate
   firing without DS. This explains why the [Hausselt2007] mechanism is unobservable in the joint
   Pareto -- it is a fixed-electrophys-only finding.

3. **Universal channel-side prior violation**: all 57 Pareto cells flag exotic on at least one of 13
   priors (NaP, NMDA per-spine, GABA spatial gradient prominently). Morphology priors mostly pass
   (soma-offset, field-elongation, AIS-length bounds), but the optimiser cannot reduce channel-side
   prior violations by varying morphology alone. This is the "acceptable negative" outcome predicted
   in the plan: morphology cannot rescue biological plausibility because the prior violations are
   channel-density, not geometry.

The single strict joint-pass cell (DSI 0.511, PD 35.1 Hz, robust 0.79; nearest anchor alt_topology)
is **162.9 Hz below** [Trenholm2013]'s 198 Hz preferred-direction peak. Even the best cell does not
approach the published biological target; this informs the project that joint search at d=68 within
the current parameter bounds cannot recover physiological firing rates and DSI simultaneously.

The agreement with [Hay2011]'s family-of-models philosophy is reproduced (57-cell Pareto exceeds the
REQ-10 threshold by 7x), and the [Ezra-Tsur2021] necessity-vs-modulator framing applies: asymmetric
morphology is **necessary** (symmetric count = 0), but asymmetry direction is **modulatory** (PD vs
ND counts not significantly different).

## Limitations

* **Only 2 of 8 planned generations completed**. The HV trajectory (+68% gen 1 to gen 2) was still
  climbing; cannot rule out gen 3+ producing a biologically-plausible cell. Mitigation: universal
  channel-side prior violation across all 57 cells suggests the negative finding is robust to
  generation depth, since prior violations are channel-side and morphology cannot fix them.

* **[Sivyer2013] PDF was paywalled in the project corpus**; the per-spine NMDA prior of 0.1 nS used
  in the scorecard comes from metadata-only access plus cross-confirmation with [Sethuramanujam2017]
  (also paywalled). The +85 to +116 sigma exotic-ness inherited from t0086/t0088 reflects this
  baseline; an RGC-specific dendritic-NMDA measurement could shift the prior.

* **No DSGC-specific NaP density measurement exists** ([MullerEgorov2024] confirms this). Our
  scorecard inherits [Stuart1999] cortical-pyramidal NaP prior (sub-1% of Nav at distal sites). The
  +9 to +34 sigma exotic-ness vs cortical prior may be smaller against an RGC-specific prior, but no
  such prior is published.

* **PSP-level DSI not measured per Pareto cell**, so [Schachter2010]'s 4x PSP-vs-spike amplification
  cannot be confirmed or refuted on our optimised cells. The published mechanism predicts our spike
  DSI = 0.51 corresponds to PSP DSI ~0.13, but this is not directly tested.

* **[Briggman2011] structural ratio is over SAC dendrites, not DSGC dendrites**. The mirror-anchor
  test we ran (PD-asym vs ND-asym DSGC morphology) is project-novel and not directly anchored to
  experimental data; the negative outcome (p = 0.331) does not necessarily refute the [Briggman2011]
  structural finding, only its DSGC-morphology analogue.

* **Comparison priors inherited from t0086 / t0088** unchanged. Cross-species (rabbit Schachter,
  rabbit Sivyer, mouse Briggman, cat Anderson) prior application is documented and accepted as a
  project caveat; an RGC-specific prior update (S-0086-05 follow-up) is open.

* **[Anderson1999] cable-theoretic v_opt = 2 lambda / tau_m sanity check** was logged per cell in
  the predictions JSONL but is not summarised here in this comparison table; that analysis is
  deferred to a follow-up Pareto-cell deep-dive task.

* **[Roy2024JNeurosci, Ankri2024JPhysiol, Riccitelli2025] are scotopic / surround / extraclassical
  regimes not modelled by our photopic 16-direction protocol**. These newly-added papers (in the
  t0091 corpus from research-internet) bound the comparison: our Pareto represents a single
  classical-RF photopic operating point, not the full DSGC adaptive repertoire.

## References

* **[Trenholm2013]**: Hb9+ DSGC peak preferred 198 Hz / null 27 Hz under control; 244 / 202 Hz under
  picrotoxin (Fig 1B / Table 1). DOI: `10.1523/JNEUROSCI.0808-13.2013`.
* **[Briggman2011]**: SAC-to-DSGC structural asymmetry 12.8:1 (524 vs 41 synapses; p. 184). DOI:
  `10.1038/nature09818`.
* **[Schachter2010]**: PSP DSI ~0.2 vs spike DSI ~0.8 (4x amplification, Fig 2C); intrinsic-DS
  opposing network-DS effect (Fig 6). DOI: `10.1371/journal.pcbi.1000899`.
* **[Sivyer2013]**: Per-spine NMDA gmax ~0.1 nS prior (Fig 2). DOI: `10.1038/nn.3565`.
* **[Hausselt2007]**: Dendritic-length-vs-DSI monotonic scaling (DSI 0.35 at 150 um vs 0.12 at 50
  um, Fig 4). DOI: `10.1371/journal.pbio.0050185`.
* **[Tukker2004]**: Distal-branch-density and length-asymmetry up to 3x DSI uplift (Fig 8). DOI:
  `10.1017/S0952523804214109`.
* **[Hay2011]**: Multi-objective NSGA-II precedent for compartmental neuroscience (Fig 1 / Table 2).
  DOI: `10.1371/journal.pcbi.1002107`.
* **[Ezra-Tsur2021]**: NSGA-II / IBEA on d=8 SAC parameter space (Fig 3 / Table 1). DOI:
  `10.1371/journal.pcbi.1009754`.
* **[Cuntz2010]**: Procedural-morphology generator framework (TREES toolbox). DOI:
  `10.1371/journal.pcbi.1000877`.
* **[Anderson1999]**: Cortical V1 dendritic-asymmetry-DS negative control (KS p=0.23). DOI:
  `10.1038/12194`.
* **[Ament2023]**: LogEI / qLogNEHVI methodology and GP-BO scaling pathology (Theorem 1). Citation:
  `no-doi_Ament2023_logei-bo`.
* **[MullerEgorov2024]**: NaP review confirming no DSGC-specific NaP measurement exists. DOI:
  `10.1007/s00424-024-02980-7`.
* **[Sethuramanujam2017]**: Silent-NMDA mechanism in adult mouse DSGC. DOI:
  `10.1016/j.neuron.2017.09.058`.
* **[t0083]**: 54-d electrophys-only NSGA-II Pareto (project task, prior baseline).
* **[t0086, t0088]**: Biological-priors scorecard with 9 priors; +85 to +122 sigma NMDA, +9 to +34
  sigma NaP exotic verdicts on t0083 Pareto cells (project tasks, prior baseline).
* **[t0093]**: Patched-generator re-sweep showing 21/60 LHS cells with DSI > 0.5 under fixed t0083
  channels (project task, prior baseline).
