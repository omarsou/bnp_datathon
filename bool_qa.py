from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW,DistilBertTokenizer
import random
import torch
import numpy as np
import pandas as pd

#loading tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('/content/drive/MyDrive/bnp-datathon/tokenizer')

#loading model
model = AutoModelForSequenceClassification.from_pretrained("/content/drive/MyDrive/bnp-datathon/model")
model.eval()

question = 'Does the tool handle personal data?'
passage = 'The table below describes Zoom’s processing of personal data as a data controller. The table does not cover customer content, including any personal data about you that may be contained in customer content—such as meeting or call recordings or transcripts—because the customer (the Zoom account holder), rather than Zoom, controls how customer content is processed. Any questions about the processing of customer content should be addressed to the customer directly.'

def predict(question, passage):
  sequence = tokenizer.encode_plus(question, passage, return_tensors="pt")['input_ids']
  
  logits = model(sequence)[0]
  probabilities = torch.softmax(logits, dim=1).detach().cpu().tolist()[0]
  output = np.argmax(probabilities)
  return output

print(predict(question,passage))