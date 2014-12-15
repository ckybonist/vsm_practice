#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

def GetWordFreq(words):
    word_freq = defaultdict(int)
    for w in words:
        word_freq[w] = word_freq[w] + 1
    return word_freq
