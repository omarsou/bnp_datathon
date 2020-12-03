from rank_bm25 import BM25Okapi
import nltk
import re
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
import nltk
nltk.download('stopwords')
nltk.download('punkt')

english_stopwords = list(set(stopwords.words('english')))
ps = PorterStemmer()
def strip_characters(text):
    t = re.sub('\(|\)|:|,|;|\.|’|”|“|\?|%|>|<', '', text)
    t = re.sub('/', ' ', t)
    t = t.replace("'",'')
    return t

def clean(text):
    t = text.lower()
    t = strip_characters(t)
    t = ps.stem(t)
    return t

def tokenize(text):
    words = nltk.word_tokenize(text)
    return list(set([word for word in words 
                     if len(word) > 1
                     and not word in english_stopwords
                     and not (word.isnumeric() and len(word) is not 4)
                     and (not word.isnumeric() or word.isalpha())] )
               )
def preprocess(text):
    t = clean(text)
    tokens = tokenize(t)
    return tokens

def split_text(text, threshold=300):
    docs = text.split('\n\n') 
    for index, doc in enumerate(docs):
        splits = doc.split()
        if len(splits) > threshold:
            chunks, chunk_size = len(splits), threshold
            sentences = [' '.join(splits[j:j+chunk_size]) for j in range(0, chunks, chunk_size)]
            docs[index] = sentences[0]
            docs.extend(sentences[1:])
    return docs

class Question1():
    def __init__(self, text_path):
        self.path = text_path
    def answer(self):
        with open(self.path, "r") as input_file:  ## PATH TO FILE TEXT
            text = input_file.read()
        texts = split_text(text)
        tokenized_corpus = list(map(preprocess, texts))
        bm25 = BM25Okapi(tokenized_corpus)
        query = preprocess('Personal Data Privacy Policy Collect Protect')
        doc_scores = bm25.get_scores(query)
        best_doc = sorted(range(len(doc_scores)), reverse=True, key=lambda i: doc_scores[i])[0]
        ans = int(max(doc_scores) > 0.5)
        if ans:
            return ans, texts[best_doc]
        else:
            return ans, None