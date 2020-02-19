# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from anki.lang import _

from .forms import getfield, getnumber, getcolor
from .utils import saveCanvasAsPNG


def chooseColor(web):
    def liveColor(qcolor):
        if qcolor.isValid():
            cor=qcolor.name()
            mw.pm.profile['ts_color']=cor
            web.eval("ts_color='%s';update_pen_settings();"%cor)

    diag=QDialog(web)
    form=getcolor.Ui_Dialog()
    form.setupUi(diag)
    cor=mw.pm.profile.get('ts_color',"#f0f")
    form.color.setCurrentColor(QColor(cor))
    form.color.currentColorChanged.connect(liveColor)
    diag.show()


def chooseWidth(web):
    def changeWidth(val):
        mw.pm.profile['ts_width']=val
        web.eval("ts_width='%s';update_pen_settings();"%val)

    ts_width=mw.pm.profile.get('ts_width',5)
    diag=QDialog(web)
    form=getnumber.Ui_Dialog()
    form.setupUi(diag)
    diag.show()
    form.input.setValue(ts_width)
    form.input.valueChanged.connect(
        lambda: changeWidth(form.input.value())
    )


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
        imgTag=saveCanvasAsPNG(data)
        n=card.note()
        fn=fields[form.fields.currentIndex()]
        n[fn]+=imgTag
        n.flush()
        tooltip("Doodle appended to %s"%fn,1500)

        #Force refresh w/o loosing card
        mw.reviewer.card=mw.col.getCard(card.id)
        mw.reviewer.card.startTimer()
        mw.reviewer._showQuestion()


def saveFieldToEditor(data, web, editor):
    imgTag=saveCanvasAsPNG(data)
    fld=editor.currentField
    editor.note.fields[fld]+=imgTag
    editor.loadNote()
    # focus field so it's saved
    editor.web.setFocus()
    editor.web.eval("focusField(%d);"%fld)
    web.close()
