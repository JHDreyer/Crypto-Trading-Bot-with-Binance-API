import pandas as pd


def ma(timeperiod, dataframe):
    dataframe['ma'] = dataframe['close'].rolling(window=timeperiod, min_periods=0).mean()
    return dataframe


def dpo(even_timePeriod, dataframe):

    dataframe[f'{even_timePeriod}ma'] = dataframe['close'].rolling(window=even_timePeriod, min_periods=0).mean()
    dataframe['MA_shifted'] = dataframe[f'{even_timePeriod}ma'].shift(periods=int((even_timePeriod / 2) + 1), fill_value=0)
    dataframe['DPO'] = dataframe['close']-dataframe['MA_shifted']
    return dataframe


def vi(n, dataframe):
    # VI from github
    df = dataframe.reset_index()

    i = 0
    TR = [0]
    while i < df.index[-1]:
        Range = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < df.index[-1]:
        Range = abs(df.loc[i + 1, 'high'] - df.loc[i, 'low']) - abs(df.loc[i + 1, 'low'] - df.loc[i, 'high'])
        VM.append(Range)
        i = i + 1
    VI = pd.Series(pd.Series(VM).rolling(n).sum() / pd.Series(TR).rolling(n).sum(), name='Vortex_' + str(n))

    VI.index = dataframe.index
    VI.fillna(method='ffill')
    dataframe['VI+'] = VI
    dataframe = dataframe.fillna(0)
    dataframe['VI-'] = (-1)*dataframe['VI+']
    return dataframe
