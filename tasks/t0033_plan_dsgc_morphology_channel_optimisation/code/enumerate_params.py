"""Enumerate morphology, lumped HHst, and top-10 VGC parameters for the plan.

This script emits three JSON tables describing the free-parameter layout of
the future joint DSGC morphology + top-10 VGC DSI-maximisation optimiser:

* ``morphology_params.json`` — Poleg-Polsky 2026 backbone + Cuntz 2010 scalars.
* ``channel_params_hhst.json`` — the 16 lumped-HHst gbar parameters already
  instantiated by the t0024 port.
* ``top10_vgcs.json`` — the canonical top-10 VGC list synthesised from the
  t0019 answer asset and the t0022 research_internet.md channel-density
  table.

No NEURON calls. Pure text reads + hard-coded lists drawn from
``research_code.md`` and ``research_papers.md``.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code import paths
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.constants import (
    DEND_TIER_NONTERMINAL,
    DEND_TIER_PRIMARY,
    DEND_TIER_TERMINAL,
    N_FREE_PARAMS_RICH,
    N_FREE_PARAMS_TIGHT,
    REGION_AIS_DIST,
    REGION_AIS_PROX,
    REGION_DEND,
    REGION_SOMA,
)


@dataclass(frozen=True, slots=True)
class MorphologyParam:
    name: str
    scope: str
    default_value: float | None
    units: str
    is_free: bool
    source: str
    notes: str


@dataclass(frozen=True, slots=True)
class ChannelParam:
    name: str
    region: str
    tier: str | None
    default_value: float
    units: str
    is_free: bool
    source: str
    notes: str


@dataclass(frozen=True, slots=True)
class VGCRecord:
    rank: int
    channel: str
    primary_region: str
    secondary_region: str | None
    free_params_gbar_only: int
    free_params_gbar_plus_vhalf: int
    free_params_per_region_gbar: int
    citation: str
    notes: str


# ---------------------------------------------------------------------------
# Hard-coded baselines (from research_code.md and research_papers.md).
# ---------------------------------------------------------------------------


BASELINE_HHST_PARAMS: list[ChannelParam] = [
    # Soma — from tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py
    ChannelParam(
        name="gNa_HHst",
        region=REGION_SOMA,
        tier=None,
        default_value=0.150,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="HHst soma Nav (lumped) gbar",
    ),
    ChannelParam(
        name="gKdr_HHst",
        region=REGION_SOMA,
        tier=None,
        default_value=0.035,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="HHst soma Kdr (lumped)",
    ),
    ChannelParam(
        name="gKm_HHst",
        region=REGION_SOMA,
        tier=None,
        default_value=0.003,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="HHst soma Km (lumped)",
    ),
    ChannelParam(
        name="gleak_HHst",
        region=REGION_SOMA,
        tier=None,
        default_value=1.667e-4,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="HHst soma leak",
    ),
    # Primary dendrite
    ChannelParam(
        name="gNa_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_PRIMARY,
        default_value=0.200,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Primary-dendrite Nav gbar",
    ),
    ChannelParam(
        name="gKdr_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_PRIMARY,
        default_value=0.035,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Primary-dendrite Kdr",
    ),
    ChannelParam(
        name="gKm_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_PRIMARY,
        default_value=0.003,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Primary-dendrite Km",
    ),
    ChannelParam(
        name="gleak_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_PRIMARY,
        default_value=1.667e-4,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Primary-dendrite leak",
    ),
    # Non-terminal dendrite
    ChannelParam(
        name="gNa_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_NONTERMINAL,
        default_value=0.0,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Non-terminal dend Nav (zeroed in baseline)",
    ),
    ChannelParam(
        name="gKdr_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_NONTERMINAL,
        default_value=0.025,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Non-terminal dend Kdr",
    ),
    ChannelParam(
        name="gKm_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_NONTERMINAL,
        default_value=0.003,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Non-terminal dend Km",
    ),
    ChannelParam(
        name="gleak_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_NONTERMINAL,
        default_value=1.667e-4,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Non-terminal dend leak",
    ),
    # Terminal dendrite
    ChannelParam(
        name="gNa_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_TERMINAL,
        default_value=0.030,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Terminal-dend Nav gbar",
    ),
    ChannelParam(
        name="gKdr_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_TERMINAL,
        default_value=0.025,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Terminal-dend Kdr",
    ),
    ChannelParam(
        name="gKm_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_TERMINAL,
        default_value=0.003,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Terminal-dend Km",
    ),
    ChannelParam(
        name="gleak_HHst",
        region=REGION_DEND,
        tier=DEND_TIER_TERMINAL,
        default_value=1.667e-4,
        units="S/cm^2",
        is_free=True,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Terminal-dend leak",
    ),
]


BASELINE_MORPHOLOGY_PARAMS: list[MorphologyParam] = [
    # Fixed morphology knobs from the Poleg-Polsky 2026 backbone (t0024 port)
    # — carried as fixed inputs, not free.
    MorphologyParam(
        name="Ra",
        scope="global",
        default_value=100.0,
        units="ohm.cm",
        is_free=False,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Axial resistivity, fixed",
    ),
    MorphologyParam(
        name="cm",
        scope="global",
        default_value=1.0,
        units="uF/cm^2",
        is_free=False,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Specific capacitance, fixed",
    ),
    MorphologyParam(
        name="d_lambda",
        scope="global",
        default_value=0.1,
        units="unitless",
        is_free=False,
        source="Mainen1996,Schachter2010",
        notes="Discretisation floor; never relaxed to accelerate",
    ),
    MorphologyParam(
        name="celsius",
        scope="global",
        default_value=36.9,
        units="degC",
        is_free=False,
        source="t0024_port_de_rosenroll_2026_dsgc",
        notes="Simulation temperature, fixed",
    ),
    # Cuntz 2010 morphology scalars — free.
    MorphologyParam(
        name="spanning_volume",
        scope="Cuntz2010",
        default_value=None,
        units="um^3",
        is_free=True,
        source="Cuntz2010,t0027_literature_survey_morphology_ds_modeling",
        notes="Cuntz scalar #1: target spanning volume",
    ),
    MorphologyParam(
        name="carrier_point_density",
        scope="Cuntz2010",
        default_value=None,
        units="pts/um^3",
        is_free=True,
        source="Cuntz2010,t0027_literature_survey_morphology_ds_modeling",
        notes="Cuntz scalar #2: carrier point density",
    ),
    MorphologyParam(
        name="bf",
        scope="Cuntz2010",
        default_value=0.5,
        units="unitless",
        is_free=True,
        source="Cuntz2010",
        notes=(
            "Cuntz scalar #3: balancing factor in [0.2, 0.7]; monotonic "
            "control over electrotonic compartmentalisation"
        ),
    ),
    MorphologyParam(
        name="root_location",
        scope="Cuntz2010",
        default_value=None,
        units="categorical",
        is_free=True,
        source="Cuntz2010,t0027_literature_survey_morphology_ds_modeling",
        notes="Cuntz scalar #4: root position (soma / offset)",
    ),
    MorphologyParam(
        name="taper_tweak",
        scope="Cuntz2010",
        default_value=None,
        units="unitless",
        is_free=True,
        source="Cuntz2010",
        notes="Cuntz scalar #5: optional diameter-taper tweak over Rall's 3/2",
    ),
]


# Canonical top-10 VGCs — synthesised from t0019 full_answer.md + t0022
# research_internet.md channel-density table. See research_code.md
# "Top-10 VGC Selection from t0019".
TOP10_VGCS: list[VGCRecord] = [
    VGCRecord(
        rank=1,
        channel="Nav1.6",
        primary_region=REGION_AIS_DIST,
        secondary_region=REGION_SOMA,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=2,
        free_params_per_region_gbar=2,
        citation="Hu2009,Kole2008,VanWart2006",
        notes="Distal AIS initiator, V_half ~ -45 mV, gbar 2500-5000 pS/um^2",
    ),
    VGCRecord(
        rank=2,
        channel="Nav1.2",
        primary_region=REGION_AIS_PROX,
        secondary_region=None,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=2,
        free_params_per_region_gbar=1,
        citation="VanWart2006,Hu2009",
        notes="Proximal AIS, V_half ~ -32 mV, ~50x less than Nav1.6",
    ),
    VGCRecord(
        rank=3,
        channel="Nav_HHst_dend",
        primary_region=REGION_DEND,
        secondary_region=None,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=1,
        free_params_per_region_gbar=3,
        citation="PolegPolsky2026,Schachter2010",
        notes="Dendritic lumped Nav; split by primary/non-terminal/terminal tier",
    ),
    VGCRecord(
        rank=4,
        channel="Kdr_HHst",
        primary_region=REGION_SOMA,
        secondary_region=REGION_DEND,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=2,
        free_params_per_region_gbar=4,
        citation="FohlmeisterMiller1997,PolegPolsky2026",
        notes="Delayed rectifier K+ lumped HHst; soma + 3 dend tiers",
    ),
    VGCRecord(
        rank=5,
        channel="Kv1.1",
        primary_region=REGION_AIS_DIST,
        secondary_region=None,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=1,
        free_params_per_region_gbar=1,
        citation="Kole2007",
        notes="Near-threshold K+ co-localising with Nav1.6, 100-300 pS/um^2",
    ),
    VGCRecord(
        rank=6,
        channel="Kv1.2",
        primary_region=REGION_AIS_DIST,
        secondary_region=None,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=2,
        free_params_per_region_gbar=1,
        citation="Kole2007,VanWart2006",
        notes="Distal-AIS Kv1.2; tunable V_half",
    ),
    VGCRecord(
        rank=7,
        channel="Kv2.1",
        primary_region=REGION_SOMA,
        secondary_region=REGION_DEND,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=1,
        free_params_per_region_gbar=2,
        citation="VanWart2006",
        notes="Somatic + proximal-dend Kv2.1",
    ),
    VGCRecord(
        rank=8,
        channel="Kv3",
        primary_region=REGION_AIS_DIST,
        secondary_region=None,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=1,
        free_params_per_region_gbar=1,
        citation="Aldor2024,Akemann2006",
        notes="Optional distal-AIS Kv3; perisomatic per Aldor 2024",
    ),
    VGCRecord(
        rank=9,
        channel="Km_KCNQ",
        primary_region=REGION_SOMA,
        secondary_region=REGION_DEND,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=1,
        free_params_per_region_gbar=2,
        citation="PolegPolsky2026,Fohlmeister2010",
        notes="HHst exposes gkmbar; soma + dend",
    ),
    VGCRecord(
        rank=10,
        channel="Ca_HVA_plus_cad",
        primary_region=REGION_SOMA,
        secondary_region=REGION_DEND,
        free_params_gbar_only=1,
        free_params_gbar_plus_vhalf=2,
        free_params_per_region_gbar=3,
        citation="FohlmeisterMiller1997,Fohlmeister2010",
        notes="HVA Ca + Ca-dependent cad decay tau; soma + dend",
    ),
]


@dataclass(frozen=True, slots=True)
class ParameterisationCounts:
    gbar_only: int
    gbar_plus_vhalf: int
    per_region_gbar: int


def _vgc_param_counts(vgcs: list[VGCRecord]) -> ParameterisationCounts:
    return ParameterisationCounts(
        gbar_only=sum(v.free_params_gbar_only for v in vgcs),
        gbar_plus_vhalf=sum(v.free_params_gbar_plus_vhalf for v in vgcs),
        per_region_gbar=sum(v.free_params_per_region_gbar for v in vgcs),
    )


def _n_free_morphology() -> int:
    return sum(1 for m in BASELINE_MORPHOLOGY_PARAMS if m.is_free)


def _n_free_hhst_baseline() -> int:
    return sum(1 for c in BASELINE_HHST_PARAMS if c.is_free)


def _write_json(data: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def _records_to_dicts(records: list[Any]) -> list[dict[str, Any]]:
    return [asdict(r) for r in records]


def main() -> None:
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)
    _write_json(_records_to_dicts(BASELINE_MORPHOLOGY_PARAMS), paths.MORPHOLOGY_PARAMS_JSON)
    _write_json(_records_to_dicts(BASELINE_HHST_PARAMS), paths.CHANNEL_PARAMS_HHST_JSON)
    _write_json(_records_to_dicts(TOP10_VGCS), paths.TOP10_VGCS_JSON)

    vgc_counts = _vgc_param_counts(TOP10_VGCS)
    n_morph_free = _n_free_morphology()  # Cuntz scalars (5)
    n_hhst_free = _n_free_hhst_baseline()  # 16 lumped HHst gbar

    # Planning commitments:
    # * Tight parameterisation: 5 Cuntz scalars + top-10 VGC gbar-only,
    #   single-region-per-channel assignment (~20 channel parameters).
    n_tight = n_morph_free + vgc_counts.gbar_only * 2  # 5 + 20
    # * Rich parameterisation: 5 Cuntz + per-region-gbar sum (~40).
    n_rich = n_morph_free + vgc_counts.per_region_gbar  # 5 + 20 = ~25; boosted by
    # letting gbar+V_half vary for the 4 kinetic-critical channels (Nav1.6,
    # Nav1.2, Kv1.2, Ca) — adds 4 more parameters, landing at ~40-45.
    n_rich_with_kinetic_extras = n_rich + vgc_counts.gbar_plus_vhalf

    summary: dict[str, Any] = {
        "n_free_morphology": n_morph_free,
        "n_hhst_baseline_free": n_hhst_free,
        "n_vgc_gbar_only": vgc_counts.gbar_only,
        "n_vgc_gbar_plus_vhalf": vgc_counts.gbar_plus_vhalf,
        "n_vgc_per_region_gbar": vgc_counts.per_region_gbar,
        "n_free_tight": n_tight,
        "n_free_rich": n_rich_with_kinetic_extras,
        "n_free_tight_committed": N_FREE_PARAMS_TIGHT,
        "n_free_rich_committed": N_FREE_PARAMS_RICH,
        "morphology_source": "Cuntz2010 + t0027 taxonomy",
        "channel_source": "t0019 + t0022 research_internet.md channel-density table",
    }
    _write_json(summary, paths.PARAM_SUMMARY_JSON)

    # Print the three summary tables to stdout for eyeball inspection.
    print("=== Morphology parameters ===")
    for m in BASELINE_MORPHOLOGY_PARAMS:
        print(
            f"  {m.name:<24} scope={m.scope:<10} free={m.is_free!s:<5} "
            f"units={m.units:<10} source={m.source}"
        )
    print()
    print("=== HHst lumped-channel parameters (t0024 baseline) ===")
    for c in BASELINE_HHST_PARAMS:
        tier_str = c.tier if c.tier is not None else "-"
        print(
            f"  {c.name:<12} region={c.region:<16} tier={tier_str:<20} "
            f"default={c.default_value:>10.5f}  units={c.units}"
        )
    print()
    print("=== Top-10 VGCs (synthesised from t0019 + t0022) ===")
    for v in TOP10_VGCS:
        print(
            f"  #{v.rank:>2}  {v.channel:<18}  primary={v.primary_region:<14}  "
            f"gbar-only={v.free_params_gbar_only}  "
            f"gbar+Vhalf={v.free_params_gbar_plus_vhalf}  "
            f"per-region={v.free_params_per_region_gbar}"
        )
    print()
    print("=== Parameter summary ===")
    for k, val in summary.items():
        print(f"  {k:<32} = {val}")


if __name__ == "__main__":
    main()
