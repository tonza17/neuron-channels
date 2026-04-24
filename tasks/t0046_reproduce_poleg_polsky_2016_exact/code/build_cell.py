"""Build the ModelDB 189347 DSGC cell via NEURON HOC.

Adapted (copied per the cross-task copy rule, NOT imported) from:

* ``tasks/t0008_port_modeldb_189347/code/build_cell.py:120-208`` for the HOC-safe sources-dir
  helper, ``load_neuron``, ``build_dsgc``, the ``SynapseCoords`` dataclass, and the
  ``read_synapse_coords`` / ``get_cell_summary`` helpers (approximately 100 lines combined).
* ``tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py:109-127`` for the
  ``_assert_bip_positions_baseline`` BIP-position guard (approximately 20 lines).

Loads ``RGCmodel.hoc`` (verbatim morphology + DSGC template) followed by ``dsgc_model_exact.hoc``
(GUI-free derivative of ``main.hoc`` with the ``simplerun(exptype, dir)`` proc intact). Python
drives the simulation by setting ``h.flickerVAR``, ``h.stimnoiseVAR``, and ``h.b2gnmda`` and then
calling ``h.simplerun(int(exptype), int(direction))``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    CELSIUS_DEG_C,
    DT_MS,
    TSTOP_MS,
    V_INIT_MV,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.paths import (
    DSGC_MODEL_HOC,
    NRNMECH_DLL,
    RGCMODEL_HOC,
    SOURCES_DIR,
    SOURCES_DIR_HOC_SAFE,
)


@dataclass(frozen=True, slots=True)
class SynapseCoords:
    """Snapshot of a single bundled-synapse placement on the DSGC."""

    index: int
    bip_locx_um: float
    bip_locy_um: float
    sac_inhib_locx_um: float
    sac_inhib_locy_um: float
    sac_exc_locx_um: float
    sac_exc_locy_um: float


@dataclass(frozen=True, slots=True)
class CellSummary:
    """Morphology and synapse counts for the instantiated DSGC."""

    num_synapses: int
    num_on_sections: int
    num_soma_sections: int
    num_dend_sections: int


def _nrnmech_dll_path() -> Path:
    if not NRNMECH_DLL.exists():
        raise FileNotFoundError(
            f"nrnmech.dll not found at {NRNMECH_DLL}. Run "
            "tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_nrnivmodl.cmd first.",
        )
    return NRNMECH_DLL


def load_neuron() -> Any:
    """Import NEURON, load the compiled mech DLL, and return ``h``."""
    from neuron import h  # noqa: PLC0415 — deferred import after bootstrap.

    if not getattr(load_neuron, "_loaded", False):
        dll_path: Path = _nrnmech_dll_path()
        loaded: float = h.nrn_load_dll(str(dll_path))
        assert loaded == 1.0, f"h.nrn_load_dll failed for {dll_path}"
        loaded_std: float = h.load_file("stdrun.hoc")
        assert loaded_std == 1.0, "h.load_file('stdrun.hoc') failed"
        load_neuron._loaded = True  # type: ignore[attr-defined]
    return h


def build_dsgc() -> Any:
    """Source RGCmodel.hoc and dsgc_model_exact.hoc; return h with RGC instantiated."""
    h: Any = load_neuron()
    # NEURON's HOC parser treats backslashes as escape sequences; emit forward slashes.
    h(f'chdir("{SOURCES_DIR_HOC_SAFE}")')

    if not RGCMODEL_HOC.exists():
        raise FileNotFoundError(f"RGCmodel.hoc missing at {RGCMODEL_HOC}")
    if not DSGC_MODEL_HOC.exists():
        raise FileNotFoundError(f"dsgc_model_exact.hoc missing at {DSGC_MODEL_HOC}")

    loaded_rgc: float = h.load_file(1, "RGCmodel.hoc")
    assert loaded_rgc == 1.0, "h.load_file('RGCmodel.hoc') failed"
    loaded_main: float = h.load_file(1, "dsgc_model_exact.hoc")
    assert loaded_main == 1.0, "h.load_file('dsgc_model_exact.hoc') failed"

    h("init_sim()")
    h("init_active()")
    h("access RGC.soma")
    h("update()")

    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.tstop = TSTOP_MS
    h.v_init = V_INIT_MV
    return h


def get_cell_summary(*, h: Any) -> CellSummary:
    """Read RGC.numsyn and countON; return CellSummary."""
    num_synapses: int = int(h.RGC.numsyn)
    num_on: int = int(h.RGC.countON)
    return CellSummary(
        num_synapses=num_synapses,
        num_on_sections=num_on,
        num_soma_sections=1,
        num_dend_sections=350,
    )


def read_synapse_coords(*, h: Any) -> list[SynapseCoords]:
    """Snapshot every BIPsyn / SACinhibsyn / SACexcsyn (locx, locy)."""
    coords: list[SynapseCoords] = []
    num_synapses: int = int(h.RGC.numsyn)
    for idx in range(num_synapses):
        coords.append(
            SynapseCoords(
                index=idx,
                bip_locx_um=float(h.RGC.BIPsyn[idx].locx),
                bip_locy_um=float(h.RGC.BIPsyn[idx].locy),
                sac_inhib_locx_um=float(h.RGC.SACinhibsyn[idx].locx),
                sac_inhib_locy_um=float(h.RGC.SACinhibsyn[idx].locy),
                sac_exc_locx_um=float(h.RGC.SACexcsyn[idx].locx),
                sac_exc_locy_um=float(h.RGC.SACexcsyn[idx].locy),
            ),
        )
    return coords


def assert_bip_positions_baseline(
    *,
    h: Any,
    baseline: list[SynapseCoords],
) -> None:
    """Assert every BIPsyn (locx, locy) matches the baseline snapshot.

    Adapted from ``t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py:109-127``.
    Guards against silent re-engagement of any rotation logic.
    """
    for s in baseline:
        assert h.RGC.BIPsyn[s.index].locx == s.bip_locx_um, (
            f"BIPsyn[{s.index}].locx = {h.RGC.BIPsyn[s.index].locx} "
            f"!= baseline {s.bip_locx_um}; rotation logic re-engaged?"
        )
        assert h.RGC.BIPsyn[s.index].locy == s.bip_locy_um, (
            f"BIPsyn[{s.index}].locy = {h.RGC.BIPsyn[s.index].locy} "
            f"!= baseline {s.bip_locy_um}; rotation logic re-engaged?"
        )


def reset_globals_to_canonical(*, h: Any) -> None:
    """Reset the global params we touch from Python to canonical values."""
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.tstop = TSTOP_MS
    h.v_init = V_INIT_MV


def get_sources_dir() -> Path:
    return SOURCES_DIR
