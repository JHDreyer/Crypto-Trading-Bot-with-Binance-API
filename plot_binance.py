import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from backtest import back_test_buy

df = pd.read_csv('csv_files/BTCUSDT-1h-data.csv', parse_dates=True, index_col=0)
df = df.drop(['volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'], axis=1)

print(df.head())

df_line = df['close']

msg, returns = back_test_buy(df) # dataframe as parameter for the backtest needs a buy/Sell column for buy/sell positions
print('\n' + msg + '\n')

#returns.to_csv('Returns.csv')
print(returns.head(), returns.tail())
# bb=20, dpo=40,400, vi=200 both, result= 1051% !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""implement simulation option for all parameters to get max
   -Basic idea, run for loops to compare all possible parameters
   - There are 6 total parameters, relationship for some parameters need to be calculated"""

#df_line = df_line.reset_index()
#df_line = df_line.map(mdates.date2num)
#df_trades = df_trades.reset_index()
#df_trades = df_trades.map(mdates.date2num)

fig = plt.figure()  # figure setup
ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((8, 1), (6, 0), rowspan=3, colspan=1, sharex=ax1)

ax1.plot(df_line.index, df_line, color='blue')

#ax2.axhline(xmin=0.5, xmax=0, color='black')

ax2.plot(df.index, df['buySell'], color='red')
plt.show()