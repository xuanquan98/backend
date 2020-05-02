from __future__ import print_function
#googleapiclient.discovery
from apiclient.discovery  import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.contrib import gce
from apiclient.http import MediaFileUpload
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import os
import pathlib
from pathlib import Path
import io
import glob
import itertools
import shutil
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import (
	LineChart,
	Reference,
	Series
	)

import random
import time
from time import sleep
import datetime
import csv


CLIENT_SECRET = "client_secret.json"

FILE_MASTERLIST = 'demo.xlsx'
FILE_TEMPLATE ='Input/Contacts_Template.xlsx'
OUTPUT_DIRECTORY = 'Output/'
EXCLUDE_LIST = []
INCLUDE_LIST = ['Calista Rosales', 'Bianca Cardenas', 'Colette Black']

now = datetime.datetime.now()
QUARTER = "2019Q2"
MONTH = "May 2019"
VERSION = str(now.month).zfill(2) + str(now.day).zfill(2)

df = pd.read_excel(FILE_MASTERLIST,"CONTACTS_FINAL")


# --------------------------------
# GDrive API: GDrive Authorization
# --------------------------------

SCOPES='https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
	creds = tools.run_flow(flow, store)
SERVICE = build('drive', 'v3', http=creds.authorize(Http()))
SS_SERVICE = build('sheets', 'v4', http=creds.authorize(Http()))


PARENT_FOLDER = '1w3PZ3bGL1FtjEESX6Igu3DhcEiR1M-7m'


# ------------------------------------
# GDrive API: Check if Filename exists
# ------------------------------------
def fileInGDrive(filename):
	results = SERVICE.files().list(q="mimeType='application/vnd.google-apps.spreadsheet' and name='"+filename+"' and trashed = false and parents in '"+PARENT_FOLDER+"'",fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])
	if items:
		return True
	else:
		return False

# ------------------------------------
# GDrive API: Check if Folder exists
# ------------------------------------
def folderInGDrive():
	folderName = str(now.date())
	results = SERVICE.files().list(q="mimeType='application/vnd.google-apps.folder' and name='"+folderName+"' and trashed = false and parents in '"+PARENT_FOLDER+"'",fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])
	if items:
		return items[0]["id"]
	else:
		return createGDriveFolder(folderName,PARENT_FOLDER)


# ---------------------------------------
# GDrive API: Upload files to Google Drive
# ---------------------------------------
def writeToGDrive(filename):
	source = './file/' + filename
	folder_id = folderInGDrive()
	file_metadata = {'name': filename,'parents': [folder_id],
					 'mimeType': 'application/pdf'}
	media = MediaFileUpload(source,
							mimetype='application/pdf')

	if fileInGDrive(filename) is False:
		file = SERVICE.files().create(body=file_metadata,
									  media_body=media,
									  fields='id').execute()
		print('Upload file success!')
		print('File ID:', file.get('id'))
		return file.get('id')

	else:
		print('File already exists as', filename)


# ---------------------------------------
# GDrive API: Create New Folder
# ---------------------------------------
def createGDriveFolder(filename,parent):
	file_metadata = {'name': filename,'parents': [parent],
					 'mimeType': "application/vnd.google-apps.folder"}

	folder = SERVICE.files().create(body=file_metadata,
									fields='id').execute()
	print('Create folder success')
	print('FolderID:', folder.get('id'))
	return folder.get('id')



def main():
	#generateNewFolders(getSalesRep())
	#(getSalesRep())
	print("------")
	writeToGDrive("Hr_Phuong.pdf")

if __name__ == '__main__':
	main()
