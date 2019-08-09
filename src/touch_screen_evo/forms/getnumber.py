# -*- coding: utf-8 -*-
from anki.lang import _

try:
    from PyQt4 import QtCore, QtGui as QtWidgets
except:
    from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(150, 40)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.input = QtWidgets.QDoubleSpinBox(Dialog)
        self.input.setMinimum(0.00)
        self.input.setMaximum(250.00)
        self.gridLayout.addWidget(self.input, 0, 1, 1, 1)

        self.upArrow = QtWidgets.QPushButton(Dialog)
        self.upArrow.clicked.connect(self.inc)
        self.gridLayout.addWidget(self.upArrow, 1, 0, 1, 1)
        self.dnArrow = QtWidgets.QPushButton(Dialog)
        self.dnArrow.clicked.connect(self.dec)
        self.gridLayout.addWidget(self.dnArrow, 1, 1, 1, 1)

        self.horizontalLayout.addLayout(self.gridLayout)
        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_("Doodle"))
        self.label.setText(_("Pen Size:"))
        self.upArrow.setText(_("▲"))
        self.dnArrow.setText(_("▼"))

    def inc(self):
        v=self.input.value()
        self.input.setValue(v+1)

    def dec(self):
        v=self.input.value()
        self.input.setValue(v-1)
