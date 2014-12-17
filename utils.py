#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def WriteLine2JSON(outfile, obj):
    with open(outfile, 'w') as fp:
        for e in obj:
            json.dump(e, fp)
            fp.write('\n')
