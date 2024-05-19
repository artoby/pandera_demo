import numpy as np
from pandera import Field, SchemaModel
from pandera.typing import DataFrame, Index, Series, Category

from pandera_demo.utils.is_sorted_ascending import is_sorted_ascending


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
