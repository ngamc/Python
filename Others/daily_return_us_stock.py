import pandas as pd
import matplotlib.pyplot as plt
import os

def symbol_to_path(symbol, base_dir="us_stock"):
       return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        dftmp=pd.read_csv(symbol_to_path(symbol),index_col='Date', usecols=['Date','Adj Close'] )
        dftmp=dftmp.rename(columns={'Adj Close':symbol})

        df=df.join(dftmp)
        if symbol=='SPY':
               df=df.dropna()
        

    return df

def plot_data(df, title="stock prices",xlabel="Date", ylabel="Price"):
       ax=df.plot(title=title, fontsize=9)
       ax.set_xlabel(xlabel)
       ax.set_ylabel(ylabel)
       plt.show()

def normalize_data(df):
       return df/df.ix[0,:]

def multiple_stock():
       start_date='2010-01-22'
       end_date='2010-01-26'
       dates=pd.date_range(start_date, end_date)

       df1=pd.DataFrame(index=dates)
       #print (df1)

       dfSPY=pd.read_csv('data/AAPL.csv', index_col='Date', usecols=['Date','Adj Close'] )
       dfSPY=dfSPY.rename(columns={'Adj Close':'SPY'})
       #print (dfSPY)

       
       df1=df1.join(dfSPY, how = 'inner')
       df1=df1.dropna()   # delte those nan lines
       #print (df1)

       # read in more stocks
       symbols = ['GOOG', 'IBM', 'GLD']
       for symbol in symbols:
              df_temp=pd.read_csv('data/{}.csv'.format(symbol), index_col='Date', usecols=['Date','Adj Close'] )
              df_temp=df_temp.rename(columns={'Adj Close':symbol})
              df1=df1.join(df_temp, how='inner')
       print (df1)

def test_run():
       df=pd.read_csv("data/AAPL.csv")
       #print (df)
       print ("last five lines")
       print (df.tail(5))

       print ("10 to 20 rows")
       print (df[10:21])
       print ("Max close: " + str(df['Close'].max()))

       df[['Close','Adj Close']].plot()
       plt.show()

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    #return pd.rolling_mean(values, window=window)
    return values.rolling(window=window, center=False).mean()


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    #return pd.rolling_std(values,window=window)
    return values.rolling(window=window,center=False).std()


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    # TODO: Compute upper_band and lower_band
    upper_band=rm+rstd*2
    lower_band=rm-rstd*2
    return upper_band, lower_band

def compute_daily_returns(df):
       daily_returns = (df/df.shift(-1,None,0))-1
       daily_returns.ix[0,:]=0
       return daily_returns

def daily_return_test():
    # Read data
    dates = pd.date_range('2012-07-01', '2012-07-31')  # one month only
    symbols = ['SPY','XOM']
    df = get_data(symbols, dates)
    plot_data(df)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")


#test_run()
#multiple_stock()

#dates = pd.date_range('2010-01-1', '2010-12-31')
#symbols = ['XOM', 'GOOG', 'GLD']
#df = get_data(symbols, dates)
#df=normalize_data(df)
#plot_data(df,"another title")
#print (df.mean())
#print (df.median())
#print (df.std())

#dates = pd.date_range('2010-01-1', '2010-12-31')
#symbols=['SPY']
#df=get_data(symbols, dates)
#ax=df['SPY'].plot(title="SPY rolling means", label='SPY')
#rm_SPY=pd.rolling_mean(df['SPY'], window=20)
#rm_SPY=df['SPY'].rolling(window=20, center=False).mean()
#rm_SPY.plot(label='rolling mean', ax=ax)
#ax.legend(loc='upper left')
#plt.show()

#dates = pd.date_range('2012-01-01', '2012-12-31')
#symbols = ['SPY']
#df = get_data(symbols, dates)

# Compute Bollinger Bands
# 1. Compute rolling mean
#rm_SPY = get_rolling_mean(df['SPY'], window=20)

# 2. Compute rolling standard deviation
#rstd_SPY = get_rolling_std(df['SPY'], window=20)

# 3. Compute upper and lower bands
#upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)
    
# Plot raw SPY values, rolling mean and Bollinger Bands
#ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
#rm_SPY.plot(label='Rolling mean', ax=ax)
#upper_band.plot(label='upper band', ax=ax)
#lower_band.plot(label='lower band', ax=ax)

# Add axis labels and legend
#ax.set_xlabel("Date")
#ax.set_ylabel("Price")
#ax.legend(loc='upper left')
#plt.show()

daily_return_test()
