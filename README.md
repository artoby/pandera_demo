# pandera_demo
Demo of `pandera` usage to improve code readability and reliability

Video explanation & demo: [link](https://youtu.be/Rj4TnOMgVo8)

# Installation
```bash
pip install pandera
```

# Schema definition example
```python
import numpy as np
from pandera import Field, SchemaModel
from pandera.typing import DataFrame, Index, Series, Category

from .utils.custom_checks import is_sorted_ascending


class RawPriceSchema(SchemaModel):
    index: Index[int] = Field(unique=True)
    symbol: Series[str]
    last_price: Series[np.float64] = Field(nullable=True)
    bid_price: Series[np.float64]
    ask_price: Series[np.float64]
    bid_size: Series[np.float64]
    ask_size: Series[np.float64]
    volume: Series[np.float64]
    scrape_timestamp: Series[str]

class NormalizedPriceSchema(SchemaModel):
    index: Index[int] = Field(unique=True)
    timestamp: Series[np.datetime64] = Field(is_sorted_ascending=True)
    price: Series[np.float32]
    symbol1: Series[Category]
    symbol2: Series[Category]
    volume_24h_sym1: Series[np.float32]

    class Config:
        strict = True

        
NormalizedPrice = DataFrame[NormalizedPriceSchema]
RawPrice = DataFrame[RawPriceSchema]
```

# Schema usage example
```python
from pandera import check_types
from .schema import RawPrice, NormalizedPrice

@check_types
def normalize_price_with_schema(df_original: RawPrice) -> NormalizedPrice:
    # df = ...
    # ...
    df = df[get_schema_columns(NormalizedPrice)]
    return df
```