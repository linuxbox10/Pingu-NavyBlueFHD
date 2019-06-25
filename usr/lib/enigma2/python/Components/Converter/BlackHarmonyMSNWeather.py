# -*- coding: utf-8 -*-
#
# j00zek: this file is just to avoid GS-es, when msn weather plugin not installed
#  
from Components.Converter.Converter import Converter
from Components.Element import cached

class fakeConverterMSNWaether(Converter, object):
	def __init__(self, type): Converter.__init__(self, type)
	def getIndex(self, key): return None
	def getText(self): return ""
	text = property(getText)
	def getIconFilename(self): return ""
	iconfilename = property(getIconFilename)

try:
    from Components.Converter.MSNWeather import MSNWeather as BlackHarmonyMSNWeather
except Exception:
    BlackHarmonyMSNWeather = fakeConverterMSNWaether  