"""
Data profiler for scientific figure generation.

Performs EDA (Exploratory Data Analysis) on input data to inform chart selection:
- Column types (numeric/categorical/datetime/text/id)
- Sample sizes and group distributions
- Distribution statistics (mean, std, skew, kurtosis, outliers)
- Missing values
- Correlation matrix
- Preliminary chart recommendations

Inspired by scipilot-figure-skill profile_data.py.
"""

import numpy as np
import pandas as pd
from collections import namedtuple

ColumnProfile = namedtuple("ColumnProfile", [
    "name", "dtype", "n_unique", "n_missing", "missing_pct",
    "is_numeric", "is_categorical", "is_datetime", "is_id",
    "mean", "std", "min", "max", "median", "skew", "kurtosis",
    "n_outliers", "outlier_pct", "top_values", "group_counts"
])


def profile_data(data, group_cols=None, id_threshold=0.95, categorical_threshold=20):
    """
    Profile a DataFrame or CSV file for scientific plotting.

    Args:
        data: pandas DataFrame or path to CSV file
        group_cols: List of column names to use as grouping variables
        id_threshold: Unique value ratio above which a column is considered an ID
        categorical_threshold: Max unique values for a numeric column to be treated as categorical

    Returns:
        dict with keys: 'columns', 'n_rows', 'n_cols', 'correlations', 'recommendations', 'warnings'
    """
    if isinstance(data, str):
        data = pd.read_csv(data)

    result = {
        "n_rows": len(data),
        "n_cols": len(data.columns),
        "columns": {},
        "correlations": None,
        "recommendations": [],
        "warnings": [],
    }

    numeric_cols = []
    for col in data.columns:
        profile = _profile_column(data[col], id_threshold, categorical_threshold)
        result["columns"][col] = profile
        if profile.is_numeric and not profile.is_id:
            numeric_cols.append(col)

    if len(numeric_cols) >= 2:
        result["correlations"] = data[numeric_cols].corr().round(3)

    if group_cols:
        for gc in group_cols:
            if gc in data.columns:
                result["columns"][gc] = result["columns"][gc]._replace(
                    group_counts=data[gc].value_counts().to_dict()
                )

    for col, prof in result["columns"].items():
        if prof.missing_pct > 20:
            result["warnings"].append(f"Column '{col}' has {prof.missing_pct:.1f}% missing values")
        if prof.is_numeric and prof.n_outliers > 0 and prof.outlier_pct > 5:
            result["warnings"].append(f"Column '{col}' has {prof.outlier_pct:.1f}% outliers")
        if prof.is_numeric and abs(prof.skew) > 2:
            result["warnings"].append(f"Column '{col}' is highly skewed (skew={prof.skew:.2f})")

    result["recommendations"] = _recommend_charts(result, group_cols)
    return result


def _profile_column(series, id_threshold, categorical_threshold):
    """Profile a single column."""
    n = len(series)
    n_missing = series.isna().sum()
    missing_pct = (n_missing / n * 100) if n > 0 else 0
    n_unique = series.nunique()
    unique_ratio = n_unique / n if n > 0 else 0

    is_numeric = pd.api.types.is_numeric_dtype(series)
    is_datetime = pd.api.types.is_datetime64_any_dtype(series)
    is_id = unique_ratio > id_threshold and not is_datetime
    is_categorical = (not is_numeric and not is_datetime) or (
        is_numeric and n_unique <= categorical_threshold and not is_id
    )

    mean = std = min_val = max_val = median = skew = kurtosis = None
    n_outliers = outlier_pct = 0
    if is_numeric and not is_id:
        clean = series.dropna()
        if len(clean) > 0:
            mean = float(clean.mean())
            std = float(clean.std())
            min_val = float(clean.min())
            max_val = float(clean.max())
            median = float(clean.median())
            skew = float(clean.skew()) if len(clean) > 2 else 0
            kurtosis = float(clean.kurtosis()) if len(clean) > 3 else 0
            if len(clean) >= 4:
                q1 = clean.quantile(0.25)
                q3 = clean.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                n_outliers = int(((clean < lower) | (clean > upper)).sum())
                outlier_pct = n_outliers / len(clean) * 100

    top_values = None
    if is_categorical and not is_id:
        top_values = series.value_counts().head(10).to_dict()

    return ColumnProfile(
        name=series.name, dtype=str(series.dtype), n_unique=n_unique,
        n_missing=n_missing, missing_pct=missing_pct,
        is_numeric=is_numeric, is_categorical=is_categorical,
        is_datetime=is_datetime, is_id=is_id,
        mean=mean, std=std, min=min_val, max=max_val,
        median=median, skew=skew, kurtosis=kurtosis,
        n_outliers=n_outliers, outlier_pct=outlier_pct,
        top_values=top_values, group_counts=None
    )


def _recommend_charts(profile, group_cols):
    """Generate preliminary chart recommendations based on data profile."""
    recs = []
    numeric_cols = [c for c, p in profile["columns"].items() if p.is_numeric and not p.is_id]
    categorical_cols = [c for c, p in profile["columns"].items() if p.is_categorical and not p.is_id]

    if group_cols:
        for gc in group_cols:
            if gc in profile["columns"] and profile["columns"][gc].group_counts:
                min_n = min(profile["columns"][gc].group_counts.values())
                if min_n < 10:
                    recs.append({"type": "warning", "chart": "stripplot / box+stripplot",
                        "reason": f"Smallest group has n={min_n} (<10). Use stripplot or box+stripplot.",
                        "avoid": "Mean-only bar chart"})

    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
        recs.append({"type": "recommendation", "chart": "Box plot + stripplot overlay",
            "reason": f"Numeric '{numeric_cols[0]}' by categorical '{categorical_cols[0]}'",
            "x": categorical_cols[0], "y": numeric_cols[0]})

    if len(numeric_cols) >= 2:
        recs.append({"type": "recommendation", "chart": "Scatter plot with regression line",
            "reason": f"Relationship between '{numeric_cols[0]}' and '{numeric_cols[1]}'",
            "x": numeric_cols[0], "y": numeric_cols[1]})

    if len(numeric_cols) >= 3:
        recs.append({"type": "recommendation", "chart": "Correlation heatmap",
            "reason": f"{len(numeric_cols)} numeric variables - correlation matrix",
            "variables": numeric_cols})

    datetime_cols = [c for c, p in profile["columns"].items() if p.is_datetime]
    if datetime_cols and numeric_cols:
        recs.append({"type": "recommendation", "chart": "Line plot with error band",
            "reason": f"Time series: '{numeric_cols[0]}' over '{datetime_cols[0]}'",
            "x": datetime_cols[0], "y": numeric_cols[0]})

    if len(categorical_cols) >= 1 and len(numeric_cols) == 0:
        recs.append({"type": "recommendation", "chart": "Horizontal bar chart (sorted)",
            "reason": f"Distribution of '{categorical_cols[0]}'", "avoid": "Pie chart"})

    return recs


def print_profile_report(profile):
    """Print a human-readable profile report."""
    lines = ["=" * 60, "DATA PROFILE REPORT", "=" * 60]
    lines.append(f"Rows: {profile['n_rows']}, Columns: {profile['n_cols']}")
    lines.append("-" * 60)

    for col, prof in profile["columns"].items():
        lines.append(f"\n[{col}] ({prof.dtype})")
        lines.append(f"  Unique: {prof.n_unique}, Missing: {prof.n_missing} ({prof.missing_pct:.1f}%)")
        if prof.is_numeric and not prof.is_id:
            lines.append(f"  Mean={prof.mean:.3f}, SD={prof.std:.3f}, Median={prof.median:.3f}")
            lines.append(f"  Range=[{prof.min:.3f}, {prof.max:.3f}], Skew={prof.skew:.2f}")
            if prof.n_outliers > 0:
                lines.append(f"  Outliers: {prof.n_outliers} ({prof.outlier_pct:.1f}%)")
        if prof.is_categorical and prof.top_values:
            lines.append(f"  Top values: {list(prof.top_values.items())[:5]}")

    if profile["warnings"]:
        lines.append("\n" + "=" * 60 + "\nWARNINGS:")
        for w in profile["warnings"]:
            lines.append(f"  ! {w}")

    if profile["recommendations"]:
        lines.append("\n" + "=" * 60 + "\nCHART RECOMMENDATIONS:")
        for r in profile["recommendations"]:
            if r["type"] == "warning":
                lines.append(f"  ! {r['chart']}: {r['reason']}")
                lines.append(f"    Avoid: {r['avoid']}")
            else:
                lines.append(f"  > {r['chart']}: {r['reason']}")

    return "\n".join(lines)