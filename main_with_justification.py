import os
import sys
from typing import List

from datathon_ai.form_company_filling import FormCompanyFilling
from datathon_ai.extractors import BasicExtractor, BasicCountryExtractor
from datathon_ai.interfaces import FormDataModel, CountryReferential, COUNTRY_QUESTIONS_NUMBERS, \
    NOT_COUNTRY_QUESTIONS_NUMBERS


def main_with_justification(documents_directory: str, output_directory: str):
    """
    Function that makes predictions with justification.
    :param documents_directory: path of directory that contains the .txt documents. One .txt document by company.
    :param output_directory: path of directory where to dump the answers and justifications hy question.
    Dumped file is under .txt format and has the following structure for each .txt file in documents_directory.
    ### Company : docusign.txt ###
    Question <question_number> | Answer <answer_id> | Justification <justification>
    """
    # Initiation of your objects
    data_model = FormDataModel.from_json_file(
        os.path.join(os.path.dirname(__file__), "resources", "data-model.json")
    )
    country_referential = CountryReferential.from_csv(
        os.path.join(os.path.dirname(__file__), "resources", "countries_code.csv")
    )
    form_company_filling = FormCompanyFilling([
        BasicExtractor(
            question_ids=NOT_COUNTRY_QUESTIONS_NUMBERS,
            form_data_model=data_model
        ),
        BasicCountryExtractor(
            question_ids=COUNTRY_QUESTIONS_NUMBERS,
            form_data_model=data_model,
            country_code_referential=country_referential
        ),
    ])

    # Get path of files
    path_to_files: List[str] = [os.path.join(documents_directory, file) for file in os.listdir(documents_directory)]
    assert len(path_to_files) == 10 # 10 files in documents directory
    # Sort list of path file by alphabetical order to match ground truth annotations order.
    path_to_files.sort()

    # Init file in output_directory
    path_output_file = os.path.join(output_directory, "answers.txt")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)


    # Compute your prediction by file (ie company)
    output_txt = ""
    for path in path_to_files:
        print(f"Running predictions for file : {path}")
        output_txt += f"### Company : {os.path.basename(path)} ###\n"
        with open(path, "r") as input_file:
            text = input_file.read()
        form_company_response = form_company_filling.fill(text)
        # Sort the response by question number for each company
        form_company_response.sort_by_question_id()
        for answer in form_company_response.answers:
            output_txt += f"Question {answer.question_id} | Answer {answer.answer_id} | Justification {answer.justification}\n"
        output_txt += "\n\n"

    with open(path_output_file, "w") as output_file:
        output_file.write(output_txt)

if __name__ == "__main__":
    documents_directory = sys.argv[1]
    output_directory = sys.argv[2]
    main_with_justification(documents_directory, output_directory)
