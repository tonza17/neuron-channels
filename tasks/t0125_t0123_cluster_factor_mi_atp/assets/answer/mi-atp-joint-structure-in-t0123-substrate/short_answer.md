---
spec_version: "2"
answer_id: "mi-atp-joint-structure-in-t0123-substrate"
answered_by_task: "t0125_t0123_cluster_factor_mi_atp"
date_answered: "2026-05-25"
---
## Question

Does the 68-d substrate of the t0123 single-seed MI vs ATP-per-spike NSGA-II run admit a joint MI x
ATP latent factor (|r| > 0.30 on both metrics simultaneously), or are MI and ATP driven by decoupled
factors?

## Answer

No, the t0123 substrate does not contain a joint MI x ATP factor. Varimax factor analysis on the
full 5760-cell pool retained 10 factors (16 Kaiser eigenvalues > 1, total variance explained 34.3%)
and zero factors satisfy |r_MI| > 0.30 AND |r_ATP| > 0.30 simultaneously. The two strongest
MI-loaded factors carry r_MI = -0.358 / +0.463 but only r_ATP = +0.205 / +0.063, and the strongest
ATP-loaded factor (F1) ranks 7th on |r_MI|. This contrasts with t0117's pooled four-seed DSI x PD
substrate which found one joint factor F1 (r_DSI = +0.421, r_PD = +0.352, 12.6% variance).

## Sources

* Task: `t0125_t0123_cluster_factor_mi_atp`
* Task: `t0123_bedb_mi_atp_per_spike_nsga2`
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
* Paper: `10.1371_journal.pcbi.0020094`
* Paper: `10.1038_nn1352`
* Paper: `10.1038_nrn1949`
