from Transcripts import Transcripts
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
