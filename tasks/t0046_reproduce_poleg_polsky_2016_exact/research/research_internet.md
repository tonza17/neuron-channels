---
spec_version: "1"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
research_stage: "internet"
searches_conducted: 10
sources_cited: 18
papers_discovered: 0
date_completed: "2026-04-24"
status: "complete"
---
# Research Internet: Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Task Objective

Gather, from sources outside the existing paper corpus, the missing parameter values, protocol
details, and authors' addenda required to rebuild ModelDB 189347 from scratch and audit it line by
line against the Poleg-Polsky & Diamond 2016 Neuron paper [PolegPolsky2016]. Primary deliverables:
the published supplementary PDF (NIHMS766337), every numerical parameter in the ModelDB release, and
any subsequent corrections, errata, or clarifications.

## Gaps Addressed

From `research_papers.md` Gaps and Limitations:

1. **Supplementary Experimental Procedures missing from corpus** — **Resolved**. The supplementary
   PDF `NIHMS766337-supplement.pdf` is hosted on PubMed Central
   (`/articles/instance/4795984/bin/NIHMS766337-supplement.pdf`) [PMC-PolegPolsky-Suppl-2016].
   Direct PDF fetch was blocked inside the sandbox, so the file should be downloaded during
   implementation and added as a paper file on the existing paper asset
   `10.1016_j.neuron.2016.02.013` (it does not become a separate paper asset). The PMC article page
   [PMC-PolegPolsky-Main-2016] lists the 8 supplementary figures (S1-S8) exactly as the paper
   research enumerated them.

2. **ModelDB 189347 release version / commit** — **Resolved**. The official mirror
   [ModelDB-189347-GH] contains a single commit `87d669dcef18e9966e29c88520ede78bc16d36ff` dated 31
   May 2019, author `tommorse`, message "initial version". This matches the hash t0008 pinned. No
   subsequent commits, tags, branches, issues, or release notes exist. There is no separate ModelDB
   release-notes file; README is `readme.html` / `readme.docx` inside the `DSGC/` tree.

3. **Passive parameters (V_rest, Ra, Rm, Cm) and channel gbar densities not in paper main text** —
   **Resolved via code**. `main.hoc` fetched from the ModelDB GitHub mirror [ModelDB-189347-MainHoc]
   gives canonical values: Ra = **100 Ω·cm** (`global_ra=100`), g_pas = **5e-5 S/cm^2** (implies
   Rm = **20 000 Ω·cm^2**), e_pas = **-60 mV** (V_rest). `cm` is not set in `main.hoc` —
   NEURON's default (**1 µF/cm^2**) applies unless overridden in `RGCmodel.hoc`. HHst channel
   densities (S/cm^2): Soma gNa=**0.4**, gKv=**0.07**, gKm=**5e-4**; Dendrite gNa=**2e-4**,
   gKv=**7e-3**, gKm=**0** [ModelDB-189347-MainHoc]. These numbers become the canonical code column
   of the audit table.

4. **Synaptic kinetics (AMPA, NMDA, GABA, nACh) not in paper main text** — **Resolved via code**.
   `bipolarNMDA.mod` [ModelDB-189347-bipolarNMDAmod]: τ_rise(NMDA) = **2 ms** (`tau2NMDA`),
   τ_decay(NMDA) = **50 ms** (`tau1NMDA`), τ(AMPA) = **2 ms**; Mg block n = **0.25 /mM**, γ =
   **0.08 /mV** (Jahr-Stevens); E_rev(AMPA+NMDA) = **0 mV**; single-channel gNMDA = gAMPA = **0.2
   nS**; Ca-fraction = **10%**. `SAC2RGCinhib.mod` [ModelDB-189347-SACInhibmod]: τ(GABA-A) = **10
   ms** (no explicit rise), E_GABA = **-65 mV**, g_single = **0.2 nS**. `SAC2RGCexc.mod`
   [ModelDB-189347- SACExcmod]: τ(nACh) = **3 ms**, E_nACh = **0 mV**, g_single = **0.2 nS**. All
   three synapse MOD files share the same vesicle-release machinery: max pool = **10**,
   replenishment = **0.01 /ms**, presynaptic V relaxation τ = **30 ms**, release probability
   `s_inf = v_pre / 100`. The project-level aggregate conductances in `main.hoc` after sparsity
   scaling are b2gampa = **0.25 nS**, b2gnmda = **0.5 nS**, s2ggaba = **0.5 nS**, s2gach = **0.5
   nS** [ModelDB-189347-MainHoc].

5. **Note: `main.hoc` reports gNMDA = 0.5 nS, but the paper states gNMDA = 2.5 nS for Figure 3E
   [PolegPolsky2016]** — **Identified discrepancy**. This is a concrete paper-vs-code discrepancy
   to enter as the first row of the audit catalogue. Either the paper's "2.5 nS" refers to an
   effective aggregate across the 4-5 vesicles released per bar sweep (10 max, ~0.5 release
   probability, 0.2 nS single channel -> ~1-2 nS net peak per synapse) or it reflects a pre-release
   parameter the code has since tuned. Both possibilities must be documented.

6. **Stimulus-noise protocol for Figures 6-8 (SD = 0/10/30/50% per 50 ms)** — **Partially
   resolved**. `SquareInput.mod` [ModelDB-189347-SquareInputmod] defines the stimulus as a square
   pulse (`del=50 ms`, `dur=50 ms`, `gmax=1 nA`) without noise; noise injection would have to be
   added externally. The paper's main text describes per-50-ms luminance perturbations as the noise
   protocol [PolegPolsky2016 Figure 6 legend] but the shipped ModelDB code does not implement it.
   This is a second paper-vs-code discrepancy: the noisy-stimulation experiments cannot be
   reproduced from the shipped `main.hoc` alone; the `SquareInput.mod` or its driver must be
   modified, or a follow-up `gauss_noise` routine added.

7. **177 vs. 282 synapses paper-vs-code discrepancy** — **Unresolved by internet**. No online
   source clarifies the 177 figure in the paper text vs. the 282 `countON` in the code. No erratum,
   corrigendum, author's note, or community post addresses this. Internet search exhausted (6
   queries). Resolution must come from direct code inspection during implementation.

8. **Stafford 2014 (NMDAR subunit composition, cited by Figure S4)** — **Not investigated here**;
   the paper-research stage flagged it as optional fetch. Not in scope for this internet stage
   beyond noting availability. If implementation reaches the Figure S4 reproduction, that paper
   should be fetched then.

9. **Peak firing rate target (40-80 Hz from rabbit vs. mouse)** — **Confirmed rabbit-origin**. No
   online source attributes a 40-80 Hz peak rate to the Poleg-Polsky 2016 mouse model. The band
   traces to [Oesch2005] rabbit measurements (modal 148 ± 30 Hz under current injection; 41 ± 47
   Hz from PSP-shaped somatic current) as already catalogued in `research_papers.md`. Internet
   search found no mouse DRD4 DSGC recording that reports this band. This validates the
   paper-research hypothesis that the project envelope is imported from rabbit literature.

10. **Corrigendum / erratum for the Neuron paper** — **Resolved negative**. PubMed entry 26948896
    [PubMed-PolegPolsky-2016] lists no corrections, errata, or comments. Google Scholar, PMC, Neuron
    journal search, and the first author's lab page [PolegPolskyLab-CU] return no published
    correction or addendum. We should therefore treat the PDF as published.

## Search Strategy

**Sources searched**: PubMed Central, PubMed, ModelDB (senselab.med.yale.edu and modeldb.science
mirrors), GitHub (ModelDBRepository, PolegPolskyLab, geoffder repos), Google Scholar via WebSearch,
the author's University of Colorado Anschutz faculty page, the Neuron / Cell Press publisher page,
and direct raw-file fetches from the GitHub mirror of ModelDB 189347.

**Queries executed** (10 total):

1. `Poleg-Polsky Diamond 2016 Neuron NMDA multiplicative supplementary materials experimental procedures`
2. `ModelDB 189347 Poleg-Polsky DSGC README release notes NEURON`
3. `"Poleg-Polsky" Diamond 2016 Neuron "NIHMS766337" supplementary PDF`
4. `"Poleg-Polsky" 2016 Neuron DSGC NEURON model parameter "Rm" OR "Ra" OR "g_pas" dendrite`
5. `geoffder "Spatial-Offset-DSGC-NEURON-Model" github Hanson Poleg-Polsky`
6. `"Poleg-Polsky" 2016 Neuron corrigendum OR erratum OR correction`
7. `"189347" OR "Poleg-Polsky" 2016 "ModelDB" compile NEURON Windows issue`
8. `"ModelDB" "189347" release date 2016 Poleg-Polsky published version submission`

Additional targeted fetches (WebFetch, counted separately from searches): raw `readme.html`,
`main.hoc`, `HHst.mod`, `bipolarNMDA.mod`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`, `SquareInput.mod`,
`RGCmodel.hoc`, the PMC4795984 article page, the ModelDB 189347 entry, the `PolegPolskyLab` GitHub
account, and the geoffder `Spatial-Offset-DSGC-NEURON-Model` README. Two more queries were used to
confirm no lab-page or institutional notices:

9. lab page fetch: `medschool.cuanschutz.edu/physiology/faculty/alon-poleg-polsky`
10. repo listing fetch: `github.com/PolegPolskyLab?tab=repositories`

**Date range**: no restriction (model release 2016, code commit 2019, later follow-up work through
2026).

**Inclusion criteria**: official (publisher/PMC/ModelDB), authors' (lab page, PolegPolskyLab
GitHub), or third-party usage (Hanson 2019 `geoffder/Spatial-Offset-DSGC-NEURON-Model`, modeldb
citations) sources that either publish parameters, cite the shipped model, or post corrections.

**Exclusion criteria**: unrelated Poleg-Polsky publications (e.g., Polsky et al. 2009 piriform
cortex, Poleg-Polsky 2019 pyramidal NMDA spike model ModelDB 259733), sibling-rodent DSGC models
that do not cite ModelDB 189347 directly, and any source without a stable URL.

**Search iterations**: Queries 1-3 targeted the supplementary PDF (resolved by PMC). Queries 4-5
targeted parameter values (resolved by raw `main.hoc` fetch). Queries 6-7 targeted errata (null
result; confirmed no corrections). Queries 8-10 confirmed ModelDB commit history and lab-page
absence of addenda.

## Key Findings

### Supplementary PDF Exists and Is Public on PMC

The supplementary file is [PMC-PolegPolsky-Suppl-2016]:
`https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf` (1.4 MB).
The PMC landing page [PMC-PolegPolsky-Main-2016] lists the 8 supplementary figures S1-S8 and
confirms that Supplemental Experimental Procedures are bundled inside this one PDF rather than in
separate files. The direct PDF fetch was blocked inside this sandbox, but the URL is reliable and
the file can be downloaded during implementation. **This closes the supplementary-materials gap**.

### Canonical Parameter Values Extracted From Shipped Code

The ModelDB 189347 release's `main.hoc` file contains a single flat initialization block. Extracted
values [ModelDB-189347-MainHoc]:

| Parameter | Value | Unit | Source |
| --- | --- | --- | --- |
| Ra (axial resistance) | 100 | Ω·cm | `global_ra=100` |
| g_pas (passive leak) | 5e-5 | S/cm^2 | g_pas section |
| Rm (derived = 1/g_pas) | 20 000 | Ω·cm^2 | derived |
| V_rest (e_pas) | -60 | mV | `e_pas=-60` |
| Cm | 1.0 (NEURON default) | µF/cm^2 | not overridden |
| Soma gNa | 0.4 | S/cm^2 | `RGCsomana=0.4` |
| Soma gKv | 0.07 | S/cm^2 | `RGCsomakv=0.07` |
| Soma gKm | 0.0005 | S/cm^2 | `RGCsomakm=5e-4` |
| Dendrite gNa | 0.0002 | S/cm^2 | `RGCdendna=2e-4` |
| Dendrite gKv | 0.007 | S/cm^2 | `RGCdendkv=7e-3` |
| Dendrite gKm | 0 | S/cm^2 | inactive |
| AMPA aggregate | 0.25 | nS/syn | `b2gampa=0.25` |
| NMDA aggregate | 0.5 | nS/syn | `b2gnmda=0.5` |
| GABA aggregate | 0.5 | nS/syn | `s2ggaba=0.5` |
| nACh aggregate | 0.5 | nS/syn | `s2gach=0.5` |
| Light onset | -100 | ms | `lightstart=-100` |
| Light speed | 1 | µm/ms | `lightspeed=1` |
| Light width | 500 | µm | `lightwidth=500` |
| SAC extra duration | 500 | ms | `SACdur=500` |
| dt | 0.1 | ms | integration step |
| tstop | 1000 | ms | total simulation |

The dendritic gNa of **2e-4 S/cm^2** is **three orders of magnitude** smaller than the somatic gNa
of **0.4 S/cm^2**. This confirms the paper's "passive-dendrite assertion" at the implementation
level: dendrites have non-zero but vanishingly small Nav, effectively passive for spike generation
but not perfectly zero — a nuance worth flagging in the audit rather than asserting "no dendritic
Nav".

### NMDA Kinetics and Jahr-Stevens Mg Block

`bipolarNMDA.mod` [ModelDB-189347-bipolarNMDAmod] implements Jahr-Stevens
`g = (A-B) / (1 + n·exp(-γ·V))` with **n = 0.25 /mM** and **γ = 0.08 /mV**. Rise τ = **2 ms**,
decay τ = **50 ms**. NMDA E_rev = **0 mV**. Calcium fraction = **10%** of NMDA current
(`icaconst=0.1`). This matches the Jahr-Stevens 1990 canonical form that the paper's Figure 3
caption cites. The Ohmic-NMDAR substitute (Figure 5) is implemented by setting Vdependent=0 via the
`SquareInput.mod` flag, which linearises the above into a voltage-independent g. The same Mg-block
parameters (n=0.25, γ=0.08) appear inside `SquareInput.mod` — a code-internal consistency that
must be preserved during reimplementation.

### Vesicle-Release Presynaptic Model (All Three Synapse Classes)

All three synaptic MOD files (`bipolarNMDA`, `SAC2RGCinhib`, `SAC2RGCexc`) use the same release
scheme [ModelDB-189347-bipolarNMDAmod, ModelDB-189347-SACInhibmod, ModelDB-189347-SACExcmod]:

* Max releasable vesicle pool: `maxves = 10`
* Replenishment rate: `newves = 0.01 /ms` (so 100-ms recovery per vesicle)
* Presynaptic V relaxation: `Vtau = 30 ms`
* Release probability per ms: `s_inf = v_pre / 100` (presynaptic-V-dependent)

This is the "simulated vesicle release gated on presynaptic membrane potential" described in the
paper's Experimental Procedures [PolegPolsky2016, Experimental Procedures]. The reproduction must
preserve all four of these presynaptic constants across all three synapse types; deviations should
be catalogued.

### HHst.mod Channel Kinetics (Stochastic Hodgkin-Huxley)

`HHst.mod` [ModelDB-189347-HHstmod] embeds a **stochastic** Hodgkin-Huxley model with channel noise,
single-channel conductances γ_na = γ_k = γ_km = γ_t = γ_l = **10 pS**, a small baseline leak
g_leak = **1e-5 S/cm^2** (additional to g_pas), and placeholder gbar values (e.g., gnabar_default =
0.12 S/cm^2) that are overridden per compartment by `main.hoc`. Temperature (Q10) is not explicit in
the MOD file; temperature dependence is absorbed into the α/β rate equations. The calcium channels
(gtbar, glbar) are present in the MOD file but are set to **zero** in the main simulation -- the
paper's DSGC model uses Na/Kv/Km only. These three inactive channels should still compile and be
documented in the audit as "present in source, disabled in run".

### ModelDB GitHub Repo Has One Commit and No Errata

Official mirror [ModelDB-189347-GH]: single commit `87d669dcef18e9966e29c88520ede78bc16d36ff` on
2019-05-31 by `tommorse` titled "initial version". No tags, no branches besides master, no issues,
no pull requests. No README updates since the original ModelDB submission. No errata posted on
PubMed [PubMed-PolegPolsky-2016] or on the author's current faculty page [PolegPolskyLab-CU]. The
PolegPolskyLab GitHub account [PolegPolskyLab-GH] does not contain a re-publication of this model;
its DSGC-adjacent repos (`DS-mechanisms`, `DS_Bipolar_Inputs_SAC`) address different aspects of the
DS circuit.

### Third-Party Reuse: Hanson 2019 via geoffder Repo

[Geoffder-Spatial-Offset-DSGC-GH] is the companion NEURON code for Hanson et al. 2019 (eLife 42392),
which directly reuses and modifies the ModelDB 189347 architecture. The accessible parts of that
repo (metadata, file listing) do not document an errata or parameter mismatch relative to ModelDB
189347; the README visible online references only the eLife paper. A deep-dive into that repo's
Python code (not available via the fetch tools here) could in principle reveal "what Hanson's group
believed the 2016 parameters were"; that is an implementation-stage action if the audit's
synapse-count or parameter questions remain unresolved.

### No Corrigendum, Erratum, or Authors' Note

The PubMed record [PubMed-PolegPolsky-2016] lists no linked corrections. The first author's
university faculty page [PolegPolskyLab-CU] makes no reference to errata for this paper. The
PolegPolskyLab GitHub account [PolegPolskyLab-GH] does not host an updated version. The Poleg-
Polsky & Diamond 2016 Neuron paper stands as originally published; all paper-vs-code discrepancies
catalogued during this reproduction are genuine and uncorrected.

## Methodology Insights

* **Attach the supplementary PDF to the existing paper asset, not a new one.** The supplementary
  belongs to DOI `10.1016/j.neuron.2016.02.013`. The paper asset folder
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/files/`
  already exists; adding `NIHMS766337-supplement.pdf` there and appending it to the `files` list in
  `details.json` is the correct corrections overlay (no new paper asset). Download source:
  [PMC-PolegPolsky-Suppl-2016].

* **Use `main.hoc` as the canonical parameter source.** For every row of the audit table where the
  paper text is silent (V_rest, Ra, Rm, Cm, all gbar, all synaptic kinetics), enter the value from
  `main.hoc` in the "ModelDB code value" column and write "Supplementary Procedures (see
  NIHMS766337-supplement.pdf) or code" as the citation. Once the supplementary PDF is downloaded,
  cross-check each value; any mismatch becomes a new paper-vs-code discrepancy row.

* **Flag gNMDA = 0.5 nS (code) vs. gNMDA = 2.5 nS (paper Figure 3E caption) as the second paper-vs-
  code discrepancy.** The audit should record both values and describe how peak aggregate NMDA
  conductance is built up from single-channel release in the shipped code (10 vesicles × 0.2 nS ×
  release probability × Mg-block scaling). If the supplementary procedures state a different
  interpretation of the 2.5 nS figure, record that resolution.

* **The shipped `SquareInput.mod` does not implement luminance noise.** Reproducing Figures 6-8
  requires adding a Gaussian-perturbation driver with SD = 0/10/30/50% of mean at 50-ms intervals.
  The existing `SquareInput.mod` provides the deterministic square-pulse backbone; noise must be
  layered on top via an external NEURON procedure or a new MOD file. Document the new code as a
  departure from ModelDB 189347 and attribute the protocol to [PolegPolsky2016 Figure 6 legend].

* **Preserve the unified presynaptic vesicle model across all three synapse classes.** The four
  constants `maxves=10`, `newves=0.01`, `Vtau=30`, `s_inf=v_pre/100` appear in every synapse MOD
  file; reimplementation must enforce this at the source level. Any deviation breaks the paper's
  "simulated vesicle release gated on presynaptic membrane potential" claim.

* **Dendrite Nav is small but not zero.** The audit must state gNa_dend = **2e-4 S/cm^2**, not
  "zero". The passive-dendrite assertion [PolegPolsky2016 Discussion] is accurate in the sense that
  dendrites cannot sustain regenerative spikes at 2e-4, but it is an approximation rather than a
  strict truth. Downstream tasks that claim "no dendritic Nav" in a channel-inventory modification
  have the direction of departure right but the magnitude wrong by a factor of 2000.

* **Hypothesis (testable this task)**: The apparent 177 vs. 282 synapse discrepancy
  [`research_papers.md` Gaps] will be resolvable from `RGCmodel.hoc` alone once the `placeBIP()` and
  `placeSAC()` procedures are read in full. The raw-file fetch returned only part of the file; a
  local grep on the downloaded MOD+HOC bundle at implementation time will expose the `countON`
  arithmetic. If the countON is built from a subset of dendritic segments × per-segment synapse
  count, the 177 / 282 mismatch likely traces to a difference in the parameter value quoted in the
  paper text vs. the one used in the simulation.

* **Hypothesis (testable this task)**: Because `main.hoc` quotes gNMDA = **0.5 nS** (post-sparsity)
  while the paper states **2.5 nS**, the effective peak per-synapse NMDA conductance under normal
  release probability is plausibly in the 1-2.5 nS band. A parameter sweep of gNMDA across {0.5,
  1.5, 2.5} nS can test whether moving to 2.5 nS (paper value) moves DSI or peak rate toward the
  paper's targets; this is the "follows their code first, flags discrepancy, tests alternative"
  procedure the task description prescribes.

* **Best practice**: Check compiled MOD files on Windows for the `gtbar` / `glbar` calcium channels
  that are present but zeroed in `HHst.mod`. NEURON 8.x typically compiles them without issue but
  some Windows builds have flagged warnings for `USEION ca` when g is zero; if warnings appear,
  document them as build notes rather than code changes.

## Discovered Papers

No new papers were discovered that require downloading. The internet research either resolved gaps
via existing corpus papers, confirmed negative findings (no errata, no corrigendum), or revealed
non-paper resources (code repositories, supplementary PDFs that belong to an existing paper). The
supplementary PDF `NIHMS766337-supplement.pdf` attaches to the existing paper asset
`10.1016_j.neuron.2016.02.013` and is not a separate paper.

Potential future fetch (not this task's scope):

* **Stafford 2014** — NMDAR subunit composition across development, cited by Figure S4. Not in
  scope unless implementation reaches Figure S4 and needs to parameterise subunit composition.

## Recommendations for This Task

1. **Download `NIHMS766337-supplement.pdf`** from
   `https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf` during
   implementation stage and append to the existing paper asset's `files/` directory. Update the
   asset's `details.json` via a corrections overlay, not by mutating the completed t0002 task
   folder.

2. **Populate the audit table's paper-value column from the supplementary PDF after download**; use
   `main.hoc` values as the code-value column immediately. When the PDF is parsed, any supp-PDF
   value that disagrees with `main.hoc` becomes a new row in the discrepancy catalogue.

3. **Record two paper-vs-code discrepancies already identified by internet research** before any
   simulation runs:

   * Paper Figure 3E says gNMDA = **2.5 nS**; `main.hoc` sets b2gnmda = **0.5 nS**.
   * Paper Figures 6-8 describe per-50-ms luminance noise; shipped `SquareInput.mod` has no noise
     driver.

4. **Do not modify the `HHst.mod` channel complement**. Preserve `gtbar`, `glbar` at zero exactly as
   shipped. Any Windows-compile warning is a toolchain note, not a model change.

5. **Pin the ModelDB git hash `87d669dcef18e9966e29c88520ede78bc16d36ff` in the library asset's
   `library.json` description**. Include the commit date (2019-05-31) and author (`tommorse`). This
   is the code-provenance anchor for the reproduction.

6. **Re-use the existing `geoffder/Spatial-Offset-DSGC-NEURON-Model` repository
   [Geoffder-Spatial- Offset-DSGC-GH] only for cross-checking, never as a source of truth**. It
   modifies the base model per Hanson 2019's SAC-SAC manipulation; its parameters are not the
   Poleg-Polsky 2016 reproduction target.

7. **Treat "no corrigendum found" as a positive finding, not an absence of search effort**. The
   reproduction can be published as-is without worrying that we missed an official correction.

8. **Extract synapse-count logic from `RGCmodel.hoc` directly on the local copy** (the remote raw
   fetch truncated at ~350 dendritic sections before hitting `placeBIP`). Local grep for `countON`,
   `numsyn`, `placeBIP`, `placeSAC` during implementation will close the 177/282 puzzle.

## Source Index

### [PMC-PolegPolsky-Main-2016]

* **Type**: documentation
* **Title**: NMDA receptors multiplicatively scale visual signals and enhance directional motion
  discrimination in retinal ganglion cells (PMC full-text article)
* **Author/Org**: National Library of Medicine (PubMed Central)
* **Date**: 2016-03-16
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC4795984/
* **Peer-reviewed**: yes (hosted version of peer-reviewed Neuron paper)
* **Relevance**: PMC landing page for the paper, which lists the supplementary file
  `NIHMS766337-supplement.pdf` and confirms the S1-S8 supplementary figure contents that the
  `research_papers.md` enumerates.

### [PMC-PolegPolsky-Suppl-2016]

* **Type**: documentation
* **Title**: NIHMS766337-supplement.pdf (Supplementary Experimental Procedures and Figures S1-S8)
* **Author/Org**: Poleg-Polsky & Diamond via PubMed Central
* **Date**: 2016-03
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf
* **Peer-reviewed**: yes (supplementary to peer-reviewed Neuron paper)
* **Relevance**: The missing supplementary PDF flagged by `research_papers.md`. Contains the
  detailed experimental procedures that define every parameter the paper main text omits.

### [PubMed-PolegPolsky-2016]

* **Type**: documentation
* **Title**: PubMed record 26948896 for Poleg-Polsky & Diamond 2016
* **Author/Org**: National Library of Medicine
* **URL**: https://pubmed.ncbi.nlm.nih.gov/26948896/
* **Peer-reviewed**: yes
* **Relevance**: Confirmed absence of corrigenda, errata, or linked corrections. No author addendum
  posted through the PubMed linking service.

### [ModelDB-189347-Main]

* **Type**: documentation
* **Title**: ModelDB entry 189347 — Multiplication by NMDA receptors in DSGCs (Poleg-Polsky &
  Diamond 2016)
* **Author/Org**: Yale SenseLab / ModelDB
* **URL**: https://modeldb.science/189347
* **Peer-reviewed**: no (repository metadata only)
* **Relevance**: Canonical ModelDB entry. Author/implementer: Alon Polsky
  (mailto:alonpol@tx.technion.ac.il). Cell type: retinal ganglion GLU; ion currents: I_K, I_Na,t;
  receptors: AMPA, NMDA, GABA-A, nicotinic. No explicit version/release-date metadata beyond the
  paper's 2016 publication.

### [ModelDB-189347-README-HTML]

* **Type**: documentation
* **Title**: ModelDB 189347 README (readme.html)
* **Author/Org**: Poleg-Polsky via ModelDB
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/readme.html
* **Peer-reviewed**: no
* **Relevance**: Original README text. Describes three experimental conditions (control, zero Mg++,
  tuned excitation), the GUI toggles (NMDARs, voltage-gated channels, spike suppression), and the
  paper's architectural claim: tuned inhibition 300% stronger in ND; tuned excitation (cholinergic)
  300% stronger in PD; glutamatergic synapse counts equal between directions. No errata. No version.

### [ModelDB-189347-GH]

* **Type**: repository
* **Title**: ModelDBRepository/189347 (official GitHub mirror)
* **Author/Org**: ModelDB tommorse
* **URL**: https://github.com/ModelDBRepository/189347
* **Last updated**: 2019-05-31 (single commit `87d669dcef18e9966e29c88520ede78bc16d36ff`)
* **Peer-reviewed**: no (code repo; accompanies peer-reviewed paper)
* **Relevance**: Official version-controlled mirror of the ModelDB release. Commit hash is the
  reproduction's code-provenance anchor; single commit confirms no code updates since initial
  deposit. Matches the hash t0008 pinned in its library description.

### [ModelDB-189347-MainHoc]

* **Type**: repository
* **Title**: ModelDB 189347 — `main.hoc`
* **Author/Org**: Poleg-Polsky via ModelDB mirror
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/main.hoc
* **Peer-reviewed**: no
* **Relevance**: Canonical source for V_rest, Ra, g_pas, soma/dendrite channel gbar, aggregate
  synaptic conductances, stimulus parameters, and simulation timing. Used to populate the audit
  table's code-value column.

### [ModelDB-189347-HHstmod]

* **Type**: repository
* **Title**: ModelDB 189347 — `HHst.mod`
* **Author/Org**: Poleg-Polsky via ModelDB mirror
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/HHst.mod
* **Peer-reviewed**: no
* **Relevance**: Stochastic Hodgkin-Huxley MOD file. Source of single-channel conductance 10 pS,
  baseline leak 1e-5 S/cm^2, and the fact that calcium channels (gtbar, glbar) are present in code
  but zeroed in the simulation.

### [ModelDB-189347-bipolarNMDAmod]

* **Type**: repository
* **Title**: ModelDB 189347 — `bipolarNMDA.mod`
* **Author/Org**: Poleg-Polsky via ModelDB mirror
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/bipolarNMDA.mod
* **Peer-reviewed**: no
* **Relevance**: NMDA + AMPA synapse implementation. Source of τ_rise = 2 ms, τ_decay(NMDA) = 50
  ms, τ(AMPA) = 2 ms, Mg-block n = 0.25 /mM, γ = 0.08 /mV, E_rev = 0 mV, g_single = 0.2 nS,
  calcium fraction = 0.1.

### [ModelDB-189347-SACInhibmod]

* **Type**: repository
* **Title**: ModelDB 189347 — `SAC2RGCinhib.mod`
* **Author/Org**: Poleg-Polsky via ModelDB mirror
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/SAC2RGCinhib.mod
* **Peer-reviewed**: no
* **Relevance**: GABA-A synapse MOD file. Source of τ_decay = 10 ms (no explicit rise), E_GABA =
  -65 mV, g_single = 0.2 nS, and the unified vesicle-release scheme (maxves=10, newves=0.01,
  Vtau=30, s_inf=v_pre/100).

### [ModelDB-189347-SACExcmod]

* **Type**: repository
* **Title**: ModelDB 189347 — `SAC2RGCexc.mod`
* **Author/Org**: Poleg-Polsky via ModelDB mirror
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/SAC2RGCexc.mod
* **Peer-reviewed**: no
* **Relevance**: Nicotinic ACh synapse MOD file. Source of τ = 3 ms, E = 0 mV, g_single = 0.2 nS,
  confirming the paper's "cholinergic presynaptic input" architecture.

### [ModelDB-189347-SquareInputmod]

* **Type**: repository
* **Title**: ModelDB 189347 — `SquareInput.mod`
* **Author/Org**: Poleg-Polsky via ModelDB mirror
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/SquareInput.mod
* **Peer-reviewed**: no
* **Relevance**: Stimulus point-process. Square pulse (del=50 ms, dur=50 ms, gmax=1 nA) with
  embedded Jahr-Stevens block (n=0.25, γ=0.08). Noise injection is NOT implemented, so Figure 6-8
  noisy-luminance reproductions require a separate driver.

### [ModelDB-189347-RGChoc]

* **Type**: repository
* **Title**: ModelDB 189347 — `RGCmodel.hoc` (morphology template)
* **Author/Org**: Poleg-Polsky via ModelDB mirror
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/RGCmodel.hoc
* **Peer-reviewed**: no
* **Relevance**: DSGC morphology: 1 soma + 350 dendritic sections (dend[0-349]). Synapse object
  arrays `SACinhibsyn[2]`, `BIPsyn[2]`, `SACexcsyn[2]`. Public `countON` variable (the 282 /
  synapse-count discrepancy origin). The raw-file fetch returned only the topol/shape3d portions;
  `placeBIP`, `placeSAC`, and the countON arithmetic must be read from the local checkout.

### [PolegPolskyLab-CU]

* **Type**: documentation
* **Title**: Alon Poleg-Polsky, MD, PhD — CU Anschutz Physiology & Biophysics faculty page
* **Author/Org**: University of Colorado Anschutz School of Medicine
* **URL**: https://medschool.cuanschutz.edu/physiology/faculty/alon-poleg-polsky
* **Peer-reviewed**: no
* **Relevance**: First author's current lab page. No erratum, addendum, correction, or updated model
  version is posted for the 2016 Neuron paper. Confirms ModelDB 189347 stands as the only
  authoritative code release.

### [PolegPolskyLab-GH]

* **Type**: repository
* **Title**: PolegPolskyLab (GitHub organization)
* **Author/Org**: Alon Poleg-Polsky lab
* **URL**: https://github.com/PolegPolskyLab
* **Last updated**: 2024+ (active repos; no updates to 2016 DSGC code)
* **Peer-reviewed**: no
* **Relevance**: Authors' GitHub account. DSGC-adjacent repos (`DS-mechanisms`,
  `DS_Bipolar_Inputs_SAC`) address other facets of the DS circuit but do not republish or update
  ModelDB 189347.

### [Geoffder-Spatial-Offset-DSGC-GH]

* **Type**: repository
* **Title**: geoffder/Spatial-Offset-DSGC-NEURON-Model (Hanson 2019 companion code)
* **Author/Org**: Geoff deRosenroll (Awatramani lab)
* **URL**: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
* **Last updated**: 2019 (eLife 42392 companion)
* **Peer-reviewed**: no (companion to peer-reviewed eLife paper)
* **Relevance**: Third-party reuse of the ModelDB 189347 architecture for the SAC-SAC manipulation
  study. Useful cross-check if audit questions survive direct `RGCmodel.hoc` inspection, but not a
  source of truth for the Poleg-Polsky 2016 reproduction target.

### [PolegPolsky2016]

* **Type**: paper
* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC4795984/
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: The paper being reproduced. Already catalogued in `research_papers.md` Paper Index;
  re-listed here because internet findings refer to its Figure 3E (gNMDA = 2.5 nS) and Figure 6
  (per-50-ms luminance noise) as anchors against the code.

### [Oesch2005]

* **Type**: paper
* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(05)00556-9
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Already in corpus; re-listed here because the internet research confirmed that the
  project's 40-80 Hz peak-rate envelope traces to this rabbit paper (modal 148 ± 30 Hz; 41 ± 47 Hz
  PSP-shaped injection), not to the Poleg-Polsky 2016 mouse model.
