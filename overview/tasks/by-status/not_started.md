# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0131 — <strong>rd1-like Na/K remodelling of the DSGC model and its effect
on DSI</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0131_rd1_na_k_remodelling_dsgc_dsi` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0121_5seed_substrate_rate_canonical_report`](../../../overview/tasks/task_pages/t0121_5seed_substrate_rate_canonical_report.md), [`t0129_t0126_signed_dsi_real_rates_1seed`](../../../overview/tasks/task_pages/t0129_t0126_signed_dsi_real_rates_1seed.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Task page** | [rd1-like Na/K remodelling of the DSGC model and its effect on DSI](../../../overview/tasks/task_pages/t0131_rd1_na_k_remodelling_dsgc_dsi.md) |
| **Task folder** | [`t0131_rd1_na_k_remodelling_dsgc_dsi/`](../../../tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/) |

# rd1-like Na/K Remodelling of the DSGC Model and Its Effect on Direction Selectivity

## Motivation

The researcher's preliminary data (`SomeResults.pdf`, repository root, panels A-D) show that
FVB/N rd1 retinal ganglion cells differ from mature wild-type (WT) cells in four ways:
elevated spontaneous activity, weaker evoked spiking, a smaller voltage-gated Na current and a
larger sustained K current. This task tests whether remodelling the soma and AIS conductances
of the existing DSGC model reproduces that phenotype, and what the remodelling does to
direction selectivity (project Research Questions 1 and 4). It also tests the researcher's
much simpler toy model of input-output distortion (panel D) against the compartmental model.

## Calibration Targets (read by eye from the figure, approximate)

| Panel | WT | rd1 |
| --- | --- | --- |
| A: spontaneous, 2 s | Near silent | About 14 spikes in 2 s (~7 Hz), irregular or bursty, ~60 mV tall |
| B: +60 pA step, 500 ms | About 4 adapting spikes (~8 Hz), peaks ~90, 70, 65 mV | Almost no spiking, small blips at onset |
| C: +100 mV voltage step | Sustained outward ~2 nA, early inward Na transient | Sustained outward ~3.5 nA (~1.7x), much smaller inward transient |

If the researcher supplies exact traces, replace these numbers and record the change in
`results_detailed.md`.

## Scope

All runs are local NEURON simulations. No remote machines, cost $0.

* **Reference cells**: 5-10 LEGIT high-DSI cells drawn with a fixed seed from the t0121 pooled
  parquet (dependency `t0121_5seed_substrate_rate_canonical_report`). List the chosen cell
  IDs.
* **Evaluator**: reuse the signed antipodal DSI evaluator and `cell_params.jsonl` per-cell
  parameter dump from `t0129_t0126_signed_dsi_real_rates_1seed`.
* **Conditions**: WT-like (scale 1.0 on gNa and gK) and rd1-like (scaling from Part 1) for
  every reference cell.

## Part 1: Voltage-Clamp Calibration (panel C)

1. Replicate the +100 mV voltage step at the soma on each reference cell.
2. Sweep soma plus AIS gNa scale (0.25-1.0x) against gK scale (1-3x) on a grid of at least 6 x
   6.
3. Choose the rd1-like scaling that matches the sustained-current ratio (~1.7x) and the
   reduced inward transient. Set the scaling from clamp data only; do not use any firing data.
4. Report the fitted scalings per cell and their spread across cells.

## Part 2: Current-Clamp Prediction (panels A and B)

1. With the Part 1 scalings, run the +60 pA, 500 ms step for WT-like and rd1-like cells. This
   is an out-of-sample test: report whether evoked firing collapses as in panel B.
2. For panel A, add a weak tonic bias current or noise at rest (exploratory; any form that
   works is acceptable, but state exactly what was used and how it was tuned). Check whether
   rd1-like cells fire irregularly at ~7 Hz while WT-like cells stay near silent.
3. Report f-I curves, spike amplitude, adaptation index and spontaneous rate for both
   conditions.
4. If soma and AIS scaling alone does not reproduce the phenotype, add a second arm that also
   scales dendritic channels and rerun Parts 1-2 for that arm.

## Part 3: Direction Selectivity

1. Run the standard protocol for WT-like and rd1-like cells: HH on, 8 directions, fixed 1400
   ms trials. Use the EPSP_PASSIVE / IPSP_PASSIVE / FULL mode trio only where the existing
   protocol calls for it.
2. Report signed antipodal DSI = (PD - ND) / (PD + ND), PD rate and ND rate per cell and
   condition, with and without the tonic bias from Part 2.
3. Produce a DSI-versus-scaling heatmap over the Part 1 gNa x gK grid.

## Part 4: Reproduce or Refute Panel D

Panel D is a toy model by the researcher. The same input (three Gaussian pulses at about 180,
430 and 680 ms over 1000 ms) drives a WT-like and an rd1-like cell. Its predictions are:

* WT output grows gradually with input strength (0-100, reaching ~15); rd1 output is flat and
  saturated (~23) at all but the lowest strengths.
* WT output is cleaner and stimulus-locked; rd1 output has an elevated baseline (~0.35),
  broader and less distinct peaks.

Steps:

1. Build the simple toy model (a rate or threshold-type model with WT-like and rd1-like
   parameters) matching this description and check that it reproduces panel D. If it cannot be
   reproduced from the description, state that and list what is missing.
2. Test both predictions in the NEURON model: sweep PD synaptic drive strength and compare the
   WT-like and rd1-like output curves; drive both with the three-pulse input and compare
   baseline, stimulus-locking and peak distinctness.
3. State for each prediction whether it is reproduced, partly reproduced or disproved.

## Key Questions

1. Does Part 1 yield rd1-like scalings that reproduce the panel C current ratio on all
   reference cells?
2. Do those scalings, with no firing data in the fit, collapse evoked firing at +60 pA?
3. Can a tonic bias give ~7 Hz irregular spontaneous firing in rd1-like but not WT-like cells?
4. Does rd1-like remodelling raise, lower or leave unchanged signed DSI, and does the answer
   depend on the tonic bias?
5. Does the compartmental model reproduce the panel D saturation and temporal-smearing
   predictions?

## Expected Outputs

* Charts in `results/images/`, each embedded in `results_detailed.md`:
  * Panel C replication: voltage-clamp current traces, WT-like vs rd1-like (time vs nA).
  * gNa x gK calibration grid: sustained-current ratio and transient amplitude.
  * Current-clamp traces at +60 pA and at rest, WT-like vs rd1-like, and f-I curves.
  * Signed DSI, PD rate and ND rate by condition, plus the DSI-versus-scaling heatmap.
  * Panel D: toy-model reproduction, and NEURON input-strength sweep and three-pulse
    responses.
* One answer asset covering questions 1-5 with the evidence for each.
* Per-cell parameter dump and results tables in `data/`.
* Registered metric: `direction_selectivity_index` (signed), reported per condition as
  variants.

## Dependencies

* `t0121_5seed_substrate_rate_canonical_report`: pooled LEGIT cell parquet used as the
  reference cell source.
* `t0129_t0126_signed_dsi_real_rates_1seed`: signed DSI evaluator and per-cell parameter-dump
  protocol.

## Compute and Budget

Local CPU only, no Vast.ai, no paid APIs. Estimated cost $0. Estimated wall-clock: a few hours
for the clamp grid and DSI runs on 5-10 cells.

## Risks

* Panel values are read by eye; calibration targets are approximate.
* A single-cell model has no presynaptic network, so network-driven rd1 hyperactivity can only
  be represented by an ad hoc bias.
* Soma and AIS scaling may not be enough; the dendritic arm is the planned fallback.

</details>

<details>
<summary>⏹ 0075 — <strong>Biologically-realistic AIS one-axis-at-a-time parameter
sweep on Bed A</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0075_bio_realistic_ais_param_sweep` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0069-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A](../../../overview/tasks/task_pages/t0075_bio_realistic_ais_param_sweep.md) |
| **Task folder** | [`t0075_bio_realistic_ais_param_sweep/`](../../../tasks/t0075_bio_realistic_ais_param_sweep/) |

# Biologically-Realistic AIS Parameter Sweep on Bed A

## Motivation

t0069 attached a virtual AIS plus 1 mm axon stub to Bed A (deposited Poleg-Polsky DSGC) and
re-ran the t0067 channel-addition sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the AIS
instead of the soma. The sweep falsified S-0067-03's prediction (AIS-localised channels show
*larger* DSI effects than soma-localised) — it actually showed the opposite, with 11 of 15
channel conditions producing zero detectable DSI change. The cause was identified clearly: the
AIS+axon halved baseline PD firing (14.2 → 6.4 spikes) and silenced ND firing (1.6 → 0.0),
pushing baseline DSI to the trivial computational ceiling 1.0. The passive AIS+axon adds an
electrical sink that quenches the cell rather than relocating spike initiation; AIS-localised
channels at our densities cannot overcome the somatic 400 mS/cm² HHst Na drive.

The follow-up question this task answers: is there *any* DSGC + AIS configuration that
simultaneously contains all the channels biologically present in a vertebrate AIS (HHst basal
Na+K, Nav1.6, Kv3, Kv7 — the canonical RGC AIS quartet) and produces non-trivial DSI at a
biologically reasonable peak rate? "Decent DSI, not 1, and reasonable firing rate" maps to the
operational pass band {DSI in [0.3, 0.95], peak Hz in [5, 50]}. The right tool is not
optimisation — it is one axis at a time. NaP is excluded from the AIS channel set on two
grounds: (a) AIS NaP expression in RGCs is controversial; (b) the t0067 NaP-high finding (DSI
sign flip) suggests NaP destabilises the DSI mechanism rather than supporting it. BK and SK
are excluded because they localise primarily to soma and dendrites in RGCs, not to the AIS.

This task addresses RQ1 (somatic + AIS VGC combinations) and RQ4 (active vs passive
components). Source suggestions covered: S-0068-04 (move Nav1.6 + Kv3 to AIS), S-0069-01
(halve somatic gnabar before AIS), S-0069-02 (shrink AIS diameter to 0.5 micrometre),
S-0069-03 (vary axon length to probe sink), S-0069-04 (Nav1.6 + Kv3 on AIS at biological
densities).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC) plus virtual AIS + axon stub.
* AIS channel set: **{HHst basal Na + K, Nav1.6, Kv3, Kv7}**. NaP, BK, SK explicitly excluded.
* Encoding: 12-angle bar-rotation protocol (same as t0074 — cross-task comparable).
* Two-stage design: Stage 1 baseline calibration; Stage 2 per-axis sweep.

### Stage 1 — Baseline calibration

* Literature-informed AIS configuration (Wang et al. 2011, Carter et al. 2008 on mouse RGC
  AIS): AIS diameter 0.8 micrometre, AIS length 30 micrometre, axon stub 1.0 mm, AIS
  gnabar_HHst 4 0 0 mS/cm^2, AIS Nav1.6 medium density (~0.3 S/cm^2 from t0067 medium), AIS
  Kv3 medium density (~0.3 S/cm^2), AIS Kv7 low density (~0.1 S/cm^2; distal AIS, weaker than
  Nav and Kv3).
* Sweep soma `gnabar_HHst` across 6 candidates: {100, 150, 200, 250, 300, 400} mS/cm^2 (the
  t0069 baseline = 400).
* 6 candidates x 12 angles x 1 seed = 72 trials, ~5 min wall-clock.
* Pick the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If multiple
  candidates qualify, pick the one closest to the centre of the band ({peak ~ 20 Hz, DSI ~
  0.6}).
* If no candidate qualifies, the task halts at Stage 1 and reports a negative result with a
  recommendation for a follow-up that loosens the AIS configuration further (e.g., reduce AIS
  Nav1.6 density first, then re-attempt).

### Stage 2 — Per-axis sweep

From the Stage-1 baseline, vary one parameter at a time with all others held at baseline:

| # | Axis | Values | Non-baseline points |
| --- | --- | --- | --- |
| 1 | Soma `gnabar_HHst` (mS / cm^2) | {100, 200, 300, 400} | 3 |
| 2 | AIS `gnabar_HHst` (mS / cm^2) | {0, 100, 200, 400, 800} | 4 |
| 3 | AIS diameter (micrometre) | {0.4, 0.6, 0.8, 1.0, 1.5} | 4 |
| 4 | AIS length (micrometre) | {15, 30, 45, 60} | 3 |
| 5 | AIS Nav1.6 density | {0, low, medium, high} | 3 |
| 6 | AIS Kv3 density | {0, low, medium, high} | 3 |
| 7 | AIS Kv7 density | {0, low, medium, high} | 3 |
| 8 | Axon length (mm) | {0.1, 0.5, 1.0, 2.0} | 3 |

Total Stage-2 conditions: 1 baseline + 26 non-baseline = **27 conditions x 12 angles x 5 seeds
= 1620 FULL trials**, ~100 min wall-clock at the t0067 measured ~3.75 s / trial under CVODE.

### Width metrics per axis (cross-comparable with t0074)

For each condition, compute:

* **HWHM** in degrees from the 12-angle tuning curve.
* **Vector-sum DSI** (circular concentration).
* **Peak rate (Hz)** at the angle with maximum mean rate.
* Rate at PD (axis-1 peak angle) and at the opposite angle.
* RMSE vs the t0004 cosine target.

### Outputs

* **Library asset**: `bed_a_with_bio_realistic_ais` — Bed A + AIS + axon model variant with
  the {HHst, Nav1.6, Kv3, Kv7} channel set wired in. Reusable by future tasks that need a
  working DSGC + AIS substrate.
* **Stage 1 candidate table** (`results/baseline_candidates.csv`) with 6 rows showing
  soma_gnabar_HHst, peak Hz, DSI, in-band y/n.
* **Stage 2 per-axis sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI,
  peak rate, RMSE vs cosine target, plotted against axis values.
* **Biologically-plausible AIS recommendation table**
  (`results/biological_ais_recommendation.md`): the band-constrained range for each axis (the
  values that keep the cell inside {DSI [0.3, 0.95], peak [5, 50] Hz}), plus a recommended
  canonical configuration.
* `results/metrics.json` with registered project metrics per condition.

## Approach

1. Fork t0069's AIS-attachment code into this task's `code/`. Replace the t0069
   channel-addition loop with the {HHst, Nav1.6, Kv3, Kv7} baseline channel set (with
   t0074-vendored Kv7).
2. Implement Stage 1 calibration as a 6-candidate sweep with explicit pass-band check and
   automated baseline selection.
3. Implement Stage 2 as 8 per-axis sweep functions sharing a common driver.
4. Run Stage 1, log selected baseline, run Stage 2.
5. Compute width metrics, generate per-axis plots, write the recommendation table.
6. Validate against t0069 sanity checks: trials with instability flags = 0, peak Vm bounded.

## Pass Criteria

* Stage 1 finds at least one in-band baseline (peak Hz in [5, 50] AND DSI in [0.3, 0.95]).
* All 1620 + 72 trials complete with no instability flags.
* Per-axis sensitivity plots show monotonic or unimodal sensitivity for at least 6 of the 8
  axes (the axes that don't are flagged as candidates for re-investigation; not a hard fail).
* Recommendation table produced with the band-constrained range for each axis.

## Compute Estimate

* ~2 h wall-clock on local CPU. 72 trials Stage 1 (~5 min) + 1620 trials Stage 2 (~100 min) +
  ~10 min plotting / metrics extraction.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code (Nav1.6, Kv3
  implementation patterns).
* `t0069_t0067_ais_localised_channel_sweep` — AIS attachment code; baseline characterisation
  of the passive-AIS sink effect.
* `t0074_channel_tuning_width_bed_a` — Kv7 MOD vendoring lands in t0074. This task inherits
  the vendored Kv7 mechanism and the calcium-pool unification (the latter is not actively used
  here but must remain compatible).

## Risks and Fallbacks

* **Stage 1 finds no in-band baseline**: the task halts after Stage 1 and reports a negative
  result with a follow-up recommendation. Time-cheap (~5 min). The follow-up would probably be
  a 2D Stage 1.5 sweep over {soma gnabar, AIS gnabar} or a baseline that further reduces AIS
  Nav1.6 density.
* **Stage 1 is over-fitted to soma_gnabar**: if the baseline soma_gnabar value is borderline
  (e.g., exactly at the edge of the in-band region), small parameter changes in Stage 2 may
  push the cell out of band rapidly. Mitigation: pick the Stage-1 baseline closest to the band
  centre, not the band edge.
* **Axes interact strongly**: the one-axis-at-a-time design assumes weak interactions. If a
  Stage-2 axis sweep produces non-monotonic behaviour (e.g., DSI rises then falls), report the
  non-monotonicity explicitly and flag the axis for a future joint sweep with one neighbouring
  axis.
* **AIS+axon discretisation artefacts**: if the segment count along the AIS or axon is too
  low, spike initiation and propagation may be artefactual. Mitigation: use NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) and validate that the
  chosen segment count doubles without changing peak Vm by more than 1 mV at the t0069
  baseline.

## Out of Scope

* Bed B (de Rosenroll) — explicitly out of scope per researcher decision; this task is Bed A
  only.
* Joint multi-axis optimisation — explicitly excluded; this is one-axis-at-a-time only.
* Other AIS channel candidates (Nav1.2, Kv1, Kv4 alpha-DTX-sensitive subtype) — out of scope;
  the channel set is fixed at {HHst, Nav1.6, Kv3, Kv7}. Future follow-ups may extend the
  channel set.

</details>

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
