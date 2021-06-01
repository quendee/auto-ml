import pandas as pd
from mlapp.helper import helper
import numpy as np
from mlapp.processer.__feature_eng import Engineer
import abc


class BaseNorm(Engineer):

    def __init__(self, columns, profile):
        super().__init__(profile)
        self.columns = list(set(columns))

    @abc.abstractmethod
    def fit(self, data: pd.DataFrame, save_pickle = "steps"):
        raise NotImplementedError
    
    @abc.abstractmethod
    def transform(self, data: pd.DataFrame, drop_columns = True):
        raise NotImplementedError

    def check_columns(self, data: pd.DataFrame):
        if not (set(self.columns).issubset(list(data.columns))):
            diffs = np.setdiff1d(self.columns, data.columns)
            raise KeyError(f"{diffs} not in data")
        else:
            self.columns = helper.get_numerics(data[self.columns])

    def store_mins(self, data: pd.DataFrame):
        self.mins = {}
        for col in self.columns:
            data[col].replace('None', np.nan, inplace = True)
            data[col] = data[col].astype(float)
            self.mins[col] = data[col].min()

        return

    def store_maxes(self, data: pd.DataFrame):
        self.maxes = {}
        for col in self.columns:
            data[col].replace('None', np.nan, inplace = True)
            data[col] = data[col].astype(float)
            self.maxes[col] = data[col].max()

        return

    def store_avgs(self, data: pd.DataFrame):
        self.avgs = {}
        for col in self.columns:
            data[col].replace('None', np.nan, inplace = True)
            data[col] = data[col].astype(float)
            self.avgs[col] = data[col].mean()

        return

    def store_stds(self, data: pd.DataFrame):
        self.stds = {}
        for col in self.columns:
            data[col].replace('None', np.nan, inplace = True)
            data[col] = data[col].astype(float)
            self.stds[col] = data[col].std()

        return

class BaseNas(Engineer):

    def __init__(self, profile, nas, columns, col_thresh = 0.5) -> None:
        super().__init__(profile)

        if col_thresh > 1:
            self.col_thresh = col_thresh/100
        else:
            self.col_thresh = col_thresh
            
        self.nas = nas
        self.columns = columns

    @abc.abstractmethod
    def fit(self, data: pd.DataFrame, save_pickle = "steps"):
        raise NotImplementedError
    
    @abc.abstractmethod
    def transform(self, data: pd.DataFrame, drop_columns = True):
        raise NotImplementedError
    
    def clean_nas(self, data):
        for na in self.nas:
            data.replace(na, np.NaN, inplace = True)
        
        return data
    
    def store_avgs(self, data: pd.DataFrame):
        self.avgs = {}
        for col in data.columns:
            data[col].replace('None', np.nan, inplace = True)
            data[col] = data[col].astype(float)
            self.avgs[col] = data[col].mean()

        return

    def store_modes(self, data: pd.DataFrame):
        self.modes = {}
        for col in data.columns:
            data[col].replace('None', np.nan, inplace = True)
            self.modes[col] = data[col].mode().iloc[0]

        return