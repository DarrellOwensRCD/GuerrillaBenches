'''Makes a geojson or updates an existing geojson of benches with locations
from the online sheet
'''
import gspread
import json
from google_auth_oauthlib.flow import InstalledAppFlow
credentials_file = 'credentials.json'
# Sheets and Google API are scope of use
scope = ['https://www.googleapis.com/auth/spreadsheets']
# Create the flow instance using the credentials JSON file and scopes
flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes=scope)# Authorize the client
credentials = flow.run_local_server()
# Perform the OAuth 2.0 authorization flow
client = gspread.authorize(credentials)
# Open specific spreadsheet
spreadsheet_id = '1nNP3-6OXPYoewe4zrMSFw-_h02gnCtSCZb1t-Md9zhQ'
spreadsheet = client.open_by_key(spreadsheet_id)
worksheet = spreadsheet.worksheet('Data')
values = worksheet.get_all_values()
for i,row in enumerate(values):
    if i == 15:
        break
    print(row)
