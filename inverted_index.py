#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from math import log

import utils
import freqtool


def RemoveDuplicatesInList(mylst):
    result = dict((x[0], x) for x in mylst).values()
    return result

def GenrIndexOfTerm(doc_index):
    term_index = dict()
    for doc_id, terms in doc_index.items():
        term_freqs = freqtool.GetWordFreq(terms)
        max_freq = max(term_freqs.values())

        for w in terms:
            term_index.setdefault(w, dict())
            tf_norm = term_freqs[w] / max_freq  # normalized term freq
            term_index[w][doc_id] = tf_norm
    return term_index

def GenrInvertedIndex(docs):
    term_indexes = GenrIndexOfTerm(docs)  # {term : (docID, term_freq (normalized)}
    inverted_index = dict()
    total_docs = len(docs)
    for term, index in term_indexes.items():  # data -> (docID, tf_norm)
        unique_index = index

        df = len(unique_index)  # doc freq
        idf = log(total_docs / df, 10)  # inverse doc freq
        for doc_id in unique_index.keys():
            tf = unique_index[doc_id]
            unique_index[doc_id] = tf * idf
        inverted_index[term] = (df, unique_index)
    return inverted_index
# GenrInvertedIndex


if __name__ == "__main__":
    with open('log/corpus.txt', 'r') as fp:
        doc_index = json.load(fp)

    inverted_index = GenrInvertedIndex(doc_index)
    utils.WriteJSONObj('log/index.txt', inverted_index)

# End of File
