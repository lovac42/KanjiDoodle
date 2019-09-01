# -*- coding: utf-8 -*-
# Copyright (C) 2019 Lovac42
# Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
# Support: https://github.com/lovac42/KanjiDoodle
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


ADDON_NAME='KanjiDoodle'

from anki import version

from .utils import readFile

CCBC=version.endswith("ccbc")

ANKI21=version.startswith("2.1") and not CCBC


if ANKI21:
    DEVICE="const DEVICE='pointer';"
else:
    DEVICE="const DEVICE='mouse';"


JS=readFile('web/canvas.js')

CSS=readFile('web/canvas.css')

HTML=readFile('web/canvas.html')

