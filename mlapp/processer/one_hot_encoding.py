import pandas as pd
from brawler.configs import db_config
from brawler.configs import variables
from brawler.helper import helper
import numpy as np
from brawler.processer.__feature_eng import BrawlerEngineer
from brawler.fetcher.sql_fetcher import DataBase
from brawler.sklearn.preprocessing import OneHotEncoder
import re


class OneHotEncode(OneHotEncoder, BrawlerEngineer):
    def __init__(self, columns, profile):

        self.columns = columns
        super().__init__(handle_unknown = 'ignore')
        self.profile = profile

    def fit(self, data: pd.DataFrame, save_pickle = "processing-storage"):
        
        self.fit_main(data[self.columns])
        
        self.cats = []
        for cat in self.categories_:
            self.cats = self.cats + list(cat)

        self.cats = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in self.cats]

        self.save_obj(self, 'onehotencoding.pickle', save_pickle, self.profile)

        return
    
    def transform(self, data: pd.DataFrame, drop_columns = True):
        trans = self.transform_main(data[self.columns])
        trans = pd.DataFrame(trans.toarray(), columns = self.cats)

        data.drop(self.columns, axis = 1, inplace = True)
        data = data.merge(trans, right_index = True, left_index = True)
        return data

    def clear(self):
        return self.self.clear_base("onehotencoding.pickle", self.profile)

        
if __name__ == "__main__":

    db = DataBase(db_config.host, db_config.user, db_config.passwd, db_config.db)
    be = OneHotEncode(['game_map', 'game_mode', 'battle_mode'], profile='miguel')
    processer = be.get_data(connection=db, table='brawlers')
    be.fit(processer)
    be.transform(processer)
    # with open('brawl_fit.pickle', 'rb') as handle:   
    #     be2 = pickle.load(handle)

    # data = be2.transform(processer)
    # data