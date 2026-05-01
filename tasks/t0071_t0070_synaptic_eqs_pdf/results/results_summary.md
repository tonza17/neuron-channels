---
spec_version: "1"
task_id: "t0071_t0070_synaptic_eqs_pdf"
date: "2026-05-01"
---
# Results Summary: Two Standard DSGC Model Beds (v2 — synaptic-current equations + typeset PDF)

## Summary

This task delivers the **v2 writeup** of the project's two standard DSGC model beds and
**supersedes** [t0070]'s `results/results_detailed.md`. The v1 writeup was thorough but had two
gaps: (1) the canonical synaptic-current ohmic blocks (one per mechanism, of the form
$I_\mathrm{syn} = g_\mathrm{syn}(t,V)\,(V - E_\mathrm{syn})$) for the AMPA, NMDA, GABA, and ACh
point-process mechanisms in Bed A and the Exp2Syn ACh + GABA mechanisms in Bed B were never spelled
out (only the parameters appeared, in prose and tables); (2) there was no typeset PDF — equations
lived inside fenced `text` blocks and rendered in monospace. Both gaps are now closed. Bed A is the
deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC ported in [t0008] (ModelDB 189347, library
`modeldb_189347_dsgc`), used by [t0020], [t0065], [t0067], [t0068], and [t0069]. Bed B is the de
Rosenroll 2026 DSGC ported in [t0024] (library `de_rosenroll_2026_dsgc`), used by [t0066]. Each bed
section opens with the canonical Hodgkin-Huxley membrane equation $C_m \,dV/dt = -\sum_i I_i -
I_\mathrm{syn} - I_\mathrm{inj}$ rendered identically in LaTeX display math, then enumerates every
active conductance with `gbar`, `V_half`, kinetics, and reversal potential in a markdown table, then
defines the synaptic excitation and inhibition models for the preferred direction (PD) and null
direction (ND). A side-by-side comparison table at the end summarises the headline differences
across **18 dimensions**. Every numerical parameter carries a `code/<file>:line` citation back to
the committed source so the document is fully auditable.

The five new synaptic-current equation blocks added in this v2 are:

* **Bed A BIPsyn AMPA** — $I_\mathrm{AMPA} = 10^{-3} g_\mathrm{AMPA} (V - 0)$ with single-decay
  evolution $\dot g_\mathrm{AMPA} = -g_\mathrm{AMPA}/\tau_\mathrm{AMPA}$ ($\tau = 2$ ms) and
  per-vesicle Bernoulli release rule (`bipolarNMDA.mod:L103, L156, L143`).
* **Bed A BIPsyn NMDA** — $I_\mathrm{NMDA} = 10^{-3} g_\mathrm{NMDA}(t,V) (V - 0)$ with the
  Jahr-Stevens-style Mg block $g_\mathrm{NMDA} = (A - B)/(1 + n e^{-\gamma V_\mathrm{loc}})$,
  bi-exponential rise/decay states $A, B$ ($\tau_1 = 60$ ms decay, $\tau_2 = 2$ ms rise), $n = 0.30$
  mM⁻¹, $\gamma = 0.07$ mV⁻¹ (`bipolarNMDA.mod:L102, L104`).
* **Bed A SACinhibsyn GABA** — $I_\mathrm{GABA} = 10^{-3} g_\mathrm{GABA} (V - (-60))$ with
  $\tau_\mathrm{GABA} = 30$ ms, vesicular release with `gabaMOD = 0.33` (PD) / `0.99` (ND) scaling
  the presynaptic envelope (`SAC2RGCinhib.mod:L55, L92, L83`; `dsgc_model.hoc:L242-L243`).
* **Bed A SACexcsyn ACh** — same kinetic form as the GABA mechanism, with $\tau_\mathrm{ACh} = 3$
  ms, $E_\mathrm{ACh} = 0$ mV, and `achMOD = 0.25` (held constant across PD and ND in [t0020];
  zeroed in [t0065]'s IPSP_PASSIVE mode).
* **Bed B Exp2Syn ACh and GABA** — NEURON's standard `Exp2Syn` form $g(t) = f(B(t) - A(t))$ with the
  normalisation factor $f = 1/(-e^{-t_p/\tau_1} + e^{-t_p/\tau_2})$. ACh: $\tau_1 = 0.1$ ms, $\tau_2
  = 4$ ms, $E = 0$ mV, NetCon weight 0.001 µS. GABA: $\tau_1 = 0.5$ ms, $\tau_2 = 12$ ms, $E = -60$
  mV, NetCon weight 0.003 µS, with per-event Bernoulli release at $p_\mathrm{rel}(\theta)$ via the
  sigmoid $p_\mathrm{rel} \approx 0.05$ (PD) / $0.80$ (ND) and an AR(2) noise envelope
  (`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/`).

The task also produces a typeset PDF (`results/results_detailed.pdf`, ~1.09 MB, 10 pages) compiled
from the Typst source `results/results_detailed.typ` via `code/render_pdf.py`. The PDF renders
equations with proper math fonts (italic Greek, real subscripts/superscripts, real fractions) and
embeds the four schematic PNGs reused verbatim from [t0070]. **The recommended way to consume this
writeup is to read the PDF.** The markdown source remains the single source of truth for all
parameter citations and downstream aggregator views; `results_detailed.md` is a strict superset of
[t0070]'s markdown plus the five new equation blocks plus the LaTeX rewrites of every existing
equation.

No biophysical parameter value has changed between [t0070] and this v2: the conductance tables,
synaptic parameter tables, gabaMOD PD/ND values, sigmoidal release-probability constants, AR(2)
noise parameters, bar geometry, temperature, resting potential, and passive cable values are all
preserved verbatim with the same `code/<file>:L<line>` citations. Only the surrounding markup has
changed and the five new equation blocks are added.

## Metrics

* **Beds documented**: 2 (Bed A — t0008 deposited Poleg-Polsky 2016; Bed B — t0024 de Rosenroll 2026
  port).
* **Active conductances tabulated per bed**: **4** in Bed A (Na, Kdr, Km, Leak — Ca-L and Ca-T
  zeroed); **7** in Bed B (Na, Kdr, Km, Leak, CaL, CaT, plus `cad` calcium-decay shell).
* **Synapse types tabulated per bed**: **3** in Bed A (BIPsyn AMPA+NMDA, SACinhibsyn GABA, SACexcsyn
  ACh); **2 active + 1 latent** in Bed B (Exp2Syn ACh and Exp2Syn GABA active; Exp2NMDA vendored but
  not wired).
* **Side-by-side comparison rows**: **18** dimensions.
* **Schematic PNGs (copied verbatim from t0070)**: **4** (`bed_a_morphology.png` 345 KB,
  `bed_b_morphology.png` 146 KB, `bed_a_synaptic_diagram.png` 150 KB, `bed_b_synaptic_diagram.png`
  159 KB).
* **New synaptic-current equation blocks added in v2**: **5** (Bed A AMPA, Bed A NMDA, Bed A GABA,
  Bed A ACh, Bed B Exp2Syn ACh + GABA).
* **Typeset PDF size**: **1 091 129 bytes** (~1.09 MB), 10 pages; size-floor threshold is **50 000
  bytes** (the script exits non-zero if the PDF is below this).
* **Quantitative project metrics measured**: **0** (this is a documentation-only correction task; no
  NEURON simulations were run, so `results/metrics.json` is `{}` by design).

## Verification

* `verify_task_results t0071_t0070_synaptic_eqs_pdf` — see the orchestrator's post-implementation
  step report; the implementation document includes the mandatory frontmatter, the `## Note`
  superseding-statement, all required sections per
  `arf/specifications/task_results_specification.md`, and a `## Task Requirement Coverage` last
  section listing all `REQ-*` items as `Done`.
* `ruff check --fix tasks/t0071_t0070_synaptic_eqs_pdf/code/` — PASSED (zero errors).
* `ruff format tasks/t0071_t0070_synaptic_eqs_pdf/code/` — PASSED (idempotent).
* `mypy -p tasks.t0071_t0070_synaptic_eqs_pdf.code` — PASSED (zero errors).
* `code/render_pdf.py` — invoked under `run_with_logs.py`; returned 0 (PDF size above the 50 KB
  size-floor check); produced `results/results_detailed.pdf`.
* The four schematic PNGs match [t0070]'s files byte-for-byte (copied via `shutil.copyfile`).
