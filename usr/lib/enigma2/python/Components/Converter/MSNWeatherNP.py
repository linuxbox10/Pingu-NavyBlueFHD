# -*- coding: utf-8 -*-
#
# WeatherPlugin E2
#
# Coded by Dr.Best (c) 2012-2013
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
from Components.Converter.Converter import Converter
from Components.Element import cached
from os import path

class MSNWeatherNP(Converter, object):

    CURRENT = -1
    DAY1 = 1
    DAY2 = 2
    DAY3 = 3
    DAY4 = 4
    DAY5 = 5    
    DAY6 = 6
    DAY7 = 7
    DAY8 = 8
    DAY9 = 9
    DAY10 = 10
    DAY11 = 11
    DAY12 = 12
    DAY13 = 13
    DAY14 = 14
    CITY = 15
    TEMPERATURE_HEIGH = 16
    TEMPERATURE_LOW = 17
    TEMPERATURE_TEXT = 18
    TEMPERATURE_CURRENT = 19
    WEEKDAY = 20
    WEEKSHORTDAY = 21
    DATE = 22
    OBSERVATIONTIME = 23
    OBSERVATIONPOINT = 24
    FEELSLIKE = 25
    HUMIDITY = 26
    WINDDISPLAY = 27
    ICON = 28
    TEMPERATURE_HEIGH_LOW = 29
    CODE = 30
    PATH = 31
    FULLDATE = 32

    def __init__(self, type):
        Converter.__init__(self, type)
        self.index = None
        self.mode = None
        self.path = None
        self.extension = None
        if type == "city": self.mode = self.CITY
        elif type == "observationtime": self.mode = self.OBSERVATIONTIME
        elif type == "observationpoint": self.mode = self.OBSERVATIONPOINT
        elif type == "temperature_current": self.mode = self.TEMPERATURE_CURRENT
        elif type == "feelslike": self.mode = self.FEELSLIKE
        elif type == "humidity": self.mode = self.HUMIDITY
        elif type == "winddisplay": self.mode = self.WINDDISPLAY
        else:
            if type.find("weathericon") != -1: self.mode = self.ICON
            elif type.find("temperature_high") != -1: self.mode = self.TEMPERATURE_HEIGH
            elif type.find("temperature_low") != -1: self.mode = self.TEMPERATURE_LOW
            elif type.find("temperature_heigh_low") != -1: self.mode = self.TEMPERATURE_HEIGH_LOW
            elif type.find("temperature_text") != -1: self.mode = self.TEMPERATURE_TEXT
            elif type.find("weekday") != -1: self.mode = self.WEEKDAY
            elif type.find("weekshortday") != -1: self.mode = self.WEEKSHORTDAY
            elif type.find("date") != -1: self.mode = self.DATE
            elif type.find("fulldate") != -1: self.mode = self.FULLDATE
            if self.mode is not None:
                dd = type.split(",")
                if len(dd) >= 2:
                    self.index = self.getIndex(dd[1])
                if self.mode == self.ICON and len(dd) == 4:
                    self.path = dd[2]
                    self.extension = dd[3]
                    
    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNWeatherConverter.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def getIndex(self, key):
        self.DEBUG('MSNWeather(Converter).getIndex key="%s"' % key) 
        if key == "current": return self.CURRENT
        elif key == "day1": return self.DAY1
        elif key == "day2": return self.DAY2
        elif key == "day3": return self.DAY3
        elif key == "day4": return self.DAY4
        elif key == "day5": return self.DAY5
        elif key == "day6": return self.DAY6
        elif key == "day7": return self.DAY7
        elif key == "day8": return self.DAY8
        elif key == "day9": return self.DAY9
        elif key == "day10": return self.DAY10
        elif key == "day11": return self.DAY11
        elif key == "day12": return self.DAY12
        elif key == "day13": return self.DAY13
        elif key == "day14": return self.DAY14
        return None

    @cached
    def getText(self):
        self.DEBUG('MSNWeather(Converter).getText self.mode=%s, self.index=%s' %( self.mode, self.index)) 
        retText = ''
        if self.mode == self.CITY:
            retText = self.source.getCity()
        elif self.mode == self.OBSERVATIONPOINT:
            retText = self.source.getObservationPoint()
        elif self.mode == self.OBSERVATIONTIME:
            retText = self.source.getObservationTime()
        elif self.mode == self.TEMPERATURE_CURRENT:
            retText = self.source.getTemperature_Current()
        elif self.mode == self.FEELSLIKE:
            retText = self.source.getFeelslike()
        elif self.mode == self.HUMIDITY:
            retText = self.source.getHumidity()
        elif self.mode == self.WINDDISPLAY:
            retText = self.source.getWinddisplay()
        elif self.mode == self.TEMPERATURE_HEIGH and self.index is not None:
            retText = self.source.getTemperature_Heigh(self.index)
        elif self.mode == self.TEMPERATURE_LOW and self.index is not None:
            retText = self.source.getTemperature_Low(self.index)
        elif self.mode == self.TEMPERATURE_HEIGH_LOW and self.index is not None:
            retText = self.source.getTemperature_Heigh_Low(self.index)
        elif self.mode == self.TEMPERATURE_TEXT and self.index is not None:
            retText = self.source.getTemperature_Text(self.index)
        elif self.mode == self.WEEKDAY and self.index is not None:
            retText = self.source.getWeekday(self.index, False)
        elif self.mode == self.WEEKSHORTDAY and self.index is not None:
            retText = self.source.getWeekday(self.index, True)
        elif self.mode == self.DATE and self.index is not None:
            retText = self.source.getDate(self.index)
        elif self.mode == self.FULLDATE and self.index is not None:
            retText = self.source.getFullDate(self.index)
        return retText
    
    text = property(getText)
    
    @cached
    def getIconFilename(self):
        retVal = ''
        if self.mode == self.ICON and self.index in (self.CURRENT, self.DAY1, self.DAY2, self.DAY3, self.DAY4, self.DAY5):
            if self.path is not None and self.extension is not None:
                retVal = self.path + self.source.getCode(self.index) + "." + self.extension
            else:
                retVal = self.source.getWeatherIconFilename(self.index)
                if len(retVal) <= 2:
                    retVal = retVal + ".png"
                if len(retVal) <= 6:
                    retVal = self.source.getIconPath() + retVal
        
        return retVal
            
    iconfilename = property(getIconFilename)
