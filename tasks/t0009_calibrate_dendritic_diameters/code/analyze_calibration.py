"""Analysis and plots for the t0009 diameter-calibration pipeline.

Reads the source SWC (uniform 0.125 um placeholder) and the calibrated SWC,
computes per-Strahler-order radius / length / surface-area / axial-resistance
statistics, writes two CSVs and ``results/metrics.json``, and emits three
PNGs into ``results/images/``.

Units:
    * Radius, length, x/y/z: micrometres (um).
    * Axial resistance: ohms. ``AXIAL_RESISTIVITY_OHM_CM`` in Ohm*cm is
      multiplied by length converted to cm and divided by cross-sectional
      area converted to cm^2.

Usage::

    uv run python -u -m arf.scripts.utils.run_with_logs \
        --task-id t0009_calibrate_dendritic_diameters -- \
        python -m tasks.t0009_calibrate_dendritic_diameters.code.analyze_calibration
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from math import pi, sqrt

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from tasks.t0009_calibrate_dendritic_diameters.code.constants import (  # noqa: E402
    AXIAL_RESISTIVITY_OHM_CM,
    PNG_DPI,
    ROOT_PARENT_ID,
    TYPE_DENDRITE,
    TYPE_SOMA,
)
from tasks.t0009_calibrate_dendritic_diameters.code.morphology import (  # noqa: E402
    MorphologyGraph,
    build_graph,
)
from tasks.t0009_calibrate_dendritic_diameters.code.paths import (  # noqa: E402
    AXIAL_RES_PNG,
    CALIBRATED_SWC_PATH,
    METRICS_JSON_PATH,
    MORPHOLOGY_METRICS_JSON_PATH,
    PER_BRANCH_AXIAL_CSV,
    PER_ORDER_RADII_CSV,
    RADIUS_DIST_PNG,
    SOMA_PROFILE_PNG,
    SOURCE_SWC_PATH,
)
from tasks.t0009_calibrate_dendritic_diameters.code.swc_io import (  # noqa: E402
    SwcCompartment,
    parse_swc_file,
)

UM_TO_CM: float = 1.0e-4


@dataclass(frozen=True, slots=True)
class CompartmentMetrics:
    compartment_id: int
    type_code: int
    strahler_order: int
    radius_um: float
    length_um: float
    surface_area_um2: float
    axial_resistance_ohm: float


@dataclass(frozen=True, slots=True)
class SummaryTotals:
    total_surface_area_um2: float
    total_dendritic_axial_resistance_ohm: float
    total_dendritic_length_um: float


def _length_from_parent_um(
    *,
    compartment: SwcCompartment,
    compartment_by_id: dict[int, SwcCompartment],
) -> float:
    if compartment.parent_id == ROOT_PARENT_ID:
        return 0.0
    parent = compartment_by_id[compartment.parent_id]
    dx = compartment.x - parent.x
    dy = compartment.y - parent.y
    dz = compartment.z - parent.z
    return sqrt(dx * dx + dy * dy + dz * dz)


def _axial_resistance_ohm(*, radius_um: float, length_um: float) -> float:
    if radius_um <= 0.0 or length_um <= 0.0:
        return 0.0
    radius_cm = radius_um * UM_TO_CM
    length_cm = length_um * UM_TO_CM
    cross_section_cm2 = pi * radius_cm * radius_cm
    return AXIAL_RESISTIVITY_OHM_CM * length_cm / cross_section_cm2


def _compute_compartment_metrics(
    *,
    graph: MorphologyGraph,
) -> list[CompartmentMetrics]:
    records: list[CompartmentMetrics] = []
    for compartment in graph.compartments:
        length = _length_from_parent_um(
            compartment=compartment,
            compartment_by_id=graph.compartment_by_id,
        )
        radius = compartment.radius
        surface = 2.0 * pi * radius * length
        axial = _axial_resistance_ohm(radius_um=radius, length_um=length)
        records.append(
            CompartmentMetrics(
                compartment_id=compartment.compartment_id,
                type_code=compartment.type_code,
                strahler_order=graph.strahler_by_id.get(compartment.compartment_id, 0),
                radius_um=radius,
                length_um=length,
                surface_area_um2=surface,
                axial_resistance_ohm=axial,
            )
        )
    return records


def _metrics_dataframe(*, records: list[CompartmentMetrics]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "compartment_id": pd.array(
                [r.compartment_id for r in records],
                dtype=pd.Int64Dtype(),
            ),
            "type_code": pd.array(
                [r.type_code for r in records],
                dtype=pd.Int8Dtype(),
            ),
            "strahler_order": pd.array(
                [r.strahler_order for r in records],
                dtype=pd.Int8Dtype(),
            ),
            "radius_um": pd.array(
                [r.radius_um for r in records],
                dtype=np.dtype("float64"),
            ),
            "length_um": pd.array(
                [r.length_um for r in records],
                dtype=np.dtype("float64"),
            ),
            "surface_area_um2": pd.array(
                [r.surface_area_um2 for r in records],
                dtype=np.dtype("float64"),
            ),
            "axial_resistance_ohm": pd.array(
                [r.axial_resistance_ohm for r in records],
                dtype=np.dtype("float64"),
            ),
        }
    )


def _compute_totals(*, df: pd.DataFrame) -> SummaryTotals:
    dendrite_df = df[df["type_code"] == TYPE_DENDRITE]
    return SummaryTotals(
        total_surface_area_um2=float(df["surface_area_um2"].sum()),
        total_dendritic_axial_resistance_ohm=float(dendrite_df["axial_resistance_ohm"].sum()),
        total_dendritic_length_um=float(dendrite_df["length_um"].sum()),
    )


def _per_order_table(
    *,
    placeholder_df: pd.DataFrame,
    calibrated_df: pd.DataFrame,
) -> pd.DataFrame:
    def _one(source_name: str, source_df: pd.DataFrame) -> pd.DataFrame:
        dendrite_only = source_df[source_df["type_code"] == TYPE_DENDRITE].copy()
        grouped = (
            dendrite_only.groupby("strahler_order", sort=True)
            .agg(
                n_compartments=("compartment_id", "count"),
                radius_mean_um=("radius_um", "mean"),
                radius_min_um=("radius_um", "min"),
                radius_max_um=("radius_um", "max"),
                total_length_um=("length_um", "sum"),
                total_surface_area_um2=("surface_area_um2", "sum"),
                total_axial_resistance_ohm=("axial_resistance_ohm", "sum"),
            )
            .reset_index()
        )
        grouped["source"] = source_name
        return grouped

    placeholder_table = _one("placeholder", placeholder_df)
    calibrated_table = _one("calibrated", calibrated_df)
    return pd.concat([placeholder_table, calibrated_table], ignore_index=True)


def _find_five_longest_branches(*, graph: MorphologyGraph) -> list[list[int]]:
    """Return the top-5 leaf-to-soma dendritic paths by path distance."""

    leaves: list[int] = []
    for compartment in graph.compartments:
        if compartment.type_code != TYPE_DENDRITE:
            continue
        if len(graph.children_by_parent.get(compartment.compartment_id, [])) == 0:
            leaves.append(compartment.compartment_id)
    leaves.sort(
        key=lambda cid: graph.path_distance_by_id.get(cid, 0.0),
        reverse=True,
    )
    top_leaves = leaves[:5]
    paths: list[list[int]] = []
    for leaf_id in top_leaves:
        path = [leaf_id]
        current_id = leaf_id
        while True:
            compartment = graph.compartment_by_id[current_id]
            parent_id = compartment.parent_id
            if parent_id == ROOT_PARENT_ID:
                break
            parent_compartment = graph.compartment_by_id[parent_id]
            if parent_compartment.type_code == TYPE_SOMA:
                break
            path.append(parent_id)
            current_id = parent_id
        path.reverse()
        paths.append(path)
    return paths


def _branch_dataframe(
    *,
    graph: MorphologyGraph,
    df: pd.DataFrame,
    paths: list[list[int]],
    source_label: str,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    axial_by_id: dict[int, float] = dict(
        zip(
            df["compartment_id"].to_numpy().tolist(),
            df["axial_resistance_ohm"].to_numpy().tolist(),
            strict=True,
        )
    )
    length_by_id: dict[int, float] = dict(
        zip(
            df["compartment_id"].to_numpy().tolist(),
            df["length_um"].to_numpy().tolist(),
            strict=True,
        )
    )
    for path_index, path in enumerate(paths):
        cumulative_axial: float = 0.0
        cumulative_length: float = 0.0
        for compartment_id in path:
            cumulative_axial += axial_by_id.get(compartment_id, 0.0)
            cumulative_length += length_by_id.get(compartment_id, 0.0)
            rows.append(
                {
                    "branch_index": path_index,
                    "compartment_id": compartment_id,
                    "path_distance_um": graph.path_distance_by_id.get(compartment_id, 0.0),
                    "cumulative_length_um": cumulative_length,
                    "cumulative_axial_resistance_ohm": cumulative_axial,
                    "source": source_label,
                }
            )
    return pd.DataFrame(rows)


def _plot_radius_distribution(
    *,
    placeholder_df: pd.DataFrame,
    calibrated_df: pd.DataFrame,
    png_path: str,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, df, title in (
        (axes[0], placeholder_df, "Placeholder (uniform 0.125 um)"),
        (axes[1], calibrated_df, "Calibrated (Poleg-Polsky bins)"),
    ):
        dendrite = df[df["type_code"] == TYPE_DENDRITE]
        orders = sorted(dendrite["strahler_order"].unique().tolist())
        for order in orders:
            subset = dendrite[dendrite["strahler_order"] == order]
            ax.hist(
                subset["radius_um"].to_numpy(),
                bins=40,
                alpha=0.55,
                label=f"order {order} (n={len(subset)})",
            )
        ax.set_xlabel("radius (um)")
        ax.set_title(title)
        ax.set_yscale("log")
        ax.legend(fontsize=8)
    axes[0].set_ylabel("count (log)")
    fig.suptitle("Per-Strahler-order radius distribution: dendrites only")
    fig.tight_layout()
    fig.savefig(png_path, dpi=PNG_DPI)
    plt.close(fig)


def _plot_surface_area_by_order(
    *,
    per_order_df: pd.DataFrame,
    png_path: str,
) -> None:
    placeholder = per_order_df[per_order_df["source"] == "placeholder"]
    calibrated = per_order_df[per_order_df["source"] == "calibrated"]
    orders = sorted(
        set(
            placeholder["strahler_order"].to_numpy().tolist()
            + calibrated["strahler_order"].to_numpy().tolist()
        )
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.4
    placeholder_map = {
        int(row["strahler_order"]): float(row["total_surface_area_um2"])
        for _, row in placeholder.iterrows()
    }
    calibrated_map = {
        int(row["strahler_order"]): float(row["total_surface_area_um2"])
        for _, row in calibrated.iterrows()
    }
    xs = np.arange(len(orders))
    placeholder_vals = [placeholder_map.get(o, 0.0) for o in orders]
    calibrated_vals = [calibrated_map.get(o, 0.0) for o in orders]
    ax.bar(xs - width / 2, placeholder_vals, width=width, label="placeholder")
    ax.bar(xs + width / 2, calibrated_vals, width=width, label="calibrated")
    ax.set_xticks(xs)
    ax.set_xticklabels([str(o) for o in orders])
    ax.set_xlabel("Strahler order (dendrites)")
    ax.set_ylabel("total surface area (um^2)")
    ax.set_title("Total dendritic surface area by Strahler order")
    ax.legend()
    fig.tight_layout()
    fig.savefig(png_path, dpi=PNG_DPI)
    plt.close(fig)


def _plot_radius_vs_path_distance(
    *,
    graph: MorphologyGraph,
    calibrated_df: pd.DataFrame,
    placeholder_df: pd.DataFrame,
    png_path: str,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    dendrite_cal = calibrated_df[calibrated_df["type_code"] == TYPE_DENDRITE]
    dendrite_pla = placeholder_df[placeholder_df["type_code"] == TYPE_DENDRITE]
    path_distance_cal = np.array(
        [
            graph.path_distance_by_id.get(int(compartment_id), 0.0)
            for compartment_id in dendrite_cal["compartment_id"].to_numpy().tolist()
        ]
    )
    path_distance_pla = np.array(
        [
            graph.path_distance_by_id.get(int(compartment_id), 0.0)
            for compartment_id in dendrite_pla["compartment_id"].to_numpy().tolist()
        ]
    )
    ax.scatter(
        path_distance_pla,
        dendrite_pla["radius_um"].to_numpy(),
        s=4,
        alpha=0.3,
        label="placeholder",
    )
    ax.scatter(
        path_distance_cal,
        dendrite_cal["radius_um"].to_numpy(),
        s=4,
        alpha=0.3,
        label="calibrated",
    )
    ax.set_xlabel("path distance from soma (um)")
    ax.set_ylabel("radius (um)")
    ax.set_title("Dendritic radius vs path distance")
    ax.legend()
    fig.tight_layout()
    fig.savefig(png_path, dpi=PNG_DPI)
    plt.close(fig)


def _compute_rin_proxies(
    *,
    graph: MorphologyGraph,
    df: pd.DataFrame,
    top_paths: list[list[int]],
) -> tuple[float | None, float | None]:
    """Return (proximal_rin_ohm, distal_rin_ohm) as cumulative axial sums.

    ``proximal`` is the mean cumulative axial resistance at the first
    dendritic compartment of each top path; ``distal`` is the mean cumulative
    axial resistance at the leaf of each path. These are first-order
    electrotonic proxies and are sensitive to the chosen branch sample.
    """

    axial_by_id: dict[int, float] = dict(
        zip(
            df["compartment_id"].to_numpy().tolist(),
            df["axial_resistance_ohm"].to_numpy().tolist(),
            strict=True,
        )
    )
    proximal_values: list[float] = []
    distal_values: list[float] = []
    for path in top_paths:
        if len(path) == 0:
            continue
        first_axial = axial_by_id.get(path[0], 0.0)
        proximal_values.append(first_axial)
        cumulative: float = 0.0
        for compartment_id in path:
            cumulative += axial_by_id.get(compartment_id, 0.0)
        distal_values.append(cumulative)
    proximal: float | None = None
    distal: float | None = None
    if len(proximal_values) > 0:
        proximal = float(np.mean(proximal_values))
    if len(distal_values) > 0:
        distal = float(np.mean(distal_values))
    return proximal, distal


def analyze() -> dict[str, object]:
    raw_compartments = parse_swc_file(swc_path=SOURCE_SWC_PATH)
    calibrated_compartments = parse_swc_file(swc_path=CALIBRATED_SWC_PATH)
    placeholder_graph = build_graph(compartments=raw_compartments)
    calibrated_graph = build_graph(compartments=calibrated_compartments)
    placeholder_records = _compute_compartment_metrics(graph=placeholder_graph)
    calibrated_records = _compute_compartment_metrics(graph=calibrated_graph)
    placeholder_df = _metrics_dataframe(records=placeholder_records)
    calibrated_df = _metrics_dataframe(records=calibrated_records)
    placeholder_totals = _compute_totals(df=placeholder_df)
    calibrated_totals = _compute_totals(df=calibrated_df)
    per_order_df = _per_order_table(
        placeholder_df=placeholder_df,
        calibrated_df=calibrated_df,
    )
    PER_ORDER_RADII_CSV.parent.mkdir(parents=True, exist_ok=True)
    per_order_df.to_csv(PER_ORDER_RADII_CSV, index=False)
    top_paths = _find_five_longest_branches(graph=calibrated_graph)
    branch_placeholder_df = _branch_dataframe(
        graph=placeholder_graph,
        df=placeholder_df,
        paths=top_paths,
        source_label="placeholder",
    )
    branch_calibrated_df = _branch_dataframe(
        graph=calibrated_graph,
        df=calibrated_df,
        paths=top_paths,
        source_label="calibrated",
    )
    branch_df = pd.concat([branch_placeholder_df, branch_calibrated_df], ignore_index=True)
    branch_df.to_csv(PER_BRANCH_AXIAL_CSV, index=False)
    RADIUS_DIST_PNG.parent.mkdir(parents=True, exist_ok=True)
    _plot_radius_distribution(
        placeholder_df=placeholder_df,
        calibrated_df=calibrated_df,
        png_path=str(RADIUS_DIST_PNG),
    )
    _plot_surface_area_by_order(
        per_order_df=per_order_df,
        png_path=str(AXIAL_RES_PNG),
    )
    _plot_radius_vs_path_distance(
        graph=calibrated_graph,
        calibrated_df=calibrated_df,
        placeholder_df=placeholder_df,
        png_path=str(SOMA_PROFILE_PNG),
    )
    proximal_placeholder, distal_placeholder = _compute_rin_proxies(
        graph=placeholder_graph,
        df=placeholder_df,
        top_paths=top_paths,
    )
    proximal_calibrated, distal_calibrated = _compute_rin_proxies(
        graph=calibrated_graph,
        df=calibrated_df,
        top_paths=top_paths,
    )
    dendrite_cal = calibrated_df[calibrated_df["type_code"] == TYPE_DENDRITE]
    distinct_radii = sorted({round(float(r), 6) for r in dendrite_cal["radius_um"].tolist()})
    # Flatten up to three dendritic bins into scalar fields (terminal/mid/primary).
    # Scalar-only metrics.json is required by the task metrics specification.
    terminal_radius_um: float | None = distinct_radii[0] if len(distinct_radii) >= 1 else None
    primary_radius_um: float | None = distinct_radii[-1] if len(distinct_radii) >= 1 else None
    mid_radius_um: float | None = distinct_radii[1] if len(distinct_radii) >= 3 else None
    soma_cal = calibrated_df[calibrated_df["type_code"] == TYPE_SOMA]
    soma_radius_um: float | None = None
    if len(soma_cal) > 0:
        soma_radius_um = float(soma_cal["radius_um"].mean())
    surface_area_ratio: float | None = None
    if placeholder_totals.total_surface_area_um2 > 0:
        surface_area_ratio = (
            calibrated_totals.total_surface_area_um2 / placeholder_totals.total_surface_area_um2
        )
    axial_resistance_ratio: float | None = None
    if placeholder_totals.total_dendritic_axial_resistance_ohm > 0:
        axial_resistance_ratio = (
            calibrated_totals.total_dendritic_axial_resistance_ohm
            / placeholder_totals.total_dendritic_axial_resistance_ohm
        )
    # Detailed numeric outputs live in MORPHOLOGY_METRICS_JSON_PATH (task-specific
    # artefact consumed by the reporting stage and by downstream biophysical tasks).
    # results/metrics.json is reserved for project-registered metrics in meta/metrics/;
    # none of this task's measurements are registered there, so metrics.json is
    # written as an empty dict per the task metrics specification.
    morphology_metrics: dict[str, object] = {
        "total_surface_area_placeholder_um2": placeholder_totals.total_surface_area_um2,
        "total_surface_area_calibrated_um2": calibrated_totals.total_surface_area_um2,
        "surface_area_ratio": surface_area_ratio,
        "total_dendritic_axial_resistance_placeholder_ohm": (
            placeholder_totals.total_dendritic_axial_resistance_ohm
        ),
        "total_dendritic_axial_resistance_calibrated_ohm": (
            calibrated_totals.total_dendritic_axial_resistance_ohm
        ),
        "axial_resistance_ratio": axial_resistance_ratio,
        "proximal_input_resistance_placeholder_ohm": proximal_placeholder,
        "proximal_input_resistance_calibrated_ohm": proximal_calibrated,
        "distal_input_resistance_placeholder_ohm": distal_placeholder,
        "distal_input_resistance_calibrated_ohm": distal_calibrated,
        "n_distinct_radii_calibrated": len(distinct_radii),
        "terminal_radius_um_calibrated": terminal_radius_um,
        "mid_radius_um_calibrated": mid_radius_um,
        "primary_radius_um_calibrated": primary_radius_um,
        "max_strahler_order": calibrated_graph.max_strahler_order,
        "soma_radius_um": soma_radius_um,
        "total_dendritic_length_um": calibrated_totals.total_dendritic_length_um,
    }
    METRICS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON_PATH.write_text("{}\n", encoding="utf-8")
    MORPHOLOGY_METRICS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    MORPHOLOGY_METRICS_JSON_PATH.write_text(
        json.dumps(morphology_metrics, indent=2) + "\n",
        encoding="utf-8",
    )
    return morphology_metrics


def main() -> int:
    metrics = analyze()
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
