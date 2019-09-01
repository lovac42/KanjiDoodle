# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from aqt.webview import AnkiWebView
from aqt.utils import shortcut
from anki.lang import _

from .main import KanjiDoodle

web=AnkiWebView()
web.setWindowTitle(_("Kanji Doodle"))
web.resize(500, 300)

def showEditorFrame(editor):
    if web.isVisible():
        return
    doo=KanjiDoodle(web,editor)
    html=doo.getBody()
    html+="<style>body{background-color:white;}</style>"
    web.stdHtml(html)
    doo.setupCallbacks()
    doo.onShowQuestion()
    web.eval('init_visibility(false);')
    web.show()


def onEditor20(editor):
    print("on edit")
    editor._addButton("kanji-doodle",
        lambda:showEditorFrame(editor),
        "", shortcut(_("Kanji Doodle")),
        text=_(u"画"), native=True, canDisable=False)
# The pen icon doesn't show up well, so I'm using kanji.

def onEditor21(righttopbtns, editor):
    editor._links["kdoodle"]=showEditorFrame
    righttopbtns.append('''<button tabindex=-1 class=linkb 
title="kanji-doodle" type="button"
onclick="pycmd('kdoodle');return false;">
<div style="display:inline-block; font-size:24px;"
class="topbut">✍</div></button>''')
    return righttopbtns

