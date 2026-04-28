"""Unit tests for the scalar gabaMOD direction-dependent multiplier."""

from __future__ import annotations

from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import GABAMOD_ND, GABAMOD_PD
from tasks.t0055_nmda_mg_block_dsi_recovery.code.synapses import gaba_mod


def test_gaba_mod_pd() -> None:
    value: float = gaba_mod(theta_deg=0.0)
    assert abs(value - GABAMOD_PD) < 1e-9, f"gaba_mod(0) = {value}, expected {GABAMOD_PD}"


def test_gaba_mod_nd() -> None:
    value: float = gaba_mod(theta_deg=180.0)
    assert abs(value - GABAMOD_ND) < 1e-9, f"gaba_mod(180) = {value}, expected {GABAMOD_ND}"


if __name__ == "__main__":
    test_gaba_mod_pd()
    test_gaba_mod_nd()
    print("[gaba_mod] PASS", flush=True)
