import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from datetime import timedelta

class StockPuller:
    def __init__(self):
        self. tickerList = ('AAPL', 
                            'MSFT', 
                            'AMZN', 
                            'FB',
                            'GOOG', 
                            'GOOGL', 
                            'TSLA', 
                            'NVDA', 
                            'PYPL', 
                            'ASML', 
                            'INTC', 
                            'CMCSA', 
                            'NFLX', 
                            'ADBE', 
                            'CSCO', 
                            'PEP', 
                            'AVGO', 
                            'TXN', 
                            'PDD', 
                            'TMUS')
        
    # get historical market data
    def plotAll(self):
        for ticker in self.tickerList:
            ticker = yf.Ticker(ticker)
            hist = ticker.history(period='5y', interval='1d')
            hist["Close"].plot(figsize=(16,9))
        plt.legend(self.tickerList)
        plt.show()
    
    def plotStock(self, ticker):
        stock = yf.Ticker(ticker)
        hist = stock.history(period='5y', interval='1d')
        hist["Close"].plot(figsize=(16,9))
        plt.legend([ticker])
        plt.show()

    def dailyData(self, ticker):
        stock = yf.Ticker(ticker)
        stockData = stock.history(period='5y',interval='1d')
        print(stockData)

    def changeOverDays(self, ticker, startDate, days):
        '''
        Returns the % change of a stocks value in a certan timeframe

        Parameters:
        ticker (str): stock ticker (ex. 'AAPL')
        startDate (str): the day which to start the comparison (ex. '2021-11-02')
        days (int): days that pass on which to compare closing values
        '''
        stock = yf.Ticker(ticker)
        stockData = stock.history(period='5y', interval='1d')

        startDatetime = datetime.strptime(startDate, '%Y-%m-%d')
        endDatetime = startDatetime + timedelta(days=days)

        startPrice = stockData.loc[startDatetime]['Open']
        endPrice = stockData.loc[endDatetime]['Close']
        changeInPrice = startPrice / endPrice
        return changeInPrice - 1

    def changeOverHours(self, ticker, startDate, hours):
        '''
        Returns the % change of a stocks value in a certan timeframe

        Parameters:
        ticker (str): stock ticker (ex. 'AAPL')
        startDate (str): the day which to start the comparison (ex. '2021-11-02')
        hours (int): hours that pass on which to compare closing values
        '''
        stock = yf.Ticker(ticker)
        stockData = stock.history(period='2y', interval='1h')
        stockData.index = stockData.index.tz_localize(None)
        
        # TO DO: limit to only allow times within market open/closing hours (9:30am-4:30pm)
        startDatetime = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        endDatetime = startDatetime + timedelta(hours=hours)

        startPrice = stockData.loc[startDatetime]['Open']
        endPrice = stockData.loc[endDatetime]['Close']
        changeInPrice = (startPrice / endPrice) - 1
        return changeInPrice
        

  
SP = StockPuller()  
SP.plotAll()
SP.plotStock('AAPL')
SP.dailyData('AAPL')
print(SP.changeOverDays('AAPL', '2019-10-02', 50))
print(SP.changeOverHours('AAPL', '2019-11-11 11:30:00', 25))