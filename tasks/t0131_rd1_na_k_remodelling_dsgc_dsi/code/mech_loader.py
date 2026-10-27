"""Load the t0024 and t0080-compatible NEURON mechanism libraries from task-local paths.

The t0080 ``code/build/nrnmech.dll`` is gitignored and absent in the worktree. A byte-identical
tracked copy lives in t0107. This module copies it into ``code/build/`` of this task and points
the t0080 path resolver at it, so the libraries' own loaders (t0090 ``_get_neuron_h``) work
without modifying any other task folder.
"""

import shutil
from typing import Any

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import paths as t0080_paths
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    BUILD_DIR,
    T0107_DLL,
    T0131_DLL,
)

_MECH_NAMES_REQUIRED: list[str] = ["nav16t80", "kdrt80", "kv3t80", "kv4t80", "HHst"]


def ensure_dll_copy() -> None:
    if not T0131_DLL.exists():
        BUILD_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(T0107_DLL, T0131_DLL)
    assert T0131_DLL.exists(), "t0131 nrnmech.dll exists"


def load_mechanisms() -> Any:
    """Return the NEURON ``h`` singleton with both mechanism libraries loaded (idempotent)."""
    ensure_dll_copy()
    t0080_paths.WINDOWS_MOD_BUILD_DLL = T0131_DLL
    from tasks.t0090_morphology_generator_diversity_test.code.generator import (
        _get_neuron_h,
    )

    h: Any = _get_neuron_h()
    sec = h.Section(name="mech_probe")
    for name in _MECH_NAMES_REQUIRED:
        sec.insert(name)
    return h
