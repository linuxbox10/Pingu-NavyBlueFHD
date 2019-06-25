try:
    from inits import myDEBUG, myDEBUGfile, PluginName
except Exception:
    PluginName = 'debug'
    myDEBUG=True
    myDEBUGfile = '/tmp/%s.log' % PluginName

import inspect

append2file=False
def printDEBUG( myText  , myFUNC = '' ):
	global append2file
	myFUNC = inspect.stack()[1][3]
	if myDEBUG:
		print ("[%s%s] %s" % (PluginName,myFUNC,myText))
		try:
			if append2file == False:
				append2file = True
				f = open(myDEBUGfile, 'w')
			else:
				f = open(myDEBUGfile, 'a')
			if myText[0:1] == '[':
				f.write('%s\n' %(myText))
			else:
				f.write('[%s] %s\n' %(myFUNC,myText))
			f.close
		except:
			pass

printDBG=printDEBUG
