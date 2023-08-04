import numpy as np
import pandas as pd


from sklearn.base import (
    BaseEstimator,
    ClassifierMixin,
)
from sklearn.tree import DecisionTreeRegressor

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from sklearn.preprocessing import OrdinalEncoder


class TrimEstimator(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.count_vector = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()
        self.clf = MultinomialNB()
        self.encoder = OrdinalEncoder()

    def fit(self, X, y=None):
        _y = self.encoder.fit_transform(y)
        train_counts = self.count_vector.fit_transform(X["VehFeats"])
        train_tfidf = self.tfidf_transformer.fit_transform(train_counts)
        print(train_tfidf.shape)
        self.clf.fit(train_tfidf, _y)
        return self

    def predict(self, X):
        train_counts = self.count_vector.transform(X["VehFeats"])
        train_tfidf = self.tfidf_transformer.transform(train_counts)
        print(train_tfidf.shape)
        res = self.clf.predict(train_tfidf)
        # print(res)
        return self.encoder.inverse_transform(res.reshape(-1, 1))


class WK2Estimator(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.cont_cols = [
            "SellerRating",
            "SellerRevCnt",
            "VehListdays",
            "VehMileage",
        ]
        self.cat_cols = [
            "SellerState",
            "VehYear",
            "VehPriceLabel",
            "Vehicle_Trim",
            "history",
        ]
        self.params = {
            "criterion": "friedman_mse",
            "max_depth": 17,
            "max_features": None,
            "min_samples_leaf": 5,
            "splitter": "random",
        }
        self.clf = DecisionTreeRegressor(**self.params)

    def fit(self, X, y=None):
        self.columns = [
            col
            for col in X.columns
            if any((c in col) and (c!=col) for c in self.cont_cols + self.cat_cols)
        ]
        print(self.columns)
        print(all(c in X.columns for c in self.columns))
        print(X[self.columns].iloc[0])
        self.clf.fit(X[self.columns], y)
        return self

    def predict(self, X):
        _X = pd.DataFrame(index=X.index)
        for col in self.columns:
            if col in X.columns:
                _X[col] = X[col]
            else:
                _X[col] = np.zeros(shape=len(X.index), dtype=np.float_)
        return self.clf.predict(_X[self.columns])


class XT5Estimator(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.cont_cols = [
            "SellerRating",
            "SellerRevCnt",
            "VehListdays",
            "VehMileage",
        ]
        self.cat_cols = [
            "SellerState",
            "VehYear",
            "VehPriceLabel",
            "Vehicle_Trim",
            "history",
        ]
        self.params = {
            "criterion": "squared_error",
            "max_depth": 14,
            "max_features": None,
            "min_samples_leaf": 3,
            "splitter": "random",
        }
        self.clf = DecisionTreeRegressor(**self.params)

    def fit(self, X, y=None):
        self.columns = [
            col
            for col in X.columns
            if any((c in col) and (c!=col) for c in self.cont_cols + self.cat_cols)
        ]
        self.clf.fit(X[self.columns], y)
        return self

    def predict(self, X):
        _X = pd.DataFrame(index=X.index)
        for col in self.columns:
            if col in X.columns:
                _X[col] = X[col]
            else:
                _X[col] = np.zeros(shape=len(X.index), dtype=np.float_)
        return self.clf.predict(_X[self.columns])
