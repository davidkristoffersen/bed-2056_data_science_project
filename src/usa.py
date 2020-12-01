import json
import requests


def get_usa():
    """
        Reads the unemployment data from U.S. Bureau of Labour Statistics, and parses it into a better format.
    """

    # Get the data from U.S. Bureau of Labour Statistics
    response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/',
                             json={"seriesid": ['LNS14000000'], "startyear": "2015", "endyear": "2020"},
                             headers={'Content-type': 'application/json'})

    # Parse the result into a json object
    json_data = json.loads(response.text)

    x, y = [], []
    # Go through the data and add the date and value
    # The list is reversed because we want to go from 2015 -> 2020
    for item in reversed(json_data['Results']['series'][0]['data']):
        x.append(f"{item['periodName'][:3]} {item['year']}")
        y.append(float(item['value']))

    return x, y

