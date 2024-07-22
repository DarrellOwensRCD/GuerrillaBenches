'''Makes a geojson or updates an existing geojson of benches with locations
from the online sheet
'''
import os
import gspread
import json
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
# Sheets and Google API are scope of use
scope = ['https://www.googleapis.com/auth/spreadsheets']
# Create the flow instance using the credentials JSON file and scopes
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=scope)# Authorize the client
credentials = flow.run_local_server()
# Perform the OAuth 2.0 authorization flow
client = gspread.authorize(credentials)
# Open 'Data' sheet
spreadsheet_id = '1nNP3-6OXPYoewe4zrMSFw-_h02gnCtSCZb1t-Md9zhQ'
spreadsheet = client.open_by_key(spreadsheet_id)
worksheet = spreadsheet.worksheet('Data')
values = worksheet.get_all_values()
# Open Map File and Append new polygons, attributes or create a file if it doesn't exist
benches_mapped = []
if os.path.exists('benches.geojson'):
    benches = json.load(open('benches.geojson'))
    # Knows what benches are already mapped for when we checked for updates on existing benches
    for bench in benches['features']:
        benches_mapped.append(bench['properties']['id'])
else:
    benches = json.loads("""{"type":"FeatureCollection","features":[]}""")
# Iterate Sheet and Update Benches or 
for i,row in enumerate(values):
    #print(row)
    if i != 0: # Skip header row
        if row[1] == '':
            # No address indicates its unfilled; benches have pre-assigned ids so cant be used as terminus
            break
        if row[0] in benches_mapped and row[16] == "TRUE":
            print(row[0])
            for i, bench in enumerate(benches['features']):
                if row[0] == bench['properties']['id']:
                    print("FOUND")
                    del benches['features'][i]
                    benches_mapped.remove(row[0])
        if row[0] not in benches_mapped:
            print(row)
            coordinates = row[7].split(",")
            print(coordinates)
            x = {"type": "Feature",
                "properties" :
                {"id": row[0],
                "address": row[2],
                "stopid" : row[1],
                "install_date" : row[3],
                "removed_date" : row[5],
                "city" : row[6],
                "lines" : row[8].split(","),
                "ridership" : row[9],
                "dirs" : row[10].split(","),
                "bench_length" : row[11],
                "adopted" : row[18],
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(coordinates[1]), float(coordinates[0])]
                }
            }
            benches['features'].append(x)
with open('benches.geojson', 'w') as f:
    json.dump(benches,f)
    f.close()

                
