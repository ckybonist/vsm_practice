#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from math import log

import freqtool


def GenrInvertedIndex(docs):
    intermediate_result = {}  # {word : (docID, term_freq (with noramlization)}
    for d in docs:
        docID = d[0]
        terms = d[1]
        #term_freqs = defaultdict(int)
        #for w in words:
        #    term_freqs[w] = term_freqs[w] + 1
        term_freqs = freqtool.GetWordFreq(terms)
        max_freq = max(term_freqs.values())

        for w in terms:
            tf_norm = float(term_freqs[w]) / float(max_freq)  # normalized term freq
            #tf_norm = float(term_freqs[w])  # non-norm, it's for debug
            intermediate_result.setdefault(w, [])
            intermediate_result[w].append([docID, tf_norm])

    final_result = []
    total_docs = len(docs)
    for word, index in intermediate_result.items():  # data -> (docID, tf_norm)
        unique_index = dict((x[0], x) for x in index).values()  # remove duplicate data
        unique_index = [e for e in unique_index]

        df = len(unique_index)  # doc freq
        idf = log(float(total_docs) / float(df), 10)  # inverse doc freq

        for idx in unique_index:
            idx[1] = idx[1] * idf  # word_weight = tf * idf

        final_result.append((word, df, unique_index))

    return final_result
# GenrInvertedIndex

def WriteJSON(data):
    with open('log/index.txt', 'w') as fp:
        for line in data:
            json.dump(line, fp)
            fp.write('\n')


if __name__ == "__main__":
    with open('log/corpus.txt', 'r') as fp:
        docs = [json.loads(l) for l in fp.readlines()]
        inverted_index = GenrInvertedIndex(docs)
        WriteJSON(inverted_index)



