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

from helper import getAuth
from helper import getService
from helper import readSheetID

import platform

def process():


    filename = "./sheetid.txt"
    SHEET_ID = readSheetID(filename)
    RANGE = "A:J"
    http = getAuth()
    service = getService(http)
    values = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute().get('values', [])
    resource = service.spreadsheets().values()


    v_length = len(values)
    # utilize values
    print(len( values ))

    print("-" * 40)
    print(" last data ....") 
    print( values[ v_length - 1 ] )


    print("Running platform:", platform.system() )
    if platform.system() == 'Windows':
        data_dir = "L:/ipython"
        #data_dir = "/Users/miyuk_000/Documents/myData/Miyuki"
    else:
        data_dir = "/Volumes/myShare/ipython"

    integrate_csvfile = os.path.join(data_dir, "integrate2.csv")
    RANGE_NAME = "A" + str(v_length)

    df = pd.read_csv(integrate_csvfile, encoding="Shift_JISx0213")
    df = df.fillna("")

    print("total record(s) of integrate2.csv" , len(df)  )

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

    process()

if __name__ == "__main__":
    main()