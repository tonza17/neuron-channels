"""t0024-specific distal-section selector.

On the t0024 morphology (``RGCmodelGD.hoc``) there is no ON-arbor HOC attribute -- the template
instantiates a single ``h.DSGC`` cell with a unified dendritic arbor. The biologically equivalent
distal-leaf set is already computed by ``_map_tree`` in t0024's ``build_cell.py`` and exposed via
``DSGCCell.terminal_dends`` (HOC leaves -- sections with ``h.SectionRef(sec=sec).nchild() == 0``).

The t0029 helper walked the t0022 template's ON subtree; that attribute path does not exist on the
t0024 template, and ``cell.terminal_dends`` is the canonical distal set for this morphology.
"""

from __future__ import annotations

from typing import Any

from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import DSGCCell


def identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]:
    """Return the list of HOC leaf-dendrite sections on the t0024 DSGC morphology.

    A section is distal if it is a HOC leaf (no children) of the unified dendritic arbor.
    ``DSGCCell.terminal_dends`` is already the correct list; this wrapper exposes it through a
    t0024-specific name so downstream code reads unambiguously as "terminal leaves of the t0024
    arbor" rather than the t0022 template's ON-subtree path.
    """
    return list(cell.terminal_dends)
