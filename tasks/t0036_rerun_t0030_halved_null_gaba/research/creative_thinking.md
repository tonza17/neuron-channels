# Creative Thinking: Why Halving GABA Didn't Unpin Null Firing on t0022

## Objective

The task's working hypothesis (from S-0030-01 + t0030's compare_literature) was that
`GABA_CONDUCTANCE_NULL_NS = 12 nS` was about 2× Schachter2010's ~6 nS compound null inhibition, so
halving to 6 nS should restore non-zero null firing. Instead, null firing stayed at **exactly 0.0 Hz
at every diameter**. This document enumerates alternative explanations and recommends follow-up
strategies.

## Alternatives Considered

1. **12 nS was not 2× the threshold — it was far above it.** The t0022 schedule delivers GABA 10 ms
   before AMPA on null trials. Even at 6 nS, this early shunt may clamp distal membrane voltage well
   below AP threshold for the entire AMPA window. The null-inhibition threshold for spike
   suppression could be as low as 2-3 nS, not 6. **Supporting evidence**: peak_mv at null direction
   is deeply negative (distal peak ~+5 mV at preferred, but null likely stays below -50 mV).

2. **Timing dominates conductance.** Schachter2010's 6 nS estimate integrates a compound inhibition
   with a specific kinetic profile; scaling the peak to 6 nS doesn't reproduce the spike-allowing
   dynamics if the 10 ms pre-AMPA lead is preserved. Reducing the lead time (e.g., to 0 ms
   simultaneous or even AMPA-leads-GABA by 2 ms) may be more productive than reducing conductance.

3. **Deterministic testbed has no stochastic source to break the null clamp.** On t0022, every trial
   uses the same seed for synaptic timing. Even if the null schedule is near- threshold,
   deterministic simulation will produce 0 Hz consistently. The t0024 AR(2) schedule produces
   0.5-1.0 Hz null firing because its release times are stochastic — occasionally the AMPA arrives
   early enough to escape the GABA shunt. **Implication**: no amount of GABA reduction on t0022
   alone will produce the stochastic tail of near-threshold spikes that the DSI discriminator needs.

4. **Distal dendritic Nav channels may be saturated below threshold.** If the distal membrane never
   reaches -55 mV (HHst Nav activation), no amount of amplification will fire spikes. Inspecting the
   distal peak_mv column shows ~+5 mV at preferred direction (well above threshold) but likely -60
   mV+ at null — i.e. the null direction stays sub-threshold everywhere along the dendrite, not just
   at the soma.

5. **Compound GABA-A + GABA-B dynamics not modelled.** The t0022 GABAmod mechanism may implement
   only GABA-A; the actual DSGC in vivo experiences GABA-A + GABA-B compound inhibition with
   different kinetics. Schachter2010's 6 nS estimate is the compound, not just GABA-A.

## Recommendation

**Highest-leverage follow-up**: try a sequence of further reductions (S-0036-01: 4 nS; if still 0, 2
nS; 1 nS). If null firing remains 0 at 1 nS, the t0022 schedule is structurally incompatible with
the peak-minus-null DSI metric on a deterministic testbed.

**Second-best alternative**: adopt Poisson-noise rescue (S-0030-02 — already high priority in the
backlog) rather than GABA reduction. Poisson background at the synapse level introduces the
stochastic tail that t0024's AR(2) schedule produces naturally, restoring the DSI discriminator
without changing the schedule's inhibitory mechanism.

**Lowest-regret path**: accept that t0022's deterministic schedule cannot support primary DSI on the
distal-morphology axes. The t0033 optimiser should use vector-sum DSI (S-0030-06) as its objective
on t0022-like testbeds, OR migrate the optimisation substrate to t0024.

## Limitations

* This creative thinking didn't examine the detailed timing dynamics inside schedule_ei_onsets — a
  proper fix may require re-reading the 10-ms lead timing.
* The distal peak_mv at null direction wasn't exported by the sweep driver; would need a
  voltage-trace capture to confirm hypothesis #4.
* Cross-task comparison to t0029/t0030/t0034/t0035 V_rest data not performed.
