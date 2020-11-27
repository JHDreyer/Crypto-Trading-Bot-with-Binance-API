import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from indicators import ma, dpo, vi

df = pd.read_csv('BTCUSDT_1min_ohlc_data.csv', parse_dates=True, index_col=0)

df_ohlc = df['close'].resample('40D').ohlc()  # the resmpling of data (smaller set)
df_ohlc = df_ohlc.reset_index()
df_ohlc['date'] = df_ohlc['timestamp'].map(mdates.date2num)
"""
Indicator are specifies here

df['100MA'] = df['close'].rolling(window=50, min_periods=0).mean()
df_volume = df['volume'].resample('5D').sum()

# the bollinger function
timePeriod = 20
k_period = 8
bollingerDataframe = ma(timePeriod, df) # add bollinger to the df
#DPOdataframe = dpo(6, df)
VI = vi(14, df)
"""

"""The plotting starts here"""
style.use('ggplot')
fig = plt.figure()  # figure setup
ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((8, 1), (6, 0), rowspan=3, colspan=1, sharex=ax1)

ax1.xaxis_date()  # converts raw mdates to dates for the axis

ax1.set_title('BTC-USD')  # requested stock
ax1.set_xlabel('Date')
ax1.set_ylabel('Price $')
ax2.set_title('Volume')  # for now

# Plotting:
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
#ax1.plot(df.index, df['100MA'], color='blue')

ax1.plot(bollingerDataframe.index, df[f'{timePeriod}ma'], color='blue')
ax1.plot(bollingerDataframe.index, df['upperBB'], color='black')
ax1.plot(bollingerDataframe.index, df['lowerBB'], color='black')

#ax2.plot(DPOdataframe.index, DPOdataframe['DPO'], color='green')
 # ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
ax2.plot(VI.index, VI['VI+'], color='blue')
ax2.plot(VI.index, VI['VI-'], color='red')

plt.show()
