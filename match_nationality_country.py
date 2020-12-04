# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:24:06 2020

@author: elias
"""

from pandas import read_csv, read_excel


def match_country(adjective, citizens=None, countries_code=None):
    if countries_code == None:
        countries_code = pd.read_csv('countries_code.csv')
    if citizens == None:
        citizen = pd.read_excel('citizens.xlsx')
    is_adjective = lambda adj : adjective.capitalize() in adj
    country = citizens[citizens['Adjective'].apply(is_adjective)]['Country'].values[0]
    return countries_code[countries_code['name'] == country]['id'].values[0]