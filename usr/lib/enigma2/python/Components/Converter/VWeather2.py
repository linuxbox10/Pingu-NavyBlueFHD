# -*- encoding: utf-8 -*-

# This is free software, you are allowed to
# modify it (if you keep the license),
# but you are not allowed to distribute/publish
# it without source code (this version and your modifications).
# This means you also have to distribute
# source code of your modifications.

#######################################################################
# AtileHD Weather for VU+
# Support: www.vuplus-support.org
# THX to iMaxxx (c) 2013 for base idea
# Extended MOD atreyou & deso1208 (c) Mai 2016
#######################################################################

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config, ConfigSubsection, ConfigNumber, ConfigSelection
from Components.Language import language
from twisted.web.client import getPage
from xml.dom.minidom import parseString
from enigma import eTimer

config.plugins.AtileHD = ConfigSubsection()
config.plugins.AtileHD.refreshInterval = ConfigNumber(default = "10")
config.plugins.AtileHD.woeid = ConfigNumber(default = "523920")
config.plugins.AtileHD.tempUnit = ConfigSelection(default = "Celsius", choices = [("Celsius", _("Celsius")),("Fahrenheit", _("Fahrenheit"))])

def localeInit():
	lang = language.getLanguage() #													getLanguage returns e.g. "fi_FI" for "language_country"
	# os.environ["LANGUAGE"] = lang[:2]
	# gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
	# gettext.textdomain("enigma2")
	# gettext.bindtextdomain("VWeather2", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/VWeather2/locale/")) #			po/mo files?
	return str(lang)

weather_data = None
current_language = localeInit()

class VWeather2(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		global weather_data
		if weather_data is None:
			weather_data = WeatherData()
		self.type = type

	@cached

	def getText(self):
		WeatherInfo = weather_data.WeatherInfo
		if self.type == "currentLocation":
			return WeatherInfo[self.type]
		elif self.type == "currentCountry":
			return WeatherInfo[self.type]
		elif self.type == "currentRegion":
			return WeatherInfo[self.type]
		elif self.type == "windChill":
			return WeatherInfo[self.type]
		elif self.type == "windDirectionShort":
			return WeatherInfo[self.type]
		elif self.type == "windDirectionLong":
			return WeatherInfo[self.type]
		elif self.type == "windSpeed":
			return WeatherInfo[self.type]
		elif self.type == "atmoHumidity":
			return WeatherInfo[self.type] + " %"
		elif self.type == "atmoPressure":
			return WeatherInfo[self.type] + " hpa"
		elif self.type == "atmoRising":
			return WeatherInfo[self.type]
		elif self.type == "atmoVisibility":
			return WeatherInfo[self.type]
		elif self.type == "astroSunrise":
			return WeatherInfo[self.type]
		elif self.type == "astroSunset":
			return WeatherInfo[self.type]
		elif self.type == "geoData":
			return WeatherInfo[self.type]
		elif self.type == "geoLat":
			return WeatherInfo[self.type]
		elif self.type == "geoLong":
			return WeatherInfo[self.type]
		elif self.type == "downloadDate":
			return WeatherInfo[self.type]
		elif self.type == "downloadTime":
			return WeatherInfo[self.type] + " °C"
		elif self.type == "currentWeatherTemp":
			return WeatherInfo[self.type]
		elif self.type == "currentWeatherText":
			return WeatherInfo[self.type]
		elif self.type == "currentWeatherCode":
			return WeatherInfo[self.type]
		elif self.type == "currentWeatherPicon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayCode":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayDay":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayDate":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayTempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayTempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayText":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayPicon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowCode":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowDay":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowDate":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowTempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowTempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowText":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowPicon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow4Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow4Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow4Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow4TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow4TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow4Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow4Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow5Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow5Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow5Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow5TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow5TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow5Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow5Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow6Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow6Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow6Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow6TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow6TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow6Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow6Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow7Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow7Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow7Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow7TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow7TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow7Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow7Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow8Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow8Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow8Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow8TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow8TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow8Text":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow8Picon":
			return WeatherInfo[self.type]
		elif self.type == "CF":
			return self.getCF()
		else:
			return ""

	def getCF(self):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			return ""
		else:
			return ""

	text = property(getText)

class WeatherData:
	def __init__(self):
		self.WeatherInfo = WeatherInfo = { 
			"currentLocation": "N/A",
			"currentCountry": "N/A",
			"currentRegion": "N/A",
			"windChill": "N/A",
			"windDirectionShort": "N/A",
			"windDirectionLong": "N/A",
			"windSpeed": "N/A",
			"atmoHumidity": "N/A",
			"atmoPressure": "N/A",
			"atmoRising": "N/A",
			"atmoVisibility": "N/A",
			"astroSunrise": "N/A",
			"astroSunset": "N/A",
			"geoData": "N/A",
			"geoLat": "N/A",
			"geoLong": "N/A",
			"downloadDate": "N/A",
			"downloadTime": "N/A",
			"currentWeatherCode": "(",
			"currentWeatherText": "N/A",
			"currentWeatherTemp": "0",
			"currentWeatherPicon": "3200",
			"forecastTodayCode": "(",
			"forecastTodayDay": "N/A",
			"forecastTodayDate": "N/A",
			"forecastTodayTempMin": "0",
			"forecastTodayTempMax": "0",
			"forecastTodayText": "N/A",
			"forecastTodayPicon": "3200",
			"forecastTomorrowCode": "(",
			"forecastTomorrowDay": "N/A",
			"forecastTomorrowDate": "N/A",
			"forecastTomorrowTempMin": "0",
			"forecastTomorrowTempMax": "0",
			"forecastTomorrowText": "N/A",
			"forecastTomorrowPicon": "3200",
			"forecastTomorrow1Code": "(",
			"forecastTomorrow1Day": "N/A",
			"forecastTomorrow1Date": "N/A",
			"forecastTomorrow1TempMin": "0",
			"forecastTomorrow1TempMax": "0",
			"forecastTomorrow1Text": "N/A",
			"forecastTomorrow1Picon": "3200",
			"forecastTomorrow2Code": "(",
			"forecastTomorrow2Day": "N/A",
			"forecastTomorrow2Date": "N/A",
			"forecastTomorrow2TempMin": "0",
			"forecastTomorrow2TempMax": "0",
			"forecastTomorrow2Text": "N/A",
			"forecastTomorrow2Picon": "3200",
			"forecastTomorrow3Code": "(",
			"forecastTomorrow3Day": "N/A",
			"forecastTomorrow3Date": "N/A",
			"forecastTomorrow3TempMin": "0",
			"forecastTomorrow3TempMax": "0",
			"forecastTomorrow3Text": "N/A",
			"forecastTomorrow3Picon": "3200",
			"forecastTomorrow4Code": "(",
			"forecastTomorrow4Day": "N/A",
			"forecastTomorrow4Date": "N/A",
			"forecastTomorrow4TempMin": "0",
			"forecastTomorrow4TempMax": "0",
			"forecastTomorrow4Text": "N/A",
			"forecastTomorrow4Picon": "3200",
			"forecastTomorrow5Code": "(",
			"forecastTomorrow5Day": "N/A",
			"forecastTomorrow5Date": "N/A",
			"forecastTomorrow5TempMin": "0",
			"forecastTomorrow5TempMax": "0",
			"forecastTomorrow5Text": "N/A",
			"forecastTomorrow5Picon": "3200",
			"forecastTomorrow6Code": "(",
			"forecastTomorrow6Day": "N/A",
			"forecastTomorrow6Date": "N/A",
			"forecastTomorrow6TempMin": "0",
			"forecastTomorrow6TempMax": "0",
			"forecastTomorrow6Text": "N/A",
			"forecastTomorrow6Picon": "3200",
			"forecastTomorrow7Code": "(",
			"forecastTomorrow7Day": "N/A",
			"forecastTomorrow7Date": "N/A",
			"forecastTomorrow7TempMin": "0",
			"forecastTomorrow7TempMax": "0",
			"forecastTomorrow7Text": "N/A",
			"forecastTomorrow7Picon": "3200",
			"forecastTomorrow8Code": "(",
			"forecastTomorrow8Day": "N/A",
			"forecastTomorrow8Date": "N/A",
			"forecastTomorrow8TempMin": "0",
			"forecastTomorrow8TempMax": "0",
			"forecastTomorrow8Text": "N/A",
			"forecastTomorrow8Picon": "3200",
		}
		if config.plugins.AtileHD.refreshInterval.value > 0:
			self.timer = eTimer()
			self.timer.callback.append(self.GetWeather)
			self.GetWeather()

	def downloadError(self, error = None):
		print "[WeatherUpdate] error fetching weather data"

	def GetWeather(self):
		timeout = config.plugins.AtileHD.refreshInterval.value * 1000 * 60
		if timeout > 0:
			self.timer.start(timeout, True)
			print "AtileHD lookup for ID " + str(config.plugins.AtileHD.woeid.value)
			url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D%22"+str(config.plugins.AtileHD.woeid.value)+"%22&format=xml"
			getPage(url,method = "GET").addCallback(self.GotWeatherData).addErrback(self.downloadError)

	def GotWeatherData(self, data = None):
		if data is not None:
			dom = parseString(data)

			weather = dom.getElementsByTagName("yweather:location")[0]
			self.WeatherInfo["currentLocation"] = self.ConvertCity(weather.getAttributeNode("city").nodeValue)
			self.WeatherInfo["currentCountry"] = self.ConvertCountry(weather.getAttributeNode("country").nodeValue)
			self.WeatherInfo["currentRegion"] = self.ConvertRegion(weather.getAttributeNode("region").nodeValue)

			weather = dom.getElementsByTagName("yweather:wind")[0]
			self.WeatherInfo["windChill"] = self.ConvertTemp(weather.getAttributeNode("chill").nodeValue)
			self.WeatherInfo["windDirectionShort"] = self.ConvertDirectionShort(weather.getAttributeNode("direction").nodeValue)
			self.WeatherInfo["windDirectionLong"] = self.ConvertDirectionLong(weather.getAttributeNode("direction").nodeValue)
			self.WeatherInfo["windSpeed"] =  self.ConvertSpeed(weather.getAttributeNode("speed").nodeValue)

			weather = dom.getElementsByTagName("yweather:atmosphere")[0]
			self.WeatherInfo["atmoHumidity"] = _(str(weather.getAttributeNode("humidity").nodeValue))
			self.WeatherInfo["atmoPressure"] = _(str(weather.getAttributeNode("pressure").nodeValue).split(".")[0])
			self.WeatherInfo["atmoRising"] = self.ConvertRise(weather.getAttributeNode("rising").nodeValue)
			self.WeatherInfo["atmoVisibility"] = self.ConvertVisibility(weather.getAttributeNode("visibility").nodeValue)

			weather = dom.getElementsByTagName("yweather:astronomy")[0]
			self.WeatherInfo["astroSunrise"] = self.ConvertTime(weather.getAttributeNode("sunrise").nodeValue)
			self.WeatherInfo["astroSunset"] = self.ConvertTime(weather.getAttributeNode("sunset").nodeValue)

			geoLat = dom.getElementsByTagName("geo:lat")
			self.WeatherInfo["geoLat"] = self.ConvertGeoLat(str(geoLat[0].firstChild.nodeValue))
			geoLong = dom.getElementsByTagName("geo:long")
			self.WeatherInfo["geoLong"] = self.ConvertGeoLong(str(geoLong[0].firstChild.nodeValue))
			self.WeatherInfo["geoData"] = self.ConvertGeoLat(str(geoLat[0].firstChild.nodeValue)) + " / " + self.ConvertGeoLong(str(geoLong[0].firstChild.nodeValue))

			weather = dom.getElementsByTagName("yweather:condition")[0]
			self.WeatherInfo["downloadDate"] = self.ConvertDownloadDate(weather.getAttributeNode("date").nodeValue)
			self.WeatherInfo["downloadTime"] = self.ConvertDownloadTime(weather.getAttributeNode("date").nodeValue)
			self.WeatherInfo["currentWeatherCode"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["currentWeatherTemp"] = self.ConvertTemp(weather.getAttributeNode("temp").nodeValue)
			self.WeatherInfo["currentWeatherText"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["currentWeatherPicon"] = _(str(weather.getAttributeNode("code").nodeValue))

			weather = dom.getElementsByTagName("yweather:forecast")[0]
			self.WeatherInfo["forecastTodayCode"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTodayDay"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTodayDate"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTodayTempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTodayTempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTodayText"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTodayPicon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[1]
			self.WeatherInfo["forecastTomorrowCode"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrowDay"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrowDate"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrowTempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrowTempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrowText"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrowPicon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[2]
			self.WeatherInfo["forecastTomorrow1Code"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrow1Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow1Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow1TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow1TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow1Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow1Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[3]
			self.WeatherInfo["forecastTomorrow2Code"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrow2Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow2Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow2TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow2TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow2Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow2Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[4]
			self.WeatherInfo["forecastTomorrow3Code"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrow3Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow3Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow3TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow3TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow3Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow3Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[5]
			self.WeatherInfo["forecastTomorrow4Code"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrow4Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow4Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow4TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow4TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow4Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow4Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[6]
			self.WeatherInfo["forecastTomorrow5Code"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrow5Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow5Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow5TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow5TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow5Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow5Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[7]
			self.WeatherInfo["forecastTomorrow6Code"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrow6Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow6Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow6TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow6TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow6Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow6Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[8]
			self.WeatherInfo["forecastTomorrow7Code"] = self.ConvertCondition(weather.getAttributeNode('code').nodeValue)
			self.WeatherInfo["forecastTomorrow7Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow7Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow7TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow7TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow7Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow7Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

			weather = dom.getElementsByTagName('yweather:forecast')[9]
			self.WeatherInfo["forecastTomorrow8Code"] = self.ConvertCondition(weather.getAttributeNode("code").nodeValue)
			self.WeatherInfo["forecastTomorrow8Day"] = self.ConvertDay(weather.getAttributeNode("day").nodeValue)
			self.WeatherInfo["forecastTomorrow8Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow8TempMax"] = self.ConvertTemp(weather.getAttributeNode("high").nodeValue)
			self.WeatherInfo["forecastTomorrow8TempMin"] = self.ConvertTemp(weather.getAttributeNode("low").nodeValue)
			self.WeatherInfo["forecastTomorrow8Text"] = self.ConvertInfo(weather.getAttributeNode("text").nodeValue)
			self.WeatherInfo["forecastTomorrow8Picon"] = _(str(weather.getAttributeNode("code").nodeValue)) 

	def getText(self,nodelist):
		rc = []
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc.append(node.data)
			return "".join(rc)

	def getWeatherDate(self, weather):
		cur_weather = str(weather.getAttributeNode('date').nodeValue).split(" ")
		str_weather = cur_weather[0]
		if len(cur_weather) >= 2:
			str_weather += ". " + _(cur_weather[1])
		return str_weather

	def ConvertCondition(self, code):
		code = int(code)
	#	Keine Daten
		condition = "("
	#	0 Tornado, 1 Tropical Storm, 2 Hurricane
		if code == 0 or code == 1 or code == 2:
			condition = "F"
	#	3 Severe Thunderstorms
		elif code == 3:
			condition = "0"
	#	4 Thunderstorms
		elif code == 4:
			condition = "Z"
	#	5 Mixed Rain and Snow, 6 Mixed Rain and Sleet, 35 Mixed Rain and Hail
		elif code == 5  or code == 6 or code == 35:
			condition = "W"
	#	8 Freezing Drizzle, 9 Drizzle, 10 Freezing Rain, 18 Sleet
		elif code == 8 or code == 9 or code == 10 or code == 18:
			condition = "U"
	#	17 Hail
		elif code == 17:
			condition = "V"
	#	25 Cold
		elif code == 25:
			condition = "G"
	#	11 Showers, 12 Rain
		elif code == 11 or code == 12:
			condition = "R"
	#	39 Scattered Showers, 40 Scattered Showers
		elif code == 39 or code == 40:
			condition = "Q"
	#	7 Snow Sleet, 13 Snow Flurries, 14 Light Snow Showers, 15 Blowing Snow, 16 Snow
	#	41 Heavy Snow, 42 Scattered Snow Showers, 43 Heavy Snow, 46 Snow Showers
		elif code == 7 or code == 13 or code == 14 or code == 15 or code == 16 or code == 41 or code == 42 or code == 43 or code == 46:
			condition = "X"
	#	19 Dusty, 22 Smoky
		elif code == 19 or code == 22:
			condition = "E"
	#	20 Foggy, 21 Hazel
		elif code == 20 or code == 21:
			condition = "M"
	#	23 Breezy, 24 Windy
		elif code == 23 or code == 24:
			condition = "F"
	#	26 Cloudy, 27 Mostly Cloudy (night), 28 Mostly Cloudy (day)
		elif code == 26 or code == 27 or code == 28:
			condition = "Y"
	#	29 Partly Cloudy (night)
		elif code == 29:
			condition = "I"
	#	30 Partly Cloudy (day)
		elif code == 30:
			condition = "H"
	#	44 Partly Cloudy
		elif code == 44:
			condition = "N"
	#	31 Clear (night), 33 Mostly Clear (night)
		elif code == 31 or code == 33:
			condition = "C"
	#	32 Sunny (day), 34 Mostly Sunny (day), 36 Hot
		elif code == 32 or code == 34 or code == 36:
			condition = "B"
	#	37 Isolated Thunderstorms, 38 Isolated Thunderstorms
		elif code == 37 or code == 38:
			condition = "O"
	#	45 Thundershowers, 47 Scattered Thundershowers
		elif code == 45 or code == 47:
			condition = "P"
	#	3200 N/A
		else:
			condition = ")"
		return str(condition)

	def ConvertInfo(self, text):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			text = text
		else:
			if text == "Tornado":
					text = "Tornado"
			elif text == "Tropical Storm":
					text = "Tropischer Sturm"
			elif text == "Hurricane":
					text = "Wirbelsturm"
			elif text == "Severe Thunderstorms":
					text = "Schwere Gewitterstürme"
			elif text == "Thunderstorms":
					text = "Gewitterstürme"
			elif text == "Rain And Snow":
					text = "Schneeregen"
			elif text == "Rain And Sleet":
					text = "Regen mit Graupel"
			elif text == "Snow And Sleet":
					text = "Schnee mit Graupel"
			elif text == "Freezing Drizzle":
					text = "Gefrierende Nieselregen"
			elif text == "Drizzle":
					text = "Nieselregen"
			elif text == "Freezing Rain":
					text = "Eisregen"
			elif text == "Showers":
					text = "Regenschauer"
			elif text == "Rain":
					text = "Regen"
			elif text == "Snow Flurries":
					text = "Leichter Schneefall"
			elif text == "Light Snow Showers":
					text = "Leichte Schneeschauer"
			elif text == "Blowing Snow":
					text = "Schneesturm"
			elif text == "Snow":
					text = "Schneefall"
			elif text == "Hail":
					text = "Hagel"
			elif text == "Sleet":
					text = "Graupel"
			elif text == "Dust":
					text = "Staubig"
			elif text == "Foggy":
					text = "Neblig"
			elif text == "Haze":
					text = "Dunstig"
			elif text == "Smoky":
					text = "Rauchbildung"
			elif text == "Breezy":
					text = "Stürmisch"
			elif text == "Windy":
					text = "Windig"
			elif text == "Cold":
					text = "Kalt"
			elif text == "Cloudy":
					text = "Bewölkt"
			elif text == "Mostly Cloudy":
					text = "Überwiegend Bewölkt"
			elif text == "Partly Cloudy":
					text = "Leicht Bewölkt"
			elif text == "Clear":
					text = "Klar"
			elif text == "Mostly Clear":
					text = "Überwiegend Klar"
			elif text == "Sunny":
					text = "Sonnig"
			elif text == "Mostly Sunny":
					text = "Überwiegend Sonnig"
			elif text == "Rain And Hail":
					text = "Regen mit Hagel"
			elif text == "Hot":
					text = "Heiss"
			elif text == "Isolated Thunderstorms":
					text = "Lokale Gewitter"
			elif text == "Scattered Thunderstorms":
					text = "Vereinzelte Gewitter"
			elif text == "Scattered Showers":
					text = "Vereinzelte Regenschauer"
			elif text == "Heavy Snow":
					text = "Schwerer Schneefall"
			elif text == "Scattered Snow Showers":
					text = "Vereinzelter Schneefall"
			elif text == "Thundershowers":
					text = "Gewitterschauer"
			elif text == "Snow Showers":
					text = "Schneeschauer"
			elif text == "Isolated Thundershowers":
					text = "Lokale Gewitterschauer"
			else:
					text = "N/A"
		return str(text)

	def ConvertDirectionShort(self, direction):
			dir = int(direction)
			if dir >= 0 and dir <= 20:
					direction = "N"
			elif dir >= 21 and dir <= 35:
					direction = "NNO"
			elif dir >= 36 and dir <= 55:
					direction = "NO"
			elif dir >= 56 and dir <= 70:
					direction = "ONO"
			elif dir >= 71 and dir <= 110:
					direction = "O"
			elif dir >= 111 and dir <= 125:
					direction = "OSO"
			elif dir >= 126 and dir <= 145:
					direction = "SO"
			elif dir >= 146 and dir <= 160:
					direction = "SSO"
			elif dir >= 161 and dir <= 200:
					direction = "S"
			elif dir >= 201 and dir <= 215:
					direction = "SSW"
			elif dir >= 216 and dir <= 235:
					direction = "SW"
			elif dir >= 236 and dir <= 250:
					direction = "WSW"
			elif dir >= 251 and dir <= 290:
					direction = "W"
			elif dir >= 291 and dir <= 305:
					direction = "WNW"
			elif dir >= 306 and dir <= 325:
					direction = "NW"
			elif dir >= 326 and dir <= 340:
					direction = "NNW"
			elif dir >= 341 and dir <= 360:
					direction = "N"
			else:
					direction = "N/A"
			return str(direction)

	def ConvertDirectionLong(self, direction):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			dir = int(direction)
			if dir >= 0 and dir <= 20:
					direction = "North"
			elif dir >= 21 and dir <= 35:
					direction = "North-Northeast"
			elif dir >= 36 and dir <= 55:
					direction = "Northeast"
			elif dir >= 56 and dir <= 70:
					direction = "East-Nordeast"
			elif dir >= 71 and dir <= 110:
					direction = "East"
			elif dir >= 111 and dir <= 125:
					direction = "East-Southeast"
			elif dir >= 126 and dir <= 145:
					direction = "Southeast"
			elif dir >= 146 and dir <= 160:
					direction = "South-Southeast"
			elif dir >= 161 and dir <= 200:
					direction = "South"
			elif dir >= 201 and dir <= 215:
					direction = "South-Southwest"
			elif dir >= 216 and dir <= 235:
					direction = "Southwest"
			elif dir >= 236 and dir <= 250:
					direction = "West-Southwest"
			elif dir >= 251 and dir <= 290:
					direction = "West"
			elif dir >= 291 and dir <= 305:
					direction = "West-Northwest"
			elif dir >= 306 and dir <= 325:
					direction = "Northwest"
			elif dir >= 326 and dir <= 340:
					direction = "North-Northwest"
			elif dir >= 341 and dir <= 360:
					direction = "North"
			else:
					direction = "N/A"
		else:
			dir = int(direction)
			if dir >= 0 and dir <= 20:
					direction = "Nord"
			elif dir >= 21 and dir <= 35:
					direction = "Nord-Nordost"
			elif dir >= 36 and dir <= 55:
					direction = "Nordost"
			elif dir >= 56 and dir <= 70:
					direction = "Ost-Nordost"
			elif dir >= 71 and dir <= 110:
					direction = "Ost"
			elif dir >= 111 and dir <= 125:
					direction = "Ost-Südost"
			elif dir >= 126 and dir <= 145:
					direction = "Südost"
			elif dir >= 146 and dir <= 160:
					direction = "Süd-Südost"
			elif dir >= 161 and dir <= 200:
					direction = "Süd"
			elif dir >= 201 and dir <= 215:
					direction = "Süd-Südwest"
			elif dir >= 216 and dir <= 235:
					direction = "Südwest"
			elif dir >= 236 and dir <= 250:
					direction = "West-Südwest"
			elif dir >= 251 and dir <= 290:
					direction = "West"
			elif dir >= 291 and dir <= 305:
					direction = "West-Nordwest"
			elif dir >= 306 and dir <= 325:
					direction = "Nordwest"
			elif dir >= 326 and dir <= 340:
					direction = "Nord-Nordwest"
			elif dir >= 341 and dir <= 360:
					direction = "Nord"
			else:
					direction = "N/A"
		return str(direction)

	def ConvertDay(self, day):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			if day == "Mon":
					day = "Monday"
			elif day == "Tue":
					day = "Tuesday"
			elif day == "Wed":
					day = "Wednesday"
			elif day == "Thu":
					day = "Thursday"
			elif day == "Fri":
					day = "Friday"
			elif day == "Sat":
					day = "Saturday"
			elif day == "Sun":
					day = "Sunday"
			else:
					day = "N/A"
		else:
			if day == "Mon":
					day = "Montag"
			elif day == "Tue":
					day = "Dienstag"
			elif day == "Wed":
					day = "Mittwoch"
			elif day == "Thu":
					day = "Donnerstag"
			elif day == "Fri":
					day = "Freitag"
			elif day == "Sat":
					day = "Samstag"
			elif day == "Sun":
					day = "Sonntag"
			else:
					day = "N/A"
		return str(day)

	def ConvertRegion(self, region):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			region = region
		else:
			if region == " BW" or region == " Baden-Wurttemberg":
					region = "Baden-Württemberg"
			elif region == " BY" or region == " Bavaria":
					region = "Bayern"
			elif region == " BE" or region == " Berlin":
					region = "Berlin"
			elif region == " BB" or region == " Brandenburg":
					region = "Brandenburg"
			elif region == " HB" or region == " Bremen":
					region = "Bremen"
			elif region == " HH" or region == " Hamburg":
					region = "Hamburg"
			elif region == " HE" or region == " Hesse":
					region = "Hessen"
			elif region == " MV" or region == " Mecklenburg-Vorpommern":
					region = "Mecklenburg-Vorpommern"
			elif region == " NI" or region == " Lower Saxony":
					region = "Niedersachsen"
			elif region == " NW" or region == " North Rhine-Westphalia":
					region = "Nordrhein-Westfalen"
			elif region == " RP" or region == " Rhineland-Palatinate":
					region = "Rheinland-Pfalz"
			elif region == " SL" or region == " Saarland":
					region = "Saarland"
			elif region == " SN" or region == " Saxony":
					region = "Sachsen"
			elif region == " ST" or region == " Saxony-Anhalt":
					region = "Sachsen-Anhalt"
			elif region == " SH" or region == " Schleswig-Holstein":
					region = "Schleswig-Holstein"
			elif region == " TH" or region == " Thuringia":
					region = "Thüringen"
			else:
					region = region
		return str(region)

	def ConvertCountry(self, country):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			country = country
		else:
			if country == "Germany":
					country = "Deutschland"
#			elif country == "Netherlands": #										Startpoint for evt. expansion
#					country = "Nederland"
			else:
				country = country
		return str(country)

	def ConvertCity(self, city):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			city = city
		else:
			if city == "Cologne":
				city = "Köln"
#			elif city == "Munich":  #												Startpoint for evt. expansion
#				city = "München"
			else:
				city = city
		return str(city)

	def ConvertRise(self, rise):
		if rise == -1:
				rise = "<<"
		elif rise == 1:
				rise = ">>"
		else:
				rise = ""
		return str(rise)

#	The below used 12/24 Hr time convert routine is not generic valid (OK for the Sunrise and Sunset values)
	def ConvertTime(self, time):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			parts = time.split()
			time3, time4 = parts[0], parts[1]
			parts = time3.split(":")
			time1, time2 = parts[0], parts[1]
			if len(time1) < 2:
				time1 = "0" + time1
			if len(time2) < 2:
				time2 = "0" + time2
			if time4 == "am":
				time = str(time1) + ":" + str(time2) + str(time4.replace("am", " AM"))
			else:
				time = str(time1) + ":" + str(time2) + str(time4.replace("pm", " PM"))
		else:
			parts = time.split()
			time3, time4 = parts[0], parts[1]
			parts = time3.split(":")
			time1, time2 = parts[0], parts[1]
			if len(time1) < 2:
				time1 = "0" + time1
			if len(time2) < 2:
				time2 = "0" + time2
			if time4 == "am":
				time = str(time1) + ":" + str(time2) + str(time4.replace("am", " Uhr"))
			else:
				time1 = int(time1) + 12
				time = str(time1) + ":" + str(time2) + str(time4.replace("pm", " Uhr"))
		return str(time)

	def ConvertDownloadDate(self, date):
#		date = "Fri, 29 Apr 2016 12:00 PM CEST" #								Debug source
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			date = str(date[8:11] + date[4:7] + ", "+ date[12:16]) #			Update date as: "May 02, 2016"
		else:
			date = str(date[5:7]) + ". " + str(self.ConvertMonth(date[8:11])) + " " + str(date[12:16]) # Update date as: "02. Mai 2016" 
		return str(date)

	def ConvertDownloadTime(self, time):
#		time = "Fri, 29 Apr 2016 01:00 PM CEST" #								Debug source
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			time = str(time[17:25]) #											Update time as: "08:43 AM/PM"
		else:
			parts = time[17:25].split()
			time3, time4 = parts[0], parts[1]
			parts = time3.split(":")
			time1, time2 = parts[0], parts[1]
			if time4 == "AM":
				if int(time1) > 11:
					time = str("00") + ":" + str(time2) + str(time4.replace("AM", " Uhr"))
				else:
					time = str(time1) + ":" + str(time2) + str(time4.replace("AM", " Uhr"))
			else:
				if int(time1) > 11:
					time = str(time1) + ":" + str(time2) + str(time4.replace("PM", " Uhr"))
				else:
					time = str(int(time1) + 12) + ":" + str(time2) + str(time4.replace("PM", " Uhr"))
		return str(time)

	def ConvertMonth(self, month):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			month = month
		else:
			if month == "May":
				month = "Mai"
			elif month == "Oct":
				month = "Okt"
			elif month == "Dec":
				month = "Dez"
			else:
				month = month
		return str(month)

	def ConvertTemp(self, temp):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			return str(int(temp)) + "°F"
		else:
			return str(int(round((float(temp) -32) * 5/9))) + "°C"

	def ConvertSpeed(self, speed):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			return str(int(round(float(speed) * 621371 / 1000000))) + " mpH"
		else:
			return str(int(round(float(speed)))) + " km/h"
#			return str(round(float(speed), 1)) + " km/h"						Sample added decimal values

	def ConvertVisibility(self, vision):
		if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
			return str(int(round(float(vision) * 621371 / 1000000))) + " miles"
		else:
			return str(int(round(float(vision)))) + " km"

	def ConvertGeoLat(self, geolat):
		geolat = float(geolat)
		if geolat >= 0:
			lat = "N"
		else:
			lat = "S"
		geolat = str(round(float(abs(geolat)), 2))
		return str(geolat.replace(".", "°")) + "' " + str(lat)
		
	def ConvertGeoLong(self, geolong):
		geolong = float(geolong)
		if geolong >= 0:
			if config.plugins.AtileHD.tempUnit.value == "Fahrenheit":
				long = "E"
			else:
				long = "O"
		else:
			long = "W"
		geolong = str(round(float(abs(geolong)), 2))
		return str(geolong.replace(".", "°")) + "' " + str(long)
