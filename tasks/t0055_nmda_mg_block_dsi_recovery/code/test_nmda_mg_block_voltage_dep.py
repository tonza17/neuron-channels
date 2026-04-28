"""Validation gate (NEW): NMDA_MgBlock voltage-dependence sanity test.

Build a single-section NEURON cell, attach a single ``NMDA_MgBlock`` POINT_PROCESS, voltage-clamp
the section at six membrane voltages spanning ``[-80, +20] mV`` via ``h.SEClamp``, drive the
NMDA mechanism with one ``NetCon`` event at ``t = 100 ms``, and record peak ``g`` over the trial.

Assertions:

1. Peak ``g`` is monotonically non-decreasing with depolarisation across the six voltages.
2. ``peak_g(-80 mV) <= 0.25 * peak_g(-20 mV)`` (Boltzmann factor at -80 mV is ~0.20 vs ~0.74 at
   -20 mV, ratio 0.27; the 0.25 cutoff includes a small margin for numerical jitter).

The six (v_clamp_mv, peak_g_us) pairs are persisted to ``results/mg_block_g_v_empirical.json``
for downstream consumption by ``render_figures.render_mg_block_g_v_curve``.

Order: this gate runs AFTER the ``nrnivmodl`` build but BEFORE the full sweep. A misconfigured
MOD (wrong sign in ``local_v``, wrong placement of ``gama``, etc.) fails fast here instead of
silently producing wrong tuning curves over a 5-hour sweep.
"""

from __future__ import annotations

import json
from typing import Any

import numpy as np

from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import (
    DT_MS,
    MG_BLOCK_GAMMA,
    MG_BLOCK_N,
    MG_BLOCK_VOFF,
    MG_BLOCK_VSET_MV,
    NMDA_E_MV,
    NMDA_TAU1_MS,
    NMDA_TAU2_MS,
    RA_OHM_CM,
    RM_OHM_CM2,
    V_INIT_MV,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    ensure_nmda_mg_block_compiled,
    load_stdrun,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.paths import MG_BLOCK_G_V_EMPIRICAL_JSON

V_CLAMP_VOLTAGES_MV: tuple[float, ...] = (-80.0, -60.0, -40.0, -20.0, 0.0, 20.0)
SECTION_LENGTH_UM: float = 10.0
SECTION_DIAM_UM: float = 1.0
NETCON_WEIGHT_US: float = 1e-3  # 1 nS-equivalent
NETCON_EVENT_T_MS: float = 100.0
RUN_DURATION_MS: float = 200.0
SECLAMP_RS_MOHM: float = 0.001  # very low series resistance to clamp tightly
RATIO_NEG80_OVER_NEG20_MAX: float = 0.25


def _measure_peak_g_at_clamp(
    *,
    h: Any,
    v_clamp_mv: float,
) -> float:
    """Build a one-section cell with a single NMDA_MgBlock under SEClamp; return peak g (uS)."""
    # Fresh section per voltage so leftover state can not leak across measurements.
    sec: Any = h.Section(name=f"sanity_v{int(v_clamp_mv):+d}")
    sec.L = SECTION_LENGTH_UM
    sec.diam = SECTION_DIAM_UM
    sec.Ra = RA_OHM_CM
    sec.cm = 1.0
    sec.insert("pas")
    for seg in sec:
        seg.pas.g = 1.0 / RM_OHM_CM2
        seg.pas.e = V_INIT_MV
    seg = sec(0.5)

    nmda_syn: Any = h.NMDA_MgBlock(seg)
    nmda_syn.tau1 = NMDA_TAU1_MS
    nmda_syn.tau2 = NMDA_TAU2_MS
    nmda_syn.e = NMDA_E_MV
    nmda_syn.n = MG_BLOCK_N
    nmda_syn.gama = MG_BLOCK_GAMMA
    nmda_syn.Voff = MG_BLOCK_VOFF
    nmda_syn.Vset = MG_BLOCK_VSET_MV

    seclamp: Any = h.SEClamp(seg)
    seclamp.dur1 = RUN_DURATION_MS
    seclamp.amp1 = v_clamp_mv
    seclamp.rs = SECLAMP_RS_MOHM

    netstim: Any = h.NetStim()
    netstim.number = 1
    netstim.noise = 0.0
    netstim.interval = 1.0
    netstim.start = NETCON_EVENT_T_MS

    netcon: Any = h.NetCon(netstim, nmda_syn)
    netcon.delay = 0.0
    netcon.weight[0] = NETCON_WEIGHT_US

    g_rec: Any = h.Vector()
    g_rec.record(nmda_syn._ref_g)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)

    h.dt = DT_MS
    h.finitialize(v_clamp_mv)
    h.continuerun(RUN_DURATION_MS)

    g_arr: np.ndarray = np.array(list(g_rec), dtype=np.float64)
    if g_arr.size == 0:
        return 0.0
    return float(np.max(g_arr))


def test_nmda_mg_block_voltage_dependence() -> None:
    """Confirm peak gNMDA is monotonic in voltage and -80/-20 mV ratio is below 0.25."""
    ensure_neuron_importable()
    load_stdrun()
    ensure_nmda_mg_block_compiled()
    enable_cvode()
    from neuron import h  # noqa: PLC0415

    peak_g_by_voltage: dict[float, float] = {}
    print(
        "[mg-sanity] sweeping NMDA_MgBlock under SEClamp at "
        f"{[f'{v:+.0f} mV' for v in V_CLAMP_VOLTAGES_MV]}",
        flush=True,
    )
    for v_clamp_mv in V_CLAMP_VOLTAGES_MV:
        peak_g: float = _measure_peak_g_at_clamp(h=h, v_clamp_mv=v_clamp_mv)
        peak_g_by_voltage[v_clamp_mv] = peak_g
        print(
            f"[mg-sanity]  v_clamp={v_clamp_mv:+6.1f} mV  peak_g={peak_g:.6e} uS",
            flush=True,
        )

    # Persist for the Mg-block g(v) sanity figure (Step 15).
    MG_BLOCK_G_V_EMPIRICAL_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload: list[dict[str, float]] = [
        {"v_clamp_mv": v, "peak_g_us": peak_g_by_voltage[v]} for v in V_CLAMP_VOLTAGES_MV
    ]
    MG_BLOCK_G_V_EMPIRICAL_JSON.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    print(f"[mg-sanity] wrote {MG_BLOCK_G_V_EMPIRICAL_JSON}", flush=True)

    # Assertion 1: monotonic non-decreasing with depolarisation.
    sorted_voltages: list[float] = sorted(peak_g_by_voltage.keys())
    for prev_v, next_v in zip(sorted_voltages[:-1], sorted_voltages[1:], strict=True):
        prev_g: float = peak_g_by_voltage[prev_v]
        next_g: float = peak_g_by_voltage[next_v]
        assert next_g >= prev_g - 1e-12, (
            f"Monotonicity violated: peak_g({prev_v:+.1f}) = {prev_g:.6e} > "
            f"peak_g({next_v:+.1f}) = {next_g:.6e}"
        )

    # Assertion 2: peak_g(-80 mV) <= 0.25 * peak_g(-20 mV).
    g_neg80: float = peak_g_by_voltage[-80.0]
    g_neg20: float = peak_g_by_voltage[-20.0]
    assert g_neg20 > 0.0, (
        f"peak_g(-20 mV) = {g_neg20:.6e} is not positive; cannot compute -80/-20 ratio"
    )
    ratio: float = g_neg80 / g_neg20
    print(
        f"[mg-sanity] peak_g(-80) / peak_g(-20) = {ratio:.4f} (must be <= "
        f"{RATIO_NEG80_OVER_NEG20_MAX:.4f})",
        flush=True,
    )
    assert ratio <= RATIO_NEG80_OVER_NEG20_MAX, (
        f"Mg block too weak at -80 mV: peak_g(-80)/peak_g(-20) = {ratio:.4f} > "
        f"{RATIO_NEG80_OVER_NEG20_MAX}"
    )


if __name__ == "__main__":
    test_nmda_mg_block_voltage_dependence()
    print("[mg-sanity] PASS", flush=True)
