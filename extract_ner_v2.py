class Extractor:
    def __init__(self, pipeline, countries_code):
        self.pipeline = pipeline
        self.countries_code = countries_code

    def extract(self, sentence, type='Country'):
        if type is 'Country':
            return self.extract_country(sentence)
        else:
            doc = self.pipeline(sentence)
            return {'countries': self.extract_country(sentence), 'companies': self.extract_company(sentence, doc)}

    def extract_country(self, sentence):
        is_in_sentence = lambda name: name in sentence
        selected_countries = self.countries_code[self.countries_code['name'].apply(is_in_sentence)]['id'].tolist()

        extensions = ['UK', 'U.K', 'US', 'U.S']
        for i, ext in enumerate(extensions):
            if (ext in sentence) and (i <= 1) and (826 not in selected_countries):
                selected_countries.append(826)
            if (ext in sentence) and (i > 1) and (840 not in selected_countries):
                selected_countries.append(840)
        return sorted(selected_countries)

    def extract_company(self, sentence, doc):
        selected_companies = []
        #i = 0
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                selected_companies.append(ent.text)
                break
                #txt = ' ' + ent.text + ' '
                #if ' the ' in txt.lower():
                    #i0 = txt.lower().index(' the ')
                    #txt = (txt[:i0] + txt[i0 + 5:]).strip()
                    #selected_companies.append(txt)
                #else:
                    #selected_companies.append(ent.text)
        return selected_companies
