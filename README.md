# MLOps (IE-7374) – GitHub Lab 1: Data Validation with CI

Based on `Github_Labs/Lab1` from the course repo. The lab covers a virtual
environment, a structured repo, unit tests with **pytest** and **unittest**,
and **GitHub Actions** that run those tests automatically.

## My modifications

## My modifications

- **New code:** replaced the calculator (`fun1`-`fun4`) with `data_validator.py`, which checks a dataset's schema, missing values and outliers, and can normalize a column.
- **New data:** added `data/sample.csv`, a small housing dataset that the tests use.
- **More tests:** 10 pytest tests and 8 unittest tests, including error cases.
- **Working CI:** moved the workflows to `.github/workflows/` so GitHub actually runs them.
- **Better CI:** tests run on Python 3.10, 3.11 and 3.12 with current action versions, and also run on pull requests, manually, and weekly.
- **Quality checks:** flake8 linting and a 90% minimum test coverage.
- **Dependencies:** added `pandas`, `pytest-cov` and `flake8`.

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
