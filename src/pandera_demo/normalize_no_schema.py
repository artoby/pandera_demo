import pandas as pd
import numpy as np

from pandera_demo.utils.extract_symbols import extract_pair_symbols


def normalize_price_no_schema(df_original: pd.DataFrame) -> pd.DataFrame:
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
