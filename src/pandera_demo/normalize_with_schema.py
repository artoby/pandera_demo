import pandas as pd
import numpy as np
from pandera import Field, SchemaModel, check_types
from pandera.typing import DataFrame, Index, Series, Category

from pandera_demo.utils.extract_symbols import extract_pair_symbols
from pandera_demo.utils.schema_helper import get_schema_columns


class RawPriceSchema(SchemaModel):
    index: Index[int] = Field(unique=True)
    symbol: Series[str] = Field(nullable=True)
    last_price: Series[np.float64]
    bid_price: Series[np.float64]
    ask_price: Series[np.float64]
    bid_size: Series[np.float64]
    ask_size: Series[np.float64]
    volume: Series[np.float64]
    scrape_timestamp: Series[str]


RawPrice = DataFrame[RawPriceSchema]


class NormalizedPriceSchema(SchemaModel):
    index: Index[int] = Field(unique=True)
    timestamp: Series[np.datetime64]
    price: Series[np.float32]
    symbol1: Series[Category]
    symbol2: Series[Category]
    volume_24h_sym1: Series[np.float32]


NormalizedPrice = DataFrame[NormalizedPriceSchema]


@check_types
def normalize_price_with_schema(df_original: RawPrice) -> NormalizedPrice:
    df = df_original[['scrape_timestamp', 'last_price', 'volume']].rename(
        columns={
            'last_price': 'price',
            'volume': 'volume_24h_sym1',
        },
    )
    df['price'] = df['price'].astype(np.float32)
    df['volume_24h_sym1'] = df['volume_24h_sym1'].astype(np.float32)

    symbol_map_df = pd.DataFrame({'symbol': df_original['symbol'].unique()})
    symbol_map_df[['symbol1', 'symbol2']] = symbol_map_df['symbol'].apply(extract_pair_symbols).to_list()
    map_sym1 = dict(symbol_map_df[['symbol', 'symbol1']].values)
    map_sym2 = dict(symbol_map_df[['symbol', 'symbol2']].values)
    df['symbol1'] = df_original['symbol'].map(map_sym1).astype('category')
    df['symbol2'] = df_original['symbol'].map(map_sym2).astype('category')

    df['timestamp'] = pd.to_datetime(df['scrape_timestamp'])

    return df
