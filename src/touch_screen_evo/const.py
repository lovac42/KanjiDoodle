# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/TouchScreenEvo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

ADDON_NAME='TouchScreenEvo'

from anki import version

from .utils import readFile

CCBC=version.endswith("ccbc")

if CCBC:
    DEVICE="const DEVICE='mouse';"
else:
    DEVICE="const DEVICE='pointer';"


JS=readFile('web/canvas.js')

CSS=readFile('web/canvas.css')

HTML=readFile('web/canvas.html')

