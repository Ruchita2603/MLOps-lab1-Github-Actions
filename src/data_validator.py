"""Small data-validation toolkit (replaces the lab's calculator.py).

Mirrors the original lab layout: simple building blocks plus one
function that combines them, so each piece can be unit tested.
"""
import pandas as pd


def load_csv(path):
    """Load a CSV file and fail clearly if it is empty."""
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Dataset is empty")
    return df


def validate_schema(df, required_columns):
    """Return a list of schema problems (empty list means valid).

    required_columns maps column name -> 'numeric' or 'string'.
    """
    errors = []
    for col, kind in required_columns.items():
        if col not in df.columns:
            errors.append(f"missing column: {col}")
            continue
        is_numeric = pd.api.types.is_numeric_dtype(df[col])
        if kind == "numeric" and not is_numeric:
            errors.append(f"column {col} should be numeric")
        if kind == "string" and is_numeric:
            errors.append(f"column {col} should be string")
    return errors


def missing_value_report(df):
    """Fraction of missing values per column, rounded to 3 places."""
    return {c: round(float(df[c].isna().mean()), 3) for c in df.columns}


def detect_outliers_iqr(series, k=1.5):
    """Return index labels of values outside [Q1 - k*IQR, Q3 + k*IQR]."""
    if k <= 0:
        raise ValueError("k must be positive")
    s = series.dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    mask = (s < q1 - k * iqr) | (s > q3 + k * iqr)
    return list(s[mask].index)


def normalize_minmax(series):
    """Scale a numeric series to the [0, 1] range."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        raise ValueError("Cannot normalize a constant column")
    return (series - lo) / (hi - lo)


def validate_dataset(df, required_columns):
    """Combine every check into one summary dict."""
    errors = validate_schema(df, required_columns)
    summary = {
        "rows": len(df),
        "schema_errors": errors,
        "missing": missing_value_report(df),
        "outliers": {},
    }
    if not errors:
        for col, kind in required_columns.items():
            if kind == "numeric":
                summary["outliers"][col] = detect_outliers_iqr(df[col])
    summary["passed"] = not errors
    return summary
