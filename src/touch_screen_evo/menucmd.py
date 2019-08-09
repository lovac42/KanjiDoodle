# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.lang import _

from .forms import getfield
from .utils import saveCanvasAsPNG


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
    ts_width=mw.pm.profile.get('ts_width',5)
    val,ok=QInputDialog.getDouble(mw,
        "Canvas Pen Size","Enter the width:",
        ts_width,min=0.1,max=250
    )
    if ok:
        val=max(0.1,val)
        mw.pm.profile['ts_width']=val
        if mw.state=='review':
            mw.reviewer.web.eval("ts_width='%s';update_pen_settings();"%val)

def chooseOpacity():
    ts_opacity=mw.pm.profile.get('ts_opacity',0.7)
    val,ok=QInputDialog.getInt(
        mw,"Canvas Opacity Settings",
        "Enter the opacity (0 = transparent, 100 = opaque):",
        100*ts_opacity,0,100,step=5
    )
    if ok:
        op=val/100.0
        mw.pm.profile['ts_opacity']=op
        if mw.state=='review':
            mw.reviewer.web.eval("canvas.style.opacity=%s;"%str(op))

def chooseSaveField(data):
    card=mw.reviewer.card
    if card:
        diag=QDialog(mw)
        form=getfield.Ui_Dialog()
        form.setupUi(diag)
        fields=[f['name'] for f in card.model()['flds']]
        form.fields.addItems(fields)
        diag.show()
        #If errors occur on linux, see old bug (qt4.8.4 or below)
        #https://bugreports.qt-project.org/browse/QTBUG-1894
        form.fields.showPopup()
        if diag.exec_():
            fieldName=fields[form.fields.currentIndex()]
            saveCanvasAsPNG(card,fieldName,data)
