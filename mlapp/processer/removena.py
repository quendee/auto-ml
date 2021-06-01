import pandas as pd
from brawler.configs import db_config
from brawler.configs import variables
from brawler.helper import helper
import numpy as np
from brawler.processer.__base import BaseNas
from brawler.fetcher.sql_fetcher import DataBase


class RemoveNas(BaseNas):

    def __init__(self, profile, nas, columns, col_thresh = 0.5) -> None:
        super().__init__(profile, nas, columns, col_thresh=col_thresh)


    def fit(self, data: pd.DataFrame, save_pickle = "processing-storage"):

        data = data[self.columns]
        data = self.clean_nas(data)
        cols_na = data.isna().sum() / data.shape[0]
        self.to_remove = list(cols_na[cols_na > self.col_thresh].index)
        self.save_obj(self, 'removenas.pickle', save_pickle, self.profile)

        return

    def transform(self, data: pd.DataFrame, drop_columns = True):
        data.drop(self.to_remove, axis = 1, inplace = True)
        data = self.clean_nas(data)
        return data.dropna(subset=self.to_remove, axis = 1, inplace = True)

    def clear(self):
        return self.clear_base("removenas.pickle", self.profile)

if __name__ == "__main__":

    db = DataBase(db_config.host, db_config.user, db_config.passwd, db_config.db)
    be = RemoveNas(['None', 'nan'], ['game_map', 'game_mode', 'battle_mode'])
    processer = be.get_data(connection=db, table='brawlers')
    be.fit(processer)

    data = be.transform(processer)
    data