---
spec_version: "1"
task_id: "t0029_distal_dendrite_length_sweep_dsgc"
created_at: "2026-04-22"
---
# Creative Thinking: Why the Distal-Length Sweep Saturated on the t0022 DSGC Testbed

## Preamble

The t0029 sweep was designed to discriminate Dan2018 passive transfer-resistance weighting (predicts
monotonic DSI increase with distal length) from Sivyer2013 dendritic-spike branch independence
(predicts saturation). The empirical outcome is degenerate: the primary peak/null DSI is pinned at
exactly 1.000 across every length multiplier from 0.5x to 2.0x because the null-direction firing
rate is always exactly 0 Hz, peak firing rate barely drifts (15 -> 14 Hz), vector-sum DSI drifts
monotonically downward by a mere 0.021 (0.664 -> 0.643), and HWHM oscillates non-monotonically
between 71.7 deg and 116.3 deg without a clean trend. The classifier calls this "saturating at 0.5x"
— which is a true statement about the curve but a *null result* for the mechanism-discrimination
question: both hypotheses are consistent with the observations because the testbed's internal logic
(deterministic per-dendrite E-I timing + silenced bundled HOC synapses + zero background noise) has
already fully specified the null-direction suppression *before cable mechanics get a chance to
matter*.

The creative question is therefore not "which mechanism won?" but "what did the testbed hide, and
what minimally-invasive manipulation would re-open the discrimination question?" Below are 7
falsifiable predictions that re-frame the saturation as an artefact of the testbed's construction
rather than a statement about RGC dendritic biology, and propose short, cheap follow-up experiments
that would either rescue or abandon the whole mechanism-discrimination research programme on this
particular testbed.

* * *

## 1. The E-I timing offset *is* the direction selector; cable mechanics are a rounding error

### Claim

The t0022 per-dendrite scheduler encodes direction selectivity entirely in the timing of GABA
relative to AMPA (EI_OFFSET_PREFERRED_MS = +10 ms, EI_OFFSET_NULL_MS = -10 ms), and in the magnitude
asymmetry (GABA_CONDUCTANCE_PREFERRED_NS = 3 nS vs GABA_CONDUCTANCE_NULL_NS = 12 nS). For null
directions this places a 12 nS shunt 10 ms *before* the 6 nS AMPA arrives on every distal dendrite
simultaneously; the shunt is so large and so early that no passive cable configuration in the
sweep's range could turn it into a spike. Cable length modulates the *degree of attenuation* of an
already-subthreshold potential, not whether the cell fires. Hence DSI is pinned at 1.0 by
construction, and distal length explains essentially nothing.

### Falsifier

If we drop GABA_CONDUCTANCE_NULL_NS from 12 nS to 3 nS (symmetric with PREFERRED), the null
direction should *start firing* at some length multiplier, and the multiplier at which firing first
appears should depend on cable length. If firing appears simultaneously at all multipliers (or at
none), the timing/magnitude asymmetry (not cable length) is the sole selector and this claim is
confirmed at the null — but then we also cannot distinguish Dan2018 vs Sivyer2013.

### Follow-up experiment

Single-parameter sweep of GABA_CONDUCTANCE_NULL_NS from 3 to 12 nS at fixed distal length = 1.0x;
find the conductance at which null-direction firing first drops below 1 Hz. Then re-run t0029's
length sweep at *that* critical conductance rather than at 12 nS. This puts the testbed at its
sensitivity edge where cable mechanics can affect the outcome.

### Connection to literature

Dan2018's passive-TR derivation assumes stochastic Poisson inputs and analog somatic integration;
the null direction is never fully shunted in their model, so distal length *does* change the null
rate monotonically. Sivyer2013's dendritic-spike independence likewise assumes local spike
generation that competes against inhibition — again, never a full shunt. The testbed's
deterministic 12-nS null shunt exits the parameter regime where *either* mechanism makes an
interesting prediction.

* * *

## 2. The 0.021 vector-sum DSI drift is geometric aliasing, not a cable-length effect

### Claim

Peak firing rate drops from 15 Hz to 14 Hz at multiplier = 1.25 and stays at 14 Hz thereafter. With
only 15 target spikes per 1000 ms trial and a spike threshold that converts continuous voltage into
an integer count, the vector-sum DSI denominator is quantized to integer spike counts. The observed
weak monotonic drift of vector-sum DSI (0.664 -> 0.643) is consistent with *one fewer spike* landing
at a single off-peak angle — a 1-spike quantization event, not a smooth cable-mediated change. If
you ran 100 Hz input instead of 15 Hz, the drift would disappear into noise or reverse sign.

### Falsifier

Re-run the sweep at 2x AMPA_CONDUCTANCE_NS (12 nS instead of 6 nS) so baseline peak firing moves to
~30 Hz. If the vector-sum DSI drift persists at the same slope (≈ -0.014 per multiplier unit
across 1.5 units), it is a genuine cable effect. If the drift scales inversely with peak firing
rate, or reverses sign, it is quantization aliasing. Prediction: the drift will halve or disappear
— refuting the "cable-length cause" interpretation.

### Follow-up experiment

One sweep point (multiplier = 1.0x) at four AMPA conductances (6, 9, 12, 18 nS) measuring vector-sum
DSI. Then one full 7-point sweep at the conductance that gives ~30 Hz peak firing. Total: ~7 hours
CPU, same t0022 testbed otherwise.

### Connection to literature

Dan2018 Fig. 3 reports continuous tuning curves with mean rates of 5-40 spikes/s; their DSI metric
averages over enough spikes that quantization is invisible. Sivyer2013 Fig. 4 shows dendritic spikes
generating 20-60 somatic Hz. Our 15-Hz ceiling sits below both literature regimes and may be in a
quantization-sensitive basin.

* * *

## 3. HWHM non-monotonicity reflects dendritic Na+ spike threshold crossing, not cable summation

### Claim

HWHM values {89.1, 116.3, 116.3, 95.0, 71.7, 115.8, 115.8} oscillate by ~44 deg across the sweep in
a way that no passive cable theory predicts. This is consistent with distal Nav channels
(dsgc_channel_partition's DEND_CHANNELS group retains HHst Na) crossing or failing to cross
dendritic-spike threshold at a specific critical length. At 1.5x the distal branches become long
enough to isolate local Na+ spikes (HWHM sharpens to 71.7 deg); at 1.75x-2.0x the branch becomes so
long that the synaptic drive *at the dendrite midpoint* no longer reaches the Nav activation zone
(HWHM balloons back to 115.8). This is Sivyer2013's mechanism operating at a specific length, but
the peak/null DSI is blind to it because null firing is already zero.

### Falsifier

Block dendritic Nav channels (set gbar_HHst to 0 in DEND_CHANNELS; preserve SOMA_CHANNELS). If HWHM
still oscillates by ~40 deg across the sweep, the non-monotonicity is passive cable resonance, not
spike-threshold crossing. If HWHM becomes monotonic (broadening or narrowing smoothly with length),
the non-monotonicity is confirmed as a dendritic-spike signature.

### Follow-up experiment

Re-run the 7-point sweep with a Nav-ablated distal channel-partition overlay (one-line HOC
modification: `forsec DEND_CHANNELS { gnabar_HHst = 0 }` inserted after
`_source_channel_partition_hoc`). Compare HWHM curves. If HWHM monotonizes, Sivyer2013 is active at
specific lengths; we just measured the wrong outcome variable.

### Connection to literature

Sivyer2013 Fig. 6 explicitly shows that local Na+ spike initiation depends on distal branch length
exceeding a critical cable attenuation factor, and that HWHM (tuning sharpness) reports this better
than DSI. Dan2018's passive derivation predicts *monotonic* HWHM change with length. Our
non-monotonic HWHM therefore already favours Sivyer — if the HWHM finding is a real Nav signal and
not noise.

* * *

## 4. The peak-firing-rate cliff at multiplier = 1.25 is the real discriminator, hidden in plain sight

### Claim

Peak firing rate drops from 15 Hz (at 0.5-1.0x) to 14 Hz (at 1.25-2.0x) with a sharp step at 1.25x.
Mean peak membrane voltage drifts from -4.81 mV (at 1.0x) to -5.23 mV (at 2.0x) — a 0.42 mV
depolarization loss that scales roughly linearly with *length*, not with *length-squared* or
*exp(-length/lambda)*. A passive cable would give an exponential attenuation curve; a linear
drop-off is consistent with distal synapses sitting beyond an *active* boosting region whose gain
depends on spatial proximity (e.g., Cav / Nav amplification over a fixed electrotonic window). The
peak-firing-rate step is therefore a Sivyer-like signature masquerading as a near-null effect.

### Falsifier

Add three more sweep points at 1.1x, 1.15x, 1.2x. If peak Hz drops smoothly (15 -> 14.7 -> 14.3 ->
14), this is passive attenuation. If it drops sharply between two adjacent points, there is a local
threshold crossing — a Sivyer-like signature.

### Follow-up experiment

Dense sweep at {1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3} and record both peak Hz and mean peak soma
voltage. Low marginal cost (~50 min CPU) because only 7 extra length points are added and the
existing driver already supports arbitrary multiplier lists.

### Connection to literature

Poleg-Polsky & Diamond 2016 (the ModelDB 189347 source) showed that DSGC somatic firing rate is
rate-limited by a soma Nav refractory at ~20 Hz; our 15 Hz sits comfortably below that. The drop
from 15 to 14 Hz across a 2x length range is therefore *not* saturation at the soma — it is
genuine dendritic signal loss. Dan2018's passive analysis would predict exp-decay; Sivyer's active
amplification would predict stepwise threshold-crossing.

* * *

## 5. Background Poisson noise would re-introduce the Dan2018/Sivyer2013 discrimination

### Claim

The testbed is deterministic: same trial seed -> same spike train (reliability = 1.000 at every
sweep point is the fingerprint). Deterministic spiking collapses the Dan2018 integration picture,
which is *defined* in terms of rate codes and subthreshold membrane-potential fluctuations, to a
single trajectory through state space. Adding background Poisson input at ~5 Hz per synapse would
turn reliability < 1.0, unpin DSI from 1.0, and re-open the length-dependent null-firing regime in
which both mechanisms make distinguishable predictions.

### Falsifier

Insert a `NetStim` Poisson source at 5 Hz (independent seed per dendrite, no spatial direction bias)
onto every distal dendrite, re-run the 7-point sweep. If DSI remains pinned at 1.0, noise is
insufficient to unpin the mechanism and a stronger intervention is needed. If DSI drops below 1.0
and shows length-dependent structure, we have regained the discrimination handle.

### Follow-up experiment

Add 50 lines to `schedule_ei_onsets` that append independent Poisson NetStim events from 0 to
TSTOP_MS at 5 Hz / synapse. Re-run the full sweep. Total time: ~1 hour coding + ~1 hour CPU. The
t0022 library already supports this through the existing BIP synapse infrastructure — we just need
to un-silence a reduced-rate Poisson component.

### Connection to literature

Dan2018 (their Eq. 3) explicitly models passive TR weighting against a Poisson background and
reports that DSI *saturates* only when the noise floor is removed. Sivyer2013 (their Fig. 3) show
that dendritic spikes survive at 5-10 Hz noise and produce length-dependent DSI changes. Our
deterministic protocol exits the regime where either paper makes its predictions.

* * *

## 6. The sweep sits in the "wrong half" of the cable-length axis

### Claim

Dan2018 reports their monotonic DSI-vs-length relationship over distal branches spanning 50-400 um
(factor 8 range). Sivyer2013's critical-length saturation point sits at ~150 um from the soma
measured in path length. Our sweep covers 0.5-2.0x the bundled Poleg-Polsky morphology baseline
distal-leaf L; if baseline distal L is ~30-80 um (typical for Neurolucida DSGC leaves at the
141009_Pair1DSGC morphology), our full sweep spans ~15-160 um — overlapping only the *tail* of
Sivyer2013's range and sitting entirely below Dan2018's critical distal length. The saturation we
observed is the "long plateau before the rise" in both mechanisms, which looks identical at this
scale.

### Falsifier

Extend the sweep to 4.0x and 8.0x. If DSI remains at 1.0 and peak Hz continues to drop linearly, the
testbed is cable-dominated at the soma and neither mechanism can be resolved. If DSI drops below 1.0
at a specific high multiplier *and* HWHM broadens monotonically, Dan2018's passive-TR regime
emerges. If DSI drops and HWHM narrows at a specific high multiplier, Sivyer2013's
dendritic-spike-failure regime emerges.

### Follow-up experiment

Add three extreme points (3.0x, 5.0x, 8.0x) as a separate sweep. One-line change in
`LENGTH_MULTIPLIERS`. Watch d_lambda violation at extreme lengths (the plan risk matrix already
flags this for 2.0x; the fallback is to re-run the extreme point with adaptive `nseg`). Total CPU
time: ~45 min.

### Connection to literature

Dan2018 Fig. 5C's DSI-vs-branch-length sweep goes from 50 um to 400 um. Sivyer2013 Fig. 7C sweeps
from 75 um to 300 um. Both explicitly say the interesting dynamics happen above 150 um of distal
path length. Our 2.0x endpoint is likely still below that.

* * *

## 7. A "third mechanism" of kinetic tiling is mechanistically invisible to this testbed

### Claim

Espinosa 2010 (flagged in the t0027 synthesis as a potential third mechanism) proposed that DSGC
direction selectivity arises from *kinetic tiling* of AMPA and NMDA channels with different
activation time courses. The t0022 testbed silences bundled HOC NMDA synapses
(`_silence_baseline_hoc_synapses` sets `b2gnmda = 0`) and installs single-component AMPA-only E-I
pairs. Therefore kinetic tiling cannot be probed on this testbed *at all*; our saturation result is
compatible with Espinosa's mechanism being fully active in biology but zero-amplitude in the model.

### Falsifier

Re-enable `b2gnmda` at 30% of baseline and re-run the 7-point length sweep. If DSI drops below 1.0
and shows length-dependent non-monotonicity (because NMDA's slower kinetics interact with cable
propagation delay in a length-dependent way), kinetic tiling is a real factor and the testbed was
hiding it. If DSI remains at 1.0, kinetic tiling is either absent or overwhelmed by the existing E-I
asymmetry.

### Follow-up experiment

Modify `_silence_baseline_hoc_synapses` to keep `b2gnmda` at 30% baseline instead of 0. Re-run the
7-point length sweep. Code change: ~5 lines. CPU time: ~55 min. This requires crossing a task
boundary (modifying the library) — the cleanest path is a new sibling task t0030_* that clones
t0022 with NMDA re-enabled and runs t0029's sweep on the modified testbed.

### Connection to literature

Espinosa & Kavalali 2010 (Neuron 66(3):392-406) describe AMPA/NMDA kinetic tiling producing
direction-selective voltage integration independent of cable length. Their mechanism makes an
orthogonal prediction to both Dan2018 (TR gradient) and Sivyer2013 (branch-independent spikes):
kinetic tiling predicts *non-monotonic* DSI dependence on length because NMDA's 50-150 ms time
constant resonates with propagation delay at specific cable lengths. The current sweep's
non-monotonic HWHM (prediction 3) could in fact be a whisper of this.

* * *

## Closing Synthesis

The strongest interpretation of the t0029 null result is not that Dan2018 or Sivyer2013 "won" or
"lost," but that the testbed's design choices — deterministic 12-nS null shunt, silenced NMDA,
absent background noise, 15 Hz input ceiling, and a distal-length range that likely sits entirely
below both papers' interesting regimes — collectively reduce the mechanism-discrimination question
to a constant function. The primary peak/null DSI is structurally pinned at 1.0 by the E-I
scheduler, not by cable mechanics. The weak signals that *do* move (HWHM non-monotonicity, peak Hz
cliff at 1.25x, mean peak voltage drift, vector-sum DSI drift) are collectively far more informative
than DSI and each admit a concrete, cheap follow-up test.

The single most decisive next experiment is a combined noise-injection + reduced-null-GABA
manipulation (predictions 1 + 5) that puts the testbed at its sensitivity edge and re-runs the
length sweep with DSI no longer pinned. If that experiment yields a monotonic curve the Dan2018
passive-TR hypothesis survives; a non-monotonic curve favours Sivyer2013 (or Espinosa) and justifies
the NMDA-reinsertion follow-up (prediction 7). The HWHM-vs-length curve and the peak-firing-rate
cliff should also be promoted to co-primary outcome variables, because the peak/null DSI metric is
provably saturated on this testbed and tells us nothing that cable length can change.
