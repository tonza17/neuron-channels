"""Write a morphology swap report comparing bundled vs calibrated SWC.

The ModelDB 189347 archive ships ``RGCmodel.hoc`` with an explicit
``topol()`` proc that constructs 1 soma + 350 dend sections via
``create soma, dend[350]`` and sets each ``pt3dclear()``/``pt3dadd()``
block inline. This is very different from the dendritic-tree SWC produced
by t0009 (6,736 compartments, Horton-Strahler calibrated). Rather than
risking a partially-coupled hybrid that violates the paper's synapse
placement logic (``RGCmodel.hoc`` relies on ``countON`` being derived
from the bundled z/y cut), the implementation stops at reporting the
comparison rather than fully swapping the morphology. This is the
"compare, don't silently hybridize" option flagged in the plan.

Outputs ``data/morphology_swap_report.md``.
"""

from __future__ import annotations

import sys

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    build_dsgc,
    get_cell_summary,
    read_synapse_coords,
)
from tasks.t0008_port_modeldb_189347.code.constants import (
    BUNDLED_NUM_DEND,
    BUNDLED_NUM_SOMA,
)
from tasks.t0008_port_modeldb_189347.code.paths import (
    CALIBRATED_SWC_PATH,
    DATA_DIR,
    MORPHOLOGY_SWAP_REPORT,
)
from tasks.t0008_port_modeldb_189347.code.swc_io import (
    parse_swc_file,
    summarize,
)


def _bbox(values: list[float]) -> tuple[float, float]:
    return (min(values), max(values))


def main() -> int:
    print("Building bundled DSGC to read its morphology...", flush=True)
    h = build_dsgc()
    summary = get_cell_summary(h=h)
    coords = read_synapse_coords(h=h)

    bip_xs = [c.bip_locx_um for c in coords]
    bip_ys = [c.bip_locy_um for c in coords]
    bip_x_min, bip_x_max = _bbox(bip_xs)
    bip_y_min, bip_y_max = _bbox(bip_ys)

    # Sum 3D lengths of bundled morphology by walking sections.
    bundled_total_length_um = 0.0
    bundled_num_segments = 0
    bundled_soma_diam_um: float | None = None
    for sec in h.allsec():
        bundled_total_length_um += float(sec.L)
        bundled_num_segments += int(sec.nseg)
        if sec.hname().endswith(".soma"):
            bundled_soma_diam_um = float(sec(0.5).diam)

    print(f"  bundled sections: {summary.num_soma_sections + summary.num_dend_sections}")
    print(f"  bundled total cable length: {bundled_total_length_um:.1f} um")
    print(f"  bundled countON={summary.num_on_sections}, numsyn={summary.num_synapses}")
    print(f"  synapse BIP x range: [{bip_x_min:.1f}, {bip_x_max:.1f}] um")
    print(f"  synapse BIP y range: [{bip_y_min:.1f}, {bip_y_max:.1f}] um")

    print("Reading calibrated SWC...", flush=True)
    if not CALIBRATED_SWC_PATH.exists():
        print(f"ERROR: calibrated SWC missing at {CALIBRATED_SWC_PATH}")
        return 1
    swc_compartments = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    swc_summary = summarize(compartments=swc_compartments)
    swc_radii = [c.radius for c in swc_compartments]
    swc_min_diam = 2.0 * min(swc_radii)
    swc_max_diam = 2.0 * max(swc_radii)
    swc_mean_diam = 2.0 * (sum(swc_radii) / len(swc_radii))
    print(f"  calibrated SWC compartments: {swc_summary.total_compartments}")
    print(f"  calibrated SWC diameter range: [{swc_min_diam:.3f}, {swc_max_diam:.3f}] um")

    # Write report.
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    report_lines: list[str] = [
        "# Morphology Swap Report: Bundled vs Calibrated DSGC",
        "",
        "## Context",
        "",
        "ModelDB 189347 ships `RGCmodel.hoc` with a fixed topology:",
        f"{BUNDLED_NUM_SOMA} soma + {BUNDLED_NUM_DEND} dend sections built via",
        "inline `pt3dadd()` blocks. Synapses are placed on ON-compartments",
        "(identified by the cut `z >= -0.16*y + 46`) with one BIP/SACinhib/",
        "SACexc point process per ON dendrite.",
        "",
        "t0009 produced a Horton-Strahler calibrated SWC of a different",
        "DSGC (141009_Pair1DSGC) with full compartmentalization. Importing",
        "this SWC into `RGCmodel.hoc` wholesale would require either:",
        "",
        "1. Stripping the bundled `create soma, dend[350]` block and its",
        "   inline 3D geometry (all ~11800 lines of it) and replacing it",
        "   with a SWC loader — but the paper's synapse placement relies",
        "   on `x3d(0..1)`/`y3d(0..1)`/`z3d(n3d()-1)` indices that assume",
        "   the bundled section ordering.",
        "2. Or keeping the bundled HOC topology and treating the calibrated",
        "   SWC as data-for-comparison only.",
        "",
        "This task chose option 2: the tuning-curve sweep runs on the",
        "bundled morphology for fidelity to the paper, and we compare the",
        "calibrated SWC here for future work (a deeper port that rebuilds",
        "`RGCmodel.hoc` around a calibrated morphology is out of scope).",
        "",
        "## Bundled Morphology (Poleg-Polsky 2016)",
        "",
        "| Metric                         | Value              |",
        "| ------------------------------ | ------------------ |",
        f"| Soma sections                  | {summary.num_soma_sections} |",
        f"| Dend sections                  | {summary.num_dend_sections} |",
        f"| Total sections                 | {summary.num_soma_sections + summary.num_dend_sections} |",  # noqa: E501
        f"| Total segments (nseg sum)      | {bundled_num_segments} |",
        f"| Total cable length (um)        | {bundled_total_length_um:.1f} |",
        f"| Soma diameter at 0.5 (um)      | {bundled_soma_diam_um if bundled_soma_diam_um is not None else 'n/a'} |",  # noqa: E501
        f"| ON sections (countON)          | {summary.num_on_sections} |",
        f"| Synapses per type (numsyn)     | {summary.num_synapses} |",
        f"| Synapse locx range (um)        | [{bip_x_min:.1f}, {bip_x_max:.1f}] |",
        f"| Synapse locy range (um)        | [{bip_y_min:.1f}, {bip_y_max:.1f}] |",
        "",
        "The synapse locx/locy values are used verbatim by `placeBIP()` to",
        "compute per-synapse arrival times of the drifting bar.",
        "",
        "## Calibrated SWC (t0009 Horton-Strahler)",
        "",
        "| Metric                         | Value              |",
        "| ------------------------------ | ------------------ |",
        f"| Compartments                   | {swc_summary.total_compartments} |",
        f"| Soma compartments              | {swc_summary.soma_compartments} |",
        f"| Dendritic compartments         | {swc_summary.dendrite_compartments} |",
        f"| Dendritic cable length (um)    | {swc_summary.total_dendritic_length_um:.1f} |",
        f"| Min diameter (um)              | {swc_min_diam:.3f} |",
        f"| Max diameter (um)              | {swc_max_diam:.3f} |",
        f"| Mean diameter (um)             | {swc_mean_diam:.3f} |",
        "",
        "## Decision",
        "",
        "The tuning-curve sweep in this task runs on the bundled Poleg-",
        "Polsky morphology because:",
        "",
        "* the paper's ON/OFF cut and synapse-per-dendrite logic are",
        "  tightly coupled to the bundled section ordering and 3D layout;",
        "* the envelope targets (DSI 0.70-0.85, peak 40-80 Hz, null <10 Hz,",
        "  HWHM 60-90 deg) were derived from the bundled morphology, so",
        "  swapping it would need a re-derivation;",
        "* a full rebuild of RGCmodel.hoc around a calibrated SWC is a",
        "  separate task (suggestion in `results/suggestions.json`).",
        "",
        "The calibrated SWC stays in t0009 and remains available for the",
        "next iteration.",
        "",
    ]
    MORPHOLOGY_SWAP_REPORT.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )
    print(f"Wrote {MORPHOLOGY_SWAP_REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
