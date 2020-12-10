import math
import json
import pandas
import requests
import urllib.request


idx_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def get_norway_population():
    """
        Gets the current population of Norway from https://restcountries.eu/
    """

    response = requests.get("https://restcountries.eu/rest/v2/alpha/nor")
    return json.loads(response.text)["population"]


def get_norway():
    """
        Reads the unemployment data from nav, and parses it into a better format.
    """

    filename = "norway.xlsx"
    # Download the data and save it as norway.xlsx
    urllib.request.urlretrieve("https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/hovedtall-om-arbeidsmarkedet/_/attachment/download/b4c655bf-de5c-4714-bf30-9d4d979fa45b:7e53be0947a6afdab3df01a0523a574d3e174277/HL100_Antall_helt_ledige_historisk._November_2020.xlsx", filename)

    # Read the correct page of the file into a pandas dataset
    df = pandas.read_excel(filename, "2. Andel av arbeidsstyrken Land")[5:]

    # Delete some unused columns
    del df["Unnamed: 0"]
    del df["Unnamed: 14"]

    # Delete data before 2015
    df.drop(df[df["Unnamed: 1"] < 2015].index, inplace=True)

    x, y = [], []
    # Go through the data and add the date and value
    # The list is reversed because we want to go from 2015 -> 2020
    for year, *values in reversed(df.values):
        for month_idx, value in enumerate(values):
            if not math.isnan(value):
                x.append(f"{idx_to_month[month_idx + 1]} {year}")
                y.append(value)

    return x, y

