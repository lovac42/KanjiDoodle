# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from anki.lang import _
from ..const import ANKI21

if ANKI21:
    from PyQt5 import QtCore, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 200)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.color = QtWidgets.QColorDialog(Dialog)
        self.color.setWindowFlags(QtCore.Qt.Widget)
        self.color.rejected.connect(Dialog.reject)
        self.color.setOptions(
            QtWidgets.QColorDialog.DontUseNativeDialog |
            QtWidgets.QColorDialog.NoButtons
        )

        self.horizontalLayout.addWidget(self.color)
        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_("Doodle"))
