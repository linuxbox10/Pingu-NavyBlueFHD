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

from Components.AVSwitch import AVSwitch
from Components.config import config
from enigma import ePixmap, eSize, eTimer
from random import randint
from Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
import os


class MSNWeatherPixmap(Renderer):
    
    def __init__(self):
        Renderer.__init__(self)
        self.pixdelay = int((randint(70,150) + randint(70,150)) / 2)
        self.picsIcons = []
        self.picsIconsCount = 0
        self.slideIcon = 0
        self.lastPic = ''
        self.timer = eTimer()
        self.timer.callback.append(self.timerEvent)
        self.pngAnimPath='/usr/share/enigma2/animatedWeatherIcons'
        self.DEBUG('MSNWeatherPixmap(Renderer)__init__ pixdelay=%s' % self.pixdelay)

    GUI_WIDGET = ePixmap

    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNWeatherPixmapRenderer.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )
    
    def postWidgetCreate(self, instance):
        for (attrib, value) in self.skinAttributes:
            if attrib == "size":
                x, y = value.split(',')
                self._scaleSize = eSize(int(x), int(y))
                break
        sc = AVSwitch().getFramebufferScale()
        self._aspectRatio = eSize(sc[0], sc[1])
        
    def doSuspend(self, suspended):
        if suspended:
            self.timer.stop()
            self.changed((self.CHANGED_CLEAR,))
        else:
            if self.picsIconsCount > 0: 
                self.timer.start(self.pixdelay, True)
            self.changed((self.CHANGED_DEFAULT,))
            
    def changed(self, what):
        if what[0] != self.CHANGED_CLEAR:
            if self.instance:
                self.instance.setScale(1)
                self.updateIcon(self.source.iconfilename)

    def doAnimation(self, pngAnimPath):
        self.DEBUG('MSNWeatherPixmap(Renderer).doAnimation pngAnimPath = %s' % pngAnimPath)
        if config.plugins.WeatherPlugin.IconsType.value == 'animIcons' and os.path.exists(pngAnimPath):
            return True
        else:
            return False
                
    def updateIcon(self, filename):
        self.DEBUG('MSNWeatherPixmap(Renderer).updateIcon(%s) lastPic= %s' % (filename,self.lastPic))
        if self.lastPic != filename and filename[-4:].lower() in ('.png','.jpg'):
            self.lastPic = filename
            IconName = os.path.basename(self.lastPic)
            pngAnimPath = os.path.join(self.pngAnimPath, IconName)[:-4]
            self.DEBUG('MSNWeatherPixmap(Renderer).updateIcon pngAnimPath=%s' % pngAnimPath)
            if self.doAnimation(pngAnimPath):
                reverseSlides = False
                self.DEBUG('MSNWeatherPixmap(Renderer).updateIcon pngAnimPath exists')
                if os.path.exists(os.path.join(pngAnimPath,'.ctrl')):
                    with open(os.path.join(pngAnimPath,'.ctrl')) as cf:
                        for line in cf:
                            lineArray = line.strip().split('=')
                            if lineArray[0] == 'delay':
                                self.pixdelay = int(lineArray[1])
                            if lineArray[0] == 'revert' and lineArray[1] == 'True':
                                reverseSlides = True
                        cf.close()
                      
                self.slideIcon = 0
                self.picsIcons = []
                pngfiles = [f for f in os.listdir(pngAnimPath) if (os.path.isfile(os.path.join(pngAnimPath, f)) and f.endswith(".png"))]
                pngfiles.sort()
                if reverseSlides:
                    pngfiles.reverse()
                for x in pngfiles:
                    self.picsIcons.append(LoadPixmap(os.path.join(pngAnimPath, x)))
                self.picsIconsCount = len(self.picsIcons)
                if self.picsIconsCount > 0: 
                    self.timer.start(self.pixdelay, True)
                    self.DEBUG('MSNWeatherPixmap(Renderer).updateIcon picsIconsCount=%s' % self.picsIconsCount)
            else:
                self.instance.setPixmap(LoadPixmap(path=self.lastPic))
              

    def timerEvent(self):
        self.timer.stop()
        self.slideIcon += 1
        if self.slideIcon >= self.picsIconsCount:
                self.slideIcon = 0
        try:
            self.instance.setPixmap(self.picsIcons[self.slideIcon])
            self.timer.start(self.pixdelay, True)
        except Exception as e:
            self.EXCEPTIONDEBUG('MSNWeatherPixmap(Renderer).timerEvent exception %s' % str(e))
