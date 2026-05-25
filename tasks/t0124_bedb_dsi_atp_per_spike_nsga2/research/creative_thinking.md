# Creative Thinking — t0124 DSI vs ATP-per-Spike

Out-of-the-box analysis and alternative interpretations of the gen-9 partial-front result. These are
speculative — concrete falsifiable variants of the headline conclusion that a continuation run, a
re-seeded run, or sibling-task could test.

## 1. Partial-front extrapolation: is r = +0.806 robust?

The bootstrap correlation r(DSI, ATP) = **+0.806 [0.716, 1.000]** comes from only **n=5 legit Pareto
cells** at gen 9 of a planned 60-gen run. Two competing hypotheses:

* **(A) The Carter-Bean Na/K-overlap penalty is real** — fast-spiking AIS biophysics demand more
  Na+/K+ overlap, so high-DSI cells (which need dendritic spike machinery + sharp AIS firing)
  naturally cluster at higher ATP/spike. Predicts r > +0.5 will persist at gen 60.
* **(B) The partial-front correlation is an early-NSGA-II artefact** — gen 9 has barely
  diversified the population. The pool-restart cadence (every 10 gen) hasn't fired yet (REQ-1,
  `_POOL_RESTART_EVERY=10`). Early high-DSI cells may all derive from a single ancestor with shared
  (high-Nav, high-overlap) features. Predicts r drops below +0.3 once pool-restart at gen 10 injects
  fresh ancestry and the front diversifies.

A 60-gen replication at the same seed (or a fresh seed) discriminates these. Hypothesis B is the
**deflationary null**; rejecting it strengthens the Carter-Bean interpretation.

## 2. The Cuntz cross-reference: joint geometric + metabolic cost

t0122 produced a DSI vs cytoplasm-volume Pareto front. t0124 produces DSI vs ATP-per-spike. **The
two fronts could be plotted in a 3-D (DSI, cytoplasm_volume, ATP/spike) cost space** to ask: do the
t0124 high-DSI cells also fall in the Cuntz [0.2, 0.7] balancing-factor band? If yes, the DSGC sits
at a **biologically plausible Pareto corner** trading three costs (function, wiring, metabolism) —
much stronger evidence for evolutionary optimisation than either pair alone.

The t0124 implementation already records `cytoplasm_volume_um3` as a diagnostic — the 3-D
cross-reference is one extra plot away in a follow-up.

## 3. Howarth 17%/21% vs DSGC-specific budget

The Howarth 2012 revision drops the per-spike signalling-ATP fraction from Attwell-Laughlin's 47% to
**17% cortex / 21% cerebellum**. DSGCs aren't cortical or cerebellar — they are retinal. The
retinal energy budget is dominated by photoreceptor outer-segment dark current, not by RGC spiking.
Predicts the **DSGC-specific signalling-ATP fraction may be even lower than 17%**, which would shift
the interpretation: the t0124 cells' implied ATP turnover is a smaller fraction of the retina's
total energy budget than the cortex anchor suggests.

A creative follow-up: compute the t0124 top-N cells' total ATP turnover (ATP/spike × PD-rate) and
compare against published whole-retina ATP consumption rates (Okawa et al. 2008). The DSGC may be
**energy-cheap in absolute terms even at the high-DSI corner**.

## 4. Wang 2025 contradiction: ooDSGC is high-baseline-ATP, not high-spike-ATP

The Wang 2025 paper's actual finding (per the add-paper subagent's correction) is that **αRGCs are
most active, but ooDSGCs have the highest baseline intracellular ATP**. Per-spike ATP is not
measured. This contradicts the working hypothesis that ooDSGCs are spike-energy-expensive.

Alternative interpretation: high baseline ATP in ooDSGCs may reflect **standby readiness** — the
cell maintains high intracellular ATP precisely because it doesn't spike often, and when it does
fire (during directional motion stimuli), the cost is amortised against a long quiet period. This is
the opposite of the Carter-Bean fast-spiking interpretation.

The t0124 front directly tests this if we compute **implied steady-state ATP demand** (ATP/spike ×
PD-rate × duty-cycle) for top-N cells and compare against the Wang ranking. Saved data files
already contain everything needed.

## 5. NMDA vs Nav dichotomy on the high-DSI corner

A predicted divergence on the front: **NMDA-driven high-DSI cells should be cheaper** than
Nav-driven ones because NMDA spikes are slower and have a 3:1 calcium influx ratio (calcium ATPase
is cheaper per ion than Na+/K+ ATPase per overlap-corrected Q). The pareto_front_seed6650.json
includes per-cell 68-d vectors with `gnmda_dend` and `nav16_dend_distal` — a follow-up scatter of
(gnmda_dend - nav16_dend_distal) vs ATP/spike on the top-N would test this directly.

This becomes a falsifiable mechanism prediction: if NMDA-cheap high-DSI cells exist on the front,
the Carter-Bean penalty applies only to Nav-pathway DSI; if they don't, the penalty is universal.

## 6. The "operator_stop" framework lesson

The truncation to gen 9 was triggered by the subagent's own session budget — not by the cost
watchdog, the gen ceiling, or HV-plateau detection. This is a **framework friction**: long NSGA-II
runs require either resumable checkpoints (S-0123-05) or shorter-context implementation skills that
hand off mid-run. A clean solution is to have the implementation subagent only set up + smoke gate +
launch, then return; the orchestrator polls for completion and triggers post-run analysis
separately. Current monolithic implementation skill bundles too much.

This is a candidate **self-improvement** task or framework PR.

## 7. Cross-task hypothesis on the t0122 ↔ t0124 ↔ t0123 lineage

* **t0122** (DSI + cytoplasm volume): geometric cost coupled with function — high-DSI corner
  expected to use larger dendrites (more compartments → more wiring).
* **t0124** (DSI + ATP per spike): metabolic cost coupled with function — high-DSI corner expected
  to use more Nav + more spikes → more ATP.
* **t0123** (MI + ATP per spike): function decoupled from selectivity — Pareto front directly
  comparable to Niven 2007 fly-photoreceptor curve.

The **joint analysis** across all three would yield a falsifiable picture of which costs (wiring vs
metabolism vs information) dominate DSGC function. A meta-task creating a unified comparison plot is
a strong candidate suggestion.

## Bottom Line

The gen-9 partial-front is **not a failure** — it is an early-stage snapshot whose +0.806
correlation is suggestive but not definitive. The infrastructure (smoke gate PASS, recipe
correctness validated, code forked, all charts generated) is in place for a clean 60-gen
continuation. The most valuable single follow-up is a **fresh-seed 60-gen replication** to
discriminate hypothesis (A) from hypothesis (B) in section 1.
