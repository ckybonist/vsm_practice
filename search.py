#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from math import log, sqrt

import freqtool


"""

  Note: the form of vector in here is a
        dict object { term(key) : weight(value) }
"""


def ComputeVectorLength(vec):
    tmp = sum([n**2 for n in vec])
    return sqrt(tmp)

def FindMatchInTwoVectors(query_vec, doc_vec):
    return set(query_vec).intersection(doc_vec)

def DotProduct(v1, v2):
    match = FindMatchInTwoVectors(v1, v2)  # match terms
    result = sum([v1[t] * v2[t] for t in match])
    return result

def ComputeCosine(query_vec, doc_vec):
    "Compute similarity of two vectors"
    qd_inner = DotProduct(query_vec, doc_vec)
    q_len = ComputeVectorLength(query_vec.values())
    d_len = ComputeVectorLength(doc_vec.values())
    cosine = 0
    if q_len * d_len != 0:
        cosine = qd_inner / (q_len * d_len)
    return cosine

def LoadInvertedIndex():
    inverted_index = dict()
    with open('log/index.txt', 'r') as fp:
        for line in fp.readlines():
            record = json.loads(line)
            term = record[0]
            doc_freq = record[1]
            weights_of_docs = record[2]
            inverted_index[term] = (doc_freq,
                                    {d : w for d, w in weights_of_docs})

    return inverted_index

def CreateEachDocVectors(inverted_index):
    docs = {}
    with open('log/corpus.txt', 'r') as fp:
        for line in fp.readlines():
            record = json.loads(line)
            doc_id = record[0]
            terms = set(record[1])
            docs[doc_id] = terms

    result = {}
    for doc_id, terms in docs.items():
        # vec -> [(term, weight), ...]
        vec = {t : inverted_index[t][1][doc_id]
               for t in terms}
        vec_len = ComputeVectorLength([weight for weight in vec.values()])
        result[doc_id] = (vec, vec_len)
    return result

def CreateQueryVector(query, total_doc, inverted_index):
    term_freqs = freqtool.GetWordFreq(query)
    max_freq = max(term_freqs.values())
    qvec = {}
    for t in query:
        idf = log(total_doc / inverted_index[t][0], 10)
        tf_norm = term_freqs[t] / max_freq  # normalize term-freq
        weight = tf_norm * idf
        #weight = term_freqs[t] * idf
        qvec[t] = weight
    return qvec

def Ranking(query, inverted_index):
    doc_vecs = CreateEachDocVectors(inverted_index)  # {doc-id : ((doc vec, vec length)}

    total_doc = len(doc_vecs)
    qvec = CreateQueryVector(query, total_doc, inverted_index)

    similarity = [(doc_id, ComputeCosine(qvec, vec_info[0]))
                   for doc_id, vec_info in doc_vecs.items()]
    similarity.sort(key = lambda tup: tup[1],
                    reverse = True)
    return similarity

def ShowRanking(result):
    print('\n')
    rank = 1
    for e in result:
        doc_id = e[0]
        cos = e[1]
        if cos > 0:
            cos = "{:.4f}".format(e[1])
            print("Rank {0} :\n   {1}\n   similarity with query => {2}\n".format(rank, doc_id, cos))
            rank = rank + 1
    print("\nTotal result : {0}".format(rank - 1))

def FilterQuery(query, corpus):
    query = query.split()
    return filter(lambda t: t in corpus, query)

def CheckQueryIsValid(query, corpus):
    " Filter query string to a list, if every word in this list \
      not appear in our corpus will get a empty list and exit the program. \
      Else, return the valid list and do the ranking process. "
    query = list(FilterQuery(query, corpus))
    if not query:
        print("Thers is no possible result for this query")
        sys.exit(1)
    else:
        return query


if __name__ == "__main__":
    query = input("Input query terms (seperate by space) : ");

    inverted_index = LoadInvertedIndex()  # {term : (df, {doc-id : weight, ...})}
    corpus = inverted_index.keys()
    query = CheckQueryIsValid(query, corpus)

    result = Ranking(query, inverted_index)
    ShowRanking(result)


# End of File
