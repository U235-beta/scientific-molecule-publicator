"""
Multi-panel figure generator for scientific publications.

Creates Figure 1-5 style composite figures with consistent layout,
panel labels, and unified styling. Supports mixed content types
(data plots, molecule structures, mechanism diagrams, images).

Integrates molecular-visualization skill for molecule panels.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pathlib import Path
from .style_config import (
    apply_journal_style, get_figure_size, save_figure,
    add_panel_label, mm_to_inch, OKABE_ITO, JOURNAL_STYLES
)
from . import data_plots
from . import mechanism_diagrams


class FigureGenerator:
    """Generate publication-quality multi-panel figures."""

    def __init__(self, journal="nature", double=True, aspect=0.7,
                 panel_labels="ABCDEFGHIJKLMNOP", dpi=None):
        self.journal = journal
        self.double = double
        self.aspect = aspect
        self.panel_labels = panel_labels
        self.dpi = dpi
        self.style = apply_journal_style(journal)
        self.fig = None
        self.axes = []

    def create_figure(self, layout="1x1", figsize=None, **kwargs):
        """Create figure with specified layout."""
        if figsize is None:
            w, h = get_figure_size(journal=self.journal, double=self.double,
                                   aspect=self.aspect)
            figsize = (w, h)

        if isinstance(layout, str) and "x" in layout:
            rows, cols = map(int, layout.split("x"))
            self.fig, self.axes = plt.subplots(rows, cols, figsize=figsize,
                                                squeeze=False, **kwargs)
            self.axes = self.axes.flatten().tolist()
        elif isinstance(layout, list):
            n_rows = len(layout)
            n_cols = max(len(row) for row in layout)
            self.fig = plt.figure(figsize=figsize, **kwargs)
            gs = gridspec.GridSpec(n_rows, n_cols, figure=self.fig)
            self.axes = []
            seen = set()
            for i, row in enumerate(layout):
                for j, panel_id in enumerate(row):
                    if panel_id not in seen:
                        seen.add(panel_id)
                        row_start, row_end = i, i
                        col_start, col_end = j, j
                        for r in range(n_rows):
                            for c in range(n_cols):
                                if r < len(layout) and c < len(layout[r]) and layout[r][c] == panel_id:
                                    row_end = max(row_end, r)
                                    col_end = max(col_end, c)
                        ax = self.fig.add_subplot(gs[row_start:row_end+1, col_start:col_end+1])
                        self.axes.append(ax)
        else:
            self.fig, ax = plt.subplots(figsize=figsize, **kwargs)
            self.axes = [ax]

        for i, ax in enumerate(self.axes):
            if i < len(self.panel_labels):
                add_panel_label(ax, self.panel_labels[i])
        return self.fig, self.axes

    def add_line_plot(self, ax, x, y_list, **kwargs):
        colors = kwargs.pop("colors", OKABE_ITO)
        labels = kwargs.pop("labels", None)
        markers = kwargs.pop("markers", ["o", "s", "^", "D", "v"][:len(y_list)])
        for i, y in enumerate(y_list):
            label = labels[i] if labels else f"Series {i+1}"
            ax.plot(x, y, label=label, color=colors[i % len(colors)],
                   marker=markers[i % len(markers)], markeredgewidth=0.5, **kwargs)
        if labels:
            ax.legend(frameon=False, fontsize=self.style["legend_size"])
        return ax

    def add_bar_plot(self, ax, categories, values_list, **kwargs):
        colors = kwargs.pop("colors", OKABE_ITO)
        labels = kwargs.pop("labels", None)
        n_series = len(values_list)
        n_groups = len(categories)
        bar_width = 0.7 / n_series if n_series > 1 else 0.7
        x = np.arange(n_groups)
        for i, values in enumerate(values_list):
            offset = (i - (n_series - 1) / 2) * bar_width if n_series > 1 else 0
            label = labels[i] if labels else f"Group {i+1}"
            ax.bar(x + offset, values, width=bar_width, label=label,
                  color=colors[i % len(colors)], **kwargs)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")
        if labels and n_series > 1:
            ax.legend(frameon=False, fontsize=self.style["legend_size"])
        return ax

    def add_scatter_plot(self, ax, x, y, **kwargs):
        ax.scatter(x, y, edgecolors="none", alpha=0.8, **kwargs)
        return ax

    def add_heatmap(self, ax, data, **kwargs):
        im = ax.imshow(data, aspect="auto", **kwargs)
        self.fig.colorbar(im, ax=ax, pad=0.02)
        return ax

    def add_text_panel(self, ax, text, title="", fontsize=None, **kwargs):
        ax.axis("off")
        fs = fontsize or self.style["font_size"] + 1
        if title:
            ax.text(0.5, 0.92, title, ha="center", va="top",
                   fontsize=fs + 1, fontweight="bold", transform=ax.transAxes)
            ax.text(0.5, 0.82, text, ha="center", va="top",
                   fontsize=fs, transform=ax.transAxes, wrap=True, **kwargs)
        else:
            ax.text(0.5, 0.5, text, ha="center", va="center",
                   fontsize=fs, transform=ax.transAxes, wrap=True, **kwargs)
        return ax

    def add_image_panel(self, ax, image_path, title="", **kwargs):
        from matplotlib.image import imread
        img = imread(image_path)
        ax.imshow(img, **kwargs)
        ax.axis("off")
        if title:
            ax.set_title(title, fontsize=self.style["title_size"])
        return ax

    def add_molecule_panel(self, ax, mol_json_path, show_orbitals=True,
                           show_electron_cloud=True, title=""):
        try:
            import sys
            molvis_path = Path(__file__).parent.parent.parent / "molecular-visualization" / "src"
            if molvis_path.exists():
                sys.path.insert(0, str(molvis_path))
                from molvis import load_mol, draw_ball_stick, draw_sp2_orbitals, draw_electron_cloud
                mol = load_mol(mol_json_path)
                draw_ball_stick(ax, mol)
                if show_orbitals:
                    draw_sp2_orbitals(ax, mol)
                if show_electron_cloud:
                    draw_electron_cloud(ax, mol)
                ax.set_aspect("equal")
                ax.axis("off")
            else:
                self.add_text_panel(ax, f"[Molecule: {Path(mol_json_path).stem}]\n(Install molecular-visualization skill)")
        except Exception as e:
            self.add_text_panel(ax, f"[Molecule render error]\n{str(e)[:50]}")
        if title:
            ax.set_title(title, fontsize=self.style["title_size"])
        return ax

    def add_mechanism_chain(self, ax, stages, **kwargs):
        ax.axis("off")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 3)
        n = len(stages)
        colors = kwargs.pop("colors", OKABE_ITO)
        box_w = 8.0 / n
        for i, stage in enumerate(stages):
            if isinstance(stage, tuple):
                label, desc = stage
            else:
                label, desc = stage, ""
            x = (10 - n * box_w) / (n + 1) + box_w/2 + i * (box_w + (10 - n * box_w) / (n + 1))
            y = 1.5
            box = FancyBboxPatch((x - box_w*0.4, y - 0.5), box_w*0.8, 1.0,
                                 boxstyle="round,pad=0.02", facecolor=colors[i % len(colors)],
                                 edgecolor="black", linewidth=0.8, alpha=0.8)
            ax.add_patch(box)
            ax.text(x, y, label, ha="center", va="center", fontsize=8, fontweight="bold")
            if i < n - 1:
                x_next = (10 - n * box_w) / (n + 1) + box_w/2 + (i+1) * (box_w + (10 - n * box_w) / (n + 1))
                ax.annotate("", xy=(x_next - box_w*0.4, y), xytext=(x + box_w*0.4, y),
                           arrowprops=dict(arrowstyle="->", lw=1.2, mutation_scale=10))
        return ax

    def set_axis_labels(self, ax, xlabel="", ylabel="", title=""):
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=self.style["label_size"])
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=self.style["label_size"])
        if title:
            ax.set_title(title, fontsize=self.style["title_size"])
        return ax

    def adjust_layout(self, tight=True, wspace=0.3, hspace=0.3):
        if tight:
            self.fig.tight_layout()
        self.fig.subplots_adjust(wspace=wspace, hspace=hspace)
        return self.fig

    def save(self, output_path, formats=("pdf", "png")):
        self.adjust_layout()
        return save_figure(self.fig, output_path, formats=formats, dpi=self.dpi)


def generate_figure_from_spec(spec, output_path):
    """Generate a figure from a specification dictionary."""
    gen = FigureGenerator(
        journal=spec.get("journal", "nature"),
        double=spec.get("double", True),
        aspect=spec.get("aspect", 0.7),
    )
    fig, axes = gen.create_figure(layout=spec.get("layout", "1x1"))

    for i, panel_spec in enumerate(spec.get("panels", [])):
        if i >= len(axes):
            break
        ax = axes[i]
        ptype = panel_spec.get("type", "text")

        if ptype == "line":
            gen.add_line_plot(ax, panel_spec["x"], panel_spec["y_list"],
                             **{k: v for k, v in panel_spec.items() if k not in ("type", "x", "y_list")})
            gen.set_axis_labels(ax, panel_spec.get("xlabel", ""),
                               panel_spec.get("ylabel", ""), panel_spec.get("title", ""))
        elif ptype == "bar":
            gen.add_bar_plot(ax, panel_spec["categories"], panel_spec["values_list"],
                           **{k: v for k, v in panel_spec.items() if k not in ("type", "categories", "values_list")})
            gen.set_axis_labels(ax, panel_spec.get("xlabel", ""),
                               panel_spec.get("ylabel", ""), panel_spec.get("title", ""))
        elif ptype == "scatter":
            gen.add_scatter_plot(ax, panel_spec["x"], panel_spec["y"],
                               **{k: v for k, v in panel_spec.items() if k not in ("type", "x", "y")})
        elif ptype == "heatmap":
            gen.add_heatmap(ax, panel_spec["data"],
                          **{k: v for k, v in panel_spec.items() if k != "type" and k != "data"})
        elif ptype == "text":
            gen.add_text_panel(ax, panel_spec.get("text", ""),
                             title=panel_spec.get("title", ""))
        elif ptype == "image":
            gen.add_image_panel(ax, panel_spec["path"],
                              title=panel_spec.get("title", ""))
        elif ptype == "molecule":
            gen.add_molecule_panel(ax, panel_spec["path"],
                                  show_orbitals=panel_spec.get("show_orbitals", True),
                                  show_electron_cloud=panel_spec.get("show_electron_cloud", True),
                                  title=panel_spec.get("title", ""))
        elif ptype == "mechanism":
            gen.add_mechanism_chain(ax, panel_spec["stages"])

    return gen.save(output_path)