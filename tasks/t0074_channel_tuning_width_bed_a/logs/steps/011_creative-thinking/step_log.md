---
spec_version: "3"
task_id: "t0074_channel_tuning_width_bed_a"
step_number: 11
step_name: "creative-thinking"
status: "completed"
started_at: "2026-05-02T03:38:27Z"
completed_at: "2026-05-02T03:55:00Z"
---
# creative-thinking

## Summary

Reviewed the 25-condition width-metrics table and identified five non-obvious findings worth deeper
analysis: (1) NaR_med / NaR_high broaden HWHM by +34 to +36 deg without changing peak rate or
vector-sum DSI — a surprising "selectivity-loss without rate-gain" effect; (2) SK_high sharpens
HWHM by 42 deg simultaneously with suppressing peak rate, the only channel in the sweep that
achieves both; (3) NaP_high collapses vector-sum DSI to 0.05 (legacy DSI to 0.008) while peak-rate
is the highest in the sweep (74 Hz) — depolarisation block at PD plus rescue at ND; (4) Kv3, Kv4,
Kv7 are inert at all densities, but for three distinct biophysical reasons that should be tested
separately rather than dismissed together; (5) BK and SK produce nearly identical narrowing patterns
(-6 to -9 deg HWHM, vector-sum DSI -0.04 to -0.07) at low / med / high densities, suggesting a
shared Ca-driven mechanism rather than two distinct channels.

## Actions Taken

1. Loaded `results/metrics_summary.csv` (25 rows) and ranked conditions by `delta_hwhm_deg` and
   `delta_vector_sum_dsi`.
2. Identified outlier channels and densities and developed alternative biophysical hypotheses for
   each.
3. Captured ideas worth following up in the suggestions step (step 14).

## Outputs

* This step log; no separate file. The analyses below feed the suggestions step.

## Issues

No issues encountered.

## Out-of-the-Box Analyses

### NaR-induced broadening without rate-gain

**Observation**: NaR_med and NaR_high produce HWHM = 117-120 deg (vs baseline 84 deg, delta +34 to
+36 deg) while peak rate barely moves (18-20 Hz vs baseline 17.4 Hz) and vector-sum DSI is unchanged
(0.19).

**Standard interpretation**: NaR is "inert" because peak rate and vector-sum DSI don't move much
(less than the 0.05 threshold). It does NOT trip the `is_inert` flag because the HWHM delta exceeds
5 deg.

**Alternative interpretation**: NaR's slow `s` reactivation gate (~12 ms time constant near -50 mV)
creates a "persistent floor" of sodium current at sub-threshold voltages. In the PD direction the
cell is already firing at peak rate, so NaR adds nothing. In the ND direction, where the cell is
below firing threshold, NaR's reactivation provides a small persistent inward current that pushes
the cell across threshold occasionally. This produces firing at angles where none was happening
before — broadening the tuning curve without lifting the peak. The vector-sum DSI doesn't change
because the broader curve still has the same circular concentration when you integrate
`r * exp(i*theta)` (the floor adds equally at all angles).

**Test**: Look at the NaR_high per-trial spike counts at angles 90-180 deg (the ND lobe). If those
angles have non-zero spikes for the first time (vs baseline = 0 at most ND angles), the hypothesis
is confirmed. This is a per-trial-CSV inspection, not a new experiment.

### SK_high: simultaneous sharpening + rate suppression

**Observation**: SK_high produces HWHM = 41 deg (delta -42 deg, the largest sharpening in the sweep)
while peak rate drops to 15.6 Hz (delta -2 Hz) and vector-sum DSI drops to 0.124. This is the only
channel that simultaneously narrows tuning AND suppresses overall firing.

**Standard interpretation**: SK is Ca-activated; Ca enters during PD direction high-rate firing, SK
opens, suppresses subsequent firing in PD. Net result: peak rate drops, but the suppression is
rate-selective (only PD has enough Ca to activate SK), so ND lobe is untouched and the curve
narrows.

**Alternative interpretation**: The HWHM narrowing might be an artefact of SK acting as a
"firing-rate ceiling" rather than as a direction-specific filter. If SK simply caps the maximum
firing rate, the curve becomes flat-topped near the peak, and HWHM measured by linear interpolation
around half-max becomes ill-defined and reports a small number. Look at the curve shape itself: if
SK_high produces a true narrowing (gaussian-like), HWHM is meaningful; if it produces a clipped
flat-top, HWHM is misleading.

**Test**: Plot the SK_high tuning curve in polar form. If it's flat-topped over 60-120 deg around PD
with sharp shoulders, the "narrowing" is a clipping artefact. If it's properly bell-shaped, the
narrowing is real.

### NaP_high: depolarisation block at PD, rescue at ND

**Observation**: NaP_high has the highest peak rate (74 Hz) and the lowest vector-sum DSI (0.05);
legacy DSI = 0.008 (essentially zero direction selectivity).

**Standard interpretation**: This was already known from t0067 (DSI inversion). NaP destroys DSI
because persistent Na current pushes the cell into high-firing regimes regardless of direction.

**New observation here**: HWHM = 49 deg (vs baseline 84 deg) — narrower, not broader. So NaP_high
doesn't flatten the curve uniformly; it sharpens it but in a way that destroys the PD/ND ratio.

**Alternative interpretation**: NaP_high may produce direction-selective depolarisation block. At PD
the cell is depolarised so strongly that its firing rate saturates / sub-threshold-blocks
periodically; at ND the cell fires more freely than at baseline (NaP rescues firing in normally
quiescent angles). The resulting curve is "narrow but inverted": the PD lobe is partially
suppressed, the ND lobe is partially enhanced, and the net direction selectivity flips sign.

**Test**: Look at the per-trial peak Vm for NaP_high at PD vs ND. If PD shows peak Vm > +50 mV
sustained for long stretches (depolarisation block) while ND shows clean spikes with peak Vm at +43
mV, the block hypothesis is confirmed.

### Kv3 / Kv4 / Kv7 inert: three different biophysical reasons

**Observation**: All three K-channels are flagged inert (delta less than 5 deg HWHM AND less than
0.05 vector-sum DSI at every density tested).

**Standard interpretation**: At the densities tested, none of these channels engage strongly enough
to reshape the tuning curve.

**Alternative interpretation**: The three are inert for different reasons, and a follow-up sweep
should adjust each channel's testing strategy individually rather than dismissing all three:

* **Kv3** activates fast (V_half = -15 mV) and deactivates fast. At the spike frequencies we reached
  (peak ~20 Hz baseline), Kv3 may be opening AFTER each spike's repolarisation but closing before
  the next subthreshold buildup. To engage Kv3, we'd need either much higher firing rates (where
  Kv3's role in narrow APs becomes visible) OR direct subthreshold depolarisation. Recommend: pair
  Kv3 with NaP or Nav1.6 in a co-expression sweep.

* **Kv4 / IA** has fast inactivation. The DSGC's resting potential (-60 mV) sits above Kv4's
  V_half_h (-50 mV), so Kv4 may be largely inactivated at rest. To engage Kv4, we'd need a
  hyperpolarising prepulse to remove inactivation. Recommend: test Kv4 in conditions where the cell
  is briefly hyperpolarised before the PD wave (e.g., in a paired-pulse protocol).

* **Kv7 / M-current** has V_half = -35 mV — the cell rarely sits long enough above this voltage
  for M-current to accumulate. Plus, the canonical Kv7 site is the AIS, not the soma (Hu 2007, Shah
  2008). Recommend: this is the AIS-localised Kv7 task already proposed (t0075 candidate).

### BK and SK produce a shared "Ca-driven narrowing" pattern

**Observation**: At each density level, BK and SK produce remarkably similar deltas:

* low: BK delta_hwhm = -0.16, SK delta_hwhm = -1.04; BK delta_vec_DSI = -0.02, SK -0.002
* med: BK = -6.79 / -0.04, SK = -1.04 / -0.024
* high: BK = -8.90 / -0.04, SK = -42.42 / -0.069

The high-density divergence (SK_high cuts HWHM in half) is the only big difference — at low and
med densities they look like the same channel.

**Alternative interpretation**: At low / med densities, both BK and SK act as Ca-dependent
firing-rate ceilings — they couple to the calcium pool, open during high-rate firing, and suppress
the subsequent spike. The biophysical detail (BK is V-dependent + Ca-dependent, SK is purely
Ca-driven) doesn't matter much when the cell never reaches voltages that differentiate them. At
SK_high, SK's higher density and slower kinetics dominate and produce the dramatic sharpening; at
BK_high, BK's V-dependence (V_half = -28 mV) means it deactivates faster and never gets to its full
effect.

**Test**: Run a co-expression sweep at BK_med + SK_med to see if the effects add or saturate. If
they add linearly, they're acting through the same Ca-pool channel. If they saturate (combined
effect ≈ single-channel effect), they're acting through different mechanisms.

## Hypotheses for the suggestions step

These will be formalised in the suggestions step:

1. **NaR is direction-selective at the threshold-crossing level, not at peak rate** — design a
   follow-up that records per-angle spike counts at sub-threshold angles (90-180 deg).
2. **SK_high HWHM narrowing might be a flat-top clipping artefact** — design a per-curve shape
   diagnostic that distinguishes true narrowing from clipping.
3. **NaP_high produces direction-selective depolarisation block** — record per-trial peak Vm
   trajectories and compare PD vs ND.
4. **Kv3, Kv4, Kv7 inertness should each be retested under conditions that engage them** — pair
   Kv3 with NaP (already loosely covered by t0074 itself), retest Kv4 with hyperpolarising prepulse,
   retest Kv7 at the AIS (t0075).
5. **BK + SK co-expression** — test linear-add vs saturation hypothesis with a small (4-condition)
   co-expression sweep.
