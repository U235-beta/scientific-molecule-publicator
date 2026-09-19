---
name: scientific-molecule-publicator
version: 2.2.0
description: "Publication-quality scientific figure generator with visualization advisor workflow + molecular visualization subpackage. Integrates EDA data profiling, chart selection with active interception, visual QA self-check loop, CJK font support, 2D/3D molecule structure panels (ball-and-stick, hybrid orbitals, electron clouds, crystal lattices), mechanism diagrams, 13 Coolors trending palettes, and 6 journal styles. Fuses K-Dense-AI/scientific-agent-skills, Imbad0202/academic-research-skills, Haojae/scipilot-figure-skill, and molecular-visualization."
keywords: [scientific figures, publication quality, matplotlib, visualization advisor, data profiling, chart selection, visual QA, CJK fonts, journal style, multi-panel, molecule visualization, molecular orbitals, electron cloud, crystal structure, ball-and-stick, mechanism diagram, quality control, colorblind-safe, coolors palettes, autofluorescence, microplastics]
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
- Optional: SciencePlots
- Optional (molecular coordinate generation): Node.js 16+ + RDKit.js WASM (run `tools/download_rdkit.ps1`)
- Optional (3D interactive HTML): py3Dmol (pip install py3Dmol)

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

### Molecular Visualization Example (v2.2.0+)

```python
from scientific_figure_generator import (
    setup_style, create_figure, save_figure,
    load_mol, draw_ball_stick, draw_sp2_orbital, draw_electron_cloud,
    draw_pi_orbital, CPK_COLORS, CHROMOPHORES, classify_chromophore,
    generate_lattice, draw_crystal_2d, render_3d_html,
)

# 1. Load molecule from JSON (generated by tools/generate_coords.js)
mol = load_mol("molecule_data/PET_dimer.json")

# 2. Draw ball-and-stick with sp2 orbitals and electron cloud
fig, ax = create_figure(journal="nature", double=False, aspect=1.0)
draw_ball_stick(ax, mol, scale=1.0, show_labels=True)
draw_sp2_orbital(ax, center=(1.5, 0), atom_index=4, scale=0.8)
draw_electron_cloud(ax, center=(1.5, 0), radius=1.2, alpha=0.15, color="#4A90D9")
draw_pi_orbital(ax, bond=(4, 5), scale=0.6)
ax.set_title("PET Dimer — Ball-and-Stick with sp² Orbitals and π Cloud")
save_figure(fig, "Fig2_PET_molecular", formats=("pdf", "png"), dpi=600)

# 3. Classify chromophore (for autofluorescence analysis)
chromophore = classify_chromophore(mol)
print(f"Chromophore type: {chromophore['type']}")
print(f"Excitation range: {chromophore['excitation_nm']} nm")
print(f"Emission range: {chromophore['emission_nm']} nm")

# 4. Crystal structure (e.g., FCC copper)
crystal = generate_lattice("FCC", a=3.615, element="Cu")
fig2, ax2 = create_figure(journal="nature", double=False, aspect=1.0)
draw_crystal_2d(ax2, crystal, projection="xy", show_labels=True)
save_figure(fig2, "FigS1_Cu_FCC", formats=("png",), dpi=300)

# 5. Interactive 3D HTML (py3Dmol)
html = render_3d_html(mol, style="stick", width=800, height=600)
with open("PET_3d.html", "w") as f:
    f.write(html)
```

### Coolors Trending Palettes Example (v2.1.0+)

```python
from scientific_figure_generator import (
    setup_style, create_figure, save_figure,
    get_palette, get_colormap, recommend_palette, preview_all_palettes,
)

# 1. Get a discrete palette for categorical data
colors = get_palette("soft_lavender", n_colors=4)  # molecular chemistry theme

# 2. Get a sequential colormap for heatmaps
cmap = get_colormap("fresh_greens")  # ecology/environment theme

# 3. Auto-recommend based on data type
palette_name, reason = recommend_palette(
    data_type="categorical", n_groups=5,
    colorblind_safe=True, theme="molecular"
)
print(f"Recommended: {palette_name} — {reason}")

# 4. Preview all palettes
preview_all_palettes(output_path="coolors_preview.png")

# 5. Use in a plot
setup_style(journal="nature", lang="en")
fig, ax = create_figure(journal="nature", double=True, aspect=0.6)
for i, (polymer, intensity) in enumerate([("PE", 12), ("PS", 45), ("PET", 78), ("PVC", 33)]):
    ax.bar(polymer, intensity, color=colors[i], label=polymer, edgecolor="white")
ax.set_ylabel("Autofluorescence Intensity (a.u.)")
ax.legend(title="Polymer")
save_figure(fig, "Fig3_additive_fluorescence", formats=("pdf", "png"), dpi=600)
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
| `coolors_palettes.py` | 13 Coolors.co trending palettes (5 discrete + 6 sequential + 2 diverging) + recommendation engine |
| `molecular/` (subpackage) | **2D/3D molecular visualization** — see below |

### Molecular Subpackage (`molecular/`)

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `utils.py` | Single source of truth: CPK colors, atomic properties, bond types, hybridization angles, chromophore classification | `CPK_COLORS`, `ATOMIC_PROPERTIES`, `CHROMOPHORES`, `get_cpk_color()`, `classify_chromophore()` |
| `molvis.py` | 2D ball-and-stick models, sp/sp²/sp³ hybrid orbitals, electron clouds, π orbitals, FRET pairs | `load_mol()`, `draw_ball_stick()`, `draw_sp2_orbital()`, `draw_electron_cloud()`, `draw_pi_orbital()`, `draw_fret_pair()` |
| `crystal.py` | 10 lattice types (SC/BCC/FCC/HCP/Diamond/NaCl/CsCl/ZnS/C60/H2O/CH4), 24 preset crystals, dynamic bonding, physics calculations (volume/density/packing), 2D projection | `generate_lattice()`, `CRYSTAL_DATABASE`, `draw_crystal_2d()`, `calc_unit_cell_volume()`, `plot_crystal()` |
| `render_3d.py` | py3Dmol interactive 3D HTML, 3Dmol.js CDN fallback, MOL block conversion | `render_3d_html()`, `smiles_to_molblock()`, `mol_to_3d_html()` |

**Molecular data**: 21 pre-generated molecule JSON files in `molecule_data/` (PET, PS, PE, PVC, PC, DEHP, OB-1, benzophenone, Nile Red, aging products, etc.). Generate new ones with `node tools/generate_coords.js --smiles "CCO" --name ethanol` (requires RDKit.js WASM from `tools/download_rdkit.ps1`).

## Five Hard Rules

1. **Render at final size, never rescale** — figsize directly sets paper dimensions
2. **Vector first** — PDF/SVG/EPS for data; never JPEG
3. **Colorblind-safe** — Okabe-Ito default + redundant encoding + grayscale check
4. **Readable type at final size** — 7-9pt body, minimum 6pt
5. **Errors must be explained** — caption states SD/SEM/CI + n + test method

## Integration

- **molecular-visualization** (merged v2.2.0) — ball-and-stick models, sp²/sp³ orbitals, electron clouds, FRET, crystal lattices, py3Dmol 3D, 21 molecule datasets, RDKit.js coordinate generator
- **coolors.co trending palettes** (merged v2.1.0) — 13 curated publication-quality color schemes with recommendation engine
- **K-Dense-AI/scientific-agent-skills** — matplotlib and visualization best practices
- **Imbad0202/academic-research-skills** — academic paper quality gates
- **Haojae/scipilot-figure-skill** — visualization advisor workflow, EDA, chart selection, visual QA

## Repository Structure

```
scientific-molecule-publicator/
├── SKILL.md                          # This file
├── README.md
├── LICENSE (MIT)
├── pyproject.toml
├── src/scientific_figure_generator/
│   ├── __init__.py                   # v2.2.0 — 80+ exports
│   ├── style_config.py               # Journal styles + CJK + Coolors integration
│   ├── data_plots.py                 # 7+ plot types
│   ├── mechanism_diagrams.py         # 5 diagram types
│   ├── figure_generator.py           # Multi-panel + spec
│   ├── quality_checker.py            # 7-category gates
│   ├── data_profiler.py              # EDA
│   ├── chart_advisor.py              # 18 interceptions
│   ├── visual_qa.py                  # Self-check loop
│   ├── layout_tools.py               # Panel labels
│   ├── coolors_palettes.py           # 13 Coolors palettes
│   └── molecular/                    # Molecular visualization subpackage
│       ├── __init__.py
│       ├── utils.py                  # CPK/atoms/bonds/hybridization/chromophores
│       ├── molvis.py                 # 2D ball-and-stick + orbitals + clouds
│       ├── crystal.py                # 10 lattices + 24 crystals + physics
│       └── render_3d.py              # py3Dmol 3D HTML
├── molecule_data/                    # 21 pre-generated molecule JSONs
├── tools/
│   ├── generate_coords.js            # Node.js RDKit.js coordinate generator
│   └── download_rdkit.ps1            # RDKit WASM downloader (Windows)
├── references/
│   ├── TrAC_review_format_guide.md   # TrAC journal formatting guide
│   └── journal_style_case_analysis.md # 10-paper style analysis (8 journals)
├── examples/
├── tests/
└── templates/
```

## License

MIT License
