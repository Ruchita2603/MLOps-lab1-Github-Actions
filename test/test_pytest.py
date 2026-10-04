import pandas as pd
import pytest

from src.data_validator import (
    detect_outliers_iqr,
    load_csv,
    missing_value_report,
    normalize_minmax,
    validate_dataset,
    validate_schema,
)

SCHEMA = {"sqft": "numeric", "bedrooms": "numeric", "price": "numeric"}


@pytest.fixture
def df():
    return load_csv("data/sample.csv")


def test_load_csv(df):
    assert df.shape == (10, 3)


def test_validate_schema_ok(df):
    assert validate_schema(df, SCHEMA) == []


@pytest.mark.parametrize(
    "schema, expected",
    [
        ({"zipcode": "numeric"}, ["missing column: zipcode"]),
        ({"price": "string"}, ["column price should be string"]),
    ],
)
def test_validate_schema_errors(df, schema, expected):
    assert validate_schema(df, schema) == expected


def test_missing_value_report(df):
    report = missing_value_report(df)
    assert report["sqft"] == 0.1
    assert report["price"] == 0.0


def test_detect_outliers_finds_9000(df):
    assert detect_outliers_iqr(df["sqft"]) == [8]


def test_detect_outliers_bad_k(df):
    with pytest.raises(ValueError):
        detect_outliers_iqr(df["sqft"], k=0)


def test_normalize_minmax():
    out = normalize_minmax(pd.Series([10, 20, 30]))
    assert list(out) == [0.0, 0.5, 1.0]


def test_normalize_constant_raises():
    with pytest.raises(ValueError):
        normalize_minmax(pd.Series([5, 5, 5]))


def test_validate_dataset_summary(df):
    s = validate_dataset(df, SCHEMA)
    assert s["passed"] is True
    assert s["rows"] == 10
    assert s["outliers"]["sqft"] == [8]
