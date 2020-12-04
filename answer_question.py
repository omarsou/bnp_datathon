import torch


class QuestionAnswering:
    def __init__(self, tokenizer_qa, model_qa):
        self.tokenizer_qa = tokenizer_qa
        self.model_qa = model_qa

    def answer_question(self, question, text):
        """Given a question and a context (text), it will return the answer if there is one, otherwise
        it will returns no answer."""
        input_dict = self.tokenizer_qa.encode_plus(question, text, return_tensors='pt', max_length=512, truncation=True)
        input_ids = input_dict["input_ids"].tolist()
        start_scores, end_scores = self.model_qa(**input_dict)
        start = torch.argmax(start_scores)
        end = torch.argmax(end_scores)
        all_tokens = self.tokenizer_qa.convert_ids_to_tokens(input_ids[0])
        answer = ''.join(all_tokens[start: end + 1]).replace('▁', ' ').strip()
        return answer if answer != '[CLS]' and len(answer) != 0 else None
