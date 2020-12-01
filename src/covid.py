import pandas
import requests


num_to_month = {
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


def add_row(row, data):
    """
        Parses the row and adds the date and value to the given data set.
    """

    row = row.split(",")
    data[0].append(f"{row[1]} {num_to_month[int(row[2])]} {row[3]}")
    data[1].append(int(row[4]))


def get_covid():
    """
        Returns the data on Covid cases in Norway and USA.
        The data is fetched from the European Centre for Disease Prevention and Control.
    """

    # Download the data
    res = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/data.csv")

    usa = [], []
    norway = [], []
    # Goes through the data and adds the values for Norway and USA
    for line in reversed(res.text.split("\n")):
        if "USA" in line:
            add_row(line, usa)
        elif "Norway" in line:
            add_row(line, norway)

    return norway, usa

