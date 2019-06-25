# -*- coding: utf-8 -*-
#######################################################################
#
#    MSNweather extension Converter for Enigma2
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem konwertera
#    Please respect my work and don't delete/change name of the converter author
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#     
####################################################################### 

from Components.config import config
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import resolveFilename, SCOPE_SKIN
from Plugins.Extensions.MSNweather.__init__ import _
import os
import datetime

class MSNWeatherWebDaily(Converter, object):
    def __init__(self, type):
        self.DEBUG('MSNWeatherWebDaily(Converter).__init__')
        Converter.__init__(self, type)
        self.mode = type
        self.WebDailyItems = {}
        self.PluginPath = '/usr/lib/enigma2/python/Plugins/Extensions/MSNweather'
        self.SkinWeatherIconsPath = resolveFilename(SCOPE_SKIN, config.skin.primary_skin.value).replace('/skin.xml','') + '/weather_icons'
            
    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNWeatherWebDailyConverter.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )
    
    def syncItems(self):
        self.DEBUG('MSNWeatherWebDaily(Converter).syncItems >>>')
        self.WebDailyItems = self.source.getWebDailyItems().copy()
    
    @cached
    def getText(self):
        self.DEBUG('MSNWeatherWebDaily(Converter).getText >>> self.mode="%s"' % self.mode)
        self.syncItems()
        retTXT = ''
        #self.DEBUG('','######\n%s\n#####' % self.WebDailyItems)
        if len(self.WebDailyItems) > 0:
            try:
                mode = self.mode.split(',')
                self.DEBUG('\t','len(mode) =%s' % str(len(mode)))
                if len(mode) >= 2:
                    record = mode[0]
                    day = int(record.split('=')[1])
                    Month = _((datetime.date.today() + datetime.timedelta(days=day)).strftime("%b"))
                    item =  mode[1]
                    line = self.WebDailyItems.get(record, [('', '', '', '', '', '', '', '', '', '')])
                    line = line[0]
                    if item ==  'date':
                        retTXT = str('%s. %s %s' % (line[1].strip().lower(), line[2].strip(), Month))
                    elif item ==  'info':
                        retTXT = str('%s/ %s/ %s\n%s' % (line[6].strip(), line[7].strip(), line[8].strip(), line[4].strip()))
            except Exception as e:
                self.EXCEPTIONDEBUG('\t','Exception %s' % str(e))
        self.DEBUG('\t','retTXT="%s"' % retTXT)
        return retTXT
        
    text = property(getText)
    
    @cached
    def getIconFilename(self):
        self.DEBUG('MSNWeatherWebDaily(Converter).getIconFilename >>> self.mode="%s"' % self.mode)
        self.syncItems()
        iconFileName = 'fake.png'
        if len(self.WebDailyItems) > 0:
            try:
                WeatherIcon = self.WebDailyItems.get('WeatherIcon4%s' % self.mode , '')
                self.DEBUG('MSNWeatherWebDaily(Converter).getIconFilename WeatherIcon ="%s" (%s/%s)' % (WeatherIcon, self.SkinWeatherIconsPath, WeatherIcon))
                if config.plugins.WeatherPlugin.IconsType.value != "serviceIcons" and WeatherIcon != '' and os.path.exists('%s/%s' % (self.SkinWeatherIconsPath, WeatherIcon)):
                    self.DEBUG('MSNWeatherWebDaily(Converter).getIconFilename using webRegex icon')
                    iconFileName = '%s/%s' % (self.SkinWeatherIconsPath, WeatherIcon)
                else:
                    line = self.WebDailyItems.get(self.mode, [('', '', '', '', '', '', '', '', '', '')])
                    line = line[0]
                    url = str('%s' % line[3].strip())
                    self.DEBUG('MSNWeatherWebDaily(Converter).getIconFilename url=%s' % url)
                    icon = '%s' % (url.split('?')[0].split('/')[-1][:-4])
                    iconFileName = '%s/icons/%s.png' % (self.PluginPath, icon)
                    if not os.path.exists(iconFileName):
                        import urllib
                        if 'url'[:4] != 'http': url = 'http:' + url
                        self.DEBUG('MSNWeatherWebDaily(Converter).getIconFilename downloading %s' % url)
                        urllib.urlretrieve(url, iconFileName)
                    self.DEBUG('MSNWeatherWebDaily(Converter).getIconFilenameiconFileName=%s' % (iconFileName))
            except Exception as e:
                self.EXCEPTIONDEBUG('MSNWeatherWebDaily(Converter).getIconFilename Exception %s' % str(e))
        return iconFileName
            
    iconfilename = property(getIconFilename)
