"""
Scientific Figure Generator - Publication-quality figure generation for research papers.

Integrates best practices from:
- K-Dense-AI/scientific-agent-skills (matplotlib, infographics, visualization)
- Imbad0202/academic-research-skills (academic-paper visualization, quality gates)
- Haojae/scipilot-figure-skill (visualization advisor, data profiling, chart selection,
  active interception, visual QA loop, CJK font support)
- molecular-visualization skill (molecule structures, orbitals, electron clouds)

Supports: Nature/Science/Cell/ACS/RSC/Elsevier journal styles,
colorblind-safe palettes, vector output, multi-panel figures,
quality checking, molecule structure panels, mechanism diagrams,
data profiling EDA, chart advisory, visual self-check loop, CJK fonts.
"""

__version__ = "2.0.0"
__author__ = "U235-beta"
__license__ = "MIT"

from .style_config import (
    apply_journal_style, get_figure_size, create_figure, save_figure,
    add_panel_label, OKABE_ITO, JOURNAL_STYLES, mm_to_inch,
    setup_style, list_cjk_fonts, CJK_FONT_PRIORITY,
)
from .data_plots import (
    plot_line, plot_bar, plot_scatter, plot_heatmap,
    plot_boxplot, plot_violin, plot_histogram,
)
from .mechanism_diagrams import (
    causal_chain, layered_framework, process_flow,
    comparison_diagram, uncertainty_propagation_chain,
)
from .figure_generator import FigureGenerator, generate_figure_from_spec
from .quality_checker import FigureQualityChecker, check_and_save
from .data_profiler import profile_data, print_profile_report
from .chart_advisor import ChartAdvisor, ChartRecommendation, PITFALLS
from .visual_qa import VisualQA
from .layout_tools import add_panel_labels, finalize_figure, align_axes

__all__ = [
    # style_config
    "apply_journal_style", "get_figure_size", "create_figure", "save_figure",
    "add_panel_label", "OKABE_ITO", "JOURNAL_STYLES", "mm_to_inch",
    "setup_style", "list_cjk_fonts", "CJK_FONT_PRIORITY",
    # data_plots
    "plot_line", "plot_bar", "plot_scatter", "plot_heatmap",
    "plot_boxplot", "plot_violin", "plot_histogram",
    # mechanism_diagrams
    "causal_chain", "layered_framework", "process_flow",
    "comparison_diagram", "uncertainty_propagation_chain",
    # figure_generator
    "FigureGenerator", "generate_figure_from_spec",
    # quality_checker
    "FigureQualityChecker", "check_and_save",
    # data_profiler (scipilot integration)
    "profile_data", "print_profile_report",
    # chart_advisor (scipilot integration)
    "ChartAdvisor", "ChartRecommendation", "PITFALLS",
    # visual_qa (scipilot integration)
    "VisualQA",
    # layout_tools (scipilot integration)
    "add_panel_labels", "finalize_figure", "align_axes",
]