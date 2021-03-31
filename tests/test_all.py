# to run: pipenv run pytest
# or: pipenv run pytest tests/tests.py

import pytest

import os.path
from os import path

import sqlite3

import project0
from project0 import main

def test_test():
    # I am testing my knowledge of how to write a test :)
    result = "echo"
    assert result == "echo"

# fetchData()
def test_f1():
    main.fetchData("https://www.normanok.gov/sites/default/files/documents/2021-02/2021-02-21_daily_incident_summary.pdf")
    assert path.exists("/tmp/data.pdf")

# readData()
def test_f2():
    incidents = main.readData()

    # Check if the output format is what we expect
    assert type(incidents) == list
    assert type(incidents[0]) == tuple
    assert type(incidents[0][0]) == str

    # Check if the contents of the first row are correct
    assert incidents[0][0] == "2/21/2021 0:12"
    assert incidents[0][1] == "2021-00010177"
    assert incidents[0][2] == "2543 W MAIN ST"
    assert incidents[0][3] == "Disturbance/Domestic"
    assert incidents[0][4] == "OK0140200"

# createDB()
def test_f3():
    main.createDB()

    # Is there a file called "normanpd.db"?
    dbExists = path.exists("normanpd.db")
    assert dbExists

    if dbExists:
        # Is there a table in our database called "incidents"?
        con = sqlite3.connect("normanpd.db")
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='incidents'")
        tableExists = cur.fetchone()[0]
        con.close()
        assert tableExists == 1

# populateDB()
def test_f4():
    incidents = [('2/21/2021 0:12', '2021-00010177', '2543 W MAIN ST', 'Disturbance/Domestic', 'OK0140200'),
                 ('2/21/2021 0:20', '2021-00010178', '2543 W MAIN ST', 'Traffic Stop', 'OK0140200'),
                 ('2/21/2021 0:12', '2021-00010179', '2543 W MAIN ST', 'Drunk Driver', 'OK0140200'),
                 ('2/21/2021 0:12', '2021-00010179', '2543 W MAIN ST', 'Drunk Driver', 'OK0140200'),]

    main.populateDB(incidents)

    con = sqlite3.connect("normanpd.db")
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM incidents")
    numRecords = cur.fetchone()[0]
    con.close()
    assert numRecords > 0

# countNature()
def test_f5():
    #output = main.countNature()

    # Compare sum of natures to sum of rows?
    #assert len(output) == 4
    assert True
