"""Apply s_Na / s_K scale factors to Na and K conductances after ``apply_parameter_vector``.

Base arm (``SOMA_AIS``): soma and both AIS sections only. ``gbar_nav16t80`` and ``gnabar_HHst``
are multiplied by ``s_na``; ``gbar_kdrt80``, ``gbar_kv3t80``, ``gbar_kv4t80`` and ``gkbar_HHst``
by ``s_k`` (only mechanisms inserted on a section). ``napt80``, ``nart80``, ``kv7t80`` and the
Ca-activated K channels stay fixed. Dendritic arm (``SOMA_AIS_DENDRITE``) additionally applies
the same factors to every dendrite section and scales ``gbar_napt80`` on dendrites by ``s_na``.
"""

from dataclasses import dataclass
from typing import Any

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    HHST_GKBAR,
    HHST_GNABAR,
    K_MECHANISMS,
    NA_DENDRITIC_EXTRA,
    NA_MECHANISMS,
    ScalingArm,
)


@dataclass(frozen=True, slots=True)
class ChannelScales:
    s_na: float
    s_k: float
    arm: ScalingArm = ScalingArm.SOMA_AIS

    def is_identity(self) -> bool:
        return self.s_na == 1.0 and self.s_k == 1.0


@dataclass(frozen=True, slots=True)
class ScaleRecord:
    group: str
    attribute: str
    n_segments: int
    old_sum: float
    new_sum: float


@dataclass(frozen=True, slots=True)
class ScalingReport:
    s_na: float
    s_k: float
    arm: str
    records: list[ScaleRecord]


def _scale_attribute(
    *,
    sections: list[Any],
    group: str,
    attribute: str,
    factor: float,
) -> ScaleRecord | None:
    n_seg: int = 0
    old_sum: float = 0.0
    new_sum: float = 0.0
    for sec in sections:
        for seg in sec:
            if not hasattr(seg, attribute):
                continue
            old: float = float(getattr(seg, attribute))
            new: float = old * factor
            setattr(seg, attribute, new)
            n_seg += 1
            old_sum += old
            new_sum += new
    if n_seg == 0:
        return None
    return ScaleRecord(
        group=group, attribute=attribute, n_segments=n_seg, old_sum=old_sum, new_sum=new_sum
    )


def apply_channel_scales(*, cell: Any, scales: ChannelScales) -> ScalingReport:
    na_attrs: list[str] = [f"gbar_{m}" for m in NA_MECHANISMS] + [HHST_GNABAR]
    k_attrs: list[str] = [f"gbar_{m}" for m in K_MECHANISMS] + [HHST_GKBAR]
    groups: dict[str, list[Any]] = {
        "soma": [cell.soma],
        "ais": [cell.ais_proximal, cell.ais_distal],
    }
    if scales.arm == ScalingArm.SOMA_AIS_DENDRITE:
        groups["dendrites"] = list(cell.all_dends)
    records: list[ScaleRecord] = []
    for group, sections in groups.items():
        for attr in na_attrs:
            rec = _scale_attribute(
                sections=sections, group=group, attribute=attr, factor=scales.s_na
            )
            if rec is not None:
                records.append(rec)
        for attr in k_attrs:
            rec = _scale_attribute(
                sections=sections, group=group, attribute=attr, factor=scales.s_k
            )
            if rec is not None:
                records.append(rec)
    if scales.arm == ScalingArm.SOMA_AIS_DENDRITE:
        for m in NA_DENDRITIC_EXTRA:
            rec = _scale_attribute(
                sections=list(cell.all_dends),
                group="dendrites",
                attribute=f"gbar_{m}",
                factor=scales.s_na,
            )
            if rec is not None:
                records.append(rec)
    return ScalingReport(s_na=scales.s_na, s_k=scales.s_k, arm=str(scales.arm), records=records)


def snapshot_gbars(*, cell: Any) -> dict[str, float]:
    """Sum of every ``gbar_*`` and HHst conductance per (section group, attribute)."""
    out: dict[str, float] = {}
    groups: dict[str, list[Any]] = {
        "soma": [cell.soma],
        "ais": [cell.ais_proximal, cell.ais_distal],
        "dendrites": list(cell.all_dends),
    }
    attrs: list[str] = [f"gbar_{m}" for m in NA_MECHANISMS + NA_DENDRITIC_EXTRA + K_MECHANISMS]
    attrs += [HHST_GNABAR, HHST_GKBAR]
    for group, sections in groups.items():
        for attr in attrs:
            total: float = 0.0
            found: bool = False
            for sec in sections:
                for seg in sec:
                    if hasattr(seg, attr):
                        total += float(getattr(seg, attr))
                        found = True
            if found:
                out[f"{group}:{attr}"] = total
    return out
