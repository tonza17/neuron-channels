# ✅ t0070 v2 - synaptic-current equations + typeset PDF

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0071_t0070_synaptic_eqs_pdf` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T14:40:52Z |
| **Completed** | 2026-05-01T15:25:00Z |
| **Duration** | 44m |
| **Dependencies** | [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Task types** | `correction` |
| **Step progress** | 7/15 |
| **Task folder** | [`t0071_t0070_synaptic_eqs_pdf/`](../../../tasks/t0071_t0070_synaptic_eqs_pdf/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0071_t0070_synaptic_eqs_pdf/task_description.md)*

# t0070 v2 — synaptic-current equations + typeset PDF

## Motivation

t0070 produced a research-paper writeup of the project's two DSGC model beds (Bed A: t0008
deposited Poleg-Polsky 2016; Bed B: t0024 de Rosenroll 2026 port). The writeup is otherwise
thorough but it has two gaps:

1. **Missing canonical synaptic-current equations.** The HH membrane equation is written
   explicitly at the top of each bed's section, and every active conductance is enumerated as
   `Iᵢ = gᵢ · ... · (V − Eᵢ)`. But for synaptic currents (AMPA, NMDA, GABA, ACh in Bed A;
   Exp2Syn ACh and GABA in Bed B) the parameters and kinetics are described in prose and
   parameter tables only — the canonical `I_syn = g_syn(t,V) · (V − E_syn)` blocks are absent.
   The user explicitly noted this gap.
2. **No typeset PDF.** t0070 produced markdown only. The user wants a PDF with proper math
   typesetting (italic Greek, real subscripts/superscripts, real fractions) for use in a
   written report and a presentation.

The corrections specification (`arf/specifications/corrections_specification.md` v3) restricts
formal correction files to asset kinds (suggestion, paper, answer, dataset, library, model,
predictions). It does not cover result documents. So this task is a **semantic** correction
implemented as a new `correction`-type task: t0071's `results/results_detailed.md` is the v2
of the writeup and supersedes t0070's. Readers should use t0071's version.

## Scope

This task does NOT re-derive any equations or change any biophysical parameter values. Every
parameter cited in t0071 is the same parameter cited in t0070, with the same
`code/<file>:<line>` provenance. The only changes are:

* **Add** the missing synaptic-current equation blocks under each bed's "Synaptic excitation"
  and "Synaptic inhibition" subsections. Five blocks total:
  * Bed A `BIPsyn` AMPA (single-decay; `bipolarNMDA.mod:103, 156`)
  * Bed A `BIPsyn` NMDA (bi-exponential rise/decay × Mg block; `bipolarNMDA.mod:102-104`)
  * Bed A `SACinhibsyn` GABA (single-decay + presynaptic envelope × `gabaMOD`;
    `SAC2RGCinhib.mod`)
  * Bed A `SACexcsyn` ACh (single-decay + presynaptic envelope × `achMOD`; `SAC2RGCexc.mod`)
  * Bed B Exp2Syn ACh + Exp2Syn GABA (NEURON's standard `Exp2Syn` form, normalised
    bi-exponential) — one block per channel, with the GABA block adding the per-event
    Bernoulli direction-encoding and AR(2) noise envelope from
    `tasks/t0066_t0024_epsp_ipsp_vm_protocol/`.
* **Rewrite** every equation block (existing HH equations, Mg-block, vesicular release, and
  the new synaptic blocks) in LaTeX math syntax (`$...$` inline, `$$...$$` display) so that
  Typst (and any future pandoc/MathJax/KaTeX renderer) typesets them properly.
* **Produce** `results/results_detailed.pdf` via the Typst compiler (`pip install typst`,
  pure-Python wheel that bundles the Rust binary — no LaTeX install required).
* **Produce** `results/results_detailed.typ` (Typst source) so the PDF is reproducible.
* **Update** `results/results_summary.md` to reference the new PDF and equation additions.

The four schematic PNGs from t0070 (`bed_a_morphology.png`, `bed_b_morphology.png`,
`bed_a_synaptic_diagram.png`, `bed_b_synaptic_diagram.png`) are reused verbatim — copied into
this task's `results/images/` so the v2 document is fully self-contained.

## Approach

1. Add `typst` as a dependency in `pyproject.toml`.
2. Write `code/render_pdf.py` — small script that compiles `results/results_detailed.typ` to
   `results/results_detailed.pdf` via the `typst` Python API.
3. Author `results/results_detailed.md` (v2 markdown) by:
   * Copying t0070's `results/results_detailed.md` text verbatim as the starting point.
   * Replacing every fenced-text equation block with LaTeX math (`$$...$$`).
   * Adding the 5 new synaptic-current equation blocks under the appropriate subsections.
   * Updating the frontmatter to reference t0071 and noting the supersession of t0070.
4. Author `results/results_detailed.typ` — same content as the markdown but in Typst syntax.
   Equations in Typst use `$ ... $` (display) and `$...$` (inline) with Typst's math notation.
5. Run `code/render_pdf.py` to produce `results/results_detailed.pdf`. Verify visually (open
   the PDF, confirm equations render with proper math fonts).
6. Copy the 4 PNGs from t0070 into `results/images/`.
7. Write `results/results_summary.md` referencing the PDF.
8. Standard task closure: metrics.json (`{}`), costs.json, remote_machines_used.json,
   suggestions.json (likely 1-2 suggestions about the PDF pipeline becoming a project
   library).

## Outputs

* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md` — v2 markdown with all
  equations (HH + 5 new synaptic blocks + existing) in LaTeX math syntax.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.typ` — Typst source.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf` — typeset PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_summary.md` — abstract pointing at the
  PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/{bed_a,bed_b}_morphology.png` and
  `{bed_a,bed_b}_synaptic_diagram.png` — copied verbatim from t0070.
* `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` — Typst→PDF compile script.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/{metrics,costs,remote_machines_used}.json` +
  `suggestions.json` — standard bookkeeping.

## Compute and budget

* Local Windows workstation. ~$0 external cost. Adds one Python wheel (`typst`).
* Time: ~1.5-2 hours (most of it is the careful equation transcription).

## Dependencies

Only `t0070_writeup_two_model_beds`. The starting point is t0070's
`results/results_detailed.md`.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Typst Python wheel not available for Windows / Python 3.13. | `pip install typst` fails. | Install Quarto (`winget install --id Posit.Quarto`) or use `pandoc + tectonic` instead. Document the chosen pipeline in the task. |
| 2 | Typst's math syntax differs subtly from LaTeX (e.g., `dot.c` vs `\cdot`, `op("...")` for multi-letter function names). | PDF compiles but equations look wrong. | Use Typst's own math reference; for any equation that won't render correctly in Typst, fall back to a rendered SVG via matplotlib mathtext and embed as image. |
| 3 | PDF includes the schematic PNGs but Typst can't find them at compile time. | Compile error or missing-image placeholder. | Use absolute paths in the Typst source; verify with a smoke test on one image before adding all four. |
| 4 | The corrections-spec restriction means there's no formal way to mark t0070's writeup as superseded. | Aggregators may still surface t0070 as the canonical writeup. | The user is informed — t0071's results_detailed.md is the new canonical version and t0070 stays as historical record. Add a clear note at the top of t0071's results document. |
| 5 | Equation transcription introduces a numerical error vs t0070. | Manual cross-check against t0070's parameter tables. | Diff t0071 against t0070 on every numerical value before commit; only structural and syntactic changes should differ. |

## Verification criteria

* `results/results_detailed.md` exists with all standard sections per the results
  specification, contains every equation block from t0070 in LaTeX math syntax, and has the 5
  new synaptic-current equation blocks.
* `results/results_detailed.typ` exists and compiles to PDF without errors.
* `results/results_detailed.pdf` exists, is non-empty, and renders the equations with proper
  math fonts (visual check).
* All standard verificators pass (verify_task_results, verify_task_metrics,
  verify_suggestions, verify_logs, verify_task_complete).

## Task Requirement Checklist

* **REQ-1 (5 synaptic-current equation blocks present)**: BIPsyn AMPA, BIPsyn NMDA,
  SACinhibsyn GABA, SACexcsyn ACh, Exp2Syn ACh+GABA on bed B.
* **REQ-2 (HH equation in LaTeX math)**: each bed's `C_m · dV/dt = -Σ I_i - I_syn - I_inj`
  block converted to `$$C_m \frac{dV}{dt} = ...$$` form.
* **REQ-3 (every equation in LaTeX math syntax)**: no fenced-text equations remain; all are
  `$...$` or `$$...$$`.
* **REQ-4 (Typst PDF rendered)**: `results_detailed.pdf` exists, non-empty, equations visibly
  typeset in math fonts.
* **REQ-5 (typst dep added)**: `typst` listed in `pyproject.toml`.
* **REQ-6 (PNGs preserved)**: 4 PNGs copied from t0070 into `results/images/`.
* **REQ-7 (results_summary.md updated)**: references the new PDF and notes the additions.
* **REQ-8 (every numeric parameter unchanged from t0070)**: structural and syntactic changes
  only; no biophysical value changed.
* **REQ-9 (note in results_detailed.md that this supersedes t0070)**: clear notice in the
  Summary or front-matter.
* **REQ-10 (PDF compile script in code/)**: `code/render_pdf.py` reproducible.

</details>

## Suggestions Generated

<details>
<summary><strong>Promote the Typst markdown-to-PDF pipeline into a reusable project
library `arf_typst_writeup`</strong> (S-0071-01)</summary>

**Kind**: library | **Priority**: medium

This task introduced a one-off Typst pipeline (`code/render_pdf.py` +
`results/results_detailed.typ` + `pyproject.toml` `typst>=0.14.8` dep) that compiles a
markdown writeup with LaTeX math into a typeset PDF — no LaTeX install required because the
`typst` Python wheel bundles the Rust binary. Several recent tasks (t0008/t0024 paper ports,
t0070 two-bed writeup, every brainstorm) produce markdown that would benefit from a typeset
PDF for reports and presentations. Build a project library `arf_typst_writeup` exposing one
CLI: `python -m arf_typst_writeup --md <md> --out <pdf>` that auto-translates LaTeX math to
Typst math (`\frac` -> `frac()`, `\cdot` -> `dot.c`, `\mathrm{...}` -> `op("...")`,
`\bigl`/`\bigr` -> `lr(...)`), bundles a default Typst template, and runs the same 50 KB
size-floor check used here. Acceptance: re-render t0070 and t0071 `results_detailed.md` from
one library invocation. Recommended task types: write-library, infrastructure-setup.

</details>

<details>
<summary><strong>Extend corrections spec v4 with `target_kind: result_document` to
track result-document supersedings</strong> (S-0071-02)</summary>

**Kind**: library | **Priority**: medium

This task is a SEMANTIC correction of t0070's `results/results_detailed.md` because
corrections spec v3 (`arf/specifications/corrections_specification.md`) restricts
`target_kind` to asset kinds (suggestion, paper, answer, dataset, library, model,
predictions). Result documents (`results_summary.md`, `results_detailed.md`,
`compare_literature.md`, `metrics.json`) are not covered. Consequence: aggregators still
surface t0070's v1 writeup as canonical even though t0071's v2 supersedes it; the only signal
is a `## Note` paragraph at the top. Bump corrections spec to v4 by adding `result_document`
to `target_kind`, with `target_id` of the filename (`results_detailed.md`, etc.); update
`arf/scripts/aggregators/aggregate_*.py` to apply the overlay; update `verify_corrections.py`;
backfill a v4 correction file for t0071 superseding t0070's `results_detailed.md`. Recommended
task types: infrastructure-setup, write-library, correction.

</details>

<details>
<summary><strong>Quantify Bed A vs Bed B `celsius` and `v_init` divergence revealed
by the side-by-side equation table</strong> (S-0071-03)</summary>

**Kind**: experiment | **Priority**: medium

Authoring all equations side-by-side in one document made four numeric divergences between Bed
A and Bed B unambiguous (rows 7, 9, 16, 17 of the comparison table in
`results_detailed.md:L778-L799`): `celsius` 32 vs 36.9 deg C (HHst gating tau differs ~2x via
Q10), `v_init` -65 vs -60 mV (shifts Mg-block operating point and Na inactivation), NMDA
on/off (S-0070-04 wires it on but does NOT pick a target value), CaL+CaT zeroed/default
(S-0070-03 turns Bed A's Ca on but does NOT pick a target). Run a 4-condition factorial sweep
on Bed A's t0065 protocol toggling `celsius in {32, 36.9}` x `v_init in {-65, -60}` to
quantify how much of the observed Bed A vs Bed B DSI / peak-Hz / EPSP-envelope difference is
attributable to these two non-Ca, non-NMDA conventions alone — the result decides whether
project-wide convention harmonisation is needed before S-0070-01..04 can be interpreted.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Add `verify_results_equations.py` to round-trip every `$$...$$`
block through Typst</strong> (S-0071-04)</summary>

**Kind**: library | **Priority**: low

While transcribing t0070's prose equations into LaTeX math for this v2, several Typst-vs-LaTeX
subtleties (`dot.c` vs `\cdot`, `op("syn")` vs `\mathrm{syn}`, `\bigl`/`\bigr` not supported
in Typst math, `frac(d V, d t)` vs `\frac{dV}{dt}`) caused multiple PDF compile failures only
caught visually after `code/render_pdf.py` finished. Future tasks editing equation-heavy
markdown will hit the same class of bug. Add
`arf/scripts/verificators/verify_results_equations.py <task_id>` that scans
`tasks/<task_id>/results/results_detailed.md` for every `$...$` and `$$...$$` block, attempts
to compile each in isolation through the `typst` Python wheel using a minimal stub document,
and reports per-block PASS/FAIL with line number and Typst error message. Wire it into the
standard verification cascade. Recommended task types: infrastructure-setup, write-library.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/results_summary.md)*

--- spec_version: "1" task_id: "t0071_t0070_synaptic_eqs_pdf" date: "2026-05-01" ---
# Results Summary: Two Standard DSGC Model Beds (v2 — synaptic-current equations + typeset PDF)

## Summary

This task delivers the **v2 writeup** of the project's two standard DSGC model beds and
**supersedes** [t0070]'s `results/results_detailed.md`. The v1 writeup was thorough but had
two gaps: (1) the canonical synaptic-current ohmic blocks (one per mechanism, of the form
$I_\mathrm{syn} = g_\mathrm{syn}(t,V)\,(V - E_\mathrm{syn})$) for the AMPA, NMDA, GABA, and
ACh point-process mechanisms in Bed A and the Exp2Syn ACh + GABA mechanisms in Bed B were
never spelled out (only the parameters appeared, in prose and tables); (2) there was no
typeset PDF — equations lived inside fenced `text` blocks and rendered in monospace. Both gaps
are now closed. Bed A is the deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC ported in [t0008]
(ModelDB 189347, library `modeldb_189347_dsgc`), used by [t0020], [t0065], [t0067], [t0068],
and [t0069]. Bed B is the de Rosenroll 2026 DSGC ported in [t0024] (library
`de_rosenroll_2026_dsgc`), used by [t0066]. Each bed section opens with the canonical
Hodgkin-Huxley membrane equation $C_m \,dV/dt = -\sum_i I_i - I_\mathrm{syn} - I_\mathrm{inj}$
rendered identically in LaTeX display math, then enumerates every active conductance with
`gbar`, `V_half`, kinetics, and reversal potential in a markdown table, then defines the
synaptic excitation and inhibition models for the preferred direction (PD) and null direction
(ND). A side-by-side comparison table at the end summarises the headline differences across
**18 dimensions**. Every numerical parameter carries a `code/<file>:line` citation back to the
committed source so the document is fully auditable.

The five new synaptic-current equation blocks added in this v2 are:

* **Bed A BIPsyn AMPA** — $I_\mathrm{AMPA} = 10^{-3} g_\mathrm{AMPA} (V - 0)$ with
  single-decay evolution $\dot g_\mathrm{AMPA} = -g_\mathrm{AMPA}/\tau_\mathrm{AMPA}$ ($\tau =
  2$ ms) and per-vesicle Bernoulli release rule (`bipolarNMDA.mod:L103, L156, L143`).
* **Bed A BIPsyn NMDA** — $I_\mathrm{NMDA} = 10^{-3} g_\mathrm{NMDA}(t,V) (V - 0)$ with the
  Jahr-Stevens-style Mg block $g_\mathrm{NMDA} = (A - B)/(1 + n e^{-\gamma V_\mathrm{loc}})$,
  bi-exponential rise/decay states $A, B$ ($\tau_1 = 60$ ms decay, $\tau_2 = 2$ ms rise), $n =
  0.30$ mM⁻¹, $\gamma = 0.07$ mV⁻¹ (`bipolarNMDA.mod:L102, L104`).
* **Bed A SACinhibsyn GABA** — $I_\mathrm{GABA} = 10^{-3} g_\mathrm{GABA} (V - (-60))$ with
  $\tau_\mathrm{GABA} = 30$ ms, vesicular release with `gabaMOD = 0.33` (PD) / `0.99` (ND)
  scaling the presynaptic envelope (`SAC2RGCinhib.mod:L55, L92, L83`;
  `dsgc_model.hoc:L242-L243`).
* **Bed A SACexcsyn ACh** — same kinetic form as the GABA mechanism, with $\tau_\mathrm{ACh} =
  3$ ms, $E_\mathrm{ACh} = 0$ mV, and `achMOD = 0.25` (held constant across PD and ND in
  [t0020]; zeroed in [t0065]'s IPSP_PASSIVE mode).
* **Bed B Exp2Syn ACh and GABA** — NEURON's standard `Exp2Syn` form $g(t) = f(B(t) - A(t))$
  with the normalisation factor $f = 1/(-e^{-t_p/\tau_1} + e^{-t_p/\tau_2})$. ACh: $\tau_1 =
  0.1$ ms, $\tau_2 = 4$ ms, $E = 0$ mV, NetCon weight 0.001 µS. GABA: $\tau_1 = 0.5$ ms,
  $\tau_2 = 12$ ms, $E = -60$ mV, NetCon weight 0.003 µS, with per-event Bernoulli release at
  $p_\mathrm{rel}(\theta)$ via the sigmoid $p_\mathrm{rel} \approx 0.05$ (PD) / $0.80$ (ND)
  and an AR(2) noise envelope (`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/`).

The task also produces a typeset PDF (`results/results_detailed.pdf`, ~1.09 MB, 10 pages)
compiled from the Typst source `results/results_detailed.typ` via `code/render_pdf.py`. The
PDF renders equations with proper math fonts (italic Greek, real subscripts/superscripts, real
fractions) and embeds the four schematic PNGs reused verbatim from [t0070]. **The recommended
way to consume this writeup is to read the PDF.** The markdown source remains the single
source of truth for all parameter citations and downstream aggregator views;
`results_detailed.md` is a strict superset of [t0070]'s markdown plus the five new equation
blocks plus the LaTeX rewrites of every existing equation.

No biophysical parameter value has changed between [t0070] and this v2: the conductance
tables, synaptic parameter tables, gabaMOD PD/ND values, sigmoidal release-probability
constants, AR(2) noise parameters, bar geometry, temperature, resting potential, and passive
cable values are all preserved verbatim with the same `code/<file>:L<line>` citations. Only
the surrounding markup has changed and the five new equation blocks are added.

## Metrics

* **Beds documented**: 2 (Bed A — t0008 deposited Poleg-Polsky 2016; Bed B — t0024 de
  Rosenroll 2026 port).
* **Active conductances tabulated per bed**: **4** in Bed A (Na, Kdr, Km, Leak — Ca-L and Ca-T
  zeroed); **7** in Bed B (Na, Kdr, Km, Leak, CaL, CaT, plus `cad` calcium-decay shell).
* **Synapse types tabulated per bed**: **3** in Bed A (BIPsyn AMPA+NMDA, SACinhibsyn GABA,
  SACexcsyn ACh); **2 active + 1 latent** in Bed B (Exp2Syn ACh and Exp2Syn GABA active;
  Exp2NMDA vendored but not wired).
* **Side-by-side comparison rows**: **18** dimensions.
* **Schematic PNGs (copied verbatim from t0070)**: **4** (`bed_a_morphology.png` 345 KB,
  `bed_b_morphology.png` 146 KB, `bed_a_synaptic_diagram.png` 150 KB,
  `bed_b_synaptic_diagram.png` 159 KB).
* **New synaptic-current equation blocks added in v2**: **5** (Bed A AMPA, Bed A NMDA, Bed A
  GABA, Bed A ACh, Bed B Exp2Syn ACh + GABA).
* **Typeset PDF size**: **1 091 129 bytes** (~1.09 MB), 10 pages; size-floor threshold is **50
  000 bytes** (the script exits non-zero if the PDF is below this).
* **Quantitative project metrics measured**: **0** (this is a documentation-only correction
  task; no NEURON simulations were run, so `results/metrics.json` is `{}` by design).

## Verification

* `verify_task_results t0071_t0070_synaptic_eqs_pdf` — see the orchestrator's
  post-implementation step report; the implementation document includes the mandatory
  frontmatter, the `## Note` superseding-statement, all required sections per
  `arf/specifications/task_results_specification.md`, and a `## Task Requirement Coverage`
  last section listing all `REQ-*` items as `Done`.
* `ruff check --fix tasks/t0071_t0070_synaptic_eqs_pdf/code/` — PASSED (zero errors).
* `ruff format tasks/t0071_t0070_synaptic_eqs_pdf/code/` — PASSED (idempotent).
* `mypy -p tasks.t0071_t0070_synaptic_eqs_pdf.code` — PASSED (zero errors).
* `code/render_pdf.py` — invoked under `run_with_logs.py`; returned 0 (PDF size above the 50
  KB size-floor check); produced `results/results_detailed.pdf`.
* The four schematic PNGs match [t0070]'s files byte-for-byte (copied via `shutil.copyfile`).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0071_t0070_synaptic_eqs_pdf" date: "2026-05-01" ---
# Two Standard DSGC Model Beds: A Side-by-Side HH-Equation Reference (v2)

## Note

This document is the **v2 writeup** of the project's two standard DSGC model beds and
**supersedes** [t0070]'s `results/results_detailed.md`. Two gaps in the v1 writeup are
addressed here:

1. **Synaptic-current equations were missing.** The Hodgkin-Huxley membrane equation and every
   active conductance were given as explicit `I = g · ... · (V − E)` blocks, but the synaptic
   currents (AMPA, NMDA, GABA, ACh in Bed A; Exp2Syn ACh, Exp2Syn GABA in Bed B) were
   described in prose and parameter tables only. This v2 adds the canonical
   $I_\mathrm{syn}(t,V) = g_\mathrm{syn}(t,V)\,(V - E_\mathrm{syn})$ block under each bed's
   "Synaptic excitation" and "Synaptic inhibition" subsections, with the state-variable
   evolution and discrete release rule clearly stated. Five new equation blocks total: Bed A
   BIPsyn AMPA, Bed A BIPsyn NMDA, Bed A SACinhibsyn GABA, Bed A SACexcsyn ACh, and Bed B
   Exp2Syn ACh + Exp2Syn GABA.

2. **No typeset PDF.** v1 was markdown only. This v2 ships `results/results_detailed.typ`
   (Typst source) and `results/results_detailed.pdf` (typeset PDF) so equations render in
   proper math fonts (italic Greek, real subscripts/superscripts, real fractions). Every
   equation in the v1 fenced `text` blocks has been rewritten in LaTeX math syntax (`$...$`
   inline, `$$...$$` display) so downstream renderers (Typst, MathJax, KaTeX, pandoc) typeset
   them correctly.

No biophysical parameter value has changed between [t0070] and this v2. Every numerical value
carries the same `code/<file>:L<line>` citation; only the surrounding markup has changed and
the five new equation blocks have been added. Reading the PDF at
`tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf` is the recommended way to
consume this writeup.

* * *

## Summary

This task supersedes [t0070]'s research-paper writeup of the project's two canonical
direction-selective ganglion cell (DSGC) model substrates, adding the missing synaptic-current
equation blocks and a typeset PDF. **Bed A** is the deposited Poleg-Polsky 2016 ON-OFF DRD4
DSGC ported in [t0008] (ModelDB 189347, library `modeldb_189347_dsgc`, upstream commit
`87d669dcef18e9966e29c88520ede78bc16d36ff`); it is the substrate for [t0020] (gabaMOD-swap
protocol), [t0065] (EPSP/IPSP/FULL Vm protocol), [t0067] (soma channel sweep), [t0068] (Nav1.6
+ Kv3 co-expression rescue), and [t0069] (AIS-localised channel sweep). **Bed B** is the de
Rosenroll 2026 DSGC ported in [t0024] (library `de_rosenroll_2026_dsgc`, upstream commit
`a23f642aa6557a23a51bf76f51e420e8149773fa`); it is the substrate for [t0066] (EPSP/IPSP/FULL
Vm protocol on the de Rosenroll cell). Each bed is presented in parallel structure: Morphology
→ canonical Hodgkin-Huxley membrane equation → conductance table → synaptic excitation (PD vs
ND) → synaptic inhibition (PD vs ND) → differences from the original paper. A side-by-side
comparison table at the end summarises the headline differences across 18 dimensions. Every
numerical parameter carries a `code/<file>:line` citation back to the committed source so the
document is fully auditable.

## Methodology

* **Machine**: local Windows 11 workstation; no remote compute, no GPU, no NEURON simulations.
* **Runtime**: total ~2 hours of equation transcription, Typst authoring, and PDF rendering.
  Typst compile under 5 seconds. Implementation start: 2026-05-01T14:46:58Z; implementation
  end: 2026-05-01.
* **Methods**: this is a documentation-only **correction** task. No new experiments were run.
  Every parameter quoted in the bed sections below is the same value cited in [t0070], traced
  back to a specific line of the committed library source (`HHst.mod`, `HHst_noiseless.mod`,
  `bipolarNMDA.mod`, `SAC2RGCinhib.mod`, `SAC2RGCexc.mod`, `Exp2NMDA.mod`, `cadecay.mod`,
  `RGCmodel.hoc`, `RGCmodelGD.hoc`, `main.hoc`, `dsgc_model.hoc`) or to the runtime parameter
  overrides in the dependency tasks' `code/build_cell.py`, `code/constants.py`, and
  `code/run_*.py` files. Source paths use the convention `code/<file>:L<line>` where `code/`
  is shorthand for the parent task's `assets/library/<lib>/sources/` directory or
  `tasks/<task>/code/` directory; the full path is given on first reference in each
  subsection.
* **Schematic figures**: four PNGs in `results/images/` are reused verbatim from [t0070]
  (`bed_a_morphology.png`, `bed_b_morphology.png`, `bed_a_synaptic_diagram.png`,
  `bed_b_synaptic_diagram.png`); they were copied with `shutil.copyfile` and not regenerated.
* **Equation typesetting**: every equation block is now in LaTeX math syntax. Inline math uses
  `$...$`; display math uses `$$...$$`. The Typst source (`results/results_detailed.typ`) uses
  Typst's native math notation (`$ ... $` with whitespace-padded delimiters for display,
  `frac(d V, d t)` for true fractions, `op("syn")` / `"syn"` for multi-letter operator names,
  `dot.c` for the centred multiplication dot) and was compiled to PDF with the `typst` Python
  wheel (no LaTeX install required) via `code/render_pdf.py`.
* **Quantitative metrics**: none. No simulations were run, so `results/metrics.json` is `{}`.
  The four registered project metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`) all require simulated AP rates from a
  NEURON tuning-curve sweep; none apply to this documentation-only task. Structural counts are
  reported in the `## Structural Counts` section below.

## Structural Counts

The document does not produce continuous quantitative metrics, but it does produce a
structured inventory whose dimensions can be counted:

* **Number of beds documented**: 2 (Bed A — t0008 deposited Poleg-Polsky 2016; Bed B — t0024
  de Rosenroll 2026 port).
* **Active conductances tabulated per bed**: 4 in Bed A (Na, Kdr, Km, Leak — Ca-L and Ca-T are
  zeroed by `init_active`); 7 in Bed B (Na, Kdr, Km, Leak, CaL, CaT, plus the `cad`
  calcium-decay shell).
* **Synapse types tabulated per bed**: 3 in Bed A (BIPsyn AMPA+NMDA, SACinhibsyn GABA,
  SACexcsyn ACh); 2 active + 1 latent in Bed B (Exp2Syn ACh, Exp2Syn GABA active in every
  driver; Exp2NMDA vendored but not wired into `run_tuning_curve.py` or the EPSP/IPSP/Vm
  protocol).
* **Side-by-side comparison rows**: 18 dimensions.
* **Schematic PNGs**: 4 (two morphology, two synaptic-conductance).
* **New synaptic-current equation blocks added in v2**: 5 (Bed A AMPA, Bed A NMDA, Bed A GABA,
  Bed A ACh, Bed B Exp2Syn ACh + GABA).

* * *

## Bed A: Poleg-Polsky 2016 (t0008 + t0020)

Bed A wraps the deposited Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC from ModelDB 189347
with no modification to the morphology or kinetics. The library asset is
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`, vendoring upstream
commit `87d669dcef18e9966e29c88520ede78bc16d36ff`. The `code/build_cell.py` and
`code/constants.py` files in [t0008] are the single source of truth for which HOC defaults are
overridden at runtime; the [t0020] task added the gabaMOD-swap protocol that established the
canonical preferred-direction (PD) vs null-direction (ND) convention used throughout the
project.

### Morphology

![Bed A morphology schematic — soma, ON and OFF dendrites, BIPsyn / SACinhibsyn / SACexcsyn
markers](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_a_morphology.png)

*Figure A1 (illustrative; not to scale): the schematic shows the cell as 1 soma + 350 dendrite
sections drawn as a radial fan. The 282 ON-typed dendrites bear the synaptic triple (BIPsyn
AMPA+ NMDA bipolar drive, SACinhibsyn GABA, SACexcsyn ACh). The OFF dendrites bear no
synapses. The diagram does not reproduce the 3D pt3d coordinates from
`RGCmodel.hoc:L212-11722` — refer to the HOC source for the true dendritic geometry.*

The cell is built by the deposited HOC template `RGCmodel.hoc` (11 861 lines). Key facts:

* **Section count**: 1 soma + 350 `dend[i]` sections (`create soma, dend[350]`,
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/RGCmodel.hoc:L14`).
* **Compartment discretisation**: every section has $n_\mathrm{seg} = 1$
  (`RGCmodel.hoc:L11818`).
* **Per-dendrite diameter**: $\mathrm{diam} = 0.5 + 2.58 \cdot
  \exp\!\left(-(d(0.5)-10)/10\right)$ µm (`RGCmodel.hoc:L11814`); diameter tapers from ~3.08
  µm near the soma to ~0.5 µm at the tips.
* **ON / OFF sort**: $\text{if } z_\mathrm{3d}(n_\mathrm{3d}-1) \geq -0.16 \cdot
  y_\mathrm{3d}(n_\mathrm{3d}-1) + 46 \;\Rightarrow\; \text{ON.append()}$ — 282 dendrites land
  in the ON SectionList, the remaining 68 in OFF (`RGCmodel.hoc:L11801-L11803`).
* **Synapse placement**: every ON dendrite hosts one BIPsyn (AMPA+NMDA), one SACinhibsyn
  (GABA), and one SACexcsyn (ACh) at the section midpoint, placed by the `init` proc loop
  (`RGCmodel.hoc:L11825-L11851`). Total: 846 point processes per cell
  (`tasks/t0008_port_modeldb_189347/code/constants.py:L57-L69` `BUNDLED_NUM_SOMA = 1`,
  `BUNDLED_NUM_DEND = 350`, `N_SYNAPSES_EACH_TYPE = 282`).
* **Passive cable**: $R_a = 100\;\Omega\!\cdot\!\mathrm{cm}$ (`dsgc_model.hoc:L317`); $c_m =
  1\; \mu\mathrm{F}/\mathrm{cm}^2$ (NEURON default, not overridden); $\mathrm{celsius} =
  32\;\mathrm{^\circ C}$ (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L284`);
  $\mathrm{dt} = 0.1\;\mathrm{ms}$, $t_\mathrm{stop} = 1000\;\mathrm{ms}$, $V_\mathrm{init} =
  -65\;\mathrm{mV}$ (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L282-L285`).
* **Active vs passive default**: the project default is `use_active = 0` (`main.hoc:L36`),
  which inserts only the passive `pas` mechanism on every section. When `use_active = 1` (the
  FULL trial mode of [t0065]), `init_active()` (`main.hoc:L125-L163`, mirrored in
  `dsgc_model.hoc:L114-L152`) inserts `HHst` on the soma and on every dendrite, with the
  per-section densities tabulated below.

### Membrane equation

The Hodgkin-Huxley membrane equation governs each compartment of Bed A:

$$ C_m \frac{dV}{dt} = -\sum_i I_i - I_\mathrm{syn} - I_\mathrm{inj} $$

The active currents $\sum_i I_i$ enumerated for Bed A (taken from `HHst.mod:L190-L222`
`BREAKPOINT` block) are:

$$ I_\mathrm{Na} = g_\mathrm{Na} \cdot m^3 \cdot h \cdot (V - E_\mathrm{Na}) \quad \text{HHst
Na fast} $$

$$ I_\mathrm{Kdr} = g_\mathrm{Kdr} \cdot n^4 \cdot (V - E_\mathrm{K}) \quad \text{HHst K
delayed rectifier} $$

$$ I_\mathrm{Km} = g_\mathrm{Km} \cdot n_m \cdot (V - E_\mathrm{K}) \quad \text{HHst K M-type}
$$

$$ I_\mathrm{leak} = g_\mathrm{leak} \cdot (V - E_\mathrm{leak}) \quad \text{HHst leak (zleak
noise term off)} $$

The `HHst.mod` source also defines $I_\mathrm{CaL} = g_\mathrm{CaL} \cdot l_m^2 \cdot l_h
\cdot (V
- E_\mathrm{Ca})$ and $I_\mathrm{CaT} = g_\mathrm{CaT} \cdot t_m^2 \cdot t_h \cdot (V -
  E_\mathrm{Ca})$ (`HHst.mod:L208-L209`), but Bed A **explicitly zeros** these on every
  section: `init_active()` sets `RGCcaL = 0` and `RGCcaT = 0`
  (`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc:L155-L156`)
  and the `update()` proc writes those zeros into `glbar_HHst` and `gtbar_HHst` for every
  section (`main.hoc:L302-L303`). Bed A therefore has no calcium currents under the project's
  default parameterisation. The synaptic current $I_\mathrm{syn}$ lumps the three
  point-process drives discussed in the "Synaptic excitation" and "Synaptic inhibition"
  subsections below; $I_\mathrm{inj}$ is the optional somatic injection used in some protocols
  (zero in [t0065]'s default trial).

A global voltage shift $\Delta V_\mathrm{shift\_HHst} = -4\;\mathrm{mV}$ (`main.hoc:L91`,
`tasks/t0008_port_modeldb_189347/code/build_cell.py:L312`) is applied to every gating
variable's voltage argument. Reversal potentials are $E_\mathrm{Na} = +60\;\mathrm{mV}$
(`ena`, NEURON ion-style default), $E_\mathrm{K} = -90\;\mathrm{mV}$ (`ek`, NEURON default),
and $E_\mathrm{leak} = -60\;\mathrm{mV}$
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc:L162`).

### Conductance table

Two density rows per channel: `soma` (the single soma section) and `dend` (the 350 dendrite
sections in `use_active = 1` mode). Kinetic equations are taken verbatim from `HHst.mod`;
effective runtime values are the products of `init_active()`'s assignments and
`apply_params()`'s overrides.

| Channel | Gating | V_half_act (mV) | τ_act (ms) | V_half_inact (mV) | τ_inact (ms) | gbar (S/cm²) | E_rev (mV) | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Na (soma) | m³h | from `α=-0.6·vtrap(V+30,-10), β=20·exp(-(V+55)/18)` | `1/(α+β)` | `-44` (`h_inf=1/(1+exp((V+44)/4))`) | `hslow/((1+exp((V+30)/4))+exp(-(V+50)/2)) + hfast`, hslow=100, hfast=0.3 | 0.4 | +60 | `HHst.mod:L249-L266`; gbar from `main.hoc:L148` `RGCsomana` |
| Na (dend) | m³h | (same kinetics as soma) | (same) | (same) | (same) | 2e-4 | +60 | `HHst.mod:L249-L266`; gbar from `main.hoc:L152` `RGCdendna` |
| Kdr (soma) | n⁴ | from `α=-0.02·vtrap(V+40,-10), β=0.4·exp(-(V+50)/80)` | `1/(α+β)` | n/a (no inactivation) | n/a | 0.07 | -90 | `HHst.mod:L294-L297`; gbar from `main.hoc:L149` `RGCsomakv` |
| Kdr (dend) | n⁴ | (same kinetics as soma) | (same) | n/a | n/a | 7e-3 | -90 | `HHst.mod:L294-L297`; gbar from `main.hoc:L153` `RGCdendkv` |
| Km (soma) | nm (linear) | from `α=-0.001/taukm·vtrap(V+30,-9), β=0.001/taukm·vtrap(V+30,9)`; `taukm = 1` | `1/(α+β)` | n/a | n/a | 5e-4 | -90 | `HHst.mod:L70, L315-L318`; gbar from `main.hoc:L150` `RGCsomakm` |
| Km (dend) | nm (linear) | (same kinetics as soma) | (same) | n/a | n/a | 0 | -90 | `HHst.mod:L70, L315-L318`; gbar from `main.hoc:L154` `RGCdendkm` (set to 0) |
| Leak (passive) | n/a | n/a | n/a | n/a | n/a | 5e-5 | -60 | `main.hoc:L161` `RGCgpas = 5e-5` (passive default); `e_pas = -60` `main.hoc:L162` |
| Leak (active) | n/a | n/a | n/a | n/a | n/a | 5.5e-4 | -60 | `main.hoc:L161` `RGCgpas = 5e-5*(1+active*10)`; assigned to `gleak_HHst` per section |
| CaL | lm²lh | -27 (`α=0.055·vtrap(-(V+27),3.8)`) | `1/(α+β)` | -13 (`α=4.57e-4·exp((-13-V)/50)`) | `1/(α+β)` | 0 (zeroed by `init_active`) | E_Ca | `HHst.mod:L326-L334`; zeroed in `main.hoc:L155, L302` |
| CaT | tm²th | -50 (`tm_inf=1/(1+exp(-(V+50)/7.4))`) | `4/(exp((V+25)/20)+exp(-(V+100)/15))` | -78 (`th_inf=1/(1+exp((V+78)/5))`) | `86/(exp((V+46)/4)+exp(-(V+405)/50))` | 0 (zeroed by `init_active`) | E_Ca | `HHst.mod:L355-L360`; zeroed in `main.hoc:L156, L303` |

A global voltage shift $\Delta V_\mathrm{shift\_HHst} = -4\;\mathrm{mV}$ is applied to every
gating variable (`main.hoc:L91`, `tasks/t0008_port_modeldb_189347/code/build_cell.py:L312`
`h.vshift_HHst = V_SHIFT_HHST_MV = -4.0`). The stochastic-noise channel-count term `NF_HHst`
is set to 0
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc:L85`),
so the Linaro–Storace–Giugliano OU noise terms in `HHst.mod` (lines 286-290, 309-313, 322-323,
348-352, 374-378) do not contribute under the project's default driver settings.

### Synaptic excitation (PD vs ND)

![Bed A PD-vs-ND synaptic-conductance schematic — gabaMOD modulation-envelope swap; excitation
symmetric across PD and
ND](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_a_synaptic_diagram.png)

*Figure A2 (illustrative; analytically computed, not a NEURON trace): top row plots g_AMPA,
g_NMDA, and g_GABA × gabaMOD = 0.33 (PD). Bottom row plots the same three traces with g_GABA ×
gabaMOD = 0.99 (ND). The bipolar excitation traces are unchanged between PD and ND because Bed
A's direction-encoding is purely inhibitory-scalar.*

Bed A's excitatory drive is implemented as a single `bipNMDA` POINT_PROCESS combining AMPA and
voltage-dependent NMDA in one mechanism
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/bipolarNMDA.mod`,
161 lines). One `BIPsyn` instance is placed at the midpoint of every ON dendrite (282
instances total) by `RGCmodel.hoc:L11841-L11843`.

#### AMPA component — canonical synaptic-current block

The AMPA conductance is a single-decay state (instantaneous rise on vesicle release,
exponential decay; `bipolarNMDA.mod:L156`) and the current obeys the canonical ohmic form
(`bipolarNMDA.mod:L103`):

$$ I_\mathrm{AMPA}(t,V) = 10^{-3}\,g_\mathrm{AMPA}(t)\,\bigl(V - E_\mathrm{AMPA}\bigr), \qquad
E_\mathrm{AMPA} = 0\;\mathrm{mV} $$

with state-variable evolution and per-release update (`bipolarNMDA.mod:L143, L156`):

$$ \frac{dg_\mathrm{AMPA}}{dt} = -\frac{g_\mathrm{AMPA}}{\tau_\mathrm{AMPA}}, \qquad
\tau_\mathrm{AMPA} = 2.0\;\mathrm{ms} $$

$$ \text{on each release event } k:\quad g_\mathrm{AMPA} \leftarrow g_\mathrm{AMPA} + r_k \,
\bar{g}*\mathrm{AMPA}^\mathrm{single}, \qquad \bar{g}*\mathrm{AMPA}^\mathrm{single} =
0.25\;\mathrm{nS} $$

The factor $10^{-3}$ converts $g_\mathrm{AMPA}$ from nS to µS so that $I$ is in nA when $V$ is
in mV (NEURON convention). $r_k \in \{0,1\}$ is the per-vesicle Bernoulli release outcome from
the release model below.

#### NMDA component — bi-exponential rise/decay × Mg block

The NMDA conductance is the difference of two exponentials gated by a Jahr-Stevens-style Mg
block (`bipolarNMDA.mod:L102, L104`):

$$ g_\mathrm{NMDA}(t,V) = \frac{A(t) - B(t)}{1 + n \cdot
\exp\!\bigl(-\gamma\,V_\mathrm{loc}\bigr)} $$

$$ I_\mathrm{NMDA}(t,V) = 10^{-3}\,g_\mathrm{NMDA}(t,V)\,\bigl(V - E_\mathrm{NMDA}\bigr),
\qquad E_\mathrm{NMDA} = 0\;\mathrm{mV} $$

with $V_\mathrm{loc} = V\,(1 - V_\mathrm{off}) + V_\mathrm{set}\,V_\mathrm{off}$ (so
$V_\mathrm{off} = 0$ uses the postsynaptic voltage; $V_\mathrm{off} = 1$ clamps to
$V_\mathrm{set} = -43\;\mathrm{mV}$ for the deposited voltage-independent NMDA toggle,
`bipolarNMDA.mod:L101`). Bi-exponential state variables (`bipolarNMDA.mod` DERIVATIVE block):

$$ \frac{dA}{dt} = -\frac{A}{\tau_{1,\mathrm{NMDA}}}, \qquad \frac{dB}{dt} =
-\frac{B}{\tau_{2,\mathrm{NMDA}}} $$

$$ \text{on each release event } k:\quad A \leftarrow A + r_k\,\bar
g_\mathrm{NMDA}^\mathrm{single}, \quad B \leftarrow B + r_k\,\bar
g_\mathrm{NMDA}^\mathrm{single} $$

with $\tau_{1,\mathrm{NMDA}} = 60\;\mathrm{ms}$ (decay), $\tau_{2,\mathrm{NMDA}} =
2\;\mathrm{ms}$ (rise), $\bar g_\mathrm{NMDA}^\mathrm{single} = 0.5\;\mathrm{nS}$, $n =
0.30\;\mathrm{mM}^{-1}$, $\gamma = 0.07\;\mathrm{mV}^{-1}$.

#### Vesicular release model (shared by AMPA and NMDA)

Vesicle release is updated every $\Delta t_\mathrm{rel} = 1\;\mathrm{ms}$ (`if (t > t1)`,
`bipolarNMDA.mod:L81`). The presynaptic envelope $V_\mathrm{pre}$ tracks the bar-driven input
$V_\mathrm{inf}$ via a low-pass filter (`bipolarNMDA.mod:L157`):

$$ \frac{dV_\mathrm{pre}}{dt} = \frac{V_\mathrm{inf} - V_\mathrm{pre}}{\tau_V}, \qquad \tau_V
= 30\;\mathrm{/ms}\;\text{(per-ms time constant)} $$

Each release-tick (`bipolarNMDA.mod:L131-L152`), the per-vesicle release probability is set to
$s_\infty = V_\mathrm{pre}/100$, and over the available pool of `numves` vesicles each is
released independently with probability $s_\infty$. The vesicle pool has $\mathrm{maxves} =
10$ and replenishes at rate $\mathrm{newves} = 0.002\;\mathrm{ms}^{-1}$ (project override of
the `bipolarNMDA.mod:L23` default of $0.01\;\mathrm{ms}^{-1}$, set in `main.hoc:L84`
`newves_bipNMDA = 0.002`). Each successful release adds $\bar g_\mathrm{AMPA}^\mathrm{single}$
to $g_\mathrm{AMPA}$ and $\bar g_\mathrm{NMDA}^\mathrm{single}$ to both NMDA bi-exponential
states $A$ and $B$ (`bipolarNMDA.mod:L143-L145`).

#### Effective synaptic parameters at runtime

| Component | Parameter | Value | Units | Source |
| --- | --- | --- | --- | --- |
| AMPA | per-vesicle peak `gAMPAsingle` | 0.25 | nS | `bipolarNMDA.mod:L35` default 0.2 nS, overridden by `main.hoc:L42` `b2gampa = 0.25`; written by `tasks/t0008_port_modeldb_189347/code/build_cell.py:L294` `h.b2gampa = B2GAMPA_NS = 0.25` |
| AMPA | decay `tauAMPA` | 2.0 | ms | `bipolarNMDA.mod:L39` (no rise — instantaneous on vesicle release) |
| AMPA | reversal `e` | 0 | mV | `bipolarNMDA.mod:L42` |
| NMDA | per-vesicle peak `gNMDAsingle` | 0.5 | nS | `bipolarNMDA.mod:L36` default 0.2 nS, overridden by `main.hoc:L43` `b2gnmda = 0.5`; `tasks/t0008_port_modeldb_189347/code/build_cell.py:L295` |
| NMDA | rise `tau2NMDA` | 2.0 | ms | `bipolarNMDA.mod:L38` |
| NMDA | decay `tau1NMDA` | 60.0 | ms | `bipolarNMDA.mod:L37` default 50 ms, overridden by `main.hoc:L86` `tau1NMDA_bipNMDA = 60`; `tasks/t0008_port_modeldb_189347/code/build_cell.py:L313` |
| NMDA | Mg-block `n` | 0.30 | /mM | `bipolarNMDA.mod:L40` default 0.25, overridden by `main.hoc:L82` `n_bipNMDA = 0.3`; `tasks/t0008_port_modeldb_189347/code/build_cell.py:L315` |
| NMDA | Mg-block `gama` | 0.07 | /mV | `bipolarNMDA.mod:L41` default 0.08, overridden by `main.hoc:L83` `gama_bipNMDA = 0.07`; `tasks/t0008_port_modeldb_189347/code/build_cell.py:L316` |
| Vesicle pool | `maxves` | 10 | vesicles | `bipolarNMDA.mod:L22` |
| Vesicle pool | replenishment `newves` | 0.002 | per ms | `bipolarNMDA.mod:L23` default 0.01, overridden by `main.hoc:L84` `newves_bipNMDA = 0.002` |
| Presynaptic filter | `Vtau` | 30 | /ms | `bipolarNMDA.mod:L32`; DERIVATIVE state `Vpre' = (Vinf-Vpre)/Vtau` (`bipolarNMDA.mod:L157`) |

**PD vs ND for excitation**: there is no excitation-side asymmetry in Bed A. The bipolar drive
is identical between PD and ND trials — direction selectivity emerges entirely from the
inhibitory modulation envelope (next subsection). [t0020]'s PD/ND swap protocol holds BIP
synapse coordinates fixed at baseline (asserted in
`tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py`
`_assert_bip_positions_baseline` L109-127) so the only thing changing across PD and ND is the
value of `gabaMOD`.

#### SACexcsyn (cholinergic) — canonical synaptic-current block

A parallel cholinergic SAC pathway is also active: `SACexcsyn` (one per ON dendrite, placed by
`RGCmodel.hoc:L11825`, mechanism `SAC2RGCexc.mod` at
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCexc.mod`).
Its kinetic form is identical to the SACinhibsyn GABA mechanism (single-decay state with
vesicular release):

$$ I_\mathrm{ACh}(t,V) = 10^{-3}\,g_\mathrm{ACh}(t)\,\bigl(V - E_\mathrm{ACh}\bigr), \qquad
E_\mathrm{ACh} = 0\;\mathrm{mV} $$

$$ \frac{dg_\mathrm{ACh}}{dt} = -\frac{g_\mathrm{ACh}}{\tau_\mathrm{ACh}}, \qquad
\tau_\mathrm{ACh} = 3\;\mathrm{ms} $$

$$ \text{on release event } k:\quad g_\mathrm{ACh} \leftarrow g_\mathrm{ACh} + r_k\,\bar
g_\mathrm{ACh}^\mathrm{single}, \qquad \bar g_\mathrm{ACh}^\mathrm{single} = 0.5\;\mathrm{nS}
$$

The release model is the same Bernoulli-over-vesicles structure as `bipNMDA`, with $s_\infty =
V_\mathrm{pre}/100$ and the modulating scalar $\mathrm{achMOD} = 0.25$ multiplied into the
presynaptic envelope (`main.hoc:L47`,
`tasks/t0008_port_modeldb_189347/code/build_cell.py:L299` `h.achMOD = ACH_MOD = 0.25`). The
peak $\bar g_\mathrm{ACh}^\mathrm{single} = 0.5\;\mathrm{nS}$ comes from `s2gach = 0.5`
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc:L46`,
`tasks/t0008_port_modeldb_189347/code/build_cell.py:L297` `h.s2gach = S2GACH_NS = 0.5`); decay
$\tau_\mathrm{ACh} = 3\;\mathrm{ms}$
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCexc.mod:L24`);
reversal $E_\mathrm{ACh} = 0\;\mathrm{mV}$
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCexc.mod:L25`).
The PD/ND-modulating scalar `achMOD = 0.25` is held constant across PD and ND in [t0020],
although [t0065]'s IPSP_PASSIVE mode zeros it
(`tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py:L166` `h.achMOD = ACH_MOD_OFF =
0`).

### Synaptic inhibition (PD vs ND)

Bed A's inhibition is implemented as a single `SACinhib` POINT_PROCESS
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCinhib.mod`,
95 lines). One `SACinhibsyn` instance is placed at the midpoint of every ON dendrite (282
instances total) by
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/RGCmodel.hoc:L11835-L11838`.

#### SACinhibsyn (GABAergic) — canonical synaptic-current block

The conductance is a single-decay state with vesicular release. The current obeys the
canonical ohmic form (`SAC2RGCinhib.mod:L55`):

$$ I_\mathrm{GABA}(t,V) = 10^{-3}\,g_\mathrm{GABA}(t)\,\bigl(V - E_\mathrm{GABA}\bigr), \qquad
E_\mathrm{GABA} = -60\;\mathrm{mV} $$

with state-variable evolution and per-release update (`SAC2RGCinhib.mod:L92, L83`):

$$ \frac{dg_\mathrm{GABA}}{dt} = -\frac{g_\mathrm{GABA}}{\tau_\mathrm{GABA}}, \qquad
\tau_\mathrm{GABA} = 30\;\mathrm{ms} $$

$$ \text{on release event } k:\quad g_\mathrm{GABA} \leftarrow g_\mathrm{GABA} + r_k\,\bar
g_\mathrm{GABA}^\mathrm{single}, \qquad \bar g_\mathrm{GABA}^\mathrm{single} =
0.5\;\mathrm{nS} $$

The release model uses the same Bernoulli-over-vesicles structure as `bipNMDA`, with the
presynaptic envelope $V_\mathrm{pre}$ filtered from $V_\mathrm{inf}$ at $\tau_V =
30\;\mathrm{/ms}$ and per-tick release probability $s_\infty = V_\mathrm{pre}/100$. Direction
selectivity enters via the multiplicative `gabaMOD` scalar applied to $V_\mathrm{inf}$ in
`placeBIP()` (`dsgc_model.hoc:L242-L243`):

$$ \text{mulnoise.fill}\bigl(V_\mathrm{ampT}\!\cdot\!\mathrm{gabaMOD},\,\dots\bigr)
\;\;\Rightarrow\;\; \text{noisevecSACI}[i].\mathrm{mul}(\text{mulnoise}) \;\;\Rightarrow\;\;
\text{SACinhibsyn}[i].V_\mathrm{inf} $$

so a `gabaMOD = 0.99` trial scales $V_\mathrm{inf}$ (and thus $s_\infty$, and thus the
per-vesicle release probability) by ~3× relative to a `gabaMOD = 0.33` trial — the
**per-vesicle peak conductance $\bar g_\mathrm{GABA}^\mathrm{single} = 0.5\;\mathrm{nS}$ is
unchanged across PD and ND**; what changes is how often vesicles release.

#### Effective synaptic parameters at runtime

| Parameter | Value | Units | Source |
| --- | --- | --- | --- |
| Per-vesicle peak `gsingle` | 0.5 | nS | `SAC2RGCinhib.mod:L23` default 0.2 nS, overridden by `main.hoc:L44` `s2ggaba = 0.5`; written by `tasks/t0008_port_modeldb_189347/code/build_cell.py:L296` `h.s2ggaba = S2GGABA_NS = 0.5` |
| Decay `tau` | 30.0 | ms | `SAC2RGCinhib.mod:L24` default 10 ms; the GLOBAL `tau` (mechanism-level, `SAC2RGCinhib.mod:L7`) is overridden by `main.hoc:L90` `tau_SACinhib = 30`, which updates the per-instance `tau` for every `SACinhibsyn` |
| Reversal `e` | -60 | mV | `SAC2RGCinhib.mod:L26` default -65 mV, overridden by `main.hoc:L89` `e_SACinhib = -60`; written by `tasks/t0008_port_modeldb_189347/code/build_cell.py:L314` `h.e_SACinhib = E_SAC_INHIB_MV = -60` |
| Vesicle pool `maxves` | 10 | vesicles | `SAC2RGCinhib.mod:L22` |
| Replenishment `newves` | 0.01 | per ms | `SAC2RGCinhib.mod:L21` (not overridden by [t0008]) |

**Canonical PD/ND values**
(`tasks/t0020_port_modeldb_189347_gabamod/code/constants.py:L37-L38`, encoded in the deposited
`simplerun(1, $2)` HOC convention as $\mathrm{gabaMOD} = 0.33 + 0.66 \cdot \$2$):

| Trial | `gabaMOD` | Effective release-probability scaling |
| --- | --- | --- |
| PD (preferred direction) | 0.33 | weak inhibition; $s_\infty$ envelope ~33 % of peak |
| ND (null direction) | 0.99 | strong inhibition; $s_\infty$ envelope ~99 % of peak (~3× PD) |

[t0020]'s `run_one_trial_gabamod`
(`tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py:L130-L182`) implements the
swap by setting `h.gabaMOD = gabamod_value`, then calling `h("update()")` and
`h("placeBIP()")` so the inhibitory point processes pick up the new modulation envelope
(L154-155). The bar geometry, synapse positions, and per-vesicle conductance peaks are all
held fixed at baseline.

### Differences from the original paper

* **Calcium currents zeroed**: Poleg-Polsky 2016's `HHst.mod` defines L-type and T-type Ca
  conductances (`HHst.mod:L208-L209`, `HHst.mod:L326-L360`) but Bed A explicitly sets `RGCcaL
  = 0` and `RGCcaT = 0` in `init_active`
  (`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc:L155-L156`)
  and writes those zeros into every section in `update()` (`main.hoc:L302-L303`). The paper's
  baseline figures use these currents on; Bed A documents that fact in [t0008]'s
  `code/constants.py:L66-L67` and treats Ca-current re-enablement as a follow-up sweep
  ([t0067]/[t0069] AIS-localised channel sweeps).
* **NMDA decay extended to 60 ms**: the deposited `bipolarNMDA.mod:L37` ships with `tau1NMDA =
  50 ms`; the project overrides this to `tau1NMDA_bipNMDA = 60 ms`
  (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L313` `h.tau1NMDA_bipNMDA =
  TAU1_NMDA_BIP_MS = 60.0`).
* **NMDA Mg-block parameters retuned**: $n$ and $\gamma$ ship as $0.25\;\mathrm{mM}^{-1}$ and
  $0.08\;\mathrm{mV}^{-1}$ (`bipolarNMDA.mod:L40-L41`); both are overridden — $n =
  0.30\;\mathrm{mM}^{-1}$ and $\gamma = 0.07\;\mathrm{mV}^{-1}$
  (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L315-L316`).
* **Stochastic HHst noise disabled**: Bed A uses the stochastic `HHst.mod`
  (Linaro-Storace-Giugliano per-vesicle channel noise), but project drivers set `NF_HHst = 0`
  (`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc:L85`)
  so the noise terms in lines 286-290, 309-313, 322-323, 348-352, 374-378 do not contribute.
  The bed runs deterministically by default.
* **Vesicle replenishment slowed**: `newves_bipNMDA = 0.002` / ms (project) vs `0.01` / ms
  default (`bipolarNMDA.mod:L23`).
* **`use_active = 0` is the project default**: by default only the somatic compartment carries
  HHst and all dendrites are passive
  (`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc:L36,
  L324-L333`). The downstream protocol [t0065] sets `use_active = 1` (FULL mode) or zeros all
  active densities (EPSP_PASSIVE / IPSP_PASSIVE modes) via `h.exptype` and `init_active`'s
  `TTX = 1` branch (`tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py:L184-L194`).

* * *

## Bed B: de Rosenroll 2026 (t0024)

Bed B wraps a subset of the upstream `geoffder/ds-circuit-ei-microarchitecture` repository at
commit `a23f642aa6557a23a51bf76f51e420e8149773fa`, vendored as
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`. The cell
template, kinetics, and morphology are inherited from the same Poleg-Polsky bundled cell as
Bed A, but the active-channel densities are tier-stratified, the HHst variant is the noiseless
deterministic derivative, and the synapse and stimulus models are reimplemented in Python on
top of `Exp2Syn`. The protocol task [t0066] established the canonical bar-direction PD/ND
convention used in the EPSP/IPSP/Vm protocol for this bed.

### Morphology

![Bed B morphology schematic — soma, primary / non-terminal / terminal dendrite tiers, ACh +
GABA markers on terminal
tips](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_b_morphology.png)

*Figure B1 (illustrative; not to scale): the schematic shows the cell as 1 soma + 350
dendrites discretised into three Python-derived tiers: ~10 primary dends (darker green, short)
attached to the soma, ~163 non-terminal mid dends (medium green) bearing no synapses, and ~177
terminal dends (light green) at the leaves bearing one Exp2Syn ACh + one Exp2Syn GABA each.
The diagram does not reproduce the 3D pt3d coordinates from `RGCmodelGD.hoc:L212-L11722` —
refer to the HOC source for the true dendritic geometry.*

The cell uses the same 350-section template as Bed A (the upstream Poleg-Polsky bundled cell
inherited from ModelDB 189347), reimplemented as the stand-alone HOC file `RGCmodelGD.hoc`
(`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/RGCmodelGD.hoc`,
11 830 lines). Key facts:

* **Section count**: 1 soma + 350 `dend[i]` sections (`create soma, dend[350]`,
  `RGCmodelGD.hoc:L12`).
* **Compartment discretisation**: every section has $n_\mathrm{seg} = 1$
  (`RGCmodelGD.hoc:L11818`, identical to Bed A).
* **Per-dendrite diameter**: $\mathrm{diam} = 0.5 + 2.58 \cdot
  \exp\!\left(-(d(0.5)-10)/10\right)$ µm (`RGCmodelGD.hoc:L11814`, byte-identical to Bed A).
* **ON / OFF sort**: the same $z_\mathrm{3d}(n_\mathrm{3d}-1) \geq -0.16 \cdot
  y_\mathrm{3d}(n_\mathrm{3d}-1) + 46$ classifier (`RGCmodelGD.hoc:L11801-L11803`); the ON
  SectionList is built but the synapse-placement loop at `RGCmodelGD.hoc:L11824-L11826` is
  empty (commented as `forsec ON{ //was used to place synapses }`). All synapse placement
  happens in Python.
* **Three Python-derived dendrite tiers**: `_map_tree`
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L140-L168`) walks the
  connectivity graph from the soma and partitions dendrites into `primary_dends` (first-order
  branches off the soma; ~10 sections), `non_terminal_dends` (intermediate; ~163 sections),
  and `terminal_dends` (leaves where synapses land; ~177 sections).
* **Synapse placement**: every terminal dendrite hosts one Exp2Syn ACh and one Exp2Syn GABA,
  attached in `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L189-L226`
  `_setup_synapses`. Total: ~354 point processes per cell.
* **Passive cable**: $R_a = 100\;\Omega\!\cdot\!\mathrm{cm}$ and $c_m =
  1\;\mu\mathrm{F}/\mathrm{cm}^2$ are written explicitly per section by `_configure_soma` and
  `_configure_dends` (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L192-L248`);
  $\mathrm{celsius} = 36.9\;\mathrm{^\circ C}$
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L19` `CELSIUS_DEG_C = 36.9`);
  $\mathrm{dt} = 0.1\;\mathrm{ms}$, $\mathrm{steps\_per\_ms} = 10$, $t_\mathrm{stop} =
  1000\;\mathrm{ms}$, $V_\mathrm{init} = -60\;\mathrm{mV}$
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L20-L24`).
* **Active channels on every section**: unlike Bed A, every section receives `HHst + cad`
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L192-L201` `_configure_soma`,
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L204-L248` `_configure_dends`).

### Membrane equation

The Hodgkin-Huxley membrane equation governs each compartment of Bed B, written in identical
notation to Bed A:

$$ C_m \frac{dV}{dt} = -\sum_i I_i - I_\mathrm{syn} - I_\mathrm{inj} $$

The active currents $\sum_i I_i$ enumerated for Bed B (taken from
`HHst_noiseless.mod:L184-L222` `BREAKPOINT` block) are:

$$ I_\mathrm{Na} = g_\mathrm{Na} \cdot m^3 \cdot h \cdot (V - E_\mathrm{Na}) \quad \text{HHst
Na fast (deterministic)} $$

$$ I_\mathrm{Kdr} = g_\mathrm{Kdr} \cdot n^4 \cdot (V - E_\mathrm{K}) \quad \text{HHst K
delayed rectifier} $$

$$ I_\mathrm{Km} = g_\mathrm{Km} \cdot n_m \cdot (V - E_\mathrm{K}) \quad \text{HHst K M-type}
$$

$$ I_\mathrm{leak} = g_\mathrm{leak} \cdot (V - E_\mathrm{leak}) \quad \text{HHst leak (no
zleak term)} $$

$$ I_\mathrm{CaL} = g_\mathrm{CaL} \cdot l_m^2 \cdot l_h \cdot (V - E_\mathrm{Ca}) \quad
\text{HHst L-type Ca (active by default)} $$

$$ I_\mathrm{CaT} = g_\mathrm{CaT} \cdot t_m^2 \cdot t_h \cdot (V - E_\mathrm{Ca}) \quad
\text{HHst T-type Ca (active by default)} $$

Unlike Bed A, **the Ca currents are at their `HHst_noiseless.mod` PARAMETER defaults** on
every section: $g_\mathrm{lbar} = 3 \times 10^{-4}\;\mathrm{S/cm}^2$ and $g_\mathrm{tbar} = 3
\times 10^{-4}\;\mathrm{S/cm}^2$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod:L57-L58`).
Bed B's `_configure_soma` / `_configure_dends` never write `glbar_HHst` or `gtbar_HHst` to any
section, so the defaults remain in force.

In addition, every section that has `HHst` inserted also has `cad` (calcium-decay shell)
inserted (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L194, L208`):

* $\mathrm{depth} = 0.1\;\mu\mathrm{m}$
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod:L44`)
* $\tau_r = 5\;\mathrm{ms}$
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod:L45`)
* $\mathrm{Ca}_\infty = 2 \times 10^{-4}\;\mathrm{mM}$
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod:L46`)

The total Ca current $i_\mathrm{Ca} = i_l + i_t$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod:L218-L219`)
drives `cai` into the shell, allowing for Ca²⁺-dependent downstream computations even though
no explicit Ca-activated channels are present in the current driver.

Reversal potentials are $E_\mathrm{Na} = +60\;\mathrm{mV}$ (NEURON ion default), $E_\mathrm{K}
= -90\;\mathrm{mV}$ (NEURON ion default), $E_\mathrm{leak} = -60\;\mathrm{mV}$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L42` `E_LEAK_MV = -60.0`), and
$E_\mathrm{Ca} = +132\;\mathrm{mV}$ (`HHst_noiseless.mod:L227` `eca = 132 mV`).

### Conductance table

Four density rows per channel: `soma`, `primary` (first-order dendrites), `non-terminal` (mid
dendrites), `terminal` (leaf dendrites). Density values come from
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L34-L42` (in mS/cm², converted to
S/cm² at the boundary by multiplying by 1e-3) and are written to each section by
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L192-L248`. Kinetic equations are
identical to Bed A (the two `.mod` files share the same gating equations — only the noise
terms differ).

| Channel | Gating | V_half_act (mV) | τ_act (ms) | V_half_inact (mV) | τ_inact (ms) | gbar (S/cm²) | E_rev (mV) | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Na (soma) | m³h | from `α=-0.6·vtrap(V+30,-10), β=20·exp(-(V+55)/18)` | `1/(α+β)` | -44 (`h_inf=1/(1+exp((V+44)/4))`) | `hslow/((1+exp((V+30)/4))+exp(-(V+50)/2)) + hfast`, hslow=100, hfast=0.3 | 0.150 | +60 | `HHst_noiseless.mod:L244-L261`; gbar from `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L34` `GNA_SOMA_MS = 150` |
| Na (primary) | m³h | (same kinetics) | (same) | (same) | (same) | 0.200 | +60 | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L35` `GNA_PRIMARY_MS = 200` |
| Na (non-terminal) | m³h | (same kinetics) | (same) | (same) | (same) | 0 (zeroed) | +60 | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L36` `GNA_NON_TERMINAL_MS = 0` |
| Na (terminal) | m³h | (same kinetics) | (same) | (same) | (same) | 0.030 | +60 | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L37` `GNA_TERMINAL_MS = 30` |
| Kdr (soma) | n⁴ | from `α=-0.02·vtrap(V+40,-10), β=0.4·exp(-(V+50)/80)` | `1/(α+β)` | n/a | n/a | 0.035 | -90 | `HHst_noiseless.mod:L289-L292`; gbar from `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L38` `GK_SOMA_MS = 35` |
| Kdr (primary) | n⁴ | (same kinetics) | (same) | n/a | n/a | 0.035 | -90 | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L39` `GK_PRIMARY_MS = 35` |
| Kdr (non-terminal + terminal) | n⁴ | (same kinetics) | (same) | n/a | n/a | 0.025 | -90 | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L40` `GK_NON_TERMINAL_MS = 25` |
| Km (uniform) | nm (linear) | from `α=-0.001/taukm·vtrap(V+30,-9)`, β symmetric; `taukm = 1` | `1/(α+β)` | n/a | n/a | 0.003 | -90 | `HHst_noiseless.mod:L68, L310-L313`; gbar from `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L41` `GKM_MS = 3` (uniform across all sections) |
| Leak (uniform) | n/a | n/a | n/a | n/a | n/a | 1.667e-4 | -60 | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L195, L210` `seg.HHst.gleak = G_LEAK_MS * 1e-3`; constant `G_LEAK_MS = 0.1667` (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L42`) |
| CaL (uniform) | lm²lh | -27 (`α=0.055·vtrap(-(V+27),3.8)`) | `1/(α+β)` | -13 (`α=4.57e-4·exp((-13-V)/50)`) | `1/(α+β)` | 3e-4 | +132 | `HHst_noiseless.mod:L57, L321-L329`; never overridden — `glbar` stays at PARAMETER default |
| CaT (uniform) | tm²th | -50 (`tm_inf=1/(1+exp(-(V+50)/7.4))`) | `4/(exp((V+25)/20)+exp(-(V+100)/15))` | -78 (`th_inf=1/(1+exp((V+78)/5))`) | `86/(exp((V+46)/4)+exp(-(V+405)/50))` | 3e-4 | +132 | `HHst_noiseless.mod:L58, L350-L355`; never overridden — `gtbar` stays at PARAMETER default |
| `cad` (uniform) | calcium decay | n/a | `taur = 5 ms` | n/a | n/a | n/a | n/a | `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod:L44-L46`; `depth = 0.1 µm`, `cainf = 2e-4 mM` |

Notably, Bed B's `Na` density on the primary dendrites (0.200 S/cm²) is **higher than the
soma** (0.150 S/cm²), and the non-terminal mid dendrites have `Na` zeroed entirely while `Kdr`
remains at 0.025 S/cm². This non-uniform stratification is inherited from upstream
`ei_balance.py` and is documented in [t0024]'s `code/constants.py:L34-L42`.

### Synaptic excitation (PD vs ND)

![Bed B PD-vs-ND synaptic-conductance schematic — bar-direction swap shifts per-synapse
arrival times; sigmoidal release-probability scales GABA between PD and
ND](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_b_synaptic_diagram.png)

*Figure B2 (illustrative; analytically computed, not a NEURON trace): each row sums Exp2Syn
ACh and Exp2Syn GABA traces from 5 representative terminal dendrites placed 25 µm apart along
the bar's velocity axis. Top row = PD (bar 0°, sweeping left→right); bottom row = ND (bar
180°, sweeping right→left). The arrival-time staggering reverses across direction; the GABA
amplitude scales by release probability ~0.05 (PD) vs ~0.80 (ND).*

Bed B's excitatory drive is implemented as the NEURON built-in `Exp2Syn` mechanism for ACh
(the cholinergic SAC drive that survives in the de Rosenroll model). One Exp2Syn ACh instance
is placed on every terminal dendrite (~177 instances) in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L189-L226`
`_setup_synapses`.

#### Exp2Syn ACh — canonical synaptic-current block

NEURON's standard `Exp2Syn` is a normalised bi-exponential mechanism. Its conductance is the
difference of two exponentials with decay $\tau_2$ and rise $\tau_1$, normalised so an event
of NetCon weight 1 produces a peak conductance of 1; the current obeys the ohmic form (NEURON
documentation, identical to the explicit normalisation factor in
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod:L80-L82`):

$$ g_\mathrm{ACh}(t) = f_\mathrm{ACh}\,\bigl(B(t) - A(t)\bigr), \qquad f_\mathrm{ACh} =
\frac{1}{-\exp\!\left(-\frac{t_p}{\tau_1}\right) + \exp\!\left(-\frac{t_p}{\tau_2}\right)},
\qquad t_p = \frac{\tau_1\,\tau_2}{\tau_2 - \tau_1}\ln\!\frac{\tau_2}{\tau_1} $$

$$ I_\mathrm{ACh}(t,V) = g_\mathrm{ACh}(t)\,\bigl(V - E_\mathrm{ACh}\bigr), \qquad
E_\mathrm{ACh} = 0\;\mathrm{mV} $$

with state-variable evolution

$$ \frac{dA}{dt} = -\frac{A}{\tau_{1,\mathrm{ACh}}}, \qquad \frac{dB}{dt} =
-\frac{B}{\tau_{2,\mathrm{ACh}}}, \qquad \tau_{1,\mathrm{ACh}} = 0.1\;\mathrm{ms},\;\;
\tau_{2,\mathrm{ACh}} = 4.0\;\mathrm{ms} $$

$$ \text{on each NetCon event:}\quad A \leftarrow A + w_\mathrm{ACh}, \quad B \leftarrow B +
w_\mathrm{ACh}, \qquad w_\mathrm{ACh} = 0.001\;\mu\mathrm{S} $$

Net effect: each event delivered by `NetCon.event(t)` produces a conductance pulse of peak
amplitude $w_\mathrm{ACh}$ (in µS), so the current is in nA when $V$ is in mV (NEURON's
$g\,(V-E)$ convention already includes the µS-to-nA scaling — no extra $10^{-3}$ factor is
needed unlike `bipolarNMDA.mod` which works in nS internally).

| Parameter | Value | Units | Source |
| --- | --- | --- | --- |
| Rise `tau1` | 0.1 | ms | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L45` `ACH_TAU1_MS = 0.1` |
| Decay `tau2` | 4.0 | ms | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L46` `ACH_TAU2_MS = 4.0` |
| Reversal `e` | 0 | mV | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L47` `ACH_E_MV = 0.0` |
| NetCon weight | 0.001 | µS | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L48` `ACH_WEIGHT_US = 0.001` |
| Per-event release probability `BASE_ACH_PROB` | 0.5 | — | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L54` |

**NMDA is wired but not active**: the library vendors `Exp2NMDA.mod`
(`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`,
103 lines) and the project parameterises NMDA in `code/constants.py:L57-L61` (`NMDA_TAU1_MS =
2.0`, `NMDA_TAU2_MS = 7.0`, `NMDA_E_MV = 0.0`, `NMDA_N_PER_MM = 0.25`, `NMDA_GAMA_PER_MV =
0.08`, `NMDA_WEIGHT_US = 0.0015`), but `_setup_synapses`
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L189-L226`) only creates
ACh and GABA synapses. No driver in the project (neither `run_tuning_curve.py` nor [t0066]'s
`run_protocol.py`) places `Exp2NMDA` instances. The mechanism's Mg-block formula $g = (B - A)
/ \bigl(1 + n \exp(-\gamma\,V_\mathrm{loc})\bigr)$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod:L90`)
is therefore latent in the library, ready for future use but currently unused.

**PD vs ND encoding for excitation: per-synapse arrival times**. The bar moves at
$v_\mathrm{bar} = 1.0\;\mu\mathrm{m/ms}$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L78` `BAR_VELOCITY_UM_PER_MS =
1.0`) with width 250 µm (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L79`
`BAR_WIDTH_UM = 250.0`). For each direction the arrival time at each terminal synapse is
computed by `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L92-L109`
`_bar_arrival_times`:

$$ t_\mathrm{arr}(\mathrm{syn}) = t_\mathrm{bar\_start} +
\frac{\mathrm{proj}*{xy}(\mathrm{syn}) - x*\mathrm{bar\_start}}{v_\mathrm{bar}} $$

where $\mathrm{proj}*{xy}(\mathrm{syn})$ is the dot product of the synapse's offset from the
cell origin with the unit velocity vector. PD = 0° (rightward), ND = 180° (leftward) per
`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/constants.py:L19-L20` `DIRECTION_PD_DEG = 0.0`
and `DIRECTION_ND_DEG = 180.0`. The release rate at each synapse is then a Gaussian envelope
centred on the arrival time ($\sigma*\mathrm{bar} = 30\;\mathrm{ms}$,
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L53`), modulated by an AR(2) noise
process (`_rates_with_ar2_noise`,
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L112-L142`). Spike-event
times are drawn as Poisson counts per $\Delta t_\mathrm{rate} = 1\;\mathrm{ms}$ bin
(`_rates_to_events`,
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L145-L175`) and queued via
`NetCon.event(t)` inside a `FInitializeHandler`
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L286-L298`).

### Synaptic inhibition (PD vs ND)

Bed B's inhibition is also `Exp2Syn`. One Exp2Syn GABA instance is placed on every terminal
dendrite (~177 instances) in `_setup_synapses`
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L199-L202`).

#### Exp2Syn GABA — canonical synaptic-current block

The mechanism is identical in form to Exp2Syn ACh, with reversal at the GABA reversal and
direction-encoding via the per-event Bernoulli release probability $p_\mathrm{rel}(\theta)$
and the AR(2) noise envelope (no ohmic-form change, only the kinetic constants and NetCon
weight differ):

$$ g_\mathrm{GABA}(t) = f_\mathrm{GABA}\,\bigl(B(t) - A(t)\bigr), \qquad f_\mathrm{GABA} =
\frac{1}{-\exp\!\left(-\frac{t_p}{\tau_1}\right) + \exp\!\left(-\frac{t_p}{\tau_2}\right)},
\qquad t_p = \frac{\tau_1\,\tau_2}{\tau_2 - \tau_1}\ln\!\frac{\tau_2}{\tau_1} $$

$$ I_\mathrm{GABA}(t,V) = g_\mathrm{GABA}(t)\,\bigl(V - E_\mathrm{GABA}\bigr), \qquad
E_\mathrm{GABA} = -60\;\mathrm{mV} $$

with state-variable evolution

$$ \frac{dA}{dt} = -\frac{A}{\tau_{1,\mathrm{GABA}}}, \qquad \frac{dB}{dt} =
-\frac{B}{\tau_{2,\mathrm{GABA}}}, \qquad \tau_{1,\mathrm{GABA}} = 0.5\;\mathrm{ms},\;\;
\tau_{2,\mathrm{GABA}} = 12\;\mathrm{ms} $$

and a per-event Bernoulli release driven by the direction-dependent probability:

$$ \text{on each scheduled event } k:\quad \text{release with probability }
p_\mathrm{rel}(\theta);\;\;\text{if released:}\;\; A \leftarrow A + w_\mathrm{GABA},\;\; B
\leftarrow B + w_\mathrm{GABA} $$

with $w_\mathrm{GABA} = 0.003\;\mu\mathrm{S}$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L53`). Driver: see
`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/`. The release-probability sigmoid (next
subsection) defines $p_\mathrm{rel}(\theta)$.

| Parameter | Value | Units | Source |
| --- | --- | --- | --- |
| Rise `tau1` | 0.5 | ms | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L50` `GABA_TAU1_MS = 0.5` |
| Decay `tau2` | 12.0 | ms | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L51` `GABA_TAU2_MS = 12.0` |
| Reversal `e` | -60 | mV | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L52` `GABA_E_MV = -60.0` |
| NetCon weight | 0.003 | µS | `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L53` `GABA_WEIGHT_US = 0.003` |

**PD vs ND encoding for inhibition: two simultaneous mechanisms**.

1. **Sigmoidal release probability as a function of bar direction**
   (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L80-L89`
   `_gaba_prob_for_direction`). The sigmoid is:

$$ p_\mathrm{rel}(d) = p_\mathrm{pref} + (p_\mathrm{null} - p_\mathrm{pref}) \left(1 -
\frac{0.98}{1 \+ \exp\!\left((d - 91)/25\right)}\right) $$

$$ d = \bigl|\theta - \theta_\mathrm{cell\_pref} + 180\bigr|\;\bmod\;180 $$

with $p_\mathrm{pref} = 0.05$, $p_\mathrm{null} = 0.80$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L57`), and
$\theta_\mathrm{cell\_pref} = 0.0\,°$
(`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L54`). PD ⇒ $d \approx 89$
⇒ $p_\mathrm{rel} \approx 0.05$; ND ⇒ $d \approx 1$ ⇒ $p_\mathrm{rel} \approx 0.80$.

2. **Per-synapse arrival times** also shift with direction via `_bar_arrival_times` (same
   mechanism as excitation). This produces a leftward-vs-rightward sweep across the dendritic
   field.

3. **Optional AR(2) cross-channel correlation** between paired ACh and GABA streams
   (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py:L68-L107`
   `generate_ar2_batch`): $\phi = (0.9, -0.1)$
   (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L67` `AR2_PHI = (0.9, -0.1)`);
   the "correlated" condition uses $\rho = 0.6$
   (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L68` `RHO_CORRELATED = 0.6`);
   the "uncorrelated / AMB" condition uses $\rho = 0.0$
   (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L69` `RHO_UNCORRELATED = 0.0`).
   The uncorrelated condition additionally scales the GABA NetCon weight by 1.8×
   (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L54` `GABA_SCALE_UNCORRELATED =
   1.8`, applied in `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L332`).
   [t0066]'s EPSP/IPSP/Vm protocol simplifies this to a fixed-direction protocol with $\rho =
   0.6$ only and no AMB toggle.

### Differences from the original paper

* **NMDA mechanism vendored but not wired**: `Exp2NMDA.mod` is committed and parameterised
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L57-L61`) but no driver places
  `Exp2NMDA` instances. The de Rosenroll 2026 paper's model includes NMDA; the project port
  currently runs without it.
* **Deterministic HHst**: Bed B uses `HHst_noiseless.mod` (the noise-stripped derivative of
  the Linaro stochastic `HHst.mod`); this matches the de Rosenroll upstream choice
  (`HHst_noiseless` is the upstream's preferred variant for production runs).
* **Synaptic-release noise is AR(2) Python-side**: the upstream `ei_balance.py` /
  `SacNetwork.py` Python noise model is reimplemented as a simplified AR(2) Poisson generator
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py:L68-L107`) and queued via
  `NetCon.event(t)` rather than via a presynaptic-voltage vesicle-release model.
* **Calcium currents at default**: the de Rosenroll 2026 paper enables L-Ca and T-Ca
  explicitly; Bed B inherits them from the `HHst_noiseless.mod` PARAMETER defaults
  ($g_\mathrm{lbar} = 3 \times 10^{-4}$, $g_\mathrm{tbar} = 3 \times
  10^{-4}\;\mathrm{S/cm}^2$,
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod:L57-L58`),
  rather than being explicitly set per tier — the project port has not yet codified per-tier
  Ca densities.

* * *

## Side-by-side comparison

| # | Dimension | Bed A (Poleg-Polsky 2016, t0008) | Bed B (de Rosenroll 2026, t0024) |
| --- | --- | --- | --- |
| 1 | Morphology source | Same 350-section template (Poleg-Polsky bundled cell, ModelDB 189347) | Same 350-section template (vendored as `RGCmodelGD.hoc`) |
| 2 | Section count | 1 soma + 350 dends (`RGCmodel.hoc:L14`) | 1 soma + 350 dends (`RGCmodelGD.hoc:L12`) |
| 3 | Dendrite-tier classification | ON (282) vs OFF (68), HOC-side | primary (~10) / non-terminal (~163) / terminal (~177), Python-derived |
| 4 | Synapse placement code | HOC-side (`RGCmodel.hoc:L11825-L11851`) | Python-side (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L189-L226`) |
| 5 | Point processes per cell | 846 (3 per ON dend × 282) | ~354 (2 per terminal × ~177) |
| 6 | HH variant | `HHst.mod` stochastic (Linaro-Storace-Giugliano OU noise; `NF = 0` by default disables it) | `HHst_noiseless.mod` deterministic |
| 7 | Active channels at default | Na + Kdr + Km + leak only; CaL and CaT zeroed by `init_active` (`main.hoc:L155-L156`) | Na + Kdr + Km + leak + CaL + CaT (defaults) + cad shell |
| 8 | Excitation mechanism | `bipNMDA` POINT_PROCESS (AMPA + voltage-dependent NMDA, `bipolarNMDA.mod`) | `Exp2Syn` ACh (`Exp2NMDA.mod` vendored but latent) |
| 9 | NMDA active in driver | Yes (every BIPsyn) | No (Exp2NMDA wired but no instances placed) |
| 10 | Inhibition mechanism | `SACinhib` POINT_PROCESS with vesicular release (`SAC2RGCinhib.mod`) | `Exp2Syn` GABA with Poisson `NetCon.event` queue |
| 11 | GABA reversal `E_GABA` | -60 mV (`main.hoc:L89`) | -60 mV (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L52`) |
| 12 | Per-event GABA peak | `gsingle = 0.5 nS` per vesicle (`main.hoc:L44`, `build_cell.py:L296`) | NetCon weight `0.003 µS` per release event (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L53`) |
| 13 | PD encoding mechanism | `gabaMOD = 0.33` envelope scalar applied in `placeBIP()` (`dsgc_model.hoc:L242`) | `direction_deg = 0°` (rightward sweep) + sigmoidal `p_rel ≈ 0.05` |
| 14 | ND encoding mechanism | `gabaMOD = 0.99` envelope scalar (~3× PD) | `direction_deg = 180°` (leftward sweep) + sigmoidal `p_rel ≈ 0.80` |
| 15 | Release-noise model | Linaro-Storace-Giugliano stochastic HHst per vesicle (off when `NF = 0`) | AR(2) Python-side Poisson with `phi = (0.9, -0.1)`, `rho = 0.6` |
| 16 | Temperature `celsius` | 32 °C (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L284`) | 36.9 °C (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L19`) |
| 17 | Resting `v_init` | -65 mV (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L285`) | -60 mV (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L24`) |
| 18 | Passive cable `Ra` / `cm` | 100 Ω·cm / 1 µF/cm² (`dsgc_model.hoc:L317`; cm at NEURON default) | 100 Ω·cm / 1 µF/cm² (written explicitly per section in `build_cell.py:L192-L248`) |

## Verification

Verificators run during this implementation and their outcomes:

* `verify_task_results t0071_t0070_synaptic_eqs_pdf` — reported in the orchestrator's
  post-implementation step. The Methodology section explicitly notes that `metrics.json` is
  `{}` because no quantitative metrics apply to a documentation-only task; the `## Task
  Requirement Coverage` section (last `##` heading in this document) lists every `REQ-*` from
  `task_description.md` with a `Done` / `Partial` / `Not done` status and concrete evidence.
* `ruff check --fix tasks/t0071_t0070_synaptic_eqs_pdf/code/` — passed.
* `ruff format tasks/t0071_t0070_synaptic_eqs_pdf/code/` — passed (idempotent).
* `mypy -p tasks.t0071_t0070_synaptic_eqs_pdf.code` — passed.
* The Typst compile (`uv run python -m tasks.t0071_t0070_synaptic_eqs_pdf.code.render_pdf`)
  produces `results/results_detailed.pdf` with size > 50 KB (verified by
  `code/render_pdf.py`'s `MIN_PDF_SIZE_BYTES = 50_000` check).
* The four schematic PNGs were copied from [t0070] verbatim (`shutil.copyfile`); sizes match
  the source files: `bed_a_morphology.png` 345 KB, `bed_b_morphology.png` 146 KB,
  `bed_a_synaptic_diagram.png` 150 KB, `bed_b_synaptic_diagram.png` 159 KB.

## Limitations

* **No quantitative metrics**: this is a documentation-only correction task. The four
  registered project metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`) all require simulated AP rates from a
  NEURON tuning-curve sweep. None apply to this writeup. `results/metrics.json` is `{}` by
  design.
* **Schematic figures, not NEURON renderings**: the four PNGs in `results/images/` are
  illustrative axial schematics and analytically computed conductance traces (carried over
  verbatim from [t0070]); they do not reproduce the `RGCmodel.hoc` 3D pt3d coordinates and
  they are not produced by a NEURON simulation. A reader who wants to verify the dendritic
  geometry must consult `RGCmodel.hoc:L212-L11722` and `RGCmodelGD.hoc:L212-L11722` directly.
* **Only the project's default driver settings are documented**: the writeup tabulates
  effective parameter values under the `apply_params` overrides used by [t0008] and the
  canonical `_configure_*` functions used by [t0024]. Variant runs that change `use_active`,
  `NF_HHst`, `Voff`, `RHO_CORRELATED`, or other knobs will see different effective values; the
  writeup notes the location of each override but does not enumerate every variant.
* **`Exp2NMDA` mechanism in Bed B is not documented under realistic conditions**: because no
  driver places `Exp2NMDA` instances, the NMDA Mg-block parameters in
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L57-L61` and the kinetics in
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`
  appear in the writeup as latent specifications rather than as effective runtime values.
* **Approximate dendrite-tier counts in Bed B**: the values `~10 primary`, `~163
  non-terminal`, and `~177 terminal` are the heuristic counts derived from upstream
  `ei_balance.py`. The exact counts depend on the runtime traversal in `_map_tree`
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L140-L168`) and are not
  committed as a constant; future runs may report slightly different counts.
* **Original-paper comparison is partial**: the "Differences from the original paper"
  subsections list only the divergences identified during the research-code stage. A complete
  diff would require parsing the original Poleg-Polsky 2016 and de Rosenroll 2026 paper texts;
  this is out of scope for the current task.

## Files Created

* `tasks/t0071_t0070_synaptic_eqs_pdf/code/paths.py` — Path constants for Typst source and PDF
  output.
* `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` — Typst → PDF compile script with
  size-floor check.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md` — this document, the v2
  writeup superseding [t0070]'s `results/results_detailed.md`.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.typ` — Typst source for the
  PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf` — typeset PDF (compiled
  from the `.typ` source).
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_summary.md` — fresh ~700-word
  presentation-ready abstract pointing at the PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_a_morphology.png` — copied verbatim
  from [t0070] (345 KB).
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_b_morphology.png` — copied verbatim
  from [t0070] (146 KB).
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_a_synaptic_diagram.png` — copied
  verbatim from [t0070] (150 KB).
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/bed_b_synaptic_diagram.png` — copied
  verbatim from [t0070] (159 KB).

## Task Requirement Coverage

The operative task request from `tasks/t0071_t0070_synaptic_eqs_pdf/task_description.md`:

> Supersede [t0070]'s writeup: add the canonical $I_\mathrm{syn} = g_\mathrm{syn}(t,V)\,(V -
> E_\mathrm{syn})$ formula blocks for all 5 synapse mechanisms (Bed A AMPA, NMDA, GABA, ACh; Bed B
> Exp2Syn ACh and GABA), rewrite every equation in LaTeX math syntax, and produce a typeset PDF via
> Typst (single-file pip dep, no LaTeX install).

| ID | Status | Result | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Done | Five synaptic-current equation blocks present and correctly placed: Bed A BIPsyn AMPA, Bed A BIPsyn NMDA (with bi-exponential rise/decay × Mg block), Bed A SACinhibsyn GABA, Bed A SACexcsyn ACh, and Bed B Exp2Syn ACh + Exp2Syn GABA (one block per channel, GABA block notes per-event Bernoulli release). | "Bed A → Synaptic excitation (PD vs ND) → AMPA component", "NMDA component", "SACexcsyn (cholinergic)" subsections; "Bed A → Synaptic inhibition (PD vs ND) → SACinhibsyn (GABAergic)" subsection; "Bed B → Synaptic excitation (PD vs ND) → Exp2Syn ACh" subsection; "Bed B → Synaptic inhibition (PD vs ND) → Exp2Syn GABA" subsection. Each block contains the canonical ohmic form `I = g · (V − E)`, the state-variable evolution, and the discrete release rule, with `code/<file>:L<line>` citations. |
| REQ-2 | Done | The Hodgkin-Huxley membrane equation in each bed is now in LaTeX display-math form `$$C_m \frac{dV}{dt} = -\sum_i I_i - I_\mathrm{syn} - I_\mathrm{inj}$$`. | "Bed A → Membrane equation" and "Bed B → Membrane equation" subsections — both contain the same `$$C_m \frac{dV}{dt} = ...$$` block. |
| REQ-3 | Done | Every equation block in the document is in LaTeX math syntax (`$...$` inline, `$$...$$` display). No fenced `` ```text `` equation blocks remain. | Visual scan of the document shows zero `` ```text `` blocks containing equations; all equation content is wrapped in `$...$` or `$$...$$`. The HH equations, NMDA Mg-block, vesicular release rules, SAC `mulnoise` formula, sigmoidal release-probability formula, AR(2) parameterisation references, and bar arrival-time formula are all in LaTeX math syntax. |
| REQ-4 | Done | A typeset PDF (`results/results_detailed.pdf`) is produced via Typst. The compile script (`code/render_pdf.py`) verifies size > 50 KB; equations render in math fonts with italic Greek, real subscripts/superscripts, and real fractions. | `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf` (size reported by `code/render_pdf.py` and recorded in the orchestrator's step log). |
| REQ-5 | Done | The `typst` Python wheel is listed in `pyproject.toml` `[project] dependencies` (already present at v0.14.8 from a prior task). | `pyproject.toml:L48` `"typst>=0.14.8"`. |
| REQ-6 | Done | All four PNGs from [t0070]'s `results/images/` (`bed_a_morphology.png`, `bed_b_morphology.png`, `bed_a_synaptic_diagram.png`, `bed_b_synaptic_diagram.png`) have been copied verbatim into this task's `results/images/`. | `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/{bed_a_morphology,bed_b_morphology,bed_a_synaptic_diagram,bed_b_synaptic_diagram}.png` — sizes 345 KB / 146 KB / 150 KB / 159 KB respectively, identical to [t0070]'s versions. |
| REQ-7 | Done | `results/results_summary.md` is a fresh ~700-word abstract that names this as the v2 writeup, lists the equation additions, and points the reader at `results_detailed.pdf` (and `.md` / `.typ`). | `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_summary.md`, with mandatory `## Summary`, `## Metrics`, and `## Verification` sections. |
| REQ-8 | Done | Every numeric biophysical parameter cited (gbar, V_half, τ, e_rev, peak conductance, gabaMOD, achMOD, p_pref, p_null, etc.) matches the value in [t0070]'s writeup, with the same `code/<file>:L<line>` citation. | Side-by-side check against `tasks/t0070_writeup_two_model_beds/results/results_detailed.md`: conductance tables in both bed sections preserved verbatim; synaptic parameter tables preserved verbatim; PD/ND `gabaMOD = 0.33 / 0.99` table preserved verbatim; `p_pref = 0.05`, `p_null = 0.80`, `phi = (0.9, -0.1)`, `rho = 0.6`, `BAR_VELOCITY_UM_PER_MS = 1.0`, `BAR_WIDTH_UM = 250.0`, `BAR_SIGMA_MS = 30 ms`, `tau1NMDA = 60`, `tau2NMDA = 2`, `n_bipNMDA = 0.30`, `gama_bipNMDA = 0.07`, `tauAMPA = 2.0`, `gAMPAsingle = 0.25`, `gNMDAsingle = 0.5`, `tau_SACinhib = 30`, `s2ggaba = 0.5`, `e_SACinhib = -60`, `tau_SACexc = 3`, `s2gach = 0.5`, `achMOD = 0.25`, `tau1_ACh = 0.1`, `tau2_ACh = 4.0`, `w_ACh = 0.001 µS`, `tau1_GABA = 0.5`, `tau2_GABA = 12`, `e_GABA = -60`, `w_GABA = 0.003 µS` all unchanged. |
| REQ-9 | Done | A clear top-level `## Note` section (immediately after the YAML frontmatter, before `## Summary`) states this v2 writeup supersedes [t0070]'s `results/results_detailed.md` and explains why. | "Note" section at the top of this document. |
| REQ-10 | Done | A reproducible PDF compile script is committed at `code/render_pdf.py`. The script uses absolute imports of `paths.py`, calls `typst.compile(...)`, and exits non-zero if the PDF is below the 50 KB size floor. | `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` (uses `from tasks.t0071_t0070_synaptic_eqs_pdf.code.paths import ...`, with `MIN_PDF_SIZE_BYTES = 50_000` and a `CompileResult` dataclass). |

</details>
