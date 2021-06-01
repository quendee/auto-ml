import pandas as pd
from mlapp.helper import helper
import numpy as np
from mlapp.processer.__feature_eng import Engineer


class ComboEncode(Engineer):


    def __init__(self, aak, ask, region) -> None:
        super().__init__(aak, ask, region)

    def fit(self, label_col = None, mapping = {}, save_pickle = "processing-steps-auto-ml"):
        self.label_col = label_col
        self.mapping = mapping

        self.save_obj(self, 'combo_encoding.pickle', save_pickle)

        return
    
    def transform(self, data: pd.DataFrame, drop_columns = True):

        for key, val in self.mapping.items():
            mask = data[self.label_col] == key
            temp = (np.multiply(np.asarray(mask.astype(int)), np.asarray(data[val].astype(int)))).sum(axis=1)
            data[key] = temp
        
        if drop_columns:
            data.drop(self.brawl_names, axis = 1, inplace = True)

        return data

    def clear(self):
        return self.clear_base("brawlerencoding.pickle", self.profile)

        
if __name__ == "__main__":

    processer = pd.read_csv(r"C:\Users\migue\Downloads\iris.csv")
    be = ComboEncode("", "")
    be.fit(label_col = 'Species', mapping = {'Iris-setosa':'SepalLengthCm'})

    data = be.transform(processer)
    data