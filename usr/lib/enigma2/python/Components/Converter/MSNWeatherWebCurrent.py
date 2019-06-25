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
from Plugins.Extensions.MSNweather.__init__ import _

class MSNWeatherWebCurrent(Converter, object):
    def __init__(self, type):
        self.DEBUG('MSNWeatherWebCurrent(Converter).__init__')
        Converter.__init__(self, type)
        if type.find('Value') > -1:
            self.valueOnly = True
            self.mode = type.replace('Value', '')
        else:
            self.valueOnly = False
            self.mode = type
        self.WebCurrentItems = {}
            
    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNWeatherWebCurrentConverter.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def syncItems(self):
        self.DEBUG('MSNWeatherWebCurrent(Converter).syncItems >>')
        self.WebCurrentItems = self.source.getWebCurrentItems().copy()
    
    @cached
    def getText(self): #self.mode = ('name','description','field1Name','field2Name','ObservationTime','field1Value','field1Status','field2Value','field2Status')
        self.syncItems()
        self.DEBUG('MSNWeatherWebCurrent(Converter).getText >>> self.mode="%s"' % self.mode)
        self.syncItems()
        retTXT = ''
        self.DEBUG('MSNWeatherWebCurrent(Converter).getText#######\n####### self.WebCurrentItems = \n%s\n##############' % str(self.WebCurrentItems).replace('Record=','\nRecord='))
        if len(self.WebCurrentItems) > 0:
            try:
                if self.mode.lower() == 'title':
                    retTXT =  self.WebCurrentItems['title'][0]
                elif self.mode.lower() == 'alltitles':
                    for line in self.WebCurrentItems.get('nowData', []):
                        retTXT += str(line[0]).strip() + ':\n'
                    retTXT = retTXT[:-1].replace('Temperatura', 'Temp.')
                elif self.mode.lower() == 'allinfo':
                    for line in self.WebCurrentItems.get('nowData', []):
                        retTXT += str(line[1]).strip() + '\n'
                    retTXT = retTXT[:-1].replace('Temperatura', 'Temp.')
                else:
                    for line in self.WebCurrentItems.get('nowData', []):
                        if line[0].lower() == self.mode.lower() and self.mode.lower() == 'barometr':
                            if self.valueOnly:
                                retTXT = str(line[1].strip())
                            else:
                                retTXT = str(_('Pressure %s') % (line[1].strip()))
                        elif line[0].lower() == self.mode.lower(): #available: 'Temperatura odczuwalna','Wiatr','Barometr','Widoczno\xc5\x9b\xc4\x87','Wilgotno\xc5\x9b\xc4\x87','Temperatura punktu rosy'
                            if self.valueOnly:
                                retTXT = str(line[1].strip())
                            else:
                                retTXT = str('%s: %s' % (line[0].strip(), line[1].strip()))
            except Exception as e:
                self.EXCEPTIONDEBUG('\t','Exception %s' % str(e))
        self.DEBUG('\t','retTXT="%s"' % retTXT)
        return retTXT.replace('.00','')
        
    text = property(getText)
