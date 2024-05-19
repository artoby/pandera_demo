from pathlib import Path
import pandas as pd

from pandera_demo.normalize_with_schema import normalize_price_with_schema


def test_normalize_with_schema():
    price_data_path = Path(__file__).parent / "data" / "price_data.csv"
    raw_price_df = pd.read_csv(price_data_path)
    normalized_price_df = normalize_price_with_schema(raw_price_df)

    assert len(normalized_price_df) == 45
