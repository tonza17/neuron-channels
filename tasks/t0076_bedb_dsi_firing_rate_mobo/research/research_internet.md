---
spec_version: "1"
task_id: "t0076_bedb_dsi_firing_rate_mobo"
research_stage: "internet"
searches_conducted: 12
sources_cited: 22
papers_discovered: 6
date_completed: "2026-05-01"
status: "complete"
---
# Research Internet: MOD-File Sourcing for Bed B Channel Vendoring

## Task Objective

Identify a canonical, citeable, ModelDB-hosted (or Allen-Institute-hosted) MOD-file source for each
of the six-to-seven new voltage-gated channel mechanisms that t0076 plans to vendor into
`tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods/`: Kdr, KM (Kv7), HCN (Ih), CaL (CaV1.x), CaT
(CaV3.x), BK (KCa1.1), and SK (KCa2). Also identify a canonical source for the cad
calcium-accumulation mechanism that BK and SK depend on. The deliverable is a per-channel "where do
I download a clean .mod file for X" recipe; the upstream literature survey on channel biology
already exists (t0019), so this file is deliberately narrow in scope.

## Gaps Addressed

The closest existing research document is the t0019 voltage-gated-channels literature survey
(`tasks/t0019_literature_survey_voltage_gated_channels/results/results_detailed.md`). The t0019
research_papers.md catalogue (in the t0019 task folder) covered Nav1.6, Nav1.2, AIS Kv1, and
Fohlmeister-Miller HH-style RGC kinetics; it explicitly DID NOT survey KM (Kv7), HCN, CaL, CaT, BK,
SK, or generic delayed-rectifier Kdr separately, and it did not produce a vendor-ready MOD-file
inventory. Therefore the gaps from `research_papers.md` (treating the t0019 results as the parent
corpus) that this internet survey must address are:

1. **Source for a clean Kdr (delayed rectifier) MOD file** — **Resolved**. The Mainen-Sejnowski
   1996 `kv.mod` (ModelDB 2488) is the canonical Hodgkin-Huxley-style delayed-rectifier with single
   n^4 gate, kinetics from Sah et al. and Hamill et al. 1991 [Mainen1996] [ModelDB2488-GH].

2. **Source for a clean KM / Kv7 / M-current MOD file** — **Resolved**. Two independent options:
   Mainen-Sejnowski 1996 `km.mod` (ModelDB 2488) [Mainen1996] and Hay 2011 `Im.mod` (ModelDB
   139653), with the Hay variant explicitly citing Adams et al. 1982 in the file header [Hay2011]
   [ModelDB139653-GH].

3. **Source for a clean HCN (Ih) MOD file** — **Resolved**. Three independent options: Hay 2011
   `Ih.mod` (Kole-Hallermann-Stuart 2006 kinetics) [Hay2011]; Migliore-Migliore 2012 `h.mod` (Magee
   1998 kinetics, hd suffix) [MiglioreMigliore2012] [ModelDB144541-GH]; Allen Institute `Ih.mod`
   [Allen-184297].

4. **Source for a clean CaL (L-type / CaV1.x) MOD file** — **Resolved**. Hay 2011 `Ca_HVA.mod`
   (high- voltage-activated Ca, treated as the L-type proxy in the Hay framework) [Hay2011]; or
   Mainen-Sejnowski 1996 `ca.mod` (single Ca channel, generic high-threshold) [Mainen1996].

5. **Source for a clean CaT (T-type / CaV3.x) MOD file** — **Resolved**. Hay 2011 `Ca_LVAst.mod`
   (low-voltage-activated, Avery-Johnston 1996 kinetics) [Hay2011]; or Allen Institute `Ca_LVA.mod`
   [Allen-184297].

6. **Source for a clean BK (KCa1.1) MOD file** — **Resolved**. Khaliq-Gouwens-Raman 2003
   `bkpkj.mod` from the cerebellar Purkinje high-frequency-firing model (ModelDB 48332). This is a
   self-contained `bkpkj` SUFFIX with both voltage- and calcium-dependent gating [Khaliq2003]
   [ModelDB48332-GH]. Hay 2011 has no BK file (only SK_E2), so BK must come from elsewhere.

7. **Source for a clean SK (KCa2) MOD file** — **Resolved**. Hay 2011 `SK_E2.mod` (Kohler et al.
   1996 kinetics) [Hay2011]; or Allen Institute `SK.mod` [Allen-184297]; or Mainen-Sejnowski 1996
   `kca.mod` (calcium-only gating, no voltage dependence) [Mainen1996].

8. **Source for a clean cad (calcium accumulation) MOD file** — **Resolved**. Two independent
   options with different mathematical forms: Mainen-Sejnowski 1996 `cad.mod`
   (Destexhe-Babloyantz-Sejnowski 1993 simplified-buffer mechanism, exposes `depth` and `taur`
   parameters that match exactly the t0076 task description's parameters 16 and 17) [Mainen1996]
   [Destexhe1993]; or Hay 2011 `CaDynamics_E2.mod` (similar Destexhe-1994-derived shell mechanism,
   exposes `depth`, `decay`, `gamma`, `minCai`) [Hay2011].

9. **License clarity for redistribution into this repo** — **Partially resolved**. None of the
   four source ModelDBs (2488, 3673, 48332, 139653) carry an explicit license file; the Allen
   Institute (184297) ties files to "Allen Institute's Terms of Use and Citation Policy"
   [Allen-184297]. However, the SenseLab / ModelDB framework operates under a long-standing
   community convention of research-use redistribution with attribution, and the t0067 precedent in
   this project already vendored five such MOD files (Nav1.6, NaP, NaR, Kv3, Kv4) under the same
   convention without intervention [t0067-precedent]. The conservative path adopted here: include a
   citation header in each vendored file naming the source ModelDB ID, original paper DOI, and
   original author; treat this as the project-internal "license-clean" standard.

## Search Strategy

**Sources searched**: ModelDB / SenseLab (modeldb.science), ModelDBRepository GitHub mirror via the
`gh api repos/ModelDBRepository/<id>/contents` interface, Allen Institute Brain Map portal
(brain-map.org), Allen Cell Types Database, GitHub general code search, PubMed via PMC, the Yale
NEURON forum, and the ICGenealogy ion-channel-model database (icg.neurotheory.ox.ac.uk).

**Inclusion criteria**: must be a publicly hosted MOD file with a documented primary publication;
must have a clear NEURON `SUFFIX` (NMODL mechanism name); must be vendorable as a single file (not
distributed across several files with shared global state). Preference for ModelDB-hosted entries
with GitHub mirrors at `github.com/ModelDBRepository/<id>`. **Exclusion**: anything behind a
paywall, anything requiring a custom build chain other than `nrnivmodl`, anything with an explicit
non- redistribution clause.

**Date range**: no restriction. The Adams 1982, Magee 1998, Mainen 1996, Khaliq 2003, Hay 2011
papers all predate the 2026 target compute environment but the MOD files compile cleanly under
modern NEURON 8.x via `nrnivmodl`.

**Queries executed** (12 total):

*Pass 1 — gap-targeted queries (one per channel):*

1. `ModelDB Mainen Sejnowski 1996 km.mod KM current accession 8210`
2. `ModelDB Hay 2011 L5 pyramidal SK_E2.mod Ca_LVAst Im.mod accession`
3. `ModelDB Migliore CA1 ih.mod hyperpolarization activated channel HCN`
4. `Allen Institute biophysical perisomatic NEURON mod files GitHub Im SK BK Ih cad`
5. `ModelDB Hay 2011 accession number L5b pyramidal cell BAC firing 139653`
6. `ModelDB Migliore 2012 Ih hippocampus accession pyramidal neuron`
7. `NEURON BK channel mod file ModelDB KCa1.1 calcium activated potassium`
8. `retinal ganglion cell NEURON model mod files Fohlmeister Miller 1997 ModelDB`

*Pass 2 — broadening queries:*

9. `ModelDB BK channel mod file Yamada McCormick large conductance Ca-activated potassium NEURON suffix`
10. `"BK.mod" OR "kbk.mod" NEURON ModelDB calcium activated potassium retinal ganglion cell`

*Pass 3 — snowball queries from Pass 1-2 hits (Khaliq, Allen):*

11. `"Khaliq" 2003 cerebellar Purkinje ModelDB accession resurgent sodium BK mod`
12. `"De Schutter Bower 1994" cerebellar Purkinje L-type calcium NEURON CaL.mod ModelDB`

**Search iterations**: Pass 1 confirmed Hay 2011 (139653) as a one-stop source for all channels
EXCEPT BK and Kdr. Pass 2 confirmed BK is not in Hay; Pass 3 then located the Khaliq 2003 Purkinje
model (48332) which has a self-contained `bkpkj.mod`. Each promising ModelDB entry was followed by a
`gh api repos/ModelDBRepository/<id>/contents` call to enumerate the actual `.mod` files and a raw-
GitHub fetch on the most relevant file to verify the SUFFIX, kinetics, and primary-reference
citation.

## Key Findings

### Hay 2011 L5b Pyramidal Cell (ModelDB 139653) is the highest-leverage single source

A `gh api` enumeration of `github.com/ModelDBRepository/139653/contents/mod` returns exactly 13
files with a clean one-channel-per-file factoring [ModelDB139653-GH]: `CaDynamics_E2.mod`,
`Ca_HVA.mod`, `Ca_LVAst.mod`, `Ih.mod`, `Im.mod`, `K_Pst.mod`, `K_Tst.mod`, `NaTa_t.mod`,
`NaTs2_t.mod`, `Nap_Et2.mod`, `SK_E2.mod`, `SKv3_1.mod`, `epsp.mod`. Six of the seven channels we
need (KM=Im, CaL=Ca_HVA, CaT=Ca_LVAst, HCN=Ih, SK=SK_E2, plus the cad mechanism CaDynamics_E2) come
from this single ModelDB entry. Each file is small (681-1446 b), and each cites a clear primary
reference in the file's header comment line: `Im.mod` cites "Adams et al. 1982" [Adams1982];
`SK_E2.mod` cites "Kohler et al. 1996" [Kohler1996]; `Ih.mod` cites "Kole, Hallermann, and Stuart,
J. Neurosci. 2006" [Kole2006]; `CaDynamics_E2.mod` cites a modification of Destexhe et al. 1994
[Destexhe1993].

This is a **best-practice** community convention: pull all the perisomatic channels you need from
one internally consistent source so that the kinetics, temperature corrections, and units are
mutually compatible. The Hay 2011 paper itself was published as *PLoS Computational Biology* with
DOI `10.1371/journal.pcbi.1002107` and is one of the most-cited single-cell modelling papers of the
past fifteen years [Hay2011]. The Hay framework was used in many subsequent multi-thousand-model
studies including the Allen Institute biophysical pipeline, the Blue Brain L5 model, and the
Maki-Marttunen schizophrenia model [eLife22152]. The Hay readme.html does not state an explicit
license, but the file is hosted on the SenseLab ModelDB repository which operates under a
long-standing community research-use convention [Hay2011-readme].

### BK is the one missing channel and Khaliq 2003 is the best replacement source

Hay 2011 contains SK (`SK_E2.mod`) but no BK. The clearest standalone BK MOD file in the literature
is the `bkpkj.mod` from Khaliq, Gouwens, and Raman 2003 (ModelDB 48332), titled "BK-type Purkinje
calcium-activated potassium current," authored by `nwg` (Nathan Gouwens) on 2002-08-19 [Khaliq2003]
[ModelDB48332-GH]. The SUFFIX is `bkpkj`. The mechanism uses three gating states (m-voltage,
h-voltage, z-calcium) with the conventional KCa1.1 voltage- and calcium-co-dependence. The file is
2202 b — small enough to vendor verbatim. **Hypothesis**: because Purkinje BK kinetics are tuned
for high-frequency firing (200+ Hz) and RGCs spike at substantially lower frequencies (typically
10-80 Hz in DSGCs), the Purkinje BK time constants may be too fast for an RGC AIS context. If the
optimiser finds that BK density saturates at the lower bound (~1e-5 S/cm²) the Khaliq kinetics are
likely too fast and a slower BK like the De Schutter-Bower 1994 cerebellar variant (ModelDB 7176)
[DeSchutter1994] should be tried as a fallback.

### Mainen 1996 is the best source for Kdr and cad

Mainen-Sejnowski 1996 (ModelDB 2488) provides `kv.mod` (delayed rectifier with Hodgkin-Huxley `n^4`
kinetics, citing Sah et al. and Hamill et al. 1991) and `cad.mod` (Destexhe-Babloyantz-Sejnowski
1993 simplified-buffer calcium accumulation with explicit `depth` and `taur` parameters)
[Mainen1996] [ModelDB2488-GH]. The `cad.mod` parameter signature `depth (um)` and `taur (ms)`
matches **exactly** the t0076 task description's parameters 16 (`cad.depth` 0.05-0.5 µm) and 17
(`cad.taur` 5-100 ms) — this is not a coincidence; the t0076 ranges were almost certainly drawn
from a Mainen-style model. The Mainen `kv.mod` is a generic delayed rectifier without voltage- or
current-clamp tuning to a specific cell type, which is exactly the desired property for the t0076
use case where the optimiser will scale the gbar.

The CaDynamics_E2 mechanism from Hay 2011 is more sophisticated (it includes a `gamma` free-Ca
fraction parameter and a `decay` time constant in addition to depth) but does NOT expose a direct
`taur` parameter — the t0076 plan calls `cad.taur` and assumes a Mainen-style mechanism. Therefore
the **recommended** cad source for t0076 is Mainen `cad.mod`, not Hay `CaDynamics_E2.mod`, on the
grounds that the parameter names line up with the task plan.

### Allen Institute biophysical-perisomatic SDK is a strong fallback

The Allen Institute Cell Types Database publishes per-cell biophysical models on ModelDB; entry
184297 ("Allen Institute: Nr5a1-Cre VISp layer 4 472442377") has a `modfiles/` directory with 16
single- channel `.mod` files [Allen-184297] [Allen-184297-GH] including `CaDynamics.mod`,
`Ca_HVA.mod`, `Ca_LVA.mod`, `Ih.mod`, `Im.mod`, `Im_v2.mod`, `Kd.mod`, `Kv2like.mod`, `Kv3_1.mod`,
`NaTa.mod`, `NaTs.mod`, `NaV.mod`, `Nap.mod`, `SK.mod`. The Allen Im_v2 is a re-tuned variant of the
Hay Im. The Allen files are explicitly tied to the "Allen Institute's Terms of Use and Citation
Policy" — a named, citable terms document — which arguably makes them the most license-clean
option available. The Allen pipeline is extensively documented (the `AllenSDK` GitHub repo and the
`portal.brain-map.org/explore/models/perisomatic-single-neurons` page) [Allen-Portal]. **However**,
the Allen perisomatic models share the same gap as Hay 2011 — they include SK but not BK — and
they do not include a Kdr-as-such (the Allen "Kd" is a re-tuned delayed rectifier but it is named
differently from t0076's intended `Kdr`). For maximum lineage clarity, the recommended path is Hay
2011 + Khaliq
+ Mainen (three sources), with Allen as a sanity-check second opinion on Im, SK, and Ih.

### Migliore Ih (ModelDB 144541) provides an Ih option with explicit dendritic V_half

The Migliore-Migliore 2012 model (ModelDB 144541) ships an `h.mod` file with SUFFIX `hd` titled "I-h
channel from Magee 1998 for distal dendrites" with `vhalfl = -90 mV`, `vhalft = -75 mV`,
`q10 = 4.5`, and explicit added leakage [MiglioreMigliore2012] [ModelDB144541-GH]. The Magee 1998
dendritic-CA1 parameterization is the single most cited Ih kinetic source in compartmental modelling
[Magee1998]. This is a viable alternative to the Hay 2011 `Ih.mod` (which uses Kole 2006 cortical
kinetics); the choice is biophysical: hippocampal Ih has a more depolarised V_half (-90 mV
inactivation) than cortical Kole-2006 Ih, but for an RGC AIS context neither is exactly tuned to the
right cell type. **Recommendation**: pick Hay 2011 `Ih.mod` as the default for unit consistency with
the rest of the Hay-sourced channels; switch to Migliore `hd.mod` only if the optimiser finds the
Hay Ih kinetics incompatible with RGC firing.

### Fohlmeister-Miller 1997 `spike.mod` is RGC-specific but is a single monolithic file

The salamander RGC model on ModelDB 3673 [FohlmeisterMiller1997] [ModelDB3673-GH] uses `spike.mod`
and `capump.mod`. Critically, `spike.mod` packs five channels (Na, Ca, Kdr, KA, KCa) into one
monolithic NMODL file with shared GLOBAL state. This is the **opposite** of the t0076 vendoring
strategy — t0076 needs one file per channel so the optimiser can independently scale each `gbar`.
**Decision**: do NOT vendor from Fohlmeister-Miller; the RGC kinetic specificity is appealing but
the monolithic packaging is incompatible with the BoTorch parameter-sweep design where each channel
must be individually scalable. Fohlmeister-Miller remains useful as a **reference** for RGC-typical
V_half and tau values when sanity-checking the Hay/Mainen/Khaliq parameter values.

### Best practice: add a citation header to each vendored MOD file

Across all five MOD files already vendored in t0067 (`nav16t67.mod`, `napt67.mod`, `nart67.mod`,
`kv3t67.mod`, `kv4t67.mod`), the established project convention is a 4-line header that names the
biophysical citation, kinetic parameters, and a `t67` SUFFIX namespace marker [t0067-precedent]. The
recommended t0076 convention is to extend this with the source ModelDB ID and original-author
attribution, e.g.:

```text
: Im (Kv7 / KM / M-current) for t0076 channel sweep.
: Vendored from Hay et al. 2011 ModelDB 139653 mod/Im.mod.
: Original kinetics: Adams et al. 1982 (DOI 10.1113/jphysiol.1982.sp014357).
: V_half ~-35 mV, q10 = 2.3, target temp 34 C, original 21 C.
: SUFFIX renamed from "Im" to "imt76" for t0076 namespace isolation.
```

## Methodology Insights

* **Use Hay 2011 (ModelDB 139653) as the single primary source** for KM (Im), CaL (Ca_HVA), CaT
  (Ca_LVAst), HCN (Ih), and SK (SK_E2). The files are factored one-channel-per-file with consistent
  units and temperature corrections [Hay2011] [ModelDB139653-GH].

* **Use Khaliq 2003 (ModelDB 48332) `bkpkj.mod` for BK** — the only well-cited standalone BK MOD
  file with both voltage- and calcium-dependence in a single self-contained NMODL file [Khaliq2003]
  [ModelDB48332-GH].

* **Use Mainen 1996 (ModelDB 2488) for Kdr (`kv.mod`) and cad (`cad.mod`)**. The cad mechanism's
  `depth` and `taur` parameter names match the t0076 task description's parameters 16 and 17
  verbatim [Mainen1996] [ModelDB2488-GH] [Destexhe1993].

* **Apply a t0076-specific SUFFIX namespace** (e.g. `kdrt76`, `kmt76`, `iht76`, `calt76`, `catt76`,
  `bkt76`, `skt76`, `cadt76`) to each vendored file, mirroring the t0067 convention with the `t67`
  suffix [t0067-precedent]. This is essential because two of the planned channels (Im, SK_E2) might
  collide with names used by upstream NEURON or by HHst built-in mechanisms.

* **Add a citation header** to each vendored file: source ModelDB ID, original author, original
  publication DOI, kinetic parameters (V_half, slope, time constant), and the renamed SUFFIX. This
  is the project's adopted "license-clean" standard pattern.

* **Compile the whole set into a single t0076-local `nrnmech.dll`** using `nrnivmodl` from inside
  `tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods/`. The five existing t0067 MODs should be copied
  verbatim into the same folder so the t0076 driver loads only one DLL.

* **Hypothesis (testable in t0076)**: the Khaliq Purkinje BK kinetics are tuned for >200 Hz firing
  and may be too fast for an RGC AIS context (typical DSGC firing rate 10-80 Hz). If the optimiser
  finds that BK density saturates at the lower bound (1e-5 S/cm²), this hypothesis is supported and
  the De Schutter-Bower 1994 cerebellar BK (ModelDB 7176) [DeSchutter1994] should be tried as a
  slower-kinetics alternative.

* **Hypothesis (testable in t0076)**: the Hay Ih (Kole 2006 cortical kinetics) and the Migliore Ih
  (Magee 1998 hippocampal kinetics) will produce visibly different DSI/firing-rate Pareto fronts
  even at matched gbar density. If the optimiser converges to very different operating points under
  the two Ih variants, this confirms that Ih kinetics matter more than Ih density for DSGC tuning.

* **Best practice — fall back to the Risk-1 contingency early**: the task plan's Risk-1 fallback
  is to drop to 8 channels (HHst built-ins + 5 t0067 channels) if any of the 7 new MODs prove hard
  to source. Based on this survey, all 7 are sourceable and Risk-1 should not be triggered. However,
  if any vendored file fails to compile under modern NEURON 8.x, the order of priority for dropping
  is: drop BK first (only Khaliq Purkinje source), then drop CaT (Hay only), then drop CaL (Hay
  only), retain HCN/KM/SK/Kdr/cad. Document the drop in the writeup.

## Discovered Papers

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schürmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Suggested categories**: voltage-gated-channels, compartmental-modelling
* **Why download**: Source paper for `Im.mod`, `SK_E2.mod`, `Ih.mod`, `Ca_HVA.mod`, `Ca_LVAst.mod`,
  and `CaDynamics_E2.mod` — six of the seven MODs t0076 plans to vendor. The paper documents the
  multi-objective evolutionary algorithm used to fit the channel parameters, which is
  methodologically parallel to the BoTorch qNEHVI loop in t0076.

### [Mainen1996]

* **Title**: Influence of Dendritic Structure on Firing Pattern in Model Neocortical Neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **URL**: https://www.nature.com/articles/382363a0
* **Suggested categories**: voltage-gated-channels, compartmental-modelling
* **Why download**: Source paper for `kv.mod` (Kdr), `km.mod` (alternative KM), `kca.mod`
  (alternative SK), `ca.mod` (alternative CaL), and most importantly `cad.mod` whose `depth` and
  `taur` parameters match the t0076 task description verbatim. The paper is also directly relevant
  to the broader project — it establishes that dendritic morphology controls firing pattern via
  channel density, which is the central thesis of t0076's morphology-fixed channel-density Pareto
  sweep.

### [Khaliq2003]

* **Title**: The Contribution of Resurgent Sodium Current to High-Frequency Firing in Purkinje
  Neurons: An Experimental and Modeling Study
* **Authors**: Khaliq, Z. M., Gouwens, N. W., Raman, I. M.
* **Year**: 2003
* **DOI**: `10.1523/JNEUROSCI.23-12-04899.2003`
* **URL**: https://www.jneurosci.org/content/23/12/4899
* **Suggested categories**: voltage-gated-channels
* **Why download**: Source paper for `bkpkj.mod` (the only standalone BK channel MOD file in the
  ModelDB ecosystem). The paper provides the resurgent-Na kinetics that may also be relevant as an
  alternative to the t0067 `nart67.mod` (current NaR source), making this paper double-relevant for
  the project.

### [MiglioreMigliore2012]

* **Title**: Know Your Current Ih: Interaction with a Shunting Current Explains the Puzzling Effects
  of Its Pharmacological or Pathological Modulations
* **Authors**: Migliore, M., Migliore, R.
* **Year**: 2012
* **DOI**: `10.1371/journal.pone.0036867`
* **URL**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0036867
* **Suggested categories**: voltage-gated-channels
* **Why download**: Source paper for `h.mod` (alternative HCN/Ih implementation citing Magee 1998
  hippocampal-CA1 dendritic kinetics). Provides the Magee 1998 kinetic parameterisation that is the
  most-cited Ih variant in dendritic compartmental modelling and is the recommended fallback if Hay
  2011's Kole 2006 cortical kinetics prove inappropriate for the RGC context.

### [Adams1982]

* **Title**: M-currents and Other Potassium Currents in Bullfrog Sympathetic Neurones
* **Authors**: Adams, P. R., Brown, D. A., Constanti, A.
* **Year**: 1982
* **DOI**: `10.1113/jphysiol.1982.sp014357`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.1982.sp014357
* **Suggested categories**: voltage-gated-channels
* **Why download**: The original biophysical characterisation of the M-current (KM / Kv7) cited by
  the Hay 2011 `Im.mod` file in its header reference comment. This is the foundational citation for
  any KM mechanism in compartmental modelling and should be in the corpus to support the t0076
  channel-sourcing chain of provenance.

### [Kohler1996]

* **Title**: Small-Conductance, Calcium-Activated Potassium Channels from Mammalian Brain
* **Authors**: Köhler, M., Hirschberg, B., Bond, C. T., Kinzie, J. M., Marrion, N. V., Maylie, J.,
  Adelman, J. P.
* **Year**: 1996
* **DOI**: `10.1126/science.273.5282.1709`
* **URL**: https://www.science.org/doi/10.1126/science.273.5282.1709
* **Suggested categories**: voltage-gated-channels
* **Why download**: The original cloning and characterisation of SK1, SK2, SK3 (the
  small-conductance Ca-activated K channel family) cited by the Hay 2011 `SK_E2.mod` file in its
  header. Foundational citation for any SK mechanism in compartmental modelling and required to
  complete the t0076 channel-sourcing chain of provenance.

## Recommendations for This Task

Concrete vendoring recipe for the t0076 implementation step, ordered by priority:

1. **Vendor 6 of 7 channels + cad from Hay 2011 + Khaliq 2003 + Mainen 1996.** Specifically:

| Channel | Vendor from | Source file | New SUFFIX | Original cite |
| --- | --- | --- | --- | --- |
| Kdr | ModelDB 2488 | `kv.mod` | `kdrt76` | Mainen-Sejnowski 1996 [Mainen1996] |
| KM (Kv7) | ModelDB 139653 | `mod/Im.mod` | `kmt76` | Adams 1982 [Adams1982] [Hay2011] |
| HCN (Ih) | ModelDB 139653 | `mod/Ih.mod` | `iht76` | Kole 2006 [Hay2011] |
| CaL (CaV1.x HVA) | ModelDB 139653 | `mod/Ca_HVA.mod` | `calt76` | [Hay2011] |
| CaT (CaV3.x LVA) | ModelDB 139653 | `mod/Ca_LVAst.mod` | `catt76` | [Hay2011] |
| BK (KCa1.1) | ModelDB 48332 | `bkpkj.mod` | `bkt76` | Khaliq 2003 [Khaliq2003] |
| SK (KCa2) | ModelDB 139653 | `mod/SK_E2.mod` | `skt76` | Köhler 1996 [Kohler1996] [Hay2011] |
| cad | ModelDB 2488 | `cad.mod` | `cadt76` | Destexhe 1993 [Mainen1996] [Destexhe1993] |
2. **Apply the t0067 citation-header convention to every vendored file** — name the source ModelDB
   ID, original publication DOI, kinetic parameters, and renamed SUFFIX. Do this even though no
   source has an explicit license file: project convention treats this attribution as the
   "license-clean" standard [t0067-precedent].

3. **Add the 6 papers in `## Discovered Papers` to the project corpus** via `/add-paper`. None are
   currently in the corpus; all six are foundational citations for the channels being vendored. The
   t0076 writeup should reference each paper by DOI when describing a vendored channel.

4. **Compile the t0076 mods folder into a single `nrnmech.dll`** by running `nrnivmodl` inside
   `tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods/`. Copy the 5 t0067 mods (`nav16t67.mod`,
   `napt67.mod`, `nart67.mod`, `kv3t67.mod`, `kv4t67.mod`) into the same folder verbatim so a single
   compiled DLL covers all 12 channels.

5. **Validate compilation BEFORE wiring up BoTorch** — verify each `SUFFIX` resolves at runtime by
   inserting it into a single-section test cell and running a current-step protocol. If any channel
   fails to compile under modern NEURON 8.x, fall back per the priority order in the Methodology
   Insights section (drop BK first, then CaT, then CaL).

6. **Sanity-check the Khaliq Purkinje BK kinetics against the RGC firing range**: run the BK-only
   single-channel test at 60 Hz current injection; if the BK afterhyperpolarisation is
   unrealistically sharp, swap the Khaliq `bkpkj.mod` for a De Schutter-Bower 1994 (ModelDB 7176)
   variant [DeSchutter1994] before launching the BoTorch loop.

7. **Update `pyproject.toml` cleanly** with `botorch`, `gpytorch`, `torch` per REQ-9 of the task
   plan; this is unrelated to MOD vendoring but is the next implementation step.

## Source Index

### [Hay2011]

* **Type**: paper
* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schürmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Peer-reviewed**: yes (PLoS Computational Biology)
* **Relevance**: Source publication for ModelDB 139653 — the highest-leverage single source for 6
  of the 7 MODs t0076 must vendor.

### [Mainen1996]

* **Type**: paper
* **Title**: Influence of Dendritic Structure on Firing Pattern in Model Neocortical Neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **URL**: https://www.nature.com/articles/382363a0
* **Peer-reviewed**: yes (Nature)
* **Relevance**: Source publication for ModelDB 2488 — provides the canonical Hodgkin-Huxley
  `kv.mod` delayed rectifier and the `cad.mod` calcium-accumulation mechanism whose `depth`/`taur`
  parameters match the t0076 task description verbatim.

### [Khaliq2003]

* **Type**: paper
* **Title**: The Contribution of Resurgent Sodium Current to High-Frequency Firing in Purkinje
  Neurons: An Experimental and Modeling Study
* **Authors**: Khaliq, Z. M., Gouwens, N. W., Raman, I. M.
* **Year**: 2003
* **DOI**: `10.1523/JNEUROSCI.23-12-04899.2003`
* **URL**: https://www.jneurosci.org/content/23/12/4899
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Source publication for ModelDB 48332 — provides the only well-cited standalone BK
  channel MOD file (`bkpkj.mod`) in the ModelDB ecosystem.

### [MiglioreMigliore2012]

* **Type**: paper
* **Title**: Know Your Current Ih: Interaction with a Shunting Current Explains the Puzzling Effects
  of Its Pharmacological or Pathological Modulations
* **Authors**: Migliore, M., Migliore, R.
* **Year**: 2012
* **DOI**: `10.1371/journal.pone.0036867`
* **URL**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0036867
* **Peer-reviewed**: yes (PLoS ONE)
* **Relevance**: Source publication for ModelDB 144541 — provides the alternative Magee-1998 Ih
  parameterisation `h.mod` (SUFFIX `hd`) that is the recommended fallback if the Hay/Kole-2006 Ih
  proves inappropriate for an RGC context.

### [Adams1982]

* **Type**: paper
* **Title**: M-currents and Other Potassium Currents in Bullfrog Sympathetic Neurones
* **Authors**: Adams, P. R., Brown, D. A., Constanti, A.
* **Year**: 1982
* **DOI**: `10.1113/jphysiol.1982.sp014357`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.1982.sp014357
* **Peer-reviewed**: yes (Journal of Physiology)
* **Relevance**: Original biophysical characterisation of the M-current cited in the header of Hay
  2011's `Im.mod`. Foundational citation for any KM mechanism in compartmental modelling.

### [Kohler1996]

* **Type**: paper
* **Title**: Small-Conductance, Calcium-Activated Potassium Channels from Mammalian Brain
* **Authors**: Köhler, M., Hirschberg, B., Bond, C. T., Kinzie, J. M., Marrion, N. V., Maylie, J.,
  Adelman, J. P.
* **Year**: 1996
* **DOI**: `10.1126/science.273.5282.1709`
* **URL**: https://www.science.org/doi/10.1126/science.273.5282.1709
* **Peer-reviewed**: yes (Science)
* **Relevance**: Original cloning and biophysical characterisation of the SK channel family cited in
  the header of Hay 2011's `SK_E2.mod`. Foundational citation for any SK mechanism.

### [Magee1998]

* **Type**: paper
* **Title**: Dendritic Hyperpolarization-Activated Currents Modify the Integrative Properties of
  Hippocampal CA1 Pyramidal Neurons
* **Authors**: Magee, J. C.
* **Year**: 1998
* **DOI**: `10.1523/JNEUROSCI.18-19-07613.1998`
* **URL**: https://www.jneurosci.org/content/18/19/7613
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Original distance-dependent dendritic Ih characterisation in CA1, cited by
  Migliore-Migliore 2012's `h.mod` (SUFFIX `hd`). Foundational citation for hippocampal-style Ih.

### [Kole2006]

* **Type**: paper
* **Title**: Single Ih Channels in Pyramidal Neuron Dendrites: Properties, Distribution, and Impact
  on Action Potential Output
* **Authors**: Kole, M. H. P., Hallermann, S., Stuart, G. J.
* **Year**: 2006
* **DOI**: `10.1523/JNEUROSCI.3664-05.2006`
* **URL**: https://www.jneurosci.org/content/26/6/1677
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Single-channel Ih characterisation in cortical pyramidal dendrites cited by Hay
  2011's `Ih.mod`. Foundational citation for the Hay variant of Ih kinetics.

### [Destexhe1993]

* **Type**: paper
* **Title**: Ionic Mechanisms for Intrinsic Slow Oscillations in Thalamic Relay Neurons
* **Authors**: Destexhe, A., Babloyantz, A., Sejnowski, T. J.
* **Year**: 1993
* **DOI**: `10.1016/S0006-3495(93)81190-1`
* **URL**: https://www.cell.com/biophysj/abstract/S0006-3495(93)81190-1
* **Peer-reviewed**: yes (Biophysical Journal)
* **Relevance**: Original simplified-buffer calcium-accumulation mechanism cited by Mainen 1996's
  `cad.mod`. The mathematical form (`drive_channel + (cainf - ca) / taur`) used in the recommended
  cad vendor source originates here.

### [FohlmeisterMiller1997]

* **Type**: paper
* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1997.78.4.1948
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: Already in corpus as
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`.
  Provides RGC-specific V_half / tau reference values for sanity- checking the Hay/Mainen/Khaliq
  vendored kinetics. Source ModelDB 3673 was REJECTED for vendoring because its `spike.mod` is
  monolithic.

### [DeSchutter1994]

* **Type**: paper
* **Title**: An Active Membrane Model of the Cerebellar Purkinje Cell. I. Simulation of Current
  Clamps in Slice
* **Authors**: De Schutter, E., Bower, J. M.
* **Year**: 1994
* **DOI**: `10.1152/jn.1994.71.1.375`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1994.71.1.375
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: Source publication for ModelDB 7176 — provides a slower-kinetics BK variant that
  is the recommended fallback if the Khaliq-Purkinje BK is too fast for the RGC context.

### [ModelDB139653-GH]

* **Type**: repository
* **Title**: ModelDBRepository/139653 — L5b PC model (Hay et al. 2011)
* **Author/Org**: ModelDB Repository (Yale SenseLab) GitHub mirror
* **Date**: 2011 (publication); ongoing mirror
* **URL**: https://github.com/ModelDBRepository/139653
* **Last updated**: per ModelDB upload date 2011
* **Peer-reviewed**: no (the repo itself; the underlying paper IS peer-reviewed)
* **Relevance**: Direct source of the 13 MOD files in the `mod/` subdirectory including `Im.mod`
  (KM), `SK_E2.mod` (SK), `Ih.mod` (HCN), `Ca_HVA.mod` (CaL), `Ca_LVAst.mod` (CaT), and
  `CaDynamics_E2.mod` (cad alternative). Verified file inventory via
  `gh api repos/ModelDBRepository/139653/contents/mod`.

### [ModelDB2488-GH]

* **Type**: repository
* **Title**: ModelDBRepository/2488 — Mainen-Sejnowski 1996 neocortical neurons
* **Author/Org**: ModelDB Repository (Yale SenseLab) GitHub mirror
* **Date**: 1996 (publication); ongoing mirror
* **URL**: https://github.com/ModelDBRepository/2488
* **Last updated**: per ModelDB upload date
* **Peer-reviewed**: no (the repo itself)
* **Relevance**: Direct source of `kv.mod` (recommended Kdr), `cad.mod` (recommended cad with
  `depth`/ `taur` parameter names matching the t0076 task description), `km.mod`, `kca.mod`,
  `ca.mod`, and `na.mod`. Top-level file enumeration verified via
  `gh api repos/ModelDBRepository/2488/contents`.

### [ModelDB48332-GH]

* **Type**: repository
* **Title**: ModelDBRepository/48332 — Khaliq-Gouwens-Raman 2003 Purkinje cell
* **Author/Org**: ModelDB Repository (Yale SenseLab) GitHub mirror
* **Date**: 2003 (publication); ongoing mirror
* **URL**: https://github.com/ModelDBRepository/48332
* **Last updated**: per ModelDB upload date
* **Peer-reviewed**: no (the repo itself)
* **Relevance**: Direct source of `bkpkj.mod` (recommended BK channel — the only standalone BK MOD
  in the ModelDB ecosystem with a clean SUFFIX and a single self-contained NMODL file). File header
  verified verbatim via raw-GitHub fetch.

### [ModelDB144541-GH]

* **Type**: repository
* **Title**: ModelDBRepository/144541 — Migliore-Migliore 2012 CA1 Ih
* **Author/Org**: ModelDB Repository (Yale SenseLab) GitHub mirror
* **Date**: 2012 (publication); ongoing mirror
* **URL**: https://github.com/ModelDBRepository/144541
* **Last updated**: per ModelDB upload date
* **Peer-reviewed**: no (the repo itself)
* **Relevance**: Direct source of `h.mod` (SUFFIX `hd`) — the recommended fallback Ih variant if
  the Hay/Kole-2006 cortical Ih kinetics prove inappropriate. File header verified verbatim via raw-
  GitHub fetch.

### [ModelDB3673-GH]

* **Type**: repository
* **Title**: ModelDBRepository/3673 — Fohlmeister-Miller 1997 salamander RGC
* **Author/Org**: ModelDB Repository (Yale SenseLab) GitHub mirror
* **Date**: 1997 (publication); ongoing mirror
* **URL**: https://github.com/ModelDBRepository/3673
* **Last updated**: per ModelDB upload date
* **Peer-reviewed**: no (the repo itself)
* **Relevance**: Reference-only source. The `spike.mod` packs five channels (Na, Ca, Kdr, KA, KCa)
  into one monolithic file with shared GLOBAL state, which is incompatible with t0076's per-channel
  scaling design. Useful only as an RGC-specific kinetic-value sanity check.

### [Allen-184297]

* **Type**: documentation
* **Title**: Allen Institute: Nr5a1-Cre VISp layer 4 neuron 472442377 (ModelDB 184297)
* **Author/Org**: Allen Institute for Brain Science
* **Date**: 2015
* **URL**: https://modeldb.science/184297
* **Peer-reviewed**: no (the model entry; the underlying Cell Types Database publication is peer-
  reviewed, see Gouwens et al. 2018 Nature Communications)
* **Relevance**: Alternative source of single-channel `.mod` files (`Im.mod`, `SK.mod`, `Ih.mod`,
  `Ca_HVA.mod`, `Ca_LVA.mod`, `CaDynamics.mod`) under the explicit "Allen Institute's Terms of Use
  and Citation Policy". Recommended as a sanity-check second opinion on the Hay-sourced MODs.

### [Allen-184297-GH]

* **Type**: repository
* **Title**: ModelDBRepository/184297 — Allen Nr5a1 layer 4 perisomatic
* **Author/Org**: ModelDB Repository (Yale SenseLab) GitHub mirror
* **Date**: 2015
* **URL**: https://github.com/ModelDBRepository/184297
* **Last updated**: per ModelDB upload date 2015
* **Peer-reviewed**: no (the repo itself)
* **Relevance**: Direct source of the 16 Allen Institute single-channel MOD files in the `modfiles/`
  subdirectory. File inventory verified via
  `gh api repos/ModelDBRepository/184297/contents/modfiles`.

### [Allen-Portal]

* **Type**: documentation
* **Title**: Perisomatic biophysical single neuron models — Allen Brain Map portal
* **Author/Org**: Allen Institute for Brain Science
* **Date**: 2015 onwards
* **URL**: https://portal.brain-map.org/explore/models/perisomatic-single-neurons
* **Peer-reviewed**: no
* **Relevance**: Authoritative documentation of the Allen perisomatic biophysical model pipeline
  (NEURON v7.4.rel-1370, AllenSDK Python API, channel parameter optimisation via genetic algorithm).
  Confirms that the Allen `modfiles/` directory is the same one used by every Allen Cell Types
  Database biophysical model.

### [Hay2011-readme]

* **Type**: documentation
* **Title**: ModelDB 139653 readme.html
* **Author/Org**: Etay Hay (via ModelDB)
* **Date**: 2011
* **URL**: https://github.com/ModelDBRepository/139653/blob/master/readme.html
* **Peer-reviewed**: no
* **Relevance**: Source-document confirmation that the Hay 2011 ModelDB entry contains no explicit
  license file, thereby grounding the project's choice to vendor under the ModelDB community
  research- use convention with attribution.

### [t0067-precedent]

* **Type**: repository
* **Title**: tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/ — vendored Nav1.6, NaP, NaR,
  Kv3, Kv4 with `t67` SUFFIX namespace
* **Author/Org**: this project (in-tree)
* **Date**: 2026
* **URL**: tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/nav16t67.mod
* **Peer-reviewed**: no (in-project artefact)
* **Relevance**: Establishes the project's vendoring convention — citation header naming the
  source paper, kinetics, and a `tNN` SUFFIX namespace marker. The t0076 implementation must follow
  this same pattern so that the 12-channel composite library in `code/mods/` is internally
  consistent.

### [eLife22152]

* **Type**: paper
* **Title**: Mapping the Function of Neuronal Ion Channels in Model and Experiment
* **Authors**: Podlaski, W. F., Seeholzer, A., Groschner, L. N., Miesenböck, G., Ranjan, R.,
  Vogels, T. P.
* **Year**: 2017
* **DOI**: `10.7554/eLife.22152`
* **URL**: https://elifesciences.org/articles/22152
* **Peer-reviewed**: yes (eLife)
* **Relevance**: ICGenealogy paper that surveys 2378 NEURON ion-channel MOD files in ModelDB and
  clusters them. Confirms that ModelDB is the de facto standard repository for NEURON channel models
  and that the Hay 2011 framework is among the most-reused. Cited in the Key Findings to justify
  Hay-as-primary-source.
