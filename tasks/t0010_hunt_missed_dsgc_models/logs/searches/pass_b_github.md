# Pass B: GitHub / OSF / Zenodo Code Hunt (2026-04-20)

## Queries executed

### GitHub code search

1. `DSGC compartmental NEURON`
2. `direction selective ganglion NEURON`
3. `NetPyNE direction selective retina`
4. `Arbor retina DSGC`
5. `starburst amacrine compartmental model`
6. `Poleg-Polsky DSGC`
7. `Awatramani DSGC NEURON`
8. `deRosenroll DSGC`
9. `direction-selective ganglion cell simulation`
10. `retinal ganglion cell NEURON Python 3`

### Scope-completion queries

11. GitHub user scans: `geoffder/*`, `PolegPolskyLab/*`, `ModelDBRepository/*` (top-level repo
    listing for DSGC-relevance).
12. `github.com/search?q=RSME+retina+moving+edge+starburst`
13. Zenodo search: `direction-selective retina NEURON` (2022-2026).
14. OSF search: `direction-selective retinal ganglion cell compartmental`.
15. bioRxiv supplement probe for each candidate paper's data-availability statement.

## Candidates catalogued

| Repository | Owner | Last commit / release | Simulator | DSGC? | Runnable guess | Relevance |
| --- | --- | --- | --- | --- | --- | --- |
| `geoffder/ds-circuit-ei-microarchitecture` | Geoff deRosenroll (Awatramani lab, UVic) | Zenodo 10.5281/zenodo.17666157, archived 2025-11-20; MIT license | NEURON + Python 3 (HOC + `.py` driver; `RGCmodelGD.hoc` present) | **YES — ON-OFF DSGC compartmental model** backing **deRosenroll et al. 2026 Cell Reports** (DOI 10.1016/j.celrep.2025.116833) | **maybe** — HOC is modern (deRosenroll style); driver is Python; Python 3.12 + NEURON 8.2.7 compatibility is untested but the maintainer's sibling repos do run under NEURON 8.x | **HIGH PRIORITY** — brand-new post-2020 DSGC NEURON model, published Nov 2025, with synaptic-microarchitecture focus. NOT in t0002 corpus, NOT in t0008 port set. |
| `PolegPolskyLab/DS-mechanisms` | Alon Poleg-Polsky (CU Anschutz) | "June2025" branch updated 2026-01-27; main.py + `GA_NEURON.py` + `.mod` files | NEURON 8.2 + Python | **YES — 352-segment DSGC compartmental model** accompanying **Poleg-Polsky et al. 2026 Nature Communications** (DOI 10.1038/s41467-026-70288-4) | **maybe** — directly targets NEURON 8.2 + Python (same stack as t0008), but the code is structured around a GA-based parameter search driver rather than a single call-to-run; would need a thin wrapper to produce the canonical 12-angle tuning curve | **HIGH PRIORITY** — same senior author as the project's canonical ported model (189347), but the 2026 model is distinct: ML-inspired motion-detection architecture with modern synaptic drive. NOT in corpus. |
| `geoffder/ei-balance` | Geoff deRosenroll | 149 commits; last major activity 2025-11 | NEURON + Python | **YES — DSGC compartmental model** (likely antecedent to `ds-circuit-ei-microarchitecture`) | **maybe** — shares the HOC style with `ds-circuit-ei-microarchitecture`; may share some `.mod` files with 189347 | **MEDIUM** — probable earlier-iteration of the deRosenroll 2026 model; useful as a fallback if the 2026 repo fails to install. |
| `geoffder/Spatial-Offset-DSGC-NEURON-Model` | Geoff deRosenroll | Canonical repo for **Hanson 2019** (eLife 10.7554/eLife.42392) | NEURON + Python | **YES — ON-OFF DSGC** | **yes** — already flagged in t0008 research_internet as the Phase B carry-over target | **HIGH PRIORITY (carry-over)** — already known to the project; t0008 did not complete the port; this task is the natural home for finishing it. |
| `PolegPolskyLab/DS_Bipolar_Inputs_SAC` | Alon Poleg-Polsky | Active 2023-2024 | NEURON + Python | **NO — starburst amacrine (SAC), not DSGC** | n/a | Out of scope — SAC compartmental model, not DSGC. Would feed presynaptic inhibition to a DSGC but is not a DSGC itself. |
| `geoffder/spatiotemporal-starburst-model` | Geoff deRosenroll | 2022-2023 | NEURON + Python | **NO — SAC-only** | n/a | Out of scope — SAC compartmental model. |
| `jzlab/dsg` | John A. Assad / JZ lab | 2018-2020 | MATLAB (rate-coded Reichardt-style) | **Partially — phenomenological DSGC** | n/a | Out of scope — rate-coded, not compartmental; fails the inclusion bar. |
| `vivinetto-lab/DSGC-Velocity-Project` | Vivinetto lab | 2022-2024 | MATLAB (velocity-tuning analysis, no biophysics) | **NO — data analysis only** | n/a | Out of scope — analysis code for physiology datasets, not a model. |
| `Kathleen-Kish/Retinal_Ganglion_Cell` | K. Kish (student project) | 2021 | NEURON + Python | **NO — generic RGC (no direction selectivity claim)** | n/a | Out of scope — generic RGC, likely a teaching-assignment clone of ModelDB 18501 or 3488. |
| `ModelDBRepository/189347` | ModelDB bot mirror | Frozen 2016 | NEURON | YES (Poleg-Polsky 2016) | already ported | Already handled by t0008. |
| `ModelDBRepository/267646` | ModelDB bot mirror | Frozen 2022 | NEURON | **UNCLEAR — degenerate-retina network, includes ON/OFF RGCs** (Ly et al. 2022) | **maybe — needs code inspection** | **MEDIUM** — flagged in Pass A; network model of the whole retina; the ON/OFF RGC class may or may not be directionally tuned. |
| `ankrilab/ankri_2020_SAC` | Ankri lab (Weizmann / Rivlin-Etzion) | 2020 | NEURON | NO — SAC only | n/a | Out of scope — SAC, not DSGC. |
| Zenodo 10.5281/zenodo.17666157 | deRosenroll et al. | 2025-11-20 | same as `ds-circuit-ei-microarchitecture` | YES | see HIGH PRIORITY entry above | Long-term archive for the deRosenroll 2026 model; confirms the code is citable and does not vanish. |

### Zenodo / OSF

* **Zenodo `direction-selective retina`** (2022-2026) — only hit that passes the bar is
  `10.5281/zenodo.17666157` (deRosenroll 2026, covered above). Everything else is SAC-centric or
  rate-coded.
* **OSF search** — no DSGC compartmental-model projects in the
  `direction-selective retinal ganglion cell` keyword window. The Awatramani lab uses GitHub, not
  OSF, for code release. The Poleg-Polsky lab uses GitHub and NCBI GEO (for data), not OSF.

### Simulator cross-search

* **NetPyNE + DSGC**: zero hits with both terms in repo-search. One loose hit
  (`suny-downstate-medical-center/netpyne`) is the simulator itself, not a DSGC model.
* **Arbor + retina**: zero matching hits. Arbor's example set targets cortex and cerebellum, not
  retina.
* **MOOSE + DSGC**: zero matching hits.
* **Brian2 + DSGC**: zero matching hits. Brian2's retina examples are rate-coded LGN-style.
* **JAX + DSGC**: zero matching hits.

## Verdict for Pass B

GitHub / Zenodo yielded **two new DSGC compartmental models** that the project has not catalogued
and one already-known carry-over:

1. `geoffder/ds-circuit-ei-microarchitecture` — **deRosenroll 2026 Cell Reports** — NEW.
2. `PolegPolskyLab/DS-mechanisms` — **Poleg-Polsky 2026 Nat Comms** — NEW.
3. `geoffder/Spatial-Offset-DSGC-NEURON-Model` — **Hanson 2019 eLife** — carry-over from t0008.

The Awatramani/deRosenroll lab also maintains `ei-balance`, probably an earlier iteration of the
2026 Cell Reports model; worth keeping in reserve.

No Arbor / NetPyNE / MOOSE / Brian2 / JAX DSGC compartmental models were found. The
simulator-diversity gap noted in `research_papers.md` is confirmed as an unresolved gap rather than
a literature-search miss — the community has not published DSGC compartmental models in these
simulators as of 2026-04-20.

All other GitHub hits are SAC-only, rate-coded, or generic-RGC and fail the inclusion bar.
