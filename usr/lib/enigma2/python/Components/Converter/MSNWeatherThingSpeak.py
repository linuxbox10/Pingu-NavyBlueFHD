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
from enigma import eTimer

class MSNWeatherThingSpeak(Converter, object):
    def __init__(self, type):
        Converter.__init__(self, type)
        self.mode = type
        self.ThingSpeakItems = {}
        try:
            config.plugins.WeatherPlugin.currEntry.addNotifier(self.currEntryChanged, initial_call=True) 
        except Exception, e:
            self.EXCEPTIONDEBUG('MSNWeatherThingSpeak:__init__ Exception: %s' % str(e))

    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNWeatherThingSpeakConverter.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def currEntryChanged(self, configElement = None): 
        self.ThingSpeakItems = {}
        try:
            currEntry = int(config.plugins.WeatherPlugin.currEntry.value)
            self.DEBUG('MSNWeatherThingSpeak:currEntryChanged currEntry = %s' % currEntry)
            if config.plugins.WeatherPlugin.Entry[currEntry].thingSpeakChannelID.value == '':
                self.downstream_elements[0].visible = False 
            else:
                self.downstream_elements[0].visible = True 
        except Exception as e:
            self.EXCEPTIONDEBUG("MSNWeatherThingSpeak:currEntryChanged Exception: %s" % str(e))
        
    def syncItems(self):
        self.DEBUG('MSNWeatherWebCurrent(Converter).syncItems >>')
        self.ThingSpeakItems = {}
        self.ThingSpeakItems = self.source.getThingSpeakItems().copy()
    
    @cached
    def getText(self): #self.mode = ('name','description','field1Name','field2Name','ObservationTime','field1Value','field1Status','field2Value','field2Status')
        self.DEBUG('MSNWeatherThingSpeak:getText','>>> self.mode="%s", currEntry=%s' % (self.mode, config.plugins.WeatherPlugin.currEntry.value))
        self.syncItems()
        retTXT = ''
        if len(self.ThingSpeakItems) > 0:
            try:
                if self.mode == 'PM2.5':
                    name = self.ThingSpeakItems.get('PM2.5Name', '')
                    if name != '':
                        fval = float(self.ThingSpeakItems.get('PM2.5Value', ''))
                        val = int(fval + 0.5)
                        stat = ''
                        if   val <= 12 : stat = 'Bardzo dobre'
                        elif val <= 36 : stat = 'Dobre'
                        elif val <= 60 : stat = 'Umiarkowane'
                        elif val <= 84 : stat = 'Dostateczne'
                        elif val <=120 : stat = 'Z쿮'
                        else: stat = 'Bardzo z쿮'
                        retTXT = '%s %s %s' %(name, val, stat)
                elif self.mode == 'PM10':
                    name = self.ThingSpeakItems.get('PM10Name', "")
                    if name != '':
                        fval = float(self.ThingSpeakItems.get('PM10Value', ''))
                        val = int(fval + 0.5)
                        stat = ''
                        if   val <= 20 : stat = 'Bardzo dobre'
                        elif val <= 60 : stat = 'Dobre'
                        elif val <=100 : stat = 'Umiarkowane'
                        elif val <=140 : stat = 'Dostateczne'
                        elif val <=200 : stat = 'Z쿮'
                        else: stat = 'Bardzo z쿮'
                        retTXT = '%s %s %s' %(name, val, stat)
                elif self.mode == 'field1': retTXT = '%s %s' %( self.ThingSpeakItems.get('field1Name', ""), self.ThingSpeakItems.get('field1Value', '') )
                elif self.mode == 'field2': retTXT = '%s %s' %( self.ThingSpeakItems.get('field2Name', ""), self.ThingSpeakItems.get('field2Value', '') )
                elif self.mode == 'field3': retTXT = '%s %s' %( self.ThingSpeakItems.get('field3Name', ""), self.ThingSpeakItems.get('field3Value', '') )
                elif self.mode == 'field4': retTXT = '%s %s' %( self.ThingSpeakItems.get('field4Name', ""), self.ThingSpeakItems.get('field4Value', '') )
                elif self.mode == 'field5': retTXT = '%s %s' %( self.ThingSpeakItems.get('field5Name', ""), self.ThingSpeakItems.get('field5Value', '') )
                else: retTXT = str(self.ThingSpeakItems.get(self.mode, ''))
            except Exception as e:
                self.EXCEPTIONDEBUG('MSNWeatherThingSpeak:getText Exception="%s"' % str(e))
            
        return retTXT
        
    text = property(getText)
    
    @cached
    def getIconFilename(self):
        self.DEBUG('MSNWeatherThingSpeak:getIconFilename','>>> self.mode="%s"' % self.mode)
        self.syncItems()
        return ""
            
    iconfilename = property(getIconFilename)
    
    def changed(self, what):
        try:
            if what[0] == self.CHANGED_POLL:
                self.downstream_elements.changed(what)
        except Exception: pass
                 