# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.lang import _
from anki.hooks import addHook
from aqt.qt import *

from .menucmd import chooseColor, chooseWidth, chooseOpacity


class Menu:
    def __init__(self, config):
        addHook("profileLoaded", self.initState)
        self.config=config
        self.setupMenu()

    def setupMenu(self):
        menu=None
        for a in mw.form.menubar.actions():
            if '&View' == a.text():
                menu=a.menu()
                break
        if not menu:
            menu=mw.form.menubar.addMenu('&View')
        subMenu=QMenu('&Touchscreen',menu)

        self.mSwitch=QAction(_('&Enable Touch Screen'),mw,checkable=True)
        hotkey=self.config.get('hotkey')
        if hotkey:
            self.mSwitch.setShortcut(QKeySequence(hotkey))
        self.mSwitch.triggered.connect(self.toggleState)

        self.mOpacity = QAction(_('Set Canvas &Opacity'),mw)
        self.mOpacity.triggered.connect(chooseOpacity)

        subMenu.addAction(self.mSwitch)
        subMenu.addSeparator()
        subMenu.addAction(self.mOpacity)
        menu.addMenu(subMenu)


    def toggleState(self):
        state=self.mSwitch.isChecked()
        mw.pm.profile['ts_state_on']=state
        self.mOpacity.setEnabled(state)
        if mw.state=='review':
            s='false' if state else 'true'
            mw.reviewer.web.eval('init_visibility(false);switch_off_buttons(%s);'%s)


    def initState(self):
        state=mw.pm.profile.get('ts_state_on',True)
        self.mSwitch.setChecked(state)
        self.mOpacity.setEnabled(state)

    def isEnabled(self):
        return self.mSwitch.isChecked()

