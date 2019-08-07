# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw
from aqt.qt import *

from .menucmd import chooseColor, chooseWidth, chooseSaveField


class Callback(QObject):
    @pyqtSlot()
    def chooseColor(self):
        chooseColor()

    @pyqtSlot()
    def chooseWidth(self):
        chooseWidth()

    @pyqtSlot(str)
    def saveCanvas(self, data):
        chooseSaveField(data)
