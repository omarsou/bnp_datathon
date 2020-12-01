from questions import BoolQuestions, CountryQuestions, SpecialQuestions

QUESTIONS_BOOL = [1, 2, 3, 4, 8, 13, 14, 15, 16, 17, 21]
QUESTIONS_COUNTRIES = [5, 6, 7, 9, 10, 11, 12, 18, 19, 20]
QUESTIONS_SPECIAL = [22]
IGNORE_NEXT = {3: [3, 4], 15: [15, 16, 17, 18, 19, 20]}
IGNORE_START = [3, 15]
response_id_bool = {'Yes': 1, 'No': 0}
response_id_special = {'No': 0, 'Yes, mentioned only': 1, 'Yes, and precise durations are specified': 2}


class WinnersFillingFormErrors(BaseException):
    pass


class WinnersFillingForm:
    def __init__(self, code_country, modelQA, modelIR, modelNER=None, k=10):
        self.code_country = code_country ## Code of the country
        self.modelQA = modelQA ## MODEL FOR QUESTION ASNWERING
        self.modelIR = modelIR ## MODEL FOR RANKING
        self.modelNER = modelNER ## Model NER if we need it
        self.topk = k ## TOP K paragraph to inspect

    def answer(self, text):
        chunks = self.split_text(text)
        answers_sheet = []
        i = 1
        while i <= 22:
            if i in QUESTIONS_BOOL:
                answers_dict, steps = self.answer_question_bool(chunks, i)
                i += steps
            elif i in QUESTIONS_COUNTRIES:
                answers_dict, steps = self.answer_question_country(chunks, i)
                i += steps
            else:
                answers_dict, steps = self.answer_question_special(chunks, i)
                i += steps
            for dict_answer in answers_dict:
                answers_sheet.append(dict_answer)
        return answers_sheet

    def split_text(self, text):
        # TO DO : HOW ARE WE GOING TO SPLIT OUR TEXT IN SEVERAL CHUNKS ?
        pass

    def find_topk_paragraphs(self,  chunks, question):
        # TO DO : HOW ARE WE GOING TO FIND THE BEST PARAGRAPHS
        pass

    def answer_question_bool(self, chunks, i):
        # TO DO : HOW ARE WE GOING TO ANSWER QUESTIONS WITH BOOLEAN
        question = BoolQuestions.id_to_questions[i]
        candidates = self.find_topk_paragraphs(chunks, question)
        # TO DO
        # TO DO
        if answer_id == 0 and i in IGNORE_START:
            id_questions_to_ignore = IGNORE_NEXT[i]
            answers_sheet = [{'answer_id': answer_id, 'question_id': j} for j in id_questions_to_ignore]
            steps = len(id_questions_to_ignore) - 1
        else:
            answers_sheet = [{'answer_id': answer_id, 'question_id': i}]
            steps = 1
        return answers_sheet, i

    def answer_question_country(self, chunks, i):
        # TO DO : HOW ARE WE GOING TO ANSWER QUESTION COUNTRY
        question = CountryQuestions.id_to_questions[i]
        candidates = self.find_topk_paragraphs(chunks, question)
        countries_expected = CountryQuestions.questions_to_id[question]
        # TO DO
        # TO DO
        countries_id = sorted(countries_id) + [0]*(len(countries_id) - len(countries_expected))
        return [{'answer_id': answer_id, 'question_id': i} for answer_id, i in zip(countries_id, countries_expected)]

    def answer_question_special(self, chunks, i):
        # TO DO : HOW ARE WE GOING TO ANSWER SPECIAL QUESTION
        question = SpecialQuestions.id_to_questions[i]
        candidates = self.find_topk_paragraphs(chunks, question)
        # TO DO
        # TO DO
        return [{'answer_id': answer_id, 'question_id': i}]