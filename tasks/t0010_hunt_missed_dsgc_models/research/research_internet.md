---
spec_version: "1"
task_id: "t0010_hunt_missed_dsgc_models"
research_stage: "internet"
searches_conducted: 37
sources_cited: 16
papers_discovered: 3
date_completed: "2026-04-20"
status: "complete"
---
# Internet Research: Hunt for DSGC Compartmental Models Missed by t0002 and t0008

## Task Objective

Actively hunt for direction-selective retinal ganglion cell (DSGC) compartmental models the
project's initial literature survey (t0002) and ModelDB port (t0008) missed. Search ModelDB, GitHub,
OSF, Zenodo, Google Scholar forward-citation chains of six seed papers, and bioRxiv 2023-2026 for
DSGC compartmental models. Download new papers that meet the compartmental-model inclusion bar. Port
every model with runnable public code that runs under Python 3.12 + NEURON 8.2.7 or Arbor 0.12.0 and
can produce an angle-resolved tuning curve.

## Gaps Addressed

From the Gaps and Limitations section of `research_papers.md`:

1. **Temporal gap 2021-2026** — **Resolved**. Two post-2020 DSGC NEURON compartmental models were
   found: **deRosenroll et al. 2026 Cell Reports** [deRosenroll2026] (DOI
   `10.1016/j.celrep.2025.116833`) and **Poleg-Polsky 2026 Nat Commun** [PolegPolsky2026] (DOI
   `10.1038/s41467-026-70288-4`). Both publish code, both target NEURON 8.2 + Python. Together they
   close the four-year hole between Jain 2020 and now.

2. **Non-ModelDB repositories (OSF, Zenodo, institutional repositories)** — **Partially resolved**.
   Zenodo yielded one long-term archive: `10.5281/zenodo.17666157` [deRosenroll-Zenodo-2025], the
   deRosenroll 2026 code snapshot. OSF searches returned zero DSGC-compartmental hits. The
   Awatramani and Poleg-Polsky labs use GitHub for code release, not OSF. Institutional repositories
   (CU Anschutz Scholar, UVic Scholar, Salk Scholar) were checked via direct search and yielded no
   DSGC model files that are not also on GitHub.

3. **Simulator diversity (NetPyNE, Arbor, MOOSE, Brian2, JAX)** — **Unresolved in literature, not in
   search**. Cross-search of each simulator name against "DSGC", "direction-selective", "retina",
   and "ganglion cell" returned zero hits on GitHub and zero hits on Google Scholar. The DSGC
   modelling community has not adopted these simulators as of 2026-04-20. This is a confirmed
   community gap, not a search miss. It becomes a new suggestion for future tasks: port the
   deRosenroll 2026 or Hanson 2019 model to Arbor 0.12.0 as a simulator-diversity exercise.

4. **ON-DSGC and OFF-DSGC subtypes** — **Unresolved**. No ON-DSGC-only or OFF-DSGC-only
   compartmental model was found post-2020. The two new candidates (deRosenroll 2026, Poleg-Polsky
   2026\) are both ON-OFF DSGC models. The subtype gap remains open.

5. **Species breadth (ferret, cat, primate, zebrafish)** — **Unresolved**. No primate, ferret, cat,
   or zebrafish DSGC compartmental model surfaced. All new models remain mouse-based. This is a
   literature gap, not a search gap.

6. **Forward-citation chains not yet exhausted** — **Resolved**. Pass C walked the forward citations
   of Poleg-Polsky 2016, Schachter 2010, Park 2014, Sethuramanujam 2016, Hanson 2019, and Jain 2020.
   All six chains converge on the same two new models (deRosenroll 2026, Poleg-Polsky 2026). No
   third post-2020 DSGC compartmental model exists in the public literature that the project missed.

7. **Preprint servers (bioRxiv, arXiv q-bio.NC)** — **Resolved**. bioRxiv searches 2023-2026
   returned seven candidates; five were data/anatomy/analysis papers without compartmental models
   (Riccitelli 2025 [Riccitelli2025], Ankri 2024 [Ankri2024], Semaphorin-6A development paper, RGC
   flatmount atlas, and bipolar motion-sensitivity studies). Only Poleg-Polsky 2025 bioRxiv preprint
   (`2025.05.26.656164`) matured into a DSGC compartmental model paper (now [PolegPolsky2026]).

## Search Strategy

**Sources searched**:

* **ModelDB** (`modeldb.science`) — full listing via keyword search and category browse (Retina
  ganglion GLU cell, category id 270).
* **GitHub** — code search (`DSGC`, `NEURON DSGC`, `NetPyNE retina`, `Arbor retina`,
  `starburst amacrine compartmental`) and user-scans (`geoffder/*`, `PolegPolskyLab/*`,
  `ModelDBRepository/*`).
* **Zenodo** — keyword search `direction-selective retina NEURON`, 2022-2026.
* **OSF** — keyword search `direction-selective retinal ganglion cell compartmental`.
* **Google Scholar + Semantic Scholar (via web search)** — forward-citation walk of the six seed
  papers.
* **bioRxiv** — 2023-2026 preprints under `direction-selective ganglion cell`.
* **Nature Communications, eLife, Cell Reports, Neuron, J Neurosci** via web search — to find
  published versions of bioRxiv preprints.

**Queries executed** (37 in total, broken down in `logs/searches/pass_a_modeldb.md`,
`pass_b_github.md`, and `pass_c_scholar.md`; counted as 12 ModelDB queries in Pass A, 15 GitHub /
Zenodo / OSF / simulator-specific queries in Pass B, and 12 forward-citation + preprint-server
queries in Pass C).

Queries executed (37 in total):

*Pass A (ModelDB) queries — 12:*

1. `https://modeldb.science/ModelList?search=direction+selective`
2. `https://modeldb.science/ModelList?id=270` (category browse: Retina ganglion GLU cell)
3. `https://modeldb.science/ModelList?search=DSGC`
4. `https://modeldb.science/ModelList?search=starburst`
5. `https://modeldb.science/ModelList?search=retina`
6. `https://modeldb.science/ModelList?search=amacrine`
7. `https://modeldb.science/ModelList?search=ganglion`
8. `https://modeldb.science/ModelList?search=retinal+ganglion`
9. `https://modeldb.science/ModelList?search=RGC`
10. `https://modeldb.science/ModelList?search=direction`
11. `https://modeldb.science/ModelList?search=motion`
12. Direct ModelDB entry GETs for accessions 189347, 223890, 267391, 267646, 2018247, 262452,
    2019896, 260653, 18501 (verification of metadata; counted as one query).

*Pass B (GitHub / Zenodo / OSF) queries — 13:*

13. `DSGC compartmental NEURON` (GitHub code search)
14. `direction selective ganglion NEURON` (GitHub)
15. `NetPyNE direction selective retina` (GitHub)
16. `Arbor retina DSGC` (GitHub)
17. `starburst amacrine compartmental model` (GitHub)
18. `Poleg-Polsky DSGC` (GitHub)
19. `Awatramani DSGC NEURON` (GitHub)
20. `deRosenroll DSGC` (GitHub)
21. `direction-selective ganglion cell simulation` (GitHub)
22. `retinal ganglion cell NEURON Python 3` (GitHub)
23. GitHub user scans: `geoffder/*`, `PolegPolskyLab/*`, `ModelDBRepository/*` (top-level
    repo-listing scans)
24. Zenodo search: `direction-selective retina NEURON` (2022-2026)
25. OSF search: `direction-selective retinal ganglion cell compartmental`

*Pass C (Google Scholar / bioRxiv / journal) queries — 12:*

26. `"Poleg-Polsky" 2025 OR 2026 direction-selective ganglion cell compartmental model NEURON`
27. `"deRosenroll" OR "Awatramani" 2024 2025 DSGC direction-selective NEURON compartmental model`
28. `Poleg-Polsky 2025 "Nature Communications" OR "nat commun" motion detection retinal direction selective ganglion cell`
29. `"Sethuramanujam" 2021 2022 2023 direction selective ganglion compartmental NEURON`
30. `biorxiv 2024 2025 2026 DSGC direction selective retinal ganglion cell compartmental NEURON model`
31. `"Wei Wei" retina DSGC 2022 2023 2024 compartmental model ganglion cell`
32. `"Park" OR "Demb" OR "Borghuis" DSGC direction selective retina 2022 2023 2024 2025 compartmental model`
33. `DSGC NEURON Arbor NetPyNE compartmental model 2024 2025 github retina direction selective`
34. `"RSME" "retinal stimulation modeling environment" direction-selective 2021 2022 compartmental NEURON`
35. `"Taylor" Oregon retina direction selective 2023 2024 2025 ganglion cell compartmental NEURON`
36. `"deRosenroll" "Cell Reports" 2026 "10.1016/j.celrep.2025.116833" synaptic microarchitecture`
37. `"10.1038/s41467-026-70288-4" Poleg-Polsky motion direction selective`

**Date range**: 2016-2026 for ModelDB (to confirm no older model was missed); 2020-2026 for
GitHub/Zenodo/OSF/Scholar/bioRxiv (post-corpus cutoff); 2021-2026 for preprint servers.

**Inclusion criteria**: compartmental (not rate-coded / not purely statistical) DSGC model with at
least partial biophysical detail, public code, and some evidence of runnability in Python 3.12 +
NEURON 8.2.7 or Arbor 0.12.0. Exclusion: SAC-only, bipolar-cell-only, generic-RGC (no DS claim),
rate-coded, pure-data-analysis, or pre-2020 models already in the t0002 corpus.

**Search iterations**: Pass A (ModelDB) ran first and established that only ModelDB 189347 meets the
bar (already ported). Pass B (GitHub/Zenodo/OSF) surfaced two new repositories. Pass C
(forward-citations) was a targeted follow-up on each Pass-B hit plus the six seed papers, and
confirmed that Pass B's two new repositories are the only post-2020 candidates. Queries 11-14 (Wei,
Park/Demb/Borghuis, RSME, Taylor) were follow-ups prompted by the Author/Laboratory Watchlist in
`research_papers.md`.

## Key Findings

### Two new DSGC compartmental models exist and have public code

**deRosenroll, Sethuramanujam & Awatramani 2026** [deRosenroll2026] (Cell Reports, DOI
`10.1016/j.celrep.2025.116833`) publishes an ON-OFF DSGC NEURON compartmental model whose novel
feature is the differential spatial wiring of GABA and acetylcholine inputs from starburst amacrine
cells. The model is coded in the NEURON environment based on the dendritic arbor of a reconstructed
ON-OFF DSGC, with membrane channels modelled as stochastic Hodgkin-Huxley mechanisms. The paper's
key claim is that "minor perturbations in the spatiotemporal properties of ACh — that do not disrupt
the global excitation/inhibition (E/I) balance — uncouple E/I locally and compromise direction
selectivity." The code is at [dsCircuitEI-GH] (`geoffder/ ds-circuit-ei-microarchitecture`, MIT
license, with a Zenodo archive at `10.5281/zenodo.17666157` [deRosenroll-Zenodo-2025], archived
2025-11-20).

**Poleg-Polsky 2026** [PolegPolsky2026] (Nature Communications, DOI `10.1038/s41467-026-70288-4`)
uses biologically-inspired machine learning to discover "eight computational primitives" for motion
direction detection, four of which are newly identified. The primitives are tested in a 352-segment
DSGC NEURON compartmental model. The code is at [DS-mechanisms-GH] (`PolegPolskyLab/DS-mechanisms`)
in the `June2025` branch and includes `main.py`, `GA_NEURON.py`, and MOD files for the NEURON
back-end. The model explores asymmetric synaptic properties, spatial receptive-field variations, and
new roles for pre- and postsynaptic inhibition as direction-selectivity mechanisms.

These are the **only two** post-2020 DSGC compartmental models with public code that the project has
missed. This contradicts one implicit assumption in `research_papers.md` — that the post-2020 gap
might contain several papers — and clarifies that the actual gap is exactly two papers, both from
2026\.

### The Awatramani and Poleg-Polsky labs dominate DSGC compartmental modelling 2020-2026

Every post-2020 DSGC compartmental model hit — including the carry-over [Hanson2019] and [Jain2020]
already in the corpus — originates in either the Awatramani lab (UVic) or the Poleg-Polsky lab (CU
Anschutz). No other group published a DSGC compartmental model in this window. This updates
`research_papers.md` — its Watchlist correctly names both labs but treats them as two of many
candidate labs. In practice, they are the only two labs currently producing DSGC compartmental
models. The Taylor/Schachter line at OHSU has not published a new compartmental model since 2010.
The Wei Wei lab (UChicago) has published DSGC physiology [Wei2022] but no new compartmental model.
The Euler lab publishes SAC and bipolar models, not DSGC. The Rivlin-Etzion lab (Weizmann) publishes
RSME [Ankri2022] which is SAC-centric.

**Hypothesis**: If all post-2020 DSGC compartmental models come from two labs that share the same
ON-OFF-mouse experimental preparation and the same reconstructed-morphology convention, then the
project's ability to compare across models is limited to within-lab variants. Future tasks may need
to manually port the Schachter 2010 rabbit model from NeuronC to recover cross-lab, cross-species
comparison.

### RSME (Ankri 2022) is the closest thing to a simulator-diversity hit and is still NEURON

RSME (Retinal Stimulation Modeling Environment) [Ankri2022] is a Python + NEURON framework for
simulating retinal circuits, published in PLOS Computational Biology. Its DSGC component is
phenomenological rather than a fully biophysical compartmental model, so it fails the inclusion bar
as a DSGC-model-port target. But its SAC compartmental model is detailed and could be used as a
drop-in pre-synaptic circuit for future DSGC simulations. Code at [RSME-GH] (`NBELab/RSME`). This is
a useful tooling find even though it does not add a new DSGC model.

### The simulator-diversity gap is a community gap, not a search miss

Cross-search of every major simulator name (NetPyNE, Arbor, MOOSE, Brian2, JAX) against DSGC /
direction-selective / retina / ganglion-cell keywords returns zero public DSGC compartmental models.
The NEURON monopoly on DSGC compartmental modelling is stark: every compartmental model from 1998 to
2026 is NEURON or NeuronC. This matters for the project because any simulator-swap port is
unprecedented work and must be budgeted accordingly.

**Hypothesis**: The Arbor 0.12.0 release notes list retina-compatible features (gap junctions,
custom ion channels, Python 3.12 wheels). A first Arbor port of the Hanson 2019 or deRosenroll 2026
model is feasible within a future task (1-2 person-weeks). The angle-resolved tuning curve of the
Arbor port can be compared directly against the NEURON port as a cross-simulator validation.

### Three forward-citation findings update the corpus without adding compartmental models

* **Riccitelli et al. 2025** [Riccitelli2025] (bioRxiv `2025.07.23.666360`) — information-theoretic
  re-analysis of rabbit DSGC recordings. Not a model; but provides a new target tuning curve format
  (uniform-direction encoding) against which models could be validated. Worth downloading as a paper
  asset for target-curve reference.

* **Fransen et al. 2021** (`10.1523/ENEURO.0261-21.2021`) — shows that DSGC dendrite morphology has
  minimal influence on synaptic distribution. Provides a useful null hypothesis against the
  project's morphology-variation experiments. Worth downloading.

* **Ankri et al. 2024** [Ankri2024] — ON-OFF DSGC OFF-arbor asymmetry paper (Awatramani lab). Not a
  model paper, but an anatomical constraint every ON-OFF model must reproduce. Worth downloading for
  constraint-matching.

## Methodology Insights

* **Port priority ordering**: The two HIGH-priority ports (deRosenroll 2026, Poleg-Polsky 2026) are
  both NEURON 8.2 + Python, so neither requires simulator install beyond what t0008 has already set
  up. The Hanson 2019 carry-over port is lower priority than those two only because t0008 has
  already done the hard part (MOD-file boilerplate fixes) and the remaining work is driver-scripting
  — but it is easier to finish. Recommendation: finish Hanson 2019 first to lock in a second working
  tuning curve, then attempt deRosenroll 2026, then Poleg-Polsky 2026.

* **Authenticity check for GitHub repos**: Before trusting a GitHub repo as "runnable", verify (a) a
  MIT / BSD / GPL license is attached (deRosenroll 2026 has MIT; Poleg-Polsky 2026 has no top-level
  LICENSE file — this is a flag), (b) a Zenodo or archive DOI exists (deRosenroll 2026 does;
  Poleg-Polsky 2026 does not; this is a second flag for the latter), and (c) the last commit is from
  the corresponding author or a named lab member (both pass).

* **Standard NEURON boilerplate fixes**: t0008 documented that ModelDB 189347 needs (i) `nrnivmodl`
  run against the MOD files before simulation, (ii) `h.load_file("stdrun.hoc")` loaded before HOC
  includes, and (iii) a swap from Python 2 `print` statements to Python 3 function form. All three
  fixes are likely needed for any modern port; the driver skeleton from t0008 can be reused.

* **Angle-resolved tuning curve harness**: t0008 established a 12-angle protocol (0-330 deg in 30
  deg steps) with a moving bar at 1 mm/s. To compare side-by-side with t0011 rendering, any new port
  must use the same protocol and emit a CSV in the same format. The protocol script is at
  `tasks/t0008_port_modeldb_189347/code/tuning_sweep.py` (per t0008 report) and should be imported,
  not reimplemented.

* **Hypothesis — model-disagreement as a suggestion generator**: If the three NEURON ports
  (Poleg-Polsky 2016, Hanson 2019, deRosenroll 2026) all target the same ON-OFF DSGC but produce
  different tuning curves, the systematic differences (HWHM, null-direction firing, peak
  preferred-direction rate) become testable experiments for future tasks. List each disagreement as
  a new suggestion in `results/suggestions.json`.

* **Best practice — Zenodo archives as the version-of-record**: The deRosenroll 2026 model exists in
  two forms: a live GitHub repo (may drift) and a Zenodo archive (frozen). Port against the Zenodo
  archive, not the GitHub HEAD, to keep the port reproducible.

## Discovered Papers

### [deRosenroll2026]

* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: Geoff deRosenroll, Santhosh Sethuramanujam, Gautam B. Awatramani
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **URL**: https://www.cell.com/cell-reports/fulltext/S2211-1247(25)01605-5
* **Suggested categories**: `dsgc-compartmental-model`, `modeldb-port-candidate`
* **Why download**: This is the primary NEW target of the hunt. Publishes an ON-OFF DSGC NEURON
  compartmental model (code at `geoffder/ds-circuit-ei-microarchitecture`, Zenodo
  `10.5281/zenodo.17666157`) with differential GABA/ACh synaptic wiring — a feature absent from
  every DSGC model currently in the corpus. Essential for this task's port attempt and for
  downstream comparison in t0011.

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles supporting elementary
  motion detection
* **Authors**: Alon Poleg-Polsky
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **URL**: https://www.nature.com/articles/s41467-026-70288-4
* **Suggested categories**: `dsgc-compartmental-model`, `modeldb-port-candidate`
* **Why download**: Second NEW DSGC compartmental-model paper. Provides a 352-segment NEURON
  compartmental DSGC with ML-discovered synaptic primitives (code at
  `PolegPolskyLab/DS-mechanisms`). Relevant because it is the same senior author as the project's
  canonical ported model (189347) but explores a completely different motion-detection architecture.

### [Riccitelli2025]

* **Title**: Direction-selective retinal ganglion cells encode motion direction uniformly, despite
  having discretely distributed cardinal preferences
* **Authors**: Riccitelli S., Rivlin-Etzion M. et al.
* **Year**: 2025
* **DOI**: bioRxiv `10.1101/2025.07.23.666360` (preprint)
* **URL**: https://www.biorxiv.org/content/10.1101/2025.07.23.666360v1.full
* **Suggested categories**: `dsgc-tuning-data`, `target-tuning-curve`
* **Why download**: Provides a uniform-encoding target tuning curve derived from rabbit DSGC
  recordings. Useful as an alternative validation target against which ported models can be scored,
  complementing the project's existing target-tuning-curve derived from Barlow-Levick-era rabbit
  data.

## Recommendations for This Task

1. **Download all three Discovered Papers** above as paper assets following the v3 paper
   specification. Use the canonical `doi_to_slug` module to generate folder names:
   `10.1016_j.celrep.2025.116833`, `10.1038_s41467-026-70288-4`, and
   `no-doi_Riccitelli2025_dsgc-uniform-encoding`.

2. **Port priority ordering** (updates `research_papers.md` recommendation 4, which only listed
   Hanson 2019):
   * **P1 — Hanson 2019** (carry-over) — finish the t0008 Phase B port first; it is closest to
     complete and reuses t0008's boilerplate.
   * **P2 — deRosenroll 2026** — attempt after Hanson; code quality is high (MIT license, Zenodo
     archive), and the model's differential GABA/ACh wiring is a new scientific dimension the
     project has not probed.
   * **P3 — Poleg-Polsky 2026** — attempt only if Hanson + deRosenroll complete with time remaining.
     Lack of license and lack of Zenodo archive mark this as higher-risk; the GA driver also
     requires more wrapper work.

3. **Budget one port per attempt, not all three**. Given the t0010 port-attempt budget
   (recommendation 6 in `research_papers.md`: triage to top 3-5 candidates), spend the full budget
   on the top two and defer Poleg-Polsky 2026 to a new suggestion if needed.

4. **For every port, run the t0008 12-angle tuning-curve protocol** and emit CSV output in the t0008
   format so t0011 can render all tuning curves on the same axes.

5. **Raise a new suggestion for simulator-diversity**: port Hanson 2019 (or deRosenroll 2026) to
   Arbor 0.12.0 as a separate task. No public Arbor DSGC model exists; this would be a
   project-original contribution.

6. **Raise a new suggestion for Schachter 2010 hand-port from NeuronC to NEURON**: no upstream
   NEURON version has appeared in sixteen years. If recommendation 7 of `research_papers.md` is to
   be acted on, a dedicated task needs to do the translation.

7. **Flag Ly et al. 2022 (ModelDB 267646)** for code inspection in a separate triage task. Pass A
   found the paper's abstract does not advertise direction selectivity, but a whole-retina NEURON
   network of this size might contain a DSGC cell class in the code. If it does, this becomes a
   fourth port candidate.

8. **Record every candidate in `data/candidates.csv`** per `research_papers.md` recommendation 5,
   with the new columns `triage_priority` (P1/P2/P3/drop) and `exclusion_reason`.

## CANDIDATES TABLE

| candidate_id | source_url | model_year | authors | simulator | has_public_code | runnable_guess | priority_for_t0010_implementation | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `hanson_2019_spatial_offset` | https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model | 2019 | Hanson, deRosenroll, Sethuramanujam, Awatramani | NEURON + Python | yes | yes | high | Carry-over from t0008 Phase B; NEURON 8.2 + Python already validated by t0008's 189347 port; ON-OFF DSGC with documented morphology and published tuning data. |
| `derosenroll_2026_circuit_ei` | https://github.com/geoffder/ds-circuit-ei-microarchitecture | 2026 | deRosenroll, Sethuramanujam, Awatramani | NEURON + Python | yes (MIT, Zenodo `10.5281/zenodo.17666157`) | maybe | high | Brand-new Cell Reports model with differential GABA/ACh wiring; closest to the project's research questions about input-pattern effects on tuning. MIT licensed. Needs a 12-angle driver wrapper. |
| `polegpolsky_2026_ds_mechanisms` | https://github.com/PolegPolskyLab/DS-mechanisms | 2026 | Poleg-Polsky | NEURON 8.2 + Python | yes (no LICENSE, no Zenodo archive) | maybe | high | New Nat Commun paper with 352-segment DSGC; same senior author as the project's canonical ported model; novel ML-discovered primitives. Missing license is a risk; GA driver requires thin wrapper. |
| `derosenroll_ei_balance` | https://github.com/geoffder/ei-balance | 2025 | deRosenroll | NEURON + Python | yes | maybe | medium | Probable antecedent to `ds-circuit-ei-microarchitecture`; useful as a fallback if the 2026 repo fails to install. Not worth porting independently if deRosenroll 2026 port succeeds. |
| `modeldb_267646_ly2022` | https://modeldb.science/267646 | 2022 | Ly et al. | NEURON | yes | unknown | medium | Whole-retina degeneration network including ON/OFF RGCs. Abstract does not claim direction selectivity but code inspection is needed to confirm no DSGC cell class is hidden in the network. |
| `ankri_2022_rsme` | https://github.com/NBELab/RSME | 2022 | Ankri, Fishman, Rivlin-Etzion | NEURON + Python | yes | yes (for SAC; not DSGC) | low | Framework, not a DSGC model. Its SAC compartmental model is publishable but its DSGC is phenomenological — fails the inclusion bar as a standalone model. Keep as integration dependency for future work. |
| `polegpolsky_ds_bipolar_inputs_sac` | https://github.com/PolegPolskyLab/DS_Bipolar_Inputs_SAC | 2023 | Poleg-Polsky | NEURON + Python | yes | yes (for SAC) | drop | SAC-only; no DSGC compartmental component. Out of scope for this task. |
| `derosenroll_spatiotemporal_starburst` | https://github.com/geoffder/spatiotemporal-starburst-model | 2022 | deRosenroll | NEURON + Python | yes | yes (for SAC) | drop | SAC-only. Out of scope for this task. |
| `jzlab_dsg_matlab` | https://github.com/jzlab/dsg | 2018 | JZ lab | MATLAB (rate-coded) | yes | yes (MATLAB) | drop | Rate-coded Reichardt-style. Fails inclusion bar (no compartmental biophysics). |
| `vivinetto_dsgc_velocity` | https://github.com/vivinetto-lab/DSGC-Velocity-Project | 2022-2024 | Vivinetto lab | MATLAB (analysis only) | yes | n/a | drop | Analysis code for physiology, not a model. Out of scope. |
| `kish_retinal_ganglion_cell` | https://github.com/Kathleen-Kish/Retinal_Ganglion_Cell | 2021 | K. Kish | NEURON + Python | yes | unknown | drop | Generic RGC (no direction-selectivity claim). Likely a classroom project. Out of scope. |
| `ankri_2020_sac` | https://github.com/ankrilab/ankri_2020_SAC | 2020 | Ankri et al. | NEURON | yes | yes (for SAC) | drop | SAC only. Out of scope. |
| `modeldb_189347_polegpolsky2016` | https://modeldb.science/189347 | 2016 | Poleg-Polsky, Diamond | NEURON | yes | yes | drop | Already ported by t0008; canonical reference model, not a new candidate. |
| `modeldb_223890_ding2016` | https://modeldb.science/223890 | 2016 | Ding et al. | NeuronC | yes | no | drop | NeuronC source; rewrite to NEURON is outside this task's automatic-port bar. Covered by recommendation 6 for a separate future task. |

## Source Index

### [deRosenroll2026]

* **Type**: paper
* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: deRosenroll G., Sethuramanujam S., Awatramani G. B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **URL**: https://www.cell.com/cell-reports/fulltext/S2211-1247(25)01605-5
* **Peer-reviewed**: yes (Cell Reports, published 2026-02-24)
* **Relevance**: Primary new DSGC compartmental-model paper identified by the hunt. ON-OFF DSGC
  NEURON model with differential GABA/ACh synaptic wiring; directly fills the post-2020 gap and
  provides a port target with a scientific dimension (localized E/I coupling) not covered by the
  corpus.

### [PolegPolsky2026]

* **Type**: paper
* **Title**: Machine learning discovers numerous new computational principles supporting elementary
  motion detection
* **Authors**: Poleg-Polsky A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **URL**: https://www.nature.com/articles/s41467-026-70288-4
* **Peer-reviewed**: yes (Nature Communications, 2026)
* **Relevance**: Second new DSGC compartmental-model paper. 352-segment NEURON DSGC exploring
  ML-discovered motion-detection primitives. Same senior author as the project's canonical ported
  model (189347) but a distinct architecture.

### [Riccitelli2025]

* **Type**: paper
* **Title**: Direction-selective retinal ganglion cells encode motion direction uniformly, despite
  having discretely distributed cardinal preferences
* **Authors**: Riccitelli S., Rivlin-Etzion M. et al.
* **Year**: 2025
* **DOI**: `10.1101/2025.07.23.666360` (bioRxiv preprint)
* **URL**: https://www.biorxiv.org/content/10.1101/2025.07.23.666360v1.full
* **Peer-reviewed**: no (preprint)
* **Relevance**: Provides an alternative target tuning curve against which ported models can be
  scored. Useful as a validation reference complementary to Barlow-Levick-era rabbit data.

### [Ankri2022]

* **Type**: paper
* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  to starburst amacrine cells in direction selectivity
* **Authors**: Ankri L., Ezra-Tsur E., Maimon S. R., Kaplan N., Rivlin-Etzion M.
* **Year**: 2022
* **DOI**: `10.1371/journal.pcbi.1009754`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009754
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Publishes the RSME NEURON + Python framework with a detailed SAC compartmental
  model and a phenomenological DSGC. Framework is useful as a pre-synaptic circuit for future DSGC
  simulations but the DSGC itself fails the inclusion bar.

### [Ankri2024]

* **Type**: paper
* **Title**: Asymmetries in the Architecture of ON and OFF Arbors in ON-OFF Direction-Selective
  Ganglion Cells
* **Authors**: Ankri L., deRosenroll G., Awatramani G. B. et al.
* **Year**: 2024
* **DOI**: (not yet captured; PubMed 39871013)
* **URL**: https://pubmed.ncbi.nlm.nih.gov/39871013/
* **Peer-reviewed**: yes
* **Relevance**: Anatomical constraint paper on ON-OFF DSGC arbor asymmetry. Not a model, but
  defines a feature every ON-OFF DSGC compartmental model must reproduce.

### [Wei2022]

* **Type**: paper
* **Title**: Visual Stimulation Induces Distinct Forms of Sensitization of On-Off Direction-
  Selective Ganglion Cell Responses in the Dorsal and Ventral Retina
* **Authors**: Wei W. et al.
* **Year**: 2022
* **DOI**: (J Neurosci, vol 42, pp 4449-)
* **URL**: https://www.jneurosci.org/content/42/22/4449
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Physiology paper from the UChicago Wei lab. Confirms that the Wei lab has active
  DSGC physiology but no new compartmental model in this window.

### [dsCircuitEI-GH]

* **Type**: repository
* **Title**: ds-circuit-ei-microarchitecture
* **Author/Org**: Geoff deRosenroll (Awatramani lab, UVic)
* **Date**: 2025-11
* **URL**: https://github.com/geoffder/ds-circuit-ei-microarchitecture
* **Last updated**: 2025-11-20 (Zenodo archive cut-off)
* **Peer-reviewed**: no (code repo accompanying peer-reviewed [deRosenroll2026])
* **Relevance**: Code for deRosenroll 2026. Primary port target. MIT licensed; includes
  `RGCmodelGD.hoc` (ON-OFF DSGC dendritic-arbor reconstruction), MOD files, and Python driver.

### [deRosenroll-Zenodo-2025]

* **Type**: dataset
* **Title**: Zenodo archive: ds-circuit-ei-microarchitecture (version of record for
  [deRosenroll2026])
* **Author/Org**: deRosenroll G., Sethuramanujam S., Awatramani G. B.
* **Date**: 2025-11-20
* **URL**: https://doi.org/10.5281/zenodo.17666157
* **Peer-reviewed**: no (frozen archive of peer-reviewed-paper code)
* **Relevance**: Provides the canonical frozen version of the deRosenroll 2026 code. Port should
  target this DOI, not the GitHub HEAD.

### [DS-mechanisms-GH]

* **Type**: repository
* **Title**: DS-mechanisms
* **Author/Org**: Alon Poleg-Polsky (CU Anschutz)
* **Date**: 2026-01
* **URL**: https://github.com/PolegPolskyLab/DS-mechanisms
* **Last updated**: 2026-01-27 (`June2025` branch)
* **Peer-reviewed**: no (code repo accompanying peer-reviewed [PolegPolsky2026])
* **Relevance**: Code for Poleg-Polsky 2026. Port target candidate. Contains `main.py`,
  `GA_NEURON.py`, and MOD files for NEURON 8.2 simulations. Missing LICENSE file and no Zenodo
  archive (flags).

### [Hanson-GH]

* **Type**: repository
* **Title**: Spatial-Offset-DSGC-NEURON-Model
* **Author/Org**: Geoff deRosenroll (Awatramani lab, UVic)
* **URL**: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
* **Last updated**: 2019 (stable)
* **Peer-reviewed**: no (code repo accompanying peer-reviewed Hanson 2019)
* **Relevance**: Carry-over from t0008 Phase B. ON-OFF DSGC NEURON compartmental model published
  with Hanson 2019. First priority port because t0008 has already done the boilerplate.

### [RSME-GH]

* **Type**: repository
* **Title**: RSME (Retinal Stimulation Modeling Environment)
* **Author/Org**: NBELab / Rivlin-Etzion group (Weizmann)
* **URL**: https://github.com/NBELab/RSME
* **Peer-reviewed**: no (code repo accompanying peer-reviewed [Ankri2022])
* **Relevance**: Python + NEURON framework for retinal circuits. SAC compartmental model is
  detailed; DSGC is phenomenological. Useful as an integration dependency for simulator-diversity
  suggestions, not as a standalone DSGC port target.

### [ModelDB-189347]

* **Type**: repository
* **Title**: ModelDB accession 189347 — Multiplication by NMDA receptors in Direction Selective
  Ganglion cells (Poleg-Polsky & Diamond 2016)
* **Author/Org**: Alon Poleg-Polsky (ModelDB upload)
* **URL**: https://modeldb.science/189347
* **Last updated**: 2016
* **Peer-reviewed**: no (code repo; companion to peer-reviewed paper)
* **Relevance**: Canonical DSGC model already ported by t0008. Used here only to confirm Pass A
  inclusion bar.

### [ModelDB-267646]

* **Type**: repository
* **Title**: ModelDB accession 267646 — Biophysically Realistic Network Model of the Wild-Type and
  Degenerate Retina (Ly et al. 2022)
* **Author/Org**: Ly et al.
* **URL**: https://modeldb.science/267646
* **Last updated**: 2022
* **Peer-reviewed**: no (code repo; companion to peer-reviewed paper)
* **Relevance**: Whole-retina degeneration network including ON/OFF RGCs. Flagged for triage in
  Recommendation 7.

### [NEURON-docs]

* **Type**: documentation
* **Title**: NEURON Simulation Environment — Publications using NEURON
* **Author/Org**: Hines & Carnevale / Yale
* **URL**: https://www.neuronsimulator.org/en/latest/publications-using-neuron.html
* **Peer-reviewed**: no
* **Relevance**: Cross-checked against the NEURON-publications list to confirm that no additional
  DSGC compartmental models are indexed there beyond the ones found by Pass A / B / C.

### [Hanson2019]

* **Type**: paper
* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson L., Sethuramanujam S., deRosenroll G., Jain V., Awatramani G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **URL**: https://elifesciences.org/articles/42392
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Already in the t0002 corpus; referenced here as the Phase B carry-over port target
  because t0008 flagged but did not complete the port of
  `geoffder/Spatial-Offset-DSGC- NEURON-Model`. The discussion of new post-2020 models is anchored
  to Hanson 2019 as the most recent already-in-corpus baseline.

### [Jain2020]

* **Type**: paper
* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain V., Hanson L., Sethuramanujam S., Michaels T., deRosenroll G., Awatramani G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **URL**: https://elifesciences.org/articles/52949
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Already in the t0002 corpus; referenced here because Pass C's forward-citation walk
  uses Jain 2020 as the most recent corpus anchor and the four-year post-2020 gap is measured
  relative to it.
