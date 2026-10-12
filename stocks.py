import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from yfinance import ticker
import re

import requests




class GetData:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_ticker(self):
        try:
            stock = yf.Ticker(self.ticker)
            data = stock.history(period='6mo')


            if data.empty:
                return False
            else:

                data.to_csv(f'{self.ticker}.csv')
        except requests.exceptions.HTTPError:
            return False

    def get_data(self):
        stock_data = pd.read_csv(f'{self.ticker}.csv')
        return stock_data

    def avg_closing(self):
        closing_data = self.get_data()['Close']
        return np.average(closing_data)

    def daily_return(self):
        daily_return_data = self.get_data()['Close']
        return daily_return_data.pct_change() * 100
    def avg_return(self):
        avg_return_data = np.mean(self.daily_return())
        return avg_return_data

    def volatility(self):
        returns = self.daily_return()
        volatility = np.nanstd(returns)
        return volatility
    def moving_average(self, window):
        if window < 0:
            return False

        moving = self.get_data()['Close']
        moving_average_data = moving.rolling(window=window).mean()
        return moving_average_data


    def get_timeframe(self):
        df = self.get_data()
        df['Date'] = pd.to_datetime(df['Date'])
        month = df['Date'].dt.month
        day = df['Date'].dt.day
        month_day = pd.DataFrame([month, day]).values.T
        timeframe = []
        tf_strings = []
        for index, value in enumerate(month_day):
            timeframe.append(value.tolist())
        for row in timeframe:
            tf_strings.append(f'{row[0]}-{row[1]}')
        return tf_strings





def main():
    tick_request = input("Enter ticker: ").upper().strip()
    get = GetData(tick_request)
    if get.get_ticker() is False:
        print("Invalid ticker")
    else:
        return_data(get, tick_request)


def return_data(get, tick_request):
    print(f'average closing price: {get.avg_closing():.02f}$')
    print(f'average daily return: {get.avg_return():.02f}%')
    print(f'volatility: {get.volatility():.02f}%')
    closing_data = get.get_data()['Close']
    timeframe = get.get_timeframe()
    window = 20
    twenty_day_moving_average = get.moving_average(window)
    sp = percent_performance(sandp())
    closing_percent = percent_performance(closing_data)
    plot_moving_closing(timeframe, closing_data, twenty_day_moving_average, window, sp, tick_request, closing_percent)

def plot_moving_closing(x, y, moving_average, window, sp, tick_request, closing_percent):
    x = np.array(x)
    fig, axes = plt.subplots(2, 1, figsize=(12,8), sharex=True)
    axes[0].plot(x, y, label='closing price')
    axes[0].plot(x, moving_average, label=f'{window} day moving average', color='purple')
    axes[0].set_xlabel('Date in month-day')
    axes[0].set_ylabel('USD')
    axes[0].set_title(f'{tick_request} to moving average')
    axes[0].legend()
    axes[0].grid()
    axes[1].plot(x, sp, label='S&P percent performance', color='purple')
    axes[1].plot(x, closing_percent, label=f'{tick_request} percent performance')
    axes[1].set_xlabel('Date in month-day')
    axes[1].set_ylabel('percent performance %')
    axes[1].set_title(f'{tick_request} to S&P 500 percent performance')
    axes[1].legend()
    axes[1].grid()
    plt.xticks(labels=x[0:len(x):10],
               ticks=np.arange(0,len(x),10),
                fontsize=8,
               rotation=45)
    #add grid lines

    plt.tight_layout()
    plt.show()


def sandp():
    hist = yf.Ticker('^GSPC').history(period='6mo')
    hist.to_csv('GSPC.csv')
    sp_data = pd.read_csv('GSPC.csv')
    sp_close = sp_data['Close']
    return sp_close
def percent_performance(x):
    percent_data = []
    for index, value in enumerate(x):
        performance = ((x.iloc[0 + index] - x.iloc[0]) / x.iloc[0]) * 100
        percent_data.append(performance)
    return np.array(percent_data)



if __name__ == "__main__":
    main()