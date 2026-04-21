---
spec_version: "1"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
date_compared: "2026-04-21"
---
# Comparison with Published Results

## Summary

The port of [deRosenroll2026] reproduces high direction selectivity (**DSI 0.8182** correlated,
8-dir) but **does not** reproduce the paper's correlation-drop signature: measured drop is **0.000**
against the published ~**0.36** (correlated **0.39** -> uncorrelated **0.25**), and both conditions
overshoot the paper's DSI envelope. Peak firing rate comes in at **5.15 Hz** versus the paper's
qualitative ~**30-40 Hz** range and the project t0004 envelope of **40-80 Hz** — consistent with
the lineage-wide firing-rate gap already seen in t0008 (**18.1 Hz**), t0020 (**14.85 Hz**), and
t0022 (**~15 Hz**). HWHM at **68.65 deg** sits close to the t0004 target of **68.51 deg**, so the
angular sharpness of tuning is matched but its amplitude and correlation-sensitivity are not.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| deRosenroll2026 (correlated, 8-dir) | DSI | 0.39 | 0.82 | +0.43 | Overshoots paper DSI envelope |
| deRosenroll2026 (uncorrelated, 8-dir) | DSI | 0.25 | 0.84 | +0.59 | Overshoots and inverts drop sign |
| deRosenroll2026 (corr -> uncorr) | DSI drop fraction | 0.36 | 0.00 | -0.36 | Port-fidelity gate REQ-5 miss |
| deRosenroll2026 | Peak firing rate (Hz) | ~30-40 | 5.15 | ~-25 to -35 | Paper range qualitative |
| t0004 target envelope | DSI (12-ang) | 0.8824 | 0.7759 | -0.1065 | Project envelope, correlated |
| t0004 target envelope | HWHM (deg) | 68.51 | 68.65 | +0.14 | Angular sharpness matches |
| t0004 target envelope | Peak firing rate (Hz) | 40-80 | 5.15 | -34.85 (to lower bound) | Lineage-wide gap |
| t0008 rotation proxy (PolegPolsky2016 geom) | DSI (12-ang) | 0.316 | 0.7759 | +0.4599 | Newer geometry + AR(2) noise |
| t0020 gabaMOD swap (PolegPolsky2016 geom) | DSI (12-ang) | 0.784 | 0.7759 | -0.0081 | Near-match on DS magnitude |
| t0022 dendritic E-I scheduling | DSI (12-ang) | 1.000 | 0.7759 | -0.2241 | Different protocol / geometry |

## Methodology Differences

* **Driver architecture**: The port implements per-terminal Exp2Syn excitation and inhibition
  parameterised directly from [dsMicro-GH] `ei_balance.py`. The upstream code also distributes the
  release drive through a spatially-structured `SacNetwork` with `bp_locs`, `probs`, and `deltas`
  that encode per-varicosity release probabilities and temporal offsets. The port keeps the
  per-terminal kinetics and noise but does not instantiate the spatial release network — the AR(2)
  drive is applied at the terminals directly rather than through the upstream SAC connectome.
* **Noise process**: AR(2) release-rate noise with `phi = [0.9, -0.1]` and cross-channel `rho` swept
  between **0.6** (correlated) and **0.0** (uncorrelated) is implemented faithfully per
  [dsMicro-GH]. The same seed policy (per-trial integer seed) is used.
* **Temperature / integration**: `celsius = 36.9 C`, `dt = 0.1 ms`, Ca2+ decay `tau = 10 ms`,
  matching the repository code exactly.
* **Biophysics**: Ra 100 Ohm*cm, cm 1 uF/cm^2, gleak 5e-5 S/cm^2, eleak -60 mV, Na (soma / primary
  dendrite / distal) 150 / 200 / 30 mS/cm^2, K 35 / 40 / 25 mS/cm^2, from repository code — not
  paper-text values (paper reports Ra 200, eleak -65, Na 200 / 70 / 35, K 40 / 12 / 18). The
  repository values were chosen as authoritative, following the upstream `README`.
* **AIS**: No explicit AIS section is modelled, matching [dsMicro-GH] (gap 2 in research-internet).
  No Nav1.6 / Nav1.2 split was added.
* **Protocol coverage**: The paper uses 8 directions; the project standard is 12. Both protocols
  were run. The port-fidelity gate uses the 8-direction protocol to match the paper exactly; the
  t0004 envelope comparison uses the 12-angle protocol to match prior ports.
* **Trial count**: 20 trials per condition per angle (800 trials total across the four condition x
  protocol combinations), matching the per-angle density in [dsMicro-GH] fig-reproduction scripts.

## Analysis

The magnitude-vs-mechanism split in the comparison table is informative. Angular selectivity in the
port is strong and sharp: **DSI 0.78-0.84** across correlated and uncorrelated conditions with HWHM
at the t0004 envelope target. This confirms the static asymmetry in the deRosenroll per-terminal
kinetics — the reversed PD-vs-ND inhibition-to-excitation timing and the 1.8x GABA scaling — is
correctly reproduced by the Exp2Syn drivers. However, the headline finding of the paper is **not**
the absolute DSI value but the **correlation-drop effect**: correlated SAC release at `rho = 0.6`
produces DSI ~**0.39**, and breaking that correlation down to `rho = 0.0` collapses DSI to
~**0.25**, a ~**36%** drop. The port shows essentially zero drop (**0.000** fraction, -0.002
absolute) because the correlation is applied at individual Exp2Syn drivers rather than across the
spatially-distributed SAC release network that the paper shows is the causal substrate of the
effect.

The **peak firing rate shortfall** (**5.15 Hz** vs paper ~**30-40 Hz** and t0004 **40-80 Hz**) is a
lineage-wide signature already present in t0008 (**18.1 Hz**), t0020 (**14.85 Hz**), and t0022
(**~15 Hz**). It is therefore not caused by this port alone, but the port is the first in the
lineage to also be fully biophysical and still hit this low a rate — earlier ports used spatial
rotation, gabaMOD swaps, or hand-scheduled E/I with simpler integration. The most probable cause is
the single-compartment Na/K density regime (150/200/30 mS/cm^2) being below the saturating spike
rate even when integrator delivers peak voltage; a paper-value override sweep (Na 200/70/35, K
40/12/18) is a reasonable follow-up.

The **angular sharpness match** (HWHM **68.65 deg** vs t0004 **68.51 deg**, delta **+0.14**) is a
non-trivial positive finding: despite the firing-rate miss and the correlation-drop miss, the
geometry of the tuning curve is correctly reproduced. This suggests the morphology import
(341-section `RGCmodelGD.hoc`) and the per-terminal inhibitory-excitatory asymmetry capture the
spatial filtering correctly; the missing ingredient is the **temporally-distributed SAC varicosity
drive** that makes the circuit sensitive to release correlation in the first place.

## Limitations

* **The port-fidelity gate is a composite criterion.** REQ-5 requires all three sub-criteria (corr
  DSI band, uncorr DSI band, drop >=20%) to pass. The port misses all three. The gate miss is a
  first-class finding per plan step 13, not a scoring bug.
* **No published numeric HWHM or per-angle tuning profile** was available in the paper text or
  [dsMicro-GH] `README`, so the HWHM comparison is against the project's own t0004 envelope (derived
  from t0022 and independent Hanson / Poleg-Polsky priors) rather than a deRosenroll-derived value.
* **Peak firing rate range (~30-40 Hz) is qualitative**: no explicit paper figure pins the peak rate
  numerically. The comparison table uses the midpoint of the plausible range.
* **The paper's 8-direction protocol cannot be plotted with the t0011 polar/Cartesian plotter**,
  which hardcodes `N_ANGLES = 12`. Figures for the 8-direction conditions are present only as raw
  CSVs, not PNGs.
* **Cross-model row for t0023_port_hanson_2019_dsgc is absent** from the comparison because t0023 is
  `intervention_blocked` pending t0022. REQ-6 cross-comparison coverage is partial (4/5 models).
* **Absolute DSI inflation on uncorrelated trials** (port 0.84 vs paper 0.25) may partly reflect the
  absence of any positive intra-varicosity mechanism that causes uncorrelated release to degrade
  selectivity — the port's uncorrelated drive still preserves the per-terminal PD/ND kinetic
  asymmetry, so DS survives. Fixing this likely requires adding the spatial release network so that
  uncorrelated release creates per-subunit DSI degradation.
* **A Nav1.6 / Nav1.2 AIS overlay was not added**, per research-internet gap 2. Whether this would
  raise peak firing rate into the t0004 envelope is not tested in this task.
