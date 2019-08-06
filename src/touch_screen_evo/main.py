# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.lang import _
from anki.hooks import addHook, wrap
from anki.template import Template
from aqt.reviewer import Reviewer
from aqt.qt import *

from .const import ADDON_NAME
from .config import Config
from .menuopt import Menu
from .const import *


class TouchScreen:
    state=None

    def __init__(self):
        addHook("showQuestion", self.onShowQuestion)
        addHook(ADDON_NAME+".configLoaded", self.onConfigLoaded)
        # addHook(ADDON_NAME+".configUpdated", self.configUpdated)
        self.config=Config(ADDON_NAME)

    def onConfigLoaded(self):
        if not self.state:
            self.state=Menu(self.config)

    def onShowQuestion(self):
        if self.state.isEnabled():
            mw.reviewer.web.eval('clear_canvas();')
            op=mw.pm.profile.get('ts_opacity',0.7)
            mw.reviewer.web.eval("canvas.style.opacity=%s;"%str(op))

            #hack to fix canvas blocking text selection on init load
            mw.reviewer.web.eval('switch_visibility();')
            mw.reviewer.web.eval('switch_visibility();')
        else:
            mw.reviewer.web.eval('switch_off_buttons(true);')

ts=TouchScreen()



def revHtml(rev, _old):
    body=_old(rev)
    c="var ts_color='%s';"%mw.pm.profile.get('ts_color','#f0f')
    w="var ts_width='%s';"%mw.pm.profile.get('ts_width','5')
    body="""
<style>%s</style>%s%s
<script>%s%s%s%s</script>
"""%(CSS,HTML,body,DEVICE,c,w,JS)
    return body

Reviewer.revHtml = wrap(Reviewer.revHtml, revHtml, 'around')

