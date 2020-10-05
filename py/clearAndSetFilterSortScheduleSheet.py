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
from pprint import pprint

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

    mysheetId = "1933349127"
    mysheetId = "473608957"

    #
    # -----------------------------------------------------------------------------

    #request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
    #values = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute().get('values', [])
    #resource = service.spreadsheets().values()

    requests = []
    requests.append( {
            'clearBasicFilter' : {
                'sheetId': mysheetId
            }
        }
    )

    requests.append( {
            "setBasicFilter": {
                "filter": {
                    "range": {    
                        "sheetId": mysheetId,
                        "startColumnIndex": 0,
                        "endColumnIndex": 10
                    },            
                }
            }
        }   
    )

    requests.append( {

            "sortRange": {
                    "range": {
                    "sheetId": mysheetId,
                    "startRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 10
                    },
                    "sortSpecs": [
                        {
                            "dimensionIndex": 4,
                            "sortOrder": "ASCENDING"
                        },
                        {
                            "dimensionIndex": 0,
                            "sortOrder": "ASCENDING"
                        }
                    ]
            }
        }
    )

    body = {
        'requests': requests
    }

    print("CLEAR sheetFilter.....")
    response = service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID,
                                                body=body).execute()
    print("SET BasiSheetFilter for Col A~J .....")
    pprint(response)
    #resource.append(spreadsheetId=SHEET_ID, range=RANGE_NAME,
    #                valueInputOption='USER_ENTERED', body=body).execute()



def main():
    process()


if __name__ == "__main__":
    main()