import pandas
import math
import urllib.request
from pprint import pprint


def get_norway():
    filename = "norway.xlsx"
    urllib.request.urlretrieve("https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/hovedtall-om-arbeidsmarkedet/_/attachment/download/b4c655bf-de5c-4714-bf30-9d4d979fa45b:7e53be0947a6afdab3df01a0523a574d3e174277/HL100_Antall_helt_ledige_historisk._November_2020.xlsx", filename)

    # TODO: Fix parsing

    df = pandas.read_excel(filename, "2. Andel av arbeidsstyrken Land")[5:]
    del df["Unnamed: 0"]
    del df["Unnamed: 14"]
    df.drop(df[df["Unnamed: 1"] < 2015].index, inplace=True)
    data = df.values.tolist()

    out = []
    for year_data in data:
        for month in [[year_data[0], 12 - it, value] for it, value in enumerate(year_data[1:][::-1]) if not math.isnan(value)]:
            out.append(month)

    return out
