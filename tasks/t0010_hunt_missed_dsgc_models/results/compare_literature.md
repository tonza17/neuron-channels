---
spec_version: "1"
task_id: "t0010_hunt_missed_dsgc_models"
date_compared: "2026-04-20"
---
# Comparison with Published Results

## Summary

This task attempted to port three HIGH-priority DSGC compartmental models (Hanson2019,
deRosenroll2026, PolegPolsky2026) missed by the t0002 and t0008 surveys. **All three attempts exited
at P2** (upstream-demo gate) within the per-candidate 90-minute wall-clock cap due to structural
driver incompatibility with the canonical 12-angle x 20-trial sweep — not biophysics bugs. As a
result, **no new quantitative tuning-curve data was produced**, and the only reproduction reference
this project has for DSGC direction selectivity remains t0008's port of ModelDB 189347
(PolegPolsky2017), which measured **DSI = 0.52** against that paper's published value of **DSI ≈
0.50**. The table below records the published DSI values the three attempted models would have been
compared against, with `—` in "Our Value" to mark ports that never reached P3.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| PolegPolsky2017 (ModelDB 189347) | DSI | 0.50 | 0.52 | +0.02 | Reference reproduction; measured in t0008 (canonical DSGC baseline) |
| Hanson2019 (Spatial-Offset-DSGC) | DSI | 0.45 | — | — | Port exited at P2: headful GUI driver + hardcoded Windows output path |
| deRosenroll2026 (ds-circuit-ei) | DSI | 0.48 | — | — | Port exited at P2: 8-direction hardcoded grid + 4 missing deps |
| PolegPolsky2026 (DS-mechanisms) | DSI | 0.55 | — | — | Port exited at P2: GA-training framework, no forward-only driver |
| PolegPolsky2017 (ModelDB 189347) | HWHM (deg) | 52 | 50 | -2 | Reference reproduction from t0008 |

## Methodology Differences

* **Canonical sweep**: This project's target harness runs a 12-angle x 20-trial full-contrast sweep
  and scores DSI + tuning-curve HWHM against the per-angle envelope. None of the three new
  candidates ship a driver matching this protocol out of the box.
* **Hanson2019**: upstream driver imports `neuron.gui` and writes to a hardcoded
  `C:\Users\geoff\NEURONoutput\` path. Running headlessly requires a non-trivial driver rewrite
  (estimated >90 min).
* **deRosenroll2026**: upstream driver hardcodes an 8-direction stimulus grid and depends on four
  packages (`statsmodels`, `h5py`, `fastparquet`, `oiffile`) not in this project's environment.
  Adapting to 12 angles requires edits in both the stimulus generator and the scoring glue.
* **PolegPolsky2026**: the only available driver is a genetic-algorithm training loop (`numGen=300`,
  `popSize=50`) that fits free parameters against a reference curve; no single-parameter-set
  forward-simulation entry point exists. The repo also has no LICENSE, which blocks library-asset
  registration even if a driver were written.
* **Reference t0008 reproduction**: the only model successfully reproduced in this project to date
  remains ModelDB 189347 (PolegPolsky2017), which was ported as a library asset in t0008 and
  measured **DSI = 0.52** (vs. **0.50** published).

## Analysis

The uniform P2 exit across three structurally different candidates (a two-compartment SAC+DSGC
model, an E/I-microarchitecture DSGC cohort, and a GA-trained mechanism-exploration framework) is
itself a useful finding: publicly released DSGC code is typically released in the shape the authors
used for their specific figure production, not as a drop-in simulation library. None of the three
upstream drivers even *attempt* to expose a forward-only "simulate at angle θ" entry point. This
matches the broader pattern that t0008's ModelDB 189347 port required a full driver rewrite against
the ModelDB release as well — the canonical 12-angle sweep in this project has so far always been
bolted on downstream of the author-released code, never adopted upstream.

Because **Our Value = —** for all three new candidates, there is no headline gap to interpret. The
t0008 reference row (**DSI 0.52** vs. **0.50** published, **HWHM 50 deg** vs. **52 deg**) continues
to be the sole concrete reproduction against which future ports will be measured.

## Limitations

* **No new numeric comparisons**: only the t0008 reference row has an Our Value; the three attempted
  candidates contribute published targets only.
* **Published DSI values are approximate**: the three candidate papers do not all report DSI in the
  canonical Raganato-style fixed-protocol form; the values in the table are the closest
  DSI-equivalent numbers extractable from each paper's figures and are therefore order-of-magnitude
  comparisons.
* **Elsevier PDF gap**: the deRosenroll2026 paper PDF could not be downloaded (HTTP 403), so the
  published DSI for that row is drawn from the paper's abstract and preprint figure captions, not
  the final text.
* **Tuning-curve HWHM is only available for t0008**: the three upstream papers do not report HWHM in
  directly comparable form.
* **No statistical comparison**: with only one reproduced model (t0008) and three `p2_failed` ports,
  there is no basis for a statistical test of agreement.

## References

* **PolegPolsky2017** — ModelDB 189347, ported in t0008 as the canonical DSGC reproduction baseline
  for this project.
* **Hanson2019** — `10.1038/s41467-019-09147-4`; upstream repo
  `geoffder/Spatial-Offset-DSGC-NEURON-Model`.
* **deRosenroll2026** — `10.1016/j.celrep.2025.116833`; upstream repo
  `geoffder/ds-circuit-ei-microarchitecture` (Zenodo `10.5281/zenodo.17666157`).
* **PolegPolsky2026** — `10.1038/s41467-026-70288-4`; upstream repo `PolegPolskyLab/DS-mechanisms`.
