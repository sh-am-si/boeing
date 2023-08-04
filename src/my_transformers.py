import numpy as np
import pandas as pd
import re

from sklearn.base import (
    BaseEstimator,
    TransformerMixin,
)

from sklearn.impute import SimpleImputer


from sklearn.preprocessing import OneHotEncoder


def get_features(st: str) -> str:
    if isinstance(st, str):
        pattern = r"\'(.*?)\'"
        m = re.findall(pattern, st[1:-1])
        return " ".join(m) if m else ""
    return ""


class FeatureTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X["VehFeats"] = X["VehFeats"].map(get_features)
        return X


class MainCleanerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()
        self.col = [
            "SellerIsPriv",
            "VehType",
            "VehBodystyle",
            "VehFuel",
            "VehMake",
        ]
        self.nan_col = ["Vehicle_Trim", "Dealer_Listing_Price", "VehMileage"]

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for col in self.col:
            if col in X.columns:
                X.drop(columns=col, inplace=True)
        return X


class NanCleanerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        self.cont_cols = [
            "SellerRating",
            "SellerRevCnt",
            "VehListdays",
            "VehMileage",
        ]
        self.cat_cols = [
            "SellerListSrc",
            "SellerName",
            "VehColorExt",
            "VehDriveTrain",
            "VehFeats",
            "VehFuel",
            "VehHistory",
            "VehPriceLabel",
            "VehSellerNotes",
            "VehType",
        ]
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for cont in self.cont_cols:
            if cont in X.columns:
                X[cont] = SimpleImputer(
                    missing_values=np.nan, strategy="mean"
                ).fit_transform(X[[cont]])

        for cat in self.cat_cols:
            if cat in X.columns:
                X[[cat]] = SimpleImputer(
                    missing_values=np.nan, strategy="constant", fill_value=""
                ).fit_transform(X[[cat]])

        if "VehYear" in X.columns:
            X[["VehYear"]] = SimpleImputer(
                missing_values=np.nan, strategy="constant", fill_value=2018
            ).fit_transform(X[["VehYear"]])
        if "SellerRevCnt" in X.columns:
            X[["SellerRevCnt"]] = SimpleImputer(
                missing_values=np.nan, strategy="constant", fill_value=2018
            ).fit_transform(X[["SellerRevCnt"]])
        if "VehListdays" in X.columns:
            X[["VehListdays"]] = SimpleImputer(
                missing_values=np.nan, strategy="mean"
            ).fit_transform(X[["VehListdays"]])

        return X

class YNanRemoveTransformer(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        self.y_cols = [
            "Vehicle_Trim",
            "Dealer_Listing_Price",
        ]
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X[X[self.y_cols].isna().sum(axis=1)==0]


class XT5CleanerTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.col = ["SellerIsPriv", "VehTransmission", "VehEngine"]
        return self

    def transform(self, X, y=None):
        for col in self.col:
            if col in X.columns:
                X.drop(columns=col, inplace=True)
        return X


class WK2CleanerTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.col = ["SellerIsPriv", "VehTransmission", "VehEngine"]
        return self

    def transform(self, X, y=None):
        for col in self.col:
            if col in X.columns:
                X.drop(columns=col, inplace=True)
        return X


class HistoryTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.history_lst = []
        for hist in X["VehHistory"]:
            if isinstance(hist, str):
                self.history_lst.extend(hist.split(", "))
        self.history_set = set(self.history_lst)
        return self

    def transform(self, X, y=None):
        df_hist = pd.DataFrame(
            data=np.zeros(
                shape=(X.shape[0], len(self.history_set)), dtype=np.float_
            ),
            columns=[f"history_{h}" for h in self.history_set],
            index=X.index,
        )

        for ind in X.index:
            hist = X.at[ind, 'VehHistory']
            for h in self.history_set:
                if h in hist:
                    df_hist.at[ind, f"history_{h}"] = 1
        X.drop(columns="VehHistory", inplace=True)

        return pd.concat([X, df_hist], axis=1)


class OHETransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        cats = ["SellerState", "VehYear", "VehPriceLabel", "Vehicle_Trim"]
        self.cats = [c for c in cats if c in X.columns]
        self.enc = OneHotEncoder(
            handle_unknown="ignore",
        )
        self.enc.fit(X[self.cats])
        return self

    def transform(self, X, y=None):
        df_ohe = pd.DataFrame(
            data=self.enc.transform(X[self.cats]).toarray(),
            index=X.index,
            columns=self.enc.get_feature_names_out(),
        )
        # X.drop(columns=self.cats, inplace=True)
        return pd.concat([X, df_ohe], axis=1)


class XT5_WK2SplitterTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.xt5_indices = X["VehModel"] == "XT5"
        self.wk2_indices = X["VehModel"] == "Grand Cherokee"
        return self

    def transform(self, X, y=None):
        return X[self.xt5_indices], X[self.wk2_indices]
