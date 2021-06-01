from brawler.fetcher.sql_fetcher import DataBase
import pandas as pd
from brawler.configs import db_config
from brawler.configs import variables
from brawler.helper import helper
import numpy as np
from brawler.processer.__base import BaseNorm

class Normalize(BaseNorm):
    def __init__(self, columns, profile):
        super().__init__(columns, profile)

    def fit(self, data: pd.DataFrame, save_pickle = "processing-storage"):
        self.check_columns(data)
        self.store_mins(data)
        self.store_maxes(data)
        
        self.save_obj(self, "norm.pickle", save_pickle, self.profile)

        return
    
    def transform(self, data: pd.DataFrame, drop_columns = True):
        for col in self.columns:
            data[col].replace('None', np.nan, inplace = True)
            data[col] = data[col].astype(float, errors = 'ignore')
            data[col] = (data[col] - self.mins[col]) / (self.maxes[col] - self.mins[col])

        return data

    def clear(self):
        return self.clear_base("norm.pickle", self.profile)

if __name__ == "__main__":

    db = DataBase(db_config.host, db_config.user, db_config.passwd, db_config.db)
    be = Normalize(['t1_total_trophies_0', 't2_total_trophies_0', 't2_total_trophies_1', 't2_tag_2'])
    processer = be.get_data(connection=db, table='brawlers')
    be.fit(processer)

    data = be.transform(processer)
    be.clear()
    data