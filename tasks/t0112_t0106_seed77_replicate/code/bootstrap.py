"""Cross-platform NEURON bootstrap for the t0080 task.

On Windows, the t0024 ``build_cell.py`` works as-is using the local
``C:\\Users\\md1avn\\nrn-8.2.7`` install plus the vendored ``nrnmech.dll``
in ``tasks/t0024_*/assets/library/de_rosenroll_2026_dsgc/sources/``.

On Linux (the Vast.ai remote), the picture is different: NEURON is the pip
``neuron==8.2.7`` wheel (no NEURONHOME), and the t0024 vendored MOD library
is a Windows ``.dll`` that NEURON cannot load on Linux. To make
``build_dsgc_cell`` work on Linux we monkey-patch t0024's ``_ensure_neuron_on_path``
to be a no-op and replace ``load_neuron`` with a Linux-aware variant that
loads the t0024 MOD shared object (compiled at task setup time by
``compile_t0024_mods_linux``).

This module must be imported BEFORE any t0024 code that calls ``load_neuron``.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

# Linux build of the t0024 vendored MOD library lives alongside the source
# files (i.e. inside the t0024 library asset's ``sources/`` folder under a
# ``x86_64/.libs/libnrnmech.so`` subtree). We only consult this path on Linux.
_T24_SOURCES_DIR = Path(
    "tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources"
).resolve()
_T24_LINUX_BUILD_DIR = _T24_SOURCES_DIR / "x86_64"
_T24_LINUX_SO = _T24_LINUX_BUILD_DIR / ".libs" / "libnrnmech.so"
_T24_LINUX_SO_FALLBACK = _T24_LINUX_BUILD_DIR / "libnrnmech.so"

_BOOTSTRAPPED: bool = False


def _is_linux() -> bool:
    return sys.platform != "win32"


def _resolve_t24_linux_so() -> Path:
    """Return the path to the Linux-compiled t0024 MOD library on disk."""
    for cand in (_T24_LINUX_SO, _T24_LINUX_SO_FALLBACK):
        if cand.exists():
            return cand
    raise FileNotFoundError(
        "t0024 Linux MOD library not found. Expected at "
        f"{_T24_LINUX_SO} or {_T24_LINUX_SO_FALLBACK}. "
        "Run compile_t0024_mods_linux() first."
    )


def compile_t0024_mods_linux() -> Path:
    """Compile the t0024 MOD sources into a Linux .so (idempotent)."""
    if not _is_linux():
        raise RuntimeError("compile_t0024_mods_linux is only valid on Linux")
    nrnivmodl = shutil.which("nrnivmodl")
    if nrnivmodl is None:
        # Fallback to the venv-relative path used by the Vast.ai instance.
        cand = Path(sys.prefix) / "bin" / "nrnivmodl"
        if cand.exists():
            nrnivmodl = str(cand)
    if nrnivmodl is None:
        raise FileNotFoundError("nrnivmodl not on PATH and not in venv/bin")

    # Run nrnivmodl from inside the sources/ dir so x86_64/ lands there.
    if _T24_LINUX_SO.exists() or _T24_LINUX_SO_FALLBACK.exists():
        return _resolve_t24_linux_so()
    subprocess.run(
        [nrnivmodl, "."],
        cwd=str(_T24_SOURCES_DIR),
        check=True,
    )
    return _resolve_t24_linux_so()


def _patched_load_neuron_linux() -> Any:
    """Linux-only replacement for t0024.code.build_cell.load_neuron."""
    from neuron import h

    so_path = _resolve_t24_linux_so()
    rc = h.nrn_load_dll(str(so_path))
    assert rc == 1.0, f"h.nrn_load_dll failed for {so_path} (rc = {rc})"
    h.load_file("stdrun.hoc")
    return h


def _resolve_neuron_share_dir() -> Path:
    """Return the directory containing NEURON's stdrun.hoc on Linux."""
    # The neuron pip wheel ships .../site-packages/neuron/.data/share/nrn
    import neuron  # type: ignore[import-untyped]

    pkg_dir = Path(neuron.__file__).resolve().parent
    candidate = pkg_dir / ".data" / "share" / "nrn"
    if (candidate / "lib" / "hoc" / "stdrun.hoc").exists():
        return candidate
    # Fallback: walk upwards looking for share/nrn
    for parent in pkg_dir.parents:
        cand = parent / "share" / "nrn"
        if (cand / "lib" / "hoc" / "stdrun.hoc").exists():
            return cand
    raise FileNotFoundError("Cannot locate NEURON share dir with stdrun.hoc")


def bootstrap_neuron() -> None:
    """Apply Linux monkey-patches if needed (idempotent)."""
    global _BOOTSTRAPPED
    if _BOOTSTRAPPED:
        return
    if _is_linux():
        # Set NEURONHOME to the wheel-bundled share dir so any t0024 / t0090
        # code path that constructs `NEURONHOME_DEFAULT / lib / hoc / stdrun.hoc`
        # finds a real file. Doing this BEFORE importing t0024 constants below
        # ensures the t0024.code.constants module's `os.environ.setdefault`
        # call reads our value (since it uses setdefault, not setenv).
        try:
            share = _resolve_neuron_share_dir()
            os.environ["NEURONHOME"] = str(share)
        except (FileNotFoundError, ImportError):
            pass

        # Compile t0024 MODs if missing.
        compile_t0024_mods_linux()
        # Patch t0024 build_cell to skip Windows-specific NEURONHOME check
        # and to load the Linux .so instead of the .dll.
        from tasks.t0024_port_de_rosenroll_2026_dsgc.code import build_cell as _bc
        from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as _c24
        from tasks.t0024_port_de_rosenroll_2026_dsgc.code import paths as _p24

        # Override the hard-coded Windows path with the Linux share dir.
        try:
            share = _resolve_neuron_share_dir()
            _c24.NEURONHOME_DEFAULT = str(share)  # type: ignore[attr-defined]
        except (FileNotFoundError, ImportError):
            pass

        # Override NRNMECH_DLL to point at the Linux .so so t0090's generator
        # loads the compiled MOD library instead of the .dll on Linux.
        try:
            so_path = _resolve_t24_linux_so()
            _p24.NRNMECH_DLL = so_path  # type: ignore[attr-defined]
        except FileNotFoundError:
            pass

        def _noop_ensure_path() -> None:  # pragma: no cover -- monkey-patch
            return None

        _bc._ensure_neuron_on_path = _noop_ensure_path  # type: ignore[assignment]
        _bc.load_neuron = _patched_load_neuron_linux  # type: ignore[assignment]
    else:
        # Windows: ensure NEURONHOME is set in env.
        os.environ.setdefault("NEURONHOME", r"C:\Users\md1avn\nrn-8.2.7")
    _BOOTSTRAPPED = True


# Apply the bootstrap as a side-effect of importing this module so
# downstream importers don't have to remember to call bootstrap_neuron().
bootstrap_neuron()
