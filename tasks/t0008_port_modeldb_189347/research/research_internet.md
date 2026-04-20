---
spec_version: "1"
task_id: "t0008_port_modeldb_189347"
research_stage: "internet"
searches_conducted: 13
sources_cited: 23
papers_discovered: 1
date_completed: "2026-04-20"
status: "complete"
---
# Research: Internet Sources for Porting ModelDB 189347 and Sibling DSGC Models

## Task Objective

This task ports ModelDB 189347 (Poleg-Polsky & Diamond 2016) into the project as a library asset,
swaps in the t0009 calibrated morphology, reproduces the published tuning-curve envelope, and
surveys sibling DSGC compartmental models for Phase B. Internet research fills concrete gaps left
open by the paper corpus: the exact code-archive layout, authoritative parameter defaults baked into
the shipped HOC source, availability and NEURON-version compatibility of sibling models, and porting
tips for NEURON 7.x-era code onto the project's NEURON 8.2.7 / NetPyNE 1.1.1 stack.

## Gaps Addressed

From `research_papers.md` Gaps and Limitations:

1. **PMC author-manuscript XML truncates Experimental Procedures (`dt`, Ri, Rm, Cm, channel
   densities, synaptic decay)** — **Partially resolved**. The canonical `main.hoc` served from the
   `ModelDBRepository/189347` GitHub mirror exposes `tstop = 1000` ms, `dt = 0.1` ms,
   `tau1NMDA_bipNMDA = 60` ms, `e_SACinhib = -60` mV, and a scaling formula
   `b2gnmda = 0.5/sparse/maxvesmul` for bipolar NMDA conductance [ModelDB-189347-mainhoc-2016]. The
   `RGCmodel.hoc` template shows **1 soma + 350 dendrite sections** organised as a branching tree
   with 3D `pt3dadd` coordinates, and declares `SACinhibsyn[2]`, `BIPsyn[2]`, and `SACexcsyn[2]`
   synapse arrays [ModelDB-189347-RGCmodel-2016]. Passive properties (Ri, Rm, Cm) and Nav/Kv channel
   densities are set in procedures referenced but not fully reproduced in the web view — Phase A
   must read these directly from the working copy after unpacking the archive.
2. **ModelDB 189347 download URL/archive structure** — **Resolved**. Canonical entry is
   https://modeldb.science/189347 [ModelDB-189347-2016]; the full archive is mirrored at
   https://github.com/ModelDBRepository/189347 [ModelDBRepo-GH]. The archive contains 14 files:
   `HHst.mod`, `RGCmodel.hoc`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`, `SquareInput.mod`,
   `bipolarNMDA.mod`, `main.hoc`, `main2.c`, `main3.c`, `model.ses`, `mosinit.hoc`, `readme.docx`,
   `readme.html`, `spike.mod`, plus a `readme.fld/` directory
   [ModelDBRepo-GH, ModelDB-189347-DwnldGuide].
3. **Existence of a Poleg-Polsky supplementary code or errata on GitHub/Zenodo** — **Unresolved (no
   erratum found)**. Searches of PubMed, Google Scholar, Zenodo, and the Poleg- Polsky lab page at
   CU Anschutz [PolegPolsky-CUAnschutz] returned the 2016 paper and ModelDB entry only; no erratum
   or supplementary code archive was found. The absence should be noted in the answer asset but
   confirms the ModelDB archive is the only canonical source. Poleg-Polsky has since moved to the
   University of Colorado Anschutz (2019+) [ModelDB-189347-citations].
4. **Sibling DSGC compartmental models in public code repos (Hanson 2019, Jain 2020, Koren 2017,
   Ding 2016)** — **Resolved**. (a) `Hanson2019` ships a working NEURON fork:
   `geoffder/Spatial-Offset-DSGC-NEURON-Model` [Geoffder-GH]; 7 files (`Exp2NMDA.mod`, `HHst.mod`,
   `RGCmodel.hoc`, `modelUtils.py`, `offsetDSGC.py`, MIT licence, README). This is the highest-
   feasibility Phase B port target. (b) `Ding2016` is deposited as ModelDB 223890 but simulates a
   SAC network (not a DSGC) and is implemented in **NeuronC**, not NEURON [ModelDB-223890-2016]; low
   port feasibility, matches the research_papers.md verdict. (c) `Jain2020` publishes only
   calcium-imaging analysis code (IGOR Pro) at `benmurphybaum/eLife_2020_Analysis` [MurphyBaum-GH];
   no NEURON source is deposited, but the paper's data/code statement points back to the shared
   Awatramani-lab fork in [Geoffder-GH] [Jain2020-eLife]. (d) `Koren2017` does not publish a
   standalone NEURON DSGC model; the paper focuses on SAC-level mGluR2 dynamics and no code URL was
   found. (e) Schachter 2010 uses NeuronC and has no NEURON mirror [Smith-Lab]. **An additional
   repository discovered during search**: `NBELab/RSME` (Retinal Stimulation Modeling Environment,
   Ezra-Tsur 2022) — a NEURON + Python SAC-DSGC network with a `SAC-DSGC_network.ipynb` notebook
   driving moving-bar stimuli [NBELab-RSME-GH, EzraTsur2022].
5. **Known porting issues between NEURON 7.x and 8.2.7 for DSGC/retina mod files** — **Resolved**.
   NEURON 8.2 implicitly declares more `nrn_` / `hoc_` API methods, which can collide with legacy
   MOD files that hand-declare the same prototypes with the wrong argument or return types; the fix
   is to delete the incorrect MOD-file declaration [NEURON-Changelog-8.2, NEURON-Porting-CPP].
   NEURON 8.2.7 ships binary installers for Windows with Python 3.12 support [NEURON-Downloads].
   8.2.7 remains backward compatible with legacy MOD files that do **not** contain VERBATIM blocks;
   VERBATIM blocks may need C++-syntax updates for the upcoming NEURON 9.0 but are fine on 8.2.7
   [NEURON-Porting-CPP]. For ModelDB 189347 the risk surface is bounded: the only VERBATIM block
   anticipated is inside `HHst.mod` / `spike.mod`, which are shared-style Hodgkin-Huxley templates
   also used in the working geoffder fork.
6. **NetPyNE 1.1 compatibility tips for hand-written HOC/Python NEURON code** — **Resolved**.
   NetPyNE's `importCell()` (`netpyne.conversion.neuronPyHoc`) extracts sections, section lists,
   mechanisms, point processes, and synapses from an instantiated HOC template and stores them as a
   NetPyNE cellRule [NetPyNE-Docs, NetPyNE-ImportCell]. Signature:
   `importCell(fileName, cellName, cellArgs=None, cellInstance=False)`. Known pitfall:
   `importCell()` can modify global `h` variables (e.g. `h.celsius`) [NetPyNE-Issue-31]. Required
   discipline is to wrap the imported HOC in a NetPyNE-compatible template (section lists named
   conventionally) before calling `importCell`; section lists with original variable names are
   supported.

## Search Strategy

**Sources searched**: ModelDB (modeldb.science + legacy senselab), GitHub (code search and specific
repositories), Google Scholar, PubMed/PMC, ResearchGate, eLife, Nature, Cell, CU Anschutz
Poleg-Polsky lab page, Zenodo, NEURON documentation (nrn.readthedocs.io), NetPyNE documentation,
NEURON simulator changelog, ModelDB citation graph, Hanson 2019 eLife article, Jain 2020 eLife
article, NEURON Yale forum.

**Queries executed** (13 total):

*Pass 1 — Gap-targeted queries:*

1. `"ModelDB 189347 Poleg-Polsky Diamond DSGC NEURON download"`
2. `"geoffder Spatial-Offset-DSGC-NEURON-Model GitHub Poleg-Polsky"`
3. `"ModelDB Schachter 2010 DSGC compartmental model NeuronC rabbit direction selective"`
4. `"Jain 2020 eLife DSGC compartmental model NEURON code repository Awatramani"`
5. `"ModelDB Koren 2017 cross-compartmental DSGC direction selectivity Wei"`
6. `"NEURON 7.x to 8.2 porting migration changes mod files compatibility issues"`

*Pass 2 — Broadening queries:*

7. `"NetPyNE HOC conversion Python import NEURON 8.2 mod files compile nrnivmodl windows"`
8. `""Poleg-Polsky" DSGC NEURON erratum correction supplementary code GitHub Zenodo"`
9. `"ModelDB retinal direction selective ganglion cell compartmental NEURON list models"`
10. `""Awatramani" lab GitHub organization DSGC retinal models starburst code"`
11. `"DSGC direction selective ganglion NEURON simulation github NMDAR retina compartmental"`

*Pass 3 — Snowball queries:*

12. `""spike.mod" "HHst.mod" "bipolarNMDA.mod" NEURON DSGC 189347 compile errors"`
13. `""nrnivmodl" windows NEURON 8.2 Visual Studio compile mod ModelDB legacy"`

Additional deep-reads via WebFetch: `modeldb.science/189347`, `github.com/ModelDBRepository/189347`,
`github.com/ModelDBRepository/189347/raw/.../readme.html`,
`raw.githubusercontent.com/ModelDBRepository/189347/master/main.hoc`,
`raw.githubusercontent.com/ModelDBRepository/189347/master/RGCmodel.hoc`,
`github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model`, the same repo's `README.md` and
`offsetDSGC.py`, `github.com/NBELab/RSME`, `modeldb.science/showmodel?model=223890`,
`elifesciences.org/articles/52949`, `github.com/benmurphybaum/eLife_2020_Analysis`, and
`modeldb.science/modellist/1882?all_simu=true`.

**Date range**: No publication-date restriction. Prioritised the most recent authoritative
fork/mirror of each candidate model.

**Inclusion criteria**: Code archive or README with verifiable file list; explicit reference to
Poleg-Polsky 2016 architecture; NEURON (not NeuronC) implementation; compatible-by-construction with
NEURON 8.2.7 or documented upgrade path. **Exclusion**: marketing pages, unrelated ModelDB hits,
non-retinal DSGC work, generic tutorials without a concrete code artefact.

**Search iterations**: Query 12 was prompted by confirming MOD-file names from
`ModelDBRepository/189347`. Query 13 was prompted by the NEURON 8.2 changelog mentioning implicit
declarations. The `NBELab/RSME` find was an unexpected yield from query 11 and triggered a follow-up
WebFetch.

## Key Findings

### Canonical Archive Is Mirrored on GitHub with a Known File Layout

ModelDB 189347 ships 14 top-level files plus a `readme.fld/` directory
[ModelDBRepo-GH, ModelDB-189347-2016]. The HOC entry point is `mosinit.hoc` (auto-launched by NEURON
when the archive is opened) which loads `main.hoc`; `main.hoc` sets `tstop = 1000` ms, `dt = 0.1` ms
and drives the stimulus GUI [ModelDB-189347-mainhoc-2016]. `RGCmodel.hoc` defines a **1-soma +
350-dendrite** template with 3D points and three 2-element synapse arrays; passive properties are
set inside a `biophys()` procedure that the webfetch summary did not fully expose
[ModelDB-189347-RGCmodel-2016]. This maps cleanly to a NetPyNE
`importCell(fileName="main.hoc", cellName="RGC")` workflow once `mosinit.hoc`'s GUI auto-launch is
disabled by loading `main.hoc` directly [NetPyNE-ImportCell].

**Hypothesis (testable this task)**: Because `main.hoc` uses `dt = 0.1` ms with NEURON's default
backward-Euler integrator, the port should reproduce the published tuning-curve envelope without
further integration-timestep tuning. If the envelope fails at `dt = 0.1` ms after a clean port,
inspect variable-step integration settings before touching channel densities.

### Sibling-Model Code Availability — A Clear Port Priority Ordering

Cross-referencing repositories against the `research_papers.md` sibling list yields this table:

| Sibling | Code location | Simulator | NEURON 8.2.7 fit | Priority |
| --- | --- | --- | --- | --- |
| Poleg-Polsky & Diamond 2016 | ModelDB 189347 / [ModelDBRepo-GH] | NEURON | Expected good after 8.2 declaration fix | Phase A |
| Hanson et al. 2019 | [Geoffder-GH] (fork of 189347 + `Exp2NMDA.mod`) | NEURON | Expected good (same base) | Phase B primary |
| Jain et al. 2020 | [MurphyBaum-GH] (IGOR Pro, imaging only); NEURON model not deposited; Methods cites `Poleg-Polsky & Diamond 2016` base | NEURON (re-using 189347) | Same base as Phase A | Phase B secondary (re-use 189347) |
| Ding et al. 2016 | ModelDB 223890 | **NeuronC** | Incompatible | Skip, document as failed candidate |
| Schachter et al. 2010 | No public deposit found | **NeuronC** | Incompatible | Skip |
| Koren et al. 2017 | No standalone DSGC model deposited | n/a | n/a | Skip |
| Ezra-Tsur et al. 2022 | [NBELab-RSME-GH] | NEURON + Python | Likely good | Phase B stretch goal |

The `geoffder/Spatial-Offset-DSGC-NEURON-Model` fork adds `Exp2NMDA.mod` and substitutes the
cholinergic / bipolar / GABAergic synapse weights to `excWeight = 0.0005 µS`,
`inhibWeight = 0.004 µS`, `ampaWeight = 0.0005 µS`, `nmdaWeight = 0.0015 µS`, with `tstop = 750` ms
[Geoffder-offsetDSGC-2019]. These weights are **not identical** to the Poleg-Polsky 2016 defaults
and explain how the Hanson 2019 paper reached different quantitative inhibition amplitudes from the
same architecture. The paper [Jain2020-eLife] and [MurphyBaum-GH] together confirm Jain 2020 builds
on the same base code, re-using the **177 paired excitatory + inhibitory synapses** on a
reconstructed DSGC arbor, which matches [PolegPolsky2016]'s architecture word-for-word.

**Hypothesis (testable this task)**: The `geoffder` fork's default synaptic weights
(`inhibWeight = 0.004 µS`, `nmdaWeight = 0.0015 µS`) may produce an envelope more consistent with
the 40-80 Hz peak / 60-90° HWHM project targets than the published Poleg-Polsky 2016 defaults,
because Hanson 2019 re-tuned these weights against a contemporary experimental dataset with explicit
spike-rate targets. If the Phase A reproduction with 189347 defaults misses the envelope on the
original morphology, the Hanson 2019 weights are the first re-tuning to try before any
channel-density change.

**Best practice (community converged)**: Across every NEURON DSGC fork surveyed, the **architecture
is held constant** (177 synaptic triplets AMPA + NMDA + GABA, passive dendrites, distributed
homogeneously on ON dendrites) and tuning is accomplished **only** by rescaling conductance weights.
Channel densities and morphology are not touched after the first calibration. This task should
follow the same discipline.

### NEURON 8.2.7 Compatibility Risk Is Low and Well-Bounded

NEURON 8.2.7 is the project's target runtime. Key findings for 8.2-era porting of 7.x models:

* **Implicit API declarations**: NEURON 8.2 implicitly includes more `nrn_` / `hoc_` function
  prototypes. MOD files that hand-declare these with incorrect return or argument types will collide
  at compile time. Fix: delete the incorrect local declaration
  [NEURON-Changelog-8.2, NEURON-Porting-CPP].
* **VERBATIM blocks**: 8.2.7 still accepts legacy C syntax in VERBATIM blocks. NEURON 9.0 will
  switch to C++ and may require updates [NEURON-Porting-CPP]. Phase A's target is 8.2.7, so VERBATIM
  migration is out of scope.
* **Windows compile path**: `nrnivmodl` on Windows ships with MinGW/gcc, not Visual Studio. Two
  interfaces exist: the legacy `mknrndll` GUI (launched from the NEURON program group icon) and the
  CLI `nrnivmodl` [NEURON-FAQ, NEURON-Windows]. Either is fine; CLI is easier to automate.
* **Python bindings**: NEURON 8.2.7 on Windows supports Python 3.12 via the prebuilt installer
  [NEURON-Downloads]. The project's pyproject should be set accordingly; no source build is needed.

**Best practice**: compile `.mod` files with `nrnivmodl` first, smoke-test the loaded module by
running the shipped demo unchanged, **then** begin porting logic into the project's library layer.
If the ModelDB archive builds clean on the first try, do not change any MOD file; all divergence
should live in the Python/NetPyNE wrapper layer.

### NetPyNE `importCell` Workflow Validates Direct HOC Reuse

NetPyNE 1.1.x's `importCell()` is the canonical bridge for the project: it instantiates a HOC
template, walks its sections, and captures morphology plus point processes into a NetPyNE cellRule
[NetPyNE-ImportCell, NetPyNE-Docs]. For ModelDB 189347 the recommended wrapper is:

1. Disable `mosinit.hoc` GUI launch (load `main.hoc` directly or copy `RGCmodel.hoc` to a GUI-free
   entry file).
2. Wrap the cell creation as a HOC template with a named section list covering soma + all 350
   dendrite sections.
3. Call `importCell(fileName="dsgc.hoc", cellName="DSGC")` inside a NetPyNE cellRule builder.
4. Define synapse mechanisms as NetPyNE `synMechParams` so that synaptic weights can be
   parameterised (and tuned) from the Python side without editing HOC
   [NetPyNE-ImportCell, Geoffder-offsetDSGC-2019].

Known pitfall: `importCell()` can silently mutate global `h` state such as `h.celsius`
[NetPyNE-Issue-31]. Workaround: reset `h.celsius` immediately after the import.

### No Erratum or Post-Publication Correction Found for Poleg-Polsky 2016

Exhaustive searches of Cell Press (Neuron), PubMed, Google Scholar, Zenodo, and the Poleg-Polsky lab
page at CU Anschutz [PolegPolsky-CUAnschutz] returned no erratum, corrigendum, or supplementary code
archive attached to the 2016 paper beyond ModelDB 189347. Poleg-Polsky has since moved from NIH to
CU Anschutz [PolegPolsky-CUAnschutz, ModelDB-189347-citations] and published newer DSGC work (2019+)
but no correction to the 2016 codebase. The answer asset should record this negative result: the
ModelDB archive is canonical, first-author contact is mailto:alonpol@tx.technion.ac.il (historical)
or via CU Anschutz.

## Methodology Insights

* **Port the ModelDB archive verbatim first**: clone `ModelDBRepository/189347`, run `nrnivmodl`,
  launch `main.hoc` in NEURON 8.2.7, confirm the shipped GUI produces the PD vs ND responses. Only
  then wrap in NetPyNE [ModelDBRepo-GH, NEURON-FAQ]. This isolates port-breakage bugs from
  architecture-change bugs exactly as the `research_papers.md` methodology insight recommends.
* **Expect and handle NEURON 8.2 implicit-declaration collisions**: if a MOD file fails to compile
  with a redeclaration error for `hoc_*` or `nrn_*`, delete the hand-declared prototype from the top
  of the affected `.mod` file; do not rename or rewrite the function
  [NEURON-Changelog-8.2, NEURON-Porting-CPP].
* **Use the geoffder fork's weights as a Phase A fallback, not an alternative baseline**: port with
  the Poleg-Polsky 2016 defaults from `main.hoc` first; if the envelope test fails only after the
  t0009 morphology swap, try the Hanson 2019 weights as a targeted re-tuning before touching channel
  densities [Geoffder-offsetDSGC-2019, Geoffder-GH].
* **Wrap HOC in NetPyNE via `importCell()`, keep `mosinit.hoc` out of the import path**: NetPyNE
  re-runs the HOC at import time; a GUI-launching `mosinit.hoc` would pop a window. Rename or skip
  it and call the underlying `main.hoc` / `RGCmodel.hoc` directly
  [NetPyNE-ImportCell, NetPyNE-Docs].
* **Bail out of Ding 2016 and Schachter 2010 early in Phase B**: both are NeuronC. NeuronC does not
  run inside NEURON and would require a full rewrite [Smith-Lab, ModelDB-223890-2016]. Record as
  "failed candidate — incompatible simulator" in the answer asset and move on.
* **Jain 2020 does not need its own port**: Jain 2020's NEURON model **is** the Poleg-Polsky 2016
  base code (architecture-identical, 177 paired synapses on the same reconstructed arbor)
  [Jain2020-eLife]. Phase A's working port covers Jain 2020 for free; only the conductance-weight
  parameter set differs, and that is a Python-side configuration, not a separate port.
* **NBELab/RSME is a stretch goal**: if Phase A completes ahead of schedule, `NBELab/RSME` provides
  a self-contained NEURON+Python SAC-DSGC **network** (not single-cell) model with a ready
  `SAC-DSGC_network.ipynb` moving-bar protocol [NBELab-RSME-GH, EzraTsur2022]. This would support
  later tasks studying bipolar/SAC presynaptic tuning; it is out of scope for this task's Phase B.
* **Windows `nrnivmodl` + `uv run`**: both legacy and modern NEURON Windows installers work with the
  project's `uv`-managed Python. Run `nrnivmodl` from the DSGC library folder wrapped in
  `run_with_logs.py`, then treat the produced `nrnmech.dll` as a task-local build artefact (do not
  commit) [NEURON-FAQ, NEURON-Windows].

## Discovered Papers

### [EzraTsur2022]

* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  to starburst amacrine cells in direction selectivity
* **Authors**: Ezra-Tsur, E. et al.
* **Year**: 2022
* **DOI**: `10.1371/journal.pcbi.1009754`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009754
* **Suggested categories**: `compartmental-modeling`, `direction-selectivity`,
  `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Companion paper to the `NBELab/RSME` GitHub repository — a NEURON + Python
  SAC-DSGC network model. Provides published parameters and protocols for the stretch-goal extension
  in Phase B, and closes a gap in the paper corpus (no NEURON SAC-DSGC network model is currently
  catalogued).

## Recommendations for This Task

1. **Clone the ModelDB 189347 archive from `github.com/ModelDBRepository/189347`**, not the raw
   SenseLab zip. Pin the commit SHA in the library asset's `details.json` for reproducibility
   [ModelDBRepo-GH]. This updates `research_papers.md` recommendation 6 with an exact source URL.
2. **Use NEURON 8.2.7 on Windows with Python 3.12** via the prebuilt installer; compile MOD files
   with `nrnivmodl` inside the library folder before launching any simulation
   [NEURON-Downloads, NEURON-FAQ].
3. **If MOD-file compile fails**, delete hand-declared `nrn_` / `hoc_` prototypes that NEURON 8.2
   implicitly provides [NEURON-Changelog-8.2, NEURON-Porting-CPP]. No deeper code rewrite is
   expected to be needed for these particular MOD files.
4. **Wrap via NetPyNE `importCell()` against `main.hoc`** (not `mosinit.hoc`) with `cellName="RGC"`
   and an explicit section list covering soma + all 350 dendrite sections [NetPyNE-ImportCell].
5. **Use the Poleg-Polsky 2016 defaults first, Hanson 2019 weights as the fallback re-tuning step**:
   `tstop = 1000` ms, `dt = 0.1` ms, `tau1NMDA = 60` ms, `e_SACinhib = -60` mV
   [ModelDB-189347-mainhoc-2016]. Fallback weights if envelope fails after morphology swap:
   `excWeight = 0.0005 µS`, `inhibWeight = 0.004 µS`, `ampaWeight = 0.0005 µS`,
   `nmdaWeight = 0.0015 µS` [Geoffder-offsetDSGC-2019].
6. **In Phase B, port only `geoffder/Spatial-Offset-DSGC-NEURON-Model`** (the Hanson 2019 NEURON
   fork). Record Ding 2016 and Schachter 2010 as NeuronC-incompatible failed candidates without
   attempting port [Geoffder-GH, ModelDB-223890-2016, Smith-Lab].
7. **Re-use Phase A's port for Jain 2020 coverage**: the Jain 2020 model is architecturally
   identical to Poleg-Polsky 2016; only the parameter set differs and is configurable from Python
   [Jain2020-eLife, PolegPolsky2016-cited-in-research-papers].
8. **Record the negative erratum result in the answer asset**: no correction or supplementary
   archive exists for [PolegPolsky2016] beyond ModelDB 189347 [PolegPolsky-CUAnschutz].
9. **Optionally add `Ezra-Tsur 2022` to the paper corpus** (see Discovered Papers) as a later
   stretch reference for any SAC-DSGC network-level task downstream of this port
   [EzraTsur2022, NBELab-RSME-GH].

## Source Index

### [ModelDB-189347-2016]

* **Type**: repository
* **Title**: Multiplication by NMDA receptors in Direction Selective Ganglion cells (Poleg-Polsky &
  Diamond 2016) — ModelDB entry 189347
* **Author/Org**: Alon Poleg-Polsky (Technion / NIH), published via ModelDB
* **Date**: 2016
* **URL**: https://modeldb.science/189347
* **Last updated**: 2016 (single upload)
* **Peer-reviewed**: no (code archive associated with a peer-reviewed paper)
* **Relevance**: Canonical ModelDB landing page and metadata for the source model being ported.
  Confirms implementer identity and sim environment (NEURON).

### [ModelDBRepo-GH]

* **Type**: repository
* **Title**: ModelDBRepository/189347 — GitHub mirror of the ModelDB archive
* **Author/Org**: ModelDB (McDougal lab, Yale)
* **Date**: 2016 (mirror created at archive deposit)
* **URL**: https://github.com/ModelDBRepository/189347
* **Last updated**: single commit on master
* **Peer-reviewed**: no
* **Relevance**: Authoritative mirror of the full archive with browsable file tree. The clone target
  for Phase A because it exposes the exact 14-file layout including `mosinit.hoc`, `main.hoc`,
  `RGCmodel.hoc`, and six `.mod` files.

### [ModelDB-189347-mainhoc-2016]

* **Type**: repository
* **Title**: ModelDBRepository/189347 — `main.hoc` (entry point)
* **Author/Org**: Alon Poleg-Polsky
* **Date**: 2016
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/main.hoc
* **Peer-reviewed**: no
* **Relevance**: Source of authoritative simulation parameters the paper omits: `tstop = 1000` ms,
  `dt = 0.1` ms, `tau1NMDA_bipNMDA = 60` ms, `e_SACinhib = -60` mV, `lightspeed = 1` µm/ms, plus the
  `b2gnmda = 0.5/sparse/maxvesmul` scaling. These are the values the port must reproduce.

### [ModelDB-189347-RGCmodel-2016]

* **Type**: repository
* **Title**: ModelDBRepository/189347 — `RGCmodel.hoc` (cell template)
* **Author/Org**: Alon Poleg-Polsky
* **Date**: 2016
* **URL**: https://raw.githubusercontent.com/ModelDBRepository/189347/master/RGCmodel.hoc
* **Peer-reviewed**: no
* **Relevance**: Reveals the architectural dimensions: 1 soma + 350 dendrite sections with `pt3dadd`
  3D coordinates, `SACinhibsyn[2]`, `BIPsyn[2]`, `SACexcsyn[2]` synapse arrays. Needed when
  designing the NetPyNE cellRule and planning the t0009 morphology swap.

### [ModelDB-189347-DwnldGuide]

* **Type**: documentation
* **Title**: ModelDB — NEURON download help
* **Author/Org**: ModelDB (McDougal lab, Yale)
* **Date**: 2022 (page revision date)
* **URL**: https://modeldb.science/NEURON_DwnldGuide
* **Peer-reviewed**: no
* **Relevance**: Confirms the canonical download workflow (zip from model page or git clone from
  ModelDBRepository GitHub) and the expected `mosinit.hoc` auto-launch convention.

### [ModelDB-189347-citations]

* **Type**: documentation
* **Title**: ModelDB paper citations for entry 189347 / Poleg-Polsky 2019 entry
* **Author/Org**: ModelDB (McDougal lab, Yale)
* **Date**: queried 2026-04
* **URL**: https://modeldb.science/citations/259733
* **Peer-reviewed**: no
* **Relevance**: Shows Poleg-Polsky's post-2016 publications at CU Anschutz, confirming no
  corrigendum / updated code archive has been posted.

### [Geoffder-GH]

* **Type**: repository
* **Title**: Spatial-Offset-DSGC-NEURON-Model
* **Author/Org**: Geoff deRosenroll (geoffder), Awatramani lab, University of Victoria
* **Date**: 2019 (original publication of associated paper)
* **URL**: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
* **Last updated**: 9 commits total, exact date not shown in the fetch
* **Peer-reviewed**: no (code for peer-reviewed paper eLife 42392)
* **Relevance**: The Hanson 2019 NEURON fork of ModelDB 189347 — highest-feasibility Phase B port
  target. Adds `Exp2NMDA.mod` and re-tunes synaptic weights while preserving architecture.

### [Geoffder-offsetDSGC-2019]

* **Type**: repository
* **Title**: offsetDSGC.py (`Spatial-Offset-DSGC-NEURON-Model`)
* **Author/Org**: Geoff deRosenroll
* **Date**: 2019
* **URL**:
  https://raw.githubusercontent.com/geoffder/Spatial-Offset-DSGC-NEURON-Model/master/offsetDSGC.py
* **Peer-reviewed**: no
* **Relevance**: Reveals the Hanson 2019 default weights (`inhibWeight = 0.004 µS`,
  `excWeight = 0.0005 µS`, `ampaWeight = 0.0005 µS`, `nmdaWeight = 0.0015 µS`, `tstop = 750` ms),
  which become the Phase A re-tuning fallback if envelope fails after morphology swap.

### [ModelDB-223890-2016]

* **Type**: repository
* **Title**: Species-specific wiring for direction selectivity in the mammalian retina (Ding et al
  2016\) — ModelDB 223890
* **Author/Org**: H. Ding, R. G. Smith, A. Poleg-Polsky, J. S. Diamond, K. L. Briggman
* **Date**: 2016
* **URL**: https://modeldb.science/showmodel?model=223890
* **Peer-reviewed**: no (archive for peer-reviewed Nature paper)
* **Relevance**: Confirms Ding 2016 is a SAC-network model in NeuronC, not a NEURON DSGC.
  Incompatible with this project's stack; used to justify the "skip" decision in Phase B.

### [MurphyBaum-GH]

* **Type**: repository
* **Title**: eLife_2020_Analysis (Jain, Murphy-Baum et al. 2020)
* **Author/Org**: Ben Murphy-Baum, Awatramani lab, University of Victoria
* **Date**: 2020
* **URL**: https://github.com/benmurphybaum/eLife_2020_Analysis
* **Peer-reviewed**: no (analysis code for peer-reviewed eLife paper)
* **Relevance**: IGOR Pro calcium-imaging analysis, not a NEURON model. Confirms Jain 2020 publishes
  no independent DSGC model source and points implementation to the shared Poleg-Polsky / Hanson
  fork.

### [Jain2020-eLife]

* **Type**: paper
* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain V., Murphy-Baum B. L., deRosenroll G., Sethuramanujam S., Delsey M., Delaney K.
  R., Awatramani G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **URL**: https://elifesciences.org/articles/52949
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Data-availability statement verified: the paper's multi-compartmental NEURON DSGC
  model is architecturally the Poleg-Polsky 2016 base ("177 paired excitatory and inhibitory
  synaptic inputs distributed across the dendritic arbor"). Also present in the existing paper
  corpus as
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/ 10.7554_eLife.52949/`.

### [NBELab-RSME-GH]

* **Type**: repository
* **Title**: RSME — Retinal Stimulation Modeling Environment
* **Author/Org**: NBELab (Ezra-Tsur group)
* **Date**: 2022
* **URL**: https://github.com/NBELab/RSME
* **Peer-reviewed**: no (code for peer-reviewed PLOS Comput Biol paper)
* **Relevance**: NEURON + Python SAC-DSGC network model with `SAC-DSGC_network.ipynb` moving-bar
  notebook. Stretch-goal Phase B candidate; closes a paper-corpus gap.

### [NEURON-Changelog-8.2]

* **Type**: documentation
* **Title**: NEURON 8.2 Changelog
* **Author/Org**: NEURON simulator project
* **Date**: 2022-07 onward; 8.2.7 on PyPI with Python 3.12 support
* **URL**: https://nrn.readthedocs.io/en/8.2.7/changelog.html
* **Peer-reviewed**: no
* **Relevance**: Authoritative source on implicit-declaration collisions that are the most likely
  compile-time break when porting 2016-era MOD files to 8.2.7.

### [NEURON-Porting-CPP]

* **Type**: documentation
* **Title**: Adapting MOD files for C++ with NEURON >= 9.0
* **Author/Org**: NEURON simulator project
* **Date**: 2024-2026 (docs site)
* **URL**: https://nrn.readthedocs.io/en/latest/guide/porting_mechanisms_to_cpp.html
* **Peer-reviewed**: no
* **Relevance**: Documents the implicit-declaration fix and explains why VERBATIM migration is
  **not** needed when staying on 8.2.7. Bounds the risk surface of the port.

### [NEURON-FAQ]

* **Type**: documentation
* **Title**: NEURON FAQ — compiling MOD files with `nrnivmodl`
* **Author/Org**: NEURON simulator project
* **Date**: 8.2.6 docs revision
* **URL**: https://nrn.readthedocs.io/en/8.2.6/guide/faq.html
* **Peer-reviewed**: no
* **Relevance**: Practical build workflow: run `nrnivmodl` in the folder containing `.mod` files or
  `nrnivmodl mod` when they live in a subfolder. Sets the compile pattern for the library asset.

### [NEURON-Windows]

* **Type**: documentation
* **Title**: NEURON Windows build and `mknrndll` workflow
* **Author/Org**: NEURON simulator project
* **Date**: 2024 docs revision
* **URL**: https://nrn.readthedocs.io/en/latest/install/windows.html
* **Peer-reviewed**: no
* **Relevance**: Confirms Windows MinGW/gcc toolchain ships with the NEURON installer; Visual Studio
  is not needed. Supports the project's Windows target environment.

### [NEURON-Downloads]

* **Type**: documentation
* **Title**: NEURON precompiled installers page (8.2.7 binaries with Python 3.12 support)
* **Author/Org**: NEURON simulator project
* **Date**: queried 2026-04
* **URL**: https://www.neuron.yale.edu/neuron/download
* **Peer-reviewed**: no
* **Relevance**: Confirms 8.2.7 Windows installer availability that matches the project's NEURON
  8.2.7 / Python 3.12 target.

### [NetPyNE-ImportCell]

* **Type**: documentation
* **Title**: NetPyNE `netpyne.conversion.neuronPyHoc.importCell` — API reference
* **Author/Org**: NetPyNE developers (SUNY Downstate / Neurosim-lab)
* **Date**: v1.x docs
* **URL**: http://doc.netpyne.org/_modules/netpyne/conversion/neuronPyHoc.html
* **Peer-reviewed**: no
* **Relevance**: The canonical bridge API from hand-written HOC into NetPyNE cellRules — the
  function the port uses to wrap the Poleg-Polsky HOC template.

### [NetPyNE-Docs]

* **Type**: documentation
* **Title**: NetPyNE User Documentation — importing externally-defined cell models
* **Author/Org**: NetPyNE developers
* **Date**: v1.x docs
* **URL**: http://doc.netpyne.org/user_documentation.html
* **Peer-reviewed**: no
* **Relevance**: Describes how NetPyNE captures morphology, sections, section lists, point
  processes, and synapses from an imported HOC template into a cellRule. Sets the wrapper
  architecture for the library asset.

### [NetPyNE-Issue-31]

* **Type**: forum
* **Title**: `importCell()` function can modify h variables (eg. h.celsius) — NetPyNE issue #31
* **Author/Org**: netpyne / Neurosim-lab
* **Date**: 2018 (issue; behaviour persists in 1.x)
* **URL**: https://github.com/suny-downstate-medical-center/netpyne/issues/31
* **Peer-reviewed**: no (community issue tracker)
* **Relevance**: Documents the global-state mutation pitfall of `importCell()`; informs the "reset
  `h.celsius` after import" workaround that the port should apply.

### [PolegPolsky-CUAnschutz]

* **Type**: documentation
* **Title**: Alon Poleg-Polsky, MD, PhD — CU Anschutz Physiology faculty page
* **Author/Org**: University of Colorado Anschutz Medical Campus
* **Date**: queried 2026-04
* **URL**: https://medschool.cuanschutz.edu/physiology/faculty/regular-faculty/alon-poleg-polsky
* **Peer-reviewed**: no
* **Relevance**: Current first-author affiliation and contact point should the port need
  clarification on undocumented 2016-era parameters. Confirms no corrigendum is publicly linked.

### [Smith-Lab]

* **Type**: documentation
* **Title**: Robert G. Smith, PhD — NeuronC lab page (Penn)
* **Author/Org**: Robert Smith, University of Pennsylvania
* **Date**: queried 2026-04
* **URL**: https://retina.anatomy.upenn.edu/~rob/
* **Peer-reviewed**: no
* **Relevance**: Authoritative source on NeuronC — the simulator used by Schachter 2010 and Ding
  2016 that is **not** NEURON. Confirms porting these to NEURON would require rewriting the
  simulator layer, not just translating files.

### [PolegPolsky2016]

* **Type**: paper
* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Alon Poleg-Polsky, Jeffrey S. Diamond
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.07.035`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(16)30463-7
* **Peer-reviewed**: yes (Neuron, Cell Press)
* **Relevance**: The source paper whose model is being ported. Present in the existing paper corpus
  at `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/` and analysed in
  `research/research_papers.md`. Referenced in body text when distinguishing the 2016 paper itself
  from the ModelDB code archive.

### [EzraTsur2022]

* **Type**: paper
* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  to starburst amacrine cells in direction selectivity
* **Authors**: Elishai Ezra-Tsur et al.
* **Year**: 2022
* **DOI**: `10.1371/journal.pcbi.1009754`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009754
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Companion paper to the `NBELab/RSME` repository — a NEURON + Python SAC-DSGC
  network model. Stretch-goal Phase B candidate; also listed in Discovered Papers for addition to
  the paper corpus.
