from txt_preprocessing import preprocess
from re import compile
import numpy as np
from rank_bm25 import BM25Okapi

# Regex to check if the paragraph mentions some data transfer outside the EU
is_transfer = compile("outside|other countries|transfer")

# List of the code of each EU country
lst_code_europe = [40, 56, 100, 191, 196, 203, 208, 233, 246, 250, 276, 348, 372, 380, 428, 440, 442, 470, 528, 616,
                   620, 642, 705, 724, 752, 826]

# Regex to check if the paragraph mentions why they are sharing data (restrictive regex as we don't have many examples)
why_share_date = [['payment', 'process', 'crm'], ['service', 'provider', 'monitoring']]

# Regex to check if the paragraph ONLY and ONLY mentions that the tool retains data (no duration precised)
keep_is_only_mentioned = [['keep', 'information', 'as long as'], ['keep', 'data', 'as long as'],
                        ['retrain', 'information', 'as long as'], ['keep', 'data', 'as long as']]

# Regex to check if the paragraph mentions that the tool retains data
keep_is_mentioned = [['keep', 'personal', 'information'], ['keep', 'personal', 'information'],
                   ['retain', 'personal', 'information'], ['retain', 'personal', 'information']]

# Regex to check if they precise the duration they keep data
key_words_duration = compile('year|month|day|hour')

# Regex to check if there is a cost to use the tool
is_payment = [['subscription', 'payment'], ['subscription', 'pricing'], ['subscription plan', 'fees'],
              ['subscription term', 'fees'], ['credit card', 'fees'], ['payment term'], ['price', 'subscription'],
              ['fees', 'subscription']]

# Multi basic regex for question 2, 8, 9
keywords = {
            2: 'data processing agreement|data protection agreement|dpa|data protection addendum|data processing '
               'agreement|data protection attachment',
            8: 'bcr|scc|binding corporate rules|standard contractual clauses|data protection clauses|contractual '
               'clauses|data protection clauses',
            13: 'iso27001|iso 27001',
}


class WinnersFillingFormErrors(BaseException):
    """Class made to handle and explicit errors."""
    pass


class WinnersFillingForm:
    """Given a text (privacy policy) it answers a list of questions.
    Parameters
    ----------
    modelQA : Pytorch model for question answering

    modelRANK : dict
                dict where key is the id of a question and the values are the extracted tokens from the train/validation's
                answers.

    modelNER : class from extract_ner_v2.py
               Pipeline made to extract company or country from a sentence.

    matchNAT : class from match_nationality_country_v2
               Pipeline made to match the nationality mentioned in a sentence with country.

    Return
    ------
    answers_sheet : array like (shape=(n,)) where n is the number of question
                    list of dict where the key is the question id (1 to 22) and the value is the answer id.
    """
    def __init__(self, modelQA, modelRANK, modelNER, matchNAT):
        self.answer_question = modelQA  # MODEL FOR QUESTION ASNWERING
        self.bm25 = modelRANK  # MODEL FOR RANKING
        self.extractor = modelNER  # Model NER if we need it
        self.match_nat = matchNAT
        self.is_8_positive = False

    def answer(self, text):
        """Given a text (privacy policy) it answers a list of questions.
        Parameters
        ----------
        text : str
                text to analyse

        Return
        ------
        answers_sheet : array like (shape=(n,)) where n is the number of question
                        list of dict where the key is the question id (1 to 22) and the value is the answer id.
        """
        chunks = self.split_text(text)
        preprocess_chunks = list(map(preprocess, chunks))
        answers_sheet = []
        answers_sheet.append(self.answer_question_1(chunks, preprocess_chunks))
        answers_sheet.append(self.answer_questions_2_8_13(chunks))
        answers_sheet.append(self.answer_questions_3_to_7(chunks, preprocess_chunks))
        answers_sheet.append(self.answer_questions_9_10(chunks, preprocess_chunks))
        answers_sheet.append(self.answer_questions_11_12(chunks, preprocess_chunks))
        answers_sheet.append(self.answer_question_14(chunks, preprocess_chunks))
        answers_sheet.append(self.answer_questions_15_16(chunks, preprocess_chunks))
        answers_sheet.append(self.answer_questions_17_20(text))
        answers_sheet.append(self.answer_question_21(chunks, preprocess_chunks))
        answers_sheet.append(self.answer_question_22(chunks, preprocess_chunks))
        answers_sheet = sorted([sheet for sheets in answers_sheet for sheet in sheets], key=lambda k: k['question_id'])
        return answers_sheet

    def answer_question_1(self, chunks, preprocess_chunks):
        bm25 = BM25Okapi(preprocess_chunks)
        doc_scores = bm25.get_scores(preprocess('Personal Data Privacy Policy Collect Protect'))
        ans = int(max(doc_scores) > 0.1)
        return [{'answer_id': ans, 'question_id': 1}]

    def answer_questions_3_to_7(self, chunks, preprocess_chunks):
        bm25 = BM25Okapi(preprocess_chunks)
        scores = np.array([np.float64(0)]*len(preprocess_chunks))
        for query in self.bm25['3']:
            scores += bm25.get_scores(query)
        best = sorted(range(len(scores)), reverse=True, key=lambda i: scores[i])[:2]
        candidates = [chunks[i] for i in best]
        return self.answer_questions_3_to_7_(*candidates)

    def answer_questions_3_to_7_(self, candidat1, candidat2):
        questions_ids = [3, 4, 5, 6, 7]
        answers_ids = [0, 0]
        code_country = list(set(self.extractor.extract(candidat2) + self.extractor.extract(candidat1)))
        outside_europe = [id_ for id_ in code_country if id_ not in lst_code_europe]
        i = len(outside_europe)
        if self.is_8_positive or i >= 1 or is_transfer.search(candidat1) or is_transfer.search(candidat2):
            answers_ids = [1, 1 * (len(code_country) - 1 > 0)]
        answers_ids = answers_ids + outside_europe[:3] + [0] * (3 - len(outside_europe[:3]))
        return self.generate_dict_answer(answers_ids, questions_ids)

    def answer_questions_2_8_13(self, chunks):
        l = []
        for question_id in keywords.keys():
            query = compile(keywords[question_id])
            found = 0
            for chunk in chunks:
                if query.search(chunk.lower()):
                    found = 1
                    if question_id == 8:
                        self.is_8_positive = True
                    break
            l += [{'answer_id': found, 'question_id': question_id}]
        return l

    def answer_questions_9_10(self, chunks, preprocess_chunks):
        bm25 = BM25Okapi(preprocess_chunks)
        scores = np.array([np.float64(0)]*len(preprocess_chunks))
        for query in self.bm25['9']:
            scores += bm25.get_scores(query)
        best = sorted(range(len(scores)), reverse=True, key=lambda i: scores[i])[:2]
        candidates = [chunks[i] for i in best]
        return self.answer_question_9(candidates)

    def answer_question_9(self, candidates):
        question_id = [9, 10]
        answer_id = [0, 0]
        for candidate in candidates:
            if 'law' in candidate.lower():
                code_country = self.extractor.extract(candidate)
                if len(code_country) > 0:
                    answer_id = code_country[:2] + [0] * (2 - len(code_country[:2]))
                    break
                else:
                    code_country = self.match_nat.match_country(candidate)
                    if len(code_country) > 0:
                        answer_id = code_country + [0]
                        break
        return self.generate_dict_answer(answer_id, question_id)

    def answer_questions_11_12(self, chunks, preprocess_chunks):
        bm25 = BM25Okapi(preprocess_chunks)
        scores = np.array([np.float64(0)]*len(preprocess_chunks))
        for query in self.bm25['11']:
            scores += bm25.get_scores(query)
        best = sorted(range(len(scores)), key=lambda i: scores[i])[-1]
        candidate = chunks[best]
        return self.answer_question_11(candidate)

    def answer_question_11(self, candidate):
        question_id = [11, 12]
        code_country = self.extractor.extract(candidate)
        answer_id = code_country[:2] + [0] * (2 - len(code_country[:2]))
        return self.generate_dict_answer(answer_id, question_id)

    def answer_question_14(self, chunks, preprocess_chunks):
        question_id = 14
        answer_id = 0
        for chunk in chunks:
            if any(all(x in chunk.lower() for x in reg) for reg in is_payment):
                answer_id = 1
                break
        return [{'answer_id': answer_id, 'question_id': question_id}]

    def answer_questions_15_16(self, chunks, preprocess_chunks):
        bm25 = BM25Okapi(preprocess_chunks)
        scores = np.array([np.float64(0)]*len(preprocess_chunks))
        for query in self.bm25['15']:
            scores += bm25.get_scores(query)
        best = sorted(range(len(scores)), reverse=True, key=lambda i: scores[i])[:3]
        candidates = [chunks[i] for i in best]
        return self.answer_question_15_16_(candidates, max(scores) > 1)

    def answer_question_15_16_(self, candidates, is_shared=False):
        answer_id = [1*is_shared, 0]
        question_id = [15, 16]
        #question = "Why share data ?"
        for candidate in candidates:
            if any(all(x in candidate.lower() for x in reg) for reg in why_share_date):
                answer_id = [1, 1]
                break
        return self.generate_dict_answer(answer_id, question_id)

    def answer_questions_17_20(self, text):
        chunks = self.split_text(text[int(len(text)*0.75):], sep='\n')
        preprocess_chunks = list(map(preprocess, chunks))
        bm25 = BM25Okapi(preprocess_chunks)
        scores = np.array([np.float64(0)]*len(preprocess_chunks))
        for query in self.bm25['17']:
            scores += bm25.get_scores(query)
        best = sorted(range(len(scores)), reverse=True, key=lambda i: scores[i])[0]
        candidate, length = chunks[best], len(chunks[best].split())
        if length > 250:
            candidate = ' '.join(chunks[best-2:best+5])
        else:
            candidate = ' '.join(chunks[best-3:best+7])
        return self.answer_question_17_20_(candidate)

    def answer_question_17_20_(self, candidate):
        answer_id = [0, 0, 0, 0]
        question_id = [17, 18, 19, 20]
        extracted_elem = self.extractor.extract(candidate, type='all')
        if len(extracted_elem['companies']) > 0:
            answer_id = [1] + extracted_elem['countries'][:3] + [0]*(3 - len(extracted_elem['countries'][:3]))
        return self.generate_dict_answer(answer_id, question_id)

    def answer_question_21(self, chunks, preprocess_chunks):
        bm25 = BM25Okapi(preprocess_chunks)
        scores = np.array([np.float64(0)]*len(preprocess_chunks))
        for query in self.bm25['21']:
            scores += bm25.get_scores(query)
        best = sorted(range(len(scores)), reverse=True, key=lambda i: scores[i])[:2]
        candidates = [chunks[i] for i in best]
        return self.answer_question_21_(candidates)

    def answer_question_21_(self, candidates):
        answer_id = 0
        question_id = 21
        for candidate in candidates:
            if 'audit' in candidate.lower():
                answer_id = 1
                break
        return [{'answer_id': answer_id, 'question_id': question_id}]

    def answer_question_22(self, chunks, preprocess_chunks):
        bm25 = BM25Okapi(preprocess_chunks)
        scores = bm25.get_scores(preprocess('retain personal keep data information long'))
        best = sorted(range(len(scores)), reverse=True, key=lambda i: scores[i])[:3]
        candidates = [chunks[i] for i in best if len(chunks[i].split()) >= 7]
        return self.answer_question_22_(candidates)

    def answer_question_22_(self, candidates):
        answer_id = 0
        question_id = 22
        js = ''
        for candidate in candidates:
            if any(all(x in candidate.lower() for x in reg) for reg in keep_is_only_mentioned):
                answer_id, js = 1, candidate
                break
            if any(all(x in candidate.lower() for x in reg) for reg in keep_is_mentioned):
                answer_id, js = 1, candidate
                if self.is_duration_in_string(candidate):
                    answer_id = 2
                    break
        return [{'answer_id': answer_id, 'question_id': question_id}]

    @staticmethod
    def is_duration_in_string(txt):
        """Check if a duration is mentioned in a sentence."""
        if key_words_duration.search(txt.lower()):
            return True
        return False

    @staticmethod
    def generate_dict_answer(answer_ids, question_ids):
        """Generate a list of dict.
        Parameters
        ----------
        answer_ids : array like (shape=(n,)) where n is the number of question
                     list of answers' id

        question_ids : array like (shape=(n,)) where n is the number of question
                       list of questions' id

        Return
        ------
        sheet : array like (shape=(n,))

        Examples
        -------
        >>>answer_ids, questions_ids = [1,2], [20,21]
        >>>generate_dict_answer(answer_ids, questions_ids)
        >>>[{'answer_id': 1, 'question_id': 20}, {'answer_id': 2, 'question_id': 21}]
        """
        return [{'answer_id': i, 'question_id': j} for i, j in zip(answer_ids, question_ids)]

    @staticmethod
    def split_text(text, threshold=300, sep='\n\n'):
        """Split text according to a separator. If one of the split contains more than threshold words, it will split
        it in len(split)/threshold.
        For instance:
        if threshold = 2 and sentence = "I love nlp and computer vision" , it will give us "I love", "nlp and" and
         "computer vision".
        """
        docs = text.split(sep)
        for index, doc in enumerate(docs):
            splits = doc.split()
            if len(splits) > threshold:
                chunks, chunk_size = len(splits), threshold
                sentences = [' '.join(splits[j:j + chunk_size]) for j in range(0, chunks, chunk_size)]
                docs[index] = sentences[0]
                docs.extend(sentences[1:])
        return docs



