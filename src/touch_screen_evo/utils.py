# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os
import base64
from anki.utils import intTime
from aqt import mw


def readFile(fname):
    addon,_=os.path.split(__file__)
    path=os.path.abspath(os.path.join(addon,fname))
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

def importDataURL(txt):
    b64dat=txt[22:].strip()
    dat=base64.b64decode(b64dat,validate=True)
    fname="%s%d.png"%("canvas",intTime())
    return mw.col.media.writeData(fname,dat)

def saveCanvasAsPNG(card, field, data):
    fileName=importDataURL(data)
    n=card.note()
    n[field]+='<img src="%s">'%fileName
    n.flush()
    #Force refresh w/o loosing card
    mw.reviewer.card=mw.col.getCard(card.id)
    mw.reviewer.card.startTimer()
    mw.reviewer._showQuestion()
