# standard Picon.py modified by @j00zek to support any picon folder name
# the name can be defined in xml by puttin attri picontype="<foldername>"
# e.g. picontype="zzpicon"
import os, re, unicodedata
from Renderer import Renderer
from enigma import ePixmap #, ePicLoad
from Tools.Alternatives import GetWithAlternative
from Tools.Directories import pathExists, SCOPE_SKIN_IMAGE, resolveFilename
try:
    from Tools.Directories import SCOPE_CURRENT_SKIN
except Exception:
    from Tools.Directories import SCOPE_ACTIVE_SKIN as SCOPE_CURRENT_SKIN

from Components.Harddisk import harddiskmanager
from ServiceReference import ServiceReference
from Components.config import config, ConfigBoolean
searchPaths = ['/usr/share/enigma2/']
lastPiconsDict = {}
#piconType = 'picon'

##### write log in /tmp folder #####
DBG = False
try:
    from Components.j00zekComponents import j00zekDEBUG
except Exception:
    def j00zekDEBUG(myText=None):
        if not myText is None:
            print(myText)
#####

def initPiconPaths():
    for part in harddiskmanager.getMountedPartitions():
        if DBG: j00zekDEBUG('[j00zekPicons]:[initPiconPaths] MountedPartitions:' + part.mountpoint)
        addPiconPath(part.mountpoint)
    if pathExists("/proc/mounts"):
        with open("/proc/mounts", "r") as f:
            for line in f:
                if line.startswith('/dev/sd'):
                    mountpoint = line.split(' ')[1]
                    if DBG: j00zekDEBUG('[j00zekPicons]:[initPiconPaths] mounts:' + mountpoint)
                    addPiconPath(mountpoint)

def addPiconPath(mountpoint):
    if DBG: j00zekDEBUG('[j00zekPicons] mountpoint=' + mountpoint)
    if mountpoint == '/':
        return
    global searchPaths
    try:
        if mountpoint not in searchPaths:
            if DBG: j00zekDEBUG('[j00zekPicons] mountpoint not in searchPaths')
            for pp in os.listdir(mountpoint):
                lpp = os.path.join(mountpoint, pp) + '/'
                if pp.find('picon') >= 0 and os.path.isdir(lpp): #any folder *picon*
                    for pf in os.listdir(lpp):
                        if pf.endswith('.png') and mountpoint not in searchPaths: #if containf *.png
                            if mountpoint.endswith('/'):
                                searchPaths.append(mountpoint)
                            else:
                                searchPaths.append(mountpoint + '/')
                            if DBG: j00zekDEBUG('[j00zekPicons] mountpoint appended to searchPaths')
                            break
                    else:
                        continue
                    break
    except Exception, e:
        if DBG: j00zekDEBUG('[j00zekPicons] Exception:' + str(e))

def onPartitionChange(why, part):
    if DBG: j00zekDEBUG('[j00zekPicons] onPartitionChange>>>')
    global searchPaths
    if why == 'add' and part.mountpoint not in searchPaths:
        addPiconPath(part.mountpoint)
    elif why == 'remove' and part.mountpoint in searchPaths:
        searchPaths.remove(part.mountpoint)


def findPicon(serviceName, selfPiconType = 'picon'):
    if serviceName is None or serviceName == '':
        return None
    pngname = None
    findPiconTypeName='%s%s' % (selfPiconType,serviceName)
    if findPiconTypeName in lastPiconsDict:
        pngname = lastPiconsDict[findPiconTypeName]
        if DBG: j00zekDEBUG('[j00zekPicons:findPicon] found in lastPiconsDict[%s] = %s' % (findPiconTypeName,pngname) )
    else:
        for path in searchPaths:
            sPath = path + selfPiconType + '/'
            if DBG: j00zekDEBUG('[j00zekPicons:findPicon] searching for %s%s.[png|gif]' % (sPath,serviceName) )
            if pathExists(sPath + serviceName + '.png'):
                pngname = sPath + serviceName + '.png'
                lastPiconsDict[findPiconTypeName] = pngname
                if DBG: j00zekDEBUG('[j00zekPicons:findPicon] lastPiconsDict[%s] = %s' % (findPiconTypeName, pngname) )
                break
            elif pathExists(sPath + serviceName + '.gif'):
                pngname = sPath + serviceName + '.gif'
                lastPiconsDict[findPiconTypeName] = pngname
                if DBG: j00zekDEBUG('[j00zekPicons:findPicon] lastPiconsDict[%s] = %s' % (findPiconTypeName, pngname) )
                break
    return pngname


def getPiconName(serviceName, selfPiconType):
    if DBG: j00zekDEBUG('[j00zekPicons:getPiconName] >>>')
    name = 'unknown'
    sname = '_'.join(GetWithAlternative(serviceName).split(':', 10)[:10])
    pngname = findPicon(sname, selfPiconType)
    if not pngname:
        fields = sname.split('_', 3)
        isChanged = False
        if len(fields) > 2 and fields[2] != '2' and fields[2] != '1':
            fields[2] = '1'
            isChanged = True
        if len(fields) > 0 and fields[0] == '4097':
            fields[0] = '1'
            isChanged = True
        if isChanged == True:
            pngname = findPicon('_'.join(fields), selfPiconType)
    if not pngname:
        name = ServiceReference(serviceName).getServiceName()
        name = unicodedata.normalize('NFKD', unicode(name, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
        name = re.sub('[^a-z0-9]', '', name.replace('&', 'and').replace('+', 'plus').replace('*', 'star').lower())
        if len(name) > 0:
            pngname = findPicon(name, selfPiconType)
            if not pngname and len(name) > 2 and name.endswith('hd'):
                pngname = findPicon(name[:-2], selfPiconType)
    if DBG:
        j00zekDEBUG('[j00zekPicons:getPiconName] serviceName=%s, picon=%s, %s, piconFile=%s, selfPiconType=%s' %(str(serviceName),
                                                                sname, name, str(pngname), selfPiconType) )
    return pngname


class j00zekPicons(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        #self.PicLoad = ePicLoad()
        #self.PicLoad.PictureData.get().append(self.updatePicon)
        self.piconsize = (0, 0)
        self.pngname = ''
        self.piconType = 'picon'
        self.GifsPath = 'animatedGIFpicons'
        self.ShowDefault = True
        self.GIFsupport = False
        return

    def addPath(self, value):
        if DBG: j00zekDEBUG('[j00zekPicons:addPath] %s' % value)
        global searchPaths
        if not value.endswith('/'):
            value += '/'
        if value not in searchPaths:
            searchPaths.append(value)

    def applySkin(self, desktop, parent):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.addPath(value)
                attribs.remove((attrib, value))
            elif attrib == 'size':
                self.piconsize = value
            elif attrib == 'picontype':
                self.piconType = value
                attribs.remove((attrib, value))
            elif attrib == 'showdefaultpic':
                if value in ('False','no'): self.ShowDefault = False
                attribs.remove((attrib, value))
            elif attrib == 'gifsupport':
                if value in ('True','yes'): self.GIFsupport = True
                attribs.remove((attrib, value))

        self.skinAttributes = attribs
        if DBG: j00zekDEBUG('[j00zekPicons:applySkin] self.piconType=%s, self.ShowDefault=%s' % (self.piconType,self.ShowDefault))
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        self.changed((self.CHANGED_DEFAULT,))

    #def updatePicon(self, picInfo = None):
    #    ptr = self.PicLoad.getData()
    #    if ptr is not None:
    #        self.instance.setPixmap(ptr.__deref__())
    #        self.instance.show()
    #    return

    def changed(self, what):
        if self.instance:
            pngname = None
            gifname = None
            try:
                if not what[0] is self.CHANGED_CLEAR:
                    if self.source.text is not None and self.source.text != '':
                        if self.GIFsupport == True: gifname = getPiconName(self.source.text, self.GifsPath)
                        pngname = getPiconName(self.source.text, self.piconType)
                        if DBG: j00zekDEBUG('[j00zekPicons]:[changed] gifname=%s, pngname=%s' %(gifname,pngname))
                    if pngname is None and self.ShowDefault == True:
                        pngname = findPicon('picon_default', self.piconType)
                        if pngname is None and pathExists(resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')):
                            pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                    if pngname is None:
                        self.instance.hide()
                    elif self.pngname != pngname:
                        if pngname:
                            self.instance.setScale(1)
                            self.instance.setPixmapFromFile(pngname)
                            self.instance.show()
                        else:
                            self.instance.hide()
                        self.pngname = pngname
                    if DBG: j00zekDEBUG('[j00zekPicons]:[changed] piconType=' + self.piconType + ', pngname=' + str(pngname))
            except Exception, e:
                j00zekDEBUG('[j00zekPicons]:[changed] Exception:' + str(e))


harddiskmanager.on_partition_list_change.append(onPartitionChange)
initPiconPaths()