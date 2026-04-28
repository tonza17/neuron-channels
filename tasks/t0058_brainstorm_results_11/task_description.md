# Brainstorm Session 11: Bar-Arrival-Locked GABA + AMPA Escape on t0057 Substrate

Eleventh brainstorming session. Run on 2026-04-29 after t0055 (Mg-block NMDA recovery test) and
t0057 (tonic-GABA amplitude sweep on t0053 spatial substrate) both completed. The session is
triggered by the convergent finding across the from-scratch minimal DSGC family (t0052, t0053,
t0054, t0055, t0057) that every variant is locked in a binary regime — either
single-spike-per-trial (DSI = 1.0 trivially, peak Hz = 0.667) or full inhibitory suppression (DSI =
0). The cell needs to escape this binary regime into the 5-50 Hz multi-spike band before DSI metrics
are biologically informative.

## Decision

* **Create t0059** — `bar_locked_gaba_ampa_sweep_t0057`. Forks t0057's
  `minimal_dsgc_tonic_gaba_sweep` library and (a) replaces the global `(t_on, t_off) = (100, 1400)`
  ms tonic GABA window with a per-synapse bar-arrival-locked window
  (`t_on_i = (x_i cos(theta) + y_i sin(theta)) / v + 100 ms`, `t_off_i = t_on_i + 200 ms`), (b)
  bundles the project-wide measurement-protocol fix (drop `E_ONLY` / `GABA_ONLY` legacy modes, add
  `EPSP_PASSIVE` / `IPSP_PASSIVE` modes that save-and-zero `gnabar_hh` / `gkbar_hh` on soma + AIS so
  synaptic envelopes are spike-free; drop the per-synapse activation histogram; fix trial length at
  1400 ms), and (c) sweeps a 5x5 (gAMPA, GABA_BASE_NS) grid covering both the sub-veto and
  multi-spike regimes. Source suggestions: S-0057-01, S-0057-02, S-0057-04, S-0055-01 (all four
  covered).

## Suggestion Cleanup

* **Reject seven high-priority suggestions** as covered or superseded by completed work: S-0011-01
  (deposited-DSGC line retired; plot_angle_raster_psth exercised on from-scratch wave), S-0012-01
  (verify_library_asset.py exists and is in active use across t0052/t0053/t0054/t0057), S-0012-03
  (deposited-DSGC line retired; tuning_curve_loss already integrated via metrics.json RMSE on the
  from-scratch lineage), S-0055-01 (covered by t0059's bundled protocol fix), S-0057-01 (covered by
  t0059's GABA grid including 0.1 / 0.2 nS), S-0057-02 (covered by t0059's AMPA grid axis),
  S-0057-04 (covered by t0059's bar-arrival-locked window mechanism).

* **Reprioritise eighteen high-priority suggestions to medium** where the brainstorm-9 from-scratch
  pivot or recent results have de-urgented them:

  * Deposited-DSGC and deRosenroll port lineage (retired): S-0003-02, S-0008-01, S-0010-02,
    S-0010-05, S-0024-01, S-0027-02, S-0046-02, S-0020-01, S-0020-02.
  * Morphology and active-channel calibration (deferred to RQ2 / RQ4 follow-ups once a working
    multi-spike substrate exists): S-0009-01, S-0009-02, S-0009-03.
  * Channel/tooling infrastructure (no longer top-of-queue): S-0007-01, S-0013-01, S-0013-02.
  * From-scratch comparisons (defer until working spatial operating point exists): S-0052-04,
    S-0053-02, S-0053-03.

## Tasks Cancelled or Updated

None.

## Assets Produced

No assets in this brainstorm task. The new task t0059 will produce one library asset
(`minimal_dsgc_bar_locked_gaba_ampa_sweep` or similar slug) and an experiment-results bundle when
executed downstream.
