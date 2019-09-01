# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.lang import _
from anki.hooks import addHook, wrap
from aqt.reviewer import Reviewer
from aqt.qt import *

from .const import ADDON_NAME, ANKI21
from .config import Config
from .callbacks import Callback
from .menuopt import Menu
from .const import *


class KanjiDoodle:
    config=Config(ADDON_NAME)
    state=None

    def __init__(self, web, parent=None):
        self.web=web
        self.parent=parent
        addHook("showQuestion", self.onShowQuestion)
        addHook("showAnswer", self.onShowAnswer)
        addHook(ADDON_NAME+".configLoaded", self.onConfigLoaded)
        # addHook(ADDON_NAME+".configUpdated", self.configUpdated)

    def onConfigLoaded(self):
        if not self.state:
            self.state=Menu(self.config)
        self.setupCallbacks()

    def setupCallbacks(self):
        self.tsCallback=Callback(self.web,self.parent)
        if ANKI21:
            self.loadUserScript()
        else:
            self.addCallback=self.web.page().mainFrame().addToJavaScriptWindowObject
        self.eval=self.web.eval

    def loadUserScript(self):
        self.web.page()._channel.registerObject("tsCallback",self.tsCallback)
        js = QFile(':/qtwebchannel/qwebchannel.js')
        assert js.open(QIODevice.ReadOnly)
        js = bytes(js.readAll()).decode('utf-8')

        script=QWebEngineScript()
        script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setName("qwebchannel.js");
        script.setRunsOnSubFrames(False)

        # TODO: fix channel error
        # Uncaught TypeError: channel.execCallbacks[message.id]
        # is not a function
        script.setSourceCode(js+'''
var tsCallback;
var chooseColor;
var chooseWidth;
var saveCanvas;
var tooltip;
var signal;
new QWebChannel(qt.webChannelTransport, function(channel) {
    try{
        tsCallback=channel.objects.tsCallback;
        chooseColor=channel.objects.tsCallback.chooseColor;
        chooseWidth=channel.objects.tsCallback.chooseWidth;
        saveCanvas=channel.objects.tsCallback.saveCanvas;
        tooltip=channel.objects.tsCallback.tooltip;
        signal=channel.objects.tsCallback.signal;
    }catch(TypeError){;}
});
        ''')
        self.web.page().profile().scripts().insert(script)

    def onShowQuestion(self):
        if not ANKI21:
            self.addCallback("tsCallback", self.tsCallback)

        self.eval('clear_canvas(true);')

        if not self.state or self.state.isEnabled():
            op=mw.pm.profile.get('ts_opacity',0.7)
            self.eval("canvas.style.opacity=%s;"%str(op))

            # Hack: toggle on/off to fix canvas blocking
            # text selection on init load
            self.eval('init_visibility(false);init_visibility(true);')
        else:
            self.eval('switch_off_buttons(true);')

    def onShowAnswer(self):
        self.eval('resize();')

    def getBody(self):
        c=mw.pm.profile.get('ts_color','#f0f')
        w=mw.pm.profile.get('ts_width','5')
        tf=self.config.get("live_update")
        q="true" if tf else "false"
        return """
<style>%s</style>%s
<script>%s
var live_update=%s;
var ts_color='%s';
var ts_width='%s';
var pen_width='%s';
%s</script>
"""%(CSS,HTML,DEVICE,q,c,w,w,JS)
