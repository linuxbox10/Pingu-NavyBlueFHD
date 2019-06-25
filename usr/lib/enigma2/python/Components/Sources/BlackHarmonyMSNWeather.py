# -*- coding: utf-8 -*-
#
# j00zek: this file is just to avoid GS-es, when msn weather plugin not installed
# 

import time
from Source import Source
    
class fakeSourcesMSNWaether(Source):

    def __init__(self): Source.__init__(self)
    def callbackAllIconsDownloaded(self): pass
    def getCity(self): return _("n/a")
    def getThingSpeakItems(self): return {}
    def getWebhourlyItems(self): return {}
    def getWebDailyItems(self): return {}
    def getObservationPoint(self): return _("n/a")
    def getObservationTime(self): return _("n/a")
    def getTemperature_Heigh(self, key): return _("n/a")
    def getTemperature_Low(self, key): return _("n/a")
    def getTemperature_Heigh_Low(self, key): return _("n/a")        
    def getTemperature_Text(self, key): return _("n/a")
    def getTemperature_Current(self): return _("n/a")
    def getFeelslike(self): return _("n/a")
    def getHumidity(self): return _("n/a")
    def getWinddisplay(self): return _("n/a")
    def getWeekday(self, key, short): return _("n/a")
    def getDate(self, key): return _("n/a")
    def getWeatherIconFilename(self, key): return ""
    def getCode(self, key): return ""
    def destroy(self): Source.destroy(self)
    def getWebCurrentItems(self): return {}

try:
    from Components.Sources.MSNWeatherNP import MSNWeatherNP as BlackHarmonyMSNWeather
except Exception:
    BlackHarmonyMSNWeather = fakeSourcesMSNWaether 
