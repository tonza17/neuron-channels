"""Unit tests: channel scaling, clamp sign, DSI rules, calibration independence, spike metrics."""

import ast
import json

import numpy as np
import pytest

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import (
    build_scaled,
    dispose_all_cells,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.clamp import (
    RECORD_NONE,
    ClampJob,
    run_clamp_job,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import ScalingArm
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.current_clamp import (
    adaptation_index,
    isi_cv,
    spike_fwhm_ms,
    spike_peak_mv,
    spike_times,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.dsi_rules import (
    TrialCount,
    summarise_counts,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import CODE_DIR, REFERENCE_CELLS_JSONL
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.scaling import (
    ChannelScales,
    apply_channel_scales,
    snapshot_gbars,
)


def _first_vector() -> tuple[str, list[float]]:
    row = json.loads(REFERENCE_CELLS_JSONL.read_text(encoding="utf-8").splitlines()[0])
    return str(row["cell_id"]), [float(x) for x in row["param_vector"]]


def test_scaling_identity_and_factors() -> None:
    _, vec = _first_vector()
    dispose_all_cells()
    base = build_scaled(
        vector_68d=vec, scales=ChannelScales(s_na=1.0, s_k=1.0), with_synapses=False
    )
    snap_base = snapshot_gbars(cell=base.cell)
    apply_channel_scales(cell=base.cell, scales=ChannelScales(s_na=1.0, s_k=1.0))
    assert snapshot_gbars(cell=base.cell) == snap_base, "identity scaling leaves gbar unchanged"

    scaled = build_scaled(
        vector_68d=vec, scales=ChannelScales(s_na=0.5, s_k=2.0), with_synapses=False
    )
    snap = snapshot_gbars(cell=scaled.cell)
    for group in ("soma", "ais"):
        assert snap[f"{group}:gbar_nav16t80"] == pytest.approx(
            0.5 * snap_base[f"{group}:gbar_nav16t80"]
        )
        assert snap[f"{group}:gnabar_HHst"] == pytest.approx(
            0.5 * snap_base[f"{group}:gnabar_HHst"]
        )
        assert snap[f"{group}:gbar_kv3t80"] == pytest.approx(
            2.0 * snap_base[f"{group}:gbar_kv3t80"]
        )
    assert snap["soma:gbar_kdrt80"] == pytest.approx(2.0 * snap_base["soma:gbar_kdrt80"])
    for key, val in snap_base.items():
        if key.startswith("dendrites:"):
            assert snap[key] == pytest.approx(val), f"dendrite density {key} unchanged in base arm"
    assert snap["soma:gbar_napt80"] == pytest.approx(snap_base["soma:gbar_napt80"])

    dend = build_scaled(
        vector_68d=vec,
        scales=ChannelScales(s_na=0.5, s_k=2.0, arm=ScalingArm.SOMA_AIS_DENDRITE),
        with_synapses=False,
    )
    snap_d = snapshot_gbars(cell=dend.cell)
    assert snap_d["dendrites:gbar_kdrt80"] == pytest.approx(
        2.0 * snap_base["dendrites:gbar_kdrt80"]
    )
    assert snap_d["dendrites:gbar_nav16t80"] == pytest.approx(
        0.5 * snap_base["dendrites:gbar_nav16t80"]
    )
    dispose_all_cells()


def test_clamp_current_sign_outward_positive() -> None:
    cid, vec = _first_vector()
    out = run_clamp_job(
        ClampJob(
            job_key="t",
            cell_id=cid,
            vector_68d=vec,
            s_na=1.0,
            s_k=1.0,
            arm=str(ScalingArm.SOMA_AIS),
            v_hold_mv=-65.0,
            v_step_mv=35.0,
            record_channels=RECORD_NONE,
            save_trace=False,
        )
    )
    assert out["sustained_na"] > 0.0, "sustained outward K current at +35 mV is positive"
    dispose_all_cells()


def test_dsi_rule_none_when_silent_or_low_count() -> None:
    silent = [
        TrialCount(direction_deg=d, seed_index=s, spike_count=0, peak_mv=-50.0, error=None)
        for d in (0.0, 180.0)
        for s in range(3)
    ]
    res = summarise_counts(trials=silent)
    assert res.dsi_signed is None and res.dsi_unguarded is None
    assert res.low_count and res.pd_spikes == 0 and res.nd_spikes == 0

    low = [
        TrialCount(direction_deg=0.0, seed_index=0, spike_count=1, peak_mv=0.0, error=None),
        TrialCount(direction_deg=0.0, seed_index=1, spike_count=1, peak_mv=0.0, error=None),
        TrialCount(direction_deg=180.0, seed_index=0, spike_count=0, peak_mv=0.0, error=None),
        TrialCount(direction_deg=180.0, seed_index=1, spike_count=0, peak_mv=0.0, error=None),
    ]
    res_low = summarise_counts(trials=low)
    assert res_low.dsi_signed is None, "PD spikes below the guard give None, not -1.0 or 0.0"
    assert res_low.low_count and res_low.pd_spikes == 2
    assert res_low.dsi_unguarded == pytest.approx(1.0)

    ok = [
        TrialCount(direction_deg=0.0, seed_index=s, spike_count=30, peak_mv=0.0, error=None)
        for s in range(3)
    ] + [
        TrialCount(direction_deg=180.0, seed_index=s, spike_count=10, peak_mv=0.0, error=None)
        for s in range(3)
    ]
    res_ok = summarise_counts(trials=ok)
    assert res_ok.dsi_signed == pytest.approx(0.5) and not res_ok.low_count
    assert res_ok.pd_rate_hz == pytest.approx(30.0 / 1.4)


def test_calibration_module_independent_of_firing_code() -> None:
    src = (CODE_DIR / "calibration.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.append(node.module)
        if isinstance(node, ast.Import):
            imported.extend(a.name for a in node.names)
    joined = " ".join(imported)
    for banned in ("current_clamp", "evaluator", "dsi_rules", "bias"):
        assert banned not in joined, f"calibration.py must not import {banned}"
    identifiers: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            identifiers.append(node.id)
        elif isinstance(node, ast.Attribute):
            identifiers.append(node.attr)
        elif isinstance(node, ast.arg):
            identifiers.append(node.arg)
    for ident in identifiers:
        low = ident.lower()
        assert "spike" not in low and "firing" not in low, f"calibration reads no firing: {ident}"


def test_spike_metric_helpers_on_synthetic_trace() -> None:
    t = np.arange(0.0, 600.0, 0.025)
    v = np.full_like(t, -60.0)
    spike_starts = [110.0, 160.0, 210.0, 510.0]
    for s in spike_starts:
        m = (t >= s) & (t < s + 1.0)
        v[m] = -60.0 + 100.0 * np.sin(np.pi * (t[m] - s) / 1.0)
    times = spike_times(t_ms=t, v_mv=v, threshold_mv=-10.0)
    assert len(times) == 4
    assert spike_peak_mv(t_ms=t, v_mv=v, times_ms=times) == pytest.approx(40.0, abs=0.5)
    fwhm = spike_fwhm_ms(t_ms=t, v_mv=v, times_ms=times)
    assert fwhm is not None and 0.4 < fwhm < 0.8
    ai = adaptation_index(times_ms=times, onset_ms=100.0, dur_ms=500.0)
    assert ai is not None
    assert ai == pytest.approx(1.0 - (1 / 0.2) / (2 / 0.1), abs=0.01)
    assert isi_cv(times_ms=[0.0, 10.0, 20.0, 30.0]) == pytest.approx(0.0)
    assert isi_cv(times_ms=[0.0, 10.0]) is None
