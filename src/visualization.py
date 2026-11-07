from pathlib import Path
import matplotlib.pyplot as plt

# Locate project root dynamically
PROJECT_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if parent.name == "bioinformatics-ml-project"
)

FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def save_figure(name: str, dpi: int = 300) -> None:
    """Save the current Matplotlib figure."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        FIGURES_DIR / f"{name}.png",
        dpi=dpi,
        bbox_inches="tight"
    )