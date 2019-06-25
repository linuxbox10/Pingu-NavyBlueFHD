# -*- coding: utf-8 -*- 
#
# j00zek: this file is just to avoid GS-es, when weather plugin not installed
#

class fakeComponentsMSNWaether:
    def  __init__(self):
        pass
      
    def OK(self):
        return False 
        
class FakeWeatherMSN:
    def __init__(self):
        self.weatherData = fakeComponentsMSNWaether()
        self.callbacks = [ ]
        self.callbacksAllIconsDownloaded = []

try:
    from Components.WeatherMSN import WeatherMSN
    weathermsn = WeatherMSN()
except Exception:
    weathermsn = FakeWeatherMSN()

