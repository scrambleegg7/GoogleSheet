#!/usr/bin/env python
# coding:utf-8
from apiclient import discovery
import oauth2client
import httplib2
import argparse
import csv
import sys
from oauth2client import file, client, tools
from httplib2 import Http
from pprint import pprint


 
#SPREADSHEET_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
RANGE_NAME = 'A1'
MAJOR_DIMENSION = 'ROWS'
 
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIAL_FILE = "./credential.json"
APPLICATION_NAME = 'CSV Appender'

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

store = file.Storage('credential.json')
creds = store.get()

if not creds or creds.invalid:


    flow = client.flow_from_clientsecrets('client_secret_sheets.json', SCOPES)
    creds = tools.run_flow(flow, store)

    #flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    #flow.user_agent = APPLICATION_NAME
    #args = '--auth_host_name localhost --logging_level INFO --noauth_local_webserver'
    #flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args(args.split())
    #credentials = oauth2client.tools.run_flow(flow, store, flags)

#service = discovery.build('sheets', 'v4', credentials=credentials)
service = build('sheets', 'v4', http=creds.authorize(Http()))

#http = credentials.authorize(httplib2.Http())
#discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
#service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
#resource = service.spreadsheets().values()
 
spreadsheet_id = '1eUQvTp5VX7IGAjeJ4b3IUPfhrFdbwPGLd6TtrXbdibA'  # TODO: Update placeholder value.

# The ranges to retrieve from the spreadsheet.
ranges = "A1:A3"  # TODO: Update placeholder value.

# True if grid data should be returned.
# This parameter is ignored if a field mask was set in the request.
include_grid_data = False  # TODO: Update placeholder value.

request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response = request.execute()




pprint( response )