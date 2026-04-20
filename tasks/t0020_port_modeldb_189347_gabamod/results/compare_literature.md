---
spec_version: "1"
task_id: "t0020_port_modeldb_189347_gabamod"
date_compared: "2026-04-20"
---
# Comparison with Published Results

## Summary

This reproduction of the Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC under the paper's native
two-condition `gabaMOD` parameter-swap protocol (PD = 0.33, ND = 0.99) achieves **DSI 0.7838** —
squarely inside the literature envelope **[0.70, 0.85]** and **+0.468** above the t0008
rotation-proxy DSI of 0.316 — but the **peak firing rate (14.85 Hz)** remains well below the
envelope **[40, 80] Hz**, so the combined two-point envelope gate fails. The split is informative:
the gabaMOD mechanism cleanly recovers the direction-selectivity *contrast* reported by
`[PolegPolsky2016]`, while the peak-rate shortfall — previously entangled with the rotation-proxy
protocol mismatch in t0008 — is now unambiguously localised to the excitation side of the port.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Poleg-Polsky 2016 [PolegPolsky2016, Figs 1G/4F/5G/6G/8E boxplot median] | DSI (median, noise-free control, spike output) | **0.80** | **0.7838** | -0.0162 | Paper reports DSI as median+/-quartile boxplots without a single aggregate number; qualitative headline **~0.8** taken from figure medians. Our protocol is the paper's native `gabaMOD` swap (PD=0.33, ND=0.99), matching the paper's direction-selectivity driver. |
| Poleg-Polsky 2016 [PolegPolsky2016, p. 1281 Exp Procedures] | Preferred-direction peak firing rate (Hz) | **40-80** (project-literature envelope; not numerically reported in the paper) | **14.85** | -25.15 (vs envelope floor 40) | `[PolegPolsky2016]` does not report a numeric peak firing rate anywhere in text or figures. The 40-80 Hz envelope floor is the project target drawn from broader DSGC literature consensus; comparison is to the envelope floor, not to a paper-verbatim number. |
| Poleg-Polsky 2016 [PolegPolsky2016, Fig 1D, n = 19] | PD NMDAR-mediated PSP component (mV) | **5.8 +/- 3.1** | not measured | — | Subthreshold validation target from patch-clamp recordings; this task measures spike output only. Listed to document a quantitative hook we did not reproduce. |
| Poleg-Polsky 2016 [PolegPolsky2016, Fig 1H, n = 19] | NMDAR multiplicative scaling slope (deg) | **62.5 +/- 14.2** | not measured | — | Multiplicativity test (additive baseline = 45 deg). Subthreshold only; not extracted in this task. |
| Poleg-Polsky 2016 [PolegPolsky2016, main.hoc stim() proc, PD setting] | Inhibitory gabaMOD scalar (PD) | **0.33** | **0.33** | +0.00 | Exact match to the paper's native protocol driver (sourced from the ModelDB 189347 `main.hoc`). |
| Poleg-Polsky 2016 [PolegPolsky2016, main.hoc stim() proc, ND setting] | Inhibitory gabaMOD scalar (ND) | **0.99** | **0.99** | +0.00 | Exact match to the paper's native protocol driver. |
| Prior task t0008 rotation-proxy port [t0008, results_summary.md] | DSI | **0.316** | **0.7838** | +0.468 | Rotation-proxy port held `gabaMOD` fixed and rotated BIP synapse coordinates. gabaMOD-swap port is 2.48x higher — reproducing the literature envelope on the DSI axis. |
| Prior task t0008 rotation-proxy port [t0008, results_summary.md] | Peak firing rate (Hz) | **18.1** | **14.85** | -3.25 | Both ports under-fire relative to envelope. gabaMOD-swap is slightly lower because PD-only firing (no rotation-based averaging) is compared against the rotation-proxy peak at the single best angle. |

## Methodology Differences

* **Direction-selectivity driver** — `[PolegPolsky2016]` implements DS via a per-condition
  `gabaMOD` parameter swap (`0.33` in PD, `0.99` in ND) inside `main.hoc`'s `stim()` procedure. This
  task uses the *same* driver verbatim (sourced from ModelDB 189347 `main.hoc` via t0008's library
  asset) — this is the protocol fix raised as suggestion **S-0008-02** after t0008 used a
  spatial-rotation proxy.
* **Stimulus structure** — `[PolegPolsky2016]` uses a moving bar in **8 directions at 45 deg
  spacing**; this task runs **no bar rotation**, using only two parameter-swapped conditions (PD and
  ND) to isolate the gabaMOD mechanism. There is therefore no angle axis, which is why `Null (Hz)`,
  `HWHM (deg)`, and trial reliability are marked N/A in the `results_detailed.md` comparison table.
* **Bar speed and stimulus window** — identical to the t0008 baseline: `tstop = 1000 ms`,
  `dt = 0.1 ms`, matching `main.hoc` verbatim.
* **Synaptic architecture** — identical to the paper: **177 AMPA + 177 NMDA + 177 GABA_A**
  synapses on ON dendrites, passive dendrites, Jahr-Stevens NMDAR Mg2+ block (all read from the
  unchanged HOC/MOD files sourced via the t0008 library asset).
* **Trial count** — `[PolegPolsky2016]` uses n = **25 / 21 / 34** cells as biological replicates;
  this task uses **20 seeded trials per condition** as computational replicates. Not directly
  comparable at the cell level but exceeds the 10-trial floor implied by the DSGC modelling
  literature.
* **Output metric reporting** — paper reports DSI as **median+/-quartile boxplots** across cells.
  This task reports DSI as the aggregate `(mean_PD - mean_ND) / (mean_PD + mean_ND)` ratio over 20
  trials per condition — the same formula the t0012 scorer's `compute_dsi()` evaluates internally.
* **Subthreshold traces not extracted** — the paper's n = 19 patch-clamp validation targets (PSP
  amplitudes, slope-angle multiplicativity) require whole-cell voltage traces; this task records
  only somatic threshold-crossings for spike counting.

## Analysis

**The native protocol recovers DSI within 0.02 of the paper's headline figure-median value.** DSI
**0.7838** sits inside the **[0.70, 0.85]** envelope and only **-0.0162** below the ~**0.80**
qualitative median that `[PolegPolsky2016]` reports via box-and-whisker plots in Figures
1G/4F/5G/6G/8E. The 40-trial sweep confirms this is not a marginal pass: PD mean 14.85 Hz vs ND mean
1.80 Hz yields an ~8x firing-rate ratio with per-condition CVs of 10.7% (PD) and 57% (ND, on a
small-integer spike count). The direction-selective *contrast* the paper reports is reproduced
faithfully under the paper's native driver.

**The peak-rate gap is real and now unambiguously localised.** PD peak of **14.85 Hz** falls **25.15
Hz below** the **40 Hz** envelope floor. Because the `gabaMOD` swap is the paper's exact native
protocol, this shortfall cannot be attributed to a protocol mismatch in the way t0008's
rotation-proxy DSI gap could. The depression is intrinsic to the port — most likely in excitation
gain (BIP synapse count, `excMOD` scalar, stimulus strength) — and is independent of whether
direction selectivity is induced by rotation or by gabaMOD swap. The gap is recorded as a genuine
experimental finding consistent with Risk-3 in the plan.

**What the comparison does NOT tell us.** `[PolegPolsky2016]` does not report a numeric peak firing
rate in text or figures (see `research_papers.md` Gaps section in t0008), so the "fails the
envelope" verdict is relative to the project envelope **[40, 80] Hz** drawn from broader DSGC
literature, not to a paper-verbatim number. A direct peak-rate reproduction of this paper is
therefore not possible from the published material alone — only envelope-compliance checks are.

### Prior Task Comparison

The plan explicitly cites t0008's rotation-proxy numbers
(`tasks/t0008_port_modeldb_189347/results/results_summary.md`) as the baseline to contrast with, so
a head-to-head comparison is mandatory per spec phase 19.

| Metric | Rotation proxy (t0008) | gabaMOD swap (t0020) | Delta | Envelope | Verdict |
| --- | --- | --- | --- | --- | --- |
| DSI | 0.316 | **0.7838** | **+0.468** (2.48x) | [0.70, 0.85] | t0020 inside envelope; t0008 below floor |
| Peak (Hz) | 18.1 | 14.85 | -3.25 | [40, 80] | Both below floor; gabaMOD-swap slightly lower |
| Null (Hz) | 9.4 | 1.80 | -7.60 | < 10 | Both pass ceiling; gabaMOD-swap much lower (ND firing is strongly suppressed by gabaMOD = 0.99) |
| HWHM (deg) | 82.81 | N/A | — | 60-90 | Two-point protocol has no angle axis |
| Reliability | 0.991 | N/A | — | > 0.9 | Two-point protocol has no per-angle trial variance |

**The DSI gap between the two ports refutes the interpretation that t0008's low DSI was caused by
port fidelity issues** (HOC sourcing, mechanism density, parameter mismatch). Every element of the
cell — HOC skeleton, MOD files, `apply_params`, synapse placement — is shared between the two
ports; only the driver changes. The fact that DSI jumps from 0.316 to 0.7838 when only the driver is
swapped confirms the hypothesis recorded in suggestion **S-0008-02**: t0008's DSI shortfall was a
protocol mismatch, not a port bug.

**The peak-rate deltas also narrow the search.** Both ports produce PD firing rates in the
14.85-18.1 Hz band (t0020 sits 3.25 Hz *below* t0008; t0008 aggregates over 12 angles whereas t0020
uses only the PD condition). Because the driver changed but the firing rate did not meaningfully
shift, the depressed peak is localised to the *excitation* side of the port — the same conclusion
reached in the `results_detailed.md` analysis. Any follow-up should target BIP synapse count,
`excMOD`, or stimulus strength rather than anything on the inhibition side.

## Limitations

* **No single published numeric DSI or peak firing rate for `[PolegPolsky2016]` control**. Every DSI
  reference in the paper is a median+/-quartile boxplot; no numeric peak firing rate is reported in
  text or figures. The comparison therefore uses figure-median readings (~**0.80** for DSI) and
  project-envelope bounds (**[40, 80] Hz** for peak) rather than paper-verbatim numbers.
* **Two-point protocol has no angle axis**. HWHM, null rate per angle, and per-angle trial
  reliability are not measurable under this protocol and are marked N/A in the prior-task comparison
  table. The t0008 rotation-proxy port remains the correct tool for tuning-curve fitting.
* **Subthreshold validation targets not extracted**. `[PolegPolsky2016, Fig 1D-H]` provides concrete
  numeric subthreshold targets (PD NMDAR PSP component **5.8 +/- 3.1 mV**, ND **3.3 +/- 2.8 mV**,
  slope **62.5 +/- 14.2 deg**) that this task does not reproduce — it records only somatic spike
  counts. A subthreshold validation sweep is a natural follow-up.
* **Single `gabaMOD` pair**. The sweep uses only the canonical **0.33 / 0.99** scalar pair from
  `main.hoc`. Sensitivity over intermediate `gabaMOD` values (e.g. 0.5, 0.7) is explicitly out of
  scope and proposed as a follow-up suggestion.
* **Mechanism-context comparisons are not attempted**. Sibling DSGC models with different
  architectures (Schachter 2010, Hanson 2019, Jain 2020, Oesch 2005) would require porting their
  weight sets and would not constitute like-for-like comparisons on the `[PolegPolsky2016]`
  baseline. Their relevance to future work is documented in t0008's `compare_literature.md`, not
  repeated here.
* **Trial-level noise controlled only by RNG seed**. Per-trial stochasticity depends on the NEURON
  RNG and may drift between NEURON/numpy/OS versions even with identical seeds; the comparison is
  stable at the aggregate (DSI, mean PD/ND) level but individual trial firing rates may not
  reproduce bit-exactly across environments.
