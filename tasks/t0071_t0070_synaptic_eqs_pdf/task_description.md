# t0070 v2 — synaptic-current equations + typeset PDF

## Motivation

t0070 produced a research-paper writeup of the project's two DSGC model beds (Bed A: t0008 deposited
Poleg-Polsky 2016; Bed B: t0024 de Rosenroll 2026 port). The writeup is otherwise thorough but it
has two gaps:

1. **Missing canonical synaptic-current equations.** The HH membrane equation is written explicitly
   at the top of each bed's section, and every active conductance is enumerated as
   `Iᵢ = gᵢ · ... · (V − Eᵢ)`. But for synaptic currents (AMPA, NMDA, GABA, ACh in Bed A; Exp2Syn
   ACh and GABA in Bed B) the parameters and kinetics are described in prose and parameter tables
   only — the canonical `I_syn = g_syn(t,V) · (V − E_syn)` blocks are absent. The user explicitly
   noted this gap.
2. **No typeset PDF.** t0070 produced markdown only. The user wants a PDF with proper math
   typesetting (italic Greek, real subscripts/superscripts, real fractions) for use in a written
   report and a presentation.

The corrections specification (`arf/specifications/corrections_specification.md` v3) restricts
formal correction files to asset kinds (suggestion, paper, answer, dataset, library, model,
predictions). It does not cover result documents. So this task is a **semantic** correction
implemented as a new `correction`-type task: t0071's `results/results_detailed.md` is the v2 of the
writeup and supersedes t0070's. Readers should use t0071's version.

## Scope

This task does NOT re-derive any equations or change any biophysical parameter values. Every
parameter cited in t0071 is the same parameter cited in t0070, with the same `code/<file>:<line>`
provenance. The only changes are:

* **Add** the missing synaptic-current equation blocks under each bed's "Synaptic excitation" and
  "Synaptic inhibition" subsections. Five blocks total:
  * Bed A `BIPsyn` AMPA (single-decay; `bipolarNMDA.mod:103, 156`)
  * Bed A `BIPsyn` NMDA (bi-exponential rise/decay × Mg block; `bipolarNMDA.mod:102-104`)
  * Bed A `SACinhibsyn` GABA (single-decay + presynaptic envelope × `gabaMOD`; `SAC2RGCinhib.mod`)
  * Bed A `SACexcsyn` ACh (single-decay + presynaptic envelope × `achMOD`; `SAC2RGCexc.mod`)
  * Bed B Exp2Syn ACh + Exp2Syn GABA (NEURON's standard `Exp2Syn` form, normalised bi-exponential) —
    one block per channel, with the GABA block adding the per-event Bernoulli direction-encoding and
    AR(2) noise envelope from `tasks/t0066_t0024_epsp_ipsp_vm_protocol/`.
* **Rewrite** every equation block (existing HH equations, Mg-block, vesicular release, and the new
  synaptic blocks) in LaTeX math syntax (`$...$` inline, `$$...$$` display) so that Typst (and any
  future pandoc/MathJax/KaTeX renderer) typesets them properly.
* **Produce** `results/results_detailed.pdf` via the Typst compiler (`pip install typst`,
  pure-Python wheel that bundles the Rust binary — no LaTeX install required).
* **Produce** `results/results_detailed.typ` (Typst source) so the PDF is reproducible.
* **Update** `results/results_summary.md` to reference the new PDF and equation additions.

The four schematic PNGs from t0070 (`bed_a_morphology.png`, `bed_b_morphology.png`,
`bed_a_synaptic_diagram.png`, `bed_b_synaptic_diagram.png`) are reused verbatim — copied into this
task's `results/images/` so the v2 document is fully self-contained.

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
5. Run `code/render_pdf.py` to produce `results/results_detailed.pdf`. Verify visually (open the
   PDF, confirm equations render with proper math fonts).
6. Copy the 4 PNGs from t0070 into `results/images/`.
7. Write `results/results_summary.md` referencing the PDF.
8. Standard task closure: metrics.json (`{}`), costs.json, remote_machines_used.json,
   suggestions.json (likely 1-2 suggestions about the PDF pipeline becoming a project library).

## Outputs

* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md` — v2 markdown with all equations
  (HH + 5 new synaptic blocks + existing) in LaTeX math syntax.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.typ` — Typst source.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf` — typeset PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_summary.md` — abstract pointing at the PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/{bed_a,bed_b}_morphology.png` and
  `{bed_a,bed_b}_synaptic_diagram.png` — copied verbatim from t0070.
* `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` — Typst→PDF compile script.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/{metrics,costs,remote_machines_used}.json`
  + `suggestions.json` — standard bookkeeping.

## Compute and budget

* Local Windows workstation. ~$0 external cost. Adds one Python wheel (`typst`).
* Time: ~1.5-2 hours (most of it is the careful equation transcription).

## Dependencies

Only `t0070_writeup_two_model_beds`. The starting point is t0070's `results/results_detailed.md`.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Typst Python wheel not available for Windows / Python 3.13. | `pip install typst` fails. | Install Quarto (`winget install --id Posit.Quarto`) or use `pandoc + tectonic` instead. Document the chosen pipeline in the task. |
| 2 | Typst's math syntax differs subtly from LaTeX (e.g., `dot.c` vs `\cdot`, `op("...")` for multi-letter function names). | PDF compiles but equations look wrong. | Use Typst's own math reference; for any equation that won't render correctly in Typst, fall back to a rendered SVG via matplotlib mathtext and embed as image. |
| 3 | PDF includes the schematic PNGs but Typst can't find them at compile time. | Compile error or missing-image placeholder. | Use absolute paths in the Typst source; verify with a smoke test on one image before adding all four. |
| 4 | The corrections-spec restriction means there's no formal way to mark t0070's writeup as superseded. | Aggregators may still surface t0070 as the canonical writeup. | The user is informed — t0071's results_detailed.md is the new canonical version and t0070 stays as historical record. Add a clear note at the top of t0071's results document. |
| 5 | Equation transcription introduces a numerical error vs t0070. | Manual cross-check against t0070's parameter tables. | Diff t0071 against t0070 on every numerical value before commit; only structural and syntactic changes should differ. |

## Verification criteria

* `results/results_detailed.md` exists with all standard sections per the results specification,
  contains every equation block from t0070 in LaTeX math syntax, and has the 5 new synaptic-current
  equation blocks.
* `results/results_detailed.typ` exists and compiles to PDF without errors.
* `results/results_detailed.pdf` exists, is non-empty, and renders the equations with proper math
  fonts (visual check).
* All standard verificators pass (verify_task_results, verify_task_metrics, verify_suggestions,
  verify_logs, verify_task_complete).

## Task Requirement Checklist

* **REQ-1 (5 synaptic-current equation blocks present)**: BIPsyn AMPA, BIPsyn NMDA, SACinhibsyn
  GABA, SACexcsyn ACh, Exp2Syn ACh+GABA on bed B.
* **REQ-2 (HH equation in LaTeX math)**: each bed's `C_m · dV/dt = -Σ I_i - I_syn - I_inj` block
  converted to `$$C_m \frac{dV}{dt} = ...$$` form.
* **REQ-3 (every equation in LaTeX math syntax)**: no fenced-text equations remain; all are `$...$`
  or `$$...$$`.
* **REQ-4 (Typst PDF rendered)**: `results_detailed.pdf` exists, non-empty, equations visibly
  typeset in math fonts.
* **REQ-5 (typst dep added)**: `typst` listed in `pyproject.toml`.
* **REQ-6 (PNGs preserved)**: 4 PNGs copied from t0070 into `results/images/`.
* **REQ-7 (results_summary.md updated)**: references the new PDF and notes the additions.
* **REQ-8 (every numeric parameter unchanged from t0070)**: structural and syntactic changes only;
  no biophysical value changed.
* **REQ-9 (note in results_detailed.md that this supersedes t0070)**: clear notice in the Summary or
  front-matter.
* **REQ-10 (PDF compile script in code/)**: `code/render_pdf.py` reproducible.
