"""
Scientific Figure Generator - Publication-quality figure generation for research papers.

Integrates best practices from:
- K-Dense-AI/scientific-agent-skills (matplotlib, infographics, visualization)
- Imbad0202/academic-research-skills (academic-paper visualization, quality gates)
- Haojae/scipilot-figure-skill (visualization advisor, data profiling, chart selection,
  active interception, visual QA loop, CJK font support)
- molecular-visualization skill (molecule structures, orbitals, electron clouds)
- coolors.co trending palettes (13 curated publication-quality color schemes)

Supports: Nature/Science/Cell/ACS/RSC/Elsevier journal styles,
colorblind-safe palettes, Coolors trending palettes, vector output, multi-panel figures,
quality checking, molecule structure panels, mechanism diagrams,
data profiling EDA, chart advisory, visual self-check loop, CJK fonts.
"""

__version__ = "2.2.0"
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
from .coolors_palettes import (
    get_palette, get_colormap, get_palette_info, list_palettes,
    recommend_palette, preview_palette, preview_all_palettes,
    DISCRETE_PALETTES, SEQUENTIAL_PALETTES, DIVERGING_PALETTES, ALL_PALETTES,
)
from .molecular import (
    # utils - single source of truth
    CPK_COLORS, ATOMIC_PROPERTIES, BOND_SINGLE, BOND_DOUBLE, BOND_TRIPLE,
    HYBRIDIZATION_ANGLES, CHROMOPHORES,
    get_cpk_color, get_atomic_radius, get_element_name, get_bond_length,
    get_hybridization_angle, classify_chromophore,
    # molvis - 2D ball-and-stick + orbitals + electron clouds
    load_mol, draw_atom, draw_bond, draw_ball_stick,
    draw_sp_orbital, draw_sp2_orbital, draw_sp3_orbital,
    draw_electron_cloud, draw_pi_orbital, draw_fret_pair,
    draw_molecule_with_orbitals,
    # crystal - lattice structures + physics
    CRYSTAL_DATABASE, generate_lattice, generate_from_database,
    calc_unit_cell_volume, calc_theoretical_density, calc_packing_efficiency,
    draw_crystal_2d, draw_coordination_polyhedron, plot_crystal,
    # render_3d - py3Dmol interactive 3D
    render_3d_html, smiles_to_molblock, mol_to_3d_html,
)

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
    # coolors_palettes (coolors.co trending)
    "get_palette", "get_colormap", "get_palette_info", "list_palettes",
    "recommend_palette", "preview_palette", "preview_all_palettes",
    "DISCRETE_PALETTES", "SEQUENTIAL_PALETTES", "DIVERGING_PALETTES", "ALL_PALETTES",
    # molecular subpackage (molecular-visualization integration)
    "CPK_COLORS", "ATOMIC_PROPERTIES", "BOND_SINGLE", "BOND_DOUBLE", "BOND_TRIPLE",
    "HYBRIDIZATION_ANGLES", "CHROMOPHORES",
    "get_cpk_color", "get_atomic_radius", "get_element_name", "get_bond_length",
    "get_hybridization_angle", "classify_chromophore",
    "load_mol", "draw_atom", "draw_bond", "draw_ball_stick",
    "draw_sp_orbital", "draw_sp2_orbital", "draw_sp3_orbital",
    "draw_electron_cloud", "draw_pi_orbital", "draw_fret_pair",
    "draw_molecule_with_orbitals",
    "CRYSTAL_DATABASE", "generate_lattice", "generate_from_database",
    "calc_unit_cell_volume", "calc_theoretical_density", "calc_packing_efficiency",
    "draw_crystal_2d", "draw_coordination_polyhedron", "plot_crystal",
    "render_3d_html", "smiles_to_molblock", "mol_to_3d_html",
]