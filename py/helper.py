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

def getService(http):

    service = apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
    return service