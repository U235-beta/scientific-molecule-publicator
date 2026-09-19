"""
Basic unit tests for scientific-figure-generator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pytest
from scientific_figure_generator import (
    FigureGenerator,
    FigureQualityChecker,
    apply_journal_style,
    get_figure_size,
    OKABE_ITO,
    JOURNAL_STYLES,
)


class TestStyleConfig:
    def test_journal_styles_exist(self):
        assert "nature" in JOURNAL_STYLES
        assert "science" in JOURNAL_STYLES
        assert "cell" in JOURNAL_STYLES
        assert "acs" in JOURNAL_STYLES
        assert "rsc" in JOURNAL_STYLES
        assert "elsevier" in JOURNAL_STYLES

    def test_okabe_ito_palette(self):
        assert len(OKABE_ITO) == 8
        assert all(c.startswith("#") for c in OKABE_ITO)

    def test_apply_journal_style(self):
        style = apply_journal_style("nature")
        assert style["font_size"] == 7
        assert style["dpi"] == 600

    def test_get_figure_size(self):
        w, h = get_figure_size(journal="nature", double=False)
        assert w > 0 and h > 0
        w2, h2 = get_figure_size(journal="nature", double=True)
        assert w2 > w


class TestFigureGenerator:
    def test_create_figure_1x1(self):
        gen = FigureGenerator(journal="nature")
        fig, axes = gen.create_figure(layout="1x1")
        assert len(axes) == 1
        assert fig is not None

    def test_create_figure_2x2(self):
        gen = FigureGenerator(journal="nature")
        fig, axes = gen.create_figure(layout="2x2")
        assert len(axes) == 4

    def test_add_line_plot(self):
        gen = FigureGenerator(journal="nature")
        fig, axes = gen.create_figure(layout="1x1")
        x = np.linspace(0, 10, 20)
        y = np.sin(x)
        gen.add_line_plot(axes[0], x, [y])
        assert len(axes[0].lines) == 1

    def test_add_bar_plot(self):
        gen = FigureGenerator(journal="nature")
        fig, axes = gen.create_figure(layout="1x1")
        gen.add_bar_plot(axes[0], ["A", "B", "C"], [[1, 2, 3]])
        assert len(axes[0].patches) > 0

    def test_add_text_panel(self):
        gen = FigureGenerator(journal="nature")
        fig, axes = gen.create_figure(layout="1x1")
        gen.add_text_panel(axes[0], "Test text", title="Test")
        assert axes[0].axis_on is False

    def test_set_axis_labels(self):
        gen = FigureGenerator(journal="nature")
        fig, axes = gen.create_figure(layout="1x1")
        gen.set_axis_labels(axes[0], xlabel="X", ylabel="Y", title="Test")
        assert axes[0].get_xlabel() == "X"
        assert axes[0].get_ylabel() == "Y"


class TestQualityChecker:
    def test_check_empty_figure(self):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        checker = FigureQualityChecker()
        issues = checker.check(fig)
        assert any(i.level == "error" for i in issues)

    def test_check_resolution(self):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(dpi=72)
        ax.plot([1, 2, 3], [1, 2, 3])
        checker = FigureQualityChecker(min_dpi=300)
        issues = checker.check(fig)
        assert any("DPI" in i.message for i in issues)

    def test_has_critical_issues(self):
        issues = [
            type("Issue", (), {"level": "error"})(),
            type("Issue", (), {"level": "warning"})(),
        ]
        assert FigureQualityChecker.has_critical_issues(issues)

    def test_get_issue_count(self):
        issues = [
            type("Issue", (), {"level": "error"})(),
            type("Issue", (), {"level": "error"})(),
            type("Issue", (), {"level": "warning"})(),
            type("Issue", (), {"level": "info"})(),
        ]
        counts = FigureQualityChecker.get_issue_count(issues)
        assert counts["error"] == 2
        assert counts["warning"] == 1
        assert counts["info"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])