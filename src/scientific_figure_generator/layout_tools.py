"""
Layout tools for multi-panel scientific figures.

Provides:
- add_panel_labels(): Add aligned a/b/c/d panel labels in unified figure coordinates
- finalize_figure(): Clean up layout with constrained/tight layout fallback
- align_axes(): Align axes across subplots

Inspired by scipilot-figure-skill layout_tools.py.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
import numpy as np


def add_panel_labels(fig, style="nature", labels=None, fontsize=None,
                     fontweight="bold", x_offset=0.0, y_offset=0.0):
    """
    Add aligned panel labels (a/b/c/d) to a multi-panel figure.

    Uses unified figure coordinates so labels align both horizontally and vertically,
    unlike manual ax.text() which is prone to misalignment.

    Args:
        fig: matplotlib Figure
        style: Label style - 'nature' (a, b, c), 'ieee' ((a), (b), (c)), 'cell' (A, B, C)
        labels: Custom list of labels (overrides style)
        fontsize: Font size (default: based on journal style)
        fontweight: Font weight (default: 'bold')
        x_offset: Additional x offset in figure fraction
        y_offset: Additional y offset in figure fraction

    Returns:
        List of Text objects
    """
    axes = []
    for ax in fig.axes:
        pos = ax.get_position()
        if pos.width > 0.02 and pos.height > 0.02:
            axes.append(ax)

    if not axes:
        return []

    if labels is None:
        if style == "nature":
            labels = [chr(ord("a") + i) for i in range(len(axes))]
        elif style == "ieee":
            labels = [f"({chr(ord('a') + i)})" for i in range(len(axes))]
        elif style == "cell":
            labels = [chr(ord("A") + i) for i in range(len(axes))]
        else:
            labels = [chr(ord("a") + i) for i in range(len(axes))]

    if fontsize is None:
        fontsize = 10 if style == "cell" else 9

    text_objects = []
    for i, ax in enumerate(axes):
        if i >= len(labels):
            break
        pos = ax.get_position()
        x = pos.x0 + x_offset
        y = pos.y1 + y_offset + 0.005

        label = fig.text(
            x, y, labels[i],
            fontsize=fontsize,
            fontweight=fontweight,
            ha="left", va="bottom",
            transform=fig.transFigure
        )
        text_objects.append(label)

    return text_objects


def finalize_figure(fig, method="constrained", tight_pad=1.5, h_pad=None, w_pad=None):
    """
    Clean up figure layout with fallback strategy.

    Tries constrained_layout first, falls back to tight_layout, then manual adjustment.
    """
    if h_pad is None:
        h_pad = tight_pad
    if w_pad is None:
        w_pad = tight_pad

    if method == "constrained":
        try:
            fig.set_constrained_layout(True)
            fig.execute_constrained_layout()
        except Exception:
            method = "tight"

    if method == "tight":
        try:
            fig.tight_layout(pad=tight_pad, h_pad=h_pad, w_pad=w_pad)
        except Exception:
            method = "manual"

    if method == "manual":
        fig.subplots_adjust(
            left=0.1, right=0.95,
            top=0.92, bottom=0.1,
            hspace=0.3, wspace=0.25
        )


def align_axes(fig, axes=None, align="x"):
    """
    Align axes positions across subplots.

    Args:
        fig: matplotlib Figure
        axes: List of axes to align (default: all axes)
        align: 'x' (align left/right edges), 'y' (align top/bottom edges), or 'both'
    """
    if axes is None:
        axes = [ax for ax in fig.axes if ax.get_position().width > 0.02]

    if len(axes) < 2:
        return

    positions = [ax.get_position() for ax in axes]

    if align in ("x", "both"):
        lefts = [p.x0 for p in positions]
        median_left = np.median(lefts)
        for ax, pos in zip(axes, positions):
            ax.set_position([median_left, pos.y0, pos.width, pos.height])

    if align in ("y", "both"):
        tops = [p.y1 for p in positions]
        median_top = np.median(tops)
        for ax, pos in zip(axes, positions):
            new_y0 = median_top - pos.height
            ax.set_position([pos.x0, new_y0, pos.width, pos.height])


def add_letter_labels(ax, labels, positions=None, fontsize=10, fontweight="bold"):
    """
    Add letter labels within a single axes (for sub-panels inside one axes).
    """
    if positions is None:
        n = len(labels)
        positions = [(0.02 + i * (0.96 / max(n - 1, 1)), 0.95) for i in range(n)]

    texts = []
    for label, (x, y) in zip(labels, positions):
        t = ax.text(
            x, y, label,
            transform=ax.transAxes,
            fontsize=fontsize,
            fontweight=fontweight,
            ha="left", va="top"
        )
        texts.append(t)
    return texts


def make_room_for_legend(fig, ax, location="right", width=0.2):
    """
    Adjust axes to make room for an external legend.
    """
    pos = ax.get_position()
    if location == "right":
        ax.set_position([pos.x0, pos.y0, pos.width * (1 - width), pos.height])
    elif location == "left":
        ax.set_position([pos.x0 + pos.width * width, pos.y0, pos.width * (1 - width), pos.height])
    elif location == "top":
        ax.set_position([pos.x0, pos.y0, pos.width, pos.height * (1 - width)])
    elif location == "bottom":
        ax.set_position([pos.x0, pos.y0 + pos.height * width, pos.width, pos.height * (1 - width)])