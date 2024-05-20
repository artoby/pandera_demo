import numpy as np
from pandera import Field, SchemaModel
from pandera.typing import DataFrame, Index, Series


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


RawPrice = DataFrame[RawPriceSchema]
