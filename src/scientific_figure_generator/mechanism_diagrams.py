"""
Mechanism diagrams and conceptual frameworks for scientific publications.

Generates: causal chains, reaction pathways, process flows,
conceptual frameworks, mechanism schematics, comparison diagrams.

Uses matplotlib primitives (patches, arrows, text) for vector output.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.lines import Line2D
import numpy as np
from .style_config import apply_journal_style, save_figure, mm_to_inch, OKABE_ITO


def draw_box(ax, x, y, w, h, text, color="#E8E8E8", text_color="black",
             fontsize=8, fontweight="normal", rounded=True, alpha=1.0,
             edgecolor="black", linewidth=0.8, **kwargs):
    """Draw a labeled box."""
    if rounded:
        box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor=edgecolor,
                             linewidth=linewidth, alpha=alpha, **kwargs)
    else:
        box = Rectangle((x - w/2, y - h/2), w, h,
                       facecolor=color, edgecolor=edgecolor,
                       linewidth=linewidth, alpha=alpha, **kwargs)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
           fontweight=fontweight, color=text_color, wrap=True)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color="black", linewidth=1.0,
               arrowstyle="->", mutation_scale=10, connectionstyle="arc3,rad=0",
               **kwargs):
    """Draw an arrow between two points."""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=arrowstyle, mutation_scale=mutation_scale,
                            color=color, linewidth=linewidth,
                            connectionstyle=connectionstyle, **kwargs)
    ax.add_patch(arrow)
    return arrow


def causal_chain(stages, title="", journal="nature", double=True,
                 aspect=0.4, colors=None, output_path=None, **kwargs):
    """Draw a horizontal causal chain diagram (A -> B -> C -> ...)."""
    apply_journal_style(journal)
    fig, ax = plt.subplots(figsize=(mm_to_inch(180), mm_to_inch(180 * aspect)))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")

    n = len(stages)
    colors = colors or OKABE_ITO
    box_w = 8.0 / n
    box_h = 1.2
    spacing = (10 - n * box_w) / (n + 1)

    for i, stage in enumerate(stages):
        if isinstance(stage, tuple):
            label, desc = stage
        else:
            label, desc = stage, ""
        x = spacing + box_w/2 + i * (box_w + spacing)
        y = 1.5
        draw_box(ax, x, y, box_w * 0.9, box_h, label,
                color=colors[i % len(colors)], fontsize=9, fontweight="bold")
        if desc:
            ax.text(x, y - box_h/2 - 0.15, desc, ha="center", va="top",
                   fontsize=7, color="#555555", wrap=True)
        if i < n - 1:
            x_next = spacing + box_w/2 + (i+1) * (box_w + spacing)
            draw_arrow(ax, x + box_w*0.45, y, x_next - box_w*0.45, y,
                      linewidth=1.2, mutation_scale=12)

    if title:
        ax.text(5, 2.7, title, ha="center", va="center", fontsize=11, fontweight="bold")
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def layered_framework(layers, title="", journal="nature", double=True,
                      aspect=0.6, colors=None, output_path=None, **kwargs):
    """Draw a layered conceptual framework (stacked horizontal layers)."""
    apply_journal_style(journal)
    fig, ax = plt.subplots(figsize=(mm_to_inch(160), mm_to_inch(160 * aspect)))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(layers) + 1)
    ax.axis("off")

    default_colors = OKABE_ITO
    for i, layer in enumerate(reversed(layers)):
        if isinstance(layer, tuple):
            if len(layer) == 3:
                label, desc, color = layer
            else:
                label, desc = layer
                color = default_colors[i % len(default_colors)]
        else:
            label, desc, color = layer, "", default_colors[i % len(default_colors)]
        y = i + 0.5
        draw_box(ax, 5, y, 9, 0.85, f"{label}: {desc}" if desc else label,
                color=color, fontsize=9, fontweight="bold", alpha=0.8)

    if title:
        ax.text(5, len(layers) + 0.5, title, ha="center", va="center",
               fontsize=11, fontweight="bold")
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def process_flow(steps, title="", journal="nature", double=True,
                 aspect=0.5, colors=None, output_path=None, **kwargs):
    """Draw a vertical process flow with numbered steps."""
    apply_journal_style(journal)
    n = len(steps)
    fig, ax = plt.subplots(figsize=(mm_to_inch(140), mm_to_inch(140 * aspect)))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, n * 1.5 + 0.5)
    ax.axis("off")

    colors = colors or OKABE_ITO
    for i, step in enumerate(steps):
        if isinstance(step, tuple):
            title_step, desc = step
        else:
            title_step, desc = step, ""
        y = (n - 1 - i) * 1.5 + 1.0

        circle = Circle((1.2, y), 0.35, facecolor=colors[i % len(colors)],
                       edgecolor="black", linewidth=0.8, zorder=2)
        ax.add_patch(circle)
        ax.text(1.2, y, str(i+1), ha="center", va="center",
               fontsize=10, fontweight="bold", color="white", zorder=3)

        draw_box(ax, 5.8, y, 7.5, 1.0, f"{title_step}\n{desc}" if desc else title_step,
                color="#F5F5F5", fontsize=8, fontweight="normal", alpha=0.9)

        if i < n - 1:
            draw_arrow(ax, 1.2, y - 0.4, 1.2, y - 1.1, linewidth=1.2, mutation_scale=10)

    if title:
        ax.text(5, n * 1.5 + 0.2, title, ha="center", va="center",
               fontsize=11, fontweight="bold")
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def comparison_diagram(left_items, right_items, left_title="", right_title="",
                       title="", journal="nature", double=True, aspect=0.7,
                       left_color="#56B4E9", right_color="#E69F00",
                       output_path=None, **kwargs):
    """Draw a side-by-side comparison diagram."""
    apply_journal_style(journal)
    n = max(len(left_items), len(right_items))
    fig, ax = plt.subplots(figsize=(mm_to_inch(170), mm_to_inch(170 * aspect)))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, n + 2)
    ax.axis("off")

    draw_box(ax, 2.5, n + 1, 4, 0.7, left_title, color=left_color,
            fontsize=10, fontweight="bold", alpha=0.8)
    draw_box(ax, 7.5, n + 1, 4, 0.7, right_title, color=right_color,
            fontsize=10, fontweight="bold", alpha=0.8)

    for i in range(n):
        y = n - i + 0.2
        if i < len(left_items):
            draw_box(ax, 2.5, y, 4, 0.7, left_items[i], color="#F0F8FF",
                    fontsize=8, alpha=0.9)
        if i < len(right_items):
            draw_box(ax, 7.5, y, 4, 0.7, right_items[i], color="#FFF8E7",
                    fontsize=8, alpha=0.9)

    if title:
        ax.text(5, n + 1.8, title, ha="center", va="center",
               fontsize=11, fontweight="bold")
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def uncertainty_propagation_chain(stages, title="Uncertainty Propagation Chain",
                                   journal="nature", double=True, aspect=0.45,
                                   output_path=None, **kwargs):
    """Draw an uncertainty propagation chain with error sources and CV% annotations."""
    apply_journal_style(journal)
    n = len(stages)
    fig, ax = plt.subplots(figsize=(mm_to_inch(185), mm_to_inch(185 * aspect)))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    box_w = 8.5 / n
    box_h = 1.0
    spacing = (10 - n * box_w) / (n + 1)

    for i, stage in enumerate(stages):
        name, error_src, cv, direction = stage
        x = spacing + box_w/2 + i * (box_w + spacing)
        y = 2.2

        color = "#D55E00" if direction == "overestimate" else "#0072B2"
        draw_box(ax, x, y, box_w * 0.9, box_h, name,
                color=color, fontsize=8, fontweight="bold", alpha=0.7)

        ax.text(x, y - box_h/2 - 0.1, error_src, ha="center", va="top",
               fontsize=6.5, color="#555555", style="italic")

        badge_color = "#F0E442" if cv < 10 else "#E69F00" if cv < 25 else "#D55E00"
        draw_box(ax, x, y + box_h/2 + 0.25, box_w * 0.5, 0.35,
                f"CV={cv}%", color=badge_color, fontsize=7, fontweight="bold",
                rounded=False, linewidth=0.5)

        if i < n - 1:
            x_next = spacing + box_w/2 + (i+1) * (box_w + spacing)
            arrow_w = 1.5 if direction == "overestimate" else 0.8
            draw_arrow(ax, x + box_w*0.45, y, x_next - box_w*0.45, y,
                      linewidth=arrow_w, mutation_scale=12,
                      color="#D55E00" if direction == "overestimate" else "black")

    legend_elements = [
        mpatches.Patch(facecolor="#D55E00", alpha=0.7, label="Overestimate"),
        mpatches.Patch(facecolor="#0072B2", alpha=0.7, label="Underestimate"),
        Line2D([0], [0], color="#D55E00", linewidth=1.5, label="Error amplified"),
        Line2D([0], [0], color="black", linewidth=0.8, label="Error preserved"),
    ]
    ax.legend(handles=legend_elements, loc="lower center", ncol=4,
             frameon=False, fontsize=7, bbox_to_anchor=(0.5, -0.05))

    ax.text(5, 3.6, title, ha="center", va="center", fontsize=11, fontweight="bold")
    if output_path:
        save_figure(fig, output_path)
    return fig, ax