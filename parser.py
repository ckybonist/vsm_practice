#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import glob
import argparse
from string import punctuation
import subprocess  # ckip_parser.rb

import utils
from stopwords import stopwords_list


def RemoveStopWords(token_list):
    tmp = [ w for w in token_list
            if w not in stopwords_list ]
    cap = lambda s: s.capitalize()
    cap_stopwords = list(map(cap, stopwords_list))
    return [ w for w in tmp
             if w not in cap_stopwords ]

def RemoveStrPunc(mystr):
    exclude = punctuation
    result = ''.join(ch for ch in mystr
                        if ch not in exclude)
    return result

def Tokenize(mystr):
    strip_str = mystr.strip()
    no_punc_str = RemoveStrPunc(strip_str);
    terms = [ w.lower()
              for w in no_punc_str.split()
              if w.isalpha() ]  #  contain duplicates
    terms = RemoveStopWords(terms)
    terms.sort()
    return terms

def GenrDocIndex(use_ckip):
    if use_ckip:
        try:
            subprocess.check_call(["ruby", "ckip_parser.rb"])
        except subprocess.CalledProcessError:
            print('Error occur when calling sub-process')
            sys.exit(1)
        except OSError:
            print('Executable not found')
            sys.exit(1)

        #TODO : create another thread to
        #       set the name of tmp_file
        tmp_file = 'log/tmp_corpus.txt'
        with open(tmp_file, 'r') as fp:
            doc_index = json.load(fp)
        os.remove(tmp_file)

    else:
        # My personal word segment tool
        doc_index = dict()
        files = glob.glob("docs/*")
        for f in files:
            with open (f, 'r') as input:
                contents = input.read()
                terms = Tokenize(contents)
                doc_index[f] = terms

    utils.WriteJSONObj('log/corpus.txt', doc_index)


if  __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description = 'Parse and filter documents then do word segment')
    arg_parser.add_argument('--use-ckip',
                            help = 'if your documents contain cjk fonts,\
                                    provide this option to use CKIP word segmentation tool',
                            dest = 'use_ckip',
                            action = 'store_true')
    arg_parser.set_defaults(use_ckip = False)
    args = arg_parser.parse_args()

    GenrDocIndex(args.use_ckip)

# End of File
