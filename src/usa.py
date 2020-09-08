import pandas
import requests
import json

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['LNS14000000'], "startyear":"2015", "endyear":"2020"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

for series in json_data['Results']['series']:
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']

        print(f"{year} {period} {value}")
    # output = open(seriesId + '.txt','w')
    # output.write (x.get_string())
    # output.close()

# a = pandas.read_excel("series.xlsx").values
# for i in a:
#     try:
#         int(i[0])
#         print(list(i))
#     except:
#         pass
