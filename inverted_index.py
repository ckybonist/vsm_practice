#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from math import log

import freqtool
from utils import WriteLine2JSON


def RemoveDuplicatesInList(mylst):
    result = dict((x[0], x) for x in mylst).values()
    return result

def GenrIndexOfTerm(docs):
    term_index = {}
    for d in docs:
        doc_id = d[0]
        terms = d[1]
        term_freqs = freqtool.GetWordFreq(terms)
        max_freq = max(term_freqs.values())

        for w in terms:
            term_index.setdefault(w, [])
            tf_norm = term_freqs[w] / max_freq  # normalized term freq
            term_index[w].append([doc_id, tf_norm])

    return term_index

def GenrInvertedIndex(docs):
    term_indexes = GenrIndexOfTerm(docs)  # {word : (docID, term_freq (with noramlization)}

    inverted_index = []
    total_docs = len(docs)
    for word, index in term_indexes.items():  # data -> (docID, tf_norm)
        unique_index = [ e for e in RemoveDuplicatesInList(index) ]
        df = len(unique_index)  # doc freq
        idf = log(total_docs / df, 10)  # inverse doc freq

        for idx in unique_index:
            idx[1] = idx[1] * idf  # word_weight = tf * idf

        inverted_index.append((word, df, unique_index))

    return inverted_index
# GenrInvertedIndex

def Write2JSON(data):
    with open('log/index.txt', 'w') as fp:
        for line in data:
            json.dump(line, fp)
            fp.write('\n')


if __name__ == "__main__":
    with open('log/corpus.txt', 'r') as fp:
        docs = [json.loads(line) for line in fp.readlines()]
        inverted_index = GenrInvertedIndex(docs)
        WriteLine2JSON('log/index.txt', inverted_index)



