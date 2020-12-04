from pandas import DataFrame
import numpy as np
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def merge_LOC(dataframe):
    dataframe['index_diff'] = dataframe['index'].diff()
    dataframe['label'] = 0; label = 0
    for i in range(dataframe.shape[0]):
        if dataframe[i:i+1]['index_diff'].values[0] <= 2 and dataframe[i:i+1]['entity'].values[0] == 'I-ORG':
            dataframe.loc[dataframe.index[i], 'label'] = label
            if (not '#' == dataframe.loc[dataframe.index[i], 'word'][0]):
                dataframe.loc[dataframe.index[i], 'word'] = ' ' + dataframe.loc[dataframe.index[i], 'word']
        else:
            label += 1
            dataframe.loc[dataframe.index[i], 'label'] = label
    tf_str = lambda str_ : ''.join(str_.split('#'))
    return np.unique(dataframe.groupby(dataframe['label'])['word'].sum().apply(tf_str))

def extract_companies(sentence, model=nlp):
    ner = model(sentence)
    if len(ner) == 0: return []
    is_org = lambda entity : 'ORG' in entity
    df = DataFrame(ner); df = df[df['entity'].apply(is_org)]; df = df[df['word'] != '.']; df = df[df['score'] >= 0.5]
    if len(df) == 0: return []
    return merge_LOC(df)