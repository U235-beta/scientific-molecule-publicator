"""
Visual quality assurance for scientific figures.

Provides post-render visual self-check loop:
1. render_preview() - Render figure to PNG for inspection
2. audit_layout() - Programmatic checks: missing glyphs, text clipping, overlapping labels
3. Grayscale conversion for colorblind safety check

Inspired by scipilot-figure-skill visual_qa.py.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import namedtuple
import warnings
import logging

VisualIssue = namedtuple("VisualIssue", ["level", "category", "message", "suggestion"])


class VisualQA:
    """
    Post-render visual quality checker.

    Usage:
        qa = VisualQA()
        qa.render_preview(fig, "preview.png")
        issues = qa.audit_layout(fig)
        qa.report(issues)
    """

    def __init__(self, min_font_size=6, dpi=150):
        self.min_font_size = min_font_size
        self.dpi = dpi
        self._glyph_warnings = []
        self._setup_glyph_capture()

    def _setup_glyph_capture(self):
        """Capture matplotlib missing-glyph warnings."""
        self._glyph_warnings = []

        def warning_handler(message, category, filename, lineno, file=None, line=None):
            msg = str(message)
            if "Glyph" in msg and "missing from" in msg:
                self._glyph_warnings.append(msg)
            elif "missing from current font" in msg:
                self._glyph_warnings.append(msg)

        warnings.showwarning = warning_handler

        class GlyphLogHandler(logging.Handler):
            def emit(self2, record):
                msg = self2.format(record)
                if "Glyph" in msg or "missing" in msg:
                    self._glyph_warnings.append(msg)

        self._log_handler = GlyphLogHandler()
        logging.getLogger("matplotlib").addHandler(self._log_handler)

    def render_preview(self, fig, output_path, dpi=None):
        """Render figure to PNG preview for visual inspection."""
        self._glyph_warnings.clear()
        dpi = dpi or self.dpi
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        return str(output_path)

    def audit_layout(self, fig):
        """
        Run programmatic visual checks on a figure.

        Checks: missing glyphs, text clipping, overlapping tick labels,
                font size compliance, empty axes.
        """
        self._glyph_warnings.clear()
        issues = []

        try:
            fig.canvas.draw()
        except Exception:
            pass

        # Check 1: Missing glyphs
        if self._glyph_warnings:
            issues.append(VisualIssue("error", "glyphs",
                f"Missing glyphs detected: {len(self._glyph_warnings)} warnings (CJK tofu boxes, minus-sign squares)",
                "Configure CJK font with setup_style(lang='zh') and set axes.unicode_minus=False"))

        # Check 2: Text clipping
        issues.extend(self._check_text_clipping(fig))

        # Check 3: Overlapping tick labels
        issues.extend(self._check_tick_overlap(fig))

        # Check 4: Font sizes
        issues.extend(self._check_font_sizes(fig))

        # Check 5: Empty axes
        issues.extend(self._check_empty_axes(fig))

        return issues

    def _check_text_clipping(self, fig):
        """Check if any text element is clipped by figure bounds."""
        issues = []
        fig_width, fig_height = fig.get_size_inches()
        fig_dpi = fig.dpi

        for text in fig.findobj(plt.Text):
            if not text.get_visible():
                continue
            try:
                bbox = text.get_window_extent()
                x0 = bbox.x0 / (fig_width * fig_dpi)
                y0 = bbox.y0 / (fig_height * fig_dpi)
                x1 = bbox.x1 / (fig_width * fig_dpi)
                y1 = bbox.y1 / (fig_height * fig_dpi)

                if x0 < -0.02 or x1 > 1.02 or y0 < -0.02 or y1 > 1.02:
                    txt = text.get_text()[:30]
                    issues.append(VisualIssue("warning", "clipping",
                        f"Text '{txt}' may be clipped (bbox extends beyond figure bounds)",
                        "Adjust subplot spacing (subplots_adjust) or reduce font size"))
                    break
            except Exception:
                continue

        return issues[:3]

    def _check_tick_overlap(self, fig):
        """Check for overlapping tick labels."""
        issues = []
        for ax in fig.axes:
            if not ax.axison:
                continue
            xticklabels = [t for t in ax.get_xticklabels() if t.get_visible() and t.get_text()]
            if len(xticklabels) > 5:
                try:
                    bboxes = [t.get_window_extent() for t in xticklabels]
                    overlaps = 0
                    for i in range(len(bboxes) - 1):
                        if bboxes[i].x1 > bboxes[i+1].x0:
                            overlaps += 1
                    if overlaps > len(bboxes) * 0.3:
                        issues.append(VisualIssue("warning", "overlap",
                            f"X-axis tick labels overlap ({overlaps}/{len(bboxes)} adjacent pairs)",
                            "Rotate labels by 45 degrees, reduce font size, or reduce tick count"))
                except Exception:
                    pass
        return issues

    def _check_font_sizes(self, fig):
        """Check font size compliance."""
        issues = []
        for text in fig.findobj(plt.Text):
            fs = text.get_fontsize()
            if isinstance(fs, (int, float)) and fs < self.min_font_size:
                issues.append(VisualIssue("warning", "font_size",
                    f"Text '{text.get_text()[:20]}' has fontsize {fs}pt (minimum {self.min_font_size}pt)",
                    f"Increase fontsize to at least {self.min_font_size}pt"))
                break
        return issues

    def _check_empty_axes(self, fig):
        """Check for empty axes."""
        issues = []
        for ax in fig.axes:
            if ax.axison and len(ax.lines) == 0 and len(ax.collections) == 0 and len(ax.patches) == 0 and len(ax.images) == 0:
                issues.append(VisualIssue("error", "empty",
                    "Axes is empty (no plotted data)",
                    "Add data to this axes or remove it"))
        return issues

    def check_grayscale(self, fig, output_path=None):
        """Convert figure to grayscale for colorblind safety check."""
        if output_path is None:
            output_path = Path("_grayscale_preview.png")
        else:
            output_path = Path(output_path)

        self.render_preview(fig, output_path)
        try:
            from PIL import Image
            img = Image.open(output_path).convert("L")
            gray_path = output_path.with_stem(output_path.stem + "_grayscale")
            img.save(gray_path)
            return str(gray_path)
        except ImportError:
            return str(output_path)

    @staticmethod
    def report(issues, output_path=None):
        """Generate a visual QA report."""
        lines = ["=" * 60, "VISUAL QA REPORT", "=" * 60]
        errors = [i for i in issues if i.level == "error"]
        warnings = [i for i in issues if i.level == "warning"]
        infos = [i for i in issues if i.level == "info"]
        lines.append(f"\nSummary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
        lines.append("-" * 60)
        for level, title in [("error", "ERRORS"), ("warning", "WARNINGS"), ("info", "INFO")]:
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