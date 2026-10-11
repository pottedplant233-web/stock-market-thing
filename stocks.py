import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from yfinance import ticker


class GetData:
    def __init__(self, ticker):
        self.ticker = ticker
    def get_ticker(self):
        stock = yf.Ticker(self.ticker)
        data = stock.history(period='1mo')

        if data.empty:
            return False
        else:

            data.to_csv(f'{self.ticker}.csv')

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

def main():
    tick_request = input("Enter ticker: ").upper().strip()
    get = GetData(tick_request)
    if get.get_ticker() == False:
        print("Invalid ticker")
    else:
        return_data(get)
        #plot data
def return_data(get):
    print(f'average closing price: {get.avg_closing():.02f}$')
    print(f'average daily return: {get.avg_return():.02f}%')
    print(f'volatility: {get.volatility():.02f}%')



if __name__ == "__main__":
    main()