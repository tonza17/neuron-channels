"""Compile the preliminary-figures slide deck via python-pptx.

One slide per figure plus a placeholder slide for the deferred DSI+PD 2-obj Pareto
panel (t0104 in_progress). Each slide has a title, a centred picture, and a slide
note containing the source-task citation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Inches, Pt

from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth


@dataclass(frozen=True, slots=True)
class SlideSpec:
    title: str
    caption: str
    png_path: Path | None
    note: str
    placeholder: bool = False


def _build_slide_specs() -> list[SlideSpec]:
    return [
        SlideSpec(
            title="Figure 1 -- Hodgkin-Huxley membrane equations (Bed A and Bed B)",
            caption="Canonical HH equation plus per-channel current decompositions.",
            png_path=pth.FIG01_HH_EQUATIONS_PNG,
            note=(
                "Source: tasks/t0070_writeup_two_model_beds/results/results_detailed.md"
                " lines 120-134 (Bed A) and 405-415 (Bed B). Rendered fresh via"
                " matplotlib mathtext."
            ),
        ),
        SlideSpec(
            title="Figure 2a -- Bed A conductance audit (11 rows)",
            caption=(
                "Per-channel gbar, E_rev, V_half_act, tau_m, V_half_inact, tau_h"
                " with code:line provenance."
            ),
            png_path=pth.FIG02_TABLE_BED_A_PNG,
            note=(
                "Source: tasks/t0070_writeup_two_model_beds/results/results_detailed.md"
                " lines 158-169. Bed A driver: t0008 ModelDB 189347."
            ),
        ),
        SlideSpec(
            title="Figure 2b -- Bed B conductance audit (12 rows)",
            caption=(
                "Bed B per-tier conductances (soma / primary / non-terminal /"
                " terminal) plus cad calcium-decay shell."
            ),
            png_path=pth.FIG02_TABLE_BED_B_PNG,
            note=(
                "Source: tasks/t0070_writeup_two_model_beds/results/results_detailed.md"
                " lines 452-465. Bed B driver: t0024 de Rosenroll 2026 port."
            ),
        ),
        SlideSpec(
            title="Figure 3a -- Bed A morphology",
            caption="Bed A radial-fan dendritic schematic (illustrative).",
            png_path=pth.FIG03_BED_A_MORPH_PNG,
            note=(
                "Source: copied verbatim from"
                " tasks/t0070_writeup_two_model_beds/results/images/bed_a_morphology.png."
            ),
        ),
        SlideSpec(
            title="Figure 3b -- Bed B morphology",
            caption="Bed B radial-fan dendritic schematic (illustrative).",
            png_path=pth.FIG03_BED_B_MORPH_PNG,
            note=(
                "Source: copied verbatim from"
                " tasks/t0070_writeup_two_model_beds/results/images/bed_b_morphology.png."
            ),
        ),
        SlideSpec(
            title="Figure 4a -- Bed A two-point polar synaptic (PD vs ND)",
            caption=(
                "Two-point polar of mean peak PSP (mV). Full angular tuning was"
                " not measured for either bed."
            ),
            png_path=pth.FIG04_BED_A_POLAR_PNG,
            note=(
                "Source: tasks/t0046_reproduce_poleg_polsky_2016_exact/results/data/"
                "fig1_psp.csv; mean peak_psp_mv across 4 trial seeds, gnmda_ns=0.5."
            ),
        ),
        SlideSpec(
            title="Figure 4b -- Bed B two-point polar synaptic (PD vs ND)",
            caption=(
                "Two-point polar of mean peak depolarisation (FULL mode). Two-point"
                " treatment because no per-angle CSV exists."
            ),
            png_path=pth.FIG04_BED_B_POLAR_PNG,
            note=(
                "Source: tasks/t0066_t0024_epsp_ipsp_vm_protocol/data/"
                "voltage_traces.csv; peak Vm of FULL-mode traces, mean across trials."
            ),
        ),
        SlideSpec(
            title="Figure 5 -- Somatic Vm three-mode overlays (2x2 bed x direction)",
            caption=(
                "EPSP_PASSIVE, IPSP_PASSIVE (HH off) and FULL (HH on) overlaid for"
                " {Bed A, Bed B} x {PD, ND}."
            ),
            png_path=pth.FIG05_THREE_MODE_PNG,
            note=(
                "Source: tasks/t0065_t0020_epsp_ipsp_vm_protocol/data/"
                "voltage_traces.csv (Bed A) and tasks/t0066_t0024_epsp_ipsp_vm_protocol/"
                "data/voltage_traces.csv (Bed B). Recomposed from raw CSV for unified"
                " axes."
            ),
        ),
        SlideSpec(
            title="Figure 6 -- Channel-introduction effect on DSI",
            caption=(
                "Unified panel combining t0067 soma sweep, t0068 Nav1.6+Kv3 rescue,"
                " and t0069 AIS-localised sweep, shared y-axis."
            ),
            png_path=pth.FIG06_CHANNEL_EFFECT_PNG,
            note=(
                "Sources: tasks/t0067_t0065_soma_channel_addition_sweep/data/"
                "dsi_by_condition.json (16 conditions);"
                " tasks/t0068_t0067_nav16_kv3_coexpression_rescue/data/"
                "dsi_by_condition.json (9 conditions);"
                " tasks/t0069_t0067_ais_localised_channel_sweep/data/"
                "dsi_by_condition.json (16 conditions)."
            ),
        ),
        SlideSpec(
            title="Figure 7 -- Top-5 Pareto cells (3-obj NSGA-II, t0102)",
            caption=(
                "Top-5 cells by joint rank on (DSI, PD-rate, robustness) after"
                " pd_rate_hz >= 5 Hz filter; morphology + two-point polar per cell."
            ),
            png_path=pth.FIG07_TOP5_PARETO_PNG,
            note=(
                "Source: tasks/t0102_seedscale_n4_gen20/results/data/"
                "pareto_front_seed{44,55}.json (60 cells total). Morphology slice"
                " uses vector_68d[54:] per t0100 correction. Polar uses pd_rate_hz"
                " as PD radius and pd_rate_hz*(1-dsi) as ND radius (two-point)."
            ),
        ),
        SlideSpec(
            title="Figure 7b -- DSI + PD 2-obj Pareto (DEFERRED)",
            caption=(
                "Deferred until t0104_nsga2_2obj_dsi_pdrate_3seeds completes."
                " A follow-up suggestion will be recorded for this panel."
            ),
            png_path=None,
            note=(
                "Reason for deferral: t0104 is still in_progress. The follow-up"
                " suggestion is captured in the orchestrator-written"
                " results/suggestions.json. No source data available yet."
            ),
            placeholder=True,
        ),
    ]


def _add_title(*, slide: object, title: str) -> None:
    # Use the slide's title placeholder if present.
    slide_obj = slide
    title_shape = slide_obj.shapes.title  # type: ignore[attr-defined]
    if title_shape is None:
        return
    title_shape.text = title
    for para in title_shape.text_frame.paragraphs:
        for run in para.runs:
            run.font.size = Pt(22)
            run.font.bold = True


def _embed_picture(
    *,
    slide: object,
    png_path: Path,
    slide_width_emu: int,
    slide_height_emu: int,
) -> None:
    # Get natural PNG aspect ratio.
    with Image.open(fp=png_path) as im:
        img_w, img_h = im.size
    aspect: float = img_h / img_w
    # Reserve top margin for title, bottom margin for caption.
    top_margin_emu: int = Inches(1.2).emu
    bottom_margin_emu: int = Inches(0.9).emu
    side_margin_emu: int = Inches(0.4).emu
    available_w_emu: int = slide_width_emu - 2 * side_margin_emu
    available_h_emu: int = slide_height_emu - top_margin_emu - bottom_margin_emu
    width_emu: int = available_w_emu
    height_emu: int = int(width_emu * aspect)
    if height_emu > available_h_emu:
        height_emu = available_h_emu
        width_emu = int(height_emu / aspect)
    left_emu: int = (slide_width_emu - width_emu) // 2
    top_emu: int = top_margin_emu
    slide.shapes.add_picture(  # type: ignore[attr-defined]
        image_file=str(png_path),
        left=Emu(left_emu),
        top=Emu(top_emu),
        width=Emu(width_emu),
        height=Emu(height_emu),
    )


def _add_caption(
    *,
    slide: object,
    caption: str,
    slide_width_emu: int,
    slide_height_emu: int,
) -> None:
    side_margin_emu: int = Inches(0.4).emu
    width_emu: int = slide_width_emu - 2 * side_margin_emu
    height_emu: int = Inches(0.7).emu
    top_emu: int = slide_height_emu - Inches(0.85).emu
    tb = slide.shapes.add_textbox(  # type: ignore[attr-defined]
        left=Emu(side_margin_emu),
        top=Emu(top_emu),
        width=Emu(width_emu),
        height=Emu(height_emu),
    )
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = caption
    for para in tf.paragraphs:
        for run in para.runs:
            run.font.size = Pt(12)
            run.font.italic = True


def _add_placeholder_body(
    *,
    slide: object,
    caption: str,
    slide_width_emu: int,
    slide_height_emu: int,
) -> None:
    side_margin_emu: int = Inches(0.7).emu
    width_emu: int = slide_width_emu - 2 * side_margin_emu
    height_emu: int = Inches(3.0).emu
    top_emu: int = (slide_height_emu - height_emu) // 2
    tb = slide.shapes.add_textbox(  # type: ignore[attr-defined]
        left=Emu(side_margin_emu),
        top=Emu(top_emu),
        width=Emu(width_emu),
        height=Emu(height_emu),
    )
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = caption
    for para in tf.paragraphs:
        for run in para.runs:
            run.font.size = Pt(20)


def _add_slide_note(*, slide: object, note_text: str) -> None:
    notes_slide = slide.notes_slide  # type: ignore[attr-defined]
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = note_text


def build_slide_deck() -> None:
    pth.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(cst.SLIDE_WIDTH_IN)
    prs.slide_height = Inches(cst.SLIDE_HEIGHT_IN)
    # Use layout 5 (title only) when available, else fall back to layout 0.
    layouts = prs.slide_layouts
    title_only_layout = layouts[5] if len(layouts) > 5 else layouts[0]
    assert prs.slide_width is not None, "Presentation slide_width set above"
    assert prs.slide_height is not None, "Presentation slide_height set above"
    slide_width_emu: int = int(prs.slide_width)
    slide_height_emu: int = int(prs.slide_height)
    specs: list[SlideSpec] = _build_slide_specs()
    for spec in specs:
        slide = prs.slides.add_slide(slide_layout=title_only_layout)
        _add_title(slide=slide, title=spec.title)
        if spec.placeholder or spec.png_path is None:
            _add_placeholder_body(
                slide=slide,
                caption=spec.caption,
                slide_width_emu=slide_width_emu,
                slide_height_emu=slide_height_emu,
            )
        else:
            assert spec.png_path.exists(), f"missing PNG: {spec.png_path}"
            _embed_picture(
                slide=slide,
                png_path=spec.png_path,
                slide_width_emu=slide_width_emu,
                slide_height_emu=slide_height_emu,
            )
            _add_caption(
                slide=slide,
                caption=spec.caption,
                slide_width_emu=slide_width_emu,
                slide_height_emu=slide_height_emu,
            )
        _add_slide_note(slide=slide, note_text=spec.note)
    prs.save(file=str(pth.DECK_PPTX))


def smoke_check_deck() -> int:
    prs = Presentation(pptx=str(pth.DECK_PPTX))
    return len(prs.slides)


def main() -> None:
    build_slide_deck()
    n_slides: int = smoke_check_deck()
    print(f"[t0105] wrote {pth.DECK_PPTX} -- {n_slides} slides")


if __name__ == "__main__":
    main()
