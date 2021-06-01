import pandas as pd
from brawler.configs import db_config
from brawler.configs import variables
from brawler.helper import helper
import numpy as np
from brawler.processer.__base import BaseNas
from brawler.fetcher.sql_fetcher import DataBase


class ReplaceNas(BaseNas):

    def __init__(self, profile, nas, columns, col_thresh = 0.5) -> None:
        super().__init__(profile, nas, columns, col_thresh=col_thresh)


    def fit(self, data: pd.DataFrame, save_pickle = "processing-storage"):
        data = data[self.columns]
        data = self.clean_nas(data)
        cols_na = data.isna().sum() / data.shape[0]
        self.to_remove = list(cols_na[cols_na > self.col_thresh].index)
        data.drop(self.to_remove, axis = 1, inplace = True)

        numerics = helper.get_numerics(data)
        self.store_avgs(data[numerics])
        self.store_modes(data.drop(numerics, axis = 1))

        self.save_obj(self, 'replacenas.pickle', save_pickle, self.profile)

        return

    def transform(self, data: pd.DataFrame, drop_columns = True, teams = True):

        data.drop(self.to_remove, axis = 1, inplace = True)
        data = self.clean_nas(data)
        full_stores = {**self.avgs, **self.modes}
        for key, value in full_stores.items():
            cols = [col for col in data.columns if key[3:-2] in col]
            numerics = helper.get_numerics(data[cols])
            if len(numerics) > 2:
                data[cols] = data[cols].astype(float)
                means = data[cols].mean(axis = 1)
                for col in cols:
                    data[col].fillna(value=means, inplace = True)
            else:
                if isinstance(value, float):
                    value = round(value,0)
                data[key] = data[key].fillna(value)

        return data

    def clear(self):
        return self.clear_base("replacenas.pickle", self.profile)

if __name__ == "__main__":

    db = DataBase(db_config.host, db_config.user, db_config.passwd, db_config.db)
    be = ReplaceNas(['None', 'nan'], columns=['t1_total_trophies_0', 't2_total_trophies_0', 't2_total_trophies_1', 't2_tag_2'])
    processer = be.get_data(connection=db, table='brawlers')
    be.fit(processer)

    data = be.transform(processer)
    be.clear()
    data