# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os

def readFile(fname):
    addon,_=os.path.split(__file__)
    path=os.path.abspath(os.path.join(addon,fname))
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
