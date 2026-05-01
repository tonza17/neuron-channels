"""Output path constants for t0072 (synaptic traces PD vs ND)."""

from __future__ import annotations

from pathlib import Path

# Resolve absolute paths so HOC ``chdir`` calls (during cell construction)
# do not divert per-task data outputs to the upstream sources folder.
_THIS_FILE: Path = Path(__file__).resolve()
TASK_ROOT: Path = _THIS_FILE.parent.parent
REPO_ROOT: Path = TASK_ROOT.parent.parent
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"

# Bed A raw trace .npz files (8 files: 4 synapse types x 2 directions).
BED_A_PD_AMPA_NPZ: Path = DATA_DIR / "bed_a_pd_ampa.npz"
BED_A_ND_AMPA_NPZ: Path = DATA_DIR / "bed_a_nd_ampa.npz"
BED_A_PD_NMDA_NPZ: Path = DATA_DIR / "bed_a_pd_nmda.npz"
BED_A_ND_NMDA_NPZ: Path = DATA_DIR / "bed_a_nd_nmda.npz"
BED_A_PD_GABA_NPZ: Path = DATA_DIR / "bed_a_pd_gaba.npz"
BED_A_ND_GABA_NPZ: Path = DATA_DIR / "bed_a_nd_gaba.npz"
BED_A_PD_ACH_NPZ: Path = DATA_DIR / "bed_a_pd_ach.npz"
BED_A_ND_ACH_NPZ: Path = DATA_DIR / "bed_a_nd_ach.npz"

# Bed B raw trace .npz files (4 files: 2 synapse types x 2 directions).
BED_B_PD_ACH_NPZ: Path = DATA_DIR / "bed_b_pd_ach.npz"
BED_B_ND_ACH_NPZ: Path = DATA_DIR / "bed_b_nd_ach.npz"
BED_B_PD_GABA_NPZ: Path = DATA_DIR / "bed_b_pd_gaba.npz"
BED_B_ND_GABA_NPZ: Path = DATA_DIR / "bed_b_nd_gaba.npz"

# Aggregated mean/SD output.
AGGREGATED_NPZ: Path = DATA_DIR / "aggregated.npz"

# Figures.
BED_A_FIG_PNG: Path = IMAGES_DIR / "bed_a_synaptic_traces.png"
BED_B_FIG_PNG: Path = IMAGES_DIR / "bed_b_synaptic_traces.png"

# Typst writeup.
TYPST_SOURCE_PATH: Path = RESULTS_DIR / "results_detailed.typ"
PDF_OUTPUT_PATH: Path = RESULTS_DIR / "results_detailed.pdf"
