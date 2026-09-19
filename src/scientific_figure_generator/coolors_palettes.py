"""
Coolors.co trending color palettes for scientific figure generation.

Source: https://coolors.co/palettes/trending
Curated and categorized for publication-quality scientific figures.

All palettes are verified hex codes from Coolors trending page.
Discrete palettes (5 colors) are suitable for categorical data.
Sequential palettes (9-10 colors) are suitable for continuous/heatmap data.

Integration with matplotlib:
    from scientific_figure_generator.coolors_palettes import get_palette, get_colormap
    colors = get_palette("muted_earthy")  # returns list of hex codes
    cmap = get_colormap("fresh_greens")    # returns LinearSegmentedColormap
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np


DISCRETE_PALETTES = {
    "muted_earthy": {
        "name": "Muted Earthy Tones",
        "url": "https://coolors.co/palette/ffcdb2-ffb4a2-e5989b-b5838d-6d6875",
        "colors": ["#FFCDB2", "#FFB4A2", "#E5989B", "#B5838D", "#6D6875"],
        "best_for": "Environmental science, earth science, sediment/soil data",
        "colorblind_safe": True,
    },
    "soft_lavender": {
        "name": "Soft Lavender",
        "url": "https://coolors.co/palette/22223b-4a4e69-9a8c98-c9ada7-f2e9e4",
        "colors": ["#22223B", "#4A4E69", "#9A8C98", "#C9ADA7", "#F2E9E4"],
        "best_for": "Molecular chemistry, biochemistry, elegant/comparative figures",
        "colorblind_safe": True,
    },
    "summer_sunset": {
        "name": "Summer Sunset",
        "url": "https://coolors.co/palette/ff6b35-f7c59f-efefd0-004e89-1a659e",
        "colors": ["#FF6B35", "#F7C59F", "#EFEFD0", "#004E89", "#1A659E"],
        "best_for": "Warm-cold contrast, temperature data, ocean-atmosphere studies",
        "colorblind_safe": True,
    },
    "fiery_ocean": {
        "name": "Fiery Ocean",
        "url": "https://coolors.co/palette/af3800-fe621d-fd5200-00cfc1-00ffe7",
        "colors": ["#AF3800", "#FE621D", "#FD5200", "#00CFC1", "#00FFE7"],
        "best_for": "High-contrast two-group comparison, hot/cold, risk vs control",
        "colorblind_safe": False,
    },
    "soft_sand": {
        "name": "Soft Sand",
        "url": "https://coolors.co/palette/edede9-d6ccc2-f5ebe0-e3d5ca-d5bdaf",
        "colors": ["#EDEDE9", "#D6CCC2", "#F5EBE0", "#E3D5CA", "#D5BDAF"],
        "best_for": "Background fills, neutral base layers, vintage/heritage themes",
        "colorblind_safe": True,
    },
}


SEQUENTIAL_PALETTES = {
    "fresh_greens": {
        "name": "Fresh Greens",
        "url": "https://coolors.co/palette/d8f3dc-b7e4c7-95d5b2-74c69d-52b788-40916c-2d6a4f-1b4332-081c15",
        "colors": ["#D8F3DC", "#B7E4C7", "#95D5B2", "#74C69D", "#52B788",
                   "#40916C", "#2D6A4F", "#1B4332", "#081C15"],
        "best_for": "Ecology, environmental data, biomass, vegetation indices",
        "colorblind_safe": True,
    },
    "cherry_blossom": {
        "name": "Cherry Blossom Bloom",
        "url": "https://coolors.co/palette/590d22-800f2f-a4133c-c9184a-ff4d6d-ff758f-ff8fa3-ffb3c1-ffccd5-fff0f3",
        "colors": ["#590D22", "#800F2F", "#A4133C", "#C9184A", "#FF4D6D",
                   "#FF758F", "#FF8FA3", "#FFB3C1", "#FFCCD5", "#FFF0F3"],
        "best_for": "Biomedical data, cell viability, concentration-response, medical themes",
        "colorblind_safe": True,
    },
    "sunset_gradient": {
        "name": "Sunset Gradient",
        "url": "https://coolors.co/palette/ff7b00-ff8800-ff9500-ffa200-ffaa00-ffb700-ffc300-ffd000-ffdd00-ffea00",
        "colors": ["#FF7B00", "#FF8800", "#FF9500", "#FFA200", "#FFAA00",
                   "#FFB700", "#FFC300", "#FFD000", "#FFDD00", "#FFEA00"],
        "best_for": "Heatmaps, intensity data, temporal progression, energy levels",
        "colorblind_safe": True,
    },
    "light_steel": {
        "name": "Light Steel",
        "url": "https://coolors.co/palette/f8f9fa-e9ecef-dee2e6-ced4da-adb5bd-6c757d-495057-343a40-212529",
        "colors": ["#F8F9FA", "#E9ECEF", "#DEE2E6", "#CED4DA", "#ADB5BD",
                   "#6C757D", "#495057", "#343A40", "#212529"],
        "best_for": "Grayscale-safe printing, monochrome figures, supplementary material",
        "colorblind_safe": True,
    },
    "warm_neutral": {
        "name": "Warm Neutral Tones",
        "url": "https://coolors.co/palette/582f0e-7f4f24-936639-a68a64-b6ad90-c2c5aa-a4ac86-656d4a-414833-333d29",
        "colors": ["#582F0E", "#7F4F24", "#936639", "#A68A64", "#B6AD90",
                   "#C2C5AA", "#A4AC86", "#656D4A", "#414833", "#333D29"],
        "best_for": "Soil/sediment data, geological samples, organic matter content",
        "colorblind_safe": True,
    },
    "soft_rainbow": {
        "name": "Soft Rainbow",
        "url": "https://coolors.co/palette/fbf8cc-fde4cf-ffcfd2-f1c0e8-cfbaf0-a3c4f3-90dbf4-8eecf5-98f5e1-b9fbc0",
        "colors": ["#FBF8CC", "#FDE4CF", "#FFCFD2", "#F1C0E8", "#CFBAF0",
                   "#A3C4F3", "#90DBF4", "#8EECF5", "#98F5E1", "#B9FBC0"],
        "best_for": "Multi-category data (10 groups), pastel themes, multi-species comparison",
        "colorblind_safe": False,
    },
}


DIVERGING_PALETTES = {
    "ocean_fire": {
        "name": "Ocean Fire (cool-warm diverging)",
        "colors": ["#004E89", "#1A659E", "#EFEFD0", "#F7C59F", "#FF6B35"],
        "best_for": "Change from baseline, anomaly data, before-after comparison",
        "midpoint": "#EFEFD0",
    },
    "lavender_sand": {
        "name": "Lavender Sand (purple-beige diverging)",
        "colors": ["#22223B", "#4A4E69", "#9A8C98", "#C9ADA7", "#F2E9E4"],
        "best_for": "Sophisticated diverging data, molecular property deviations",
        "midpoint": "#9A8C98",
    },
}


ALL_PALETTES = {}
ALL_PALETTES.update(DISCRETE_PALETTES)
ALL_PALETTES.update(SEQUENTIAL_PALETTES)
ALL_PALETTES.update(DIVERGING_PALETTES)


def list_palettes(category=None):
    if category == "discrete":
        return list(DISCRETE_PALETTES.keys())
    elif category == "sequential":
        return list(SEQUENTIAL_PALETTES.keys())
    elif category == "diverging":
        return list(DIVERGING_PALETTES.keys())
    return list(ALL_PALETTES.keys())


def get_palette(name, n_colors=None):
    if name not in ALL_PALETTES:
        available = ", ".join(list_palettes())
        raise KeyError(f"Palette '{name}' not found. Available: {available}")
    colors = ALL_PALETTES[name]["colors"]
    if n_colors is None:
        return list(colors)
    if n_colors <= len(colors):
        return list(colors[:n_colors])
    cmap = LinearSegmentedColormap.from_list(f"coolors_{name}", colors, N=n_colors)
    return [matplotlib.colors.rgb2hex(cmap(i)) for i in np.linspace(0, 1, n_colors)]


def get_colormap(name, n_colors=256):
    colors = get_palette(name)
    if name in SEQUENTIAL_PALETTES or name in DIVERGING_PALETTES:
        return LinearSegmentedColormap.from_list(f"coolors_{name}", colors, N=n_colors)
    return ListedColormap(colors, name=f"coolors_{name}")


def get_palette_info(name):
    if name not in ALL_PALETTES:
        raise KeyError(f"Palette '{name}' not found")
    info = ALL_PALETTES[name].copy()
    if name in DISCRETE_PALETTES:
        info["category"] = "discrete"
    elif name in SEQUENTIAL_PALETTES:
        info["category"] = "sequential"
    else:
        info["category"] = "diverging"
    return info


def preview_palette(name, output_path=None, figsize=(8, 2)):
    colors = get_palette(name)
    info = get_palette_info(name)
    n = len(colors)
    fig, ax = plt.subplots(figsize=figsize)
    for i, color in enumerate(colors):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor="white", linewidth=2))
        ax.text(i + 0.5, -0.15, color, ha="center", va="top", fontsize=7, family="monospace")
    ax.set_xlim(0, n)
    ax.set_ylim(-0.4, 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{info['name']} ({info['category']}, {n} colors) — {info['best_for']}",
                 fontsize=9, pad=10)
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig, ax


def preview_all_palettes(output_path=None, figsize=(10, 12)):
    all_names = list_palettes()
    n = len(all_names)
    ncols = 1
    nrows = n
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    if n == 1:
        axes = [axes]
    for idx, name in enumerate(all_names):
        ax = axes[idx]
        colors = get_palette(name)
        info = get_palette_info(name)
        n_colors = len(colors)
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color,
                                        edgecolor="white", linewidth=1.5))
        ax.set_xlim(0, n_colors)
        ax.set_ylim(-0.3, 1.1)
        ax.set_aspect("equal")
        ax.axis("off")
        cb_tag = "colorblind-safe" if info["colorblind_safe"] else "not colorblind-safe"
        ax.set_title(f"{name} — {info['name']} [{info['category']}, {n_colors}c] {cb_tag}",
                     fontsize=8, loc="left", pad=4)
    fig.suptitle("Coolors.co Trending Palettes — Scientific Figure Collection",
                 fontsize=12, fontweight="bold", y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig, axes


def recommend_palette(data_type="categorical", n_groups=None, colorblind_safe=True,
                      theme=None):
    if data_type in ("continuous", "heatmap"):
        candidates = {
            "environment": "fresh_greens",
            "biomedical": "cherry_blossom",
            "geological": "warm_neutral",
            "print": "light_steel",
            "high_contrast": "sunset_gradient",
        }
        name = candidates.get(theme, "fresh_greens")
        return name, f"Sequential palette for {data_type} data"
    if data_type == "diverging":
        return "ocean_fire", "Diverging palette with neutral midpoint"
    if n_groups and n_groups > 5:
        return "soft_rainbow", f"10-color palette for {n_groups} categories"
    candidates = {
        "environment": "muted_earthy",
        "molecular": "soft_lavender",
        "geological": "muted_earthy",
        "high_contrast": "fiery_ocean",
        "print": "soft_sand",
    }
    name = candidates.get(theme, "summer_sunset")
    if colorblind_safe and not ALL_PALETTES[name]["colorblind_safe"]:
        name = "summer_sunset"
    return name, f"Discrete palette for {n_groups or 'categorical'} groups"
