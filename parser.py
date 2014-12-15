#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json
from string import punctuation

from stopwords import stopwords_list

def RemoveStopWords(token_list):
    tmp = [ w for w in token_list if w not in stopwords_list ]
    cap = lambda s: s.capitalize()
    cap_stopwords = list(map(cap, stopwords_list))
    return [ w for w in tmp if w not in cap_stopwords ]

def RemoveStrPunc(mystr):
    exclude = punctuation
    result = ''.join(ch for ch in mystr if ch not in exclude)
    return result

def Tokenize(mystr):
    strip_str = mystr.strip()
    no_punc_str = RemoveStrPunc(strip_str);
    terms = [w.lower() for w in no_punc_str.split() if w.isalpha()]  #  contain duplicates
    terms = RemoveStopWords(terms)
    terms.sort()
    return terms

def GenrDocIndex():
    doc_index = []
    read_files = glob.glob("docs/*")

    for f in read_files:
        with open (f, 'r') as input:
            contents = input.read()
            terms = Tokenize(contents)
            record = [f, terms]
            doc_index.append(record)

    with open('log/corpus.txt', 'w') as fp:
        for data in doc_index:
            json.dump(data, fp)
            fp.write('\n')


if  __name__ == "__main__":
    GenrDocIndex()


