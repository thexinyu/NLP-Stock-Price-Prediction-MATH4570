from PdfCleaner import PdfCleaner
from os import listdir
from os.path import isfile, join
from PerformanceTester import PerformanceTester
import pdfplumber
import json
import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient


class Transcripts:
    def __init__(self, ticker):
        self.ticker = ticker
        xinyu = "/Users/xinyuwu/Desktop/fall21/ds3500/DS3500-Final-Project"
        marco = "C:/Users/mtort/Repositories/DS3500-Final-Project"
        emily = "/Users/emilywang/Desktop/DS3500-Final-Project-main-2"
        kelly = "/Users/kelly/Desktop/ds3500/DS3500-Final-Project"
        qi = ""
        self.path = xinyu + "/transcripts/"+ticker+"_transcripts/"

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
                dct_cleaned = {'price_change': classification_xy[1][0], 'name': self.ticker, 'date': date, 'transcript': txt_cleaned}
                lst_cleaned.append(dct_cleaned)
        return lst_cleaned




