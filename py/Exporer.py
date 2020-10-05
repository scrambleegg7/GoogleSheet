import boto3
import numpy as np  
import pandas as pd  

class Exporter: 
    def __init__(self, row_limit=10000, profile_name=None): 

        self.row_limit = row_limit
        #if profile_name != '': 
        #    boto3.setup_default_session(profile_name=profile_name) 
        self.client = boto3.client('dynamodb',endpoint_url='http://localhost:8000') 
        #self.resource = boto3.resource('dynamodb') 
        self.resource = boto3.resource('dynamodb',endpoint_url='http://localhost:8000')
  
    def get_rows(self, table_name, rows=[], last_evaluated_key=None): 
        response = self.client.scan( 
            TableName=table_name,
            Limit=self.row_limit,
            **({"ExclusiveStartKey": last_evaluated_key} 
            if last_evaluated_key else {}) 
        ) 

        #table = self.resource.Table('schedular')
        #print("total table count for schedular", table.item_count)

        #jd = json.dumps

        rows = rows + response['Items'] 
        # for testing recursion on small tables (< 10000 (default) rows) 
        # if 'LastEvaluatedKey' in response and len(rows) < 100000000000: 
        if 'LastEvaluatedKey' in response and len(rows) < self.row_limit: 
            return rows, response['LastEvaluatedKey'] 
        else: 
            return rows, None 
