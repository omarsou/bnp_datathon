# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:28:03 2020

@author: elias
"""

def extract_country_codes(sentence, countries_code):
    is_in_sentence = lambda name : name in sentence
    return countries_code[countries_code['name'].apply(is_in_sentence)]['id'].tolist()