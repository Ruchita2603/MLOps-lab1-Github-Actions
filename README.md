# MLOps (IE-7374) – GitHub Lab 1: Data Validation with CI

Based on `Github_Labs/Lab1` from the course repo. The lab covers a virtual
environment, a structured repo, unit tests with **pytest** and **unittest**,
and **GitHub Actions** that run those tests automatically.

## My modifications

| Area | Original lab | This repo |
| --- | --- | --- |
| Code under test | `calculator.py`: `fun1`-`fun3` (add, subtract, multiply, with a number type check) and `fun4` (sum of three numbers) | `data_validator.py`: `load_csv`, `validate_schema`, `missing_value_report`, `detect_outliers_iqr`, `normalize_minmax`, and a combined `validate_dataset` |
| Data | `data/` holds only an `__init__.py` | `data/sample.csv` (housing data with one missing value and one outlier) used by the tests |
| Pytest tests | `test_fun1`-`test_fun4`, plain asserts | 10 tests with fixtures, parametrization and `pytest.raises` |
| Unittest tests | `TestCalculator` with four tests, using a `sys.path` workaround | 8 tests with `setUp` and `assertRaises`, no path hacks (`pytest.ini` handles imports) |
| Workflow location | `workflows/` at the repo root, which GitHub does not run | `.github/workflows/`, so the workflows actually execute |
| CI: pytest | Python 3.8, `@v2` actions, push to `main`/`releases/**` | Python 3.10 / 3.11 / 3.12 matrix, `@v4`/`@v5` actions, pip caching |
| CI quality gates | none | flake8 lint, coverage minimum of 90%, JUnit report uploaded per Python version |
| CI triggers | push to `main` (plus issue/label events in the pytest workflow) | push and pull requests to `main`, manual run, weekly schedule (unittest workflow) |
| Dependencies | `pytest` only | `pandas`, `pytest`, `pytest-cov`, `flake8` |

## Structure

```
.
├── .github/workflows/
│   ├── pytest_action.yml
│   └── unittest_action.yml
├── data/sample.csv
├── src/data_validator.py
├── test/
│   ├── test_pytest.py
│   └── test_unittest.py
├── pytest.ini
└── requirements.txt
```

## Run locally

```bash
python -m venv lab_01
source lab_01/bin/activate        # Windows: lab_01\Scripts\activate
pip install -r requirements.txt

pytest --cov=src
python -m unittest test.test_unittest -v
flake8 src test --max-line-length=100
```

## CI

- **Testing with Pytest**: lint, tests and coverage on a 3-version Python matrix, then uploads `pytest-report.xml`.
- **Python Unittests**: runs the unittest suite on Python 3.11.
