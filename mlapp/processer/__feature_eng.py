import pandas as pd
import boto3
import abc
import pickle

from mlapp.helper import helper


class Engineer(abc.ABC):
    def __init__(self, aak, ask, region) -> None:
        self.aak = aak
        self.ask = ask
        self.region = region
        
    @abc.abstractmethod
    def fit(self, data: pd.DataFrame, save_pickle = "steps"):
        raise NotImplementedError
    
    @abc.abstractmethod
    def transform(self, data: pd.DataFrame, drop_columns = True):
        raise NotImplementedError

    def save_obj(self, obj, name, save_pickle = "steps"):

        if save_pickle not in helper.list_buckets(self.ask, self.aak):
            helper.create_bucket(save_pickle, self.ask, self.aak, self.region)
        session = boto3.Session(aws_access_key_id = self.aak, aws_secret_access_key = self.ask)

        s3_resource = session.resource('s3')

        bucket = save_pickle
        key = name
        pickle_byte_obj = pickle.dumps(obj) 
        s3_resource.Object(bucket,key).put(Body=pickle_byte_obj)
