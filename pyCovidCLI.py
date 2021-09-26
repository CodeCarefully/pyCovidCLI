"""
COVID CLI getter

This is everyone's little pet project during lockdown.
Data on COVID-19 (coronavirus) by Our World in Data (https://github.com/owid/covid-19-data/tree/master/public/data)

usage:
    pyCovidCLI -h | --help | --version | --licence
    pyCovidCLI [--URL=<url>] [--cachedir=<directory>] [--verbose] [--cacheoff] [--format=<fmt>] [--countries=<csvcount>]

options:
  -h --help              Show this screen.
  --version              Show the version.
  --verbose              be chatty.
  --cacheoff             Disable cache
  --format=<fmt>         1 is table, 2 is HTML table, 3 is HTML tagged [default: 1].
  --countries=<csvcount> CSV of countries

"""
import sys

from datetime import timedelta, datetime
from loguru import logger
from prettytable import PrettyTable
import requests
import csv
import os
from docopt import docopt

logger.remove()  # remove the .env set logger, i'm too lazy to customize environments right now.

arguments = docopt(__doc__, options_first=True, version='1.0.0')

# handle basic arguments
if arguments["--licence"]:
    print("GNU GENERAL PUBLIC LICENSE Version 3")
    exit(0)

if arguments["--cachedir"] is None:
    arguments["--cachedir"] = "Cache.csv"

if arguments["--URL"] is None:
    arguments["--URL"] = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

if arguments["--verbose"]:
    logger.add(sys.stderr, level="DEBUG")

if arguments["--countries"] is None:
    arguments["--countries"] = (
    "Israel", "Estonia", "United States", "Italy", "Spain", "Netherlands", "India", "Canada", "China")
else:
    arguments["--countries"] = arguments["--countries"].split(",")
    arguments["--countries"] = tuple(e for e in arguments["--countries"])

logger.debug("Post processing arguments: " + str(arguments))

# set remaining important vars
today = datetime.today().strftime('%Y-%m-%d')
countrydict = {}


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

response = None
docache = True
filefail = False

if arguments["--cacheoff"]:
    docache = False

if (not (os.path.isfile(arguments["--cachedir"])) \
        or modification_date(arguments["--cachedir"]) < datetime.now() - timedelta(hours=5)):
    docache = False
    filefail = True

if not docache:
    logger.debug("Fetching from URL")
    try:
        response = requests.request("GET", arguments["--URL"]).text
        if not arguments["--cacheoff"]:
            logger.debug("Writing to cache")
            with open(arguments["--cachedir"], "w") as f:
                f.writelines(response)
        response = response.splitlines()
    except Exception as e:
        if filefail == False:
            docache=True
        else:
            print("URL failure, no cache available")
            exit(1)


if response == None and docache:
    logger.debug("reading from cache")
    with open(arguments["--cachedir"]) as f:
        response = f.readlines()

if response == None:
    logger.debug("Fail state, no caching but no data either")
    exit(1)

csvreader = csv.reader(response)
for country in csvreader:
    if country[2] in arguments["--countries"] and country[
        4] != "":  # second test there makes sure we don't have an incomplete day
        countrydict[country[2]] = country

t = PrettyTable(['PLACE', 'TOTAL CASES', 'NEW CASES', 'TOTAL DEATHS', 'NEW DEATHS', 'VACCINATED', 'NEW VAX', 'Updated'])
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
    t.add_row(
        [state, total_cases, new_cases, total_deaths, new_deaths, people_fully_vaccinated, new_vaccinations, datestamp])

if arguments["--format"] == "1":
    print(t)
if arguments["--format"] == "2":
    print(t.get_html_string(attributes={"name": "my_table", "class": "red_table"}))
if arguments["--format"] == "3":
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
