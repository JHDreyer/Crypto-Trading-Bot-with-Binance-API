from runner import trade_buySell
from backtest import back_test_buy
import pandas as pd
from binance_API import current_position, market_price_order, get_1min_ohlc_df_binance
from math import floor

df = get_1min_ohlc_df_binance('BTCUSDT', 2)
print(df.head())

back_test_buy(df)
#trade_buySell('BTCUSDT')
