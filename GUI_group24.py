"""
Module for running the Graphical User Interface developed using Streamlit
"""
#Import packages
from requests.sessions import session
import streamlit as st
import pandas as pd
import numpy as np
import __getters as gt
import forecasting as __forecast
import descriptive as _desc
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
import base64

# Plot 
def plot_chart(_figure):
    st.session_state.col2.plotly_chart(_figure, use_container_width=True)

def get_table(values):
    fig=go.Figure(data=go.Table(
                    header=dict(values=list(values.columns),fill_color='#5DADE2',
                        align='center'),
                    cells=dict(values=[values[values.columns.values[x]] for x in range(len(values.columns))],
                        fill_color='#0E1117',
                        align='left')))
    fig.update_layout(margin=dict(l=5,r=5,b=10,t=10),paper_bgcolor = '#0E1117')
    return fig

# Provides option to download dataset as CSV
def download_csv(data):
	csvfile = data.to_csv()
	b64 = base64.b64encode(csvfile.encode()).decode()
	new_filename = "{}.csv".format({st.session_state.tckr})
	href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Download CSV</a>'
	st.session_state.col2.markdown(href,unsafe_allow_html=True)

# Gets data for maximum time range of user selected stock
def get_data():
    st.session_state.orig_data=gt.get_quote(st.session_state.tckr,"max")
    st.session_state.orig_data.reset_index(inplace=True)
    st.session_state.data=st.session_state.orig_data.copy(deep=True)
    st.session_state.company_info=gt.get_info(st.session_state.tckr)
    st.session_state.stock_record=st.session_state.listings[(st.session_state.listings.symbol.str.lower() == st.session_state.tckr.lower())]

# Ensures that start date is not greater than the end date
def time_data_filter():
    if(st.session_state._start_date_<st.session_state._end_date_):
        try:
            st.session_state.data=st.session_state.orig_data.copy(deep=True)
            start_date,end_date=st.session_state._start_date_.strftime("%Y-%m-%d"),st.session_state._end_date_.strftime("%Y-%m-%d")
            st.session_state.data=st.session_state.data[(st.session_state.data['Date']>=start_date)&(st.session_state.data['Date']<=end_date)]
            st.session_state.max_days=len(st.session_state.data)-1
            if st.session_state.number_days>=st.session_state.max_days:
                st.session_state.number_days=int(st.session_state.max_days/2)+1
        except:
            st.session_state.col2.subheader('Please enter a stock symbol.')
    else:
        st.session_state.col2.subheader('Start Date cannot be greater than the End Date.')

# Renders the view each time
def change_view():
    st.session_state.col1,st.session_state.col2=st.columns((1,4))
    st.session_state.col1.markdown("<h1 style='text-align: center; color: #5DADE2;'>Stocks Quote Application</h1>", unsafe_allow_html=True)
    st.session_state.col1.text_input('Enter Stock Symbol',key='tckr',on_change=check_stock)
    filters=st.session_state.col1.expander(label='Query specific time range')
    st.session_state._start_date_=filters.date_input(label='Start Date',key='date_start',value=st.session_state.START_DATE_DEFAULT,min_value=st.session_state.EPOCH,max_value=st.session_state.YESTERDAY)#,on_change=time_data_filter)
    st.session_state._end_date_=filters.date_input(label='End Date',key='date_end',value=st.session_state.DATE_MAX,max_value=st.session_state.DATE_MAX)#,on_change=time_data_filter)
    filters.button('Apply Time Range',key='time_check',on_click=time_data_filter)
    views = ('Overview','Descriptive Statistics','Forecasting','Raw Data')
    st.session_state.col1.selectbox('Select View',views,key='views',index=0)
    try:
        if (st.session_state.tckr!='') & (st.session_state.company_info!='No info.'):
            st.session_state.views_options[st.session_state.views]()
        else:
            page_overview()
    except AttributeError:
        st.session_state.col2.subheader('Please enter a stock symbol.')

# Generates page overview for the user containing information about the company, closing price and associated percentage change
def page_overview():
    if(st.session_state.tckr!=''):
        if(st.session_state.listings[(st.session_state.listings.symbol.str.lower() == st.session_state.tckr.lower())].empty != True):
            if(st.session_state.data.empty==True):
                st.session_state.col2.subheader('No such symbol found, the symbol may be delisted.')
            else:
                st.session_state.col2.header(st.session_state.stock_record.name.item().upper() + " ( "+st.session_state.tckr.upper()+" )")
                st.session_state.col2.metric('Closing Price',st.session_state.stock_record.lastsale.item()[1:],st.session_state.stock_record.netchange.item()+" ("+st.session_state.stock_record.pctchange.item() + " )")
                overview_fig=_desc.clo_vol_chart(st.session_state.data, st.session_state.stock_record.netchange.item())
                plot_chart(overview_fig)
                expander_1=st.session_state.col2.expander(label='Information about the company',expanded=True)
                with expander_1:
                    expander_1.write(st.session_state.company_info)
    else:
        st.session_state.col2.subheader('Please enter a stock symbol.')

#Plots tables and graphs for each of the descriptive statistics optinos
def page_stats():
    if(st.session_state.listings[(st.session_state.listings.symbol.str.lower() == st.session_state.tckr.lower())].empty != True):
        st.session_state.col2.header(st.session_state.stock_record.name.item().upper() + " ( "+st.session_state.tckr+" )")
        desc_menu=('Summary','Simple Moving Average Trend','Exponential Moving Average Trend','MACD','Bollinger Band','Candlestick Diagram')#,'Cumulative Return'),'Relative Strength Index')
        desc_option=st.session_state.col1.selectbox('Select Technical Indicator:', desc_menu,index=0)
        expander_desc=st.session_state.col2.expander(label='Graph Description',expanded=True)
        # Summary page
        if(desc_option=='Summary'):
            st.session_state.col2.subheader("Descriptive Statistics")
            with expander_desc:
                expander_desc.write("Raw Time Series: A chart that displays a sequence of data points that occur throughout a given time period. Time series are usually used in tandem with other technical indicators and allow analysts to identify and track any changes in a given series over time.")
            summary_data=_desc.summary(st.session_state.data)
            rt_fig=_desc.raw_time_series(st.session_state.data)
            plot_chart(rt_fig)
            fig=get_table(summary_data)
            plot_chart(fig)
        elif(desc_option=='Simple Moving Average Trend'):
            st.session_state.col2.subheader("Simple Moving Average Trend")
            with expander_desc:
                expander_desc.write("Simple Moving Average (SMA): A technical indicator calculated by finding the sum of a given range of values for (n) periods and dividing this sum by the total periods (n). SMAs are useful for smoothing out volatility and visualising the price trend of a given stock.")
            st.session_state.max_days=len(st.session_state.data)-1
            days_filter=st.session_state.col1.slider("Select Period (Number of Days):",value=st.session_state.number_days,min_value=1,max_value=st.session_state.max_days)
            ma_fig=_desc.moving_average_trend(st.session_state.data,days_filter)
            plot_chart(ma_fig)
            # st.session_state.col1.button('Plot Graph',key='ma_btn',on_click=_desc.moving_average_trend,args=(st.session_state.data,st.session_state.number_days))
        elif(desc_option=='Exponential Moving Average Trend'):
            st.session_state.col2.subheader("Exponential Moving Average Trend")
            with expander_desc:
                expander_desc.write("Exponential Moving Average (EMA): An indicator in the family of weighted moving averages. This indicator possesses a weighted calculation on top of the moving average calculation that puts more emphasis on recent periods of stock information. This indicator is useful for producing buy and sell signals revolving around crossovers and divergence from historical trends.")
            st.session_state.max_days=len(st.session_state.data)-1
            days_filter=st.session_state.col1.slider("Select Period (Number of Days):",value=st.session_state.number_days,min_value=1,max_value=st.session_state.max_days)
            ema_fig=_desc.exp_moving_average_trend(st.session_state.data,days_filter)
            plot_chart(ema_fig)
            # st.session_state.col1.button('Plot Graph',key='ema_btn',on_click=_desc.exp_moving_average_trend,args=(st.session_state.data,st.session_state.number_days))
        elif(desc_option=='MACD'):
            st.session_state.col2.subheader("Moving Average Convergence/Divergence")
            with expander_desc:
                expander_desc.write("‘Moving Average Convergence Divergence’: Displays the relationship between two moving averages of a stock price. It is calculated by subtracting a 26-period exponential moving average (EMA) from the 12-period EMA. This tool is useful for signaling when to sell or buy if a security crosses above or below the signal line.")
            if(st.session_state.max_days > 27):
                print(st.session_state.data)
                macd_fig=_desc.moving_average_conv_div(st.session_state.data)
                plot_chart(macd_fig)
            else:
                st.session_state.col2.markdown("<h5 style='text-align: center; color: #5DADE2;'>The Time Range for calculating MACD should be greater than 26 days</h5>", unsafe_allow_html=True)
        elif(desc_option=='Bollinger Band'):
            st.session_state.col2.subheader("Bollinger Band")
            with expander_desc:
                expander_desc.write("Bollinger Bands: Allow analysts to determine how volatile stock prices are by visualising a simple moving average trend line that is accompanied by an upper and lower band. These bands are plotted two standard deviations away from the mean. When securities are then plotted against these trendlines it will indicate whether the closing stock prices are high or low in a given period identifying which stocks may be overbought or oversold. ")
            bb_fig=_desc.bollinger_band(st.session_state.data) 
            plot_chart(bb_fig)
        elif(desc_option=='Candlestick Diagram'):
            st.session_state.col2.subheader("Candlestick Diagram")
            with expander_desc:
                expander_desc.write("'Candlestick Diagram: Useful tool that allows for analysts to visualise the high, low, open and closing stock prices for a given period. This chart is useful for deciding when to trade a given security.")
            candle_fig=_desc.candlestick(st.session_state.data)
            plot_chart(candle_fig)  

# Allows user to forecase future stock values with linear and non-linear models
def page_forecast():
    if(st.session_state.listings[(st.session_state.listings.symbol.str.lower() == st.session_state.tckr.lower())].empty != True):
        st.session_state.col2.header(st.session_state.stock_record.name.item().upper() + " ( "+st.session_state.tckr+" )")
        models = ('Linear','Non-Linear')
        forecast_model = st.session_state.col1.selectbox('Select Forecating Model', models,index=0)
        st.session_state._forecast_date_=st.session_state.col1.date_input(label='Forecast Date',value=st.session_state.TODAY + dt.timedelta(days=365),key='date_forecast',min_value=dt.date.today())
        if forecast_model=='Linear':
            st.session_state.col2.subheader("Linear Forecasting")
            linear_fig, linear_rmse, linear_r2, linear_predict=__forecast.linear_forecasting(st.session_state.data,st.session_state._end_date_,st.session_state._forecast_date_)
            plot_chart(linear_fig)
            st.session_state.col2.write("Predicted value for "+st.session_state._forecast_date_.strftime("%Y-%m-%d")+" : "+str(round(linear_predict.item(),2)))
            st.session_state.col2.write("RMSE : "+ str(round(linear_rmse,2)))
            st.session_state.col2.write("R\u00b2 : "+str(round(linear_r2,2)))
            #predictive metrics
        elif forecast_model=='Non-Linear':
            st.session_state.col2.subheader("Non-Linear Forecasting")
            nlinear_fig, nlinear_rmse, nlinear_r2, nlinear_predict=__forecast.nlinear_forecasting(st.session_state.data,st.session_state._end_date_,st.session_state._forecast_date_)
            plot_chart(nlinear_fig)
            st.session_state.col2.write("Predicted value for "+st.session_state._forecast_date_.strftime("%Y-%m-%d")+" : "+str(round(nlinear_predict,2)))
            st.session_state.col2.write("RMSE : "+ str(round(nlinear_rmse,2)))
            st.session_state.col2.write("R\u00b2 : "+str(round(nlinear_r2,2)))

# Gets data for the raw data page
def page_data():
    if(st.session_state.listings[(st.session_state.listings.symbol.str.lower() == st.session_state.tckr.lower())].empty != True):
        st.session_state.col2.header(st.session_state.stock_record.name.item().upper() + " ( "+st.session_state.tckr+" )")
        st.session_state.col2.header('Raw Data')
        fig=get_table(st.session_state.data)
        plot_chart(fig)
        download_csv(st.session_state.data)

# Identfies whether or not a stock exists, and suggests possible stocks in the event of a stock being mistyped 
def check_stock():
    if(st.session_state.tckr!=''):
        if(st.session_state.listings[(st.session_state.listings.symbol.str.lower() == st.session_state.tckr.lower())].empty == True):
            filter_listings = st.session_state.listings [(st.session_state.listings.symbol.str.lower().str.contains(st.session_state.tckr.lower())) | (st.session_state.listings.name.str.lower().str.contains(st.session_state.tckr.lower()))][["symbol","name"]]
            if(filter_listings.empty==True):
                st.session_state.col2.subheader('No such Ticker.')
            else:
                st.session_state.col2.subheader('Did you mean:')
                fig=get_table(filter_listings)
                plot_chart(fig)
        else:
            get_data()
    else:
        st.session_state.data=st.session_state.data.drop(st.session_state.data.index[:])

def main():
    st.set_page_config(page_title="Stock Quotes Application",layout="wide")
    st.session_state.views_options={
        'Overview':page_overview,
        'Descriptive Statistics':page_stats,
        'Forecasting':page_forecast,
        'Raw Data':page_data
    }
    st.session_state.models_options={
        'Linear':'sec_linear',
        'Non-Linear':'sec_nlinear'
    }
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown(f""" <style>
        .reportview-container .main .block-container{{
            padding-top: 1px;
            padding-left: 3rem;
            padding-bottom: 0rem;
        }} </style> """, unsafe_allow_html=True)
    
    if 'last_date' not in st.session_state:
        st.session_state.last_record= gt.get_quote('MSFT','1d')
        st.session_state.last_date=st.session_state.last_record.copy(deep=True)
        st.session_state.last_date.reset_index(inplace=True)
        st.session_state.TODAY = pd.to_datetime(st.session_state.last_date.Date.item()).date()

    if 'listings' not in st.session_state:
      st.session_state.update({
            'ma_graph': 0,
            'data':pd.DataFrame(),
            'orig_data':pd.DataFrame(),
            'quote_data':pd.DataFrame(),
            'stock_record':pd.DataFrame(),
            'company_info':'',
            'listings' : gt.get_listings(),
            'max_days' : 300,
            'EPOCH': dt.datetime(1970,1,1),
            'START_DATE_DEFAULT': st.session_state.TODAY- dt.timedelta(days=365),
            'YESTERDAY': st.session_state.TODAY- dt.timedelta(days=1),
            'DATE_MAX' : st.session_state.TODAY
            })

    if '_forecast_date_' not in st.session_state:
        st.session_state._forecast_date_=st.session_state.TODAY + dt.timedelta(days=365)

    if '_start_date_' not in st.session_state:
        st.session_state._start_date_ = st.session_state.TODAY - dt.timedelta(days=365)

    if '_end_date_' not in st.session_state:
        st.session_state._end_date_ = st.session_state.TODAY

    if 'tckr' not in st.session_state:
        st.session_state.tckr=''

    if 'number_days' not in st.session_state:
        st.session_state.number_days=20

    change_view()

if __name__ == "__main__":
    main()