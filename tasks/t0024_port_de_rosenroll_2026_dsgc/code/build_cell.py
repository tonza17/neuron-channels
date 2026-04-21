"""NEURON bootstrap + DSGC cell construction for the de Rosenroll 2026 port.

This module loads the NEURON 8.2.7 Python bridge, compiles / loads the
vendored ``nrnmech.dll`` from the library asset's sources directory, sources
the ``RGCmodelGD.hoc`` morphology template, and returns a configured cell
plus its terminal dendrites (which are the sites where ACh/GABA synapses
land in the upstream code when ``term_syn_only=True``).

The active/passive channel densities are taken from
``tasks/.../code/constants.py`` which mirrors the upstream ``ei_balance.py``
``Model.set_default_params`` defaults. Values are in S/cm^2 (constants are in
mS/cm^2 and converted at the boundary).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C
from tasks.t0024_port_de_rosenroll_2026_dsgc.code import paths as P

# ---------------------------------------------------------------------------
# NEURON bootstrap
# ---------------------------------------------------------------------------


def _ensure_neuron_on_path() -> None:
    """Make sure the local NEURON 8.2.7 install is reachable.

    The project venv is Python 3.13 but NEURON 8.2.7 has no PyPI wheel for
    Windows, so we use the cp313 bindings that ship with the local install at
    ``C:/Users/md1avn/nrn-8.2.7/``.
    """
    neuron_home = Path(os.environ.get("NEURONHOME", C.NEURONHOME_DEFAULT))
    if not neuron_home.exists():
        raise RuntimeError(f"NEURONHOME not found at {neuron_home}. Set NEURONHOME env var.")

    # Prepend NEURON bin to PATH so hoc.pyd can find its DLLs.
    bin_dir = neuron_home / "bin"
    path_sep = os.pathsep
    existing_path = os.environ.get("PATH", "")
    if str(bin_dir) not in existing_path:
        os.environ["PATH"] = f"{bin_dir}{path_sep}{existing_path}"

    # Prepend NEURON's Python site directory to sys.path for ``import neuron``.
    py_dir = neuron_home / "lib" / "python"
    py_str = str(py_dir)
    if py_str not in sys.path:
        sys.path.insert(0, py_str)


def _sources_dir_hoc_safe() -> str:
    """HOC ``load_file`` / ``nrn_load_dll`` requires forward slashes on Windows."""
    return str(P.LIBRARY_SOURCES_DIR).replace("\\", "/")


def load_neuron() -> Any:
    """Return the ``h`` object after loading stdrun and ``nrnmech.dll``."""
    _ensure_neuron_on_path()

    from neuron import h

    if not P.NRNMECH_DLL.exists():
        raise RuntimeError(
            f"nrnmech.dll not found at {P.NRNMECH_DLL}. Run "
            f"``{P.LIBRARY_NRNIVMODL_CMD}`` to compile the MOD files first."
        )

    dll_path = str(P.NRNMECH_DLL).replace("\\", "/")
    h.nrn_load_dll(dll_path)

    # stdrun.hoc isn't on NEURON's default search path when running via the
    # venv Python, so source it explicitly from the local install.
    stdrun_path = Path(C.NEURONHOME_DEFAULT) / "lib" / "hoc" / "stdrun.hoc"
    stdrun_str = str(stdrun_path).replace("\\", "/")
    loaded = h.load_file(1, stdrun_str)
    assert loaded == 1, f"stdrun.hoc failed to load from {stdrun_str}"

    return h


# ---------------------------------------------------------------------------
# Cell assembly
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DSGCCell:
    """A constructed DSGC cell with its terminal dendrites enumerated."""

    h: Any
    rgc: Any  # the h.DSGC(0, 0) object
    soma: Any
    all_dends: list[Any]
    primary_dends: list[Any]  # order_list[0]
    non_terminal_dends: list[Any]
    terminal_dends: list[Any]
    terminal_locs_xy: NDArray[np.float64]  # (n_terminals, 2)
    origin_xy: tuple[float, float]


def _find_origin(h: Any, dends: list[Any]) -> tuple[float, float]:
    """Find the (x, y) centre of the dendritic arbour (from ``modelUtils.py``)."""
    left_x, right_x = 1000.0, -1000.0
    bot_y, top_y = 1000.0, -1000.0
    for dend in dends:
        dend.push()
        pts = int(h.n3d())
        if pts % 2:
            x_loc = h.x3d((pts - 1) // 2)
            y_loc = h.y3d((pts - 1) // 2)
        else:
            x_loc = (h.x3d(pts // 2) + h.x3d(pts // 2 - 1)) / 2.0
            y_loc = (h.y3d(pts // 2) + h.y3d(pts // 2 - 1)) / 2.0
        left_x = min(left_x, x_loc)
        right_x = max(right_x, x_loc)
        bot_y = min(bot_y, y_loc)
        top_y = max(top_y, y_loc)

        x_term = h.x3d(pts - 1)
        y_term = h.y3d(pts - 1)
        left_x = min(left_x, x_term)
        right_x = max(right_x, x_term)
        bot_y = min(bot_y, y_term)
        top_y = max(top_y, y_term)
        h.pop_section()
    return (
        float(left_x + (right_x - left_x) / 2.0),
        float(bot_y + (top_y - bot_y) / 2.0),
    )


def _map_tree(h: Any, cell: Any) -> tuple[list[list[Any]], list[Any], list[Any]]:
    """Sort dendrite sections by branch order; from ``modelUtils.map_tree``."""
    cell.soma.push()

    order_pos = [0]
    order_list: list[list[Any]] = [[]]
    terminals: list[Any] = []
    non_terms: list[Any] = []

    while True:
        sref = h.SectionRef()
        if order_pos[-1] < sref.nchild():
            if len(order_pos) > 1:
                non_terms.append(h.cas())
            sref.child[order_pos[-1]].push()
            if len(order_pos) > len(order_list):
                order_list.append([])
            order_list[len(order_pos) - 1].append(h.cas())
            order_pos.append(0)
        else:
            if len(order_pos) == 1:
                break
            if not sref.nchild():
                terminals.append(h.cas())
            del order_pos[-1]
            order_pos[-1] += 1
            h.pop_section()

    return order_list, terminals, non_terms


def _terminal_midpoint(h: Any, dend: Any) -> tuple[float, float]:
    """Return the 3D midpoint (x, y) of a section (used as synapse location)."""
    dend.push()
    try:
        pts = int(h.n3d())
        if pts == 2:
            x = (h.x3d(0) + h.x3d(1)) / 2.0
            y = (h.y3d(0) + h.y3d(1)) / 2.0
        elif pts % 2:
            u = (pts - 1) // 2
            x, y = h.x3d(u), h.y3d(u)
        else:
            u1 = pts // 2
            u2 = (pts - 1) // 2
            x = (h.x3d(u1) + h.x3d(u2)) / 2.0
            y = (h.y3d(u1) + h.y3d(u2)) / 2.0
        return float(x), float(y)
    finally:
        h.pop_section()


def _configure_soma(h: Any, soma: Any) -> None:
    soma.insert("HHst")
    soma.insert("cad")
    soma.gnabar_HHst = C.GBAR_NA_SOMA_MS_CM2 * 1e-3
    soma.gkbar_HHst = C.GBAR_K_SOMA_MS_CM2 * 1e-3
    soma.gkmbar_HHst = C.GBAR_KM_SOMA_MS_CM2 * 1e-3
    soma.gleak_HHst = C.GLEAK_S_CM2
    soma.eleak_HHst = C.ELEAK_MV
    soma.Ra = C.RA_OHM_CM
    soma.cm = C.CM_UF_CM2


def _configure_dends(
    h: Any,
    primary_dends: list[Any],
    non_terminal_dends: list[Any],
    terminal_dends: list[Any],
) -> None:
    """Insert HHst + cad on every dendrite with tier-appropriate densities.

    Upstream's default is ``active_terms=True`` and ``dend_pas=False`` which
    puts HHst + cad on every dendrite, with primaries getting higher gNa and
    non-terminal middle dendrites getting gNa zeroed out. We follow that
    layout.
    """
    for dend in primary_dends:
        dend.insert("HHst")
        dend.insert("cad")
        dend.gnabar_HHst = C.GBAR_NA_PRIMARY_MS_CM2 * 1e-3
        dend.gkbar_HHst = C.GBAR_K_PRIMARY_MS_CM2 * 1e-3
        dend.gkmbar_HHst = C.GBAR_KM_PRIMARY_MS_CM2 * 1e-3
        dend.gleak_HHst = C.GLEAK_S_CM2
        dend.eleak_HHst = C.ELEAK_MV
        dend.Ra = C.RA_OHM_CM
        dend.cm = C.CM_UF_CM2

    for dend in non_terminal_dends:
        dend.insert("HHst")
        dend.insert("cad")
        dend.gnabar_HHst = 0.0  # upstream: gnabar zeroed on mid dends
        dend.gkbar_HHst = C.GBAR_K_DISTAL_MS_CM2 * 1e-3
        dend.gkmbar_HHst = C.GBAR_KM_DISTAL_MS_CM2 * 1e-3
        dend.gleak_HHst = C.GLEAK_S_CM2
        dend.eleak_HHst = C.ELEAK_MV
        dend.Ra = C.RA_OHM_CM
        dend.cm = C.CM_UF_CM2

    for dend in terminal_dends:
        dend.insert("HHst")
        dend.insert("cad")
        dend.gnabar_HHst = C.GBAR_NA_DISTAL_MS_CM2 * 1e-3
        dend.gkbar_HHst = C.GBAR_K_DISTAL_MS_CM2 * 1e-3
        dend.gkmbar_HHst = C.GBAR_KM_DISTAL_MS_CM2 * 1e-3
        dend.gleak_HHst = C.GLEAK_S_CM2
        dend.eleak_HHst = C.ELEAK_MV
        dend.Ra = C.RA_OHM_CM
        dend.cm = C.CM_UF_CM2


def build_dsgc_cell() -> DSGCCell:
    """Build and configure the DSGC cell, returning a :class:`DSGCCell`."""
    h = load_neuron()

    # Source the HOC template from the vendored sources directory.
    # The ``chdir`` approach avoids having HOC ``load_file`` choke on Windows
    # path separators while still resolving the file relative to this location.
    prev_cwd = Path.cwd()
    try:
        os.chdir(P.LIBRARY_SOURCES_DIR)
        loaded = h.load_file(1, "RGCmodelGD.hoc")
        assert loaded == 1, "RGCmodelGD.hoc failed to load"

        # Instantiate the DSGC template.
        rgc = h.DSGC(0, 0)
    finally:
        os.chdir(prev_cwd)

    soma = rgc.soma
    all_dends = list(rgc.dend)
    origin = _find_origin(h, all_dends)
    order_list, terminals, non_terms = _map_tree(h, rgc)

    primary_dends = list(order_list[0])
    non_terminal_dends = list(non_terms)
    terminal_dends = list(terminals)

    _configure_soma(h, soma)
    _configure_dends(h, primary_dends, non_terminal_dends, terminal_dends)

    # Capture terminal locations now (after morphology is built).
    terminal_locs = np.zeros((len(terminal_dends), 2), dtype=np.float64)
    for i, dend in enumerate(terminal_dends):
        terminal_locs[i, 0], terminal_locs[i, 1] = _terminal_midpoint(h, dend)

    return DSGCCell(
        h=h,
        rgc=rgc,
        soma=soma,
        all_dends=all_dends,
        primary_dends=primary_dends,
        non_terminal_dends=non_terminal_dends,
        terminal_dends=terminal_dends,
        terminal_locs_xy=terminal_locs,
        origin_xy=origin,
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> int:
    """Build the cell once and print a compact summary."""
    cell = build_dsgc_cell()
    n_prim = len(cell.primary_dends)
    n_non = len(cell.non_terminal_dends)
    n_term = len(cell.terminal_dends)
    print(f"DSGC cell built: {len(cell.all_dends)} dendrites")
    print(f"  primaries     = {n_prim}")
    print(f"  non-terminals = {n_non}")
    print(f"  terminals     = {n_term}")
    print(f"  origin (x,y)  = ({cell.origin_xy[0]:.2f}, {cell.origin_xy[1]:.2f})")
    xy = cell.terminal_locs_xy
    print(
        f"  terminal x range = [{xy[:, 0].min():.1f}, {xy[:, 0].max():.1f}],"
        f" y range = [{xy[:, 1].min():.1f}, {xy[:, 1].max():.1f}]"
    )

    # Sanity checks.
    assert n_prim > 0, "at least one primary dendrite"
    assert n_term > 0, "at least one terminal dendrite"
    assert cell.terminal_locs_xy.shape == (n_term, 2)
    assert all(np.isfinite(cell.terminal_locs_xy.ravel())), "finite terminal locs"

    print("build_cell self-test PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(_self_test())
