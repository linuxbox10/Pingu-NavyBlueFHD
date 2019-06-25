from inits import PluginLanguagePath

from inits import PluginLanguageDomain
from Components.Language import language
import gettext
from os import environ

def localeInit():
    lang = language.getLanguage()[:2]
    environ["LANGUAGE"] = lang
    gettext.bindtextdomain(PluginLanguageDomain, PluginLanguagePath)

def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
            t = gettext.gettext(txt)
    return t

localeInit()
language.addCallback(localeInit)
