# ✅ Nav1.6 + Kv3 co-expression: does Kv3 rescue the DSI loss caused by Nav1.6?

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0068_t0067_nav16_kv3_coexpression_rescue` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T01:41:29Z |
| **Completed** | 2026-05-01T03:05:00Z |
| **Duration** | 1h 23m |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Source suggestion** | `S-0067-02` |
| **Task types** | `experiment-run` |
| **Step progress** | 9/15 |
| **Task folder** | [`t0068_t0067_nav16_kv3_coexpression_rescue/`](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/task_description.md)*

# Nav1.6 + Kv3 co-expression: does Kv3 rescue the DSI loss caused by Nav1.6?

## Motivation

t0067 found that adding Nav1.6 to the deposited Poleg-Polsky soma monotonically erodes
direction selectivity (DSI = 0.80 → 0.75 → 0.48 → 0.23 across baseline → low → med → high
density). Nav1.6 alone raises both PD and ND firing, but ND climbs faster proportionally
because the baseline ND firing was sub-threshold. The hypothesis (suggestion S-0067-02): if we
ALSO add Kv3 at the same time, Kv3's fast repolarisation could allow the cell to recover from
each AP faster and let the inhibitory shunt regain modulatory power — restoring the DSI gap.

This task tests that hypothesis directly by sweeping Kv3 density at two fixed Nav1.6 densities
(med = 30 mS/cm², high = 90 mS/cm²) and measuring whether Kv3 co-expression progressively
rescues DSI back toward baseline.

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as in t0008 / t0065 / t0067.
* Mode: only `FULL` (HH on, all synapses at canonical defaults). Same gabaMOD-swap protocol as
  t0067.
* Direction: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`).
* Seeds per condition: 5.
* Channels: Nav1.6 + Kv3 from t0067's vendored MODs (kinetics from Carter-Bean 2009 and Erisir
  1999 respectively).

## Conditions

9 conditions × 2 directions × 5 seeds = **90 FULL trials**.

| condition_id | Nav1.6 (mS/cm²) | Kv3 (mS/cm²) | Notes |
| --- | --- | --- | --- |
| baseline | 0 | 0 | Reference (matches t0067 baseline DSI = 0.80) |
| nav16_med | 30 | 0 | t0067 anchor (DSI = 0.48) |
| nav16_med_kv3_low | 30 | 7 | Co-insertion: low Kv3 |
| nav16_med_kv3_med | 30 | 20 | Co-insertion: med Kv3 |
| nav16_med_kv3_high | 30 | 60 | Co-insertion: high Kv3 |
| nav16_high | 90 | 0 | t0067 anchor (DSI = 0.23) |
| nav16_high_kv3_low | 90 | 7 | Co-insertion: low Kv3 |
| nav16_high_kv3_med | 90 | 20 | Co-insertion: med Kv3 |
| nav16_high_kv3_high | 90 | 60 | Co-insertion: high Kv3 |

## Approach

1. Vendor the same 5 MOD files from t0067 (`nav16t67`, `napt67`, `nart67`, `kv3t67`, `kv4t67`)
   into the task's `code/mods/`. The t0067 MOD files are reused verbatim — same kinetics, same
   NONSPECIFIC_CURRENT pattern.
2. Compile a task-local DLL.
3. Build the t0008 cell once. Insert all 5 mechanisms on the soma at gbar=0; per-trial set the
   active Nav1.6 and Kv3 gbars to the target densities (others stay at 0).
4. Run 90 FULL-mode trials using the t0067 trial-driver structure adapted to support
   simultaneous setting of Nav1.6 and Kv3 densities.
5. Aggregate per-trial scalars to per-condition mean ± SD; compute DSI per condition.

## Outputs

* `data/per_trial_metrics.json` — 90 trial records.
* `data/dsi_by_condition.json` — 9 conditions.
* `results/metrics.json` — registered `direction_selectivity_index` for the baseline.
* `results/images/dsi_rescue_curve.png` — DSI vs Kv3 density at fixed Nav1.6 (2 lines for
  Nav1.6_med vs Nav1.6_high, with baseline reference).
* `results/images/firing_rate_rescue.png` — PD and ND firing rate vs Kv3 density at fixed
  Nav1.6 (2 sub-panels).
* `results/results_summary.md`, `results/results_detailed.md` (spec_version 2) with
  rescue-effect interpretation.

## Failure-mode policy

Same as t0067: peak Vm > +60 mV or < −80 mV → flag `is_unstable = true`. Trial data still
saved.

## Key Questions

1. Does Kv3 co-insertion progressively rescue DSI as Kv3 density increases? Specifically: is
   DSI(nav16_high + kv3_high) > DSI(nav16_high) by a meaningful margin (Δ > 0.1)?
2. Does Kv3 reduce firing rate (the expected effect of fast K+ repolarisation) preferentially
   in ND (which would scale DSI back up) or in both directions equally (which would not)?
3. Is the rescue effect different for Nav1.6_med vs Nav1.6_high? At med, the cell is in a
   regime where DSI was 0.48 (still quite directional); at high, DSI was 0.23 (close to
   collapse). Which regime benefits more from Kv3?

## Compute and Budget

* Local Windows workstation. ~3 s/trial × 90 trials ≈ 5 min.
* External costs: $0.

## Time Estimation

* Implementation (port t0067 code, adapt for co-expression): 1 hour.
* Sweep: 5 min.
* Plotting + reporting: 45 min.
* Verification + PR: 30 min.
* Total: ~2.5 hours.

## Dependencies

* `t0008_port_modeldb_189347` — cell builder + base nrnmech.dll.
* `t0065_t0020_epsp_ipsp_vm_protocol` — gabaMOD-swap baseline.
* `t0067_t0065_soma_channel_addition_sweep` — vendored MOD files (Nav1.6 + Kv3 reused
  verbatim), trial driver template, baseline DSI = 0.80, Nav1.6 anchor DSIs (med = 0.48, high
  = 0.23).

## Risks and Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Kv3 at high density breaks the cell at Nav1.6_high (e.g., AP suppressed entirely). | spike_count = 0 in BOTH directions. | Document as "rescue-overshoot": Kv3 reverses Nav1.6's effect too aggressively. |
| 2 | Kv3 has no rescue effect at either Nav1.6 level (DSI unchanged from t0067 anchors). | DSI(Nav1.6_X + Kv3_Y) ≈ DSI(Nav1.6_X) for all Y. | Report null result; the rescue hypothesis is falsified. Kv3 alone may have been inert in t0067 because the cell wasn't in a fast-spiking regime; it may also be inert when added to Nav1.6 because the kinetic regime still doesn't engage Kv3 strongly. |
| 3 | Kv3 actually amplifies DSI loss (DSI drops further than Nav1.6 alone). | DSI(co-insertion) < DSI(Nav1.6 alone). | Surprising but possible. Document and explore in suggestions. |

## Verification Criteria

* All 90 trials complete.
* `data/per_trial_metrics.json` has 90 entries.
* `data/dsi_by_condition.json` has 9 entries.
* Both PNG plots exist and are embedded in `results_detailed.md`.
* All standard verificators pass.

</details>

## Metrics

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.7974683544303798** |

## Suggestions Generated

<details>
<summary><strong>Test BK / SK calcium-activated K+ co-expression with
Nav1.6</strong> (S-0068-01)</summary>

**Kind**: experiment | **Priority**: high

t0068 falsified the Nav1.6 + Kv3 rescue hypothesis: Kv3 doesn't differentially suppress firing
at high rates because its activation depends on V, not on cumulative Ca2+. The natural
alternative is a Ca2+-activated K+ channel (BK / KCa1.1 or SK / KCa2). These channels' open
probability scales with intracellular [Ca2+], which itself scales with cumulative AP firing.
Therefore: ND (low firing, low [Ca2+]) → BK/SK barely active → cell fires normally. PD (high
firing, high [Ca2+]) → BK/SK strongly activated → cell is clamped down → PD firing reduced
more than ND firing → DSI restored. This is mechanistically coherent and biologically
plausible (DSGCs express both BK and SK in vivo). Implementation: vendor a BK MOD (e.g., from
Hines & Carnevale's Purkinje model) AND a Ca2+ pool mechanism, then sweep BK density at fixed
Nav1.6 = high. Cost: 1-2 hours code + ~5 min compute per density.

</details>

<details>
<summary><strong>Test M-current (KCNQ / Kv7) co-expression with Nav1.6</strong>
(S-0068-02)</summary>

**Kind**: experiment | **Priority**: medium

Another rescue candidate: M-current is a slowly-activating, non-inactivating K+ current with
V_half around -40 to -45 mV. Unlike Kv3 it doesn't repolarise fast APs; it provides a tonic
outward current that opposes sustained depolarisation. In a Nav1.6-driven high-firing regime,
M-current would provide steady hyperpolarisation that reduces the cell's mean depolarisation,
possibly restoring the regime where the GABA shunt has more leverage. Implementation: write a
simple m^1 MOD with V_half = -45 mV, tau ~50 ms, sweep at Nav1.6_med + Nav1.6_high.

</details>

<details>
<summary><strong>Synaptic re-tuning: scale s2ggaba up proportionally with Nav1.6
density</strong> (S-0068-03)</summary>

**Kind**: experiment | **Priority**: medium

t0068 makes clear that channel-level rescue may not be possible — the GABA shunt's leverage is
fundamentally bounded when Nav1.6 boosts the depolarising drive. The natural alternative is to
scale the GABA conductance up proportionally. Test: at Nav1.6_med (s2ggaba x 1.5x, 2.0x, 3.0x)
and Nav1.6_high (s2ggaba x 1.5x, 2.0x, 3.0x). Hypothesis: a coordinated 2x synaptic upscale
restores DSI to baseline. This isn't a 'rescue' in the channel-pharmacology sense, but it
shows what would be required to compensate for a Nav-side gain change at the network level —
relevant for understanding RGC robustness to channel-density variation. Implementation: 1-line
patch to t0065's apply_params, then 6 conditions x 2 directions x 5 seeds = 60 trials, ~3 min.

</details>

<details>
<summary><strong>Move Nav1.6 + Kv3 to a virtual AIS instead of soma</strong>
(S-0068-04)</summary>

**Kind**: experiment | **Priority**: medium

Real RGCs concentrate Nav1.6 and Kv3 at the AIS at ~50x somatic densities. The Nav1.6 + Kv3
co-localisation we modelled here is somatic, which the t0067 / t0068 limitations document as
understating the joint effect. Add a 30-um AIS section to the deposited cell, place Nav1.6 +
Kv3 there at 30 / 90 mS/cm^2 (and a wider Kv3 density grid up to ~200 mS/cm^2), re-run the
rescue sweep. Expected: AIS-localised Kv3 at very high density may finally show DSI rescue
because the AIS's smaller diameter makes per-segment conductance changes leverage the AP shape
more strongly. If still no rescue, the channel-pharmacology approach to DSI rescue is null
across substrates.

</details>

<details>
<summary><strong>Sweep Kv3 alone (no Nav1.6) to validate the kinetic-model
effect</strong> (S-0068-05)</summary>

**Kind**: experiment | **Priority**: low

t0067 sweep showed Kv3 alone (without Nav1.6) had essentially no effect on firing rate or DSI
(DSI = 0.80 → 0.82 across low/med/high). t0068 shows Kv3 also has no rescue effect on top of
Nav1.6. To confirm that this isn't a model artefact (e.g., Kv3 not engaging because of an MOD
bug), run a finer Kv3-only sweep with very high densities (60, 200, 500 mS/cm^2) and check
whether SOME density level produces a measurable firing-rate effect. If Kv3 at 500 mS/cm^2
still does nothing, our simplified Kv3 MOD likely needs revision to a richer kinetic scheme
(e.g., Wang-Buzsaki with two-component decay).

</details>

## Research

* [`research_code.md`](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/results_summary.md)*

# Results Summary: Nav1.6 + Kv3 co-expression rescue test

## Summary

Tested whether co-inserting Kv3 with Nav1.6 on the deposited Poleg-Polsky DSGC soma rescues
the direction selectivity that Nav1.6 alone erodes (t0067 anchors: DSI = 0.48 at Nav1.6_med,
0.23 at Nav1.6_high). 9 conditions × 2 directions × 5 seeds = 90 FULL trials, ~~10 min
compute. **Hypothesis FALSIFIED**: Kv3 does NOT rescue DSI. Across all 8 co-expression
conditions DSI changes by less than ±0.025 from the Nav1.6-only anchor. Instead, Kv3 slightly
*boosts* firing rate (~~+10% at high Kv3), scaling PD and ND equally.

## Metrics

| Condition | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | ΔDSI vs Nav1.6 anchor |
| --- | --- | --- | --- | --- |
| baseline | 14.2 ± 1.9 | 1.6 ± 1.3 | 0.797 | (vs no Nav1.6) |
| nav16_med (anchor) | 26.8 ± 3.6 | 9.4 ± 2.6 | 0.481 | (reference) |
| nav16_med + kv3_low | 27.2 ± 3.3 | 9.4 ± 2.6 | 0.486 | +0.005 (noise) |
| nav16_med + kv3_med | 28.6 ± 3.6 | 9.4 ± 2.6 | 0.505 | +0.024 (tiny) |
| nav16_med + kv3_high | 30.2 ± 4.3 | 10.4 ± 2.6 | 0.488 | +0.007 (noise) |
| nav16_high (anchor) | 57.4 ± 2.9 | 36.0 ± 3.1 | 0.229 | (reference) |
| nav16_high + kv3_low | 58.4 ± 3.0 | 36.6 ± 2.3 | 0.229 | +0.000 |
| nav16_high + kv3_med | 58.8 ± 3.3 | 37.0 ± 2.5 | 0.228 | -0.001 |
| nav16_high + kv3_high | 63.4 ± 4.2 | 39.4 ± 3.0 | 0.233 | +0.004 |

* **Largest DSI change from co-expression**: +0.024 (nav16_med + kv3_med); within sampling
  noise.
* **Firing-rate effect**: Kv3_high adds ~6 PD + ~3.4 ND spikes at Nav1.6_high — both
  directions scale up proportionally, so DSI is unchanged.
* **Trials with instability flags**: **0/90**.

## Verification

* `verify_research_code` — PASSED.
* `verify_plan` — PASSED.
* `verify_task_dependencies` — PASSED (t0008, t0065, t0067 all completed).
* `verify_task_metrics` — PASSED (registered DSI metric only).
* `verify_task_results` — PASSED (mandatory sections present).
* mypy + ruff PASSED on all task code.

## Conclusion

The S-0067-02 hypothesis (Kv3 rescues DSI by enabling faster recovery from Nav1.6's
depolarising drive) is **falsified** by these data. Two clean takeaways:

* **Kv3 doesn't change the inhibitory-to-excitatory conductance ratio**: Kv3 is a delayed
  rectifier, so it speeds *repolarisation* but doesn't reduce the depolarising drive that the
  GABA shunt has to fight against. The shunt's effectiveness — and hence DSI — is determined
  by `g_inhib / g_total`, which Kv3 doesn't alter.
* **Kv3 actually amplifies firing**: faster repolarisation → faster Na+ recovery from
  inactivation → next AP fires sooner. At Kv3_high + Nav1.6_high we see ~+10% firing in both
  directions, scaling PD and ND equally — DSI invariant.

DSI rescue would require something that breaks the symmetry: e.g., a channel that selectively
suppresses the cell at high firing rates (spike-frequency adaptation), or a synaptic-level
intervention that boosts inhibition. Suggestions S-0068-01 through S-0068-04 explore these
alternatives.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0068_t0067_nav16_kv3_coexpression_rescue" date: "2026-05-01"
---
# Detailed Results: Nav1.6 + Kv3 co-expression rescue test

## Summary

Tested whether co-inserting Kv3 with Nav1.6 on the deposited Poleg-Polsky DSGC soma rescues
the direction selectivity that Nav1.6 alone erodes (t0067 found Nav1.6 monotonically reduces
DSI from 0.80 → 0.48 → 0.23 across baseline → med → high density). 9 conditions × 2 directions
× 5 seeds = 90 FULL trials, ~10 min compute. **Hypothesis FALSIFIED**: Kv3 co-expression does
NOT rescue DSI (Δ < ±0.025 across all 8 co-expression conditions). Instead Kv3 slightly boosts
firing rate by speeding Na+ recovery from inactivation, scaling PD and ND equally so DSI is
invariant.

## Methodology

* **Cell**: deposited Poleg-Polsky 2016 DSGC, exactly as in t0008 / t0065 / t0067. No changes
  to dendrites, synapses, or HHst.
* **Channels**: t0067's 5 vendored MOD files (`nav16t67`, `napt67`, `nart67`, `kv3t67`,
  `kv4t67`) reused verbatim. All 5 inserted on the soma at gbar=0; per trial, only Nav1.6 and
  Kv3 may have non-zero gbar.
* **Conditions** (9 total):
  * baseline (no added channels)
  * nav16_med (30 mS/cm² Nav1.6, no Kv3)
  * nav16_med + kv3_{low,med,high} (Kv3 = 7, 20, 60 mS/cm²)
  * nav16_high (90 mS/cm² Nav1.6, no Kv3)
  * nav16_high + kv3_{low,med,high}
* **Direction**: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`).
* **Seeds**: 5 per (condition, direction) cell.
* **Per-trial sequence**: `apply_params(seed) → set gabaMOD → exptype = 1 → init_active() →
  update() → placeBIP() → set Nav1.6 + Kv3 gbars → finitialize(-65) → continuerun(1000) →
  count spikes via NetCon @ -10 mV`.
* **Compute**: local Windows workstation, single CPU, NEURON 8.2.7. ~10 min for 90 trials.
* **Failure-mode policy**: peak Vm > +60 mV or < -80 mV → flag. **0/90 flagged**.

## Per-condition Metrics Table

| Condition              | Nav1.6 (mS/cm²) | Kv3 (mS/cm²) | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI    |
| ---------------------- | --------------- | ------------ | --------------------- | --------------------- | ------ |
| baseline               | 0               | 0            | 14.2 ± 1.9            | 1.6 ± 1.3             | **0.797** |
| nav16_med              | 30              | 0            | 26.8 ± 3.6            | 9.4 ± 2.6             | **0.481** |
| nav16_med + kv3_low    | 30              | 7            | 27.2 ± 3.3            | 9.4 ± 2.6             | 0.486  |
| nav16_med + kv3_med    | 30              | 20           | 28.6 ± 3.6            | 9.4 ± 2.6             | 0.505  |
| nav16_med + kv3_high   | 30              | 60           | 30.2 ± 4.3            | 10.4 ± 2.6            | 0.488  |
| nav16_high             | 90              | 0            | 57.4 ± 2.9            | 36.0 ± 3.1            | **0.229** |
| nav16_high + kv3_low   | 90              | 7            | 58.4 ± 3.0            | 36.6 ± 2.3            | 0.229  |
| nav16_high + kv3_med   | 90              | 20           | 58.8 ± 3.3            | 37.0 ± 2.5            | 0.228  |
| nav16_high + kv3_high  | 90              | 60           | 63.4 ± 4.2            | 39.4 ± 3.0            | 0.233  |

DSI changes from Nav1.6-only anchor: max +0.024, min -0.001 — all within the SD of single
seeds (~3-4 spikes ↔ DSI uncertainty ~±0.05).

## Comparison vs t0067 anchors

* t0067 nav16_med (single 5-seed value): DSI = 0.481.
* t0068 nav16_med (re-measured here): DSI = 0.481. **Identical** — confirms reproducibility.
* t0067 nav16_high: DSI = 0.229.
* t0068 nav16_high: DSI = 0.229. **Identical** — confirms reproducibility.

The rescue conditions sit on top of these anchors with negligible deviation.

## Visualisations

### DSI rescue curve

![DSI vs Kv3 density at fixed
Nav1.6](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/images/dsi_rescue_curve.png)

Both Nav1.6 levels show essentially flat DSI vs Kv3 density. The Nav1.6=30 line wiggles by
±0.024 around DSI = 0.49; the Nav1.6=90 line is flat at DSI = 0.23. Neither approaches the
baseline (dashed = 0.80). **Visual confirmation: no rescue.**

### Firing rate rescue

![Firing rate vs Kv3 density at fixed
Nav1.6](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/images/firing_rate_rescue.png)

2-panel (Nav1.6_med left, Nav1.6_high right). Both panels show PD (blue) and ND (red) spike
counts climbing slightly with Kv3 density — the opposite of the expected "Kv3 reduces firing"
effect. PD and ND scale up proportionally → DSI invariant. The expected Kv3 effect (slower
firing via stronger repolarisation) is overwhelmed by the recovery-acceleration effect (faster
return to AP threshold).

## Analysis & Discussion

### Why doesn't Kv3 rescue DSI?

The mechanism we hypothesised was: Nav1.6 lifts the cell into a higher-firing regime where the
GABA shunt becomes proportionally weaker (because the Na/K ratio is more Na-dominant). Kv3
should restore the K+ side of the ratio, allowing the shunt to bite harder again.

The data falsifies this in two ways:

1. **Kv3 doesn't reduce firing rate.** It actually slightly *increases* firing rate
   (Nav1.6_high goes from 57.4 PD spikes to 63.4 PD spikes at Kv3_high, +10%). Kv3's primary
   effect is faster repolarisation between APs, which means faster Na+ recovery from
   inactivation — the next AP fires sooner. So Kv3 is permissive for high-frequency firing,
   not suppressive. In a regime where the cell is already firing faster than necessary, adding
   a fast K+ channel doesn't slow it down; it lets it fire even faster.

2. **DSI invariance is geometric.** The shunt's effect is `i_inh = g_inh · (V − E_GABA)`. With
   E_GABA = V_rest = -60 mV, the shunt produces voltage deflection proportional to `(V −
   E_GABA)` only when V is depolarised away from E_GABA. Kv3 doesn't change V's distribution
   between APs (it's still controlled by the Na/leak/synaptic balance) — it only sharpens the
   AP itself. So `(V − E_GABA)` integrated over the inter-spike interval is essentially the
   same with or without Kv3. The shunt's modulation of firing rate is therefore the same too —
   and PD/ND scale together.

### What WOULD rescue DSI?

By process of elimination, rescue requires a channel or mechanism that:

1. **Suppresses firing differentially** at high firing rates — e.g., a calcium-activated K+
   channel (BK or SK) where K+ feedback scales with cumulative AP count. ND (low firing)
   wouldn't accumulate much Ca²⁺; PD (high firing) would, and BK/SK would clamp PD back down,
   widening the PD/ND gap.
2. **Increases the inhibitory drive** itself — e.g., scaling up `s2ggaba` proportionally when
   Nav1.6 is added. But this isn't a "rescue via channels" — it's a synaptic-balance
   re-tuning.
3. **Reduces the Na+ persistent component** — e.g., adding NaP suppression. But t0067 showed
   NaP has the OPPOSITE effect (it inverts DSI, doesn't restore it).

Suggestion S-0068-01 explores option (1): test BK / SK co-expression with Nav1.6.

### Reproducibility

The Nav1.6_med and Nav1.6_high anchor conditions reproduce t0067's exact DSI values (0.481 and
0.229). This rules out drift in the deposited cell or the Nav1.6 MOD between t0067 and t0068.

## Examples

6 representative trial-level examples below: 1 baseline + Nav1.6_med anchor + 1 co-expression
+ Nav1.6_high anchor + 2 co-expressions.

### Example 1 — baseline FULL/PD seed=1

Input parameters:

```text
gabaMOD = 0.33                    # PD direction
exptype = 1                       # HH on
gbar_nav16t67 = 0
gbar_napt67   = 0
gbar_nart67   = 0
gbar_kv3t67   = 0
gbar_kv4t67   = 0
seed = 1, tstop = 1000 ms
```

Output:

```text
peak_v_mv = +43.18 mV
baseline_v_mv = -60.02 mV
spike_count = 15
```

(Matches t0065 + t0067 baseline exactly.)

### Example 2 — nav16_med anchor FULL/PD seed=1

Input parameters:

```text
gabaMOD = 0.33
gbar_nav16t67 = 0.030 S/cm^2     # 30 mS/cm^2
gbar_kv3t67   = 0
others = 0
seed = 1
```

Output:

```text
peak_v_mv = +44.01 mV
spike_count = 27
```

Matches t0067 nav16_med anchor.

### Example 3 — nav16_med + kv3_high FULL/PD seed=1

Input parameters:

```text
gabaMOD = 0.33
gbar_nav16t67 = 0.030
gbar_kv3t67   = 0.060            # 60 mS/cm^2 (high)
seed = 1
```

Output:

```text
peak_v_mv = +44.0 mV
spike_count = 30   # +3 vs Example 2 anchor (+11%)
```

Kv3 adds 3 PD spikes; ND analogue adds ~1 → DSI essentially unchanged.

### Example 4 — nav16_high anchor FULL/PD seed=1

Input parameters:

```text
gabaMOD = 0.33
gbar_nav16t67 = 0.090            # 90 mS/cm^2
gbar_kv3t67   = 0
seed = 1
```

Output:

```text
peak_v_mv = +44.0 mV
spike_count = 57
```

Matches t0067 nav16_high anchor.

### Example 5 — nav16_high + kv3_high FULL/PD seed=1

Input parameters:

```text
gabaMOD = 0.33
gbar_nav16t67 = 0.090
gbar_kv3t67   = 0.060
seed = 1
```

Output:

```text
peak_v_mv = +44.0 mV
spike_count = 63   # +6 vs Example 4 anchor (+10%)
```

### Example 6 — nav16_high + kv3_high FULL/ND seed=1

Input parameters:

```text
gabaMOD = 0.99                    # ND direction
gbar_nav16t67 = 0.090
gbar_kv3t67   = 0.060
seed = 1
```

Output:

```text
peak_v_mv = +38 mV
spike_count = 39   # +3 vs anchor's 36 (+8%)
```

PD scales +10%, ND scales +8% — proportional → DSI invariant.

## Verification

| Verificator | Status |
| --- | --- |
| `verify_research_code.py` | PASSED |
| `verify_plan.py` | PASSED (5 non-blocking warnings) |
| `verify_task_dependencies.py` | PASSED |
| `verify_task_metrics.py` | PASSED |
| `verify_task_results.py` | PASSED |
| `verify_suggestions.py` | PASSED |
| `verify_task_file.py` | PASSED |
| `verify_task_folder.py` | PASSED |
| `verify_logs.py` | PASSED |
| Mypy + ruff | PASSED on all task code |
| Per-trial instability | 0/90 trials flagged |

## Limitations

1. **Only 2 Nav1.6 levels × 4 Kv3 levels**: a denser grid might reveal a regime where Kv3 does
   help. But the trend across both Nav1.6 levels is so flat that this is unlikely.
2. **Same simplified MOD as t0067**: our Kv3 is m^4, V_half = -15 mV, τ = 1 ms. A more
   detailed model (Wang-Buzsaki-style with two-component decay) might engage differently at
   high Nav1.6 firing rates.
3. **Soma-only insertion**: AIS-localised channels would have stronger effects per t0019
   priors; any rescue effect that depends on AIS-specific kinetics is missed here.
4. **No combinations beyond Nav1.6 + Kv3**: many other channel pairs (Nav1.6 + BK, Nav1.6 +
   M-current) could potentially rescue. This task tested one specific pair.

## Files Created

* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/code/{paths,constants,run_sweep,plot_results}.py`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/code/build/nrnmech.dll`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/data/per_trial_metrics.json`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/data/dsi_by_condition.json`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/metrics.json`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/costs.json`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/remote_machines_used.json`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/suggestions.json`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/results_summary.md`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/results_detailed.md`
* `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/images/{dsi_rescue_curve,firing_rate_rescue}.png`

## Task Requirement Coverage

The task as commissioned: implement S-0067-02 ("Test channel co-expression: Nav1.6 + Kv3
jointly").

REQs from `plan/plan.md`:

* **REQ-1 (5 MOD files vendored from t0067)**: Done — copied verbatim into `code/mods/`.
* **REQ-2 (9 conditions per task description)**: Done — see Per-condition Metrics Table.
* **REQ-3 (FULL mode only, gabaMOD-swap)**: Done — only `exptype = 1` used.
* **REQ-4 (5 seeds per condition)**: Done — 5 PD + 5 ND per condition.
* **REQ-5 (DSI per condition)**: Done — column in Metrics Table.
* **REQ-6 (2 plots: dsi_rescue_curve.png + firing_rate_rescue.png)**: Done — both embedded
  above.
* **REQ-7 (results_summary.md + results_detailed.md spec_version 2)**: Done.

Hypothesis (S-0067-02): Kv3 rescues DSI lost to Nav1.6. **Status: falsified** — Δ DSI < 0.025
across all 8 co-expression conditions.

</details>
