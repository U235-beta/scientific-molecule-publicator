"""
Example: Generate a publication-quality multi-panel figure.

Demonstrates: FigureGenerator with 2x2 layout, line plot, bar plot,
mechanism diagram, text panel, quality checking.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
from scientific_figure_generator import (
    FigureGenerator,
    FigureQualityChecker,
)


def main():
    np.random.seed(42)
    x = np.linspace(0, 48, 20)

    y_control = 100 * np.exp(-x / 24) + np.random.normal(0, 3, len(x))
    y_treatment = 100 * np.exp(-x / 12) + 50 + np.random.normal(0, 4, len(x))

    polymers = ["PET", "PS", "PC", "ABS", "PVC", "PLA", "PE", "PP"]
    fluorescence = [85, 45, 72, 60, 55, 40, 12, 8]
    errors = [8, 5, 7, 6, 5, 4, 2, 1]

    gen = FigureGenerator(journal="nature", double=True, aspect=0.75)
    fig, axes = gen.create_figure(layout="2x2")

    gen.add_line_plot(axes[0], x, [y_control, y_treatment],
        labels=["Control", "UV-aged"], markers=["o", "s"])
    gen.set_axis_labels(axes[0], xlabel="Aging time (h)",
        ylabel="Fluorescence intensity (a.u.)", title="Fluorescence decay under UV exposure")
    axes[0].legend(frameon=False, loc="upper right")

    gen.add_bar_plot(axes[1], polymers, [fluorescence], colors=["#0072B2"])
    x_pos = np.arange(len(polymers))
    axes[1].errorbar(x_pos, fluorescence, yerr=errors, fmt="none",
                     ecolor="black", capsize=2, elinewidth=0.8)
    gen.set_axis_labels(axes[1], xlabel="Polymer type",
        ylabel="Autofluorescence (a.u.)", title="Intrinsic autofluorescence by polymer")

    gen.add_mechanism_chain(axes[2], [
        ("Pure polymer", "Weak baseline"),
        ("+ Additives", "Dominant signal"),
        ("+ Aging", "Spectral drift"),
        ("Mixed output", "Uncertain signal"),
    ])
    axes[2].set_title("Causal chain: fluorescence signal composition",
                       fontsize=gen.style["title_size"])

    gen.add_text_panel(axes[3],
        "Commercial plastic fluorescence is\ndominated by additives (>80%),\nnot polymer backbone.\n\nAging causes 15-30 nm red shift.\n\nNew-particle calibration curves\nsystematically underestimate\nenvironmental sample fluorescence.",
        title="Key Findings")

    checker = FigureQualityChecker(journal="nature")
    issues = checker.check(fig)
    print("\n" + "=" * 50 + "\nQUALITY CHECK REPORT\n" + "=" * 50)
    checker.report(issues)

    output_dir = Path(__file__).parent
    output_path = output_dir / "example_multipanel_figure"
    paths = gen.save(str(output_path))
    print(f"\nFigure saved to: {paths}")
    return fig, axes


if __name__ == "__main__":
    main()