"""5 morphology anchors for the warm-start population (REQ-4).

Anchor 1: bedb_like      = BEDB_BASE_POINT (anchor 1).
Anchor 2: symmetric      = base with PD-symmetry knobs zeroed.
Anchor 3: pd_asymmetric  = base with soma offset +100 um, field elongation 2x,
                           branch density gradient +0.5, primary branch PD
                           concentration +0.5.
Anchor 4: nd_asymmetric  = exact mirror of pd_asymmetric.
Anchor 5: alt_topology   = base with num_primary_branches=7, max_strahler=5,
                           smaller field (mean_segment_length=15).
"""

from __future__ import annotations

import json
from dataclasses import asdict

import numpy as np
from numpy.typing import NDArray

from tasks.t0090_morphology_generator_diversity_test.code.constants import BEDB_BASE_POINT
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.constants_morphology import ANCHOR_NAMES
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.paths import (
    RESULTS_DATA_DIR,
    ensure_directories,
)

ANCHOR_DEFINITIONS_JSON = RESULTS_DATA_DIR / "anchor_definitions.json"


def _base_dict() -> dict[str, float]:
    return {k: float(v) for k, v in BEDB_BASE_POINT.items()}


def _make_params(*, overrides: dict[str, float], anchor_seed: int) -> MorphologyParams:
    d = _base_dict()
    d.update(overrides)
    d["morph_seed"] = float(anchor_seed)
    return MorphologyParams(
        num_primary_branches=int(round(d["num_primary_branches"])),
        branch_prob_per_um=float(d["branch_prob_per_um"]),
        max_strahler_depth=int(round(d["max_strahler_depth"])),
        mean_branching_angle_deg=float(d["mean_branching_angle_deg"]),
        rall_exponent=float(d["rall_exponent"]),
        soma_offset_pd_um=float(d["soma_offset_pd_um"]),
        field_elongation_pd=float(d["field_elongation_pd"]),
        branch_density_gradient_pd=float(d["branch_density_gradient_pd"]),
        primary_branch_pd_concentration=float(d["primary_branch_pd_concentration"]),
        mean_segment_length_um=float(d["mean_segment_length_um"]),
        soma_diameter_um=float(d["soma_diameter_um"]),
        ais_length_um=float(d["ais_length_um"]),
        morph_seed=int(round(d["morph_seed"])),
        branch_length_cv=float(d["branch_length_cv"]),
    )


def get_anchors() -> dict[str, MorphologyParams]:
    """Return the 5 named anchors as MorphologyParams.

    Per-anchor `morph_seed` is set deterministically (1..5) for reproducibility.
    """
    return {
        "bedb_like": _make_params(overrides={}, anchor_seed=1234),
        "symmetric": _make_params(
            overrides={
                "soma_offset_pd_um": 0.0,
                "field_elongation_pd": 1.0,
                "branch_density_gradient_pd": 0.0,
                "primary_branch_pd_concentration": 0.0,
            },
            anchor_seed=2,
        ),
        "pd_asymmetric": _make_params(
            overrides={
                "soma_offset_pd_um": 100.0,
                "field_elongation_pd": 2.0,
                "branch_density_gradient_pd": 0.5,
                "primary_branch_pd_concentration": 0.5,
            },
            anchor_seed=3,
        ),
        "nd_asymmetric": _make_params(
            overrides={
                "soma_offset_pd_um": -100.0,
                "field_elongation_pd": 2.0,
                "branch_density_gradient_pd": -0.5,
                "primary_branch_pd_concentration": -0.5,
            },
            anchor_seed=4,
        ),
        "alt_topology": _make_params(
            overrides={
                "num_primary_branches": 7.0,
                "max_strahler_depth": 5.0,
                "mean_segment_length_um": 15.0,
            },
            anchor_seed=5,
        ),
    }


def anchor_to_14d_vector(*, anchor: MorphologyParams) -> NDArray[np.float64]:
    """Convert a MorphologyParams to a 14-d float vector in canonical field order."""
    return np.array(
        [
            float(anchor.num_primary_branches),
            float(anchor.branch_prob_per_um),
            float(anchor.max_strahler_depth),
            float(anchor.mean_branching_angle_deg),
            float(anchor.rall_exponent),
            float(anchor.soma_offset_pd_um),
            float(anchor.field_elongation_pd),
            float(anchor.branch_density_gradient_pd),
            float(anchor.primary_branch_pd_concentration),
            float(anchor.mean_segment_length_um),
            float(anchor.soma_diameter_um),
            float(anchor.ais_length_um),
            float(anchor.morph_seed),
            float(anchor.branch_length_cv),
        ],
        dtype=np.float64,
    )


def main() -> None:
    ensure_directories()
    anchors = get_anchors()
    out: dict[str, object] = {
        "n_anchors": len(anchors),
        "anchor_names": list(ANCHOR_NAMES),
        "anchors": [
            {
                "anchor_index": i,
                "anchor_name": name,
                "morphology_params": asdict(p),
                "vector_14d": anchor_to_14d_vector(anchor=p).tolist(),
            }
            for i, (name, p) in enumerate(anchors.items())
        ],
    }
    ANCHOR_DEFINITIONS_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[anchor_definitions] wrote {ANCHOR_DEFINITIONS_JSON} with {len(anchors)} anchors")


if __name__ == "__main__":
    main()
