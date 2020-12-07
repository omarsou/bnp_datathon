class MatchCountryFromNationality:
    """Given a sentence, it will match the nationality mentioned with the associated country.
    Parameters
    ----------
    citizens_data : dataframe
                    dataframe that contains for each nationality the corresponded country.

    countries_code_data : dataframe
                          dataframe that contains for each country the corresponded id country.
    """
    def __init__(self, citizens_data, countries_code_data):
        self.citizens = citizens_data
        self.countries_code = countries_code_data

    def match_country(self, sentence):
        """
        Parameters
        ----------
        sentence : str
                   sentence target

        Return
        ------
        matched : array_like (shape=(n,)) where n is the number of matched countries

        Examples
        --------
        >>> sentence = "I love american tequila"
        >>> match_coutry(sentence)
        >>> [840]
        """
        candidates = sentence.lower().split()
        is_adjective = lambda adj: adj.lower() in candidates
        try:
            country = self.citizens[self.citizens['Adjective'].apply(is_adjective)]['Country'].values[0]
        except IndexError:
            return []
        return [int(self.countries_code[self.countries_code['name'] == country]['id'].values[0])]
