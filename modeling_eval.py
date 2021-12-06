from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

class Modeling:
    def __init__(self):
        self.estimators = {
            'Logistic Regression' : LogisticRegression(), 
            'Support Vector Machine': LinearSVC(max_iter=1000000),
            'Gaussian Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier()}
        self.models = {}

        self.parameters = ['Base', 'Cross-Validated GridSearch', 'KFold Cross-Validation']
        self.performance = 'placeholder'

    def metrics_df(self):
        # Empty lists to add estimator models and model selection types as column labels
        methods = []
        models = []

        # Add to column names using estimators dictionary
        for parameter in self.parameters:
            for key, value in self.estimators.items():
                methods.append(parameter)
                models.append(key)

        # Performance metrics for each target value (0: Decrease, 1: Increase)
        report_keys = ['0', '1']

        # Different metrics and grouping functions
        report_agg = ['macro avg', 'weighted avg']
        report_values = ['precision', 'recall', 'f1-score', 'support']

        # Initialize empty lists to add metric names
        column_idx = []
        column_metric = []

        # Add to list of row names
        # For performance metrics based off of target value (0, 1)
        for key in report_keys:
            for value in report_values:
                column_idx.append(key)
                column_metric.append(value)

        # For accuracy performance metric
        column_idx.append('all')
        column_metric.append('accuracy')

        # For aggregate performance metrics
        for agg in report_agg:
            for value in report_values:
                column_idx.append(agg)
                column_metric.append(value)
    
    
    
        #part 2: initialize dataframe
        # Define columns and rows (indices) for empty dataframe
        columns = [methods, models]
        indices = [column_idx, column_metric]

        # Fill dataframe with 0 values (to be replaced with actual performance metric values)
        data = [ [0] * len(methods) for _ in range(len(column_idx))]

        # Create dataframe to store evaluation metrics
        self.performance = pd.DataFrame(data, columns = columns, index = indices)
        self.performance.head()
    
    def metrics(self, method, estimator, model, predicted, y_test):
        """ method: scaling, sampling, hyperparameter tuning, etc
            estimator: different models (knn, decision tree, naive bayes)
            model: trained model from given method and estimator
            predicted: using model to run on test set and find predicitons
            y_test: actual values corresponding to predictions"""
        
        # Find predicted and expected outcomes of model
        expected = y_test
        
        # Calculate classification report corresponding to model
        report = classification_report(y_true=expected, y_pred=predicted, output_dict=True)
        
        # Initialize empty list to append and store evaluation matrix values
        data = []
        
        # Add in order of performance dataframe indices
        # Append performance scores for target values (0, 1)
        for i in range(2):
            dct = report[str(i)]
            for metric, value in dct.items():
                data.append(value)
        
        # Append accuracy score
        data.append(report['accuracy'])
        
        # Append aggregated performance scores
        report_labels = ['macro avg', 'weighted avg']
        for label in report_labels:
            for metric, value in report[label].items():
                data.append(value)
        
        # From data list, add in each value to corresponding spot in predefined performance dataframe
        for i in range(len(data)):
            self.performance[method, estimator].iloc[i] = data[i]
            
                    
    def base_models(self, pca_df):
        features = pca_df.drop("target", axis = 1)
        target = pca_df["target"]

        for estimator_name, estimator_object in self.estimators.items():
            # split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(features, target, random_state=3000)

            # select a classifier and create the model by fitting the training data
            model = estimator_object.fit(X=X_train, y=y_train)

            # prediction accuracy
            accuracy_test = model.score(X_test, y_test)
            accuracy_train = model.score(X_train, y_train)
            predicted = model.predict(X=X_test)
            print(estimator_name, ":")
            print("Prediction accuracy on the test data:", f"{accuracy_test:.2%}", "\n")
            print("Prediction accuracy on the test data:", f"{accuracy_train:.2%}", "\n")
            self.metrics('Base', estimator_name, model, predicted, y_test)

    def cross_validation(self, pca_df):
        features = pca_df.drop("target", axis = 1)
        target = pca_df["target"]

        for estimator_name, estimator_object in self.estimators.items():
            #split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(features, target, random_state=3000)

            #select a classifier and create the model by fitting the training data
            model = estimator_object.fit(X=X_train, y=y_train)

            #prediction accuracy
            accuracy = model.score(X_test, y_test)
            print(estimator_name, ":")
            print("Prediction accuracy on the training data:", format(model.score(X_train, y_train)*100, ".2f"))
            print("Prediction accuracy on the test data:", f"{accuracy:.2%}", "\n")
            
            self.models[estimator_name] = model
            
        #     kfold = KFold(n_splits=10, random_state=3000, shuffle=True)
            
        #     scores = cross_val_score(estimator=estimator_object, X=features, y=target, cv=kfold)
            
        #     print(estimator_name + ": \n\t" + f'mean accuracy={scores.mean():.2%}, ' + f'standard deviation={scores.std():.2%}' +"\n")
                            
                            


