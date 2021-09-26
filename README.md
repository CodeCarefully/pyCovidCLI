# pyCovidCLI
Everyone has a covid app. I made one to play with GoLang, 
and now I'm making one in python. 

This is pretty much a silly fun project, somewhat based on my 
[earlier work](https://github.com/CodeCarefully/myCOVIDcli) 

Data on COVID-19 (coronavirus) by Our World in Data (https://github.com/owid/covid-19-data/tree/master/public/data)

COVID CLI getter

This is everyone's little pet project during lockdown.
Data on COVID-19 (coronavirus) by Our World in Data (https://github.com/owid/covid-19-data/tree/master/public/data)

```
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
```
### ToDo:

* Make into a PIP Package?
* Handle fail cases better
* Tests