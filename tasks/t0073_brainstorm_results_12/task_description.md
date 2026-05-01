# Brainstorm Session 12: Channel Tuning-Width and Biologically-Realistic AIS Parameter Sweeps on Bed A

Twelfth brainstorming session. Run on 2026-05-01 after t0070 (two-bed writeup), t0071 (typeset PDF +
synaptic-current equations), and t0072 (synaptic conductance/current traces for PD and ND on both
beds) all completed. The session is triggered by two convergent gaps in the t0067 / t0068 / t0069
voltage-gated-channel arc on Bed A (the deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC):

* **Tuning-width gap**: t0067 measured DSI as a point estimate from PD vs ND only. Whether the
  channels {Nav1.6, NaP, NaR, Kv3, Kv4} also reshape the *width* of the angle-to-AP-rate tuning
  curve has not been measured. The biologically more interesting question is whether channels
  broaden or sharpen tuning, not just whether they raise or lower DSI at the two cardinal angles.

* **Biologically-realistic AIS gap**: t0069 falsified the AIS-channel-relocation hypothesis on the 4
  0 0 mS/cm² somatic Na background, but did so by collapsing the cell into a regime where ND firing
  = 0 and DSI = 1 trivially. We therefore have no DSGC + AIS configuration that simultaneously
  contains all the channels biologically present in a vertebrate AIS (HHst basal Na+K, Nav1.6, Kv3,
  Kv7) while keeping DSI in the [0.3, 0.95] band and the peak rate in the [5, 50] Hz band. Finding
  such a configuration via one-axis-at-a-time parameter sweeps (not optimisation) is a prerequisite
  for any future AIS-localised-channel hypothesis test.

## Decisions

* **Create t0074** — `channel_tuning_width_bed_a`. Forks t0067's somatic channel-addition layer on
  Bed A and runs a 12-angle bar-rotation tuning-curve protocol per condition. Channel set is the
  five existing channels {Nav1.6, NaP, NaR, Kv3, Kv4} plus three newly vendored channels {BK, SK,
  Kv7/M-current} at low/medium/high densities. 8 channel types times 3 densities plus 1 baseline =
  25 conditions; 25 times 12 angles times 5 seeds = 1500 FULL trials, plus 25 times 12 angles times
  1 seed times 2 passive modes = 600 EPSP_PASSIVE / IPSP_PASSIVE diagnostic trials; total ~2.2 h
  wall-clock on local CPU under CVODE. Width metrics: HWHM (deg), vector-sum DSI, peak rate at PD,
  RMSE vs the t0004 cosine target. Vendoring overhead (~3-4 h coding) covers BK + SK + Kv7 MOD
  files, a calcium-pool mechanism for BK / SK, and unzeroing CaL / CaT in Bed A's `init_active` with
  a regression gate that reproduces t0067's baseline DSI = 0.797 within 1e-3 before any new channel
  is added.

* **Create t0075** — `bio_realistic_ais_param_sweep`. Forks t0069's AIS attachment code on Bed A.
  AIS channel set: {HHst basal Na+K, Nav1.6, Kv3, Kv7} (NaP, BK, and SK explicitly excluded — NaP
  inverts DSI per t0067 and is controversial in AIS; BK / SK are more soma / dendrite than AIS in
  RGCs). Two-stage design: Stage 1 calibrates a working baseline by running 6 candidate soma-gnabar
  settings at a literature-informed AIS configuration (diameter 0.8 micrometre, length 3 0
  micrometre, axon stub 1 mm) at 12 angles times 1 seed = 72 trials; the candidate that lands inside
  {peak Hz in [5, 50], DSI in [0.3, 0.95]} is selected. Stage 2 runs 8 one-at-a-time axes from that
  baseline (soma `gnabar_HHst`, AIS `gnabar_HHst`, AIS diameter, AIS length, AIS Nav1.6 density, AIS
  Kv3 density, AIS Kv7 density, axon length); 27 conditions times 12 angles times 5 seeds = 1620
  FULL trials, ~100 min wall-clock. Total compute ~2 h. Outputs: per-axis HWHM / DSI / peak Hz
  sensitivity plots and a "biologically-plausible AIS recommendation" table. t0075 depends on t0074
  (Kv7 vendoring lands in t0074); the two are commissioned in this brainstorm but serialised by
  dependency.

## Suggestion Cleanup

* **Reject nine high-priority suggestions** as covered by the new tasks or as duplicates: S-0068-01
  (BK / SK with Nav1.6 — covered by t0074), S-0068-02 (Kv7 with Nav1.6 — covered by t0074),
  S-0068-04 (move Nav1.6 + Kv3 to AIS — covered by t0075), S-0068-05 (Kv3 alone validation —
  superseded by t0074's per-channel tuning-width sweep), S-0069-01 (halve somatic gnabar — covered
  by t0075 axis 1), S-0069-02 (shrink AIS diameter to 0.5 micrometre — covered by t0075 axis 3),
  S-0069-03 (vary axon length to probe sink — covered by t0075 axis 8), S-0069-04 (Nav1.6 + Kv3 on
  AIS at biological densities — covered by t0075 baseline plus axes 5 + 6), S-0065-01 (apply EPSP
  / IPSP / FULL to from-scratch family — duplicate of S-0066-02; the more recent S-0066-02 is
  kept).

* **Reprioritise three high-priority suggestions to medium** where the t0065 / t0066 / t0067
  shunting-inhibition discovery has changed the strategic frame: S-0002-01 (factorial g_Na x g_K
  grid search) and S-0002-04 (factorial morphology sweep) — both pre-shunting-discovery framing,
  the project has moved on; S-0070-02 (unified model-bed-runner library) — pure infrastructure,
  not blocking any current experiment.

## Tasks Cancelled or Updated

None.

## Assets Produced

No assets in this brainstorm task. The two new tasks (t0074 and t0075) will produce one library
asset each (channel-vendoring library plus tuning-width sweep code in t0074; biologically-realistic
AIS variant of Bed A plus per-axis sweep code in t0075) and a results bundle each when executed
downstream.
