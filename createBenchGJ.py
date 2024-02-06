'''Makes a geojson or updates an existing geojson of benches with locations
from the online sheet
'''
import os
import gspread
import json
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
    if i != 0: # Skip header row
        if row[1] == '':
            # No address indicates its unfilled; benches have pre-assigned ids so cant be used as terminus
            break
            if row[0] in benches_mapped and row[15] == "TRUE" or row[0] not in benches_mapped:
                if row[0] in benches_mapped and row[15] == "TRUE":
                # Erase outdated data and update shapefile
                for bench in benches['features']:
                    if bench['properties']['id'] == row[0]:
                        del bench
                        '''update to sheets not working:
                        cell = 'P' + str(i + 1)
                        worksheet.update(cell, "")
                        print(f"Bench {i - 1} Updated")'''
                        coordinates = row[4].split(",")
                        x = {"type": "Feature",
                        "properties" :
                        {"id": row[0],
                        "address": row[1],
                        "stopid" : row[2],
                        "city": row[3],
                        "lines": row[5],
                        "dirs": row[6],
                        "length": row[7],
                        "service_date": row[9],
                        "status": row[10]
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

                
