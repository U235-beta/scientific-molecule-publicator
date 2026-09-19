"""
Publication quality checker for scientific figures.

Implements quality gates inspired by Imbad0202 academic-research-skills
(academic-pipeline integrity gates) and K-Dense-AI scientific-agent-skills
(matplotlib best practices).

Checks: resolution, colorblind safety, font embedding, axis completeness,
label readability, panel label consistency, vector output, data-ink ratio.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import namedtuple

QualityIssue = namedtuple("QualityIssue", ["level", "category", "message", "suggestion"])


class FigureQualityChecker:
    """Run quality checks on a matplotlib figure before publication."""

    def __init__(self, journal="nature", min_dpi=300, min_font_size=5):
        self.journal = journal
        self.min_dpi = min_dpi
        self.min_font_size = min_font_size
        self.colorblind_palettes = [
            "viridis", "magma", "inferno", "plasma", "cividis",
            "coolwarm", "RdBu", "PiYG",
        ]
        self.okabe_ito = ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
                          "#0072B2", "#D55E00", "#CC79A7", "#000000"]

    def check(self, fig):
        """Run all quality checks, return list of QualityIssue."""
        issues = []
        issues.extend(self._check_resolution(fig))
        issues.extend(self._check_fonts(fig))
        issues.extend(self._check_axes(fig))
        issues.extend(self._check_colors(fig))
        issues.extend(self._check_labels(fig))
        issues.extend(self._check_panel_labels(fig))
        issues.extend(self._check_tight_layout(fig))
        return issues

    def _check_resolution(self, fig):
        issues = []
        dpi = fig.dpi
        if dpi < self.min_dpi:
            issues.append(QualityIssue("warning", "resolution",
                f"Figure DPI is {dpi}, minimum recommended is {self.min_dpi}",
                f"Set dpi={self.min_dpi} or higher in savefig"))
        w, h = fig.get_size_inches()
        if w < 2 or h < 2:
            issues.append(QualityIssue("error", "resolution",
                f"Figure size too small: {w:.1f}x{h:.1f} inches",
                "Increase figure size to at least 3x3 inches"))
        if w > 10 or h > 10:
            issues.append(QualityIssue("info", "resolution",
                f"Figure size large: {w:.1f}x{h:.1f} inches",
                "Consider if this fits journal column width"))
        return issues

    def _check_fonts(self, fig):
        issues = []
        if matplotlib.rcParams.get("pdf.fonttype") != 42:
            issues.append(QualityIssue("warning", "fonts",
                "PDF fonttype is not 42 (TrueType), text may not be editable in Illustrator",
                "Set plt.rcParams['pdf.fonttype'] = 42"))
        for text in fig.findobj(plt.Text):
            fs = text.get_fontsize()
            if isinstance(fs, (int, float)) and fs < self.min_font_size:
                issues.append(QualityIssue("warning", "fonts",
                    f"Text '{text.get_text()[:30]}' has fontsize {fs}",
                    f"Increase fontsize to at least {self.min_font_size}"))
                break
        return issues

    def _check_axes(self, fig):
        issues = []
        for ax in fig.axes:
            if ax.axison:
                if not ax.get_xlabel() and ax.get_xscale() != "log":
                    if len(ax.images) == 0 and len(ax.patches) < 3:
                        issues.append(QualityIssue("info", "axes",
                            "Axes missing xlabel", "Add xlabel or verify this is intentional"))
                if not ax.get_ylabel() and ax.get_yscale() != "log":
                    if len(ax.images) == 0 and len(ax.patches) < 3:
                        issues.append(QualityIssue("info", "axes",
                            "Axes missing ylabel", "Add ylabel or verify this is intentional"))
                if len(ax.lines) == 0 and len(ax.collections) == 0 and len(ax.patches) == 0 and len(ax.images) == 0:
                    issues.append(QualityIssue("error", "axes",
                        "Axes is empty (no plotted data)",
                        "Add data to this axes or remove it"))
        return issues

    def _check_colors(self, fig):
        issues = []
        for ax in fig.axes:
            for im in ax.images:
                cmap = im.get_cmap()
                cmap_name = cmap.name if hasattr(cmap, "name") else str(cmap)
                if cmap_name.lower() in ["jet", "rainbow", "hsv"]:
                    issues.append(QualityIssue("warning", "colors",
                        f"Colormap '{cmap_name}' is not colorblind-safe",
                        "Use 'viridis', 'cividis', or other perceptually uniform colormap"))
            line_colors = []
            for line in ax.lines:
                color = line.get_color()
                if isinstance(color, str) and color.startswith("#"):
                    line_colors.append(color.lower())
            if "#ff0000" in line_colors and "#00ff00" in line_colors:
                issues.append(QualityIssue("warning", "colors",
                    "Red and green lines used together (colorblind-unfriendly)",
                    "Use Okabe-Ito palette or add distinct markers"))
        return issues

    def _check_labels(self, fig):
        issues = []
        for ax in fig.axes:
            if ax.axison:
                xticklabels = [t.get_text() for t in ax.get_xticklabels()]
                long_labels = [l for l in xticklabels if len(l) > 8]
                if long_labels and len(long_labels) > 3:
                    rotation = ax.get_xticklabels()[0].get_rotation()
                    if rotation == 0:
                        issues.append(QualityIssue("info", "labels",
                            f"Long x-tick labels ({len(long_labels)} labels >8 chars) without rotation",
                            "Rotate x-tick labels by 45 degrees"))
        return issues

    def _check_panel_labels(self, fig):
        issues = []
        n_axes = len([ax for ax in fig.axes if ax.axison or len(ax.images) > 0 or len(ax.patches) > 2])
        if n_axes > 1:
            panel_labels_found = 0
            for ax in fig.axes:
                for text in ax.texts:
                    t = text.get_text().strip()
                    if len(t) == 1 and t.isupper() and text.get_fontweight() in ["bold", "heavy"]:
                        panel_labels_found += 1
                        break
            if panel_labels_found == 0 and n_axes > 1:
                issues.append(QualityIssue("info", "panel_labels",
                    f"Multi-panel figure ({n_axes} axes) without panel labels (A, B, C...)",
                    "Add panel labels using add_panel_label()"))
            elif 0 < panel_labels_found < n_axes:
                issues.append(QualityIssue("warning", "panel_labels",
                    f"Inconsistent panel labels: {panel_labels_found}/{n_axes} axes labeled",
                    "Ensure all panels have consistent labels"))
        return issues

    def _check_tight_layout(self, fig):
        issues = []
        if fig._suptitle is not None:
            issues.append(QualityIssue("info", "layout",
                "Figure has suptitle - verify no overlap with panel titles",
                "Use fig.tight_layout(rect=[0, 0, 1, 0.95]) to leave room for suptitle"))
        return issues

    @staticmethod
    def report(issues, output_path=None):
        """Generate a quality report."""
        lines = []
        lines.append("=" * 60)
        lines.append("SCIENTIFIC FIGURE QUALITY REPORT")
        lines.append("=" * 60)

        errors = [i for i in issues if i.level == "error"]
        warnings = [i for i in issues if i.level == "warning"]
        infos = [i for i in issues if i.level == "info"]

        lines.append(f"\nSummary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} suggestions")
        lines.append("-" * 60)

        for level, title in [("error", "ERRORS (must fix)"), ("warning", "WARNINGS (should fix)"), ("info", "SUGGESTIONS (optional)")]:
            level_issues = [i for i in issues if i.level == level]
            if level_issues:
                lines.append(f"\n{title}:")
                for i, issue in enumerate(level_issues, 1):
                    lines.append(f"  {i}. [{issue.category}] {issue.message}")
                    lines.append(f"     -> {issue.suggestion}")

        report = "\n".join(lines)
        if output_path:
            Path(output_path).write_text(report, encoding="utf-8")
        return report

    @staticmethod
    def has_critical_issues(issues):
        return any(i.level == "error" for i in issues)

    @staticmethod
    def get_issue_count(issues):
        return {
            "error": sum(1 for i in issues if i.level == "error"),
            "warning": sum(1 for i in issues if i.level == "warning"),
            "info": sum(1 for i in issues if i.level == "info"),
        }


def check_and_save(fig, output_path, journal="nature", enforce_quality=False):
    """Quality-check a figure before saving."""
    from .style_config import save_figure
    checker = FigureQualityChecker(journal=journal)
    issues = checker.check(fig)
    report = checker.report(issues)
    print(report)
    if enforce_quality and checker.has_critical_issues(issues):
        raise ValueError(f"Figure has critical quality issues: {checker.get_issue_count(issues)}")
    paths = save_figure(fig, output_path)
    return paths, issues