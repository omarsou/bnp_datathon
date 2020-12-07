import os
from extract_ner_v2 import Extractor
from match_nationality_country_v2 import MatchCountryFromNationality
import pandas as pd
import json
from info_retrieval_v5 import WinnersFillingForm
import spacy

## MODEL NER ##
pip_ner = spacy.load('/apps/models/ner_spacy_en')

countries_codes = pd.read_csv('countries_code.csv')  # Codes of the countries
citizens_data = pd.read_excel('citizens.xlsx')  # nationality for each country

## MATCH NATIONALITY TO COUNTRY ##
match_nat = MatchCountryFromNationality(citizens_data, countries_codes)


# INITIALISATION of the Extractor (NER)
extractor = Extractor(pip_ner, countries_codes)
answer_question = None
# Extract answers' tokens for BM25 (Paragraph Ranking)
bm25 = json.load(open("tokensBM25", "r"))


#### PATH TO THE DOCUMENTS ####
documents_directory = "/data"
path_to_files = [os.path.join(documents_directory, file) for file in os.listdir(documents_directory)]
assert len(path_to_files) == 10
path_to_files.sort()  # SORT AS IT IS ESSENTIAL (ASKIP)

# Initialise the pipeline
bnp_pipeline = WinnersFillingForm(answer_question, bm25,  extractor, match_nat)


def main():
    results = {}
    for i, path in enumerate(path_to_files):
        with open(path, "r") as input_file:
            text = input_file.read()  # Here we have all the document's text
        all_answers = bnp_pipeline.answer(text)
        for answer in all_answers:
            question_number = answer['question_id'] + i*22  # TO IMPLEMENT WITH THE CLASS MODEL
            results[question_number] = answer['answer_id']
    assert len(results) == len(path_to_files) * 22
    assert set(list(results.keys())) == {i for i in range(1, 221)}
    return results


if __name__ == "__main__":
    main()
