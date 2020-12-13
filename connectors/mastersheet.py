from __future__ import print_function
import pickle
import os.path
import urllib
import shutil
import tempfile
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']

# The ID and range of a sample spreadsheet.
EXPENSE_SHEET = '1_FsoV6f-jgPHPGCxVOVRB8OGxrRkfNEIX4zfV_gq5vI'
TOTAL_RANGE = 'Master!A:Q'
HEADER_RANGE = 'Master!A3:Q3'

def download():
    drive = drive_conn()

    SRC_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
    DST_MIMETYPE = 'text/csv'

    data = drive.files().export(fileId=EXPENSE_SHEET, mimeType=DST_MIMETYPE).execute()
    with open(os.path.join("parser", "mastersheet.csv"), 'wb') as f:
        f.write(data)

def drive_conn():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def insert(entries):
    service = sheet_conn()
    sheet = service.spreadsheets()
    
    headers = sheet.values().get(spreadsheetId=EXPENSE_SHEET,range=HEADER_RANGE).execute().get('values', [])[0]

    for header in headers:
        if header not in entries.columns.values:
            # print(header)
            entries[header] = ""
        
    entries = entries.reindex(columns = headers)         
    values = entries.values.tolist()
    # print(entries)
    
    body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=EXPENSE_SHEET, 
        range=TOTAL_RANGE,
        body=body,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        ).execute()

    print('{0} cells appended.'.format(result \
                                        .get('updates') \
                                        .get('updatedCells')))

def test():
    service = sheet_conn()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=EXPENSE_SHEET,
                                range=SAMPLE_RANGE_NAME).execute()

    headers = sheet.values().get(spreadsheetId=EXPENSE_SHEET,
                                range='Master!A3:Q3').execute()
    print(headers)

    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)


def sheet_conn():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)