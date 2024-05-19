import pandas as pd
from pandera.extensions import register_check_method


@register_check_method()
def is_sorted_ascending(series: pd.Series) -> bool:
    return series.is_monotonic_increasing
