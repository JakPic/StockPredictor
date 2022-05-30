"""
Text interface stock Application
"""

#Importing packages
import __getters as gt
import forecasting as fc
import descriptive as desc
from datetime import datetime

#Welcome note to the text menu application
def display_welcome():
    print("Welcome to the Stock Quote Application")

#Main Menu
def print_menu():
    print(" 1. Search Stocks\n 2. Query time range\n 3. Descriptive Statistics\n 4. Forecasting\n 5. Download csv\n 6. Read T&C\n 99.Quit\n") 

#Take choice input from all the menu
def get_choice():
    return input("Please choose option: ")

#Choice selection for forecast menu
def get_fchoice():
    return input("Please choose the forecast option: ")

#Choice selection for descriptive statistics menu
def get_dchoice():
    return input("Please choose the descriptive statistics option: ")

#Take input for the name of the ticker
def get_ticker():
    return input(("Enter the ticker symbol: "))

#Input the start and end date and handle start > end error    
def get_date_range():
    a = True
    while a is True:
        start = input("Input the start date YYYY-MM-DD: ")
        end = input("Input the end date YYYY-MM-DD: ")
        if (start > end):
            print("Error: Start Date greater than End Date - Please correct the date")
            continue
        else:
            break    
    return start, end

#Error handling for ticker
def get_error_handling():
    try:
        ticker = get_ticker()
        start, end = get_date_range()
        return gt.get_quote(ticker,start,end), ticker, start, end
    except:
        print('Error: Invalid Symbol - Please try again.') 

#Error handling for ticker
def get_error_handlingN():
    try:
        ticker = get_ticker()
        start, end = get_date_range()
        days = int(input("Enter period(N): "))
        return gt.get_quote(ticker,start,end), ticker, start, end, days
    except:
        print('Error: Invalid Symbol - Please try again.')
    
#Fetch the stock names based on the ticker
def get_search_stock():
    symbol = get_ticker()
    company_list = gt.get_listings()
    if(company_list[(company_list.symbol.str.lower() != symbol.lower())].empty == False):
        filtered_companies = company_list[(company_list.symbol.str.lower().str.contains(symbol.lower()))| (company_list.name.str.lower().str.contains(symbol.lower()))]
        if(filtered_companies.empty==True):
            print("No such Ticker")
        else:
            print('Did you mean: ?')
            print(filtered_companies)

#Input the prediction date and training period - training start and end dates
def get_date_range_forecast():
    train_start = input("Input the training start date YYYY-MM-DD: ")
    train_end = input("Input the training end date YYYY-MM-DD: ")
    train_pred = input("Enter the prediction date YYYY-MM-DD: ")
    start_date = datetime.strptime(train_start, '%Y-%m-%d').date()
    end_date = datetime.strptime(train_end, '%Y-%m-%d').date()
    pred_date = datetime.strptime(train_pred, '%Y-%m-%d').date()
    return start_date, end_date, pred_date
 
#Fetch the stock values based on the start date, end date and ticker value
def get_query_time():
    print("Query Time Range")  
    df_range = get_error_handling()
    print(df_range)
    
#Menu for descriptive statistics   
def get_descriptive_stats():
    print("\n 1. Summary\n 2. Closing & Volume Trend\n 3. Raw Time Series\n 4. Simple Moving Average Trend\n 5. Exponential Moving Average Trend\n 6. Moving Average Convergence/Divergence\n 7. Bollinger Band\n 8. Candlestick Diagram\n")
    forecast = get_dchoice()
    get_descriptive_type(forecast)

#Choice entry for descriptive statistics    
def get_descriptive_type(dchoice):
    if dchoice == "1":
        get_summary()
    elif dchoice == "2":
        get_closing_volume_trend()
    elif dchoice == "3":
        get_raw_time_series()
    elif dchoice == "4":
        get_moving_average_trend()
    elif dchoice == "5":
        get_exp_moving_average_trend()
    elif dchoice == "6":
        get_macd()
    elif dchoice == "7":
        get_bollinger_band()
    elif dchoice == "8":
        get_candlestick()
    else:
        print("Wrong choice, please try again")
        dchoice = get_descriptive_stats()

#Technical indicator - Summary of descriptive statistics
def get_summary():
    print("**************Summary***************")
    df_summary, ticker, start, end = get_error_handling()
    df_summary.reset_index(inplace = True)
    data = desc.summary(df_summary)
    print(data)

#Technical indicator - Closing and volume of each stock with graph
def get_closing_volume_trend():
    print("*************Closing & Volume Trends**************")
    df_clo_vol, ticker, start, end = get_error_handling()
    symbol = ticker
    company_list = gt.get_listings()
    company_value = company_list[(company_list.symbol.str.lower() == symbol.lower())]
    df_clo_vol.reset_index(inplace = True)
    change = float(company_value.netchange.item())
    fig = desc.clo_vol_chart(df_clo_vol,change)
    fig.show()
    
#Technical indicator - Raw time series graph    
def get_raw_time_series():
    print("*************Raw time series***************")
    df_raw, ticker, start, end = get_error_handling()
    fig = desc.raw_time_series(df_raw)
    fig.show()
    
#Technical indicator - Simple moving average value with graph    
def get_moving_average_trend():
    print("*************Simple Moving Average Trends****************")
    df_mat, ticker, start, end, days = get_error_handlingN()
    df_mat.reset_index(inplace = True)
    fig = desc.moving_average_trend(df_mat,days)
    fig.show()
 
#Technical indicator - Exponential moving average value with graph      
def get_exp_moving_average_trend():
    print("*************Exponential Moving Average Trends****************")
    df_emat, ticker, start, end, days = get_error_handlingN()
    df_emat.reset_index(inplace = True)
    fig = desc.exp_moving_average_trend(df_emat,days)
    fig.show()
    
#Technical indicator - Moving Average Convergence/Divergence graph
def get_macd():
    print("*************Moving Average Convergence/Divergence**************")
    df_macd, ticker, start, end = get_error_handling()
    df_macd.reset_index(inplace = True)
    fig = desc.moving_average_conv_div(df_macd)
    fig.show()

#Technical indicator - Bollinger band value with graph    
def get_bollinger_band():
    print("*************Bollinger Band****************")
    df_boll, ticker, start, end = get_error_handling()
    df_boll.reset_index(inplace = True)
    fig = desc.bollinger_band(df_boll)
    fig.show()

#Technical indicator - Candlestick graph    
def get_candlestick():
    print("*************Candlestick Graph****************")
    df_cand, ticker, start, end = get_error_handling()
    df_cand.reset_index(inplace = True)
    fig = desc.candlestick(df_cand)
    fig.show()

#Menu for the type of forecasting        
def get_forecast():
    print("\n 1. Linear forecast\n 2. Non-Linear forecast\n")
    forecast = get_fchoice()
    get_forecast_type(forecast)
 
#Choice entry for Forecasting
def get_forecast_type(fchoice):
    if fchoice == "1":
        print("Linear forecast\n")
        get_linearforecast()
    elif fchoice == "2":
        print("Non-Linear forecast\n")
        get_nlinearforecast()
    else:
        print("Wrong choice, please try again")
        fchoice = get_forecast()

#Linear forecasting with predicted value, RMSE, R^2 and the graphical representation of the prediction
def get_linearforecast():
    ticker = get_ticker()
    start_date, end_date, pred_date = get_date_range_forecast()
    df_fcl = gt.get_quote(ticker,start_date,end_date)
    df_fcl.reset_index(inplace = True)
    fig, rmse, r2, predict = fc.linear_forecasting(df_fcl,end_date,pred_date)
    print("The predicted value is: ", predict)
    print("The RMSE value: ",rmse)
    print("The R^2 value: ",r2)
    fig.show()

#Non-Linear forecasting with predicted value, RMSE, R^2 and the graphical representation of the prediction    
def get_nlinearforecast():
    ticker = get_ticker()
    start_date, end_date, pred_date = get_date_range_forecast()
    df_nfcl = gt.get_quote(ticker,start_date,end_date)
    df_nfcl.reset_index(inplace = True)
    nfig, nrmse, nr2, npredict = fc.nlinear_forecasting(df_nfcl,end_date,pred_date)
    print("The predicted value is: ", npredict)
    print("The RMSE value: ",nrmse)
    print("The R^2 value: ",nr2)
    nfig.show()

#Download the csv file for the queried range of the stock
def get_download_csv():
    ticker = get_ticker()
    start, end = get_date_range()
    data_df = gt.get_quote(ticker,start,end)
    data_df.to_csv(ticker.lower() + '.csv')
    print("Data has been downloaded")
    return data_df

#Choice entry for the Main Menu    
def process_choice(choice):
    while choice !="99":
        if choice == "1":
            get_search_stock()
        elif choice == "2":
            get_query_time()
        elif choice == "3":
            get_descriptive_stats()
        elif choice == "4":
            get_forecast()
        elif choice == "5":
            get_download_csv()
        elif choice == "6":
            get_t_and_c()
        else:
            print("Wrong choice, please try again")
        print_menu() 
        choice = get_choice()        

#Get the terms and conditions from the terms file        
def get_t_and_c():
    print("***************Terms and conditions*******************")
    for line in open("terms.txt"):
        print(line, end = "")
    print("\n")

    
def main():    
    display_welcome()
    print_menu()  
    choice = get_choice()
    process_choice(choice)
    
if __name__ == '__main__':
    main()