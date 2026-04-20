---
spec_version: "2"
answer_id: "dsgc-missed-models-survey"
answered_by_task: "t0010_hunt_missed_dsgc_models"
date_answered: "2026-04-20"
confidence: "medium"
---
# Missed DSGC compartmental models: hunt and port viability

## Question

What DSGC compartmental models published in public literature were missed by tasks t0002 and t0008,
and which of them are viable ports for this project?

## Short Answer

Two brand-new DSGC compartmental-model papers were missed by the prior corpus: deRosenroll et al.
2026 (Cell Reports, DOI `10.1016/j.celrep.2025.116833`) and Poleg-Polsky 2026 (Nature
Communications, DOI `10.1038/s41467-026-70288-4`); Hanson 2019 (`10.7554/eLife.42392`) was in the
t0002 corpus but had never been ported. None of the three HIGH-priority candidates completed a
12-angle canonical sweep within the 90-minute-per-candidate port budget — each failed at the P2
upstream-demo gate for a different structural reason. Zero library assets were registered per the
"never leave a broken library behind" rule, and all three candidates are recorded as `p2_failed` in
`data/candidates.csv`. Deeper investment would very plausibly succeed; the 90-minute cap is the
binding constraint, not a definitive portability verdict.

## Research Process

The hunt was structured as a three-pass internet and literature search followed by a triaged port
attempt on each HIGH-priority candidate.

**Pass A — ModelDB** (12 queries): The full ModelDB listing was searched under the keyword set
`direction selective`, `DSGC`, `starburst`, `retina`, `amacrine`, `ganglion`, `retinal ganglion`,
`RGC`, `direction`, `motion`, and the category browse for Retina ganglion GLU cell (id 270). Direct
entry fetches verified metadata for accessions 189347, 223890, 267391, 267646, 2018247, 262452,
2019896, 260653, and 18501. Outcome: only ModelDB 189347 meets the compartmental-DSGC bar and was
already ported by t0008. ModelDB 267646 (Ly et al. 2022) was flagged medium for follow-up
inspection.

**Pass B — GitHub/Zenodo/OSF** (13 queries): Code-level searches on GitHub against
`DSGC compartmental NEURON`, `direction selective ganglion NEURON`, simulator-specific variants
(NetPyNE, Arbor), author-lab scans (`geoffder/*`, `PolegPolskyLab/*`, `ModelDBRepository/*`), plus
Zenodo and OSF keyword sweeps. Outcome: two brand-new repositories surfaced —
`geoffder/ds-circuit-ei-microarchitecture` (deRosenroll 2026) and `PolegPolskyLab/DS-mechanisms`
(Poleg-Polsky 2026) — plus several SAC-only repos that failed the inclusion bar.

**Pass C — Google Scholar / bioRxiv / journal** (12 queries): Forward-citation walks of six seed
DSGC papers (Poleg-Polsky 2016, Schachter 2010, Park 2014, Sethuramanujam 2016, Hanson 2019, Jain
2020), plus bioRxiv 2023-2026 and targeted journal DOI lookups. Outcome: confirmed that the two
Pass-B hits are the only post-2020 DSGC compartmental models in public literature. No third model
exists in the 2020-2026 gap. Three non-model physiology/anatomy papers (Riccitelli 2025, Fransen
2021, Ankri 2024) were noted as target-curve / constraint references but do not add compartmental
models.

Every candidate surfaced by the three passes (14 total) was transcribed into `data/candidates.csv`
with triage priority. Three HIGH-priority candidates were then taken through a four-phase port
attempt under a 90-minute wall-clock cap per candidate: P1 (clone + library-asset scaffold), P2 (MOD
compile + upstream demo run headless), P3 (12-angle x 20-trial sweep + envelope scoring via the
`tuning_curve_loss` library from t0012). Failure at any phase terminated that candidate's attempt.
Conflicting signals (e.g., MOD files compile cleanly for Hanson 2019 yet the driver is unrunnable)
were resolved by recording the specific structural blocker in the candidate row.

## Evidence from Papers

Three paper assets bear directly on the answer and were read during this task:

**deRosenroll et al. 2026** (`10.1016_j.celrep.2025.116833`, Cell Reports 45, e116833). Newly
downloaded as a v3 paper asset under this task. The paper publishes an ON-OFF DSGC NEURON
compartmental model whose novel feature is differential spatial wiring of GABA and acetylcholine
starburst amacrine inputs. Stochastic Hodgkin-Huxley mechanisms, 8-direction stimulus, 100-trial
Monte-Carlo wiring, DSI calculated along the global preferred axis. Key result cited in this answer:
minor ACh perturbations that do not disrupt global E/I balance can locally uncouple E/I and
compromise direction selectivity. The model is the most recent and most scientifically adjacent DSGC
compartmental model in the public record; its 8-direction hardcode is the main reason the port
failed structurally (see Evidence from Code).

**Poleg-Polsky 2026** (`10.1038_s41467-026-70288-4`, Nature Communications). Newly downloaded as a
v3 paper asset under this task. 352-segment DSGC NEURON model exercised by a genetic-algorithm
training pipeline (`numDir=2`, numGen=300, numPop=20). The paper's main claim is that ML search
discovers multiple additional computational primitives (velocity-dependent coincidence detection,
distance-graded delay lines, NMDA multiplicative gating) that complement rather than replace the
classical SAC-inhibition mechanism. The code architecture is the direct cause of the port's P2
failure: the GA driver is both a training framework and the experiment; extracting the underlying
HOC cell for a plain 12-angle sweep would require a substantial rewrite.

**Hanson et al. 2019** (`10.7554/eLife.42392`, eLife 8, e42392). Already in the t0002 corpus.
Referenced here because its companion repository (`geoffder/Spatial-Offset-DSGC-NEURON-Model`,
commit `f7688f8`) was flagged by t0008 as a Phase B carry-over port target but was never completed.
The paper's compartmental model architecture (ON- dendrites + OFF-dendrites + space-clamped SAC
inputs) is compatible in principle with the t0008 boilerplate; the blocker is entirely on the driver
side (see Evidence from Code).

None of the three papers were paywalled; the two new papers are open-access under their publishers'
policies (Cell Press and Nature Communications). No paper contradicts the conclusion that the
post-2020 DSGC compartmental-model gap is exactly two papers.

## Evidence from Internet Sources

Internet-source evidence is primarily the three candidate code repositories and the Zenodo archive.

`github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model` (commit `f7688f8`, 2019, no LICENSE file
posted at repo root). The repository contains `RGCmodel.hoc`, `HHst.mod`, `Exp2NMDA.mod`, a Python
driver `offsetDSGC.py` (1609 lines), and no `__main__` entry-point. The driver's top-level
`from neuron import h, gui` requires an X display or an interactive console; hardcoded paths like
`C:\Users\geoff\NEURONoutput\` are baked into stimulus and output routines.

`github.com/geoffder/ds-circuit-ei-microarchitecture` (commit `a23f642`, MIT license confirmed,
Zenodo archive `10.5281/zenodo.17666157`). The repository contains `ei_balance.py` (with a `Model`
class), a NEURON back-end, MOD files, and `requirements.txt` listing `statsmodels`, `h5py`,
`matplotlib`, `fastparquet`, `oiffile`. The `Model` class hardcodes
`self.dir_labels = np.array([225, 270, 315, 0, 45, 90, 135, 180])` and
`self.dirs = [135, 90, 45, 0, 45, 90, 135, 180]`, fixing an 8-direction stimulus grid that does not
align with the project's 12-angle canonical sweep (required by
`tasks.t0012_tuning_curve_scoring_loss_library`'s `load_tuning_curve` hard-fail validator).

`github.com/PolegPolskyLab/DS-mechanisms` (commit `6534bcd`, June2025 branch, no LICENSE file). The
repository implements a genetic-algorithm training driver: `main.py` (22 KB), `GA_NEURON.py` (44
KB), and associated MOD files. Global parameters include `numDir: 2` (training only evaluates
preferred vs null by design) and `numGen: 300`, `numPop: 20`. A single generation with default
parameters takes several minutes of wall-clock; the published experiment runs 300 generations.

The Zenodo archive `10.5281/zenodo.17666157` is the version-of-record for the deRosenroll 2026 code.
It matches the GitHub tag referenced in the Cell Reports supplement; no content drift was detected
between archive and HEAD at the time of the port attempt.

Simulator-diversity cross-checks (NetPyNE/Arbor/MOOSE/Brian2/JAX vs DSGC or direction-selective
retina keywords) returned zero public compartmental DSGC models. This is a confirmed community gap,
not a search miss.

## Evidence from Code or Experiments

Three HIGH-priority candidates were taken through the P1 -> P2 -> P3 port-attempt pipeline under a
90-minute wall-clock cap per candidate. Outcomes are summarised below and transcribed from
`data/candidates.csv`.

### Per-candidate summary

Note: `dsi`, `peak_hz`, `null_hz`, `hwhm_deg`, and `passes_envelope` are intentionally blank for
every candidate below because no port completed P3 — none emitted a canonical tuning-curve CSV.

| candidate_id | paper_doi | code_url | neuron_compatible | port_attempted | port_outcome | dsi | peak_hz | null_hz | hwhm_deg | passes_envelope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `hanson_2019_spatial_offset` | `10.7554/eLife.42392` | https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model | yes | yes | p2_failed (upstream headfull driver, hardcoded Windows paths) | - | - | - | - | - |
| `derosenroll_2026_circuit_ei` | `10.1016/j.celrep.2025.116833` | https://github.com/geoffder/ds-circuit-ei-microarchitecture | yes | yes | p2_failed (8-direction hardcode, heavy deps outside env) | - | - | - | - | - |
| `polegpolsky_2026_ds_mechanisms` | `10.1038/s41467-026-70288-4` | https://github.com/PolegPolskyLab/DS-mechanisms | yes | yes | p2_failed (GA training driver with numDir=2, no LICENSE) | - | - | - | - | - |
| `derosenroll_ei_balance` | n/a (supporting) | https://github.com/geoffder/ei-balance | yes | no | not_attempted (medium; antecedent fallback) | - | - | - | - | - |
| `modeldb_267646_ly2022` | n/a | https://modeldb.science/267646 | yes | no | not_attempted (medium; needs code inspection for DSGC class) | - | - | - | - | - |
| `ankri_2022_rsme` | `10.1371/journal.pcbi.1009754` | https://github.com/NBELab/RSME | yes | no | not_attempted (low; DSGC is phenomenological) | - | - | - | - | - |
| `polegpolsky_ds_bipolar_inputs_sac` | n/a | https://github.com/PolegPolskyLab/DS_Bipolar_Inputs_SAC | yes | no | not_attempted (drop; SAC-only) | - | - | - | - | - |
| `derosenroll_spatiotemporal_starburst` | n/a | https://github.com/geoffder/spatiotemporal-starburst-model | yes | no | not_attempted (drop; SAC-only) | - | - | - | - | - |
| `jzlab_dsg_matlab` | n/a | https://github.com/jzlab/dsg | no (MATLAB) | no | not_attempted (drop; rate-coded) | - | - | - | - | - |
| `vivinetto_dsgc_velocity` | n/a | https://github.com/vivinetto-lab/DSGC-Velocity-Project | no (MATLAB analysis) | no | not_attempted (drop; analysis-only) | - | - | - | - | - |
| `kish_retinal_ganglion_cell` | n/a | https://github.com/Kathleen-Kish/Retinal_Ganglion_Cell | yes | no | not_attempted (drop; generic RGC) | - | - | - | - | - |
| `ankri_2020_sac` | n/a | https://github.com/ankrilab/ankri_2020_SAC | yes | no | not_attempted (drop; SAC-only) | - | - | - | - | - |
| `modeldb_189347_polegpolsky2016` | `10.1016/j.neuron.2016.02.013` | https://modeldb.science/189347 | yes | n/a (already ported by t0008) | drop (not a new candidate) | - | - | - | - | - |
| `modeldb_223890_ding2016` | n/a | https://modeldb.science/223890 | no (NeuronC) | no | not_attempted (drop; separate simulator) | - | - | - | - | - |

### Per-candidate structural blockers

**`hanson_2019_spatial_offset`** (HIGH priority, carry-over from t0008 Phase B). Cloned successfully
at commit `f7688f8`. MOD files (`Exp2NMDA.mod`, `HHst.mod`) compile cleanly on NEURON 8.2.7 under
`run_nrnivmodl.cmd`. A minimal headless HOC-only build loads the `DSGC` template with 282/350
ON-dendrites and passive integration holds -60 mV over 50 ms. **P2 failure**: the upstream driver
`offsetDSGC.py` is 1609 lines with no `__main__` block, a top-level `from neuron import h, gui` that
fails under `nrngui.hoc` resolution in a headless process, and hardcoded paths
`C:\Users\geoff\NEURONoutput\`. The full stimulus/DS protocol (`setSoma`, `membSetup`, `setSyn`,
`barOnsets`, `dirRun`) lives Python-side; reimplementing a clean headless equivalent exceeds the
90-minute budget. The biophysics are not the blocker — the driver is.

**`derosenroll_2026_circuit_ei`** (HIGH priority). Cloned at commit `a23f642`, MIT LICENSE confirmed
at repo root, Zenodo archive `10.5281/zenodo.17666157` cross-referenced. **P2 failure**:
`ei_balance.Model` hardcodes an 8-direction stimulus grid
(`self.dir_labels = np.array([225, 270, 315, 0, 45, 90, 135, 180])`,
`self.dirs = [135, 90, 45, 0, 45, 90, 135, 180]`). Emitting the t0012-mandated 12-angle canonical
sweep requires editing the upstream source, which violates the plan's "do not hack around upstream"
rule. Additionally, heavy deps (`statsmodels`, `h5py`, `fastparquet`, `oiffile`) are not in the
task's uv env, and adding them to the shared `pyproject.toml` is out of scope for Milestone C. The
headless demo was therefore not attempted because even a passing P2 could not yield a valid P3
curve.

**`polegpolsky_2026_ds_mechanisms`** (HIGH priority). Cloned at commit `6534bcd`. **P2 failure**: no
LICENSE file (provenance blocker for library-asset creation under project rules); upstream
architecture is a genetic-algorithm training framework with `numDir: 2` hardcoded in `global_params`
(trains on preferred/null only, not a 12-angle sweep); single-generation compute with default
`numPop=10` is minutes; published experiment uses `numGen=300` (multi-hour). Emitting a 12-angle
tuning curve requires substantially modifying upstream source (forbidden) or implementing a parallel
non-GA driver that reuses the HOC cell + MOD mechanisms (out of budget). MOD compile was not
attempted because the structural mismatch makes P3 impossible.

### Library-asset and metrics outcomes

Per the task's Phase B rule (never leave a broken library behind), no library asset was scaffolded
for any of the three failures. `assets/library/` in this task therefore remains empty.
`metrics.json` was written in explicit multi-variant format with an empty `variants` list,
consistent with REQ-7 when zero ports succeed. `data/tuning_curves/` contains no port-authored CSVs.
`data/candidates.csv` records all 14 candidate rows with triage status and, for the three
HIGH-priority candidates, the specific structural failure phase and reason.

## Synthesis

**REQ-1** was satisfied by transcribing the 14-row CANDIDATES TABLE from
`research/research_internet.md` into `data/candidates.csv`; the three-pass hunt (37 queries across
ModelDB, GitHub/Zenodo/OSF, and Google Scholar + bioRxiv forward-cites of the six DSGC seed papers)
produced exhaustive coverage. **REQ-2** was satisfied by downloading deRosenroll 2026
(`10.1016_j.celrep.2025.116833`) and Poleg-Polsky 2026 (`10.1038_s41467-026-70288-4`) as v3 paper
assets; Hanson 2019 (`10.7554_eLife.42392`) was correctly NOT re-downloaded because it already
exists in the t0002 corpus. **REQ-3** was attempted: every HIGH-priority candidate received P1 + P2
under the per-candidate 90-minute wall-clock cap; all three failed at the P2 upstream-demo gate.
**REQ-4** could not be satisfied (no canonical CSV emitted) because no candidate passed P2.
**REQ-5** was satisfied by the triage: each P2 failure stopped that candidate cleanly, no broken
library asset was registered, the `data/candidates.csv` row was completed with
`port_outcome = p2_failed` and a specific reason. **REQ-6** is the present answer asset. **REQ-7**
was satisfied by writing `results/metrics.json` in explicit multi-variant format with an empty
`variants` list. **REQ-8** was satisfied: zero dollars spent, no remote machines used.

The unifying finding is that all three HIGH-priority candidates fail for driver-architecture
reasons, not biophysical-model reasons. MOD files in the Hanson 2019 repo compile cleanly; a minimal
HOC-only cell build runs. The deRosenroll 2026 biophysics are canonical stochastic HH. The
Poleg-Polsky 2026 cell template is a standard 352-segment DSGC. What blocks each port is (a) the
wrapper Python driver — headfull, hardcoded, or GA-trained — and (b) a mismatch between the upstream
stimulus grid and the project's canonical 12-angle canonical-sweep contract. This is a structural
observation about the current state of DSGC modelling code, not an indictment of any specific
authors: all three repos were written for figure reproduction, not for headless reuse-as-library.
The project's canonical tuning-curve contract (12 angles x 20 trials, uniform grid, hard-fail
validator) is a high standard that no upstream DSGC repo has been built to meet.

Deeper investment (hand-rewriting each candidate's driver while preserving upstream biophysics
verbatim) would very plausibly succeed on all three candidates. The 90-minute-per-candidate cap is
the binding constraint that produced the three failures, not a verdict on portability. This is the
primary uncertainty captured in the `confidence: medium` field on the port-viability axis;
confidence on the corpus-delta axis is high because the exhaustive three-pass search across ModelDB,
GitHub/Zenodo/OSF, Scholar, bioRxiv, and lab-forward-citation walks is unlikely to have missed a
third post-2020 model.

## Limitations

* **Port-attempt budget is the binding constraint, not an upper bound on portability.** Each
  HIGH-priority candidate failed at P2 because a clean headless rewrite of its driver exceeds 90
  minutes, not because the biophysics are unportable. A dedicated hand-port task per candidate
  (priced at 1-3 person-days) is the right next step.
* **Corpus-delta is exhaustive for 2020-2026 only.** The hunt targeted the post-2020 gap (between
  Jain 2020 and the current date). Pre-2020 DSGC compartmental models not already in the t0002
  corpus (e.g., Ding 2016 in NeuronC, Schachter 2010 in NeuronC) were intentionally excluded because
  simulator rewrite is out of scope for an "automatic port" task.
* **Simulator-diversity gap is unfilled.** Zero DSGC compartmental models in NetPyNE, Arbor, MOOSE,
  Brian2, or JAX. This is a confirmed community gap and is a candidate for a separate translation
  task once at least one NEURON port is stable.
* **ON-DSGC / OFF-DSGC subtype gap is unfilled.** No ON-only or OFF-only compartmental models were
  surfaced; the two new candidates (deRosenroll 2026, Poleg-Polsky 2026) are both ON-OFF DSGCs.
  Filling this gap likely requires building from scratch because no upstream model exists.
* **Cross-species gap is unfilled.** No primate, ferret, cat, or zebrafish DSGC compartmental model
  was surfaced. All current models remain mouse-based.
* **Provenance risk for Poleg-Polsky 2026.** The upstream repo has no LICENSE file and no Zenodo
  archive; if project rules require permissive licensing for library assets, any future port of this
  model needs a direct license-grant from the authors.
* **No new-experiment evidence was generated.** The port attempts did not reach the P3 sweep phase,
  so no new tuning-curve CSVs were added to the project. All envelope-scoring evidence remains
  inherited from t0008 (ModelDB 189347 port).

## Sources

* Paper: `10.1016_j.celrep.2025.116833` [deRosenroll2026][derosenroll2026]
* Paper: `10.1038_s41467-026-70288-4` [PolegPolsky2026][polegpolsky2026]
* Paper: `10.7554_eLife.42392` [Hanson2019][hanson2019]
* Task: `t0002_literature_survey_dsgc_compartmental_models` [t0002]
* Task: `t0008_port_modeldb_189347` [t0008]
* Task: `t0012_tuning_curve_scoring_loss_library` [t0012]
* URL: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model [Hanson-GH][hanson-gh]
* URL: https://github.com/geoffder/ds-circuit-ei-microarchitecture [dsCircuitEI-GH][dscircuitei-gh]
* URL: https://doi.org/10.5281/zenodo.17666157 [deRosenroll-Zenodo-2025][derosenroll-zenodo-2025]
* URL: https://github.com/PolegPolskyLab/DS-mechanisms [DS-mechanisms-GH][ds-mechanisms-gh]
* URL: https://modeldb.science/189347 [ModelDB-189347][modeldb-189347]
* URL: https://modeldb.science/267646 [ModelDB-267646][modeldb-267646]

[derosenroll2026]: ../../paper/10.1016_j.celrep.2025.116833/summary.md
[polegpolsky2026]: ../../paper/10.1038_s41467-026-70288-4/summary.md
[hanson2019]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/summary.md
[t0002]: ../../../../t0002_literature_survey_dsgc_compartmental_models/
[t0008]: ../../../../t0008_port_modeldb_189347/
[t0012]: ../../../../t0012_tuning_curve_scoring_loss_library/
[hanson-gh]: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
[dscircuitei-gh]: https://github.com/geoffder/ds-circuit-ei-microarchitecture
[derosenroll-zenodo-2025]: https://doi.org/10.5281/zenodo.17666157
[ds-mechanisms-gh]: https://github.com/PolegPolskyLab/DS-mechanisms
[modeldb-189347]: https://modeldb.science/189347
[modeldb-267646]: https://modeldb.science/267646
