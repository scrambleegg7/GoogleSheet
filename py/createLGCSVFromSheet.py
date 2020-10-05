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
import platform

from helper import readSheetID
from helper import getAuth
from helper import getService


def write_csv(fd, rows, encoding='utf-8', dialect='excel'):
    csvfile = csv.writer(fd, dialect=dialect)
    for r in rows:
        #csvfile.writerow([c.decode('unicode-escape') for c in r])
        csvfile.writerow(r)

def process():

    filename = "./sheetid.txt"
    SHEET_ID = readSheetID(filename)

    http = getAuth()

    service = getService(http)

    RANGE = "A:J"
    service = apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
    #request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
    doc = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
    values = doc.get('values', [])
    resource = service.spreadsheets().values()

    v_length = len(values)
    # utilize values

    print("-" * 40)
    print("[createLGCSVFromSheet] total length of data...",len( values ))
    print("[createLGCSVFromSheet] last data ....") 
    print( values[ v_length - 1 ] )

    print("[createLGCSVFromSheet] Running platform:", platform.system() )
    if platform.system() == 'Windows':
        data_dir = "L:/ipython"
        #data_dir = "/Users/miyuk_000/Documents/myData/Miyuki"
    else:
        data_dir = "/Volumes/myShare/ipython"

    integrate_csvfile = os.path.join(data_dir, "longterm2.csv")

    with open(integrate_csvfile, 'w') as fd:
        write_csv(fd, values)

    print("[createLGCSVFromSheet] done.")
    print("[createLGCSVFromSheet] generated file -->", integrate_csvfile)

    include_grid_data = False
    request = service.spreadsheets().get(spreadsheetId=SHEET_ID, ranges=RANGE, includeGridData=include_grid_data)
    response = request.execute()
    sheets = response["sheets"]
    for s in sheets:
        sheet_id = s["properties"]["sheetId"]  
        print("[createLGCSVFromSheet] targeet shhetid --> ",sheet_id)

    



def main():
    process()



if __name__ == "__main__":
    main()