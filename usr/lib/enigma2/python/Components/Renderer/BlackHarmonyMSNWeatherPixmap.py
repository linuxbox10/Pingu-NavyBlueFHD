# -*- coding: utf-8 -*-
#
# j00zek: this file is just to avoid GS-es, when weather plugin not installed
#

from Renderer import Renderer
from enigma import ePixmap
from Components.AVSwitch import AVSwitch
from enigma import eEnv, ePicLoad, eRect, eSize, gPixmapPtr

class fakeRendererMSNWeatherPixmap(Renderer):
	def __init__(self): Renderer.__init__(self)
	GUI_WIDGET = ePixmap

try:
    from Components.Renderer.MSNWeatherPixmapNP import MSNWeatherPixmapNP as BlackHarmonyMSNWeatherPixmap
except Exception:
    BlackHarmonyMSNWeatherPixmap = fakeRendererMSNWeatherPixmap  