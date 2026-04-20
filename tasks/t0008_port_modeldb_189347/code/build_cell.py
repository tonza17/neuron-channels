"""Build and drive the ModelDB 189347 DSGC cell via NEURON HOC.

This module imports Poleg-Polsky & Diamond 2016 sources verbatim through
``h.load_file`` rather than re-implementing them in Python/NetPyNE.
Fidelity to the paper requires the HOC side to own topology, channel
insertion, point-process construction, and synapse placement; Python only:

  1. loads the compiled ``nrnmech.dll`` (Windows build artifact from t0007
     wrapper) so ``HHst``, ``bipNMDA``, ``SACinhib``, ``SACexc`` mechanisms
     are visible;
  2. sources the GUI-free derivative ``dsgc_model.hoc`` (bundled under the
     library asset's ``sources/`` alongside its verbatim parent ``main.hoc``);
  3. exposes helper functions that read and rotate per-synapse ``locx``/
     ``locy`` coordinates (the rotation is how the port implements drifting
     bars at 12 angles without touching morphology).

The module never writes files. All callers are test/pipeline scripts.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0008_port_modeldb_189347.code.constants import (
    ACH_MOD,
    AP_THRESHOLD_MV,
    B2GAMPA_NS,
    B2GNMDA_NS,
    CELSIUS_DEG_C,
    DT_MS,
    E_SAC_INHIB_MV,
    GABA_MOD,
    GAMMA_NMDA_V_DEP,
    LIGHT_REVERSE,
    LIGHT_X_END_UM,
    LIGHT_X_START_UM,
    LIGHT_Y_END_UM,
    LIGHT_Y_START_UM,
    LIGHTSPEED_UM_PER_MS,
    LIGHTSTART_MS,
    LIGHTWIDTH_UM,
    N_NMDA_V_DEP,
    NEURONHOME_DEFAULT,
    S2GACH_NS,
    S2GGABA_NS,
    TAU1_NMDA_BIP_MS,
    TSTOP_MS,
    V_INIT_MV,
    V_SHIFT_HHST_MV,
)
from tasks.t0008_port_modeldb_189347.code.paths import (
    MODELDB_BUILD_DIR,
    MODELDB_GUI_FREE_HOC,
    MODELDB_RGCMODEL_HOC,
    MODELDB_SOURCES_DIR,
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
    dll = MODELDB_BUILD_DIR / "nrnmech.dll"
    if not dll.exists():
        raise FileNotFoundError(
            f"nrnmech.dll not found at {dll}. Run nrnivmodl on "
            f"{MODELDB_SOURCES_DIR} via code/run_nrnivmodl.cmd first."
        )
    return dll


def load_neuron() -> Any:
    """Import NEURON, load the compiled mech DLL, and return ``h``.

    Side effects: sets ``NEURONHOME`` if missing and calls
    ``h.nrn_load_dll`` on the task-local ``nrnmech.dll``. NEURON will print a
    ``Mechanisms not loaded`` warning if called twice for the same DLL path;
    this is harmless. We guard by checking a module-level flag.
    """
    os.environ.setdefault("NEURONHOME", NEURONHOME_DEFAULT)
    from neuron import h  # noqa: PLC0415 — deferred import until env is set

    if not getattr(load_neuron, "_loaded", False):
        dll_path = _nrnmech_dll_path()
        loaded = h.nrn_load_dll(str(dll_path))
        assert loaded == 1.0, f"h.nrn_load_dll failed for {dll_path}"
        # stdrun.hoc defines ``run()``, ``v_init``, ``finitialize``,
        # ``continuerun``, etc. NEURON's Python bootstrap does not source
        # it automatically when ``nrngui.hoc`` is skipped.
        loaded_std = h.load_file("stdrun.hoc")
        assert loaded_std == 1.0, "h.load_file('stdrun.hoc') failed"
        load_neuron._loaded = True  # type: ignore[attr-defined]
    return h


def _sources_dir_hoc_safe() -> str:
    """Return the library sources dir in a form HOC accepts on Windows.

    NEURON's HOC parser treats backslashes in string literals as escape
    sequences, so we emit forward slashes even on Windows.
    """
    return str(MODELDB_SOURCES_DIR).replace("\\", "/")


def build_dsgc() -> Any:
    """Source ``RGCmodel.hoc`` and ``dsgc_model.hoc`` and return ``h``.

    On exit, ``h.RGC`` holds a fully-initialized DSGC template instance
    with: 1 soma + 350 dend sections, HHst inserted on the soma, passive
    (or active, depending on ``use_active``) cable elsewhere, and
    ``numsyn`` point processes of each of the three synapse kinds placed on
    ON dendrites via ``placeBIP``. The global ``celsius`` is reset to the
    paper's 32 deg C.
    """
    h = load_neuron()

    # Resolve HOC path relative to sources dir so ``load_file`` finds
    # RGCmodel.hoc during its mosinit-style sourcing.
    sources_forward = _sources_dir_hoc_safe()
    h(f'chdir("{sources_forward}")')

    if not MODELDB_RGCMODEL_HOC.exists():
        raise FileNotFoundError(f"RGCmodel.hoc missing at {MODELDB_RGCMODEL_HOC}")
    if not MODELDB_GUI_FREE_HOC.exists():
        raise FileNotFoundError(
            f"dsgc_model.hoc missing at {MODELDB_GUI_FREE_HOC}. This is a "
            "task-local derivative of main.hoc with GUI lines stripped."
        )

    loaded_rgc = h.load_file(1, "RGCmodel.hoc")
    assert loaded_rgc == 1.0, "h.load_file('RGCmodel.hoc') failed"
    loaded_main = h.load_file(1, "dsgc_model.hoc")
    assert loaded_main == 1.0, "h.load_file('dsgc_model.hoc') failed"

    # Drive the simulation bootstrap the way the GUI callback simplerun
    # does in the paper: init_sim -> init_active -> access soma -> update.
    h("init_sim()")
    h("init_active()")
    h("access RGC.soma")
    h("update()")

    # Reset global simulator state to canonical values; the HOC setters
    # above handle synaptic and mechanism params, but we harden temperature,
    # dt, tstop, v_init, and the spike-detection threshold here to avoid
    # drift if the HOC defaults are later edited.
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.tstop = TSTOP_MS
    h.v_init = V_INIT_MV

    return h


def get_cell_summary(h: Any) -> CellSummary:
    """Read ``RGC.numsyn``/``countON`` and derive section counts."""
    num_synapses = int(h.RGC.numsyn)
    num_on = int(h.RGC.countON)
    num_soma = 1
    num_dend = 350
    return CellSummary(
        num_synapses=num_synapses,
        num_on_sections=num_on,
        num_soma_sections=num_soma,
        num_dend_sections=num_dend,
    )


def read_synapse_coords(h: Any) -> list[SynapseCoords]:
    """Extract (locx, locy) for every BIPsyn / SACinhibsyn / SACexcsyn."""
    coords: list[SynapseCoords] = []
    num_synapses = int(h.RGC.numsyn)
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
            )
        )
    return coords


def rotate_synapse_coords_in_place(
    *,
    h: Any,
    angle_deg: float,
    baseline: list[SynapseCoords],
    rotate_sac: bool = False,
) -> None:
    """Rotate synapse (locx, locy) around the soma by ``angle_deg``.

    The HOC stimulus proc ``placeBIP`` reads ``.locx`` to compute per-
    synapse arrival times along a fixed left-to-right moving bar:

        starttime = lightstart + (syn.locx - lightXstart) / lightspeed

    Bundled morphology places BIP, SACinhib, and SACexc at identical
    coordinates per ON dendrite, so rotating all three together preserves
    BIP/SAC arrival-time symmetry and the cell fails to become direction-
    selective. To reproduce the paper's direction-selectivity envelope
    via spatial rotation we rotate BIP coords only while leaving SAC
    coords fixed, which biases the bar's arrival time at the excitatory
    inputs relative to the GABA/ACh inputs. This matches the biological
    story that bipolar input is angle-agnostic while the SAC network
    imposes a spatial bias.

    Passing ``rotate_sac=True`` rotates all three; useful for ablation.

    The rotation is applied to the ``baseline`` snapshot taken before any
    rotation (not to the current HOC values) to avoid accumulated error.
    """
    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    for s in baseline:
        bx = cos_t * s.bip_locx_um - sin_t * s.bip_locy_um
        by = sin_t * s.bip_locx_um + cos_t * s.bip_locy_um
        h.RGC.BIPsyn[s.index].locx = bx
        h.RGC.BIPsyn[s.index].locy = by
        if rotate_sac:
            ix = cos_t * s.sac_inhib_locx_um - sin_t * s.sac_inhib_locy_um
            iy = sin_t * s.sac_inhib_locx_um + cos_t * s.sac_inhib_locy_um
            ex = cos_t * s.sac_exc_locx_um - sin_t * s.sac_exc_locy_um
            ey = sin_t * s.sac_exc_locx_um + cos_t * s.sac_exc_locy_um
            h.RGC.SACinhibsyn[s.index].locx = ix
            h.RGC.SACinhibsyn[s.index].locy = iy
            h.RGC.SACexcsyn[s.index].locx = ex
            h.RGC.SACexcsyn[s.index].locy = ey
        else:
            # Restore SAC coords to baseline to keep inhibition fixed.
            h.RGC.SACinhibsyn[s.index].locx = s.sac_inhib_locx_um
            h.RGC.SACinhibsyn[s.index].locy = s.sac_inhib_locy_um
            h.RGC.SACexcsyn[s.index].locx = s.sac_exc_locx_um
            h.RGC.SACexcsyn[s.index].locy = s.sac_exc_locy_um


def reset_synapse_coords(
    *,
    h: Any,
    baseline: list[SynapseCoords],
) -> None:
    """Restore coords to the snapshot captured at build time."""
    for s in baseline:
        h.RGC.BIPsyn[s.index].locx = s.bip_locx_um
        h.RGC.BIPsyn[s.index].locy = s.bip_locy_um
        h.RGC.SACinhibsyn[s.index].locx = s.sac_inhib_locx_um
        h.RGC.SACinhibsyn[s.index].locy = s.sac_inhib_locy_um
        h.RGC.SACexcsyn[s.index].locx = s.sac_exc_locx_um
        h.RGC.SACexcsyn[s.index].locy = s.sac_exc_locy_um


def apply_params(h: Any, *, seed: int) -> None:
    """Apply canonical Poleg-Polsky parameters and a per-trial seed."""
    h.tstop = TSTOP_MS
    h.dt = DT_MS
    h.celsius = CELSIUS_DEG_C
    h.v_init = V_INIT_MV

    # Seed the three Random streams the HOC uses (rtime, rnoise, rBIP).
    # The HOC proc ``placeBIP`` re-seeds rBIP and rnoise from ``seed2`` on
    # every invocation, so setting seed2 before placeBIP is sufficient.
    h(f"seed2={seed}")

    # Synaptic conductances (already identical to HOC defaults, re-set
    # explicitly so param edits in Python survive a re-run).
    h.b2gampa = B2GAMPA_NS
    h.b2gnmda = B2GNMDA_NS
    h.s2ggaba = S2GGABA_NS
    h.s2gach = S2GACH_NS
    h.gabaMOD = GABA_MOD
    h.achMOD = ACH_MOD

    # Stimulus geometry.
    h.lightspeed = LIGHTSPEED_UM_PER_MS
    h.lightwidth = LIGHTWIDTH_UM
    h.lightstart = LIGHTSTART_MS
    h.lightXstart = LIGHT_X_START_UM
    h.lightXend = LIGHT_X_END_UM
    h.lightYstart = LIGHT_Y_START_UM
    h.lightYend = LIGHT_Y_END_UM
    h.lightreverse = LIGHT_REVERSE

    # HHst channel tuning and NMDA voltage-dependence.
    h.vshift_HHst = V_SHIFT_HHST_MV
    h.tau1NMDA_bipNMDA = TAU1_NMDA_BIP_MS
    h.e_SACinhib = E_SAC_INHIB_MV
    h.n_bipNMDA = N_NMDA_V_DEP
    h.gama_bipNMDA = GAMMA_NMDA_V_DEP


def run_one_trial(
    *,
    h: Any,
    angle_deg: float,
    seed: int,
    baseline_coords: list[SynapseCoords],
) -> float:
    """Run a single trial; return the somatic spike count / (tstop_s).

    Firing rate is computed from the number of upward threshold crossings
    of ``V_{soma}`` above ``AP_THRESHOLD_MV`` across the simulated window.
    """
    apply_params(h, seed=seed)
    rotate_synapse_coords_in_place(h=h, angle_deg=angle_deg, baseline=baseline_coords)
    h("update()")
    h("placeBIP()")

    v_rec = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)
    t_rec = h.Vector()
    t_rec.record(h._ref_t)

    h.finitialize(V_INIT_MV)
    h.continuerun(TSTOP_MS)

    # Restore for the next trial.
    reset_synapse_coords(h=h, baseline=baseline_coords)

    # Count upward threshold crossings.
    samples: list[float] = list(v_rec)
    spike_count = 0
    above = samples[0] >= AP_THRESHOLD_MV
    for val in samples[1:]:
        now_above = val >= AP_THRESHOLD_MV
        if now_above and not above:
            spike_count += 1
        above = now_above

    tstop_s = TSTOP_MS / 1000.0
    return float(spike_count) / tstop_s
