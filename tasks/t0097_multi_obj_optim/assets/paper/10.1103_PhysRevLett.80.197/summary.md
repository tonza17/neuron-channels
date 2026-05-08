---
spec_version: "3"
paper_id: "10.1103_PhysRevLett.80.197"
citation_key: "Strong1998"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---

# Entropy and Information in Neural Spike Trains

## Metadata

* **File**: `files/strong_1998_entropy-spike-trains.pdf`
* **Published**: 1998
* **Authors**: Steven P. Strong 🇺🇸, Roland Koberle 🇺🇸, Rob R. de Ruyter van Steveninck 🇺🇸, William Bialek 🇺🇸
* **Venue**: Physical Review Letters (Vol. 80, Issue 1, pp. 197-200)
* **DOI**: `10.1103/PhysRevLett.80.197`

## Abstract

The nervous system represents time dependent signals in sequences of discrete action potentials or
spikes; all spikes are identical so that information is carried only in the spike arrival times. We
show how to quantify this information, in bits, free from any assumptions about which features of
the spike train or input signal are most important, and we apply this approach to the analysis of
experiments on a motion sensitive neuron in the fly visual system. This neuron transmits
information about the visual stimulus, at rates of up to 90 bits/s, within a factor of two of the
physical limit set by the entropy of the spike train itself.

## Overview

This paper introduces what is now known as the "direct method" for estimating the information rate
that a spike train carries about a time-varying stimulus, without having to assume any particular
decoding scheme or feature of the spike train. The central insight is that the mutual information
between stimulus and spike train can be written as the difference between two entropies: the total
entropy rate `S(Δτ)` of the spike train (across all stimulus conditions) and the noise entropy rate
`N(Δτ)` measured at fixed stimulus across many repeats. Information rate is then `R_info = S - N`,
and the efficiency `ε = R_info / S` quantifies how much of the spike train representational
capacity is actually used to encode the stimulus.

The paper methodological contribution is a practical recipe for computing these entropies despite
finite recording lengths. The authors discretize the spike train into bins of size `Δτ`, read out
windows of length `T` as binary "words," tabulate word frequencies, and then combine three
techniques to handle undersampling: (a) extrapolation of the naive plug-in entropy `S_naive` to
infinite data via a `1/size` and `1/size^2` polynomial fit, (b) the Ma lower bound from coincidence
counting in fixed-spike-count sectors, and (c) extrapolation in window length `T` using the linear
approach of `S(T)/T` to its asymptote `S(Δτ) + C(Δτ)/T`. The "sampling disaster" — the value of
`T` at which `S_naive` falls below the Ma lower bound — provides a concrete diagnostic for when
the naive estimate becomes unreliable.

The authors apply this to spike trains recorded from H1, a wide-field motion-sensitive neuron in
the fly visual system, while presenting random-walk horizontal motion stimuli. They report a total
entropy rate of **157 ± 3 bits/s** at `Δτ = 3 ms`, a noise entropy rate that yields an
information rate of **78 ± 5 bits/s** (or **1.8 ± 0.1 bits/spike**), and roughly **50%
efficiency** sustained over a 400-fold range of time resolutions (`2 ms ≤ Δτ ≤ 800 ms`).
Information rates reach up to **90 bits/s** at the finest resolution. The conclusion is that fine
spike timing — down to millisecond precision — carries genuine stimulus information in a sensory
neuron four synaptic layers removed from the photoreceptors, and that this can be demonstrated
*without* a model of the neural code.

## Architecture, Models and Methods

The method has no learned model; it is an information-theoretic estimator applied to spike trains.

**Word construction.** Spike trains are discretized into bins of size `Δτ` (a binary indicator per
bin: spike vs no spike). A window of length `T` is read as a binary word of length `T/Δτ`. The
estimator sweeps `Δτ` from `800 ms` down to `2 ms` (at which point `Δτ` is roughly 5% of the
typical interspike interval) and `T` over a range up to and beyond the behavioral response time of
the fly (~30 ms).

**Naive entropy and finite-size correction.** The plug-in estimate `S_naive(T, Δτ; size)` from
word frequencies `p_i` is biased downward at finite sample size. The authors fit
`S_naive = S_0 + S_1/size + S_2/size^2` (Eq. 4) using subsamples of the recording at fractions of
the full data set; the intercept `S_0` is the extrapolation to infinite data. They also enforce the
upper bound `S(Δτ) ≤ [S(T+Δτ, Δτ) - S(T, Δτ)]/Δτ` from the supra-additivity of the entropy
(Eq. 8).

**Ma lower bound.** Following Ma (1981), the authors compute a coincidence-based lower bound on the
entropy that is stratified by spike count `N_sp` (Eq. 6). Within each `N_sp` sector, distributions
are closer to uniform so the bound is tight. The "crash" of `S_naive` below `S_Ma` at `T ~ 100 ms`
defines the onset of the sampling disaster and the maximum trustworthy window for the direct
method.

**Extensivity extrapolation.** For finite-range correlations,
`S(T, Δτ) = S(Δτ)*T + C(Δτ) + ...`, so plotting `S(T, Δτ)/T` versus `1/T` gives a straight line
whose intercept is the entropy rate. This linear regime is reached in well-sampled `T` before the
crash, providing a clean estimate.

**Noise entropy.** For each time `t` relative to the stimulus, the local conditional histogram
`p_i(t)` is computed across many repeats of the same stimulus, the local naive noise entropy
`N_naive_local(t, T, Δτ)` is then averaged over `t`, and the same `1/size` and `1/T` extrapolation
is applied. The information rate is `R_info = S - N`.

**Recording.** Tungsten microelectrode recording from H1 in an immobilized fly viewing a CRT
oscilloscope at 13.24 cm with a stimulus area of `875 deg^2` covering 3762 photoreceptors. The
stimulus is vertical bars with random grey levels undergoing a horizontal random walk in `2 ms`
steps (refresh-locked) with diffusion constant `2.8 deg^2/s`, mean radiance `180 mW/(sr*m^2)`
(approximately photon rate `5e4 s^-1` per receptor, dusk light level). Many hours of data are
collected to support the extrapolation. The data set in the H1 example contains roughly `2e5`
distinct words with significant probability at `T = 100 ms`.

## Results

* Total spike train entropy rate at `Δτ = 3 ms`: **157 ± 3 bits/s** by extrapolation, in
  agreement with the upper-bound plateau of **157 ± 4 bits/s** in the range `18 < T < 60 ms`
  (± 2.7%).
* Noise entropy rate at `Δτ = 3 ms` yields an information rate of **78 ± 5 bits/s**, or
  **1.8 ± 0.1 bits/spike**, for the H1 fly motion-sensitive neuron under random-walk stimuli.
* Across `Δτ` from `800 ms` (~30 spikes per bin) down to `2 ms` (~5% of mean ISI), the entropy
  rate varies by a factor of ~40, but information rate scales roughly proportionally — the
  efficiency `ε = R_info / S` is approximately **50%** across this range.
* Peak information rate (at the finest resolution) reaches **up to ~90 bits/s**, within a factor
  of two of the physical capacity set by the spike-train entropy itself.
* Naive vs Ma bound separation is small: `S_naive` and `S_Ma` are within **10-15%** of each other
  in the well-sampled regime; the "sampling disaster" where `S_naive` crosses below `S_Ma` occurs
  at `T ~ 100 ms` and identifies the largest trustworthy window for the direct method.
* Finite-data corrections to `S_naive` at `T = 30 ms` and `Δτ = 3 ms` are tiny (**< 1e-3**) and
  well-described by the `1/size` + `1/size^2` form (Eq. 4).
* Application to monkey V1 motion-sensitive cell data (Britten et al. 1993, via Bair & Koch 1996)
  yields **~2 bits/spike** at `Δτ = 5 ms` from just **3 minutes** of recording, demonstrating that
  the direct method is feasible on mammalian central neurons with much smaller datasets than the
  H1 baseline required.

## Innovations

### Direct (Model-Free) Estimation of Stimulus Information

The paper primary innovation is showing that the mutual information between a stimulus and a
spike train can be measured directly as `R_info = S(spike train) - N(spike train | stimulus)`, with
no assumption about which features of the spike train matter (rate, timing, bursts, etc.) and no
decoding model. This is the canonical "direct method" cited throughout subsequent
neuroscience-information-theory work and provides a model-independent yes/no answer to the question
"does spike timing carry information?"

### Practical Recipe for Finite-Data Entropy Estimation

The combination of (a) `1/size` + `1/size^2` extrapolation to infinite data, (b) Ma
coincidence-based lower bound stratified by spike count, and (c) `1/T` linear extrapolation in
window size is a self-checking pipeline. The crossover where `S_naive` drops below `S_Ma` provides
a hard diagnostic for when the estimator becomes unreliable, removing guesswork from finite-data
information measurements.

### Demonstration That Spike Timing Is Used

By measuring efficiency at progressively finer `Δτ` and showing it stays near **50%** down to
`Δτ = 2 ms`, the paper provides what was at the time the first model-free demonstration that
millisecond-precision spike timing carries genuine stimulus information in a real sensory neuron
several synapses deep into the visual system.

## Datasets

This is a methodological paper; no public datasets are released. The empirical analysis uses custom
electrophysiological recordings from H1, a single wide-field motion-sensitive neuron in the lobula
plate of the blowfly visual system, recorded in the lab of de Ruyter van Steveninck and Bialek.
Stimulus protocol: a fixed vertical-stripe pattern undergoing a horizontal random walk at `2 ms`
time steps with diffusion constant `2.8 deg^2/s`, presented on a CRT oscilloscope to an immobilized
fly. Recording duration: many hours of repeated and unrepeated trials, supporting the `~2e5`
distinct word histogram at `T = 100 ms`. A secondary, much smaller dataset (roughly 3 minutes) from
a monkey V1 motion-sensitive cell (Britten, Shadlen, Newsome, Movshon 1993; via Bair & Koch 1996)
is reanalyzed to demonstrate the method feasibility on mammalian central neurons.

## Main Ideas

* **Information rate as a difference of entropies.** For any neuron, mutual information between
  stimulus and spike train can be computed as `S - N` where `S` is the entropy rate of the spike
  train across all stimuli and `N` is the noise entropy rate at fixed stimulus measured across
  repeats. This is the practical recipe to compute the **information transmission rate (ITR)**
  objective in the t0097 multi-objective catalogue without committing to a specific neural code.
* **Repeats are mandatory.** The noise entropy `N(Δτ)` requires many presentations of the *same*
  stimulus. For the t0097 catalogue ITR objective on a DSGC model, this means the simulation
  protocol must produce many repeated runs at the same wave angle/parameters with stochastic
  synaptic input or noise, not just a single deterministic trial.
* **Finite-data corrections matter.** Use the Strong et al. extrapolation
  (`S_0 + S_1/size + S_2/size^2`) and the Ma lower bound as a sanity check. The point at which
  `S_naive` falls below `S_Ma` defines the largest window `T` you can trust; do not extrapolate
  past it.
* **Time-resolution sweep.** Compute information at a range of `Δτ` from coarse (rate-coded) to
  fine (5% of mean ISI or smaller) and report efficiency `ε = R_info / S`. A flat efficiency
  curve across `Δτ` is the model-free signature that fine timing is being used.
* **Achievable rates.** A real central sensory neuron achieves **~50% efficiency** and
  **~1.8 bits/spike**. Use these as ballpark sanity checks for ITR values produced by simulated
  DSGC spike trains in t0097.

## Summary

Strong, Koberle, de Ruyter van Steveninck, and Bialek address a foundational question in sensory
neuroscience: how much information about a time-varying stimulus does a single neuron spike train
actually transmit, and in particular, does the precise timing of spikes (down to millisecond
resolution) contribute, or is the relevant variable just the firing rate? The paper scope is
deliberately model-free — it refuses to assume any particular decoding scheme or hypothesized
feature of the code (rate, ISI, bursts, latency) — and instead grounds the measurement in
Shannon mutual information.

The core methodology is the "direct method." The spike train is discretized at resolution `Δτ`,
windowed into binary words of length `T`, and the empirical word distribution gives a naive plug-in
entropy. Three innovations make this practical at finite sample sizes: a polynomial extrapolation
`S_0 + S_1/size + S_2/size^2` to infinite data, the Ma coincidence-based lower bound stratified by
spike count, and a linear extrapolation of `S(T)/T` versus `1/T` to recover the entropy rate.
Information rate is then the difference of total spike-train entropy and noise entropy
`R_info = S - N`, where the noise entropy is computed from many repeats of the same stimulus. The
crossover where the naive estimate drops below the Ma bound provides a hard diagnostic for when
sampling becomes unreliable.

Applied to H1 in the fly visual system under random-walk motion stimuli, the method yields
`S = 157 ± 3 bits/s` and `R_info = 78 ± 5 bits/s` at `Δτ = 3 ms`, equivalent to
**1.8 ± 0.1 bits/spike** and roughly **50% efficiency**. Information rates reach **~90 bits/s**
at the finest resolution. Across a 400-fold sweep of time resolutions (`2 ms ≤ Δτ ≤ 800 ms`),
efficiency stays approximately constant — the model-free signature that fine spike timing is
genuinely encoding information. A reanalysis of monkey V1 data shows that the method works on
mammalian central neurons with as little as 3 minutes of recording.

For the t0097 multi-objective optimization task, this paper is the foundational citation underlying
the information-theoretic objective category. It supplies the concrete computational recipe —
discretize into binary words, count word frequencies, extrapolate to infinite data, subtract noise
entropy estimated across repeats — for computing the **information transmission rate (ITR)** of a
simulated DSGC spike train. The practical implications are: (i) the simulation protocol must
support many repeated trials at fixed stimulus to estimate `N(Δτ)`; (ii) ITR should be reported
across a sweep of `Δτ` so the efficiency curve can be inspected; (iii) the Ma lower bound and the
`1/size`-extrapolation are essential sanity checks that should be implemented alongside the naive
estimator; and (iv) a target efficiency in the 30-50% range with information per spike of order
1-2 bits/spike is a reasonable biological sanity-check range for the optimised DSGC model.
