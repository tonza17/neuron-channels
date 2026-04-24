# Brainstorm Session 8 — Full Transcript

Date: 2026-04-24. Duration: ~90 min.

## Project State Presented

### Budget and task counts

* Budget: $0.00 spent / $1.00 total.
* Tasks: 39 total. 37 completed, 1 `not_started` (t0031), 1 `intervention_blocked` (t0023).
* Work since brainstorm 7 (t0032): 7 new completed tasks (t0033–t0039), all zero-cost.
* Uncovered suggestions: 151 total; 50 high-priority after this session's reassessment.

### Research questions (from `project/description.md`)

1. Which Nav / Kv combinations at the soma maximise preferred-direction AP firing while suppressing
   null firing?
2. How sensitive is directional AP tuning to morphology (branching, segment length, diameter)?
3. How do AMPA:GABA density ratios and their spatial distribution shape tuning sharpness?
4. Do active dendritic VGCs improve, degrade, or not affect the match to the target curve vs passive
   dendrites?
5. How closely can the optimised single-cell model reproduce the target curve, and what residual
   error remains?

### Recent results (t0033–t0039) — key numbers

* **t0033** — Vast.ai plan: $50.54 central (range $23–$119), ~74 h on RTX 4090 with
  surrogate-NN-assisted GA. 25 free params. Key assumption: 5x CoreNEURON GPU speedup (unvalidated).
* **t0034** — Distal-length sweep on t0024 (840 trials). Primary DSI 0.545–0.774, slope -0.1259
  (p=0.038). Vector-sum DSI clean monotonic decline (R^2=0.91, p<0.001). Falsifies Dan 2018
  monotonic-increase; signature matches Tukker 2004 cable-filtering.
* **t0035** — Distal-diameter sweep on t0024 (840 trials). DSI 0.680–0.808 but slope +0.0041
  (p=0.88). Neither Schachter 2010 nor passive-filtering supported. Length / diameter asymmetry
  explained by cable theory (L/lambda linear; 1/sqrt(d)).
* **t0036** — Halving t0022 GABA to 6 nS. Null firing still pinned at 0 Hz, DSI 1.000. Rescue
  hypothesis falsified at 6 nS.
* **t0037** — Null-GABA ladder on t0022: {4, 2, 1, 0.5, 0} nS. Sweet spot 4 nS: DSI=0.429,
  preferred 40.8 deg, peak 15 Hz, null 6 Hz (matches Park 2014 in vivo 0.40–0.60). Below 2 nS:
  preferred direction randomises.
* **t0038** — Correction propagated: t0022 base GABA = 4.0 nS (not 12). One correction file, no
  sims.
* **t0039** — 7-diameter sweep on t0022 @ GABA=4 nS. DSI 0.429 -> 0.368 across 0.5x–2.0x, slope
  -0.0336 (p=0.008). Classified passive_filtering, not Schachter 2010 active amplification.
  Preferred direction stable 37–41 deg (E-I encodes axis; morphology sets gain).

### Strategic implications distilled

1. Length is ~2.8x the DSI lever that diameter is. Cable-theory asymmetry confirmed on both t0022
   and t0024. S-0035-01 (zero-cost L/lambda collapse analysis) would lock this in.
2. t0022 deterministic schedule is not salvageable for primary-DSI mechanism discrimination — only
   AR(2) stochastic t0024 gives measurable primary DSI. Implies t0033 should use t0024 as substrate
   (S-0034-07), not t0022. S-0030-06 (switch objective to vector-sum DSI) is now superseded and
   should be dropped.
3. Schachter 2010 active-amplification signature not detected on any diameter sweep (t0030, t0035,
   t0039). Mechanism appears to be cable filtering, not dendritic-spike gain.
4. Preferred-direction pinning is E-I, not morphology: the t0033 optimiser cannot tune the DS axis
   under the current E-I schedule — only magnitude.
5. AR(2) rho=0.6 is load-bearing for unpinning null firing on any Poleg-Polsky-derived testbed.
6. Paywalled Kim 2014 and Sivyer 2013 still block full compare_literature on cable-filtering
   interpretation.
7. t0023 (Hanson 2019 port, DEFERRED) can now proceed — t0022 is done — but should use t0024
   substrate per (2) above.

## Clarification Questions

AI: "Before I propose new tasks and suggestion cleanups, I need your direction: 1. Notes/context? 2.
Focus area? 3. Budget/compute? 4. Batch size? 5. Anything in the recent results that changed your
thinking?"

Researcher: "Now that you have generated a bunch of tests I would like you to summarise in a big
table and also compare this to published data. Looks like we have quite a lot of difference with
published data. We need to assess this and find ways to correct for this in our models."

AI: "Good direction. Let me pull together the cross-task synthesis table + literature discrepancies.
This needs reading 13 compare_literature.md files and the corresponding results_summary.md files —
delegating to an agent to keep context clean."

## Project State Presented — Cross-Task Audit

### Master test table

See `results/test_vs_literature_table.md` section 1 for the full 13-row master table. Summary: every
one of our 13 simulation tests across t0008, t0020, t0022, t0024, t0026 (x2), t0029, t0030, t0034,
t0035, t0036, t0037, t0039 is enumerated with primary DSI, vector-sum DSI, preferred direction, peak
Hz, null Hz, and key finding.

### Published-data comparison

See `results/test_vs_literature_table.md` section 2 for the full 35-row comparison table. The most
severe recurring mismatches:

* Peak firing rate 10x too low across every port (5–18 Hz vs 40–150 Hz published).
* DSI saturates to 1.000 on t0022 deterministic schedule with GABA >= 6 nS (t0029, t0030, t0036).
* t0024 correlation-drop signature missing (ours 0.000 vs paper 0.36).
* Schachter 2010 active amplification missing on every diameter sweep (t0030, t0035, t0039).
* Length / diameter asymmetry ~25–30x.
* Dan 2018 passive-TR prediction sign-inverted on t0024.

### Correction strategies (C1–C7) proposed

| # | Theme | Fix | Task | Cost |
| --- | --- | --- | --- | --- |
| C1 | Peak Hz low | Nav1.6 + Kv3 + NMDA restoration on t0022 | t00XX | local ~6 h |
| C2 | t0022 DSI pinned | Poisson background release | t00XX | local ~5 h |
| C3 | t0024 corr-drop missing | Port dsMicro-GH SAC network | t00XX | ~$20–40 Vast.ai ~14 h |
| C4 | L/d asymmetry | Replot t0034 + t0035 on L/lambda axis | t00XX | zero-cost ~1 h |
| C5 | DSI ceiling at 0.429 on t0022 | Fine-grained GABA ladder {3.5, 3.0, 2.5} nS | t00XX | local ~1 h |
| C6 | Missing Schachter amp | Re-test post-C1 | t00XX | local ~8 h |
| C7 | Peak Hz alt lever | BIP burst-rate / AMPA calibration | t00XX | local ~4 h |

## Discussion — Round 1: New Tasks

AI: "Proposed priority: C4 + C5 + C1 + C6 as a coherent block. C2 and C7 are hedges. C3 is
out-of-scope unless you want t0024 substrate for t0033."

Researcher: "I like C4 + C5 + C1 + C6."

AI: "Locked in. Formalised the four tasks: t0041 (C4, L/lambda analysis), t0042 (C5, fine GABA
ladder), t0043 (C1, Nav1.6 + Kv3 + NMDA on t0022), t0044 (C6, Schachter re-test on t0043). Execution
order: t0041, t0042, t0043 can run in parallel; t0044 waits for t0043."

## Discussion — Round 2: Suggestion Cleanup

AI proposed:

* Covered (handled automatically by `source_suggestion` field): S-0035-01, S-0019-03 (partial),
  S-0018-03 (partial), S-0022-02, S-0002-02.
* Reject (clearly superseded): S-0030-06 (vector-sum DSI as t0033 objective) — superseded by
  S-0034-07.
* Deprioritise high -> medium: S-0029-01, S-0029-02, S-0030-02, S-0010-01.

AI also asked about adding a Sheffield paywalled-paper retrieval task (Kim 2014, Sivyer 2013) and
whether to fold in t0031's fetch scope.

Researcher: "Confirm 1-3. 4 not yet. Please also save the comparison table in the brainstorm session
so that I can see it."

## Discussion — Round 3: Confirmation

AI summary:

* New tasks (4): t0041, t0042, t0043, t0044.
* Suggestion corrections (5): reject S-0030-06; reprioritise S-0029-01, S-0029-02, S-0030-02,
  S-0010-01 from high to medium.
* Scope note: comparison table saved in brainstorm task (per researcher's request); Sheffield paper
  retrieval deferred.

Researcher confirmed with "Confirm 1-3". Proceeding to Phase 3–6 per skill.

## Decisions Summary

1. Create t0041 (L/lambda electrotonic-length collapse analysis of t0034 and t0035). Data analysis
   only. Covers S-0035-01.
2. Create t0042 (fine-grained null-GABA ladder {3.5, 3.0, 2.5} nS on t0022 baseline diameter).
   Experiment. No source suggestion.
3. Create t0043 (add Nav1.6 + Kv3 to AIS_DISTAL and distal dendrites of t0022; restore NMDA at PD
   and ND BIPs). Feature-engineering + experiment. Covers S-0019-03.
4. Create t0044 (7-diameter Schachter re-test on t0043 substrate at GABA = 4 nS). Experiment.
   Depends on t0043. Covers S-0002-02.
5. Reject S-0030-06 (vector-sum DSI as t0033 objective). Superseded by S-0034-07.
6. Reprioritise S-0029-01, S-0029-02, S-0030-02, S-0010-01 from high to medium.
7. Sheffield paywalled-paper retrieval (Kim 2014, Sivyer 2013): deferred to a later wave.
8. Save master test table + published-data comparison as `results/test_vs_literature_table.md` at
   the researcher's explicit request.
9. No task cancellations or updates. t0023 remains intervention_blocked; t0031 remains not_started.

## Notes

* Researcher's phrasing "find ways to correct for this in our models" drove the "correction
  strategy" framing of the session rather than the usual "next experiments" framing. The
  master-table-first-then-discrepancies-then-corrections structure was adopted in response.
* Session did not ask the standard clarifying questions; the researcher substituted direct strategic
  direction which took precedence.
* The cross-task audit relies on numbers already reported in each task's `compare_literature.md`. No
  PDFs were re-read. Known caveat: Kim 2014 and Sivyer 2013 remain paywalled; where the compare
  files already noted "partial abstract only", that limitation carries forward.
