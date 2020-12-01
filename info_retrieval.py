from questions import BoolQuestions, CountryQuestions, SpecialQuestions

QUESTIONS_BOOL = [1, 2, 3, 4, 8, 13, 14, 15, 16, 17, 21]
QUESTIONS_COUNTRIES = [5, 6, 7, 9, 10, 11, 12, 18, 19, 20]
QUESTIONS_SPECIAL = [22]
IGNORE_NEXT = {3: 1, 15: 5}
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
        i = 0

        while i <= 22:
            if i in QUESTIONS_BOOL:
                answer_id = self.answer_question_bool(chunks, i)
        pass

    def split_text(self, text):
        # TO DO : HOW ARE WE GOING TO SPLIT OUR TEXT IN SEVERAL CHUNKS ?
        pass

    def find_topk_paragraphs(self,  chunks, i):
        # TO DO : HOW ARE WE GOING TO FIND THE BEST PARAGRAPHS
        pass

    def answer_question_bool(self, chunks, i):
        # TO DO : HOW ARE WE GOING TO ANSWER QUESTIONS WITH BOOLEAN
        pass

    def answer_question_country(self, chunks, i):
        # TO DO : HOW ARE WE GOING TO ANSWER QUESTION COUNTRY
        pass

    def answer_question_special(self, chunks, i):
        # TO DO : HOW ARE WE GOING TO ANSWER SPECIAL QUESTION
        pass