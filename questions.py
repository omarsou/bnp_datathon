class BoolQuestions:
    questions_to_id = {"Does the tool handle personal data? ": 1,
                       "Is a Data Processing Agreement/Addendum mentioned?": 2,
                       "Can the data be transferred / accessed outside of the EU?": 3,
                       "If yes, are the recipient countries of personal data clearly mentioned ?": 4,
                       "If the recipient countries is / are outside of the EU, does the legal documents mention "
                       "Binding Corporate Rules (BCR) or Standard Contractual Clauses (SCC)?" : 8,
                       "Does the supplier mention an ISO 27001 certification?": 13,
                       "Is there a cost to using the tool?": 14,
                       "Can the tool transfer the collected data and/or give access to third parties or "
                       "subcontractors?": 15,
                       "If Yes, are the reasons for these transfers and/or access detailed?": 16,
                       "If Yes, are these third parties/ sub-contractors / sub-processors listed?": 17,
                       "Does the contract includes a right of audit?": 21
                       }
    id_to_questions = {v: k for k, v in questions_to_id.items()}


class CountryQuestions:
    questions_to_id = {"In which countries outside of the EU the data can be transferred to ?": [5, 6, 7],
                       "What are the countries of the applicable law of the contract?": [9, 10],
                       "What are the countries jurisdiction applicable in the event of a dispute?": [11, 12],
                       "If Yes, what are the location of these third parties/ sub-contractors / sub-processors?": [18,
                                                                                                                   19,
                                                                                                                   20],
                       }
    id_to_questions = {v: k for k, v in questions_to_id.items()}


class SpecialQuestions:
    questions_to_id = {"Is a data retention period defined?": 22}
    id_to_questions = {v: k for k, v in questions_to_id.items()}
