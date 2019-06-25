#######################################################################
#
#    Renderer for Enigma2
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem renderera
#    Please respect my work and don't delete/change name of the renderer author
#
#    Nie zgadzam sie na wykorzystywanie tego renderera w projektach platnych jak np. Graterlia!!!
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
#    To use it do the following:
#       - download package of animated picons, for example from my opkg
#       - write them in the animatedPicons folder on mounted device or in /usr/share/enigma2/
#             NOTE:if you want to use any other folder, you need to specify it in widget definition. E.g. pixmaps="animatedPicons/Flara/"
#       - include J00zekPiconAnimation widget in the infobar skin definition.
#             E.g. <widget source="session.CurrentService" render="j00zekPiconAnimation" position="30,30" size="220,132" zPosition="5" transparent="1" alphatest="blend" />
#             NOTE:
#                   -  position="X,Y" should be the same like position of a picon in skin definition
#                   -  size="X,Y" should be the same like size of a picon in skin definition
#                   -  zPosition="Z" should be bigger than zPosition of a picon in skin definition, to display animation over the picon.
#
#             OTHER PARAMETERS:
#                   - pixmaps           : name of the directory, default 'animatedPicons'
#                   - pixdelay          : delay between showing frames, default 50ms
#                   - lockpath="True"   : always use path defined in skin, default "False" - very usefull if skin author want to have many different animations
#                   - loop="True"       : run animation in a loop, default "False"
#                   - loopdelay         : delay between showing frames, default 50ms, default 5* pixdelay
#
#    OPTIONAL animations control:
#       - to set speed put '.ctrl' file  in the pngs folder containing 'delay=TIME' where TIME is miliseconds to wait between frames
#       - to overwrite skin setting use config attributes from your own plugin or use UserSkin which has GUI to present them
#       - to disable user settings (see above) put lockpath="True" attribute in widget definition
#       - to randomize animations put all in the subfolders of main empy animations folder. If you want to disable any just put ".off" at the end of the folder name
#                 Example:
#                         create /usr/shareenigma2/animatedPicons/ EMPTY folder
#                         create /usr/shareenigma2/animatedPicons/Flara subfolder with animation png's
#                         create /usr/shareenigma2/animatedPicons/OldMovie subfolder with second animation png's
#
####################################################################### 
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Renderer import Renderer
from enigma import ePixmap, eTimer, iPlayableService
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigDirectory
from Components.Harddisk import harddiskmanager
from random import randint
import os

config.plugins.j00zekPiconAnimation = ConfigSubsection() 
config.plugins.j00zekPiconAnimation.UserPathEnabled = ConfigYesNo(default = False) 
config.plugins.j00zekPiconAnimation.UserPath = ConfigDirectory(default = "")  
##### write log in /tmp folder #####
DBG = False
try:
    from Components.j00zekComponents import j00zekDEBUG
except Exception:
    def j00zekDEBUG(myText=None):
        if not myText is None:
            try: print(myText)
            except Exception: pass
#####

searchPaths = ['/usr/share/enigma2/']

def initPiconPaths():
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[initPiconPaths] >>>')
    for part in harddiskmanager.getMountedPartitions():
        addPiconPath(part.mountpoint)
    if os.path.exists("/proc/mounts"):
        with open("/proc/mounts", "r") as f:
            for line in f:
                if line.startswith('/dev/sd'):
                    mountpoint = line.split(' ')[1]
                    addPiconPath(mountpoint)

def addPiconPath(mountpoint):
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] >>> mountpoint=' + mountpoint)
    if mountpoint == '/':
        return
    global searchPaths
    try:
        if mountpoint not in searchPaths:
            if DBG: j00zekDEBUG('j00zekPiconAnimation]:[addPiconPath] mountpoint not in searchPaths')
            for pp in os.listdir(mountpoint):
                lpp = os.path.join(mountpoint, pp) + '/'
                if pp.find('picon') >= 0 and os.path.isdir(lpp): #any folder *picon*
                    for pf in os.listdir(lpp):
                        if pf.endswith('.png') and mountpoint not in searchPaths: #if containf *.png
                            if mountpoint.endswith('/'):
                                searchPaths.append(mountpoint)
                            else:
                                searchPaths.append(mountpoint + '/')
                            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] mountpoint appended to searchPaths')
                            break
                    else:
                        continue
                    break
    except Exception, e:
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] Exception:' + str(e))

def onPartitionChange(why, part):
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[onPartitionChange] >>>')
    global searchPaths
    if why == 'add' and part.mountpoint not in searchPaths:
        addPiconPath(part.mountpoint)
    elif why == 'remove' and part.mountpoint in searchPaths:
        searchPaths.remove(part.mountpoint)

class j00zekPiconAnimation(Renderer):
    __module__ = __name__

    def __init__(self):
        Renderer.__init__(self)
        self.pixmaps = 'animatedPicons'
        self.delayBetweenFrames = 50
        self.delayBetweenLoops = self.delayBetweenFrames * 5
        self.doAnim = False
        self.doLockPath = False
        self.doInLoop = False
        self.animCounter = 0
        self.FramesCount = 0
        self.slideFrame = 0
        self.FramesList = []
        self.animationsFoldersList = []
        self.animTimer = eTimer()
        self.animTimer.callback.append(self.timerEvent)
        self.what = ['CHANGED_DEFAULT', 'CHANGED_ALL', 'CHANGED_CLEAR', 'CHANGED_SPECIFIC', 'CHANGED_POLL']
        self.whatDescr = ['# initial "pull" state ', '# really everything changed ',
                    '# we are expecting a real update soon. do not bother polling NOW, but clear data. ',
                    '# second tuple will specify what exactly changed ', '# a timer expired ']
        self.CH_SP_ev = ['evStart', 'evEnd', 'evTunedIn', 'evTuneFailed', 'evUpdatedEventInfo', 'evUpdatedInfo', 'evSeekableStatusChanged',
                        'evEOF', 'evSOF', 'evCuesheetChanged','evUpdatedRadioText', 'evUpdatedRtpText', 'evUpdatedRassSlidePic',
                        'evUpdatedRassInteractivePicMask', 'evVideoSizeChanged', 'evVideoFramerateChanged', 'evVideoProgressiveChanged',
                        'evBuffering', 'evStopped', 'evHBBTVInfo', 'evFccFailed', 'evUser']

    def applySkin(self, desktop, parent):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] >>>')
        #Load attribs
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'pixmaps':
                self.pixmaps = value
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] self.pixmaps=%s' % value)
            elif attrib == 'pixdelay':
                self.delayBetweenFrames = int(value)
                if self.delayBetweenFrames < 40: self.delayBetweenFrames = 40
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] self.delayBetweenFrames=%s' % self.delayBetweenFrames)
            elif attrib == 'lockpath':
                if value == 'True': self.doLockPath = True
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] self.doLockPath=%s' % self.doLockPath)
            elif attrib == 'loop':
                if value == 'True': self.doInLoop = True
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] self.doInLoop=%s' % self.doInLoop)
            elif attrib == 'loopdelay':
                self.delayBetweenLoops = int(value)
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] self.delayBetweenLoops=%s' % self.delayBetweenLoops)
            else:
                attribs.append((attrib, value))
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] unknown %s=%s' % (attrib,value))

        self.skinAttributes = attribs
        #Load animation into memory
        try:
            if config.plugins.j00zekPiconAnimation.UserPathEnabled.value == True and self.doLockPath == False:
                if DBG: j00zekDEBUG('if config.plugins.j00zekPiconAnimation.UserPathEnabled.value == True and self.doLockPath == False:')
                if os.path.exists(config.plugins.j00zekPiconAnimation.UserPath.value):
                    self.loadPNGsAnim(config.plugins.j00zekPiconAnimation.UserPath.value)
                    self.loadPNGsSubFolders(config.plugins.j00zekPiconAnimation.UserPath.value)
                elif DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] User path "%s" selected but does NOT exist' % config.plugins.j00zekPiconAnimation.UserPath.value)
            else:
                if DBG: j00zekDEBUG('if self.doLockPath == True:')
                for path in searchPaths:
                    if self.loadPNGsAnim(os.path.join(path, self.pixmaps)) == True:
                        break
                self.loadPNGsSubFolders(os.path.join(path, self.pixmaps))
        except Exception, e:
            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] Exception %s' % str(e))
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[postWidgetCreate] >>>')
#self.changed((self.CHANGED_DEFAULT,))
        return

    def preWidgetRemove(self, instance):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[preWidgetRemove] >>>')
        if not self.animTimer is None:
            self.animTimer.stop()
            self.animTimer.callback.remove(self.timerEvent)
            self.animTimer = None

    def connect(self, source):
        Renderer.connect(self, source)

    def doSuspend(self, suspended):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[doSuspend] >>> suspended=%s' % suspended)
        if suspended:
                self.changed((self.CHANGED_CLEAR,))
        else:
                self.changed((self.CHANGED_DEFAULT,))
            
    def loadPNGsSubFolders(self, animPath):
        self.animationsFoldersList = []
        if len(self.FramesList) == 0 and os.path.exists(animPath):
            picsFolder = [f for f in os.listdir(animPath) if (os.path.isdir(os.path.join(animPath, f)) and not f.endswith(".off"))]
            for x in picsFolder:
                for f in os.listdir(os.path.join(animPath, x)):
                    if f.endswith(".png"):
                        self.animationsFoldersList.append(os.path.join(animPath, x))
                        if DBG: j00zekDEBUG('[j00zekPiconAnimation]]:[loadPNGsSubFolders] found *.png in subfolder "%s"' % os.path.join(animPath, x))
                        break
                    
    def loadPNGsAnim(self, animPath):
        if animPath == self.pixmaps: return False
        if os.path.exists(animPath):
            self.pixmaps = animPath
            pngfiles = [f for f in os.listdir(self.pixmaps) if (os.path.isfile(os.path.join(self.pixmaps, f)) and f.endswith(".png"))]
            pngfiles.sort()
            self.FramesList = []
            self.doAnim = False
            for x in pngfiles:
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] read image %s' % os.path.join(self.pixmaps, x))
                self.FramesList.append(LoadPixmap(os.path.join(self.pixmaps, x)))
            if len(self.FramesList) > 0:
                self.FramesCount = len(self.FramesList)
                self.doAnim = True
                if os.path.exists(os.path.join(animPath,'.ctrl')):
                    with open(os.path.join(animPath,'.ctrl')) as cf:
                        try:
                            myDelay=cf.readline().strip()
                            cf.close()
                            self.delayBetweenFrames = int(myDelay.split('=')[1])
                            if self.delayBetweenFrames < 40: self.delayBetweenFrames = 40
                        except Exception, e:
                            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] Exception "%s" loading .ctrl' % str(e))
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] Loaded from path=%s, pics=%s, pixdelay=%s' % (self.pixmaps,self.FramesCount,self.delayBetweenFrames))
                return True
            else:
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] No *.png in given path "%s".' % (animPath))
        else:
            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] Path "%s" does NOT exist.' % (animPath))
        return False
         
      
    def changed(self, what):
        if self.instance:
            self.instance.setScale(1) 
            if DBG: 
                try:
                    if what[0] == self.CHANGED_SPECIFIC:
                        j00zekDEBUG('[j00zekPiconAnimation]:[changed] > what(%s,%s)=%s:%s, self.doAnim=%s' % (what[0],
                                                                                                        what[1],
                                                                                                        self.what[int(what[0])],
                                                                                                        self.CH_SP_ev[int(what[1])],
                                                                                                        self.doAnim)
                                                                                                        )
                    else: 
                        j00zekDEBUG('[j00zekPiconAnimation]:[changed] > what(%s)=%s %s, self.doAnim=%s' % (what[0],
                                                                                                        self.what[int(what[0])],
                                                                                                        self.whatDescr[int(what[0])],
                                                                                                        self.doAnim)
                                                                                                        )
                except Exception as e:
                    j00zekDEBUG('[j00zekPiconAnimation]:[changed]  exception %s' % str(e))
            if what[0] == self.CHANGED_CLEAR: #we are expecting a real update soon. do not bother polling NOW, but clear data
                if not self.animTimer is None: self.animTimer.stop()
                self.instance.hide()
                self.slideFrame = 0
                self.doAnim = True
            elif what[0] == self.CHANGED_SPECIFIC and what[1] not in (iPlayableService.evStart,): #Do nothing for some CHANGED_SPECIFIC codes
                    if DBG: j00zekDEBUG('CHANGED_SPECIFIC is not iPlayableService.evStart')
                    pass
            elif self.doAnim == True:
                self.doAnim = False
                self.slideFrame = 0
                self.instance.show()
                self.animTimer.start(self.delayBetweenFrames, True)

    def timerEvent(self):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] >>> self.slideFrame=%s' % self.slideFrame)
        self.animTimer.stop()
        if self.slideFrame < self.FramesCount:
            self.instance.setPixmap(self.FramesList[self.slideFrame])
            self.slideFrame += 1
            if self.slideFrame >= self.FramesCount: self.slideFrame = self.FramesCount
            self.animTimer.start(self.delayBetweenFrames, True)
        elif self.slideFrame == self.FramesCount: #Note last frame does NOT exists
            if self.doInLoop == True:
                self.slideFrame = 0
                self.animTimer.start(self.delayBetweenLoops, True)
                if DBG: j00zekDEBUG('\t\t\t loop animation')
            else:
                if DBG: j00zekDEBUG('\t\t\t Finished stop animation')
                self.instance.hide()
                self.doAnim = True
                self.animCounter = self.animCounter + 1
                if len(self.animationsFoldersList) > 1:
                    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] change animation')
                    self.loadPNGsAnim(self.animationsFoldersList[randint(0, len(self.animationsFoldersList)-1)])
        #if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] <<<')

harddiskmanager.on_partition_list_change.append(onPartitionChange)
initPiconPaths()
