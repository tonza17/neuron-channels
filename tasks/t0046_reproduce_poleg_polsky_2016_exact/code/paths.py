"""Centralized path constants for t0046 (exact reproduction of Poleg-Polsky 2016).

All file paths used by simulation drivers, audit scripts, and figure renderers are defined here
per the project Python style guide. No code outside this module hardcodes paths.
"""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent

TASK_ID: str = "t0046_reproduce_poleg_polsky_2016_exact"
LIBRARY_ID: str = "modeldb_189347_dsgc_exact"
ANSWER_ID: str = "poleg-polsky-2016-reproduction-audit"

# Asset folders.
LIBRARY_ASSET_DIR: Path = TASK_ROOT / "assets" / "library" / LIBRARY_ID
LIBRARY_DETAILS_JSON: Path = LIBRARY_ASSET_DIR / "details.json"
LIBRARY_DESCRIPTION_MD: Path = LIBRARY_ASSET_DIR / "description.md"
LIBRARY_SOURCES_DIR: Path = LIBRARY_ASSET_DIR / "sources"

ANSWER_ASSET_DIR: Path = TASK_ROOT / "assets" / "answer" / ANSWER_ID
ANSWER_DETAILS_JSON: Path = ANSWER_ASSET_DIR / "details.json"
ANSWER_SHORT_MD: Path = ANSWER_ASSET_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ANSWER_ASSET_DIR / "full_answer.md"

# Code folder + ModelDB sources copied verbatim from t0008's library asset.
CODE_DIR: Path = TASK_ROOT / "code"
SOURCES_DIR: Path = CODE_DIR / "sources"
MAIN_HOC: Path = SOURCES_DIR / "main.hoc"
RGCMODEL_HOC: Path = SOURCES_DIR / "RGCmodel.hoc"
DSGC_MODEL_HOC: Path = SOURCES_DIR / "dsgc_model_exact.hoc"
RUN_NRNIVMODL_CMD: Path = CODE_DIR / "run_nrnivmodl.cmd"

# NEURON install (validated by t0007). nrnivmodl on Windows writes its dll into the source dir
# itself (mknrndll style), not into an x86_64 subdir.
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"
NRNMECH_DLL: Path = SOURCES_DIR / "nrnmech.dll"
NRNIVMODL_BAT: Path = Path(NEURONHOME_DEFAULT) / "bin" / "nrnivmodl.bat"

# Task data outputs.
DATA_DIR: Path = TASK_ROOT / "results" / "data"
FIG1_PSP_CSV: Path = DATA_DIR / "fig1_psp.csv"
FIG2_IMK801_PSP_CSV: Path = DATA_DIR / "fig2_imk801_psp.csv"
FIG3_GNMDA_SWEEP_CSV: Path = DATA_DIR / "fig3_gnmda_sweep.csv"
FIG4_HIGHCL_PSP_CSV: Path = DATA_DIR / "fig4_highcl_psp.csv"
FIG5_ZEROMG_PSP_CSV: Path = DATA_DIR / "fig5_zeromg_psp.csv"
FIG6_NOISE_CSV: Path = DATA_DIR / "fig6_noise.csv"
FIG7_ROC_CSV: Path = DATA_DIR / "fig7_roc.csv"
FIG7_ROC_NOISE_CSV: Path = DATA_DIR / "fig7_roc_noise.csv"
FIG8_SPIKES_CSV: Path = DATA_DIR / "fig8_spikes.csv"

# Task results.
RESULTS_DIR: Path = TASK_ROOT / "results"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
IMAGES_DIR: Path = RESULTS_DIR / "images"
FIG1_PNG: Path = IMAGES_DIR / "fig1_psp_vs_angle.png"
FIG2_PNG: Path = IMAGES_DIR / "fig2_imk801_psp.png"
FIG3_PNG: Path = IMAGES_DIR / "fig3_gnmda_sweep.png"
FIG4_PNG: Path = IMAGES_DIR / "fig4_highcl_psp.png"
FIG5_PNG: Path = IMAGES_DIR / "fig5_zeromg_psp.png"
FIG6_PNG: Path = IMAGES_DIR / "fig6_noise_dsi_by_sd.png"
FIG7_PNG: Path = IMAGES_DIR / "fig7_roc_noise.png"
FIG8_PNG: Path = IMAGES_DIR / "fig8_spike_tuning_and_failures.png"

# Corrections folder.
CORRECTIONS_DIR: Path = TASK_ROOT / "corrections"

# Existing paper asset (t0002) - destination for the supplementary PDF correction.
T0002_PAPER_ASSET_DIR: Path = (
    REPO_ROOT
    / "tasks"
    / "t0002_literature_survey_dsgc_compartmental_models"
    / "assets"
    / "paper"
    / "10.1016_j.neuron.2016.02.013"
)

# HOC path-safe (forward slashes) form of code/sources/.
SOURCES_DIR_HOC_SAFE: str = str(SOURCES_DIR).replace("\\", "/")
