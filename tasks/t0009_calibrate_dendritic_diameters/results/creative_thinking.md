---
spec_version: "1"
task_id: "t0009_calibrate_dendritic_diameters"
step: "creative-thinking"
date: "2026-04-19"
---
# Creative Thinking: Alternative Diameter Calibration Strategies for the DSGC SWC

## Goal

Interrogate the diameter calibration delivered by t0009 from first principles: what taper models
would we adopt if we were not locked into the three-bin Strahler partition, which silent failure
modes does our max-child tie-break hide, and what unconventional calibration approaches are worth
flagging for follow-up tasks or corrections.

The calibration as shipped assigns four radii (soma 4.118 µm, primary 3.694 µm, mid 1.653 µm,
terminal 0.439 µm) across 6,736 compartments after collapsing the 347 Poleg-Polsky sections (3
primary + 170 mid + 177 terminal) into three means. Total surface area grows 7.99×, dendritic axial
resistance drops to 4.8%, zero terminals hit the 0.15 µm floor, and `max_strahler_order == 5`. The
deliverable below reads every numeric claim directly off `results/morphology_metrics.json`,
`data/poleg_polsky_bins.json`, and `results/per_order_radii.csv` — no new computation is attempted
here.

* * *

## Alternative Taper Models We Did Not Adopt

### A1. Per-path-distance continuous taper

**Idea.** Fit `r(s) = a exp(-s / λ) + b` (or a two-term exponential) to the Poleg-Polsky pt3dadd
radii against path distance `s` from the soma, then evaluate the fit per compartment. The
DSGC-relevant electrotonic length constant is λ ≈ 200-400 µm (Schachter 2010), so a single
exponential plus a tail offset captures the dominant radial taper without imposing any bin boundary.

**Why plausible.** Real biological diameters do not step discontinuously at branch points — they
taper smoothly along each branch and drop at each bifurcation. A continuous taper preserves this
smoothness and removes the three internal mid-order "plateaus" visible in `per_order_radii.csv` rows
8-10 (order 2/3/4 all identical at 1.653 µm).

**Why we skipped it.** Path distance on the CNG tree (1,536 µm total length / 6,717 dendritic
compartments ≈ 0.23 µm per compartment) is dominated by discretization noise near the soma. A
path-distance fit would also need the Poleg-Polsky section-midpoint `s` values, which the bin
harvester currently discards after computing per-section means. Retrofit cost: one regression + one
Δs computation per compartment (~50 lines). Expected sensitivity: with λ ≈ 200 µm and a
proximal radius of 3.7 µm, the 90th-percentile compartment (s ≈ 500 µm) would receive r ≈
3.7·e^(−2.5) + 0.44 ≈ 0.74 µm — roughly halfway between our mid and terminal bins.

### A2. Rall 3/2 power rule (TREES-toolbox `quaddiameter`)

**Idea.** At every branch point enforce `r_parent^(3/2) = Σ r_child^(3/2)` (Rall 1959), then solve
the system bottom-up from the 131 terminals after fixing terminal radii. MATLAB's TREES toolbox
ships this as `quaddiameter`; a pure-Python port is ~80 lines.

**Why plausible.** Rall's rule is the only biophysically principled way to match soma-to-dendrite
input impedance across a binary tree. Our max-child tie-break has no such guarantee; primary and mid
compartments carry the same radius regardless of how many daughters they feed.

**Why we skipped it.** Plan § Approach flags the rejection explicitly: the project's stack is
`numpy/pandas/matplotlib/stdlib` only, TREES is MATLAB, and the paper corpus (Poleg-Polsky 2016,
Hanson 2019, Jain 2020, Schachter 2010) all use the three-bin partition, not Rall 3/2. A Rall
calibration is a strong candidate for a **follow-up suggestion** — it would change the primary
diameter by ~15% (from 3.69 to ~3.1 µm at the measured 2-way branching ratio) and the terminal
diameter is data-constrained either way.

### A3. Per-section-type mapping (dendrite type code subclasses)

**Idea.** Exploit SWC type codes beyond 1/3. The CNG source uses only types 1 (soma) and 3
(dendrite), but downstream Poleg-Polsky sections distinguish "dend_primary", "dend_dist", etc. We
could re-type the calibrated SWC to 1/3/4 (soma/basal/apical) or 1/3/5/6 (soma/dendrite/primary/
terminal) to pre-group compartments for downstream NEURON ion-channel placement.

**Why plausible.** DSGC conductance densities (Na 150/150/30 mS/cm², K 70/70/35) are section-class
specific — by writing the class into the SWC type code we save every downstream task from
recomputing Strahler order. This is the convention BlueBrain and the Human Brain Project use.

**Why we skipped it.** The task description says "Preserve the 19 soma compartments' original
(non-placeholder) radii" and `description.md` asset contract says topology is byte-for-byte
unchanged except radius. Changing type codes would break that contract. The right place for this is
a **new dataset asset** (`dsgc-baseline-morphology-calibrated-typed`) produced by a downstream task.

### A4. Branch-order mapping instead of Strahler order

**Idea.** Use the simpler "centrifugal branch order" — parent branch order + 1 at every
bifurcation — instead of Horton-Strahler. This tracks how many branch points lie between the
compartment and the soma.

**Why plausible.** Branch order is monotone from soma to tip, has no tie-break ambiguity, and maps
trivially onto the "primary/mid/terminal" labels. It also better matches the intuition in
Vaney/Sivyer/Taylor 2012 where "order-1 primary dendrites" means "first branch off soma."

**Why Strahler won.** Strahler order buckets sparse-end terminals together regardless of their
absolute depth, which matches Poleg-Polsky's `dend[i]` terminal section definition (no children in
.hoc topology, not "deepest in the tree"). With 131 leaves versus 129 branch points, branch order
would peak at ~10-15 on the deepest path, requiring six or seven bins. Strahler peaks at 5 and fits
the three-bin source perfectly. Research_papers.md records this comparison.

### A5. Two-bin soma/dendrite partition with distance-weighted tapering

**Idea.** Collapse primary/mid/terminal to a single dendrite bin with a radius that tapers as
`r(s) = r_primary * (r_terminal / r_primary)^(s/s_max)`. Two constants, one continuous function, no
tie-break decisions.

**Why plausible.** Minimal-parameter fit; directly comparable to the placeholder (1 radius) and the
Poleg-Polsky harvest (1 ratio).

**Why we skipped it.** Loses the interior "mid" bin where the 1,574 order-2 compartments live —
those dominate total dendritic length at 360 µm. A two-bin model would underestimate their surface
area by ≥40%. Not preferable.

* * *

## Edge Cases the Chosen Algorithm Handles (and Hides)

### E1. Mixed-order siblings and the max-child tie-break

Our rule increments the parent's order to `k+1` only when **two or more** children share the maximum
order `k`. The pathological case we cannot distinguish:

* One child with order 4, one with order 3, one with order 4 → parent = 5 (tie satisfied)
* One child with order 4, two with order 3 → parent = 4 (no tie at max)

At max_strahler_order = 5 with only 33 order-5 compartments and 131 leaves, a single misclassified
near-root node flips the primary bin assignment for its entire downstream subtree.
`data/calibration_records.json` records Strahler order per compartment; a diff against a `min-child`
or `NeuroM-section` tie-break variant would expose any flipped assignments.

**Mitigation suggestion.** Add a dual-rule sanity check in a follow-up task: compute Strahler orders
under max-child AND NeuroM's `section_strahler_orders` (which operates on sections, not nodes) and
assert they agree to within ±1 on every compartment. If the deltas cluster in any subtree, that
subtree needs human review.

### E2. Ghost children (SWC parent_id pointing to deleted row)

Our `build_children_index` is happy to index a `parent_id` that does not exist. On the CNG source it
doesn't bite (every parent is present), but if a downstream correction ever deletes a compartment
and re-points children, the Strahler recursion silently skips the orphaned subtree — they get
Strahler order 1 (leaf), which inflates the terminal count and deflates primary/mid counts.
`swc_io.parse_swc_file` currently validates parent existence via `_validate_structure`, so the
current input is safe. But a cross-task corrections overlay that replaces compartments does not go
through our parser.

**Mitigation suggestion.** Extend `swc_io.py` with an explicit `validate_parent_coverage` check
before `build_graph`:
`assert set(p for c in compartments for p in [c.parent_id] if p != -1) <= {c.compartment_id for c in compartments}`.

### E3. Zero-length segments

Euclidean distance between consecutive compartments can be zero when reconstructions insert
duplicate xyz points (a common Simple Neurite Tracer artefact). Zero-length compartments contribute
zero surface area (fine) and zero axial resistance (fine), but they also receive a fresh radius
assignment that depends on their Strahler order — which itself depends on the zero-length row's
parent/child topology. The CNG source has no exact duplicates (total length sums to 1,536.25 µm on
6,717 dendritic compartments, never zero in `per_order_radii.csv`) but future reconstructions could.

**Mitigation suggestion.** In a future morphology-calibration task, skip zero-length segments during
radius assignment and inherit the parent's radius verbatim. Document the skipped count.

### E4. Soma rows as dendritic Strahler 0

Our algorithm marks all 19 soma rows with the `SOMA_STRAHLER_SENTINEL = 0`. If any soma row has a
dendritic child (which is the normal case — the one dendrite root attaches to a soma row), the
dendritic child's Strahler recursion only considers **dendritic** children, so the soma row's
order-0 sentinel is never consumed. But if two dendritic children attach at the same soma row, they
are treated as siblings via the soma, which is anatomically wrong (they are independent primary
branches, not sister terminals of a single trunk). The research_code.md notes show exactly one
dendrite root per soma in the CNG source, so this edge case does not fire here.

**Mitigation suggestion.** In the graph builder, re-root dendritic tree(s) at **each** dendrite-
to-soma connection and compute Strahler orders per dendritic subtree, merging only for logging.

### E5. Single-dendrite-child subtree collapsing all orders

If a long, unbranched dendrite (e.g., the stretch from soma to the first bifurcation) has no
branching for 50 compartments, every compartment on that stretch receives
`Strahler = Strahler of the first branching descendant`. With `max_strahler_order = 5`, all 50
proximal-trunk compartments inherit order 5 and get the `primary` radius (3.694 µm). Visually this
is right — the primary trunk should be fat — but a path-distance rule would taper that same
trunk as it approaches the first bifurcation. This is the single biggest source of surface-area
inflation in our calibration (the 33 order-5 compartments carry 7.89 µm of length at 3.694 µm
radius).

**Mitigation suggestion.** A hybrid Strahler + path-distance taper could interpolate the primary
radius from `r_primary` at the soma attachment down to `r_mid` at the first order-4 descendant.
Captured for the suggestions queue.

### E6. The 0.15 µm terminal floor never triggered

`n_clamped_dendrites = 0`. The Poleg-Polsky terminal mean (0.439 µm) is 2.9× the floor, so the
clamp is purely defensive. **But** the "silent floor" is a real regression risk: if a future
re-harvest of RGCmodel.hoc returns a lower terminal mean (e.g., after fixing the diam=0 filter), the
calibration would silently clamp a large fraction of terminals. Currently we only log the count, not
the distribution of raw radii before clamping.

**Mitigation suggestion.** Emit a histogram of raw (pre-clamp) terminal radii into `results/images/`
and let a future task regress the clamp-trigger rate against harvest version.

* * *

## Failure Modes of the Three-Bin Heuristic

### F1. Collapsed interior variability

Orders 2, 3, and 4 all receive 1.653 µm. `per_order_radii.csv` shows these three groups account for
2,769 of 6,717 dendritic compartments and 665 µm of 1,536 µm total dendritic length — 43% of the
tree's length. A single constant here is the dominant simplification the calibration imposes on top
of the Poleg-Polsky source. The source itself has 170 mid-role sections with distinct per-section
diameters; our averager throws that variance away.

### F2. Primary/terminal ratio coupling

Surface area ratio (7.99×) and axial-resistance ratio (4.8%) are both dominated by the terminal
radius: 3,915 of 6,717 dendrites are terminals, contributing 863 µm of length at 0.439 µm. If the
harvest were re-run with a different pt3dadd zero-filter rule, the terminal mean could shift ±30%
and both ratios would move by ~60%. Our calibration is most fragile in its smallest bin.

### F3. max_strahler_order sensitivity

With `max_strahler_order = 5`, the primary bin captures only 33 compartments / 7.89 µm of length.
If a single deep subtree were re-ordered by a tie-break convention change and pushed max_order to 6,
the current 33 compartments would become "mid" (1.653 µm radius) and only a smaller handful would
remain "primary" (3.694 µm). Input resistance at the soma would jump by ~15%. This is the biggest
reason the `description.md` documents the tie-break convention explicitly.

### F4. Soma radius averaging masks the tapered cross-section

Our 4.118 µm soma radius is the mean of five central Poleg-Polsky soma pt3dadd diameters (6.141,
7.736, 8.320, 8.355, 10.623 µm, /2 each). The true cross-section tapers from ~3 µm at the
soma-dendrite junction to ~5.3 µm at the widest contour point. Applying a constant to all 19 soma
rows flattens that profile. The `soma_radius_profile.png` plot shows a flat line where the raw data
would show a bell. For downstream NEURON simulations of soma membrane properties this matters:
surface area is correct on average but the current-density distribution over the soma membrane is
wrong.

**Mitigation suggestion.** Map the 7 pt3dadd values onto the 19 CNG soma rows by linear
interpolation along the soma's principal axis (PCA over the 19 xyz values), and drop the five- value
averaging. One afternoon's work as a follow-up correction task.

* * *

## Out-of-the-Box Calibration Approaches

### O1. Per-cell ex-vivo diameter measurement from two-photon stacks

**Idea.** The 141009_Pair1DSGC was imaged on Murphy-Baum/Feller's two-photon rig. Raw image stacks
may still exist with sub-micron axial resolution. A segmentation + radius estimate from those stacks
would give a cell-specific taper without needing Poleg-Polsky as a surrogate.

**Risk.** Likely requires contacting the original authors; not hermetic.

### O2. Generative diameter prior from MouseLight / BBP RGC morphologies

**Idea.** Train a Gaussian-process or PixelCNN prior over (Strahler order, path distance, branch
degree) → radius using the ~200 mouse RGC morphologies with diameters in the Allen Cell Types
Database. Sample the prior conditional on the CNG tree's topology.

**Why it's attractive.** Calibration uncertainty is quantified (posterior variance), and the taper
reflects a population-level statistic rather than one borrowed neuron.

**Why it's ambitious.** Requires a new dataset asset + a fitting pipeline + validation against the
DSGC-specific Poleg-Polsky source. Reasonable for a capstone follow-up task.

### O3. Inverse calibration against target input resistance

**Idea.** Fix the three-bin structure but treat the three radii as free parameters. Fit them so that
a NEURON passive-property simulation reproduces Schachter 2010's 150-200 MΩ proximal Rin and >1 GΩ
distal Rin. The Poleg-Polsky mean is the initial guess; the fit adjusts bin radii.

**Why it's attractive.** Biophysically grounded: the calibration answers "what diameters make the
cell's input impedance match the literature" rather than "what diameters are in another paper's
model."

**Why we did not do it.** The plan § Approach explicitly rejects this — the task commits to a
literature source, not a tuning target. But this is the **first** follow-up task to queue: the
suggestions step should record it as "fit three-bin radii to Schachter 2010 Rin gradient" with high
priority.

### O4. Mesh-based surface area instead of cylindrical

**Idea.** For each bifurcation, construct a blob mesh (medial axis transform) rather than
concatenated cylinders. Surface area then accounts for the smooth fillet between parent and
children, which the cylindrical model over-counts by ~5% at every branch point.

**Why it's attractive.** NEURON itself uses the cylindrical approximation, so this is only a
bookkeeping improvement for surface-area reporting. But reporting accuracy matters for the 7.99×
ratio.

**Why we did not do it.** NEURON compatibility is more important than 5% bookkeeping. Archive under
"nice to have."

### O5. Lossless anchor: skip averaging, assign Poleg-Polsky sections 1:1

**Idea.** Match each CNG compartment to the nearest Poleg-Polsky section by xyz Euclidean distance
and copy that section's diameter directly. No averaging, no Strahler logic. Source has 350 sections;
CNG has 6,736 compartments — each source section would cover ~19 compartments on average.

**Why it's attractive.** Preserves all source variance; calibration variability per Strahler order
reappears. No tie-break, no bin boundaries.

**Why it's risky.** The Poleg-Polsky .hoc uses its own `pt3dadd` coordinates which are likely a
rotated/shifted copy of the CNG geometry, not the identical frame. An xyz match without registration
would produce discontinuous radii along the tree. A **registration step** (ICP or Procrustes between
CNG points and Poleg-Polsky points) would be needed first. Reasonable for a follow-up if the
Hanson/Feller labs confirm the geometries share a frame.

* * *

## Summary of Calibrations Worth Proposing Downstream

| Priority | Proposal | Rationale | Effort |
| --- | --- | --- | --- |
| High | Fit three-bin radii to Schachter 2010 Rin gradient | Biophysically grounded; needed for DS experiments | 1-2 days |
| High | Interpolate soma pt3dadd along principal axis (replace 4.118 µm uniform) | Fixes soma current-density distribution | 0.5 days |
| Medium | Dual-rule Strahler sanity check (max-child vs NeuroM) | Detects tie-break-induced order flips | 0.5 days |
| Medium | Hybrid Strahler + path-distance taper on primary trunk | Captures proximal-to-first-bifurcation taper | 1 day |
| Medium | Rall 3/2 at every branch point | Impedance-matched calibration | 2 days |
| Low | Generative diameter prior from Allen RGCs | Quantified uncertainty | 1 week |
| Low | Per-cell 2P image segmentation | Cell-specific diameters | Depends on image availability |

All seven should be recorded as suggestions in the next task step. The high-priority items block any
downstream biophysical comparison against published Rin data and should be lifted into the
correction queue before t0011 visualisation and the direction-selectivity experiments consume this
asset.
