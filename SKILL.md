---
name: scientific-molecule-publicator
version: 2.0.0
description: "Publication-quality scientific figure generator with visualization advisor workflow. Integrates EDA data profiling, chart selection with active interception, visual QA self-check loop, CJK font support, molecule structure panels, mechanism diagrams, and 6 journal styles. Fuses K-Dense-AI/scientific-agent-skills, Imbad0202/academic-research-skills, and Haojae/scipilot-figure-skill."
keywords: [scientific figures, publication quality, matplotlib, visualization advisor, data profiling, chart selection, visual QA, CJK fonts, journal style, multi-panel, molecule visualization, mechanism diagram, quality control, colorblind-safe]
license: MIT
author: U235-beta
---

# Scientific Molecule Publicator

Publication-quality figure generation for scientific research papers with a **visualization advisor workflow** — think first, plot second.

## Core Philosophy: Think First, Plot Second

This is not just a plotting tool. It follows an **8-step advisor workflow**:

```
0. Understand task  — What argument should this figure make?
   ↓
1. Profile data     — EDA: column types, n, distribution, outliers, correlations
   ↓
2. Select chart     — Decision framework: data shape + argument intent
   ↓ (active interception of 18 common pitfalls)
3. Check specs      — Journal column width, font size, DPI
   ↓
4. Setup style      — Journal preset + CJK font + SciencePlots
   ↓
5. Plot             — 9+ chart types with publication recipes
   ↓
6. Self-check loop  — Program audit (glyphs/clipping/overlap) + grayscale check
   ↓
7. Export           — PDF/SVG/PNG at final size, never rescale
```

## When to Use

- Generating Figure 1-5 for a research paper, review, or thesis
- You have data but don't know which chart type best conveys your conclusion
- Creating multi-panel composite figures with consistent layout
- Producing data plots (line, bar, scatter, heatmap, boxplot, violin, histogram)
- Drawing mechanism diagrams, causal chains, process flows, comparison diagrams
- Adding molecule structure panels (integrates with molecular-visualization skill)
- Quality-checking figures before submission with visual QA loop
- Chinese paper figures (auto CJK font configuration, no tofu boxes)

## Prerequisites

- Python 3.9+
- matplotlib >= 3.7, numpy >= 1.24
- seaborn >= 0.13, pandas >= 2.0, scipy >= 1.10, Pillow >= 10.0
- Optional: SciencePlots, molecular-visualization skill

## Quick Start

### Advisor Workflow Example

```python
import pandas as pd
from scientific_figure_generator import (
    profile_data, print_profile_report, ChartAdvisor,
    setup_style, FigureGenerator, VisualQA, add_panel_labels, save_figure
)

# Step 0-1: Understand + Profile data
df = pd.read_csv("results.csv")
profile = profile_data(df, group_cols=["condition"])
print(print_profile_report(profile))

# Step 2: Get chart recommendations with active interception
advisor = ChartAdvisor()
recs = advisor.recommend(profile, argument="group_difference", group_cols=["condition"])
for r in recs:
    print(f"{'!' if r.is_warning else '>'} {r.chart_type}: {r.reason}")

# Step 3-5: Setup style + plot
setup_style(journal="nature", lang="en")
gen = FigureGenerator(journal="nature", double=True, aspect=0.8)
fig, axes = gen.create_figure(layout="2x2")
gen.add_boxplot(axes[0], df, x="condition", y="fluorescence")
gen.add_scatter_plot(axes[1], df["time"], df["intensity"])
gen.add_mechanism_chain(axes[2], ["Pure polymer", "+ Additives", "+ Aging"])
gen.add_text_panel(axes[3], "Key finding", title="Summary")

# Step 6: Visual QA self-check
qa = VisualQA()
qa.render_preview(fig, "preview.png")
issues = qa.audit_layout(fig)
print(VisualQA.report(issues))

# Step 7: Export
add_panel_labels(fig, style="nature")
save_figure(fig, "Figure1", formats=("pdf", "png"), dpi=600)
```

### Chinese Figure Example

```python
from scientific_figure_generator import setup_style, create_figure, save_figure

# Auto-configures CJK fonts + fixes minus-sign boxes
setup_style(journal="general", lang="zh", serif_for_zh=True)
fig, ax = create_figure(journal="general", double=False, aspect=0.7)
ax.plot([1,2,3], [1,4,9], label="实验组")
ax.set_xlabel("时间 (小时)")
ax.set_ylabel("荧光强度 (a.u.)")
ax.legend()
save_figure(fig, "图1_中文示例", formats=("pdf", "png"))
```

## 18 Active Interceptions (Pitfalls)

The advisor actively intercepts common scientific plotting mistakes:

| ID | Pitfall | Alternative |
|----|---------|-------------|
| P1 | Mean bar with n<10/group | Box + stripplot overlay |
| P2 | Dual Y-axis for unrelated vars | Split subplots or standardize |
| P3 | Pie chart for proportions | Horizontal bar (sorted) |
| P4 | 3D bar/pie | 2D bar, heatmap |
| P5 | Y-axis truncation without indication | Start from 0 or log scale |
| P6 | Line connecting categorical x | Scatter / dot plot / bar |
| P9 | Rainbow/jet colormap | viridis/magma/cividis/RdBu_r |
| P11 | Error bars without caption | Caption: SD/SEM/CI + n + test |
| P14 | JPEG for data figures | PDF/SVG/EPS (vector) |
| P16 | CJK/minus-sign tofu boxes | setup_style(lang="zh") |
| P18 | Panel labels manually positioned | add_panel_labels() |

## Journal Styles

| Journal | Single Col (mm) | Double Col (mm) | Font | DPI |
|---------|----------------|----------------|------|-----|
| Nature | 89 | 183 | 7pt | 600 |
| Science | 58 | 120 | 6pt | 600 |
| Cell | 85 | 174 | 8pt | 600 |
| ACS | 82 | 172 | 8pt | 300 |
| RSC | 82 | 170 | 7pt | 600 |
| Elsevier | 90 | 190 | 8pt | 300 |

## Module Reference

| Module | Purpose |
|--------|---------|
| `style_config.py` | Journal styles, color palettes, CJK fonts, setup_style() |
| `data_profiler.py` | EDA: column types, n, distribution, outliers, correlations |
| `chart_advisor.py` | Chart selection decision framework + 18 active interceptions |
| `data_plots.py` | 7+ data plot types |
| `mechanism_diagrams.py` | Causal chains, process flows, layered frameworks |
| `figure_generator.py` | Multi-panel figure generator + spec-based generation |
| `quality_checker.py` | 7-category quality gates |
| `visual_qa.py` | Post-render visual self-check: glyphs, clipping, overlap, grayscale |
| `layout_tools.py` | Panel label alignment, layout finalization, axes alignment |

## Five Hard Rules

1. **Render at final size, never rescale** — figsize directly sets paper dimensions
2. **Vector first** — PDF/SVG/EPS for data; never JPEG
3. **Colorblind-safe** — Okabe-Ito default + redundant encoding + grayscale check
4. **Readable type at final size** — 7-9pt body, minimum 6pt
5. **Errors must be explained** — caption states SD/SEM/CI + n + test method

## Integration

- **molecular-visualization** — ball-and-stick models, sp²/sp³ orbitals, electron clouds, FRET
- **K-Dense-AI/scientific-agent-skills** — matplotlib and visualization best practices
- **Imbad0202/academic-research-skills** — academic paper quality gates
- **Haojae/scipilot-figure-skill** — visualization advisor workflow, EDA, chart selection, visual QA

## License

MIT License