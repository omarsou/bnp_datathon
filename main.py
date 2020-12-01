import os

#### PATH TO THE DOCUMENTS ####
documents_directory = "/data"
path_to_files = [os.path.join(documents_directory, file) for file in os.listdir(documents_directory)]
assert len(path_to_files) == 10
path_to_files.sort()  # SORT AS IT IS ESSENTIAL (ASKIP)

class_model = None  # TO IMPLEMENT


def main():
    results = {}
    for i, path in enumerate(path_to_files):
        with open(path, "r") as input_file:
            text = input_file.read()  # Here we have all the document's text
        all_answers = class_model.answer(text)
        for answer in all_answers:
            question_number = answer.question_id + i*22  # TO IMPLEMENT WITH THE CLASS MODEL
            results[question_number] = answer.answer_id
    assert len(results) == len(path_to_files) * 22
    assert set(list(results.keys())) == {i for i in range(1, 221)}
    return results

if __name__ == "__main__":
    main()





