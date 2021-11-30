from PdfCleaner import PdfCleaner
from os import listdir
from os.path import isfile, join
from PerformanceTesting import PerformanceTester
import pdfplumber
import json
import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient


class Transcripts:
    def __init__(self, ticker):
        self.ticker = ticker
        self.path = "C:/Users/mtort/Repositories/DS3500-Final-Project/transcripts/"+ticker+"_transcripts/"

    def read_files(self):
        return [f for f in listdir(self.path) if isfile(join(self.path, f))]

    def create_dct(self):
        lst_files = self.read_files()
        lst_cleaned = []
        for file in lst_files:
            file_path = self.path + file
            if file_path[-3:] == 'pdf':
                txt = PdfCleaner(file_path)
                date = file[:8]
                # txt_cleaned = txt.clean_stopwords_punctuation()
                txt_cleaned = txt.clean_nums()
                PerfTest = PerformanceTester()
                PerfTest.setTimeframe('day', 1)
                PerfTest.loadArticles([[self.ticker, date, txt_cleaned]])
                try:
                    classification_xy = PerfTest.aquireTargetValues()
                except KeyError:
                    print(f'''Warning: attempted to access market during weekend or after hours
                          Earnings Transcript {file_path} Not Added
                          ''')
                    continue
                dct_cleaned = {'name': self.ticker, 'date': date, 'transcript': txt_cleaned, 'price_change': classification_xy[1][0]}
                lst_cleaned.append(dct_cleaned)
        return lst_cleaned

class Database:
    def __init__(self):
        client = MongoClient()
        client.drop_database('transcripts')
        self.db = client.transcripts

    def store_data(self, tickers_lst):
        for t in tickers_lst:
            store = Transcripts(t)
            transcript = store.create_dct()
            self.db.transcript.insert_many(transcript)
            print(t + " transcripts stored successfully")
        return self.db

def main():
    tickers = ['AAPL']
        #, 'MSFT', 'FB', 'GOOGL', 'NFLX', 'TSLA', 'ADBE', 'CMCSA', 'COST', 'AMZN']
    # works: APPL, MSFT
    # doesn't work: FB, GOOGL, NFLX, TSLA, ADBE, CMCSA, COST, AMZN

    # 'APPL', 'MSFT', 'FB', 'GOOGL', 'NFLX', 'TSLA', 'ADBE', 'CMCSA', 'COST', 'AMZN'
    # client = MongoClient()
    # client.drop_database('transcripts')
    # db = client.transcripts


    # for t in tickers:
    #     store = Transcripts(t)
    #     transcript = store.create_dct()
    #     # print(transcript)
    #     db.transcript.insert_many(transcript)
    #     print(t + " transcripts stored successfully")

    # db.transcript.find() # client.transcripts.transcript.find()

    database = Database()
    db = database.store_data(tickers)
    all_transcripts = db.transcript.find()
    for transcript in all_transcripts:
        print(transcript)


if __name__ == '__main__':
    main()





