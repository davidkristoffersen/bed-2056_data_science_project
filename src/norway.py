import pandas
import math
import urllib.request
from pprint import pprint

filename = "norway.xlsx"

urllib.request.urlretrieve("https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/hovedtall-om-arbeidsmarkedet/_/attachment/download/ab00f9e5-efbf-458e-a01f-dae7196aa805:21959eedc8a1d065601548b4c8dd0a7d348e816c/HL100_Antall_helt_ledige_historisk._August_2020.xlsx", filename)

df = pandas.read_excel(filename, "2. Andel av arbeidsstyrken Land")[5:]
del df["Unnamed: 0"]
del df["Unnamed: 14"]
df.drop(df[df["Unnamed: 1"] < 2015].index, inplace=True)
data = df.values.tolist()

out = []
for year_data in data:
    for month in [[year_data[0], 11 - it, value] for it, value in enumerate(year_data[1:][::-1]) if not math.isnan(value)]:
        out.append(month)

pprint(out)
