import pandas as pd
import numpy as np
import spacy


def extract_country(sentence, coutries_codes=None):
    if coutries_codes == None:
        countries_code = pd.read_csv('countries_code.csv')
    is_in_sentence = lambda name : name in sentence
    selected_countries = countries_code[countries_code['name'].apply(is_in_sentence)]['id'].tolist()

    extensions = ['UK', 'U.K', 'US', 'U.S']
    for i, ext in enumerate(extensions):
        if (ext in sentence) and (i <= 1) and (826 not in selected_countries):
            selected_countries.append(826)
        if (ext in sentence) and (i > 1) and (840 not in selected_countries):
            selected_countries.append(840)
    return selected_countries

def extract_company(sentence, nlp=None):
    if nlp == None:
        nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    selected_companies = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            txt = ' ' + ent.text + ' '
            if ' the ' in txt.lower():
                i0 = txt.lower().index(' the ')
                txt = (txt[:i0] + txt[i0+5:]).strip()
                selected_companies.append(txt)
            else:
                selected_companies.append(ent.text)
    return np.unique(selected_companies)