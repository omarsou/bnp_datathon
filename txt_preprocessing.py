import nltk
from stopwords import english_stopwords
import re
from nltk.stem import PorterStemmer

ps = PorterStemmer()


def strip_characters(text):
    t = re.sub('\(|\)|:|,|;|\.|’|”|“|\?|%|>|<', '', text)
    t = re.sub('/', ' ', t)
    t = t.replace("'", '')
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
                     and (not word.isnumeric() or word.isalpha())])
                )


def preprocess(text):
    t = clean(text)
    tokens = tokenize(t)
    return tokens
