import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    def plotStock(self, stock):
        ticker = yf.Ticker(stock)
        hist = ticker.history(period='5y', interval='1d')
        hist["Close"].plot(figsize=(16,9))
        plt.legend(stock)
        plt.show()

    def dailyData(self, ticker):
        stock = yf.Ticker(ticker)
        stockData = stock.history(period='5y',interval='1d')
        print(stockData)
  
SP = StockPuller()  
SP.plotAll()
SP.plotStock('AAPL')
SP.dailyData('AAPL')