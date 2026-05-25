---
spec_version: "2"
answer_id: "dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact"
answered_by_task: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
date_answered: "2026-05-25"
---

# DSGC DSI vs ATP-per-spike: Carter-Bean / Howarth / Attwell-Laughlin

## Question

Does the DSGC DSI-vs-ATP-per-spike Pareto front show a Carter-Bean Na/K-overlap penalty, and where do its top cells sit relative to the revised Howarth 2012 17% cortex / 21% cerebellum signalling-ATP budget (and historically, the original Attwell-Laughlin 2001 47% anchor)?

## Answer

INSUFFICIENT EVIDENCE: only 6 legit cells passed the silence guard. The Pareto front structure cannot be quantitatively characterised under the single-seed protocol. The bootstrap Pearson r between DSI and ATP-per-spike across the legit top-6 cohort is r = 0.980 (95% CI: [0.972, 1.000], n_legit = 6, n_pareto = 6). Run reached 60 / 60 gens at $0.96; stop trigger n_gen_reached.

## Sources

* Sengupta et al. 2010 (10.1371/journal.pcbi.1000840)
* Howarth, Gleeson & Attwell 2012 (10.1038/jcbfm.2012.35)
* Attwell & Laughlin 2001 (10.1097/00004647-200110000-00001)
* Carter & Bean 2009 (10.1016/j.neuron.2009.12.011)
* t0122_dsi_cytoplasm_volume_nsga2 (cytoplasm cross-reference)
* t0123_bedb_mi_atp_per_spike_nsga2 (ATP recipe predecessor)
