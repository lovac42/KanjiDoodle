# -*- coding: utf-8 -*-
from anki.lang import _

try:
    from PyQt4 import QtCore, QtGui as QtWidgets
except:
    from PyQt5 import QtCore, QtWidgets


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
