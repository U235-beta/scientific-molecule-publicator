"""
Data plot generators for scientific publications.

Covers: line, bar, scatter, heatmap, boxplot, violin, histogram,
errorbar, regression, dual-axis, multi-series, polar, ternary.

All functions accept journal style parameters and return (fig, ax).
"""

import numpy as np
from .style_config import create_figure, save_figure, add_panel_label, OKABE_ITO


def plot_line(x, y_list, labels=None, xlabel="", ylabel="", title="",
              journal="nature", double=False, aspect=0.7,
              colors=None, linestyles=None, markers=None,
              yerr_list=None, log_x=False, log_y=False,
              xlim=None, ylim=None, legend=True, grid=False,
              panel_label=None, output_path=None, **kwargs):
    """Publication-quality line plot."""
    fig, ax = create_figure(journal=journal, double=double, aspect=aspect)
    colors = colors or OKABE_ITO
    linestyles = linestyles or ["-"] * len(y_list)
    markers = markers or ["o", "s", "^", "D", "v", "<", ">", "p"][:len(y_list)]
    labels = labels or [f"Series {i+1}" for i in range(len(y_list))]

    for i, (y, label) in enumerate(zip(y_list, labels)):
        yerr = yerr_list[i] if yerr_list else None
        if yerr is not None:
            ax.errorbar(x, y, yerr=yerr, label=label, color=colors[i % len(colors)],
                       linestyle=linestyles[i], marker=markers[i], capsize=2,
                       elinewidth=0.8, markeredgewidth=0.5, **kwargs)
        else:
            ax.plot(x, y, label=label, color=colors[i % len(colors)],
                   linestyle=linestyles[i], marker=markers[i],
                   markeredgewidth=0.5, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if log_x:
        ax.set_xscale("log")
    if log_y:
        ax.set_yscale("log")
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if legend:
        ax.legend(frameon=False)
    if grid:
        ax.grid(True, alpha=0.3, linewidth=0.5)
    if panel_label:
        add_panel_label(ax, panel_label)
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def plot_bar(categories, values_list, labels=None, xlabel="", ylabel="", title="",
             journal="nature", double=False, aspect=0.7,
             colors=None, yerr_list=None, width=0.7,
             log_y=False, ylim=None, legend=True, grid=False,
             horizontal=False, panel_label=None, output_path=None, **kwargs):
    """Bar plot with optional error bars and grouping."""
    fig, ax = create_figure(journal=journal, double=double, aspect=aspect)
    colors = colors or OKABE_ITO
    labels = labels or [f"Group {i+1}" for i in range(len(values_list))]
    n_groups = len(categories)
    n_series = len(values_list)
    bar_width = width / n_series if n_series > 1 else width
    x = np.arange(n_groups)

    for i, (values, label) in enumerate(zip(values_list, labels)):
        offset = (i - (n_series - 1) / 2) * bar_width if n_series > 1 else 0
        yerr = yerr_list[i] if yerr_list else None
        if horizontal:
            ax.barh(x + offset, values, height=bar_width, label=label,
                   color=colors[i % len(colors)], xerr=yerr, capsize=2, **kwargs)
        else:
            ax.bar(x + offset, values, width=bar_width, label=label,
                  color=colors[i % len(colors)], yerr=yerr, capsize=2, **kwargs)

    if horizontal:
        ax.set_yticks(x)
        ax.set_yticklabels(categories)
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if log_y and not horizontal:
        ax.set_yscale("log")
    if ylim:
        ax.set_ylim(ylim)
    if legend and n_series > 1:
        ax.legend(frameon=False)
    if grid:
        ax.grid(True, alpha=0.3, linewidth=0.5, axis="y")
    if panel_label:
        add_panel_label(ax, panel_label)
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def plot_scatter(x, y, c=None, s=None, xlabel="", ylabel="", title="",
                 journal="nature", double=False, aspect=1.0,
                 cmap="viridis", alpha=0.8, edgecolors="none",
                 xlim=None, ylim=None, colorbar=False, cbar_label="",
                 panel_label=None, output_path=None, **kwargs):
    """Scatter plot with optional color/size mapping."""
    fig, ax = create_figure(journal=journal, double=double, aspect=aspect)
    sc = ax.scatter(x, y, c=c, s=s, cmap=cmap, alpha=alpha,
                    edgecolors=edgecolors, linewidths=0.3, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if colorbar and c is not None:
        cbar = fig.colorbar(sc, ax=ax, pad=0.02)
        cbar.set_label(cbar_label)
    if panel_label:
        add_panel_label(ax, panel_label)
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def plot_heatmap(data, row_labels=None, col_labels=None, xlabel="", ylabel="", title="",
                 journal="nature", double=False, aspect=1.0,
                 cmap="viridis", vmin=None, vmax=None, annot=False, fmt=".2f",
                 cbar_label="", panel_label=None, output_path=None, **kwargs):
    """Heatmap with optional annotations."""
    fig, ax = create_figure(journal=journal, double=double, aspect=aspect)
    im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto", **kwargs)
    if row_labels is not None:
        ax.set_yticks(range(len(row_labels)))
        ax.set_yticklabels(row_labels)
    if col_labels is not None:
        ax.set_xticks(range(len(col_labels)))
        ax.set_xticklabels(col_labels, rotation=45, ha="right")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if annot:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                val = data[i, j]
                color = "white" if (vmax or data.max()) - val > (vmax or data.max()) / 2 else "black"
                ax.text(j, i, format(val, fmt), ha="center", va="center",
                       color=color, fontsize=plt.rcParams["xtick.labelsize"])
    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label(cbar_label)
    if panel_label:
        add_panel_label(ax, panel_label)
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def plot_boxplot(data_list, labels=None, xlabel="", ylabel="", title="",
                 journal="nature", double=False, aspect=0.7,
                 colors=None, showfliers=True, notch=False,
                 ylim=None, panel_label=None, output_path=None, **kwargs):
    """Box plot with colored boxes."""
    fig, ax = create_figure(journal=journal, double=double, aspect=aspect)
    colors = colors or OKABE_ITO
    bp = ax.boxplot(data_list, labels=labels, patch_artist=True,
                    showfliers=showfliers, notch=notch,
                    medianprops={"color": "black", "linewidth": 1},
                    whiskerprops={"linewidth": 0.8},
                    capprops={"linewidth": 0.8},
                    flierprops={"marker": "o", "markersize": 3, "alpha": 0.5}, **kwargs)
    for patch, color in zip(bp["boxes"], colors * len(data_list)):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        patch.set_edgecolor("black")
        patch.set_linewidth(0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if ylim:
        ax.set_ylim(ylim)
    if labels:
        ax.set_xticklabels(labels, rotation=45, ha="right")
    if panel_label:
        add_panel_label(ax, panel_label)
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def plot_violin(data_list, labels=None, xlabel="", ylabel="", title="",
                journal="nature", double=False, aspect=0.7,
                colors=None, showmedians=True, showextrema=True,
                ylim=None, panel_label=None, output_path=None, **kwargs):
    """Violin plot."""
    fig, ax = create_figure(journal=journal, double=double, aspect=aspect)
    colors = colors or OKABE_ITO
    vp = ax.violinplot(data_list, showmedians=showmedians, showextrema=showextrema, **kwargs)
    for i, pc in enumerate(vp["bodies"]):
        pc.set_facecolor(colors[i % len(colors)])
        pc.set_alpha(0.7)
        pc.set_edgecolor("black")
        pc.set_linewidth(0.8)
    if "cmedians" in vp:
        vp["cmedians"].set_color("black")
        vp["cmedians"].set_linewidth(1.2)
    ax.set_xticks(range(1, len(data_list) + 1))
    if labels:
        ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if ylim:
        ax.set_ylim(ylim)
    if panel_label:
        add_panel_label(ax, panel_label)
    if output_path:
        save_figure(fig, output_path)
    return fig, ax


def plot_histogram(data_list, labels=None, xlabel="", ylabel="Frequency", title="",
                   journal="nature", double=False, aspect=0.7,
                   colors=None, bins=30, alpha=0.6, density=False,
                   log_y=False, xlim=None, ylim=None, legend=True,
                   panel_label=None, output_path=None, **kwargs):
    """Histogram with multiple datasets."""
    fig, ax = create_figure(journal=journal, double=double, aspect=aspect)
    colors = colors or OKABE_ITO
    labels = labels or [f"Dataset {i+1}" for i in range(len(data_list))]
    for i, (data, label) in enumerate(zip(data_list, labels)):
        ax.hist(data, bins=bins, label=label, color=colors[i % len(colors)],
               alpha=alpha, density=density, edgecolor="white", linewidth=0.3, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if log_y:
        ax.set_yscale("log")
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if legend:
        ax.legend(frameon=False)
    if panel_label:
        add_panel_label(ax, panel_label)
    if output_path:
        save_figure(fig, output_path)
    return fig, ax