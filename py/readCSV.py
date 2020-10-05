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


data_dir = "/Volumes/myShare/ipython"
integrate_csvfile = os.path.join(data_dir, "integrate2.csv")

#RANGE_NAME = "A" + str(v_length)


df = pd.read_csv(integrate_csvfile, encoding="Shift_JISx0213")

df = df.fillna("")

#print(df.head())

data = df.values.tolist()

print(data)
