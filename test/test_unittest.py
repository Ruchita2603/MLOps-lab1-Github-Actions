import unittest

import pandas as pd

from src.data_validator import (
    detect_outliers_iqr,
    load_csv,
    missing_value_report,
    normalize_minmax,
    validate_dataset,
    validate_schema,
)

SCHEMA = {"sqft": "numeric", "bedrooms": "numeric", "price": "numeric"}


class TestDataValidator(unittest.TestCase):
    def setUp(self):
        self.df = load_csv("data/sample.csv")

    def test_load_csv(self):
        self.assertEqual(self.df.shape, (10, 3))

    def test_validate_schema_ok(self):
        self.assertEqual(validate_schema(self.df, SCHEMA), [])

    def test_validate_schema_missing_column(self):
        errs = validate_schema(self.df, {"zipcode": "numeric"})
        self.assertEqual(errs, ["missing column: zipcode"])

    def test_missing_value_report(self):
        self.assertEqual(missing_value_report(self.df)["sqft"], 0.1)

    def test_detect_outliers(self):
        self.assertEqual(detect_outliers_iqr(self.df["sqft"]), [8])

    def test_detect_outliers_bad_k(self):
        with self.assertRaises(ValueError):
            detect_outliers_iqr(self.df["sqft"], k=-1)

    def test_normalize_minmax(self):
        out = normalize_minmax(pd.Series([0, 5, 10]))
        self.assertEqual(list(out), [0.0, 0.5, 1.0])

    def test_validate_dataset(self):
        s = validate_dataset(self.df, SCHEMA)
        self.assertTrue(s["passed"])
        self.assertEqual(s["rows"], 10)


if __name__ == "__main__":
    unittest.main()
