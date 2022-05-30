"""
Module containg functions for Linear Regression Forecasting and Non-Linear Regression Forecasting
"""
#import packages
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression
from datetime import date, datetime
import datetime
import time
from sklearn import metrics
from plotly import graph_objs as go
from fbprophet import Prophet

#Function for Linear Regression Forecasting
def linear_forecasting(data, end_date, prediction_date):
    fdate = (prediction_date - end_date)
    futuredate = fdate.days + 1

    #Setting index as date
    data['Date'] = pd.to_datetime(data.Date)
    data.index = data['Date']

    #converting dates into number of days as dates cannot be passed directly to the regression model
    data.index = (data.index - pd.to_datetime('1970-01-01')).days

    # Convert the pandas series into numpy array
    y = np.asarray(data['Close'])
    x = np.asarray(data.index.values)

    # Model initialization
    # by default the degree of the equation is 1.
    # Hence the mathematical model of a line equation that is y = mx + c
    regression_model = LinearRegression()

    # Train the model
    regression_model.fit(x.reshape(-1, 1), y.reshape(-1, 1))

    # Prediction for historical dates. Calling the learned values.
    y_learn = regression_model.predict(x.reshape(-1, 1))
    y_learned=pd.DataFrame(y_learn,columns=['Learned'])

    # Adding future dates to the date index and passing that index to the regression model for future prediction.
    newindex = np.asarray(pd.RangeIndex(start=x[-1], stop=x[-1] + futuredate))

    # Prediction for future dates
    y_predict = regression_model.predict(newindex.reshape(-1, 1))
    y_predicted=pd.DataFrame(y_predict,columns=['Predicted'])

    #Convert the days index back to dates index for plotting the graph
    x = pd.to_datetime(data.index, origin='1970-01-01', unit='D')
    future_x = pd.to_datetime(newindex, origin='1970-01-01', unit='D')
    #Generating chart for Linear Regression
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=data['Close'], name="Closing Price History"))
    fig.add_trace(go.Scatter(x=x, y=y_learned['Learned'], name="Mathematical Model",line=dict(color="red")))
    fig.add_trace(go.Scatter(x=future_x, y=y_predicted['Predicted'], name="Future predictions",line=dict(color="green")))
    fig.layout.update(xaxis_rangeslider_visible=True,height=300,margin=dict(l=5,r=5,b=10,t=10))
    
    #calculate RMSE and R^2 value
    rmse = np.sqrt(metrics.mean_squared_error(y, y_learned))
    r2 = metrics.r2_score(y, y_learned)

    return fig, rmse, r2, y_predict[-1]


#Function for Non-linear Regression Forecasting
def nlinear_forecasting(data,end_date,prediction_date):
    fdate = (prediction_date - end_date)
    futuredate = fdate.days

    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    #Initialising FBProphet
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=futuredate)
    forecast = m.predict(future)
    #Generating chart for Non-linear Regression
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_train['ds'], y=df_train['y'], name="Closing Price History"))
    fig.add_trace(go.Scatter(x=df_train['ds'], y=forecast.loc[:len(df_train),'yhat'], name="Mathematical Model",line=dict(color="red")))
    fig.add_trace(go.Scatter(x=forecast.loc[len(df_train)-1:,'ds'], y=forecast.loc[len(df_train)-1:,'yhat'], name="Future predictions",line=dict(color="green")))
    fig.add_trace(go.Scatter(x=forecast.loc[len(df_train)-1:,'ds'], y=forecast.loc[len(df_train)-1:,'yhat_lower'], marker = { 'color': 'rgba(0,0,0,0)' }, showlegend = False, hoverinfo = 'none' ))
    fig.add_trace(go.Scatter(x=forecast.loc[len(df_train)-1:,'ds'], y=forecast.loc[len(df_train)-1:,'yhat_upper'], fill='tonexty', fillcolor = 'rgba(0, 204, 102,.20)', name = 'Confidence of Future Predictions', hoverinfo = 'none', mode = 'none' ))
    fig.layout.update(xaxis_rangeslider_visible=True,height=300,margin=dict(l=5,r=5,b=10,t=10))

    metric_df = forecast.set_index('ds')[['yhat']].join(df_train.set_index('ds').y).reset_index()
    metric_df.dropna(inplace=True)
    rmse=np.sqrt(metrics.mean_squared_error(metric_df.y, metric_df.yhat))
    r2=metrics.r2_score(metric_df.y, metric_df.yhat)
    return fig, rmse, r2, forecast['yhat'].tail(1).item()

def main():
    _ticker='AMZN'
    stock_data=yf.download("MSFT",'2016-01-01','2018-01-01')
    stock_data.reset_index(inplace=True)
    prediction_date = input("Enter prediction date in YYYY-MM-DD format: ")
    year, month, day = map(int, prediction_date.split('-'))
    future_date = datetime.date(year, month, day) 
    end_date=datetime.date(2018,1,1)
    linear_forecasting(stock_data,end_date, future_date)
    nlinear_forecasting(stock_data,end_date, future_date)

if __name__=="__main__":
    main()
