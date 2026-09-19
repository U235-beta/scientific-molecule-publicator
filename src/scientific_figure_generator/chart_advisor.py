"""
Chart advisor for scientific figure generation.

Provides:
- Chart selection decision framework (data shape + argument intent)
- Active interception of common scientific plotting mistakes (18 pitfalls)
- "Same data, different argument -> different chart" mapping

Inspired by scipilot-figure-skill chart_selection.md and viz_pitfalls.md.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ChartRecommendation:
    """A chart recommendation with reasoning."""
    chart_type: str
    reason: str
    x: Optional[str] = None
    y: Optional[str] = None
    alternatives: List[str] = field(default_factory=list)
    is_warning: bool = False
    avoid: Optional[str] = None


@dataclass
class Pitfall:
    """A plotting pitfall to intercept."""
    id: str
    title: str
    consequence: str
    alternative: str
    severity: str = "warning"


PITFALLS = [
    Pitfall("P1", "Mean bar chart with n<10 per group",
            "Hides distribution, reviewers suspect hidden data",
            "Box plot + stripplot overlay, or direct stripplot/dot plot", "error"),
    Pitfall("P2", "Dual Y-axis for unrelated variables",
            "Visual correlation/divergence is fabricated by plotter",
            "Split into stacked subplots sharing x, or standardize to common axis", "error"),
    Pitfall("P3", "Pie chart for proportions",
            "Human angle judgment 3x worse than length",
            "Horizontal bar chart sorted by value", "warning"),
    Pitfall("P4", "3D bar / 3D pie charts",
            "Perspective distorts all values",
            "2D bar, heatmap, or treemap", "error"),
    Pitfall("P5", "Y-axis truncation without indication",
            "Small differences appear artificially large",
            "Start from 0, use log scale, or add explicit break mark", "error"),
    Pitfall("P6", "Line connecting categorical x values",
            "Implies nonexistent continuous relationship",
            "Scatter / dot plot / bar chart", "warning"),
    Pitfall("P7", "Colormap without colorbar",
            "Reader cannot map color intensity to values",
            "Always add colorbar with label and units", "warning"),
    Pitfall("P8", "Too many series in one plot (>8)",
            "Overplotting, impossible to distinguish",
            "Use small multiples / facet grid, or reduce series", "warning"),
    Pitfall("P9", "Rainbow / jet colormap for continuous data",
            "Perceptually non-uniform, creates false peaks",
            "viridis / magma / inferno / cividis / RdBu_r", "error"),
    Pitfall("P10", "One figure with 5+ arguments",
            "No clear message, reader confused",
            "Split into multiple figures, one core claim per figure", "warning"),
    Pitfall("P11", "Error bars without caption explanation",
            "SD vs SEM differ by sqrt(n), can reverse conclusion",
            "Caption must state: error type (SD/SEM/CI), n, test method, correction", "error"),
    Pitfall("P12", "Log scale without indication",
            "Reader misinterprets magnitudes",
            "Explicitly label axis as 'log10(...)'", "warning"),
    Pitfall("P13", "Insufficient font size at final size (<6pt)",
            "Unreadable at print, editor rejects",
            "7-9pt body text, minimum 6pt, set figsize to final dimensions", "error"),
    Pitfall("P14", "JPEG for data figures",
            "Compression artifacts at edges, journal PDF checker rejects",
            "PDF/SVG/EPS for data; TIFF/PNG (300-600dpi) for photos only", "error"),
    Pitfall("P15", "Rescaling figure in Word/LaTeX after export",
            "Font sizes shrink proportionally (9pt -> 4.5pt at 50%)",
            "Set figsize to final dimensions, never rescale after export", "error"),
    Pitfall("P16", "CJK / minus-sign tofu boxes",
            "Chinese characters and negative signs render as squares",
            "Configure CJK font + disable unicode_minus, run visual QA before export", "error"),
    Pitfall("P17", "Panel labels (a/b/c) manually positioned",
            "Misaligned across panels, inconsistent sizing",
            "Use add_panel_labels() with unified figure coordinates", "warning"),
    Pitfall("P18", "No grayscale check for colorblind safety",
            "~8% males, 0.5% females cannot distinguish red-green",
            "Export grayscale preview, verify categories remain distinguishable", "warning"),
]


class ChartAdvisor:
    """
    Advisor that recommends chart types and intercepts common mistakes.

    Usage:
        advisor = ChartAdvisor()
        recs = advisor.recommend(data_profile, argument="group_difference")
        for r in recs: print(r.chart_type, r.reason)
    """

    ARGUMENT_TYPES = [
        "distribution", "proportion", "group_difference",
        "relationship", "trend", "correlation", "composition",
    ]

    def __init__(self):
        self.pitfalls = {p.id: p for p in PITFALLS}

    def recommend(self, data_profile, argument=None, group_cols=None):
        """Recommend chart types based on data profile and argument intent."""
        recs = []
        numeric_cols = [c for c, p in data_profile["columns"].items()
                       if p.is_numeric and not p.is_id]
        categorical_cols = [c for c, p in data_profile["columns"].items()
                           if p.is_categorical and not p.is_id]
        datetime_cols = [c for c, p in data_profile["columns"].items() if p.is_datetime]

        recs.extend(self._check_pitfalls(data_profile, group_cols))

        if argument == "distribution" or (argument is None and len(numeric_cols) == 1 and len(categorical_cols) == 0):
            recs.append(ChartRecommendation("Histogram + KDE overlay",
                f"Show distribution of '{numeric_cols[0]}'", x=numeric_cols[0],
                alternatives=["Box plot", "Violin plot"]))

        elif argument == "proportion" or (argument is None and len(categorical_cols) == 1 and len(numeric_cols) == 0):
            recs.append(ChartRecommendation("Horizontal bar chart (sorted by value)",
                f"Show proportions of '{categorical_cols[0]}'", x=categorical_cols[0],
                alternatives=["Stacked bar", "Treemap"], avoid="Pie chart"))

        elif argument == "group_difference" or (argument is None and len(numeric_cols) >= 1 and len(categorical_cols) >= 1):
            x_col = categorical_cols[0]
            y_col = numeric_cols[0]
            small_n = False
            if group_cols and x_col in group_cols:
                prof = data_profile["columns"].get(x_col)
                if prof and prof.group_counts:
                    small_n = min(prof.group_counts.values()) < 10

            if small_n:
                recs.append(ChartRecommendation("Stripplot / dot plot (show all points)",
                    f"Small sample (n<10) - show individual points for '{y_col}' by '{x_col}'",
                    x=x_col, y=y_col, alternatives=["Box + stripplot overlay"],
                    is_warning=True, avoid="Mean-only bar chart (hides distribution)"))
            else:
                recs.append(ChartRecommendation("Box plot + stripplot overlay",
                    f"Compare '{y_col}' across '{x_col}' groups",
                    x=x_col, y=y_col, alternatives=["Violin plot", "Bar with error bars"]))

        elif argument == "relationship" or (argument is None and len(numeric_cols) >= 2):
            recs.append(ChartRecommendation("Scatter plot with regression line + r value",
                f"Relationship between '{numeric_cols[0]}' and '{numeric_cols[1]}'",
                x=numeric_cols[0], y=numeric_cols[1],
                alternatives=["Hexbin (for large n)", "2D density"]))

        elif argument == "trend" or (argument is None and len(datetime_cols) >= 1 and len(numeric_cols) >= 1):
            recs.append(ChartRecommendation("Line plot with error band (SD/SEM/CI)",
                f"Trend of '{numeric_cols[0]}' over '{datetime_cols[0]}'",
                x=datetime_cols[0], y=numeric_cols[0],
                alternatives=["LOESS smooth", "Area chart"]))

        elif argument == "correlation" or len(numeric_cols) >= 3:
            recs.append(ChartRecommendation("Correlation heatmap (viridis/RdBu_r)",
                f"{len(numeric_cols)} numeric variables - correlation matrix",
                alternatives=["Pairplot / scatterplot matrix", "PCA biplot"]))

        else:
            recs.append(ChartRecommendation("Consult chart_selection framework",
                "Please specify the argument intent (distribution/proportion/group_difference/relationship/trend/correlation)",
                alternatives=self.ARGUMENT_TYPES))

        return recs

    def _check_pitfalls(self, data_profile, group_cols):
        """Check for common pitfalls and return warning recommendations."""
        recs = []
        if group_cols:
            for gc in group_cols:
                prof = data_profile["columns"].get(gc)
                if prof and prof.group_counts:
                    min_n = min(prof.group_counts.values())
                    if min_n < 10:
                        p = self.pitfalls["P1"]
                        recs.append(ChartRecommendation(p.alternative, p.consequence,
                            is_warning=True, avoid=p.title))

        recs.append(ChartRecommendation("Use viridis/magma/cividis colormap",
            "Avoid rainbow/jet colormaps - perceptually non-uniform",
            is_warning=True, avoid="rainbow/jet colormap"))

        recs.append(ChartRecommendation("Specify error type in caption",
            "Caption must state: SD/SEM/CI + n + test method + correction",
            is_warning=True))

        return recs

    def get_pitfall(self, pitfall_id):
        return self.pitfalls.get(pitfall_id)

    def list_pitfalls(self):
        return list(self.pitfalls.values())


def same_data_different_argument():
    """Reference: same dataset, different argument -> different chart."""
    return {
        "distribution": "Histogram + KDE / violin plot",
        "group_difference": "Box + stripplot / bar with error bars",
        "relationship": "Scatter + regression + r value",
        "trend": "Line + error band",
        "proportion": "Horizontal bar (sorted)",
        "correlation": "Correlation heatmap / pairplot",
    }