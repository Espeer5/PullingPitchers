"""
This module contains the functions for parsing CSV data from Savant 
CSVs into a format which is consumable for clustering and other data 
processing.

Author: Edward Speer
Date: 5/1/23
"""

import csv

CSVPATH = "../../csvs"


def collect():
    """Parses data from the collection of pitching arsenal CSVs
    into a dicitonary mapping each player to a dictionary of the 
    characteristics of their arsenal, removing all string valued 
    fields from the arsenal (name and ID number)"""
    arsenals = {}
    with open(f"{CSVPATH}/pitch_arsenals.csv", "r") as spn:
        spn_rd = csv.DictReader(spn, restval = 0)
        for row in spn_rd:
            arsenals[row['pitcher']] = row
    with open(f"{CSVPATH}/pitch_arsenals_pct.csv", 'r') as pct:
        pct_rd = csv.DictReader(pct, restval = 0)
        for row in pct_rd:
            arsenals[row['pitcher']].update(row)
    with open(f"{CSVPATH}/pitch_arsenals_spd.csv", 'r') as spd:
        spd_rd = csv.DictReader(spd, restval = 0)
        for row in spd_rd:
            arsenals[row['pitcher']].update(row)
    clean_strs(arsenals)
    return arsenals

def clean_strs(arsenals):
    """ Removes all non-numeric fields from the data scraped from 
    baseball savant CSVs.
    """
    for player in arsenals:
        dict = arsenals[player]
        for str in ['pitcher', ' first_name', 'last_name']:
            dict.pop(str)