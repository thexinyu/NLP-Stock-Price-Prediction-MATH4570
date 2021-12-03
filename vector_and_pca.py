from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from store_transcripts import Database
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pymongo import MongoClient

class Vectorizer:
    def __init__(self, tickers):
        self.tickers = tickers
        self.db = MongoClient().transcripts
        
    def query_data(self):
        ''' Function to query for all transcripts and store as list '''
        all_companies = self.db.transcript.find()

        data = {}
        text = []

        for transcript in all_companies:
            data[transcript["name"]+" "+transcript["date"]] = transcript["transcript"]
            text.append(transcript["transcript"])
    
        return data, text  

    def tfidf(self, text):
        ''' Tfidf vectorizer to match words to TFIDF values '''
        vect = TfidfVectorizer(min_df=1, ngram_range = (1, 1)).fit(text)
        bag_of_words = vect.transform(text)
        feature_names = vect.get_feature_names()

        tfidf_df = pd.DataFrame(bag_of_words.toarray(), columns = feature_names)
        #display(tfidf_df)
        return tfidf_df, bag_of_words
    
    def create_pca_df(self, bag_of_words):
        ''' PCA to reduce total number of features before feeding into ML model '''
        # instantiate the PCA object and request reduced number of components (reduces number of columns/features)
        #pca = PCA(n_components=150, random_state=3000)
        pca = PCA(n_components=1, random_state=3000)


        # standardize the features so they are all on the same scale
        features_standardized = StandardScaler().fit_transform(bag_of_words.toarray())

        # transform the standardized features using the PCA algorithm 

        reduced_data = pca.fit_transform(features_standardized)

            

        # show transformed results in dataframe
        pca_df = pd.DataFrame(reduced_data)#, columns = components)

        ''' Obtain target values (whether stock price increased, decreased, or stayed the same) 
        from database '''
        price_changes = []
        all_transcripts = self.db.transcript.find()
        for transcript in all_transcripts:
            price_changes.append(transcript['price_change'])

        pca_df['target'] = price_changes 

        return pca_df

    