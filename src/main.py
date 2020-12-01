import json
import requests
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from usa import get_usa
from norway import get_norway


fg = "#ebf0f2"

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

layout = go.Layout(paper_bgcolor="rgb(0,0,0,0)",
                   plot_bgcolor="rgb(0,0,0,0)",
                   font_color=fg)


def _plot_unemployment(fig, data, name):
    x, y = [], []
    for row in reversed(data):
        x.append(f"{num_to_month[row[1]]} {row[0]}")
        y.append(row[2])

    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=name))


def plot_unemployment():
    fig = go.Figure(layout=layout)
    _plot_unemployment(fig, get_norway(), "Norway")
    _plot_unemployment(fig, get_usa(), "USA")
    fig.update_xaxes(gridcolor="#a9a9a9")
    fig.update_yaxes(gridcolor="#a9a9a9")
    fig.update_layout(title="Unemployment rate in Norway and USA", xaxis_title="Month", yaxis_title="Rate")
    fig.write_html("plots/unemployment.html")


def plot_covid():
    res = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/data.csv")

    x1, y1 = [], []
    x2, y2 = [], []
    for line in reversed(res.text.split("\n")):
        if "Norway" in line:
            row = line.split(",")
            x1.append(f"{row[1]} {num_to_month[int(row[2])]} {row[3]}")
            y1.append(int(row[4]))
        elif "USA" in line:
            row = line.split(",")
            x2.append(f"{row[1]} {num_to_month[int(row[2])]} {row[3]}")
            y2.append(int(row[4]))

    fig = go.Figure(layout=layout)
    fig.add_trace(go.Bar(x=x1, y=y1))
    fig.update_layout(title="Confirmed COVID cases in Norway", xaxis_title="Day", yaxis_title="# Cases")
    fig.write_html("plots/covid_norway.html")

    fig = go.Figure(layout=layout)
    fig.add_trace(go.Bar(x=x2, y=y2, marker_color="red"))
    fig.update_layout(title="Confirmed COVID cases in USA", xaxis_title="Day", yaxis_title="# Cases")
    fig.write_html("plots/covid_usa.html")


def update_template():
    with open("template.html", "r") as f:
        soup = BeautifulSoup(f.read(), features="html5lib")

    for div in soup.find_all("div", class_="plot"):
        with open(div["src"], "r") as f:
            plot = BeautifulSoup(f.read(), features="html5lib")
            div.replace_with(plot.html.body.div)

    with open("document.html", "w") as f:
        f.write(soup.prettify())


if __name__ == "__main__":
    plot_unemployment()
    plot_covid()
    update_template()

