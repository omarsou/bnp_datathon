class Extractor:
    """Given a sentence, it will extract both country and companies mentioned in the sentence.

    Parameters
    ----------
    pipeline : NER pipeline

    countries_code_data : dataframe
                          dataframe that contains for each country the corresponded id country.
    """
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
        """Extract countries from a sentence and return the corresponded code.
        Parameters
        ----------
        sentence : str

        Returns
        -------
        selected_countries : array_like (shape=(n,)) where n is the number of countries found
        """
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
        """Extract companies from a sentence and return the corresponded code.
        Parameters
        ----------
        sentence : str

        Returns
        -------
        selected_companies : array_like (shape=(n,)) where n is the number of companies found
        """
        selected_companies = []
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                txt = ' ' + ent.text + ' '
                if ' the ' in txt.lower():
                    i0 = txt.lower().index(' the ')
                    txt = (txt[:i0] + txt[i0 + 5:]).strip()
                    selected_companies.append(txt)
                else:
                    selected_companies.append(ent.text)
        return list(set(selected_companies))

