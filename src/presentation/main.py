#!/usr/bin/env python3

from bs4 import BeautifulSoup

def update_template(graph):
    """
        Combines template.html with the plots.
        The resulting file (document.html) is the finished report.
    """

    # Open, and read, the template file
    with open("templates/" + graph + ".html", "r") as f:
        soup = BeautifulSoup(f.read(), features="html5lib")

    # Add the plots in the correct places
    for div in soup.find_all("div", class_="plot"):
        with open(div["src"], "r") as f:
            plot = BeautifulSoup(f.read(), features="html5lib")
            div.replace_with(plot.html.body.div)

    # Write the finished report to document.html
    with open("documents/" + graph + ".html", "w") as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    update_template("unemployment")
    update_template("covid_norway")
    update_template("covid_usa")
