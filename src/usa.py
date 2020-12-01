import requests
import json
from pprint import pprint

def get_usa():
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['LNS14000000'], "startyear": "2015", "endyear": "2020"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    out = []
    for series in json_data['Results']['series']:
        for item in series['data']:
            out.append([int(item['year']), int(item['period'][1:]), float(item['value'])])

    return out

