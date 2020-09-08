import pandas
import urllib.request

filename = "norway.xlsx"

urllib.request.urlretrieve("https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/hovedtall-om-arbeidsmarkedet/_/attachment/download/ab00f9e5-efbf-458e-a01f-dae7196aa805:21959eedc8a1d065601548b4c8dd0a7d348e816c/HL100_Antall_helt_ledige_historisk._August_2020.xlsx", filename)

data = pandas.read_excel(filename, "2. Andel av arbeidsstyrken Land")
print(data)
