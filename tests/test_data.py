import pandas as pd, pytest, os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "finrebut600.csv")

def test_file_exists():
    assert os.path.isfile(DATA_PATH), "finrebut600.csv missing"

def test_shape():
    df = pd.read_csv(DATA_PATH)
    assert len(df) == 600, f"Expected 600 rows, got {len(df)}"

def test_columns():
    df = pd.read_csv(DATA_PATH)
    assert list(df.columns) == ["text", "rebuttal"], f"Wrong columns: {df.columns}"
