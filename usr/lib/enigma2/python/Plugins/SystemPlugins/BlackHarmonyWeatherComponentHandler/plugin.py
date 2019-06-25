from Plugins.Plugin import PluginDescriptor

def sessionstart(session, **kwargs):
    try:
        from Components.Sources.BlackHarmonyMSNWeather import BlackHarmonyMSNWeather
        session.screen['BlackHarmonyMSNWeather'] = BlackHarmonyMSNWeather()
    except Exception, e:
        print "Exception: %s" % str(e)


def Plugins(**kwargs):
    return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart)]