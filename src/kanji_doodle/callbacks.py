# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from aqt.editor import Editor
from anki.hooks import runHook

from .menucmd import chooseColor, chooseWidth, chooseSaveField, saveFieldToEditor
from .const import ADDON_NAME


class Callback(QObject):

    def __init__(self, web, parent=None):
        QObject.__init__(self)
        self.web=web
        self.parent=parent

    @pyqtSlot()
    def chooseColor(self):
        chooseColor(self.web)

    @pyqtSlot()
    def chooseWidth(self):
        chooseWidth(self.web)

    @pyqtSlot(str)
    def saveCanvas(self, data):
        if isinstance(self.parent,Editor):
            saveFieldToEditor(data,self.web,self.parent)
        elif not self.parent and mw.state=='review':
            chooseSaveField(data)

    @pyqtSlot(str)
    def tooltip(self, msg):
        tooltip(msg)

    @pyqtSlot(bool)
    def signal(self, tf):
        "Signal timer addons to pause while drawing"
        runHook(ADDON_NAME+".draw",tf)
