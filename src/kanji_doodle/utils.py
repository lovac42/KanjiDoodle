# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os, sys
import base64
from aqt import mw
from anki.utils import intTime

PY2=sys.version_info[0]<3
if PY2:
    import io
    open=io.open


def readFile(fname):
    addon,_=os.path.split(__file__)
    path=os.path.abspath(os.path.join(addon,fname))
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

def importDataURL(txt):
    b64dat=txt[22:].strip()
    dat=base64.b64decode(b64dat)
    fname=u"%s%d.png"%("canvas",intTime())
    return mw.col.media.writeData(fname,dat)

def saveCanvasAsPNG(data):
    ts_opacity=mw.pm.profile.get('ts_opacity',0.7)
    fileName=importDataURL(data)
    return '''
<img src="%s" style="opacity:%s;">
'''%(fileName,ts_opacity)
