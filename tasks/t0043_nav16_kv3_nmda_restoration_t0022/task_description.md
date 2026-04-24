# Nav1.6 + Kv3 + NMDA Restoration on t0022

## Source Suggestion

S-0019-03 primary (implement Nav1.6 / Nav1.2 / Kv1 / Kv3 channels with AIS-specific densities). This
task covers the Nav1.6 and Kv3 portion of S-0019-03. It also partially covers S-0018-03 (NMDA
restoration) and S-0022-02 (Nav1.6 distal-AIS density).

## Motivation

The cross-task audit in brainstorm session 8 (see
`tasks/t0040_brainstorm_results_8/results/test_vs_literature_table.md`) identifies peak firing rate
as the most universal mismatch: 15 Hz across t0022 baseline and every t0022-based sweep, vs 30–150
Hz in every cited published source (Oesch 2005: 148 Hz; Chen 2009: 166 Hz; Sivyer 2013: 80–150
Hz). The likely causes stack: (a) t0022 uses lumped HHst which lacks Nav1.6 persistent Na current
and Kv3 fast repolarisation, both of which are needed for high-frequency AP firing; (b) the t0022
E-I schedule zeros NMDA at both PD and ND BIPs, removing the expected NMDA-mediated gain boost; (c)
AMPA-only drive caps the effective depolarisation.

The audit also shows that Schachter 2010's predicted active-amplification diameter signature is
absent on every diameter sweep we have run (t0030, t0035, t0039). One candidate explanation is that
without Nav1.6 / Kv3 in the distal dendrite, the regenerative threshold-crossing regime Schachter
2010 relies on cannot be recruited.

This task restores the channel inventory and NMDA drive so the peak-rate mismatch can be attacked,
and so the Schachter re-test in t0044 runs against a model that matches published DSGC channel
priors.

## Objective

Produce a new library asset (tentatively `modeldb_189347_dsgc_t0043` or similar) that is a fork of
the t0022 testbed with three modifications:

1. Nav1.6 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~8 mS/cm^2
   (per t0019's cited DSGC priors). If a Nav1.6 MOD file is not already available, adapt one from
   the t0019 channel corpus.
2. Kv3 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~5 mS/cm^2.
3. NMDA synapse component restored at both PD and ND BIP terminals with conductance matching the
   Poleg-Polsky 2016 parameter backbone (read from t0008's library asset if available, else sourced
   from the Poleg-Polsky 2016 paper).

Hold the t0037 null-GABA sweet spot of 4 nS as the base parameter per t0038's correction. Keep the
12-direction × 10-trial sweep protocol identical to t0022 / t0037 / t0039 so results are directly
comparable.

Pass criterion (both must hold):

* Peak firing rate in [40, 80] Hz at V_rest = -60 mV.
* Primary DSI within +/- 0.1 of the t0037 anchor of 0.429 at the 1.0x baseline diameter.

## Scope

* Local CPU only. No remote compute. ~6 hours wall-clock including MOD recompilation.
* Produce a library asset with the modified model plus a baseline 12-direction x 10-trial sweep at
  V_rest = -60 mV, GABA = 4 nS.
* Write a test harness that can be reused by t0044 for the diameter sweep.

## Out of Scope

* Nav1.2 and Kv1 (part of the fuller S-0019-03 scope, deferred).
* Morphology sweeps (covered by t0044 which uses this task's output as substrate).
* V_rest sweep (covered by t0026 on the prior testbed; a re-run on the new testbed could be a
  follow-up suggestion emitted from this task).

## Deliverables

* `assets/library/modeldb_189347_dsgc_t0043/` — library asset with the modified model, compiled
  MOD files, and baseline sweep driver.
* Baseline 12-direction x 10-trial sweep CSV under `results/`.
* Tuning curve (Cartesian and polar) under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections and an
  explicit Pass/Fail verdict against both criteria above.
* `results/metrics.json` with baseline primary DSI, vector-sum DSI, preferred direction, peak Hz,
  null Hz, and a boolean `peak_rate_pass` and `dsi_preserved_pass`.
* If Pass: the library asset is fit for use as t0044's substrate. If Fail: emit a suggestion for a
  follow-up calibration task (BIP burst rate + AMPA scale; see S-0040-01 or analogous) and stop
  before t0044.

## Anticipated Risks

* Nav1.6 MOD files in the t0019 corpus may not compile under NEURON 8.2.7 without adaptation; budget
  time for MOD debugging.
* Adding Nav1.6 may push the cell into runaway firing if the Kv3 density is too low; tune Kv3 first,
  Nav1.6 second.
* Restoring NMDA may break the t0037 4 nS sweet spot by over-exciting at the null direction; if this
  happens, emit a follow-up suggestion to repeat a GABA sweet-spot search on the new testbed.
