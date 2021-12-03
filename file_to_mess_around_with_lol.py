#starbucks predictions
from vector_and_pca import Vectorizer
from pymongo import MongoClient
from modeling_eval import Modeling

import numpy as np
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

tickers = ['AAPL']

estimators = {
            'Logistic Regression' : LogisticRegression(), 
            'Support Vector Machine': LinearSVC(max_iter=1000000),
            'Gaussian Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier()}
parameters = ['Base', 'Cross-Validated GridSearch', 'KFold Cross-Validation']


Creator = Vectorizer(tickers)
Creator.db = MongoClient().transcripts
data, text = Creator.query_data()
tfidf_df, bag_of_words = Creator.tfidf(text)

pca_df = Creator.create_pca_df(bag_of_words)
pca_df


Modeler = Modeling()
print(Modeler.estimators)
print(Modeler.parameters)
pca_metric = Modeler.metrics_df()

Modeler.base_models(pca_df)

Modeler.cross_validation(pca_df)

Modeler.performance


# Modeler.models['Support Vector Machine'].predict(np.array(pca_df[0]).reshape(-1, 1))
# X = np.array(pca_df[0]).reshape(-1, 1)

Creator = Vectorizer(tickers)
Creator.db = MongoClient().starbucks_transcripts
data, text = Creator.query_data()
tfidf_df, bag_of_words = Creator.tfidf(text)
pca_df = Creator.create_pca_df(bag_of_words)
pca_df

X = np.array(pca_df[0]).reshape(-1, 1)
for name, model in estimators.items():
    print(Modeler.models[name].predict(X))
