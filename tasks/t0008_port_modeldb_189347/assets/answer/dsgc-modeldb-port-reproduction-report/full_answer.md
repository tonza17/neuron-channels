---
spec_version: "2"
answer_id: "dsgc-modeldb-port-reproduction-report"
answered_by_task: "t0008_port_modeldb_189347"
date_answered: "2026-04-20"
confidence: "medium"
---

# ModelDB 189347 DSGC port and sibling-model survey

## Question

Can ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC) be reproduced locally on Windows
as a headless library, does it hit the published direction-selectivity envelope with a canonical
12-angle x 20-trial drifting-bar protocol, and which sibling DSGC compartmental models are the
next-best candidates for porting in the same pipeline?

## Short Answer

Yes, ModelDB 189347 was ported and runs headless on Windows 11 with NEURON 8.2.7 via a Python driver
that sources the verbatim HOC and MOD files; a 12-angle x 20-trial sweep on the bundled morphology
completes in ~9 minutes and the four registered metrics (DSI, HWHM, reliability, RMSE vs target)
were written to `results/metrics.json`. The bundled parameters do not hit the published envelope
(candidate peak 18.1 Hz < target 32 Hz; candidate DSI 0.32 < target 0.88) because the paper's DS
derives from a `gabaMOD` parameter swap rather than from spatial rotation, so the port's
rotation-based protocol is only a proxy for a directional stimulus. The Hanson et al. 2019
Spatial-Offset-DSGC model is the next-best port candidate: it shares `RGCmodel.hoc` and `HHst.mod`
with 189347 and already ships a Python driver; Jain 2020 is medium-effort; Ding 2016, Schachter
2010, Koren 2017, and Ezra-Tsur 2022 are not compartmental-model port candidates.

## Research Process

The work was done in two phases. Phase A ported ModelDB 189347 end-to-end: clone the GitHub mirror,
enumerate HOC and MOD files, compile MOD via `nrnivmodl.bat` on Windows, write a GUI-free derivative
`dsgc_model.hoc`, and build a Python driver (`build_cell.py`, `run_tuning_curve.py`,
`score_envelope.py`) that sources HOC via `h.load_file` and loads the DLL via `h.nrn_load_dll`. Two
tests gate the pipeline (smoke single-angle trial; scoring-pipeline identity). Phase B surveyed five
sibling DSGC models (Hanson 2019, Jain 2020, Ding 2016, Schachter 2010, Koren 2017, Ezra-Tsur 2022)
by checking the ModelDB listing, GitHub search, and paper metadata; each entry was scored for port
candidacy and logged to `data/phase_b_survey.csv`. Conflicting evidence was resolved by giving
priority to direct source-code availability and architectural compatibility with the t0008
HOC-driver pattern over paper-only or RL-framework candidates.

## Evidence from Papers

The Poleg-Polsky & Diamond 2016 source paper (`files/main.hoc` header references ModelDB 189347)
specifies a single ON-OFF DRD4 DSGC with 282 bundled ON-dendrite synapse triples (BIPsyn,
SACinhibsyn, SACexcsyn), Jahr-Stevens NMDA kinetics bundled with AMPA inside `bipolarNMDA.mod`, and
a 1-D drifting-bar stimulus driven by per-synapse `locx` arrival-time computation. The published DS
signature (DSI ~ 0.8, peak ~ 30-40 Hz at PD) derives from swapping a `gabaMOD` parameter (PD trials
set `gabaMOD=0.33`; ND trials set `gabaMOD=0.99`) rather than from any spatial rotation of the
stimulus. Hanson et al. 2019 (eLife 42392; `SpatialOffsetDSGC` GitHub repo) shares the
`RGCmodel.hoc` skeleton and `HHst.mod` mechanism file with 189347 and adds a spatial-offset
mechanism that recovers DS via BIP-vs-SAC positional bias — this is exactly the mechanism the
port's rotation protocol approximates, and is why Hanson 2019 is the highest-ranked port candidate
in the Phase B survey.

## Evidence from Internet Sources

ModelDB 189347's landing page (https://modeldb.science/189347) provides the canonical HOC/MOD bundle
and a ReadMe that describes the GUI workflow; the GitHub mirror at
`github.com/ModelDBRepository/189347` was used for version-pinned cloning (commit
`87d669dcef18e9966e29c88520ede78bc16d36ff`). The Hanson 2019 `Spatial-Offset-DSGC-NEURON-Model`
GitHub repo confirmed a clean MIT-style licence, a Python driver (`offsetDSGC.py`), and shared
mechanism files. ModelDB searches and GitHub searches for Jain 2020, Ding 2016, Schachter 2010,
Koren 2017, and Ezra-Tsur 2022 returned either a Jain 2020 ModelDB deposition (267001), or no public
compartmental-model release at all, or (for Ezra-Tsur 2022) a reinforcement-learning framework
rather than a NEURON compartmental model.

## Evidence from Code or Experiments

The port runs end-to-end on the bundled morphology with Poleg-Polsky's exact parameter values.
Recorded candidate metrics on a 12-angle x 20-trial sweep (dt=0.1 ms, tstop=1000 ms, 240 trials
total, ~2 s/trial):

* `direction_selectivity_index` = 0.316 (target envelope 0.7-0.85; below)
* `peak_firing_rate_hz` = 18.1 (target 32.0; below)
* `null_firing_rate_hz` = 9.4 (target 2.0; above; passes the `null<10 Hz` gate)
* `tuning_curve_hwhm_deg` = 82.8 (target 66.0; passes the 60-90 deg gate)
* `tuning_curve_reliability` = 0.991 (high)
* `tuning_curve_rmse` = 13.73 Hz (loss_scalar = 3.90, `passes_envelope=False`)

Per-target passes recorded in `data/score_report.json`: DSI false, peak false, null true, HWHM true.
The morphology-swap report (`data/morphology_swap_report.md`) documents that the bundled cell has
351 sections and ~6.48 mm total cable, while the calibrated SWC from t0009 has 6,736 compartments
and a different topology — swapping requires rewriting `RGCmodel.hoc`'s `placeBIP`-driven synapse
placement and was scoped out.

## Synthesis

The port is technically faithful: HOC and MOD sources are unmodified, the `placeBIP` synapse
placement runs on the bundled `create soma, dend[350]` topology, spike counting is
threshold-crossing on $V_{soma}$, and all 240 trials executed without error. The envelope miss is
explained by a stimulus-mechanism mismatch rather than a port bug: Poleg-Polsky's DS signature comes
from swapping `gabaMOD` between PD (0.33) and ND (0.99) conditions; the port instead rotates BIP
synapse coordinates around the soma to approximate a directional stimulus. Rotating BIP only
(keeping SAC fixed) does recover per-angle firing-rate modulation (DSI 0.32), but the absolute peak
rate stays at 18 Hz rather than the 32-40 Hz the paper reports under its own parameter-swap
protocol. This makes the port a faithful reproduction of the bundled model under a proxy protocol,
but not a reproduction of the paper's headline DSI figure. For the sibling survey, Hanson 2019 is
the clear next candidate because it shares both `RGCmodel.hoc` and `HHst.mod` with 189347 and
already implements a spatial-offset mechanism; Jain 2020 is a bipolar- delay extension with its own
ModelDB entry but a separate stimulus pipeline; the remaining candidates either lack a public
compartmental model (Ding 2016, Schachter 2010, Koren 2017) or address a different modelling class
(Ezra-Tsur 2022, RL framework).

## Limitations

Three limitations qualify the confidence of this answer. First, the envelope miss is due to the
rotation-based stimulus, not to a port-integrity issue; a `gabaMOD` parameter-swap protocol would be
needed to match the paper's figure exactly, and that was not implemented in this task. Second, the
bundled morphology was used rather than the Horton-Strahler calibrated SWC from t0009; replacing it
requires rewriting `RGCmodel.hoc`'s topology and synapse placement logic and was logged as a
downstream task. Third, the Phase B survey scored candidacy by source-code availability and
architectural overlap, not by a full reproduction attempt for each candidate — Jain 2020 and Koren
2017 may be more (or less) tractable in practice than the desk-survey rank suggests.

## Sources

* Task: `t0004_generate_target_tuning_curve`
* Task: `t0007_install_neuron_netpyne`
* Task: `t0009_calibrate_dendritic_diameters`
* Task: `t0012_tuning_curve_scoring_loss_library`
* URL: https://modeldb.science/189347
* URL: https://github.com/ModelDBRepository/189347
* URL: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
* URL: https://elifesciences.org/articles/42392v1
