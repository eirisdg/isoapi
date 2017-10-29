#! /usr/bin/env python
"""
Script to recollect Countries data from wikipedia ISO-3166 page (https://en.wikipedia.org/wiki/ISO_3166-1) and store
in separate DB.
"""

import os
print(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())

import sqlite3
import bs4
import requests

db = sqlite3.connect("./sqlite/iso3166.db")
c = db.cursor()
c.execute("DROP TABLE IF EXISTS countries")
columns = ['name', 'alpha_2', 'alpha_3', 'numeric']
c.execute("CREATE TABLE IF NOT EXISTS countries ({} VARCHAR(100), {} VARCHAR(100), {} VARCHAR(100), {} VARCHAR(100))".format(*columns))
db.commit()

countries = [{
            ['name', 'alpha_2', 'alpha_3', 'numeric'][no]:
                td.find_all()[-1].text
            for no, td in enumerate(row.find_all('td')[:-2])
        }
        for row in bs4.BeautifulSoup(
        requests.get('http://en.wikipedia.org/wiki/ISO_3166-1').text, 'html.parser'
    ).find_all('table', {'class': 'wikitable sortable'})[1].find_all('tr')
]

query = "INSERT INTO countries values (?, ?, ?, ?)"

for country in countries:
    if country != {}:
        values = [country['name'], country['alpha_2'], country['alpha_3'], country['numeric']]
        c = db.cursor()
        c.execute(query, values)
        c.close()
db.commit()
db.close()
