---
task_id: "t0007_install_neuron_netpyne"
intervention_id: "python_version_mismatch"
filed_at: "2026-04-19T21:40:00Z"
severity: "blocker"
---
# Intervention Required: Pin project Python to 3.13 (or lower) for NEURON 8.2.7

## Summary

The project's uv virtualenv is running **Python 3.14.4**, but the only NEURON 8.2.7 Windows
installer published on GitHub is `nrn-8.2.7.w64-mingw-py-39-310-311-312-313-setup.exe` — it
bundles Python bindings (`.pyd` files) for **Python 3.9 - 3.13 only**. `import neuron` will fail
with `ImportError: DLL load failed` on Python 3.14 regardless of how we wire the package in via
`.pth`.

This matches Risk Row 4 in `plan/plan.md`: *"NEURON's Python package incompatible with uv venv's
Python version"*. The plan assumed the venv was 3.11; it is 3.14.

## Evidence

* `uv run python -c "import sys; print(sys.version)"` →
  `3.14.4 (main, Apr 14 2026, 14:30:57) [MSC v.1944 64 bit (AMD64)]`
* NEURON 8.2.7 release assets (from
  `https://api.github.com/repos/neuronsimulator/nrn/releases/tags/8.2.7`):
  * `nrn-8.2.7-macosx-10.13-universal2-py-39-310-311-312-313.pkg` (macOS)
  * `nrn-8.2.7.w64-mingw-py-39-310-311-312-313-setup.exe` (Windows, 39.9 MB) — **only Python
    3.9-3.13**
  * `nrn-full-src-package-8.2.7.tar.gz` (source)
* `pyproject.toml` currently has `requires-python = ">=3.12"`, so Python 3.13 is already allowed by
  the project's constraint — we just need to pick 3.13 over 3.14.

## What the User Must Decide

Pick one of:

### Option 1 (recommended): pin the project uv venv to Python 3.13

Minimal project-wide change. Python 3.13 satisfies `requires-python = ">=3.12"` and all project
dependencies (pandas, numpy, matplotlib, pydantic, vastai, openai, pymupdf, pyyaml, tqdm) have
Python 3.13 wheels. Concretely:

1. Tighten `pyproject.toml` to `requires-python = ">=3.12,<3.14"` so uv picks 3.13.
2. Write `.python-version` at repo root containing the single line `3.13`.
3. Delete `.venv/` and re-run `uv sync` to rebuild on Python 3.13.
4. Resume t0007 at plan step 1 (download the installer).

Impact on other tasks: very low. Any task running in a worktree off a commit that predates the pin
will keep its own 3.14 venv until the next `uv sync`; after rebase + sync, they all move to 3.13.
None of the framework code requires 3.14-specific features.

### Option 2: per-task Python 3.13 venv, keep project on 3.14

Leave the project's main venv on 3.14. Create a secondary venv *inside this task's worktree* (e.g.,
`.venv-nrn/`) at Python 3.13, install NEURON `.pth` wire + NetPyNE there, and run all t0007
implementation commands against that secondary venv. Downstream tasks (t0008, t0010, t0011) that
need NEURON would also need to use the secondary venv.

This breaks the single-toolchain discipline stated in `plan/plan.md` `## Approach` and makes
downstream tasks more complex. Not recommended unless 3.14 is needed elsewhere in the project.

### Option 3: upgrade the NEURON version to one that ships 3.14 wheels

NEURON 8.2.7 is pinned by `task.json` `short_description`. If the user is willing to loosen that, we
could target the latest 8.2.x or 9.0 release if it ships a `py-314` installer. This would require:

1. Updating `task.json` `short_description` + `task_description.md` to allow "latest 8.2.x" or
   similar.
2. Checking `https://api.github.com/repos/neuronsimulator/nrn/releases` for a release with 3.14
   bindings.
3. Re-running research to confirm API compatibility.

Not recommended because it changes the task's scope.

## Verification After Intervention

If Option 1 is chosen:

```bash
uv run python -c "import sys; print(sys.version_info[:2])"   # expect (3, 13)
```

Then resume at plan step 1.

## Resumption Procedure

1. User picks Option 1, 2, or 3 and reports the choice.
2. If Option 1: tighten `requires-python`, write `.python-version`, rebuild venv.
3. If Option 2: create `.venv-nrn/` per-task venv, update plan to reference it in every `uv run`
   invocation.
4. If Option 3: revise `task.json` + plan to target a newer NEURON version.
5. Resume implementation at plan step 1 (download the installer with the correct Python-suffix asset
   name).

## Blocking Steps

This intervention blocks:

* `implementation` (currently in_progress; plan steps 2-8 all depend on a working `import neuron`)
* `results`
* `suggestions`
* `reporting`

Downstream parallel tasks `t0009`, `t0012`, `t0013` do not depend on t0007 and can still run.
