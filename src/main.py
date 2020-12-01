import plotly.graph_objects as go
from bs4 import BeautifulSoup
from usa import get_usa
from norway import get_norway
from covid import get_covid


# A general layout used to configure the plots
layout = go.Layout(paper_bgcolor="rgb(0,0,0,0)",
                   plot_bgcolor="rgb(0,0,0,0)",
                   font_color="#ebf0f2")


def plot_unemployment():
    """
        Plots the unemployment rate of Norway and USA.
        The result is an html file with the plot.
    """

    # Create the plot
    fig = go.Figure(layout=layout)

    # Plot the data from Norway
    x, y = get_norway()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="Norway"))

    # Plot the data from USA
    x, y = get_usa()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="USA"))

    # Add a vertical line that represents when the lockdown started
    fig.add_vline(x="Mar 2020", line_color="#00cc96")
    fig.add_annotation(x="Mar 2020", yref="y domain", y=1.1, text="Lockdown", showarrow=False)

    # Customize the grid colors
    fig.update_xaxes(gridcolor="#a9a9a9")
    fig.update_yaxes(gridcolor="#a9a9a9")

    # Add titles for plot and axis
    fig.update_layout(title="Unemployment rate in Norway and USA", xaxis_title="Month", yaxis_title="Rate")

    # Create the finished html file
    fig.write_html("plots/unemployment.html")


def _plot_covid(x, y, country, lockdown, color1, color2):
    """
        Helper function for plot_covid.
        Creates the plots for the given data, and saves it as an html file.
    """

    # Create the plot
    fig = go.Figure(layout=layout)

    # Plot the given data
    fig.add_trace(go.Bar(x=x, y=y, marker_color=color1))

    # Add a vertical line representing the lockdown
    fig.add_vline(x=lockdown, line_color=color2)
    fig.add_annotation(x=lockdown, yref="y domain", y=1.1, text="Lockdown", showarrow=False)


    # Add titles for plot and axis
    fig.update_layout(title="Confirmed COVID cases in " + country, xaxis_title="Day", yaxis_title="# Cases")

    # Create the finished html file
    fig.write_html("plots/covid_" + country.lower() + ".html")


def plot_covid():
    """
        Plots the number of Covid cases per day for Norway and USA.
    """

    norway, usa = get_covid()
    _plot_covid(norway[0], norway[1], "Norway", "12 Mar 2020", "#636efa", "#ef553b")
    _plot_covid(usa[0], usa[1], "USA", "22 Mar 2020", "#ef553b", "#636efa")


def update_template():
    """
        Combines template.html with the plots.
        The resulting file (document.html) is the finished report.
    """

    # Open, and read, the template file
    with open("template.html", "r") as f:
        soup = BeautifulSoup(f.read(), features="html5lib")

    # Add the plots in the correct places
    for div in soup.find_all("div", class_="plot"):
        with open(div["src"], "r") as f:
            plot = BeautifulSoup(f.read(), features="html5lib")
            div.replace_with(plot.html.body.div)

    # Write the finished report to document.html
    with open("document.html", "w") as f:
        f.write(soup.prettify())


if __name__ == "__main__":
    plot_unemployment()
    plot_covid()
    update_template()

