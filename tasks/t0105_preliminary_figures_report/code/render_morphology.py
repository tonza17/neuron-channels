"""Copy Bed A and Bed B morphology PNGs verbatim from t0070 into this task's images/.

The radial-fan schematics live at
``tasks/t0070_writeup_two_model_beds/results/images/bed_{a,b}_morphology.png``
and are reused as-is per task_description.md and research_code.md.
"""

from __future__ import annotations

import shutil

from tasks.t0105_preliminary_figures_report.code import paths as pth


def copy_morphology_pngs() -> None:
    pth.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src=pth.T0070_BED_A_MORPH_PNG, dst=pth.FIG03_BED_A_MORPH_PNG)
    shutil.copy2(src=pth.T0070_BED_B_MORPH_PNG, dst=pth.FIG03_BED_B_MORPH_PNG)


def main() -> None:
    copy_morphology_pngs()
    print(f"[t0105] copied -> {pth.FIG03_BED_A_MORPH_PNG}")
    print(f"[t0105] copied -> {pth.FIG03_BED_B_MORPH_PNG}")


if __name__ == "__main__":
    main()
