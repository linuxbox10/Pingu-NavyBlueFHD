# -*- coding: utf-8 -*-
#
# WeatherPlugin E2
#
# Coded by Dr.Best (c) 2012-2013
# modified by j00zek 2018
# Support: www.dreambox-tools.info
# E-Mail: dr.best@dreambox-tools.info
#
# This plugin is open source but it is NOT free software.
#
# This plugin may only be distributed to and executed on hardware which
# is licensed by Dream Multimedia GmbH.
# In other words:
# It's NOT allowed to distribute any parts of this plugin or its source code in ANY way
# to hardware which is NOT licensed by Dream Multimedia GmbH.
# It's NOT allowed to execute this plugin and its source code or even parts of it in ANY way
# on hardware which is NOT licensed by Dream Multimedia GmbH.
#
# If you want to use or modify the code or parts of it,
# you have to keep MY license and inform me about the modifications by mail.
#

from Components.config import config
from Plugins.Extensions.MSNweather.__init__ import _
from Plugins.Extensions.MSNweather.updater import weathermsn
from Source import Source
import time

class MSNWeatherNP(Source):

    def __init__(self):
        self.DEBUG('MSNWeather(Source) __init__')
        Source.__init__(self)
        #weathermsn.callbacksAllIconsDownloaded.append(self.callbackAllIconsDownloaded)
        weathermsn.callbacks.append(self.refreshCallback)
        weathermsn.getData()

    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNWeatherSource.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )
    
    def getIconPath(self):
        #self.DEBUG('MSNWeather(Source) getThingSpeakItems')
        return weathermsn.weatherData.iconpath
        
    def getThingSpeakItems(self):
        #self.DEBUG('MSNWeather(Source) getThingSpeakItems')
        return weathermsn.weatherData.thingSpeakItems
        
    def getWebCurrentItems(self):
        #self.DEBUG('MSNWeather(Source) getWebCurrentItems')
        return weathermsn.weatherData.WebCurrentItems
        
    def getWebhourlyItems(self):
        #self.DEBUG('MSNWeather(Source) getWebhourlyItems')
        return weathermsn.weatherData.WebhourlyItems
        
    def getWebDailyItems(self):
        #self.DEBUG('MSNWeather(Source) getWebDailyItems')
        return weathermsn.weatherData.WebDailyItems
        
    def refreshCallback(self, result = None, errortext=None):
        self.DEBUG('MSNWeather(Source) refreshCallback')
        self.changed((self.CHANGED_ALL,))
            
    def callbackAllIconsDownloaded(self, result = None, errortext=None):
        self.DEBUG('MSNWeather(Source) callbackAllIconsDownloaded')
        self.changed((self.CHANGED_ALL,))
    
    def getCity(self):
        return weathermsn.weatherData.city
        
    def getObservationPoint(self):
        skey = "-1"
        if weathermsn.weatherData.weatherItems.has_key(skey):
            retVal = weathermsn.weatherData.weatherItems[skey].observationpoint
        else:
            retVal = ''
        self.DEBUG('MSNWeather(Source) getObservationPoint = "%s"' % retVal)
        return retVal
        
    def getObservationTime(self):
        skey = "-1"
        retVal = ''
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            if item.observationtime != "":
                c =  time.strptime(item.observationtime, "%H:%M:%S")
                retVal = time.strftime("%H:%M",c)
        return retVal
        
    def getTemperature_Heigh(self, key):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            highTemp = item.high
            if highTemp != '':
                retVal = "%s°%s" % (highTemp, weathermsn.weatherData.degreetype)
        if retVal == '':
            try:
                if skey == '-1': skey = "0"
                else: skey = str( int(skey) - 1)
                #self.DEBUG('MSNWeather(Source) getTemperature_Heigh skey = "%s"' % skey)
                line = self.getWebDailyItems().get("Record=%s" % skey, [('day=UNKNOWN', '', '', '', '', '', '', '', '')])[0]
                self.DEBUG('MSNWeather(Source) getTemperature_Heigh "Record=%s" = "%s"' % (skey,str(line)))
                retVal = "%s%s" % (line[6].strip(), weathermsn.weatherData.degreetype)
            except Exception as e:
                self.EXCEPTIONDEBUG('MSNWeather(Source) Exception %s' % str(e) )
        self.DEBUG('MSNWeather(Source) getTemperature_Heigh(%s) = "%s"' % (str(key),retVal))
        return retVal
    
    def getTemperature_Low(self, key):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            lowTemp = item.low
            if lowTemp != '':
                retVal = "%s°%s" % (lowTemp, weathermsn.weatherData.degreetype)
        if retVal == '':
            try:
                if skey == '-1': skey = "0"
                else: skey = str( int(skey) - 1)
                #self.DEBUG('MSNWeather(Source) getTemperature_Low skey = "%s"' % skey)
                line = self.getWebDailyItems().get("Record=%s" % skey, [('day=UNKNOWN', '', '', '', '', '', '', '', '')])[0]
                self.DEBUG('MSNWeather(Source) getTemperature_Low "Record=%s" = "%s"' % (skey,str(line)))
                retVal = "%s%s" % (line[7].strip(), weathermsn.weatherData.degreetype)
            except Exception as e:
                self.EXCEPTIONDEBUG('MSNWeather(Source) getTemperature_Low Exception %s' % str(e) )
        self.DEBUG('MSNWeather(Source) getTemperature_Low(%s) = "%s"' % (str(key),retVal))
        return retVal
            
    def getTemperature_Heigh_Low(self, key):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            highTemp = item.high
            lowTemp = item.low
            if highTemp != '' and lowTemp != '':
                retVal = "%s°%s | %s°%s" % (highTemp, weathermsn.weatherData.degreetype, lowTemp, weathermsn.weatherData.degreetype)
        if retVal == '':
            try:
                if skey == '-1': skey = "0"
                else: skey = str( int(skey) - 1)
                #self.DEBUG('MSNWeather(Source) getTemperature_Heigh_Low skey = "%s"' % skey)
                line = self.getWebDailyItems().get("Record=%s" % skey, [('day=UNKNOWN', '', '', '', '', '', '', '', '')])[0]
                self.DEBUG('MSNWeather(Source) getTemperature_Heigh_Low "Record=%s" = "%s"' % (skey,str(line)))
                retVal = "%s%s | %s%s" % (line[6].strip(), weathermsn.weatherData.degreetype, line[7].strip(), weathermsn.weatherData.degreetype)
            except Exception as e:
                self.EXCEPTIONDEBUG('MSNWeather(Source) getTemperature_Heigh_Low Exception %s' % str(e) )
        self.DEBUG('MSNWeather(Source) getTemperature_Heigh_Low(%s) = "%s"' % (str(key),retVal))
        return retVal
        self.DEBUG('MSNWeather(Source) getTemperature_Heigh_Low(%s) = "%s"' % (str(key),retVal))
        return retVal
    
    def getTemperature_Text(self, key):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            if skey == "-1":
                return item.skytext
            else:
                return  item.skytextday
        else:
            return '-?-'
            
    def getTemperature_Current(self):
        retVal = ''
        skey = "-1"
        if weathermsn.weatherData.weatherItems.has_key(skey):
            return "%s°%s" % (weathermsn.weatherData.weatherItems[skey].temperature, weathermsn.weatherData.degreetype)
        else:
            return '-?-'
            
    def getFeelslike(self):
        retVal = ''
        skey = "-1"
        if weathermsn.weatherData.weatherItems.has_key(skey):
            return "%s°%s" % (weathermsn.weatherData.weatherItems[skey].feelslike, weathermsn.weatherData.degreetype)
        else:
            return '-?-'
    
    def getHumidity(self):
        retVal = ''
        skey = "-1"
        if weathermsn.weatherData.weatherItems.has_key(skey):
            return weathermsn.weatherData.weatherItems[skey].humidity
        else:
            return '-?-'
            
    def getWinddisplay(self):
        retVal = ''
        skey = "-1"
        if weathermsn.weatherData.weatherItems.has_key(skey):
            return weathermsn.weatherData.weatherItems[skey].winddisplay
        else:
            return '-?-'
    
    def getWeekday(self, key, short):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            if short:
                return item.shortday
            else:
                return item.day
        else:
            return '-?-'
            
    def getDate(self, key):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            c = time.strptime(item.date,"%Y-%m-%d")
            return time.strftime("%d. %b",c)
        else:
            return '-?-'
            
    def getFullDate(self, key):
        self.DEBUG("MSNWeather(Source).getFullDate(key=%s)" % key)
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            item = weathermsn.weatherData.weatherItems[skey]
            c = time.strptime(item.date,"%Y-%m-%d")
            Day = time.strftime("%d",c)
            weekday = _(item.day)
            Month = _(time.strftime("%b",c)) 
            return str('%s. %s %s' % (weekday, Day, Month))
        else:
            return '-?-'
            
    def getWeatherIconFilename(self, key):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            retVal = weathermsn.weatherData.weatherItems[skey].iconFilename
        if retVal == '':
            try:
                if skey == '-1': skey = "0"
                else: skey = str( int(skey) - 1)
                #self.DEBUG('MSNWeather(Source) getWeatherIconFilename recordID = "%s"' % skey)
                retVal = self.getWebDailyItems().get('WeatherIcon4Record=%s' % skey , '')
                #self.DEBUG(str(self.getWebDailyItems()).replace("'WeatherIcon4Record=","\n'WeatherIcon4Record=").replace("'Record=","\n'Record="))
                if retVal == '':
                    line = self.getWebDailyItems().get("Record=%s" % skey, [('day=UNKNOWN', '', '', '', '', '', '', '', '')])[0]
                    retVal = '/usr/lib/enigma2/python/Plugins/Extensions/WeatherPlugin/icons/%s' % str('%s' % line[3].strip()).split('?')[0].split('/')[-1][:-4]
                    self.DEBUG('MSNWeather(Source) getWeatherIconFilename "Record=%s" = "%s"' % (skey,str(line)))
            except Exception as e:
                self.EXCEPTIONDEBUG('MSNWeather(Source) getWeatherIconFilename Exception %s' % str(e) )
        self.DEBUG('MSNWeather(Source) getWeatherIconFilename(%s) = "%s"' % (str(key),retVal))
        return retVal
            
    def getCode(self, key):
        retVal = ''
        skey = str(key)
        if weathermsn.weatherData.weatherItems.has_key(skey):
            retVal = weathermsn.weatherData.weatherItems[skey].code
        if retVal == '':
            try:
                if skey == '-1': skey = "0"
                else: skey = str( int(skey) - 1)
                #self.DEBUG('MSNWeather(Source) getCode skey = "%s"' % skey)
                line = self.getWebDailyItems().get("Record=%s" % skey, [('day=UNKNOWN', '', '', '', '', '', '', '', '')])[0]
                self.DEBUG('MSNWeather(Source) getCode "Record=%s" = "%s"' % (skey,str(line)))
                #retVal = line[7].strip()
            except Exception as e:
                self.EXCEPTIONDEBUG('MSNWeather(Source) getCode Exception %s' % str(e) )
        self.DEBUG('MSNWeather(Source) getCode(%s) = "%s"' % (str(key),retVal))
        return retVal

    def destroy(self):
        weathermsn.callbacksAllIconsDownloaded.remove(self.callbackAllIconsDownloaded)
        Source.destroy(self)
