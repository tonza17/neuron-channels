# Null-GABA Reduction Ladder on t0022 DSGC

## Motivation

t0036 reduced `GABA_CONDUCTANCE_NULL_NS` from 12 nS to 6 nS (Schachter2010-matched) on the t0022
distal-diameter sweep and found **null firing still pinned at 0.0 Hz** across every diameter — the
rescue hypothesis S-0030-01 was falsified at 6 nS. t0036's creative-thinking enumerated 5
explanations (notably: 12 nS was far above threshold, so 6 nS is still too high), and suggestion
S-0036-01 proposed further reductions in sequence: **4 nS → 2 nS → 1 nS**.

This task runs that ladder efficiently as a focused **1D sweep at baseline diameter only** (instead
of 3× full diameter sweeps). The question: at what GABA level (if any) does null- direction firing
become non-zero on the t0022 deterministic schedule? The answer bounds whether a future full
diameter sweep at the unpinning level is worth the compute.

If **all** tested GABA levels still yield 0 Hz null firing (including 0 nS — full GABA block), the
null result falsifies any conductance-only rescue on t0022 and rules out future work along that axis
— forcing the optimiser to either use t0024 or adopt vector-sum DSI on t0022 (already queued as
S-0030-06).

## Scope

1. Use the **t0022 DSGC testbed** as-is. Distal diameter locked at **1.0× baseline** (no diameter
   variation).
2. Sweep `GABA_CONDUCTANCE_NULL_NS` across **5 levels**: **{4.0, 2.0, 1.0, 0.5, 0.0}** nS. Brackets
   S-0036-01's specified 4/2/1 with a finer end (0.5) and full GABA block (0.0) as a sanity extreme.
3. At each GABA level, run the standard **12-direction × 10-trial protocol = 120 trials**. Total =
   **5 × 120 = 600 trials**.
4. Measure **null-direction firing rate (critical diagnostic)** + primary DSI + vector-sum DSI +
   peak Hz + HWHM per GABA level.
5. Report: the lowest GABA level at which null firing becomes non-zero (if any); recommend a
   follow-up full diameter sweep at that level OR definitively falsify the conductance-only rescue.

## Approach

* **Local CPU only.** No remote compute, $0.
* Copy the t0036 `gaba_override` monkey-patch pattern into a CLI-switchable version that accepts a
  numeric GABA value per run.
* Run the 12-direction × 10-trial protocol five times, one per GABA level, accumulating into a tidy
  CSV keyed by `(gaba_null_ns, direction_deg, trial)`.
* Analyse: per-GABA null_hz, peak_hz, DSI primary, DSI vector-sum, HWHM.
* Chart: `null_hz_vs_gaba.png` (critical diagnostic), `primary_dsi_vs_gaba.png`,
  `vector_sum_dsi_vs_gaba.png`, `peak_hz_vs_gaba.png`, polar overlay of all 5 levels.

## Expected Outputs

* `results/results_summary.md` — headline: lowest GABA level with non-zero null firing (or
  definitive falsification).
* `results/results_detailed.md` — per-GABA metrics, per-direction breakdown at each level,
  recommendation for follow-up.
* `results/images/null_hz_vs_gaba.png` (THE key chart), plus primary-DSI, vector-sum-DSI, peak-Hz,
  polar-overlay.
* `results/metrics.json` — per-GABA-level registered DSI metrics.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: **~20-30 minutes** (600 trials × ~2 s/trial on t0022
  deterministic).
* $0 external cost.

## Measurement

* **Primary diagnostic**: **null-direction firing rate per GABA level**. Non-zero at any level → the
  rescue works at that level.
* **Secondary**: primary DSI (expected to drop below 1.000 once null firing unpins), vector-sum DSI,
  peak Hz, HWHM, per-direction spike counts.

## Key Questions

1. At what (if any) GABA level does null-direction firing become non-zero?
2. If null firing unpins at some level, what is the primary DSI at that level?
3. If NO level unpins null firing — including 0 nS full GABA block — what does that imply about the
   t0022 schedule? Does the AMPA EPSP simply never reach AP threshold at null angles, independent of
   GABA?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the testbed architecture.
* **t0036_rerun_t0030_halved_null_gaba** (completed) — provides the `gaba_override` monkey-patch
  pattern, the baseline-GABA=6 nS null result, and the 177-section distal- selection rule. Also
  provides code/constants inheritance.

## Scientific Context

Source suggestion **S-0036-01** (high priority). The 4/2/1 nS sequence was the explicit
recommendation; extended here to 0.5 and 0 nS to bracket the extreme case. Result interacts directly
with:
- **S-0030-02** (Poisson noise rescue): if GABA ladder fails, Poisson is the next attempt
- **S-0030-06** (vector-sum DSI objective): if GABA ladder fails, this becomes the recommended t0033
  objective on t0022

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 + t0030 + t0036 cover mechanism priors).
* Include `research-code` — need to copy t0036's `gaba_override` and generalise it.
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `creative-thinking` — if rescue fails even at 0 nS, the finding is mechanism- defining for
  t0022.
* Include `compare-literature` — compare unpinning threshold to Schachter2010 / Park2014
  null-inhibition ranges.
