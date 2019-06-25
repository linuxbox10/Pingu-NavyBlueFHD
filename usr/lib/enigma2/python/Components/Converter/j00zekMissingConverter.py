# -*- coding: utf-8 -*-
#
# j00zek: this file can be used to avoid GS-es on missing components
#  
from Components.Converter.Converter import Converter

class j00zekMissingConverter(Converter, object):
	def __init__(self, type): Converter.__init__(self, type)
	def getIndex(self, key): return None
	def getText(self): return "N.INST"
	text = property(getText)
	def getIconFilename(self): return ""
	iconfilename = property(getIconFilename)
