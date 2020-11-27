import pandas as pd
import matplotlib.pyplot as plt
from indicators import dpo, vi, ma
import numpy as np


def calculate_buy_or_sell_position(df):

    # Results from experimental testing of parameters
    # parameters crypto: 3,5,200,600,40,180 (1 minute)

    ma_par = 3
    dpo_par_1 = 5
    dpo_par_2 = 200
    dpo_par_3 = 600
    vi_par_1 = 40
    vi_par_2 = 180

    df_ma = ma(ma_par, df)

    df['buySell_ma'] = np.where(df['close'].astype(float) > df_ma['ma'].astype(float), 5000, -5000)

    df_dpo = dpo(dpo_par_1, df)
    df['DPO_MA1'] = df_dpo['DPO'].rolling(window=dpo_par_2, min_periods=0).mean()
    df['DPO_MA2'] = df_dpo['DPO'].rolling(window=dpo_par_3, min_periods=0).mean()  # was 420
    df['buySell_DPO'] = np.where(df['DPO_MA1'] > df['DPO_MA2'], 5000, -5000)

    df_vi = vi(vi_par_1, df)
    df['VI_MA+'] = df_vi['VI+'].rolling(window=vi_par_2, min_periods=0).mean()  # was 250 both
    df['VI_MA-'] = df_vi['VI-'].rolling(window=vi_par_2, min_periods=0).mean()
    df['buySell_VI'] = np.where(df['VI_MA+'] > df['VI_MA-'], 5000, -5000)

    print('Compiling all indicators')

    df['buySell'] = np.where(df['buySell_DPO'] & df['buySell_VI'] == 5000, 5000, -5000)
    df['buySell'] = np.where(df['buySell'] & df_ma['buySell_ma'] == 5000, 5000, -5000)
    df_buySell = df

    print('Compilation complete')
    return df_buySell


def back_test_buy(df):

    df = calculate_buy_or_sell_position(df)
    datapoints = int(df['close'].size)

    i = 0
    value_open = 0
    value_close = 0
    df = df.reset_index(drop=True)
    buy_sell = [0]

    # get stock price when a trade is indicated (change in buy/sell recommendation)
    while i < df.index[-1]:
        if df.loc[i + 1, 'buySell'] > df.loc[i, 'buySell']:
            value_open = df.loc[i + 1, 'open']
            # df.loc[i+1, 'trade_buy'] = value_open
        if df.loc[i + 1, 'buySell'] < df.loc[i, 'buySell']:
            value_close = df.loc[i, 'close']
            # df.loc[i, 'trade_sell'] = value_close
        if value_open > 0:
            buy_sell.append(value_open)
        if value_close > 0:
            buy_sell.append((-1) * value_close)

        value_open = 0
        value_close = 0
        i += 1

    buy_sell = pd.Series(buy_sell)

    # calculate return on trades (from buy and sell price, buy+ & sell-)
    i = 0
    returns = []

    while i < buy_sell.size:
        if buy_sell[i] > 0 and buy_sell[i + 1] < 0:
            pct = ((buy_sell[i + 1] * (-1) - buy_sell[i]) / buy_sell[i]) * 100
            returns.append(pct)
        i += 1

    returns = pd.Series(returns)
    sum = returns.sum()

    index = 0
    compound_interest = 1
    while index < returns.size:
        if returns[index] >= 0:
            multiplier = (returns[index]/100) + 1
            compound_interest = compound_interest * multiplier
        else:
            multiplier = (returns[index] / 100) - 1
            compound_interest = compound_interest * multiplier

        index += 1

    # this calculation is not compound interest

    print(f'The  simple return is: {sum}\n')
    print(f'The compounded return is {int(compound_interest)}%')
    print(f'The total trades: {int(returns.size)}\n')
    print(f"The total timeperiods: {datapoints} ")
    print(f"The return per timeperiod is {sum/(df['close'].size)}%")

    plt.title('Returns based on the backtest')
    plt.xlabel(f'Number of trades (Over {round(datapoints/1440)} Days) ')
    plt.ylabel(f'% Profit per trade ') #(Sum = {round(sum)}%)
    plt.fill_between(returns.index, returns, color='green')
    plt.axhline(color='black')
    plt.show()
    return

