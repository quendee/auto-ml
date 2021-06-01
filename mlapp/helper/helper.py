from random import randint
import pickle
import boto3
import numpy as np


def get_numerics(table):
    cols = list(table.columns)
    for col in cols:
        table[col].replace('None', np.nan, inplace = True)
        table[col] = table[col].astype(float, errors='ignore')
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    table = table.select_dtypes(include=numerics)

    cols = list(table.columns)
    return cols

def check_inputs(**kwargs):
    check = []
    for key, value in kwargs.items():
        if (value is None) or (value == ''):
            check.append(True)
        else:
            check.append(False)
    return check

def count_duplicates(seq): 
    seq = [s for s in seq if s != 'None']
    return len(seq) - len(set(seq))

def create_pop(message, stat_type, title):

    return  f"""
            Swal.fire({{
            icon: "{stat_type}",
            title: "{title}",
            text: "{message}"
            }})
            """

def create_bucket(bucket_name, sk, ak, region = "us-east-2"):

    s3_client = boto3.client('s3', aws_secret_access_key = sk, aws_access_key_id = ak, region_name = region)
    location = {'LocationConstraint': region}
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)


    return True

def list_buckets(sk, ak):
    s3_client = boto3.client('s3', aws_secret_access_key = sk, aws_access_key_id = ak)
    response = s3_client.list_buckets()

    # Output the bucket names
    buckets = [bucket for bucket in response['Buckets']]
    return buckets

def update_options(cols, iall = True):

        # cols = list(table.columns)
        # for col in cols:
        #     table[col].replace('None', np.nan, inplace = True)
        #     table[col] = table[col].astype(float, errors='ignore')
        # numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        # table = table.select_dtypes(include=numerics)

        final = [{'label': d, 'value': d} for d in cols]
        if iall: 
            final.insert(0, {'label': 'ALL', 'value': 'ALL'})
        return final