"""
Module contains all the descriptive statistics calculations and graphs
"""
#Importing packages
import yfinance as yf
import pandas as pd
from datetime import date
from datetime import datetime, timedelta
import numpy as np
import __getters as gt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Returns summary table consisting of all descriptive statistics
def summary(df_summ):
    _mean = mean(df_summ)
    _range = range(df_summ)
    _quartiles = quartiles(df_summ)
    _sd = sd(df_summ)
    _cv = cv(df_summ)
    _close = df_summ['Close'].tail(1).item()
    _data = {'Name':['Mean', 'Range', ' 1st Quartile', '2nd Quartile / Median', '3rd Quartile', 'Standard Deviation', 'Coefficient of Variation','Price Value'], 'Values':[round(_mean,3), round(_range,3), round(_quartiles[0.25],3), round(_quartiles[0.50],3), round(_quartiles[0.75],3), round(_sd,3), round(_cv,3), round(_close,3)]}
    return pd.DataFrame(data=_data)

#Returns figure for raw time series for Close, Open, High, Low
def raw_time_series(df_rts):
    time_data = df_rts.copy()
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data['Close'], name="Closing Price",line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data['Open'], name="Opening Price",line=dict(color="yellow")))
    fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data['High'], name="Daily High",line=dict(color="green")))
    fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data['Low'], name="Daily Low",line=dict(color="red")))
    fig.layout.update(xaxis_rangeslider_visible=True,height=300,margin=dict(l=5,r=5,b=10,t=10))
    return fig

# Returns mean of dataframe column 'Close'    
def mean(df_desc_stats):
    df_mean = df_desc_stats["Close"].mean()
    return df_mean

# Determines moving average of 'Close' column for a user selected period of days
def n_day_ma(df_ma, days):
    df_ma.loc[:, f"MA{days}"] = df_ma.Close.rolling(days).mean()
    return df_ma

# Calculates the range i.e. the max - min value of closing price
def range(df_desc_stats):
    return df_desc_stats["Close"].max()-df_desc_stats["Close"].min()


# Returns 1st quartile (0.25), median (0.5) and 3rd quartile (0.75)
def quartiles(df_desc_stats):
    return df_desc_stats.Close.quantile([0.25, 0.5, 0.75])

# Determines standard deviation for the Close column over user selected period
def sd(df_desc_stats):
    df_std = (df_desc_stats["Close"].std())
    return df_std

# Calculates exponential moving average (placing a greater weight on recent values) for close column over user selected period
def n_day_ema(df_ema, days):
    df_ema[f"EMA{days}"] = df_ema["Close"].ewm(span=days, adjust=False).mean()
    return df_ema

# Calculates coefficient of variation (standardised measure of dispersion) based on mean and standard deviation
def cv(df_desc_stats):
    df_std = sd(df_desc_stats)
    df_mean = mean(df_desc_stats)
    cv = df_std / df_mean 
    return cv 

#Returns Closing-Volume trend chart
def clo_vol_chart(time_data,change):
    fig=go.Figure()
    y2 = go.layout.YAxis(title= 'Volume', titlefont=dict( family = 'Arial, sans-serif', size = 18, color = 'SteelBlue' ),showgrid=False)
    y2.update(overlaying='y', side='right')
    fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data['Volume'], fill='tozeroy', fillcolor = 'rgba(70, 130, 180,.50)', name = 'Volume', yaxis='y2', mode = 'none' ))
    if(float(change)<0):
        fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data['Close'], name="Closing Price",line=dict(color="red")))
        y1 = go.layout.YAxis(title='Closing Price', titlefont=dict( family = 'Arial, sans-serif', size = 18, color = 'red' ),showgrid=False)
    else:
        fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data['Close'], name="Closing Price",line=dict(color="green")))
        y1 = go.layout.YAxis(title='Closing Price', titlefont=dict( family = 'Arial, sans-serif', size = 18, color = 'green' ),showgrid=False)
    fig.update_xaxes(showgrid=False)
    fig.layout.update(xaxis_rangeslider_visible=True,height=300,margin=dict(l=5,r=5,b=10,t=10),yaxis1 = y1, yaxis2 = y2)
    return fig

#Returns Graph for MA 
def moving_average_trend(time_data,days):
    # Creates a copy of the close column in time_data
    time_data_close = time_data.copy()
    
    # Calculates moving average of "Close" column over user selected period of days
    time_data_ma=n_day_ma(time_data_close, days)
    
    # Plots moving average trend
    fig=go.Figure()
    #Remove NA values
    data = time_data_ma.dropna()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Closing price",line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=data['Date'], y=data[f'MA{days}'], name=f"{days} days Moving Average",line=dict(color="yellow")))
    fig.layout.update(xaxis_rangeslider_visible=True,height=400,margin=dict(l=5,r=5,b=10,t=10))
    return fig

#Returns graph for EMA
def exp_moving_average_trend(time_data,days): 
    # Creates a copy of the close column in time_data
    time_data_close = time_data.copy()
    
    # Calculates exponetial moving average of "Close" column over user selected period of days
    time_data_ema=n_day_ema(time_data_close, days)
   
    # Plots exponential moving average trend
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data_ema['Close'], name="Closing price",line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=time_data['Date'], y=time_data_ema[f'EMA{days}'], name=f"{days} days Exponential Moving Average",line=dict(color="yellow")))
    fig.layout.update(xaxis_rangeslider_visible=True,height=400,margin=dict(l=5,r=5,b=10,t=10))
    return fig
    
    
#Returns graph for MACD    
def moving_average_conv_div(time_data):
    time_data_close = time_data.copy()
    time_data_ema=n_day_ema(time_data_close, 12)
    time_data_ema=n_day_ema(time_data_close, 26)
    time_data_ema.reset_index(inplace=True) 
    time_data_ema['macd'] = time_data_ema['EMA12'] - time_data_ema['EMA26']
    time_data_ema['signal'] = time_data_ema['macd'].ewm(span=9, adjust=False).mean()
    fig=go.Figure()

    fig.add_trace(go.Scatter(x=time_data_ema['Date'], y=time_data_ema["macd"], name="MACD",line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=time_data_ema['Date'], y=time_data_ema["signal"], name="Signal",line=dict(color="orange")))
    fig.layout.update(xaxis_rangeslider_visible=True,height=400,margin=dict(l=5,r=5,b=10,t=10))
    return fig

# Plots a bollinger band one standard deviation above and below the moving average
# Can be used to measure market's volatility.
def bollinger_band(time_data):
    # Creates a copy of the time_data dataframe
    time_data=time_data.copy()
    
    # The default values for the lookback period and n_std is 20 and 2 respectively     
    lookback = 20
    n_std = 2
    
    # Creates upper and lower bands
    hlc_avg = (time_data.High + time_data.Low + time_data.Close) / 3
    mean = hlc_avg.rolling(lookback).mean()
    std = hlc_avg.rolling(lookback).std()
    time_data['upper'] = mean + std * n_std
    time_data['lower'] = mean - std * n_std
    
    # Remove NA values
    data = time_data.dropna()
    
    # Plot exponential moving average
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Closing Price",line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['upper'], name="Upper",marker = { 'color': 'rgba(0,0,0,0)' }, showlegend = False, hoverinfo = 'none',line=dict(color="rgba(70, 130, 180,.50)")))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['lower'], fill='tonexty', fillcolor = 'rgba(70, 130, 180,.20)',showlegend = False,hoverinfo = 'none',line=dict(color="rgba(70, 130, 180,.50)")))
    fig.layout.update(xaxis_rangeslider_visible=True,height=400,margin=dict(l=5,r=5,b=10,t=10))
    # fig.show()
    return fig

    
# Generates a candlestick graph. 
# Each candlestick represents a particular day - can be used to predict short-term price movements based on previous days
def candlestick(time_data):
    fig=go.Figure()
    fig = go.Figure(data=[go.Candlestick(x=time_data['Date'],open=time_data['Open'], high=time_data['High'],low=time_data['Low'], close=time_data['Close'])])
    fig.layout.update(xaxis_rangeslider_visible=True,height=400,margin=dict(l=5,r=5,b=10,t=10))
    return fig

def main():
    hist=yf.download("MSFT",period="1y")
    time_data_up=summary(hist)
    

if __name__ == '__main__':
    main()
    
