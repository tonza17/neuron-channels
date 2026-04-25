"""Extract per-synapse 3D coordinates and section metadata from the deposited DSGC.

Builds the cell once via t0046's library, runs ``simplerun(exptype=1, direction=0)`` once via
``run_one_trial`` to honour the literal "build cell + simplerun" instruction in the task
description, then iterates over every BIPsyn / SACexcsyn / SACinhibsyn instance pulling the
parent section, the section's 3D centroid, the path distance from soma, and the radial 3D
distance from the soma centroid. Writes the result to ``results/synapse_coordinates.csv``.

The deposited synapse RANGE variables only store ``locx`` / ``locy`` (no z); this script supplies
``z`` from the parent section's 3D-point centroid. With ``forall { nseg=1 }`` (per
RGCmodel.hoc:11824) this is the correct approximation for a single-segment section.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from numpy import dtype as np_dtype
from pandas.api.extensions import ExtensionDtype

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    Direction,
    ExperimentType,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import (
    ensure_neuron_importable,
)
from tasks.t0050_audit_syn_distribution.code import paths
from tasks.t0050_audit_syn_distribution.code.constants import (
    COLUMN_BIP_LOCX_UM,
    COLUMN_BIP_LOCY_UM,
    COLUMN_BIP_Z_UM,
    COLUMN_INDEX,
    COLUMN_PARENT_SECTION_CENTROID_X_UM,
    COLUMN_PARENT_SECTION_CENTROID_Y_UM,
    COLUMN_PARENT_SECTION_CENTROID_Z_UM,
    COLUMN_PARENT_SECTION_LENGTH_UM,
    COLUMN_PARENT_SECTION_NAME,
    COLUMN_PATH_DISTANCE_UM,
    COLUMN_RADIAL_DISTANCE_UM,
    COLUMN_SAC_EXC_LOCX_UM,
    COLUMN_SAC_EXC_LOCY_UM,
    COLUMN_SAC_EXC_Z_UM,
    COLUMN_SAC_INHIB_LOCX_UM,
    COLUMN_SAC_INHIB_LOCY_UM,
    COLUMN_SAC_INHIB_Z_UM,
    EXPECTED_NUMSYN,
)


@dataclass(frozen=True, slots=True)
class SynapseAuditRecord:
    """Per-synapse 3D coordinate snapshot, parent section metadata, and distances."""

    index: int
    bip_locx_um: float
    bip_locy_um: float
    bip_z_um: float
    sac_inhib_locx_um: float
    sac_inhib_locy_um: float
    sac_inhib_z_um: float
    sac_exc_locx_um: float
    sac_exc_locy_um: float
    sac_exc_z_um: float
    parent_section_name: str
    parent_section_length_um: float
    parent_section_centroid_x_um: float
    parent_section_centroid_y_um: float
    parent_section_centroid_z_um: float
    path_distance_um: float
    radial_distance_from_soma_um: float


def section_centroid_3d(*, sec: Any) -> tuple[float, float, float]:
    """Return the average of (x3d, y3d, z3d) over all 3D points of a NEURON section.

    Adapted from ``tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:181-196`` and
    extended to 3D. With ``nseg=1`` (per ``RGCmodel.hoc:11824``) the centroid approximates the
    section's 0.5-segment location.
    """
    n_points: int = int(sec.n3d())
    if n_points == 0:
        return (0.0, 0.0, 0.0)
    x_sum: float = 0.0
    y_sum: float = 0.0
    z_sum: float = 0.0
    for i in range(n_points):
        x_sum += float(sec.x3d(i))
        y_sum += float(sec.y3d(i))
        z_sum += float(sec.z3d(i))
    return (x_sum / n_points, y_sum / n_points, z_sum / n_points)


def soma_centroid_3d(*, h: Any) -> tuple[float, float, float]:
    """Locate the soma section and return its 3D centroid.

    The deposited template names the soma section ``RGC.soma``; ``sec.name()`` returns
    ``"RGC[0].soma"`` (or similar with the template-instance prefix). We match by ending in
    ``.soma`` to avoid false positives from any future ``soma2`` or ``soma_axon``-named sections.
    """
    for sec in h.allsec():
        if sec.name().endswith(".soma"):
            return section_centroid_3d(sec=sec)
    # Fallback: use the template attribute directly.
    return section_centroid_3d(sec=h.RGC.soma)


def build_cell_and_run_simplerun() -> Any:
    """Build the DSGC once and run simplerun(exptype=1, direction=0) exactly once.

    The simplerun call is a side-effect-only invocation (its return value is unused) honouring the
    task description's literal "build cell once + simplerun() call" requirement. Synapse
    ``(locx, locy)`` values are baked in at ``build_dsgc()`` time and are NOT modified by
    ``simplerun()`` — see research/research_code.md.
    """
    ensure_neuron_importable()
    # Deferred import: ensure_neuron_importable may re-exec; importing earlier would break it.
    from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import (  # noqa: PLC0415
        run_one_trial,
    )

    trial = run_one_trial(
        exptype=ExperimentType.CONTROL,
        direction=Direction.PREFERRED,
        trial_seed=1,
        b2gnmda_override=0.5,
    )
    print(
        f"[extract] simplerun completed: peak_psp_mv={trial.peak_psp_mv:.3f}, "
        f"baseline_mean_mv={trial.baseline_mean_mv:.3f}",
        flush=True,
    )

    from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import (  # noqa: PLC0415
        _CELL_STATE,
    )

    h: Any = _CELL_STATE["h"]
    assert int(h.RGC.numsyn) == EXPECTED_NUMSYN, (
        f"h.RGC.numsyn={int(h.RGC.numsyn)} != expected {EXPECTED_NUMSYN}"
    )
    assert int(h.RGC.countON) == EXPECTED_NUMSYN, (
        f"h.RGC.countON={int(h.RGC.countON)} != expected {EXPECTED_NUMSYN}"
    )
    return h


def extract_synapse_audit(*, h: Any) -> list[SynapseAuditRecord]:
    """Extract per-synapse audit records for all 282 synapses.

    Sets path-distance origin once at soma center, then iterates over every synapse index. For
    each index, fetches BIP / SACexc / SACinhib instances, asserts they share the same parent
    section (single-segment placement at 0.5), computes the section centroid, path distance, and
    radial distance from soma.
    """
    soma_xyz: tuple[float, float, float] = soma_centroid_3d(h=h)
    print(
        f"[extract] soma centroid (x,y,z) = "
        f"({soma_xyz[0]:.3f}, {soma_xyz[1]:.3f}, {soma_xyz[2]:.3f}) um",
        flush=True,
    )

    # NEURON Python ``h.distance(seg1, seg2)`` returns the path distance between two segments
    # without relying on the stateful origin. We use this two-segment form throughout for
    # robustness; the legacy ``h.distance(0, seg)`` form also sets a stateful origin but its
    # return value depends on the section position semantics, which can mislead.
    soma_seg: Any = h.RGC.soma(0.5)
    self_distance: float = float(h.distance(soma_seg, soma_seg))
    assert abs(self_distance) < 1e-6, (
        f"h.distance(soma(0.5), soma(0.5)) returned {self_distance} != 0; "
        "two-segment distance form not supported."
    )

    num_synapses: int = int(h.RGC.numsyn)
    records: list[SynapseAuditRecord] = []

    for idx in range(num_synapses):
        bip: Any = h.RGC.BIPsyn[idx]
        sex: Any = h.RGC.SACexcsyn[idx]
        sin: Any = h.RGC.SACinhibsyn[idx]

        bip_seg: Any = bip.get_segment()
        sex_seg: Any = sex.get_segment()
        sin_seg: Any = sin.get_segment()

        bip_sec: Any = bip_seg.sec
        sex_sec: Any = sex_seg.sec
        sin_sec: Any = sin_seg.sec
        # All three channels are placed at 0.5 of the same ON section (RGCmodel.hoc:11839-11857).
        assert bip_sec.name() == sex_sec.name() == sin_sec.name(), (
            f"idx={idx}: parent section name mismatch: "
            f"BIP={bip_sec.name()} SACexc={sex_sec.name()} SACinhib={sin_sec.name()}"
        )

        centroid: tuple[float, float, float] = section_centroid_3d(sec=bip_sec)
        sec_length_um: float = float(bip_sec.L)
        path_um: float = float(h.distance(soma_seg, bip_seg))
        radial_um: float = math.sqrt(
            (centroid[0] - soma_xyz[0]) ** 2
            + (centroid[1] - soma_xyz[1]) ** 2
            + (centroid[2] - soma_xyz[2]) ** 2,
        )

        # Strip the template-instance prefix (e.g., "RGC[0].dend[5]" -> "dend[5]").
        sec_name_clean: str = bip_sec.name().rsplit(".", 1)[-1]

        records.append(
            SynapseAuditRecord(
                index=idx,
                bip_locx_um=float(bip.locx),
                bip_locy_um=float(bip.locy),
                bip_z_um=centroid[2],
                sac_inhib_locx_um=float(sin.locx),
                sac_inhib_locy_um=float(sin.locy),
                sac_inhib_z_um=centroid[2],
                sac_exc_locx_um=float(sex.locx),
                sac_exc_locy_um=float(sex.locy),
                sac_exc_z_um=centroid[2],
                parent_section_name=sec_name_clean,
                parent_section_length_um=sec_length_um,
                parent_section_centroid_x_um=centroid[0],
                parent_section_centroid_y_um=centroid[1],
                parent_section_centroid_z_um=centroid[2],
                path_distance_um=path_um,
                radial_distance_from_soma_um=radial_um,
            ),
        )

    assert len(records) == EXPECTED_NUMSYN, (
        f"extracted {len(records)} records != expected {EXPECTED_NUMSYN}"
    )
    return records


def write_records_csv(*, records: list[SynapseAuditRecord], output_path: Path) -> None:
    """Write the records to a CSV with explicit dtypes for downstream consumers."""
    rows: list[dict[str, Any]] = [asdict(r) for r in records]
    df: pd.DataFrame = pd.DataFrame.from_records(data=rows)

    dtype_spec: dict[str, np_dtype[Any] | ExtensionDtype] = {
        COLUMN_INDEX: pd.UInt32Dtype(),
        COLUMN_BIP_LOCX_UM: np.dtype("float64"),
        COLUMN_BIP_LOCY_UM: np.dtype("float64"),
        COLUMN_BIP_Z_UM: np.dtype("float64"),
        COLUMN_SAC_INHIB_LOCX_UM: np.dtype("float64"),
        COLUMN_SAC_INHIB_LOCY_UM: np.dtype("float64"),
        COLUMN_SAC_INHIB_Z_UM: np.dtype("float64"),
        COLUMN_SAC_EXC_LOCX_UM: np.dtype("float64"),
        COLUMN_SAC_EXC_LOCY_UM: np.dtype("float64"),
        COLUMN_SAC_EXC_Z_UM: np.dtype("float64"),
        COLUMN_PARENT_SECTION_NAME: pd.StringDtype(),
        COLUMN_PARENT_SECTION_LENGTH_UM: np.dtype("float64"),
        COLUMN_PARENT_SECTION_CENTROID_X_UM: np.dtype("float64"),
        COLUMN_PARENT_SECTION_CENTROID_Y_UM: np.dtype("float64"),
        COLUMN_PARENT_SECTION_CENTROID_Z_UM: np.dtype("float64"),
        COLUMN_PATH_DISTANCE_UM: np.dtype("float64"),
        COLUMN_RADIAL_DISTANCE_UM: np.dtype("float64"),
    }
    for col, dt in dtype_spec.items():
        df[col] = df[col].astype(dt)

    df.to_csv(path_or_buf=output_path, index=False)


def main() -> None:
    h: Any = build_cell_and_run_simplerun()
    records: list[SynapseAuditRecord] = extract_synapse_audit(h=h)
    write_records_csv(records=records, output_path=paths.SYNAPSE_COORDINATES_CSV)

    # Validation gate output.
    df_check: pd.DataFrame = pd.read_csv(filepath_or_buffer=paths.SYNAPSE_COORDINATES_CSV)
    print(f"[extract] CSV written to {paths.SYNAPSE_COORDINATES_CSV}", flush=True)
    print(f"[extract] CSV shape: {df_check.shape}", flush=True)
    print("[extract] First 5 rows:", flush=True)
    print(df_check.head().to_string(), flush=True)
    print(
        "[extract] 282 synapses extracted; "
        "BIP/SACexc/SACinhib parent sections match for all indices",
        flush=True,
    )


if __name__ == "__main__":
    main()
