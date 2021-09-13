# import argparse
import sys

from datetime import timedelta, datetime
from loguru import logger
from prettytable import PrettyTable
import requests
import csv
import os

# set important vars
description = """COVID CLI getter

This is everyone's little pet project during lockdown
"""


url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
filename = "Cache.csv"
today = datetime.today().strftime('%Y-%m-%d')
countries_to_watch = ("Israel", "Estonia", "United States", "Italy", "Spain", "Netherlands", "India", "Canada", "China")
countrydict = {}
mode = 2

logger.remove()  # remove the .env set logger, i'm too lazy to customize environments right now.
logger.add(sys.stderr, level="DEBUG")


# functions
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

def format_builtin(n):
    return format(n, ',')

def clean_data(n):
    if n != "":
        n = format_builtin(round(float(n)))
    return n

# lets go

# check to see if cache needs updating

if not (os.path.isfile(filename)) or modification_date(filename) < datetime.now() - timedelta(hours=12):
    logger.debug("re-getting file")
    response = requests.request("GET", url).text
    with open(filename, "w") as f:
        f.writelines(response)
    response = response.splitlines()



else:
    logger.debug("OK in cache")
    with open(filename) as f:
        response = f.readlines()

csvreader = csv.reader(response)
for country in csvreader:
    if country[2] in countries_to_watch and country[4] != "": #second test there makes sure we don't have an incomplete day
        countrydict[country[2]] = country

t = PrettyTable(['PLACE', 'TOTAL CASES', 'NEW CASES','TOTAL DEATHS','NEW DEATHS','VACCINATED', 'NEW VAX', 'Updated'])
t.align = "l"
t.sortby = "PLACE"
for countryname, country in countrydict.items():
    region = country[1]  # like Asia
    state = country[2]  # like israel
    total_cases = clean_data(country[4])
    new_cases = clean_data(country[5].split(".")[0])
    total_deaths = clean_data(country[7].split(".")[0])
    new_deaths = clean_data(country[8].split(".")[0])
    people_fully_vaccinated = clean_data(country[35].split(".")[0])
    new_vaccinations = clean_data(country[37].split(".")[0])
    datestamp = country[3]
    t.add_row([state, total_cases, new_cases, total_deaths, new_deaths, people_fully_vaccinated, new_vaccinations, datestamp])

if mode == 0:
    print(t)
if mode == 1:
    print(t.get_html_string(attributes={"name":"my_table", "class":"red_table"}))
if mode == 2:
    htmlblock = f"""
<figure>
<figcaption>COVID stats</figcaption>
<pre>
<code>
{t}
</code>
</pre>
</figure>
    """.format(t)
    print(htmlblock)