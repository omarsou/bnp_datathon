class MatchCountryFromNationality:
    def __init__(self, citizens_data, countries_code_data):
        self.citizens = citizens_data
        self.countries_code = countries_code_data

    def match_country(self, adjective):
        if adjective is None:
            return []
        is_adjective = lambda adj: adjective.capitalize() in adj
        try:
            country = self.citizens[self.citizens['Adjective'].apply(is_adjective)]['Country'].values[0]
        except IndexError:
            return []
        return [int(self.countries_code[self.countries_code['name'] == country]['id'].values[0])]
