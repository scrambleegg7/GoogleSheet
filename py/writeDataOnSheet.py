import httplib2
import os

import oauth2client
import httplib2
import argparse
import apiclient

import sys
import csv
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd

import argparse
from pprint import pprint

def readSheetID(filename):

    df = pd.read_csv(filename,header=None)
    return df.iloc[0,0]

def getAuth():

    #
    # -----------------------------------------------------------------------------
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    APPLICATION_NAME = 'read sample'  # 

    # -----------------------------------------------------------------------------


    # read credential file
    store = oauth2client.file.Storage("./credential.json")  # is there any credential file ?
    credentials = store.get()

    # allow ?
    if not credentials or credentials.invalid:
        flow = oauth2client.client.flow_from_clientsecrets('client_secret.json', SCOPES)
        flow.user_agent = APPLICATION_NAME

        # initialize
        args = '--auth_host_name localhost --logging_level INFO --noauth_local_webserver'
        flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args(args.split())

        credentials = oauth2client.tools.run_flow(flow, store, flags)  # 

    # access to use credentials
    http = credentials.authorize(httplib2.Http())
    return http


def readCSVData():

    fdir = "/Volumes/ReceptyN/TEXT/result"

    file1 = "dailystockmove.csv"
    file2 = "dailyExclude.csv"
    file3 = "dailyOnly.csv"
    file4 = "dailyTablets.csv"


    filename1 = os.path.join(fdir,file1)
    df = pd.read_csv(filename1, encoding="Shift_JISx0213")
    df = df.fillna("")

    return df

def main():

    filename = "sheetid.txt"
    SHEET_ID = readSheetID(filename)
    print("-" * 30)
    print("Target Sheet ID.",SHEET_ID)

    http = getAuth()

    # read sheets
    RANGE = 'A:J'  # 
    service = apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
    #values = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute().get('values', [])
    #resource = service.spreadsheets().values()

    ranges = []
    include_grid_data = False
    request = service.spreadsheets().get(spreadsheetId=SHEET_ID, ranges=ranges, includeGridData=include_grid_data)
    response = request.execute()
    pprint(response)

    requests = []
    data_sheets_id = []
    sheets = response["sheets"]
    for s in sheets:
        sheet_id = s["properties"]["sheetId"]  
        if sheet_id != 0:
            data_sheets_id.append(sheet_id)

            requests.append( 
                {
                    "deleteSheet": {
                    "sheetId": sheet_id
                    }
                }
            )
            
            print("delete sheet. ",sheet_id)


    body = {
        'requests': requests
    }

    print("DELETE total sheets.....", len(data_sheets_id))
    response = service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID,
                                                body=body).execute()
    pprint(response)




if __name__ == "__main__":
    main()