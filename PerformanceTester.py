from os import error
from PdfCleaner import PdfCleaner
from StockPuller import StockPuller
   
class PerformanceTester():
    def __init__(self) -> None:
        articleData = []
       
        timeFrame = 'day'
        preferredTimespan = 1
   
    def loadArticles(self, articleList):
        '''
        Loads article data [ticker, date, transcript] into the PerformanceTester interior variable
 
        Parameters:
            articleList (list): a nested list in the form [ticker, date, transcript].This is stock ticker, the date of a report, and the transcript text
        '''
        self.articleData = articleList
   
    def setTimeframe(self, frame='day', span=1):
        '''
        Sets timeframe
 
        Parameters:
            frame (str): what unit (day or hour) are we using to look ahead
            span (int): how many units forward forward do you want the tester to test
        '''
        if frame == 'hour':
            self.timeframe = 'hour'
        elif frame == 'day':
            self.timeframe = 'day'
        else:
            raise Exception('invalid frame')
        self.preferredTimespan = span
   
    def aquireTargetValues(self):
        '''
        Creates x values (list of articles) and y values (list of stock price change after article release) for nlp training
        '''
        x_values = [article[2] for article in self.articleData]
        y_values = []
        Puller = StockPuller()
        for article in self.articleData:
            if self.timeframe == 'day':
                priceChange = Puller.changeOverDays(article[0], article[1], self.preferredTimespan)
            elif self.timeframe == 'hour':
                priceChange = Puller.changeOverHours(article[0], article[1], self.preferredTimespan)
            else:
                raise Exception('Please choose a reference type (\'hour\' or \'day\') using function setTimeframe')
            if priceChange >= 0:
                priceChange = 1
            else:
                priceChange = 0
            y_values.append(priceChange)
        return [x_values, y_values]
       
           
               
               
 
# Test
 
# Get clean stock transcripts
def main():
    origin = PdfCleaner("AAPL Transcripts/APPL_2016Q3.pdf")
    cleaned_text = origin.clean_stopwords_punctuation()
    
    Tester = PerformanceTester()
    articles = [['AAPL', '20191002', cleaned_text], ['AAPL', '20191002', cleaned_text]]
    Tester.loadArticles(articles)
    Tester.setTimeframe('day', 1)
    xy = Tester.aquireTargetValues()
    X = xy[0]
    y = xy[1]
    print('This is the text in list format to input into the model: \n\n', X, '\n\n', 
        'This is the classification in list format (1 for positive movement 0 for negative movement):', y)

if __name__=='__main__':
    main()
