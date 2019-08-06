# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.lang import _


def chooseColor():
    cor=mw.pm.profile.get('ts_color',"#f0f")
    qcolor_old=QColor(cor)
    qcolor=QColorDialog.getColor(qcolor_old)
    if qcolor.isValid():
        cor=qcolor.name()
        mw.pm.profile['ts_color']=cor
        if mw.state=='review':
            mw.reviewer.web.eval("ts_color='%s';update_pen_settings();"%cor)

def chooseWidth():
    width=mw.pm.profile.get('ts_width',5)
    val,ok=QInputDialog.getDouble(mw,"Touch Screen","Enter the width:",width)
    if ok:
        mw.pm.profile['ts_width']=val
        if mw.state=='review':
            mw.reviewer.web.eval("ts_width='%s';update_pen_settings();"%val)

def chooseOpacity():
    ts_opacity=mw.pm.profile.get('ts_opacity',0.7)
    val,ok=QInputDialog.getDouble(
        mw,"Touch Screen",
        "Enter the opacity (100 = transparent, 0 = opaque):",
        100*ts_opacity,0,100,2
    )
    if ok:
        op=val/100.0
        mw.pm.profile['ts_opacity']=op
        if mw.state=='review':
            mw.reviewer.web.eval("canvas.style.opacity=%s;"%str(op))
