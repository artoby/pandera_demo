import pandas as pd
import numpy as np
from pandera import check_types
import logging

from pandera_demo.utils.extract_symbols import extract_pair_symbols
from pandera_demo.utils.schema_helper import get_schema_columns
from pandera_demo.schema.raw_price import RawPrice
from pandera_demo.schema.normalized_price import NormalizedPrice


@check_types
def normalize_price_with_schema(df_original: RawPrice) -> NormalizedPrice:
    df = df_original[['scrape_timestamp', 'last_price', 'volume']].rename(
        columns={
            'last_price': 'price',
            'volume': 'volume_24h_sym1',
        },
    )
    filter_na_price = df['price'].isna()
    if filter_na_price.sum() > 0:
        df = df[~filter_na_price].copy()
        logging.warning(f'price contains some NaN values, dropping them. '
                        f'N={filter_na_price.sum():,}, for example: {df[filter_na_price][:2]}')

    df['price'] = df['price'].astype(np.float32)
    df['volume_24h_sym1'] = df['volume_24h_sym1'].astype(np.float32)

    symbol_map_df = pd.DataFrame({'symbol': df_original['symbol'].unique()})
    symbol_map_df[['symbol1', 'symbol2']] = symbol_map_df['symbol'].apply(extract_pair_symbols).to_list()
    map_sym1 = dict(symbol_map_df[['symbol', 'symbol1']].values)
    map_sym2 = dict(symbol_map_df[['symbol', 'symbol2']].values)
    df['symbol1'] = df_original['symbol'].map(map_sym1).astype('category')
    df['symbol2'] = df_original['symbol'].map(map_sym2).astype('category')

    df['timestamp'] = pd.to_datetime(df['scrape_timestamp'])
    df = df.sort_values(by='timestamp')

    df = df[get_schema_columns(NormalizedPrice)]

    return df
