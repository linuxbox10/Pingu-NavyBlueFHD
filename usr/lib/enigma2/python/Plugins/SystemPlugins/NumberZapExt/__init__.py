from Components.Language import language
import os, gettext

PLUGIN_NAME = "NumberZapExt"
PLUGIN_PATH = os.path.dirname( __file__ )

def localeInit():
	lang = language.getLanguage()[:2]
	os.environ["LANGUAGE"] = lang
	gettext.bindtextdomain(PLUGIN_NAME, "%s/locale"%(PLUGIN_PATH))

def _(txt):
	t = gettext.dgettext(PLUGIN_NAME, txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)
