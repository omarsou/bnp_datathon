import os
import sys
from extract_ner_v2 import Extractor
from match_nationality_country_v2 import MatchCountryFromNationality
import pandas as pd
import json
from info_retrieval_v5_justif import WinnersFillingForm
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


def main(documents_directory, output_directory):
    #### PATH TO THE DOCUMENTS ####
    path_to_files = [os.path.join(documents_directory, file) for file in os.listdir(documents_directory)]
    assert len(path_to_files) == 10
    path_to_files.sort()  # SORT AS IT IS ESSENTIAL (ASKIP)

    # Initialise the pipeline
    bnp_pipeline = WinnersFillingForm(answer_question, bm25, extractor, match_nat)
    path_output_file = os.path.join(output_directory, "answers.txt")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    output_txt = ""
    for i, path in enumerate(path_to_files):
        output_txt += f"### Company : {os.path.basename(path)} ###\n"
        with open(path, "r") as input_file:
            text = input_file.read()  # Here we have all the document's text
        all_answers = bnp_pipeline.answer(text)
        for answer in all_answers:
            output_txt += f"Question {answer['question_id']} | Answer {answer['answer_id']} | Justification " \
                          f"{answer['justification']}\n"
        output_txt += "\n\n"
    with open(path_output_file, "w") as output_file:
        output_file.write(output_txt)


if __name__ == "__main__":
    documents_directory = sys.argv[1]
    output_directory = sys.argv[2]
    main(documents_directory, output_directory)
