---
spec_version: "2"
library_id: "tuning_curve_viz"
documented_by_task: "t0011_response_visualization_library"
date_documented: "2026-04-20"
---
# Tuning Curve Visualizer

## Metadata

* **Name**: Tuning Curve Visualizer
* **Version**: 0.1.0
* **Task**: `t0011_response_visualization_library`
* **Dependencies**: numpy, pandas, matplotlib, scipy
* **Modules**: `code/tuning_curve_viz/cartesian.py`, `code/tuning_curve_viz/polar.py`,
  `code/tuning_curve_viz/overlay.py`, `code/tuning_curve_viz/raster_psth.py`,
  `code/tuning_curve_viz/cli.py`, `code/tuning_curve_viz/loaders.py`,
  `code/tuning_curve_viz/stats.py`, `code/tuning_curve_viz/constants.py`,
  `code/tuning_curve_viz/paths.py`

## Overview

`tuning_curve_viz` is the project's canonical matplotlib wrapper for turning firing-rate-vs-angle
data into publication-ready PNG figures. It accepts the three canonical tuning-curve CSV schemas
used across the project — canonical `(angle_deg, trial_seed, firing_rate_hz)`, the t0004 per-trial
layout `(angle_deg, trial_index, rate_hz)`, and the t0004 mean layout `(angle_deg, mean_rate_hz)` —
via a thin wrapper over the loader from `tasks.t0012_tuning_curve_scoring_loss_library`.

The library exposes four plot primitives — Cartesian, polar, multi-model overlay, and per-angle
raster+PSTH — plus a small `argparse` command-line interface. Every plot uses the eight-colour
Okabe-Ito palette (with black reserved for the target curve) to stay colour-blind safe, dashes the
target overlay so it can never be confused with a candidate model, and always closes the matplotlib
figure with `plt.close(fig=fig)` so long-running loops do not leak figures. All PNGs are written at
150 DPI with a tight bounding box and a white facecolour.

The library is the PNG producer for downstream scoring, human-review, and paper-figure tasks. Task
t0012 consumes the same CSV schemas, so any curve file produced by t0004 or t0008 can be rendered
without format conversion.

## API Reference

All public functions live under `tasks.t0011_response_visualization_library.code.tuning_curve_viz`
and accept `pathlib.Path` arguments only.

### `plot_cartesian_tuning_curve`

```python
def plot_cartesian_tuning_curve(
    curve_csv: Path,
    out_png: Path,
    *,
    show_trials: bool = True,
    target_csv: Path | None = None,
) -> None: ...
```

Renders firing rate (Hz) vs direction (deg) as a line plot with markers. When `show_trials=True` and
the CSV carries per-trial rows the individual trials are drawn as translucent scatter and a 95
percent bootstrap confidence-interval band (1000 resamples via `scipy.stats.bootstrap`, seed =
`SMOKE_RNG_SEED`) is shaded around the mean. When `target_csv` is supplied it is overlaid as a
dashed black line labelled `"target"`.

### `plot_polar_tuning_curve`

```python
def plot_polar_tuning_curve(
    curve_csv: Path,
    out_png: Path,
    *,
    target_csv: Path | None = None,
) -> None: ...
```

Polar projection with the default matplotlib convention (`theta_direction=1`, CCW, `theta_offset=0`
at east). Input angles are never transformed. The preferred direction — the angle of the maximum
per-angle mean — is annotated with a red arrow from the origin. Optional `target_csv` is drawn as a
dashed black closed curve.

### `plot_multi_model_overlay`

```python
def plot_multi_model_overlay(
    curves_dict: dict[str, Path],
    out_png: Path,
    *,
    target_csv: Path | None = None,
) -> None: ...
```

Side-by-side Cartesian (left) and polar (right) figure that overlays several candidate models drawn
in distinct Okabe-Ito colours. When more than `MAX_OVERLAY_MODELS` (= 6) models are supplied the
function emits a `UserWarning` and truncates to the first six keys (insertion order). Optional
`target_csv` is always dashed black.

### `plot_angle_raster_psth`

```python
def plot_angle_raster_psth(
    spike_times_csv: Path,
    out_png: Path,
    *,
    angle_deg: float,
) -> None: ...
```

Per-angle spike raster above a PSTH histogram arranged via `GridSpec(2, 1, height_ratios=[3, 1])`
with shared time axis. Reads a CSV with columns `(angle_deg, trial_index, spike_time_s)`, filters
rows to the requested angle, and draws an `eventplot` raster (one row per trial) plus a 10 ms-bin
histogram (`PSTH_BIN_WIDTH_S`). Raises `ValueError` when no rows match the requested angle or when
required columns are missing.

### `tuning_curve_viz.cli`

```text
python -m tasks.t0011_response_visualization_library.code.tuning_curve_viz.cli \
    --curve-csv CURVE_CSV --out-dir OUT_DIR \
    [--target-csv TARGET_CSV] [--spike-times-csv SPIKE_TIMES_CSV] \
    [--curve-label CURVE_LABEL]
```

Renders `cartesian.png`, `polar.png`, `overlay.png` (if `--target-csv`), and one
`raster_psth_<deg>deg.png` per distinct `angle_deg` value in `--spike-times-csv`.

## Usage Examples

Render a single Cartesian plot with trials and a 95 percent CI band:

```python
from pathlib import Path
from tasks.t0011_response_visualization_library.code.tuning_curve_viz import (
    plot_cartesian_tuning_curve,
    plot_polar_tuning_curve,
    plot_multi_model_overlay,
)

target_csv = Path(
    "tasks/t0004_generate_target_tuning_curve/assets/dataset/"
    "target-tuning-curve/files/curve_mean.csv"
)
t0008_csv = Path(
    "tasks/t0008_port_modeldb_189347/data/tuning_curves/curve_modeldb_189347.csv"
)

plot_cartesian_tuning_curve(
    curve_csv=t0008_csv,
    out_png=Path("out/t0008_cartesian.png"),
    show_trials=True,
    target_csv=target_csv,
)
plot_polar_tuning_curve(
    curve_csv=t0008_csv,
    out_png=Path("out/t0008_polar.png"),
    target_csv=target_csv,
)
plot_multi_model_overlay(
    curves_dict={
        "target_mean": target_csv,
        "t0008_simulated": t0008_csv,
    },
    out_png=Path("out/overlay.png"),
    target_csv=target_csv,
)
```

Render raster+PSTH for a single angle from a spike-time CSV:

```python
from pathlib import Path
from tasks.t0011_response_visualization_library.code.tuning_curve_viz import (
    plot_angle_raster_psth,
)

plot_angle_raster_psth(
    spike_times_csv=Path("spikes.csv"),
    out_png=Path("out/raster_psth_90deg.png"),
    angle_deg=90.0,
)
```

## Dependencies

* **numpy** — array maths for angle grids, per-trial stacks, and the bootstrap fallback.
* **pandas** — reading the three supported CSV schemas, and selecting rows by `angle_deg` for the
  raster+PSTH plot.
* **matplotlib** — all plotting (`pyplot`, `GridSpec`, `projections.polar.PolarAxes`).
* **scipy** — `scipy.stats.bootstrap` powers the default 95 percent CI computation. When scipy is
  unavailable the library transparently falls back to a seeded NumPy percentile bootstrap so the
  plotting code path stays functional in minimal environments.

The library also imports `load_tuning_curve` and the `TuningCurve` dataclass from
`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader`. This is a cross-task
import of a library asset, allowed because t0012 publishes a library.

## Testing

The library ships with a smoke test that renders every plot type against real project data:

```bash
uv run python -u -m \
    tasks.t0011_response_visualization_library.code.tuning_curve_viz.test_smoke
```

It produces seven PNGs in `assets/library/tuning_curve_viz/files/`:

1. `target_cartesian.png` — t0004 target (mean + trials + 95 percent CI).
2. `target_polar.png` — t0004 target in polar form.
3. `t0008_cartesian.png` — t0008 simulated curve with target overlay.
4. `t0008_polar.png` — t0008 simulated curve in polar form with target overlay.
5. `overlay_target_vs_t0008.png` — two-model overlay with target dashed overlay.
6. `raster_psth_0deg.png` — synthetic Poisson raster+PSTH at 0 deg.
7. `raster_psth_90deg.png` — synthetic Poisson raster+PSTH at 90 deg.

The raster+PSTH plots use a deterministic `numpy.random.Generator` seeded with `SMOKE_RNG_SEED` (=
42\) so repeated runs produce byte-identical PNGs. The module is intentionally named `test_smoke.py`
but is not picked up by `pytest`: every public callable begins with an underscore or is `run_all`,
and there are no `def test_*` functions. Run it as a script, not with pytest.

## Main Ideas

* The library is a thin presentation layer — it never transforms angles, never re-normalizes rates,
  and delegates all CSV parsing to the t0012 loader. What goes in is what gets plotted.
* The Okabe-Ito eight-colour palette is the only palette used; black is reserved exclusively for the
  optional target overlay, and the target is always dashed so it is unambiguous.
* Figures are always closed with `plt.close(fig=fig)` after writing to PNG so batch jobs and long
  CLI loops never leak figures. DPI, facecolour, and `bbox_inches` are centralized in `constants.py`
  (`DEFAULT_DPI=150`, `DEFAULT_FACECOLOR="white"`, `DEFAULT_BBOX_INCHES="tight"`).
* Overlays cap at six models (`MAX_OVERLAY_MODELS`) to preserve palette distinguishability; a
  `UserWarning` is emitted and later keys are dropped rather than recycled colours.
* Angle grids are validated permissively: the plotting functions accept 8, 12, or 16-sample uniform
  grids (`ACCEPTED_ANGLE_COUNTS`), so any curve produced by t0004, t0008, or a future task with one
  of those sampling densities renders without change.

## Summary

`tuning_curve_viz` is the project's matplotlib front end for every firing-rate-vs-direction figure.
It renders Cartesian, polar, side-by-side multi-model overlay, and per-angle raster+PSTH panels from
the three canonical CSV schemas shared with the t0012 scoring library. A 95 percent bootstrap
confidence band (`scipy.stats.bootstrap`, 1000 resamples) sits on top of every Cartesian plot that
has per-trial data, a red preferred-direction arrow annotates every polar plot, and the optional
target overlay is always drawn dashed in black.

The library is consumed by downstream scoring and human-review tasks (starting with t0011 itself,
which bundles a seven-panel smoke test written straight into the library asset folder) as well as by
the paper-figure pipeline. Tasks that produce a tuning-curve CSV or a spike-time CSV in the standard
schema can call the entry points directly without preprocessing — no angle remapping, no rate
rescaling, no unit conversion. The companion `tuning_curve_viz.cli` script supports the same
workflow from the shell, which keeps the library usable by agents that prefer scripted invocation
over Python imports.
