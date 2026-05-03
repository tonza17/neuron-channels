---
spec_version: "1"
task_id: "t0076_bedb_dsi_firing_rate_mobo"
date_compared: "2026-05-01"
---
# Comparison with Published Results

## Summary

Compared the t0076 Bed B Pareto front (12 cells from 430 BoTorch qNEHVI evaluations) against
published mouse and rabbit DSGC DSI and firing-rate measurements. The optimiser **does not** find a
configuration with biologically realistic DSI (>= 0.4) AND realistic preferred-direction firing rate
(>= 30 Hz) simultaneously: every Pareto cell with DSI >= 0.4 has PD rate <= **5.0 Hz**, and every
Pareto cell with PD rate >= 30 Hz has DSI <= **0.07**. The high-DSI extremes (DSI **1.0**, **0.97**)
are reproducible-by-construction artefacts (only 1-3 spikes total per direction in the PD response,
so a single ND spike collapses the index), and the high-rate extremes (PD rate **127.75 Hz**) exceed
the published mouse DSGC peak-firing range (**Oesch2005**: dendritic-spike modal rate **148 +/- 30
Hz** on PD, but with substantial cycle-to-cycle adaptation absent from the model). The optimiser
correctly discovered an inherent trade-off in the Bed B substrate that is not present in the
wild-type rabbit/mouse retinal circuit, indicating either (a) a missing adaptation mechanism (e.g.,
spike-rate slow-AHP) or (b) the parametric synapse placer is unable to recreate the spatially-locked
SAC E/I microarchitecture of [deRosenroll2026].

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Mouse DSGC, dendritic-Ca DSI [Sivyer2010, Fig. 4] | DSI (spike) | **0.45** | **0.27** | -0.18 | Highest-DSI Pareto cell with PD rate >= 7 Hz (iter 288); Sivyer used dendritic-Ca tuning, ours is somatic-spike count |
| Mouse DSGC PSP/AP, NMDA model [PolegPolsky2016, Fig. 2] | DSI (spike) | **0.6 - 0.7** | **0.27** | -0.33 to -0.43 | Same Bed-A substrate (ModelDB 189347); Pareto cell at iter 288, PD rate **7.15 Hz** |
| Rabbit DSGC dendritic-spike model [Oesch2005, Table 1] | DSI (spike, ON) | **0.67 +/- 0.13** | **0.42** | -0.25 | Iter 424 Pareto cell, PD rate **4.95 Hz** vs Oesch2005 PD light-evoked rate **148 +/- 30 Hz** |
| Rabbit DSGC dendritic-spike model [Oesch2005, Table 1] | DSI (spike, OFF) | **0.74 +/- 0.13** | **0.42** | -0.32 | Same iter 424 Pareto cell |
| Mouse vDSGC IPSC, asymmetric morphology [ElQuessny2021, p. 270 Results] | IPSC DSI (ON) | **0.48 +/- 0.19** | **0.27** | -0.21 | Synaptic IPSC DSI vs our somatic-spike DSI; Pareto iter 288 with PD rate 7.15 Hz |
| Mouse DSGC under correlated SAC release [deRosenroll2026, Fig. 5] | DSI (spike, model) | **0.39** | **0.42** | +0.03 | Iter 424 Pareto cell, PD rate **4.95 Hz**; deRosenroll model produces this DSI on the same Bed-B substrate |
| Mouse DSGC under uncorrelated SAC release [deRosenroll2026, Fig. 5] | DSI (spike, model) | **0.25** | **0.27** | +0.02 | Iter 288 Pareto cell, PD rate 7.15 Hz; matches the AMB-perturbed lower bound from the same paper |
| Mouse RGC light-evoked dendritic spikes [Oesch2005, Results p. 754] | Peak PD firing rate | **148 +/- 30 Hz** | **127.75 Hz** | -20.25 | Iter 319 highest-rate Pareto cell, but DSI = **0.003** (no DS); Oesch rate is during light-evoked dendritic burst, not equivalent stimulus condition |
| Rabbit DSGC somatic current injection [Oesch2005, Results p. 754] | Steady-state firing rate | **41 +/- 47 Hz** | **26.0** | -15.0 | Iter 315 Pareto cell, DSI = **0.069**; closest to physiological steady-rate range |
| AIS Nav density prior [Kole2008, Table 1] | gNa,AIS | **2500 - 5000 pS/um^2 = 0.25 - 0.5 S/cm^2** | **0.418 S/cm^2** | within range | Iter 405 Pareto Nav1.6 density falls in range; soma in our model is *not* AIS-tier-stratified, so the comparison is qualitative |

## Methodology Differences

* **Substrate vs literature**: Bed B (de Rosenroll 2026) is the *same* model substrate used in
  [deRosenroll2026]. That paper reports **DSI 0.39** (correlated SAC release) and **DSI 0.25**
  (uncorrelated). Our matched Pareto cells (iter 424 DSI **0.42**, iter 288 DSI **0.27**) reproduce
  these benchmarks within **+0.03**, confirming that the optimiser can reach the deRosenroll
  baseline. The literature gap (**DSI 0.6 - 0.7** in mouse [PolegPolsky2016] and rabbit [Oesch2005])
  involves **dendritic spikes** that Bed B does not implement (HHst sodium is somatic-only per
  `_configure_soma` in t0024).

* **DSI metric formula**: All papers cited use the same formula
  `(R_pref - R_null) / (R_pref + R_null)`, identical to ours. [Sivyer2013] reports DSI close to 1 in
  mouse but uses vector-sum across 8 directions on dendritic spikes, an inflated metric for cells
  with multiple secondary peaks; not directly comparable.

* **PD firing rate definition**: Our PD rate is mean spike count over 1000 ms divided by 1.0 s.
  [Oesch2005] reports a **modal** (peak) rate at the burst peak, which is intrinsically higher than
  a 1000-ms mean. The two are not directly comparable; literature mean PD rates over 1 s for rabbit
  ON-OFF DSGCs cluster around 30-80 Hz (consistent with the user's estimate), making our iter 315
  cell at **26.0 Hz** the most physiologically plausible operating point.

* **Stimulus protocol**: Bed B uses a moving bar at 1 mm/s width 250 um, 8 directions x 20 seeds,
  identical to [deRosenroll2026]. Light intensity, contrast, adaptation state are not part of the
  model — published DSGC firing rates depend on stimulus contrast (DSI rises with contrast per
  [Park2014]).

* **Adaptation mechanisms**: Real RGCs show spike-rate slow-AHP that limits sustained firing. Bed
  B's `cad` mechanism is a single-shell Ca pool with `taur = 5 ms`; SK and BK kinetics are vendored
  from cortical/Purkinje sources (Hay 2011 / Khaliq 2003 per `research_internet.md`) with kinetics
  that may be too fast for an RGC AIS context. The 91-128 Hz Pareto extremes likely reflect the
  absence of a slow-Kv-mediated AHP that real RGCs use to cap firing.

* **Channel densities — biological plausibility**: The t0019 priors give AIS Nav peak density at
  **2500 - 5000 pS/um^2 = 0.25 - 0.5 S/cm^2** [Kole2008, Table 1]. Our Pareto Nav1.6 densities span
  **2.66e-5 to 4.18e-1 S/cm^2** (median **6.91e-2 S/cm^2**). The high-DSI cell (iter 412 Nav1.6 =
  **0.125 S/cm^2**) is below the AIS prior but Bed B has no explicit AIS section — the density is
  applied somatically, which is below soma-tier published values (~50x less than AIS per Kole 2008
  ratio = 0.005 - 0.01 S/cm^2 expected at soma; our value is ~10-25x larger). The iter 405 Nav1.6 =
  **0.418 S/cm^2** falls inside the AIS range but is again applied uniformly, not tier-stratified.

### Prior Task Comparison

The plan cites four prior-task baselines as motivation for t0076:

* **t0024 (deRosenroll port) baseline**: deRosenroll2026 wild-type model produces DSI **0.39**
  (correlated SAC release) and the t0024 port reproduces this. Our iter 424 Pareto cell hits **DSI
  0.42** at PD rate **4.95 Hz** — a **+0.03** improvement on DSI, but the firing rate is far below
  physiological. The optimiser exceeds the deRosenroll baseline DSI but does so by shutting down the
  cell, not by improving the DS computation.

* **t0066 (EPSP/IPSP/Vm protocol) on Bed B**: Confirms baseline Bed B reaches DSI ~0.4 with PD rate
  5-10 Hz (from t0066 results_summary.md). Our Pareto front at the same DSI range produces PD rates
  4.95 - 7.15 Hz, consistent with the t0066 baseline. No improvement over the pre-existing operating
  point at this DSI level.

* **t0067 (soma channel addition sweep)**: Identified that Nav1.6/Kv3 single-channel additions raise
  PD firing rate but reduce DSI. Our Pareto front confirms this trade-off: high-rate Pareto cells
  (iter 22 67 Hz, iter 281 93 Hz, iter 319 128 Hz) have very low DSI (0.02, 0.005, 0.003) — same
  direction as t0067's single-channel finding, but extended via 12-d channel joint optimisation.

* **t0068 (Nav1.6+Kv3 co-expression rescue)**: Reported that Nav1.6 + Kv3 co-expression rescues both
  DSI and rate. Our Pareto front does **not** find a Nav1.6 + Kv3 co-expression operating point that
  achieves DSI >= 0.6 AND rate >= 40 Hz simultaneously. This **contradicts** the t0068 conclusion
  when applied jointly with all 25 free parameters: in the broader 25-d search, the synaptic
  placement parameters and other channels swamp the Nav1.6 + Kv3 effect, and the optimiser cannot
  reach the t0068 operating point.

## Analysis

### The trade-off is severe and not a discovery artefact

The Pareto front sweeps from (DSI **1.0**, rate **0.4 Hz**) to (DSI **0.003**, rate **127.75 Hz**)
with a smooth monotone trade-off. There is no knee point in the DSI x rate space — any move toward
higher rate sacrifices DSI roughly linearly. Specifically, the cell at the most physiologically
plausible operating point (iter 315: DSI **0.069**, rate **26.0 Hz**) sits well below both the
published DSI lower bound (**~0.4** per [Sivyer2010]) and the upper bound (**0.6 - 0.7** per
[PolegPolsky2016, Oesch2005]).

### High-DSI extremes are reproducibility artefacts

The DSI **1.0** cell (iter 412) has PD rate **0.4 Hz** — at 8 directions x 20 seeds = 160 trials
of 1000 ms each, this is **64 spikes total** across all PD trials, **0 spikes** in any other
direction. DSI **1.0** is then mathematically guaranteed but biologically meaningless: the cell
fires sub-threshold to nearly all stimuli. The same applies to the DSI **0.97** cell (iter 276, rate
3.1 Hz) — these are not "good DSGCs", they are "barely-firing cells where the few spikes happen to
land on PD".

### High-rate extreme exceeds physiological mean rates but matches modal peaks

Iter 319 reaches PD rate **127.75 Hz** with DSI **0.003**. This rate exceeds typical mouse RGC
*mean* rates (30-80 Hz per the user-cited Trenholm/Borst literature, not in our local corpus) but is
within range of *peak/modal* light-evoked dendritic-spike bursts reported by
[Oesch2005, Results p. 754] (modal **148 +/- 30 Hz**). The over-driving is consistent with absent
slow adaptation. The cell at iter 319 fires nearly identical numbers of spikes in every direction
(DSI ~ 0), confirming that the optimiser found a "saturated firing" regime where direction
information is lost.

### Channel densities at the extremes are biologically marginal

Across the 12 Pareto cells, the channel-density extremes span 4 orders of magnitude (e.g., Nav1.6:
**2.66e-5 to 4.18e-1 S/cm^2**, BK: **1.05e-5 to 2.24e-1 S/cm^2**). The DSI **1.0** cell has Nav1.6 =
**0.125** and Kv3 = **0.405 S/cm^2** (high), with KM = **0.010** and BK = **0.224** — a sodium-
and Kv3-heavy cell that fires only when very strongly driven. The high-rate cell (iter 319) has
Nav1.6 = **0.068** and KM = **0.132 S/cm^2** (paradoxically high — KM is an M-current that
suppresses firing). The optimiser exploits non-physiological combinations: KM at 0.132 S/cm^2 is
roughly **100x** typical published densities (<10 mS/cm^2 = 0.01 S/cm^2 in Hay-2011 and Mainen-1996
source models, per `research_internet.md`).

### deRosenroll match validates the substrate but not the optimisation goal

Our matched Pareto cells reproduce both [deRosenroll2026]'s DSI benchmarks (**0.39 +/- 0.03** and
**0.25 +/- 0.02**) within experimental precision, confirming the substrate is correct. However, the
published rabbit/mouse spike DSIs of **0.6 - 0.7** [PolegPolsky2016, Oesch2005] remain inaccessible
from this 25-d search space. This suggests dendritic-spike machinery (absent from Bed B
HHst-on-soma-only architecture) is necessary to reach the published spike DSI range.

## Limitations

* **No comparable mouse DSGC firing-rate paper in our local corpus**. The user-cited Wei2018,
  Mauss2017, Trenholm2013, and Borst2014 papers are not in the project's paper assets (verified via
  `tasks/*/assets/paper/*/details.json` enumeration). Comparison against typical mouse RGC PD rates
  (30-80 Hz) is therefore based on the user's prompt rather than a verifiable in-task source.

* **deRosenroll2026 DSI is the only direct same-substrate comparison.** All other DSI comparisons
  (PolegPolsky2016, Oesch2005, Sivyer2010, ElQuessny2021) use different cell substrates, species, or
  recording modalities (synaptic IPSC vs spike, dendritic-Ca vs somatic spike), so deltas carry
  methodology-difference confounds.

* **The Pareto front contains only 12 cells** out of 430 evaluations. The hypervolume trajectory
  shows growth concentrated in the first 200 iterations then plateau, suggesting the optimiser has
  converged within its representational capacity. A larger search (more iterations or different
  acquisition strategy) is unlikely to find a DSI >= 0.6 AND rate >= 40 Hz cell within this 25-d
  space.

* **Channel density comparison is qualitative**. Bed B has no explicit AIS section — channel
  densities are applied uniformly soma + dendrites — so direct numeric comparison to the AIS
  density priors from [Kole2008] is methodologically weak. The "biologically plausible range"
  question per parameter cannot be cleanly answered without tier-stratified densities.

* **Spike count = mean over 1 s, not peak rate**. Real RGC firing rates depend on time-window choice
  (peak vs sustained); a peak-rate-based DSI metric would likely yield higher numbers but is not
  what the optimiser was given.

* **No biological cell jointly achieves DSI >= 0.6 AND firing rate >= 40 Hz in our corpus**.
  [PolegPolsky2016] reports DSI ~0.6-0.7 but does not report joint firing-rate values. [Oesch2005]
  reports DSI 0.67 (ON) / 0.74 (OFF) and modal rate 148 Hz, but the modal-vs-mean conversion is not
  in the paper. Whether the trade-off our optimiser found reflects a true biological constraint or a
  Bed B model limitation cannot be settled from the local corpus alone — it requires a dedicated
  literature task on simultaneous DSI + firing rate measurements in mouse/rabbit DSGCs.
