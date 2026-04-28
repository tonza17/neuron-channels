# Brainstorm Session 10: Tonic GABA Window Fix on t0053

Tenth brainstorming session. Run on 2026-04-28 after the from-scratch minimal DSGC wave (t0052,
t0053, t0054) completed and t0055 (Mg-block NMDA recovery test) started. The session is triggered by
a researcher observation while reviewing t0053's traces: GABA conductance is only present in a
narrow ~100-200 ms window per trial because each spatial-gating GABA synapse fires exactly once at
the bar-arrival time and the Exp2Syn decay is only `tau2 = 20 ms`. With a 1500 ms trial duration,
this leaves the cell uninhibited for the remaining ~1100 ms — biologically wrong (real SAC→DSGC
IPSCs envelope over 100-300 ms via multiple release events) and a likely contributor to the
amplitude-calibration sensitivity that produced t0053's degenerate flat-zero FULL tuning.

## Decision

* **Create t0057** — `tonic_gaba_sweep_t0053`. Replace t0053's per-event Exp2Syn GABA mechanism
  with a new `gaba_tonic.mod` point process that delivers a sustained conductance over a
  configurable `(t_on, t_off)` window. Default window: `t_on = 100 ms`, `t_off = 1400 ms` (full
  trial minus 100 ms BASE_OFFSET buffer). Preserve t0053's spatial centripetal-gating rule
  (`cos(theta_stim - theta_centrifugal) < 0` selects active synapses); replace amplitude. Sweep
  `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS to locate the operating point that produces a
  non-zero FULL-mode tuning curve. Source suggestion: S-0053-01 (covered).

## Suggestion Cleanup

* **Reject four high-priority suggestions** as covered or superseded by completed work: S-0015-04
  (covered by t0052), S-0016-03 (covered by t0054 + t0055), S-0017-03 (AIS+NMDA done in t0052/t0054
  and voltage-clamp block in t0049), S-0018-03 (AMPA+NMDA+GABA done in t0053+t0054, temporal
  co-tuning piece deferred to a future fresh suggestion).

* **Reprioritise nineteen high-priority suggestions to medium**:

  * t0022 testbed lineage (de-emphasised by brainstorm 9 pivot): S-0022-01, S-0022-02, S-0022-03.
  * t0024 testbed follow-ups: S-0026-02, S-0026-06, S-0034-01, S-0034-02, S-0034-07, S-0035-02,
    S-0039-01.
  * t0033 optimiser prerequisites (deferred until from-scratch substrate is mature): S-0033-02,
    S-0033-03, S-0033-06.
  * Sheffield paywalled-paper retrievals (already bundled into not-started t0031): S-0015-01,
    S-0016-01, S-0017-01, S-0018-01, S-0019-01.
  * Retired deposited-DSGC line: S-0048-01.

## Tasks Cancelled or Updated

None.

## Assets Produced

No assets in this brainstorm task. The new task t0057 will produce a library asset (the new
`gaba_tonic.mod` mechanism wrapped in a Python builder) and an experiment-results bundle when
executed.
