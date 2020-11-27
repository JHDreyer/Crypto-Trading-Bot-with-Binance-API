from binance.client import Client

import pandas as pd
from datetime import datetime, timedelta
from math import floor

# This file is to update data-frames with current marker quotes(to do buy sell calculations)
# And to make trades using buy sell info
# Automate data collection, analysis and placing buy and sell orders

SYMBOL_TYPE_SPOT = 'SPOT'

ORDER_STATUS_NEW = 'NEW'
ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
ORDER_STATUS_FILLED = 'FILLED'
ORDER_STATUS_CANCELED = 'CANCELED'
ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'
ORDER_STATUS_REJECTED = 'REJECTED'
ORDER_STATUS_EXPIRED = 'EXPIRED'

KLINE_INTERVAL_1MINUTE = '1m'
KLINE_INTERVAL_3MINUTE = '3m'
KLINE_INTERVAL_5MINUTE = '5m'
KLINE_INTERVAL_15MINUTE = '15m'
KLINE_INTERVAL_30MINUTE = '30m'
KLINE_INTERVAL_1HOUR = '1h'
KLINE_INTERVAL_2HOUR = '2h'
KLINE_INTERVAL_4HOUR = '4h'
KLINE_INTERVAL_6HOUR = '6h'
KLINE_INTERVAL_8HOUR = '8h'
KLINE_INTERVAL_12HOUR = '12h'
KLINE_INTERVAL_1DAY = '1d'
KLINE_INTERVAL_3DAY = '3d'
KLINE_INTERVAL_1WEEK = '1w'
KLINE_INTERVAL_1MONTH = '1M'

SIDE_BUY = 'BUY'
SIDE_SELL = 'SELL'

ORDER_TYPE_LIMIT = 'LIMIT'
ORDER_TYPE_MARKET = 'MARKET'
ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

TIME_IN_FORCE_GTC = 'GTC'
TIME_IN_FORCE_IOC = 'IOC'
TIME_IN_FORCE_FOK = 'FOK'

ORDER_RESP_TYPE_ACK = 'ACK'
ORDER_RESP_TYPE_RESULT = 'RESULT'
ORDER_RESP_TYPE_FULL = 'FULL'

# For accessing the data returned by Client.aggregate_trades().
AGG_ID             = 'a'
AGG_PRICE          = 'p'
AGG_QUANTITY       = 'q'
AGG_FIRST_TRADE_ID = 'f'
AGG_LAST_TRADE_ID  = 'l'
AGG_TIME           = 'T'
AGG_BUYER_MAKES    = 'm'
AGG_BEST_MATCH     = 'M'

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)


def get_1min_ohlc_df_binance(ticker_str, number_of_days):

    number_of_days_ago = datetime.now() - timedelta(days=number_of_days)
    date = datetime.strftime(number_of_days_ago, "%d %b, %Y %H:00:00")

    klines = client.get_historical_klines(ticker_str, Client.KLINE_INTERVAL_1MINUTE, date, "today UTC")

    frame = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'  ])
    frame = frame.drop(['volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'], axis=1)
    frame['timestamp'] = pd.to_datetime(frame['timestamp'], unit='ms')
    frame.set_index('timestamp', inplace=True)
    frame.to_csv(ticker_str+'_1min_ohlc_data.csv')

    return frame


def update_data_binance(df_ohlc, str_name_binance):

    # get input df, check last data
    # get values from a specific date to the current date (from binance with the api)
    # IMPLEMENT: is it possible to include the hour to improve efficiency? YES, moving window of data points
    # manipulate into ohlc format
    # update the existing data with the new data
    # It returns a dataframe does not save the updated data as a file, it returns 1 min data

    date = datetime.strftime(datetime.strptime(df_ohlc.last_valid_index(),'%Y-%m-%d %H:%M:%S'), "%d %b, %Y %H:%M:00")
    klines = client.get_historical_klines(str_name_binance, Client.KLINE_INTERVAL_1MINUTE, date, "today UTC")

    new_values = pd.DataFrame(klines,
                         columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                  'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    new_values = new_values.drop(['volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'], axis=1)
    new_values = new_values.iloc[1:]
    new_values['timestamp'] = pd.to_datetime(new_values['timestamp'], unit='ms')
    new_values.set_index('timestamp', inplace=True)

    # IMPLEMENT: for the last part keep last 700 entries (arbitrarily as indicators need a max of 600 for
    # rolling window),
    # to boost preformance

    df_ohlc_updated = df_ohlc.append(new_values)
    '''df_shortened = pd.DataFrame
    # keep only last 700 elements in df (faster processing)
    for index in range(-650, -1):
        df_shortened = df_shortened.append(df_ohlc_updated.iloc[index])'''

    return df_ohlc_updated


def get_top_5_binance():
    prices = client.get_all_tickers()

    for index in prices:
        if index["symbol"] == "BTCUSDT":
            print("BTCUSDT price is: " + index["price"])

        if index["symbol"] == "ETHBTC":
            print("ETHBTC price is: " + index["price"])

        if index["symbol"] == "XRPBTC":
            print("XRPBTC price is: " + index["price"])

        if index["symbol"] == "EOSBTC":
            print("EOSBTC price is: " + index["price"])

        if index["symbol"] == "LTCBTC":
            print("LTCBTC price is: " + index["price"])

    return


def all_fees():
    fees = client.get_trade_fee()
    return fees


def market_price_order(symbol_binance, quantity, type):

    if type == 'BUY':
        market_order = client.order_market_buy(
            symbol=symbol_binance,
            quantity=quantity)
    elif type == 'SELL':
        market_order = client.order_market_sell(
            symbol=symbol_binance,
            quantity=quantity)
    else:
        print('\nError: type of order not specified correctly')

    return market_order


def current_position(str_name_binance, str_name_binance_pair):

    # this function returns the current position of the trading pair (long/ short),
    # and returns the quantity of asset that can be traded

    # IMPLEMENT THIS: get symbol info, read precision required and
    # implement the rounding needed (line 238/9 does it work?)

    # this records change in balances of the trading pair

    balance = client.get_asset_balance(asset=str_name_binance)
    balance_pair = client.get_asset_balance(asset=str_name_binance_pair)

    print(f"{balance['free']} {str_name_binance} is available")
    print(f"{balance_pair['free']} {str_name_binance_pair} is available")

    available_coin = balance['free']
    available_coin_pair = balance_pair['free']

    date = str(datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S'))  # error
    date_and_balance = {'Date': date, f'{str_name_binance}': available_coin,
                        f'{str_name_binance_pair}': available_coin_pair}
    df_date_and_balance = pd.DataFrame(date_and_balance, index=[0])
    df_date_and_balance.set_index('Date')

    try:
        df = pd.read_csv(f'{str_name_binance}_portfolio_price_over_time.csv')
        df_available_coin = df.append(date_and_balance, ignore_index=True)
        df_available_coin.set_index('Date', inplace=True)

    except:
        df_available_coin = pd.DataFrame(date_and_balance, index=[0])
        df_available_coin.set_index('Date', inplace=True)

    df_available_coin.to_csv(f'{str_name_binance}_portfolio_price_over_time.csv')
    print('Balance logged')

    balances = {'balance': available_coin, 'balance_pair': available_coin_pair}

    prices = client.get_all_tickers()

    # loop for the current asset
    # price (through list of all assets and prices from Binance)
    for index in prices:
        if index["symbol"] == "BTCUSDT":
            current_BTC_price = float(index['price'])
            current_USDT_price_ito_BTC = float(1/current_BTC_price)

            BTC_portfolio_current = float(balances['balance'])
            USDT_portfolio_current = float(balances['balance_pair'])

            # manipulate amounts to a valid precision (get precision from info) for the API

            info = client.get_symbol_info('BTCUSDT')
            min_qty = info['filters'][2]['minQty']
            min_qty = float(min_qty)

            USDT_ito_BTC_balance = USDT_portfolio_current * current_USDT_price_ito_BTC

            sell_amount_BTC = floor(BTC_portfolio_current*(1/min_qty))/(1/min_qty)
            buy_amount_BTC = floor(USDT_ito_BTC_balance*(1/min_qty))/(1/min_qty)

            # display balances to user in terminal

            print('The balances in terms of BTC is:')
            print(f"  The current BTC balance (sellable) is {sell_amount_BTC}BTC")
            print(f"  The current USDT balance (buyable) in BTC is {buy_amount_BTC}BTC")

            if sell_amount_BTC > buy_amount_BTC:
                trading_position = 'LONG'
            else:
                trading_position = 'SHORT'

            trading_position = {'position': trading_position, 'btc_balance': sell_amount_BTC,
                                'usdt_ito_btc': buy_amount_BTC}

    return trading_position






