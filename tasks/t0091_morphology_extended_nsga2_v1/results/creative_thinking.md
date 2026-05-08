# Creative Thinking: Out-of-the-Box Reading of t0091 Results

## What the headline finding actually rules out

The plan framed this as a binary question: does morphology variation rescue biological plausibility
on the v3 substrate? The answer is **no, at this parametrisation, in 2 generations of NSGA-II**.
Three angles are worth pulling apart.

### 1. The substrate's prior violations are baked into the channel set, not the morphology

All 57 Pareto cells flag exotic or stretched on the t0086/t0088 priors. The priors that fail
**must** be those measured on the channel-set side: NaP density, NMDA per-spine conductance, GABA
spatial-gradient asymmetry. The 4 morphology priors added in `biological_priors_68d.json` (e.g.,
soma-offset bounds, dendritic-field elongation bounds, AIS-length bounds) are likely passing for
most cells — the optimiser stayed inside biologically-plausible morphology box. Morphology can't
rescue what is essentially a channel-density prior violation.

This is interesting because it inverts the usual concern. We worried morphology would let the
optimiser "cheat" by producing biologically implausible cells. The actual situation is the
**opposite**: morphology stays biologically reasonable; the channel set is what's exotic, and
nothing the optimiser does to morphology fixes that.

### 2. The symmetric anchor was completely abandoned

Anchor distribution: bedb_like 20, **symmetric 0**, pd_asymmetric 12, nd_asymmetric 9, alt_topology
16\. The symmetric anchor's score is zero — meaning the optimiser fully discarded all 19 symmetric
warm-start variants. **This is a signal**: the substrate's electrophys + spatial inhibition pattern
needs *some* morphological asymmetry (or non-Bed-B topology) to produce DS at all. Symmetric cells
under this channel set are dominated everywhere on the (DSI, PD-rate, robustness) front.

Counter-finding: the asymmetry that the optimiser preserves is **not** PD-vs-ND directional. The PD
vs ND counts (12 vs 9) are not significant (p=0.331). The "morphology asymmetry rescues
soma-displacement-toward-PD" prediction (Schachter 2010 / Trenholm 2013) is **not** confirmed.
What's preferred is *any* asymmetry, equally toward PD or ND — possibly because the eval grid is
symmetric in direction (16 directions, vector-sum DSI) and either-side asymmetric morphology
provides spatial selectivity that the symmetric one can't.

### 3. Alt-topology survived against bedb_like at almost equal weight

bedb_like 20 vs alt_topology 16 in the Pareto. The original concern in brainstorm 18 was that
alt-topology might produce no joint-pass cells. The opposite happened: alt-topology cells are well
represented even after bedb_like's strong t0083-Pareto lineage advantage. Combined with the
joint-pass cell from gen 2 being **nearest to alt_topology** (per the snapshot check earlier in this
session), this suggests:

* The substrate has at least two distinct morphological basins of joint-pass-adjacency.
* These basins differ on traits other than soma-offset asymmetry. Number of primary branches and
  Strahler depth are likely candidates.

## What this run did NOT test (alternative hypotheses for future tasks)

1. **Channel set vs morphology coupling**. We held the channel set free while morphology varied. The
   opposite — fix morphology, let priors-respecting channel set be searched — is what S-0086-01
   asks (NSGA-II re-run with tightened NMDA bounds). With $3.80 of project budget left, that's the
   natural next experiment to disambiguate channel-side vs morphology-side prior violations.

2. **Real morphology library (Option G from brainstorm 18)**. Procedural generation can't capture
   the dendritic asymmetries that real DSGCs display (Briggman 2011 SAC wiring, Wei 2011 starburst
   wiring). A NeuroMorpho.org-anchored real-cell library would test whether **specific** observed
   DSGC morphologies escape the prior-violation ceiling, even when procedural ones can't.

3. **Cross-bed validation (S-0086-06)**. We tested only Bed B (de Rosenroll 2026 port, t0024). Bed A
   (Poleg-Polsky 2016 port, t0008) has fundamentally different presynaptic encoding (gabaMOD scalar
   vs spatial bar rotation — see S-0070-01). The negative result on Bed B does not transfer to Bed
   A; the alt_topology survival result on Bed B might fail on Bed A's gabaMOD encoding.

4. **Multi-objective formulation revision**. Three objectives (DSI, PD-rate, robustness) plus
   biological-priors as a *post-hoc filter* may be wrong. If priors enter the optimiser as
   additional objectives or hard constraints, the Pareto might spread differently. Hay 2011 multi-
   objective biophysics work is precedent.

5. **Tuning-curve shape, not vector-sum DSI**. Vector-sum DSI is direction-blind; it averages across
   the orientation tuning. Brendly 2025 / Riccitelli 2025 (now in the corpus) report
   *direction-tuning* DSGC subtypes that vector-sum collapses. A future task could re-evaluate
   t0091's 57 Pareto cells under per-direction DSI to surface subtype-specific rescues that the
   current scoring missed.

## What surprises me as a meta-observation

The cost-watchdog never triggered. The plan estimated $3.00–3.50 for 8 generations; we landed at
$0.65 for 2 generations. The HV trajectory went 14.07 → 23.71 in two gens (+68%) and was very
likely still climbing — but we stopped when the implementation subagent decided 57 Pareto cells
were enough to satisfy REQ-10. **That's a process pattern worth flagging**: experiment cost can drop
dramatically when REQ-fulfilment thresholds are conservative. The flip side is we cannot rule out
gen 3+ producing a biologically-plausible joint-pass that didn't exist in gens 1–2.

## Practical follow-up recommendation

The cheapest, most informative next experiment is a **constrained re-run on the same substrate** at
fixed t0093 morphology with priors-respecting NMDA bounds (S-0086-01, ~$1.50). This isolates the
channel-side prior-violation question. If priors-respecting NMDA + fixed morphology *also* fails to
produce joint-pass cells, the v3 substrate is genuinely incompatible with biological plausibility
and Option G real-cell library is the only escape route. If it succeeds, the v3 substrate is
rescuable on channel parameters alone, and morphology was a red herring.
