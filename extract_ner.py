from pandas import DataFrame
import numpy as np


class Extractor:
    def __init__(self, pipeline, countries_code):
        self.pipeline = pipeline
        self.countries_code = countries_code

    def extract(self, sentence, type='Country'):
        ner = self.pipeline(sentence)
        if type is 'Country':
            return self.extract_country(sentence, ner)
        else:
            return {'countries': self.extract_country(sentence, ner), 'companies': self.extract_companies(sentence, ner)}

    def extract_country(self, sentence, ner):
        ### quick search of country names that appear in the sentence ###
        is_in_sentence = lambda name: name in sentence
        selected_countries = self.countries_code[self.countries_code['name'].apply(is_in_sentence)]['id'].tolist()
        #################################################################

        ### let's see what the NER discovers new ###
        if len(ner) == 0:
            return selected_countries
        location_criteria = lambda entity: 'LOC' in entity
        df = DataFrame(ner)
        df = df[df['entity'].apply(location_criteria)]
        df = df[df['word'] != '.']
        df = df[df['score'] >= 0.8]
        extracted_countries = self.extract_country_names(df)
        ############################################

        for country in extracted_countries:
            if country.lower() == 'usa':
                if 840 not in selected_countries:
                    selected_countries.append(840)
                    break
            if country.lower() == 'us':
                if 840 not in selected_countries:
                    selected_countries.append(840)
                    break
            if country.lower() == 'uk':
                if 826 not in selected_countries:
                    selected_countries.append(826)
        return sorted(selected_countries)

    def extract_companies(self, sentence, ner):
        if len(ner) == 0:
            return []
        is_org = lambda entity: 'ORG' in entity
        df = DataFrame(ner)
        df = df[df['entity'].apply(is_org)]
        df = df[df['word'] != '.']
        df = df[df['score'] >= 0.96]
        if len(df) == 0:
            return []
        return self.merge_loc(df)

    @staticmethod
    def merge_loc(dataframe):
        dataframe['index_diff'] = dataframe['index'].diff()
        dataframe['label'] = 0;
        label = 0
        for i in range(dataframe.shape[0]):
            if dataframe[i:i + 1]['index_diff'].values[0] <= 2 and dataframe[i:i + 1]['entity'].values[0] == 'I-ORG':
                dataframe.loc[dataframe.index[i], 'label'] = label
                if not '#' == dataframe.loc[dataframe.index[i], 'word'][0]:
                    dataframe.loc[dataframe.index[i], 'word'] = ' ' + dataframe.loc[dataframe.index[i], 'word']
            else:
                label += 1
                dataframe.loc[dataframe.index[i], 'label'] = label
        tf_str = lambda str_: ''.join(str_.split('#'))
        return np.unique(dataframe.groupby(dataframe['label'])['word'].sum().apply(tf_str))

    @staticmethod
    def extract_country_names(dataframe):
        dataframe['index_diff'] = dataframe['index'].diff()
        dataframe['label'] = 0
        label = 0
        for i in range(dataframe.shape[0]):
            if dataframe[i:i + 1]['index_diff'].values[0] <= 2 and dataframe[i:i + 1]['entity'].values[0] == 'I-LOC':
                dataframe.loc[dataframe.index[i], 'label'] = label
                if len(dataframe[i - 1:i]['word'].values[0]) > 3:
                    dataframe.loc[dataframe.index[i - 1], 'word'] = ' ' + dataframe.loc[dataframe.index[i - 1], 'word']
            else:
                label += 1
                dataframe.loc[dataframe.index[i], 'label'] = label
        return np.unique(dataframe.groupby(dataframe['label'])['word'].sum())
