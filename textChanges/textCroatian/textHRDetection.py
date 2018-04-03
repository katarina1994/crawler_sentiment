#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 25. ozu 2018.

@author: Katarina123
'''

"""
from text_hr.detect import WordTypeRecognizerExample
import text_hr.base


def test_it(word_list, wt_filter=None, level=1):
    wdh = WordTypeRecognizerExample(word_list, silent=True)
    if not wt_filter is None:
        wdh.detect(wt_filter=wt_filter, level=level)  # e.g. wt_filter=["N"]
    else:
        wdh.detect(level=level)  # all word types
    lines_file = LinesFile()
    wdh.dump_result(lines_file) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    print "\n".join(lines_file.lines)
    return wdh

class LinesFile(object):
    def __init__(self):
        self.lines = []
    def write(self, s):
        self.lines.append(repr(s.rstrip()))

word_list = [
  u"Katarinom   1"
]

wdh = test_it(word_list, level=1)
"""


