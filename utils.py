#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

def WriteLine2JSON(outfile, obj):
    with open(outfile, 'w') as fp:
        for e in obj:
            json.dump(e, fp)
            fp.write('\n')

def WriteJSONObj(outfile, obj):
    with open(outfile, 'w') as fp:
        json.dump(obj,
                  fp,
                  ensure_ascii = False,
                  indent = 2)
