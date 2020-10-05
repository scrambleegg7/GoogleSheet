import numpy as np
import pandas as pd
import os

import hashlib
import json
import decimal

import csv
import boto3
#from decimal import *

from Exporer import Exporter
import httplib2
import oauth2client
import httplib2
import argparse
import apiclient

import sys
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

def exportToDataFrame():

    exporter = Exporter()

    table_name = "schedular"
    print("-" * 30)
    print("dynamo Table name : ", table_name)
    rows, _ = exporter.get_rows(table_name) 

    df = pd.io.json.json_normalize(rows)
    columns_ = df.columns
    dot_splitter = lambda x: x.split('.')[0] 

    columns_ = list( map( dot_splitter, columns_ )   )
    df.columns = columns_

    print(df.columns.tolist())
    
    newcolname = ["name","hospital","medicine","nextDate","total_amount","expiry","czDate"]
    df_ = df[newcolname].copy()
    df_["mark"] = ""
    df_["mark2"] = ""
    df_["standard"] = ""
    
    newcolname = ["name","mark","hospital","medicine","nextDate","total_amount","mark2","expiry","standard","czDate"]
    df_new = df_.copy()
    df_new = df_new[newcolname]
    
    print(df_new.shape)
    print(df_new.loc[0,:])
    return df_new


def insertDataSheet(df):

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    APPLICATION_NAME = 'read sample'  # 
    SHEET_ID = '17iCNpYNaM4Lt88LtrBfJKCcwfLSdb8wLkFz1kicRk5o'
    RANGE = 'A:J'  # 
    # -----------------------------------------------------------------------------
    # read credential file
    store = oauth2client.file.Storage("./credential.json")  # is there any credential file ?
    credentials = store.get()

    # allow ?
    if not credentials or credentials.invalid:
        flow = oauth2client.client.flow_from_clientsecrets('client_secret.json', SCOPES)
        flow.user_agent = APPLICATION_NAME

        # initialize
        import argparse
        args = '--auth_host_name localhost --logging_level INFO --noauth_local_webserver'
        flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args(args.split())

        credentials = oauth2client.tools.run_flow(flow, store, flags)  # 

    # access to use credentials
    http = credentials.authorize(httplib2.Http())

    # read sheets

    service = apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')

    #request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)

    values = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute().get('values', [])

    resource = service.spreadsheets().values()


    print("-" * 40)
    print(" call dynamodb ....")
    RANGE_NAME = "A2" 
#    df = exportToDataFrame()
    df = df.fillna("")

    print("total record(s) of dynamodb.." , len(df)  )

    if df.shape[0] > 0:
        data = df.values.tolist()

        body = {
            "range": RANGE_NAME ,
            "majorDimension": "ROWS",
            "values": data
        }

        resource.append(spreadsheetId=SHEET_ID, range=RANGE_NAME,
                        valueInputOption='USER_ENTERED', body=body).execute()

    else:
        print("Sorry, but data is ZERO.")





def main():

    df = exportToDataFrame()
    insertDataSheet(df)



if __name__ == "__main__":
    main()