# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:28:03 2020

@author: elias
"""

import numpy as np
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from pandas import DataFrame

def extract_country_names(dataframe):
    dataframe['index_diff'] = dataframe['index'].diff()
    dataframe['label'] = 0; label = 0
    for i in range(dataframe.shape[0]):
        if dataframe[i:i+1]['index_diff'].values[0] <= 2:
            dataframe.loc[dataframe.index[i], 'label'] = label
            if len(dataframe[i-1:i]['word'].values[0]) > 3:
                dataframe.loc[dataframe.index[i-1], 'word'] += ' '
        else:
            label += 1
            dataframe.loc[dataframe.index[i], 'label'] = label
    return np.unique(dataframe.groupby(dataframe['label'])['word'].sum())

def extract_country(sentence, countries_code):
    ### quick search of country names that appear in the sentence ###
    is_in_sentence = lambda name : name in sentence
    selected_countries = countries_code[countries_code['name'].apply(is_in_sentence)]['id'].tolist()
    #################################################################

    ### define the model for NER ###
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    ################################

    ### let's see what the NER discovers new ###
    ner = nlp(sentence)
    if len(ner) == 0: return selected_countries
    location_criteria = lambda entity : 'LOC' in entity
    df = DataFrame(ner); df = df[df['entity'].apply(location_criteria)]; df = df[df['word'] != '.']; df = df[df['score'] >= 0.8]
    extracted_countries = extract_country_names(df)
    ############################################

    for country in extracted_countries:
        if country == 'svk826': # cas particulier
            selected_countries.append(703)
        elif country == ' kr': # cas particulier
            selected_countries.append(410)
        elif len(country) == 3:
            country_id = countries_code[countries_code['alpha3'] == country.lower()]['id'].values
            if len(country_id) != 0 and country_id[0] not in selected_countries:
                selected_countries.append(country_id)
        elif len(country) == 2:
            country_id = countries_code[countries_code['alpha2'] == country.lower()]['id'].values
            if len(country_id) != 0 and country_id[0] not in selected_countries:
                selected_countries.append(country_id)
    return selected_countries