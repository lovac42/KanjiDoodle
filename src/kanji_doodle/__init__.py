# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.hooks import wrap, addHook
from aqt.reviewer import Reviewer

from .const import CCBC, ANKI20
from .main import KanjiDoodle
from .editor import onEditor20, onEditor21


if CCBC or ANKI20:
    addHook("setupEditorButtons", onEditor20)
else:
    addHook("setupEditorButtons", onEditor21)


doodle=KanjiDoodle(mw.reviewer.web)


def onProfile():
    Reviewer._revHtml += doodle.getBody()


def wrap_revHtml(rev, _old):
    return _old(rev) + doodle.getBody()


if ANKI20:
    addHook('profileLoaded', onProfile)
else:
    Reviewer.revHtml = wrap(Reviewer.revHtml, wrap_revHtml, 'around')


# Compatibility with NightMode:
# NM uses decorators to wrap revHtml which screws up other addons that wrap the same parts of Anki. No other method is as effective as ensuring this addon is loaded first before NM gets loaded. They either screw up the JS or causes NM colors to be locked to the reviewer. Rename NM with a 'z' prefix to ensure it is loaded last or rename this addon with an 'a' prefix to ensure it is loaded first.

