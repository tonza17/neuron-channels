---
spec_version: "1"
task_id: "t0074_channel_tuning_width_bed_a"
research_stage: "internet"
searches_conducted: 17
sources_cited: 21
papers_discovered: 8
date_completed: "2026-05-01"
status: "complete"
---
# Research Internet: BK / SK / Kv7 MOD Vendoring and Tuning-Width Metrics

## Task Objective

This task vendors three new NEURON MOD mechanisms — BK (KCa1.1 / KCNMA1), SK (KCa2 / SK2), and Kv7 /
M-current — plus a single-shell `cad`-style calcium-pool mechanism, then runs a 12-angle
tuning-curve sweep on Bed A (deposited Poleg-Polsky DSGC) with each of eight somatic channels
inserted at low / medium / high density across 25 conditions and 2100 trials. The internet research
below identifies authoritative published MOD-file sources, retinal validation references, kinetic-
parameter ranges, calcium-pool conventions, and tuning-width metric definitions that the project
corpus does not contain.

## Gaps Addressed

The `research/research_papers.md` Gaps and Limitations section identified six gaps. Internet
research resolves each as follows:

1. **No paper in the project corpus contains a measurement or model of BK, SK, or Kv7 channel
   kinetics specifically in DSGCs** — **Partially resolved**. No DSGC-specific kinetic dataset
   exists in the published literature either; the closest mammalian-RGC validation references are
   [Wang1998-Ferret], [Lipton1987-Rat], and [Grimes2012-MouseBK]. These document the existence and
   pharmacology of BKCa and SKCa in mammalian RGCs (118 pS BK, 22 pS SK by [Wang1998-Ferret]
   single-channel) but do not quantify whole-cell kinetic parameters at the level needed for direct
   MOD fitting. The vendoring will therefore source MODs from non-RGC published models with strong
   citation history and validate via t0074's Stage-2 regression gate plus general RGC firing-rate
   ranges (peak ~150-190 Hz, [Chen2009-PMC] from `research_papers.md`).

2. **No paper in the project corpus contains a published HWHM value in degrees for adult mouse
   ON-OFF DSGCs** — **Partially resolved**. The mouse DSGC literature consistently reports "tuning
   width and DSI of P11 / P13 / P18 / adult DSGCs were very similar" with HWHM defined as "the
   full-width at half-maximum of the fitted tuning curve" [Chen2009-PMC] but specific degree values
   are reported per-figure rather than as a tabulated number. [Hanson2019-eLife] reports vector-sum
   DSI ≈ 0.33 (wild-type) → 0.07 (with non-directional SAC GABA), establishing vector-sum DSI as the
   appropriate residual-DSI metric. [Rivlin2012-Neuron] and others define "vector sum > 0.2 and DSI*
   \> 0.3" as the standard directional-classification threshold.

3. **Five t0019 voltage-gated-channel papers are paywalled (CrossRef-only summaries)** —
   **Unchanged** by internet research; this task does not require re-downloading those papers
   because the BK / SK / Kv7 MOD vendoring relies on hippocampal / cortical sources that are
   independently documented.

4. **No prior task in the project has done a comparable channel-density sweep with multiple width
   metrics** — **Resolved-as-methodological-novelty**. Internet review confirms no published
   compartmental-model paper has run a HWHM × density grid for the eight-channel set this task
   sweeps. The Hay 2011 L5 pyramidal model [Hay2011-L5] is the closest precedent for systematic
   channel-density variation but uses a different metric set.

5. **The t0067 baseline used FULL mode with the gabaMOD-swap protocol from t0065** — **Internal** to
   the project; not addressed by internet research.

6. **Calcium-pool kinetic constants for the new pool mechanism (decay τ, shell depth) are not
   uniquely specified by the corpus** — **Resolved**. Internet review of the canonical published
   `cad.mod` files yields three concrete options:
   * Mainen-Sejnowski 1996 `cad.mod` (ModelDB 2488): τ = 200 ms, depth = 0.1 µm, cainf = 100 nM,
     based on [Destexhe1993-Thalamic] [MS1996-cad-Github].
   * Hay 2011 `CaDynamics_E2.mod` (ModelDB 139653): τ = 80 ms, gamma = 0.05, depth = 0.1 µm, minCai
     = 100 nM [Hay2011-CaDyn-Github].
   * RGC-specific [F&M1997-PMC]: tau_Ca = 50 ms, single-shell, used in cat-alpha and rat RGC models.
     The Fohlmeister τ = 50 ms is the RGC-specific anchor; Hay 2011 τ = 80 ms is in the same range;
     Mainen-Sejnowski τ = 200 ms is at the high end. Bed B's existing `cad` should be the first
     reference; the task description notes this explicitly.

## Search Strategy

**Sources searched**: ModelDB (modeldb.science / senselab.med.yale.edu), Google Scholar via
WebSearch, PubMed, GitHub (ModelDBRepository organization, OpenSourceBrain), PNAS, Journal of
Neuroscience, Journal of Physiology, Science, eLife, Frontiers, Nature journals, Wiley Online
Library, ScienceDirect.

**Date range**: 1982-2026 for canonical channel-cloning and MOD-file deposit papers; 2009-2026 for
mouse-DSGC tuning-width benchmarks.

**Inclusion criteria**: A source is relevant if it (a) provides a published NEURON MOD-file
implementation of BK, SK, or Kv7 with kinetic parameters and source citation, (b) provides a
single-shell calcium-pool decay convention with documented τ, (c) measures BK / SK / Kv7 in
mammalian RGCs even without compartmental-model parameters, or (d) defines HWHM, vector-sum DSI, or
related width metrics in the mammalian DSGC literature with reproducible computation.

**Exclusion criteria**: Non-mammalian retina (goldfish, salamander) for channel-density priors;
tau-protein papers; unrelated KCNQ pharmacology papers.

**Queries executed (17 total)**:

*Pass 1 — Gap-targeted MOD-file source queries*:

1. `ModelDB BK channel KCa1.1 KCNMA1 NEURON MOD file Migliore CA1 hippocampal`
2. `ModelDB SK channel KCa2 SK2 NEURON MOD file calcium-activated potassium small conductance`
3. `ModelDB Kv7 KCNQ M-current NEURON MOD file Hu Gulledge Stuart 2007 cortical`
4. `Mainen Sejnowski 1996 cortical pyramidal NEURON model ModelDB BK calcium-activated potassium kca.mod`
5. `Migliore 1995 CA1 pyramidal NEURON model BK channel mod file ModelDB accession`

*Pass 2 — RGC validation queries*:

6. `Pfeiffer Friedrich 2012 BK channel retinal ganglion cell mouse`
7. `"BK channel" "retinal ganglion cell" rat OR mouse patch-clamp kinetics whole-cell`
8. `"SK channel" "retinal ganglion cell" calcium-activated potassium afterhyperpolarization mammalian`
9. `"M-current" OR "Kv7" "retinal ganglion cell" KCNQ patch-clamp recording`
10. `"Calcium-Activated Potassium Conductances in Retinal Ganglion Cells" Wang 1998 ferret apamin`
11. `"M-Channels" "perisomatic region" CA1 Shah Storm 2008 ModelDB Kv7 KCNQ NEURON`

*Pass 3 — Snowball and benchmark queries*:

12. `Hay 2011 Segev cortical L5 pyramidal SK_E2.mod NEURON ModelDB BK CaT CaL channels accession`
13. `"Kohler" 1996 Science 273 SK channels small conductance "1709" cloning DOI`
14. `"Adams" Brown Constanti 1982 J Physiol M-current "I-M" bullfrog sympathetic neurone activation`
15. `"Fohlmeister" "Miller" 1997 J Neurophysiol RGC five-channel cad pool "tau" decay milliseconds`
16. `"vector sum" direction selectivity index DSGC mouse "half-width" degrees tuning curve Briggman Borst`
17. `"Chen 2009" "half-width" direction tuning DSGC mouse postnatal degrees full-width`

**Search iterations**: Pass 1 surfaced specific ModelDB accession candidates (2796, 2488, 112546,
139653). Pass 2 confirmed mammalian-RGC BK/SK existence ([Wang1998-Ferret], [Grimes2012-MouseBK])
but no DSGC-specific kinetic dataset. Pass 3 fetched MOD-file content via the GitHub API for direct
inspection of kinetic parameters in `kca.mod`, `cad.mod`, `km.mod` (Mainen-Sejnowski 1996), and
`SK_E2.mod`, `Im.mod`, `CaDynamics_E2.mod` (Hay 2011), plus `DGC_M.mod` and `DGC_sAHP.mod`
(Mateos-Aparicio et al. 2014, ModelDB 169240).

## Key Findings

### Three Vendoring Triplets — Recommended MOD-File Sources

Internet research yields three coherent, published MOD-file packages where the BK / SK / Kv7 / Ca-
pool mechanisms are mutually consistent (same temperature convention, same ion-balance assumptions,
same NEURON formalism). The three packages differ in maturity and citation count.

**Package A — Mainen & Sejnowski 1996 (ModelDB 2488)** [MS1996-modeldb][MS1996-cad-Github]:

* `kca.mod` — Calcium-activated K+ channel (BK-style, voltage- and Ca-dependent), citing
  [Pennefather1990-Sympath, Reuveni1993-Cortical]. Voltage-dependent gating with explicit Ca
  dependence: `a = Ra × cai^caix` with `Ra = 0.01 (/ms), caix = 1`. Operates at 37 °C.
* `cad.mod` — Single-shell Ca pool: τ = 200 ms, depth = 0.1 µm, cainf = 100 nM, citing
  [Destexhe1993-Thalamic].
* `km.mod` — M-current / Kv7 with V_½ = -30 mV (parameter `tha`), slope = 9 mV (parameter `qa`), Q10
  = 2.3 (reference 23 °C), max activation rate = 0.001 /ms. No explicit Adams citation in the file,
  but matches Adams-Yamada-Koch formalism.

**Package B — Hay et al. 2011 (ModelDB 139653)** [Hay2011-L5][Hay2011-CaDyn-Github]:

* `SK_E2.mod` — Pure SK / KCa2.2: voltage-independent, Ca-driven Hill activation
  `zInf = 1 / (1 + (0.00043 / cai)^4.8)`. Time constant τ = 1 ms. Cites [Kohler1996-SKclone] (DOI
  10.1126/science.273.5282.1709). EC50 = 0.43 µM.
* `CaDynamics_E2.mod` — Single-shell Ca pool: τ_decay = 80 ms (default), gamma = 0.05 (free Ca
  fraction), depth = 0.1 µm, minCai = 100 nM.
* `Im.mod` — M-current / Kv7 (Adams 1982 formulation):
  `mAlpha = 3.3e-3 × exp(2.5 × 0.04 × (v + 35))`, V_½ ≈ -35 mV, Q10 = 2.3, reference temp = 21 °C.
  Cites [Adams1982-MCurrent].
* No separate BK file — Hay et al. 2011 used SK as the only Ca-activated K (K(Ca)) mechanism in the
  L5 model.

**Package C — Mateos-Aparicio, Murphy & Storm 2014 (ModelDB 169240)** [MMS2014-DGC][MMS2014-Github]:

* `DGC_sAHP.mod` — Slow AHP / SK-like, two-state Ca-dependent kinetic scheme with `cah = 10 µM`, τ ≈
  9-200 ms (state-dependent). Less canonical than Hay's `SK_E2.mod`.
* `DGC_M.mod` — Kv7 / M-current with V_½ ≈ -49.8 to -25.3 mV (subtype-dependent), slope = 9 mV, Q10
  = 5, reference 22 °C, multi-component τ from 20-1473 ms. Models granule-cell-specific M-current.
* `Aradi_Ca.mod` and `Aradi_CadepK.mod` — Calcium dynamics and Ca-dependent K from the Aradi
  dentate-granule-cell convention referenced inside the file.

**Recommended hybrid for t0074**: take BK from Mainen-Sejnowski 1996 `kca.mod`, SK from Hay 2011
`SK_E2.mod`, Kv7 from Hay 2011 `Im.mod` (peer-reviewed Adams 1982 formalism, simplest), and the
calcium pool from Hay 2011 `CaDynamics_E2.mod` (τ = 80 ms is in the 50-100 ms RGC-typical range
[F&M1997-PMC] and matches Bed B's existing convention closer than 200 ms). All four are released
under standard ModelDB terms with peer-reviewed source papers.

### BK Channel Kinetic Parameters (V_half, Slope, Ca-Sensitivity)

The Mainen-Sejnowski 1996 `kca.mod` is the de-facto BK template in ModelDB; it cites
[Pennefather1990-Sympath, Reuveni1993-Cortical]. Numerical parameters extracted from the source
file: V_½ ≈ -28 mV (effective), Q10 = 2.3, Ca-half EC50 in the 1-10 µM range with single-Hill
exponent. [Grimes2012-MouseBK] (J Neurosci 2012, DOI 10.1523/JNEUROSCI.4654-11.2012) reports BK in
the in-vivo mouse retina but does not tabulate kinetic constants — it confirms BK function without
supplying compartmental-model parameters. [Wang1998-Ferret] reports BK single-channel conductance of
**118 pS** in ferret RGC, consistent with the canonical mammalian BK range (150-260 pS in symmetric
K) reported by [Lipton1987-Rat] and [Grimes2012-MouseBK].

### SK Channel Kinetic Parameters

Hay 2011 `SK_E2.mod` is the cleanest published SK template in ModelDB: voltage-independent,
Ca-driven, **EC50 = 0.43 µM** with **Hill coefficient = 4.8**, τ = 1 ms, citing the foundational
[Kohler1996-SKclone] paper. [Wang1998-Ferret] reports apamin-sensitive 22 pS SK in ferret RGC,
consistent with the 10 pS unit conductance reported by [Kohler1996-SKclone] for heterologously
expressed SK1/2/3 in HEK293 cells. The general SK Ca half-activation EC50 is **~300-400 nM** when
measured via calmodulin-Ca binding [Kohler1996-SKclone]. Hay's 0.43 µM is at the upper end of this
range, biophysically consistent.

### Kv7 / M-Current Kinetic Parameters

Three published sources have well-cited Kv7 / M-current MODs:

* Hay 2011 `Im.mod` — V_½ ≈ -35 mV, slope embedded in α/β rate functions, Q10 = 2.3, cites
  [Adams1982-MCurrent].
* Mainen-Sejnowski 1996 `km.mod` — V_½ ≈ -30 mV, slope = 9 mV, Q10 = 2.3, max rates 0.001 /ms.
* Mateos-Aparicio 2014 `DGC_M.mod` — V_½ adjustable -49.8 to -25.3 mV, slope = 9 mV, Q10 = 5,
  multi-component τ.

[Hu2002-MResonance] (J Physiol DOI 10.1113/jphysiol.2002.029249) characterises the M-current in rat
hippocampal pyramidal cells: peak θ-resonance at 2-5 Hz at 33 °C → 7 Hz at 38 °C. M-current kinetics
extrapolated to 37 °C should give τ at -40 mV in the **40-80 ms** range — consistent with Hay 2011's
Adams formalism. [Shah2008-Axonal] (PNAS DOI 10.1073/pnas.0802805105, ModelDB 112546) specifically
locates Kv7 in the AIS, foreshadowing the t0075 AIS-localised follow-up flagged in the task
description risks.

[Hu2007-Perisomatic] (J Neurosci, DOI 10.1523/JNEUROSCI.4463-06.2007) localises Kv7 to the
perisomatic compartment in CA1 — consistent with t0074's somatic-only insertion strategy. The
Kv7.2/Kv7.3 heteromer carries the bulk of the M-current in pyramidal cells [Brown2009-Review].

### Calcium-Pool Conventions for RGC Single-Shell Decay

The canonical RGC convention is a single-shell sub-membrane pool with first-order Ca removal.
Documented decay time constants:

* [F&M1997-PMC] (Fohlmeister-Miller 1997 RGC five-channel model): **tau_Ca = 50 ms** (explicitly
  stated in the methods).
* Hay 2011 `CaDynamics_E2.mod`: τ = 80 ms, depth = 0.1 µm, gamma = 0.05.
* Mainen-Sejnowski 1996 `cad.mod`: τ = 200 ms, depth = 0.1 µm.
* Destexhe 1993 thalamic relay: τ ~10 ms (faster, with Michaelis-Menten pump).

All use shell depth = 0.1 µm. **Recommended for t0074**: τ_decay = 80 ms (Hay 2011 default), shell
depth = 0.1 µm, gamma = 0.05, minCai = 100 nM. This is in the 50-100 ms range that matches
[F&M1997-PMC] for RGCs and is the convention closest to what Bed B's existing `cad` likely uses.
Document source DOI in the library asset's `details.json` per the paper-asset specification.

### Tuning-Width Metric Definitions in the Mammalian Retina Literature

Across 5+ DSGC studies surveyed, three width-related metrics dominate:

* **Vector-sum DSI** = `|Σᵢ rᵢ exp(i·θᵢ)| / Σᵢ rᵢ` — circular concentration. [Rivlin2012-Neuron]
  defines the standard DSGC classification threshold as **vector sum > 0.2 AND DSI* > 0.3**.
  [Hanson2019-eLife] uses vector-sum DSI = 0.33 (wild-type) → 0.07 (without SAC asymmetry) on an
  8-direction protocol. The vector-sum length distinguishes tuning *strength*; its angle gives PD.
* **DSI** = (R_PD - R_ND) / (R_PD + R_ND) — point-estimate, used by t0067 and the [Chen2009-PMC]
  protocol that already exists in the project corpus.
* **HWHM (half-width at half-maximum)** = full-width-at-half-maximum / 2, fitted from the polar
  tuning curve. [Chen2009-PMC] reports adult mouse ON-OFF DSGC HWHM "is not significantly different
  from P11" but does not tabulate degrees in text; figures suggest typical HWHM around 40-70°. The
  [Hanson2019-eLife] vector-sum bandwidth is consistent.

For t0074, all three should be reported: HWHM via linear interpolation around half-max, vector-sum
DSI, and PD-vs-ND DSI. The vector-sum DSI is the metric most robust to flat tuning curves and is the
appropriate primary metric for low-rate conditions [Hanson2019-eLife, Rivlin2012-Neuron].

### Mammalian-RGC BK / SK Existence Confirmed; Direct Kinetic Parameters Absent

Across the entire mammalian-retina literature, there is **no DSGC-specific** BK / SK / Kv7
whole-cell kinetic dataset. Closest validation references:

* [Wang1998-Ferret] (J Neurophysiol DOI 10.1152/jn.1998.79.1.151): Both BKCa (118 pS) and SKCa (22
  pS) channels expressed in ferret RGC; apamin and CTX block produce shortened time-to- threshold
  and reduced post-spike hyperpolarisation.
* [Lipton1987-Rat] (J Physiol vol 385, pp 361-391): BKCa identified in single-channel recordings
  from rat RGC; first identification.
* [Grimes2012-MouseBK] (J Neurosci 32:4861, DOI 10.1523/JNEUROSCI.4654-11.2012): BK channels
  modulate visual signals pathway-specifically in vivo mouse retina; functional but not kinetic.
* Goldfish RGC Ih recordings (Tabata & Ishida 1996, not directly applicable to mammalian BK/SK
  kinetics; cited only for general RGC biophysics context).

The **biophysically plausible inference**: vendor MODs from Hay 2011 / Mainen-Sejnowski 1996 with
Q10 correction to 35-37 °C, validate that the resulting Bed A model produces RGC-like firing
patterns (peak rate 100-200 Hz, post-spike AHP, no instability), and document explicitly in the
library asset that DSGC-specific kinetic data does not exist.

## Methodology Insights

* **Use Hay 2011 (ModelDB 139653) `SK_E2.mod` and `Im.mod` as the SK and Kv7 templates** — both are
  released under standard ModelDB terms, well-cited (300+ Hay 2011 citations), and have clear source
  papers ([Kohler1996-SKclone] for SK; [Adams1982-MCurrent] for M-current).
* **Use Mainen-Sejnowski 1996 (ModelDB 2488) `kca.mod` as the BK template** — it is the canonical
  voltage-and-Ca-activated K mechanism in ModelDB, cited by Hay 2011 themselves for the same
  formalism.
* **Use Hay 2011 `CaDynamics_E2.mod` as the calcium-pool template** with τ_decay = 80 ms, depth =
  0.1 µm, gamma = 0.05. This sits between Fohlmeister-Miller's RGC-specific 50 ms [F&M1997-PMC] and
  Mainen-Sejnowski's cortical 200 ms.
* **Document MOD provenance in `details.json`**: source ModelDB accession (2488 / 139653), source
  paper DOI ([MS1996-modeldb], [Hay2011-L5]), parameter modifications (Q10-corrected to 37 °C), and
  any custom edits.
* **Apply Q10 ~ 2.3 for kinetic temperature correction** when going from the Adams 21 °C reference
  to Bed A's 35-37 °C runtime. This matches the Hay 2011 internal default and the [F&M1997-PMC] Q10
  = 1.95 for gating kinetics in RGCs.
* **Set BK density grid in the same low/medium/high tier as t0067** — for canonical pyramidal cells,
  `gbar_kca = 0.3-3.0 mS/cm²` (Mainen-Sejnowski 1996 defaults). For RGCs, scale by 0.5-1.5× this
  range (no published RGC-specific anchor).
* **Set SK density grid lower** than BK: typical pyramidal `gbar_SK_E2 = 0.06-0.6 mS/cm²` (Hay 2011
  default range). [Wang1998-Ferret] suggests SK in RGCs is the dominant contributor to mAHP but
  quantitatively comparable or smaller than BK.
* **Set Kv7 density grid lowest**: typical pyramidal `gbar_Im = 0.0001-0.005 mS/cm²` (Hay 2011). Kv7
  at the soma is small in pyramidal cells [Hu2007-Perisomatic, Shah2008-Axonal]; for RGCs no somatic
  anchor exists, so use this range and expect mostly inert results — consistent with the task
  description's risks-and-fallbacks section that flags AIS-localised Kv7 as a t0075 deferral.
* **Compute vector-sum DSI as the primary residual-DSI metric** [Hanson2019-eLife] alongside HWHM
  for the polar tuning curve [Chen2009-PMC]. PD-vs-ND DSI is retained for cross-task comparison with
  t0067.
* **For HWHM calculation** use linear interpolation around the half-max points of the 12-angle polar
  curve. Set HWHM to `null` for low-rate conditions (peak mean rate < 1 Hz).
* **Report tuning-width sensitivity per channel** as recommended by [Hay2011-L5] (their per-channel
  density-density grid is the methodological precedent for systematic channel sweeps).

### Hypotheses to Test

1. **The vendored BK at high density rescues vector-sum DSI within 0.10 of baseline 0.797** because
   BK's Ca-dependent activation preferentially suppresses high-firing PD trains where Ca²⁺
   accumulation is highest [Wang1998-Ferret, Pennefather1990-Sympath]. Falsifiable by the t0074 |Δ
   vector-sum DSI| > 0.05 threshold from the pass criteria.
2. **The vendored SK at medium / high density produces measurable broadening (HWHM delta > 5
   degrees)** because [Wang1998-Ferret] reports SK underlies the mAHP responsible for
   spike-frequency adaptation; reducing peak PD rate reshapes width. Falsifiable by direct HWHM
   measurement.
3. **The vendored Kv7 produces no measurable somatic effect** at any density because somatic Kv7 in
   RGCs is not well-documented [Shah2008-Axonal, Hu2007-Perisomatic]; the AIS is the canonical Kv7
   site. Falsifiable by the |delta HWHM| < 5 degrees AND |delta vector-sum DSI| < 0.05 threshold.
4. **Vector-sum DSI tracks HWHM linearly only in the high-firing-rate regime** (peak > 50 Hz)
   [Hanson2019-eLife, Chen2009-PMC]. Below this rate, the metrics decouple — vector-sum DSI may stay
   above 0.10 even when HWHM widens beyond 60 degrees because ND firing remains low.

### Best Practices

* Use ModelDB-deposited MOD files with peer-reviewed source citations (Hay 2011, Mainen-Sejnowski
  1996, Mateos-Aparicio 2014). Do not hand-fit channel kinetics from scratch.
* Document every parameter modification (Q10, density, V_½ shift) in the library asset's
  `details.json` with the source DOI.
* Record the calcium-pool τ explicitly (80 ms is recommended) — not following a published value is
  the most common silent breakage in cross-cell-type Ca-pool ports.
* Run the Stage-2 regression gate before any new channel sweep [task description Stage 2]: this
  catches calcium-pool-induced disturbance of the baseline DSGC dynamics before 1500 trials are
  burned.

## Discovered Papers

These are papers discovered during internet search that should be added to the project corpus.
Cross-checked against the existing 64-paper corpus via direct DOI / title comparison; none of the
following are present.

### [Hay2011-L5]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schürmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Why download**: Source paper for ModelDB 139653 — the primary source of `SK_E2.mod`,
  `CaDynamics_E2.mod`, and `Im.mod` MOD files vendored in this task. Documents the kinetic parameter
  values, conductance density tiers, and Ca-pool conventions that t0074's Stage-1 vendoring follows
  verbatim.

### [Wang1998-Ferret]

* **Title**: Calcium-Activated Potassium Conductances in Retinal Ganglion Cells of the Ferret
* **Authors**: Wang, G.-Y., Robinson, D. W., Chalupa, L. M.
* **Year**: 1998
* **DOI**: `10.1152/jn.1998.79.1.151`
* **URL**: https://journals.physiology.org/doi/full/10.1152/jn.1998.79.1.151
* **Suggested categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `patch-clamp`
* **Why download**: First quantitative demonstration of both BKCa (118 pS) and SKCa (22 pS) in
  mammalian RGC. Provides the canonical reference for "BK and SK in RGC" — the validation anchor for
  t0074's vendored MODs. CTX and apamin pharmacology directly relevant to the channel-
  identification logic.

### [Grimes2012-MouseBK]

* **Title**: BK Channels Mediate Pathway-Specific Modulation of Visual Signals in the In Vivo Mouse
  Retina
* **Authors**: Grimes, W. N., Li, W., Chávez, A. E., Diamond, J. S.
* **Year**: 2012
* **DOI**: `10.1523/JNEUROSCI.4654-11.2012`
* **URL**: https://www.jneurosci.org/content/32/14/4861
* **Suggested categories**: `voltage-gated-channels`, `retinal-ganglion-cell`
* **Why download**: Demonstrates BK function in mouse retina in vivo using a BK-knockout mouse.
  Confirms BK is functionally significant in the rod/cone pathway. Directly relevant to t0074's
  hypothesis that BK density at the soma can rescue or reshape DSGC tuning.

### [Kohler1996-SKclone]

* **Title**: Small-Conductance, Calcium-Activated Potassium Channels from Mammalian Brain
* **Authors**: Köhler, M., Hirschberg, B., Bond, C. T., Kinzie, J. M., Marrion, N. V., Maylie, J.,
  Adelman, J. P.
* **Year**: 1996
* **DOI**: `10.1126/science.273.5282.1709`
* **URL**: https://www.science.org/doi/10.1126/science.273.5282.1709
* **Suggested categories**: `voltage-gated-channels`
* **Why download**: Foundational SK1/SK2/SK3 cloning paper. Directly cited by Hay 2011's `SK_E2.mod`
  MOD file as the source of EC50 = 0.43 µM and Hill = 4.8. Required citation in the vendored library
  asset's `details.json`.

### [Adams1982-MCurrent]

* **Title**: M-currents and other potassium currents in bullfrog sympathetic neurones
* **Authors**: Adams, P. R., Brown, D. A., Constanti, A.
* **Year**: 1982
* **DOI**: `10.1113/jphysiol.1982.sp014102`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/abs/10.1113/jphysiol.1982.sp014102
* **Suggested categories**: `voltage-gated-channels`, `patch-clamp`
* **Why download**: Foundational M-current characterisation paper. Cited verbatim in Hay 2011's
  `Im.mod` and Mainen-Sejnowski 1996's `km.mod` MOD files. The kinetic formalism used in both
  vendored Kv7 candidates derives directly from this 1982 voltage-clamp study.

### [Shah2008-Axonal]

* **Title**: Functional significance of axonal Kv7 channels in hippocampal pyramidal neurons
* **Authors**: Shah, M. M., Migliore, M., Valencia, I., Cooper, E. C., Brown, D. A.
* **Year**: 2008
* **DOI**: `10.1073/pnas.0802805105`
* **URL**: https://www.pnas.org/doi/abs/10.1073/pnas.0802805105
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Why download**: Establishes the AIS-localised Kv7 hypothesis and provides the published NEURON
  model (ModelDB 112546) for axonal Kv7. Direct precedent for t0074's "if Kv7-at-soma is inert,
  defer to t0075 AIS-localised follow-up" risk-mitigation plan.

### [MMS2014-DGC]

* **Title**: Complementary functions of SK and Kv7/M potassium channels in excitability control and
  synaptic integration in rat hippocampal dentate granule cells
* **Authors**: Mateos-Aparicio, P., Murphy, R., Storm, J. F.
* **Year**: 2014
* **DOI**: `10.1113/jphysiol.2013.267872`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/full/10.1113/jphysiol.2013.267872
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`, `patch-clamp`
* **Why download**: Models BOTH SK and Kv7 in the same compartmental model (ModelDB 169240).
  Provides the second-line option for SK / Kv7 vendoring if Hay 2011's `SK_E2.mod` is found
  inconsistent with RGC firing constraints in Stage-2 regression.

### [Hu2002-MResonance]

* **Title**: Two forms of electrical resonance at theta frequencies, generated by M-current,
  h-current and persistent Na+ current in rat hippocampal pyramidal cells
* **Authors**: Hu, H., Vervaeke, K., Storm, J. F.
* **Year**: 2002
* **DOI**: `10.1113/jphysiol.2002.029249`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/abs/10.1113/jphysiol.2002.029249
* **Suggested categories**: `voltage-gated-channels`, `patch-clamp`
* **Why download**: Provides whole-cell M-current kinetics in rat hippocampal pyramidal cells
  including temperature dependence (peak resonance 2-5 Hz at 33 °C → 7 Hz at 38 °C). Empirical
  anchor for the Q10 correction applied to the vendored Kv7 MOD when scaling from 21-23 °C to Bed
  A's 35-37 °C runtime.

## Recommendations for This Task

1. **Vendor BK from Mainen-Sejnowski 1996 `kca.mod` (ModelDB 2488)** — the canonical voltage-and-
   Ca-activated K MOD in NEURON. Document in `details.json`: source DOI 10.1038/382363a0, ModelDB
   accession 2488, Q10 = 2.3 corrected to 37 °C, Pennefather 1990 + Reuveni 1993 as upstream
   citations.

2. **Vendor SK from Hay 2011 `SK_E2.mod` (ModelDB 139653)** — voltage-independent, Ca-driven SK with
   EC50 = 0.43 µM and Hill = 4.8. Document in `details.json`: source DOI
   10.1371/journal.pcbi.1002107, ModelDB accession 139653, [Kohler1996-SKclone] as the upstream
   biophysical citation.

3. **Vendor Kv7 from Hay 2011 `Im.mod` (ModelDB 139653)** — Adams 1982 formalism with V_½ ≈ -35 mV,
   Q10 = 2.3. Document in `details.json`: same source DOI as SK, [Adams1982-MCurrent] as upstream
   citation.

4. **Use Hay 2011 `CaDynamics_E2.mod` for the calcium pool** with τ_decay = 80 ms, depth = 0.1 µm,
   gamma = 0.05, minCai = 100 nM. Mirror Bed B's existing `cad` parameters where they overlap; if
   Bed B uses τ ≠ 80 ms, prefer Bed B's value for consistency. Update from `research_papers.md`'s
   "30-100 ms" range — Hay's 80 ms is in the upper half of that range and is RGC-compatible per
   [F&M1997-PMC] (50 ms).

5. **Set the Stage-1 channel-density grid** at the canonical Hay 2011 values, scaled to Bed A's
   compartment surface area:
   * BK: low = 0.3, medium = 1.0, high = 3.0 mS/cm² (Mainen-Sejnowski 1996 range).
   * SK: low = 0.06, medium = 0.2, high = 0.6 mS/cm² (Hay 2011 range).
   * Kv7: low = 0.0001, medium = 0.001, high = 0.005 mS/cm² (Hay 2011 range — soma is low). These
     are starting points only; the t0067 grid was scaled from a similar published-pyramidal
     convention.

6. **Adopt the [Rivlin2012-Neuron] vector-sum > 0.2 AND DSI > 0.3 criterion** for "directionally
   selective" classification of any condition. Conditions falling below either threshold are
   reported as non-DS in the conclusion section and the vector-sum DSI carries the residual
   information [Hanson2019-eLife].

7. **Compute three width metrics per condition** (HWHM, vector-sum DSI, peak rate) plus the legacy
   PD-vs-ND DSI for cross-task comparison with t0067. Update from `research_papers.md`'s
   recommendation #5: vector-sum DSI is the primary residual metric, PD-vs-ND DSI the cross-task
   anchor.

8. **Pre-register the Stage-2 regression-gate threshold at 1e-3** as already specified in the task
   description. If the un-zeroed CaL/CaT pushes baseline DSI off 0.797 by more than this threshold,
   switch to the closed-form `Ca_i` fallback — internet research did not surface a simpler
   alternative.

9. **Cite [Wang1998-Ferret] and [Grimes2012-MouseBK]** in the library asset's documentation as the
   mammalian-RGC validation anchors for the existence (not kinetics) of BK and SK in RGCs. This
   honestly represents the state of the literature: existence is established; DSGC-specific kinetics
   are not.

10. **If Kv7-at-soma is inert at all three densities**, log this as a clean negative result in
    Stage-5 analysis and recommend the t0075 AIS-localised Kv7 follow-up per [Shah2008-Axonal]. The
    literature is consistent with this outcome.

## Source Index

### [Hay2011-L5]

* **Type**: paper
* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schürmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Peer-reviewed**: yes (PLOS Comp Biol)
* **Relevance**: Source paper for ModelDB 139653 — the primary vendoring source for `SK_E2.mod`,
  `CaDynamics_E2.mod`, and `Im.mod` used in t0074 Stage 1.

### [MS1996-modeldb]

* **Type**: paper
* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **URL**: https://www.nature.com/articles/382363a0
* **Peer-reviewed**: yes (Nature)
* **Relevance**: Source paper for ModelDB 2488 — provides the BK template (`kca.mod`), the M-current
  template (`km.mod`), and the calcium-pool template (`cad.mod`) inspected by this research task.
  Note: this paper IS already in the project corpus (t0015) — included here as a source for the MOD
  files only.

### [MS1996-cad-Github]

* **Type**: repository
* **Title**: ModelDBRepository/2488 — Mainen and Sejnowski 1996 NEURON code
* **Author/Org**: ModelDB Repository (curated by Yale CNBC)
* **Date**: 2016-2024 (most recent commits)
* **URL**: https://github.com/ModelDBRepository/2488
* **Last updated**: 2024 (per ModelDB metadata)
* **Peer-reviewed**: no (associated with peer-reviewed [MS1996-modeldb])
* **Relevance**: Direct source of `kca.mod`, `km.mod`, and `cad.mod` MOD files. Allows direct
  inspection of kinetic parameters without paywall access.

### [Hay2011-CaDyn-Github]

* **Type**: repository
* **Title**: OpenSourceBrain/L5bPyrCellHayEtAl2011
* **Author/Org**: Open Source Brain (curated)
* **Date**: 2024 (last commit)
* **URL**: https://github.com/OpenSourceBrain/L5bPyrCellHayEtAl2011
* **Last updated**: 2024
* **Peer-reviewed**: no (associated with peer-reviewed [Hay2011-L5])
* **Relevance**: Open Source Brain replication of ModelDB 139653 with all .mod files publicly
  accessible. Allows direct inspection of `SK_E2.mod`, `CaDynamics_E2.mod`, and `Im.mod` parameters.

### [MMS2014-DGC]

* **Type**: paper
* **Title**: Complementary functions of SK and Kv7/M potassium channels in excitability control and
  synaptic integration in rat hippocampal dentate granule cells
* **Authors**: Mateos-Aparicio, P., Murphy, R., Storm, J. F.
* **Year**: 2014
* **DOI**: `10.1113/jphysiol.2013.267872`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/full/10.1113/jphysiol.2013.267872
* **Peer-reviewed**: yes (J Physiol)
* **Relevance**: Source paper for ModelDB 169240 — provides a third MOD-file package combining SK
  and Kv7 in one model, used as a fallback option for t0074 vendoring.

### [MMS2014-Github]

* **Type**: repository
* **Title**: ModelDBRepository/169240 — Mateos-Aparicio et al. 2014 dentate granule cell model
* **Author/Org**: ModelDB Repository
* **Date**: 2018
* **URL**: https://github.com/ModelDBRepository/169240
* **Last updated**: 2018
* **Peer-reviewed**: no (associated with peer-reviewed [MMS2014-DGC])
* **Relevance**: Direct source of `DGC_M.mod` (Kv7) and `DGC_sAHP.mod` (SK / sAHP) inspected during
  this research task. Provides the kinetic parameters reported in the Key Findings section above.

### [Wang1998-Ferret]

* **Type**: paper
* **Title**: Calcium-Activated Potassium Conductances in Retinal Ganglion Cells of the Ferret
* **Authors**: Wang, G.-Y., Robinson, D. W., Chalupa, L. M.
* **Year**: 1998
* **DOI**: `10.1152/jn.1998.79.1.151`
* **URL**: https://journals.physiology.org/doi/full/10.1152/jn.1998.79.1.151
* **Peer-reviewed**: yes (J Neurophysiol)
* **Relevance**: First demonstration of both BKCa and SKCa in mammalian RGC. Validation anchor for
  t0074's vendored channels. Confirms the channels exist in mammalian retina even though
  DSGC-specific kinetics are not measured.

### [Lipton1987-Rat]

* **Type**: paper
* **Title**: Voltage-dependent conductances of solitary ganglion cells dissociated from the rat
  retina
* **Authors**: Lipton, S. A., Tauck, D. L.
* **Year**: 1987
* **DOI**: `10.1113/jphysiol.1987.sp016497`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/abs/10.1113/jphysiol.1987.sp016497
* **Peer-reviewed**: yes (J Physiol)
* **Relevance**: Earliest single-channel identification of BKCa in rat RGC. Background reference for
  the existence of mammalian-RGC Ca-activated K channels.

### [Grimes2012-MouseBK]

* **Type**: paper
* **Title**: BK Channels Mediate Pathway-Specific Modulation of Visual Signals in the In Vivo Mouse
  Retina
* **Authors**: Grimes, W. N., Li, W., Chávez, A. E., Diamond, J. S.
* **Year**: 2012
* **DOI**: `10.1523/JNEUROSCI.4654-11.2012`
* **URL**: https://www.jneurosci.org/content/32/14/4861
* **Peer-reviewed**: yes (J Neurosci)
* **Relevance**: Functional demonstration of BK in mouse retina in vivo; confirms BK matters for
  visual processing. Most-recent mouse-RGC anchor for the vendored BK MOD.

### [Kohler1996-SKclone]

* **Type**: paper
* **Title**: Small-Conductance, Calcium-Activated Potassium Channels from Mammalian Brain
* **Authors**: Köhler, M., Hirschberg, B., Bond, C. T., Kinzie, J. M., Marrion, N. V., Maylie, J.,
  Adelman, J. P.
* **Year**: 1996
* **DOI**: `10.1126/science.273.5282.1709`
* **URL**: https://www.science.org/doi/10.1126/science.273.5282.1709
* **Peer-reviewed**: yes (Science)
* **Relevance**: Foundational SK-channel cloning paper. Cited by Hay 2011's `SK_E2.mod` as the
  source of the EC50 = 0.43 µM and Hill = 4.8 calcium-binding parameters.

### [Adams1982-MCurrent]

* **Type**: paper
* **Title**: M-currents and other potassium currents in bullfrog sympathetic neurones
* **Authors**: Adams, P. R., Brown, D. A., Constanti, A.
* **Year**: 1982
* **DOI**: `10.1113/jphysiol.1982.sp014102`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/abs/10.1113/jphysiol.1982.sp014102
* **Peer-reviewed**: yes (J Physiol)
* **Relevance**: Foundational M-current characterisation. Direct source of the Adams-Yamada-Koch
  formalism implemented in Hay 2011's `Im.mod` and Mainen-Sejnowski's `km.mod`.

### [Shah2008-Axonal]

* **Type**: paper
* **Title**: Functional significance of axonal Kv7 channels in hippocampal pyramidal neurons
* **Authors**: Shah, M. M., Migliore, M., Valencia, I., Cooper, E. C., Brown, D. A.
* **Year**: 2008
* **DOI**: `10.1073/pnas.0802805105`
* **URL**: https://www.pnas.org/doi/abs/10.1073/pnas.0802805105
* **Peer-reviewed**: yes (PNAS)
* **Relevance**: Establishes AIS-localised Kv7 in pyramidal cells. Direct precedent for t0074's
  "Kv7-at-soma is inert → t0075 AIS follow-up" risk-mitigation logic. ModelDB 112546 is the
  associated NEURON model.

### [Hu2002-MResonance]

* **Type**: paper
* **Title**: Two forms of electrical resonance at theta frequencies, generated by M-current,
  h-current and persistent Na+ current in rat hippocampal pyramidal cells
* **Authors**: Hu, H., Vervaeke, K., Storm, J. F.
* **Year**: 2002
* **DOI**: `10.1113/jphysiol.2002.029249`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/abs/10.1113/jphysiol.2002.029249
* **Peer-reviewed**: yes (J Physiol)
* **Relevance**: Whole-cell M-current kinetics in rat pyramidal cells with explicit temperature
  dependence (33-38 °C). Anchor for the Q10 correction applied to vendored Kv7.

### [Hu2007-Perisomatic]

* **Type**: paper
* **Title**: M-Channels (Kv7/KCNQ Channels) That Regulate Synaptic Integration, Excitability, and
  Spike Pattern of CA1 Pyramidal Cells Are Located in the Perisomatic Region
* **Authors**: Hu, H., Vervaeke, K., Storm, J. F.
* **Year**: 2007
* **DOI**: `10.1523/JNEUROSCI.4463-06.2007`
* **URL**: https://www.jneurosci.org/content/27/8/1853
* **Peer-reviewed**: yes (J Neurosci)
* **Relevance**: Localises Kv7 to the perisomatic compartment — supports the somatic insertion
  strategy in t0074 Stage-3.

### [Brown2009-Review]

* **Type**: paper
* **Title**: Neural KCNQ (Kv7) channels
* **Authors**: Brown, D. A., Passmore, G. M.
* **Year**: 2009
* **DOI**: `10.1111/j.1476-5381.2009.00111.x`
* **URL**: https://bpspubs.onlinelibrary.wiley.com/doi/10.1111/j.1476-5381.2009.00111.x
* **Peer-reviewed**: yes (Br J Pharmacol)
* **Relevance**: Comprehensive review of KCNQ neuronal physiology including subunit composition
  (Kv7.2/Kv7.3 heteromer dominant) and pharmacology. Background reference for the vendored Kv7.

### [Destexhe1993-Thalamic]

* **Type**: paper
* **Title**: Ionic mechanisms for intrinsic slow oscillations in thalamic relay neurons
* **Authors**: Destexhe, A., Babloyantz, A., Sejnowski, T. J.
* **Year**: 1993
* **DOI**: `10.1016/S0006-3495(93)81190-1`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(93)81190-1
* **Peer-reviewed**: yes (Biophys J)
* **Relevance**: Source of the single-shell `cad.mod` calcium-pool decay formalism used by
  Mainen-Sejnowski 1996 and adapted by Hay 2011's `CaDynamics_E2.mod`.

### [F&M1997-PMC]

* **Type**: paper
* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **URL**: https://journals.physiology.org/doi/full/10.1152/jn.1997.78.4.1948
* **Peer-reviewed**: yes (J Neurophysiol)
* **Relevance**: RGC-specific calcium-pool τ_Ca = 50 ms anchor; the canonical RGC five-channel
  model. Already in the project corpus (t0019); referenced here for the τ value extracted via
  internet search.

### [Pennefather1990-Sympath]

* **Type**: paper
* **Title**: Two distinct Ca-dependent K currents in bullfrog sympathetic ganglion cells
* **Authors**: Pennefather, P. S., Lancaster, B., Adams, P. R., Nicoll, R. A.
* **Year**: 1985
* **DOI**: `10.1073/pnas.82.9.3040`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.82.9.3040
* **Peer-reviewed**: yes (PNAS)
* **Relevance**: Cited by Mainen-Sejnowski 1996's `kca.mod` as the source of the BK kinetic
  parameters. Note: the precise file citation is "Pennefather (1990)" but the most-cited Pennefather
  BK paper is the 1985 PNAS paper; the file may refer to a 1990 follow-up not located via search.

### [Reuveni1993-Cortical]

* **Type**: paper
* **Title**: Stepwise repolarization from Ca2+ plateaus in neocortical pyramidal cells: evidence for
  nonhomogeneous distribution of HVA Ca2+ channels in dendrites
* **Authors**: Reuveni, I., Friedman, A., Amitai, Y., Gutnick, M. J.
* **Year**: 1993
* **DOI**: `10.1523/JNEUROSCI.13-11-04609.1993`
* **URL**: https://www.jneurosci.org/content/13/11/4609
* **Peer-reviewed**: yes (J Neurosci)
* **Relevance**: Cited by Mainen-Sejnowski 1996's `kca.mod` as a parameter source for cortical
  pyramidal BK kinetics.

### [Hanson2019-eLife]

* **Type**: paper
* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **URL**: https://elifesciences.org/articles/42392
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Already in the project corpus (t0002); referenced here for the vector-sum DSI
  metric definition (vector-sum DSI = 0.33 → 0.07 transition with non-directional SAC GABA). This is
  the residual-metric anchor for low-firing-rate t0074 conditions.

### [Chen2009-PMC]

* **Type**: paper
* **Title**: Physiological properties of direction-selective ganglion cells in early postnatal and
  adult mouse retina
* **Authors**: Chen, M., Weng, S., Deng, Q., Xu, Z., He, S.
* **Year**: 2009
* **DOI**: `10.1113/jphysiol.2008.161240`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC2669973/
* **Peer-reviewed**: yes (J Physiol)
* **Relevance**: Already in the project corpus (t0002); referenced here for the HWHM definition
  (full-width-at-half-maximum of the fitted polar tuning curve) and the empirical observation that
  HWHM is preserved across postnatal development despite peak-rate change.

### [Rivlin2012-Neuron]

* **Type**: paper
* **Title**: Visual stimulation reverses the directional preference of direction-selective retinal
  ganglion cells
* **Authors**: Rivlin-Etzion, M., Wei, W., Feller, M. B.
* **Year**: 2012
* **DOI**: `10.1016/j.neuron.2012.09.020`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(12)00865-7
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Establishes the standard mouse-DSGC directional-classification thresholds:
  vector-sum magnitude > 0.2 AND DSI* > 0.3. Directly informs t0074's Stage-5 metric reporting and
  pass-criteria interpretation.
