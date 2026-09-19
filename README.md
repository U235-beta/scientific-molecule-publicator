# Scientific Molecule Publicator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)]()

> Publication-quality scientific figure generation with a **visualization advisor workflow** — think first, plot second. Fuses K-Dense-AI/scientific-agent-skills, Imbad0202/academic-research-skills, and Haojae/scipilot-figure-skill.

## Why This Isnt Just a Plotting Tool

```
Generic plotter             Scientific Molecule Publicator
──────────────              ─────────────────────────────
"plot a bar chart"   →     Profiles data first: types, n, distribution, outliers
plt.bar()                     Asks: "What argument do you want this figure to make?"
                              Decides chart type from data shape + intent
                              Refuses bad choices (n=5 mean bar → stripplot)
                              Only then renders → spec → visual QA → export
```

## Features

- **Visualization Advisor** — 8-step workflow: understand → profile → select → spec → style → plot → QA → export
- **Data Profiling EDA** — column types, sample sizes, distributions, outliers, correlations
- **Chart Selection** — decision framework by data shape + argument intent, with 18 active interceptions
- **Visual QA Loop** — post-render program audit (missing glyphs, text clipping, label overlap) + grayscale check
- **CJK Font Support** — auto-configures Chinese fonts, fixes minus-sign tofu boxes
- **7+ Data Plot Types** — line, bar, scatter, heatmap, boxplot, violin, histogram
- **6 Journal Styles** — Nature, Science, Cell, ACS, RSC, Elsevier
- **Colorblind-Safe** — Okabe-Ito, viridis family, ColorBrewer palettes
- **Multi-Panel Figures** — Figure 1-5 style composite layouts with aligned panel labels
- **Molecule Panels** — integrates with molecular-visualization skill (ball-and-stick, orbitals, electron clouds)
- **Mechanism Diagrams** — causal chains, process flows, layered frameworks, uncertainty propagation
- **Quality Checking** — 7-category automated pre-submission quality gates
- **Vector Output** — PDF/SVG with editable text (TrueType fonts, pdf.fonttype=42)

## Installation

```bash
git clone https://github.com/U235-beta/scientific-molecule-publicator.git
cd scientific-molecule-publicator
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
import pandas as pd
from scientific_figure_generator import (
    profile_data, ChartAdvisor, setup_style,
    FigureGenerator, VisualQA, add_panel_labels, save_figure
)

# 1. Profile data
df = pd.read_csv("results.csv")
profile = profile_data(df, group_cols=["condition"])

# 2. Get chart recommendations (with active interception)
advisor = ChartAdvisor()
recs = advisor.recommend(profile, argument="group_difference")
for r in recs:
    print(f"{'!' if r.is_warning else '>'} {r.chart_type}: {r.reason}")

# 3. Setup + plot
setup_style(journal="nature", lang="en")
gen = FigureGenerator(journal="nature", double=True, aspect=0.8)
fig, axes = gen.create_figure(layout="2x2")
gen.add_boxplot(axes[0], df, x="condition", y="value")
gen.add_scatter_plot(axes[1], df["x"], df["y"])

# 4. Visual QA
qa = VisualQA()
issues = qa.audit_layout(fig)
print(VisualQA.report(issues))

# 5. Export
add_panel_labels(fig, style="nature")
save_figure(fig, "Figure1", formats=("pdf", "png"), dpi=600)
```

## 18 Active Interceptions

| ID | Pitfall | Alternative |
|----|---------|-------------|
| P1 | Mean bar with n<10 | Box + stripplot |
| P2 | Dual Y-axis | Split subplots |
| P3 | Pie chart | Horizontal bar |
| P4 | 3D bar/pie | 2D bar/heatmap |
| P5 | Y-axis truncation | Start from 0 / log |
| P9 | Rainbow/jet colormap | viridis/cividis |
| P11 | Error bars no caption | SD/SEM/CI + n + test |
| P14 | JPEG data figures | PDF/SVG vector |
| P16 | CJK tofu boxes | setup_style(lang="zh") |
| P18 | Manual panel labels | add_panel_labels() |

## Project Structure

```
scientific-molecule-publicator/
├── SKILL.md
├── README.md
├── plugin.json
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── LICENSE
├── src/scientific_figure_generator/
│   ├── __init__.py
│   ├── style_config.py        # Journal styles + CJK fonts + setup_style()
│   ├── data_profiler.py       # EDA data profiling
│   ├── chart_advisor.py       # Chart selection + 18 active interceptions
│   ├── data_plots.py          # 7+ data plot types
│   ├── mechanism_diagrams.py  # Causal chains, process flows
│   ├── figure_generator.py    # Multi-panel figure generator
│   ├── quality_checker.py     # 7-category quality gates
│   ├── visual_qa.py           # Post-render visual self-check
│   └── layout_tools.py        # Panel label alignment, layout
├── examples/
│   └── example_figure.py
├── tests/
│   └── test_basic.py
└── templates/
    └── figure_spec.json
```

## Five Hard Rules

1. **Render at final size, never rescale**
2. **Vector first** — PDF/SVG/EPS for data, never JPEG
3. **Colorblind-safe** — Okabe-Ito + redundant encoding + grayscale check
4. **Readable type at final size** — 7-9pt body, minimum 6pt
5. **Errors must be explained** — caption states SD/SEM/CI + n + test

## Acknowledgments

This project fuses best practices from:
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) — matplotlib and visualization best practices
- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) — academic paper quality gates
- [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill) — visualization advisor workflow, EDA, chart selection, visual QA

## License

MIT License