import os
from answer_question import QuestionAnswering
from extract_ner import Extractor
from match_nationality_country import MatchCountryFromNationality
import pandas as pd
import json
from info_retrieval_v2 import WinnersFillingForm
from transformers import pipeline, AlbertTokenizer, AlbertForQuestionAnswering, AutoTokenizer, \
    AutoModelForTokenClassification
from rank_bm25 import BM25Okapi

## MODEL NER ##
tokenizer_ner = AutoTokenizer.from_pretrained("/apps/models/bert_base_ner") # to modify
model_ner = AutoModelForTokenClassification.from_pretrained("/apps/models/bert_base_ner") # to modify

## MODEL QUESTION ANSWERING ##
tokenizer_qa = AlbertTokenizer.from_pretrained('smalbert/')
model_qa = AlbertForQuestionAnswering.from_pretrained('smalbert/')
pip_ner = pipeline("ner", model=model_ner, tokenizer=tokenizer_ner)

countries_codes = pd.read_csv('countries_code.csv')  # Codes of the countries
citizens_data = pd.read_excel('citizens.xlsx')

## MATCH NATIONALITY TO COUNTRY ('spanish' => 'spain')
match_nat = MatchCountryFromNationality(citizens_data, countries_codes)

countries_codes = pd.read_csv('countries_code.csv')  # Codes of the countries

# INITIALISATION of the Extractor (NER) / Question Answering
country_extractor = Extractor(pip_ner, countries_codes)
answer_question = QuestionAnswering(tokenizer_qa, model_qa)

# BM25 FOR PARAGRAPH RANKING
bm25 = json.load(open("tokensBM25", "r"))
bm25 = {k: BM25Okapi(v) for k,v in bm25.items()}


#### PATH TO THE DOCUMENTS ####
documents_directory = "/data"
path_to_files = [os.path.join(documents_directory, file) for file in os.listdir(documents_directory)]
assert len(path_to_files) == 10
path_to_files.sort()  # SORT AS IT IS ESSENTIAL (ASKIP)

bnp_pipeline = WinnersFillingForm(answer_question, bm25,  country_extractor, match_nat)


def main():
    results = {}
    for i, path in enumerate(path_to_files):
        with open(path, "r") as input_file:
            text = input_file.read()  # Here we have all the document's text
        all_answers = bnp_pipeline.answer(text)
        for answer in all_answers:
            question_number = answer['question_id'] + i*22  # TO IMPLEMENT WITH THE CLASS MODEL
            results[question_number] = answer['answer_id']
    #assert len(results) == len(path_to_files) * 22
    #assert set(list(results.keys())) == {i for i in range(1, 221)}
    return results


if __name__ == "__main__":
    main()
