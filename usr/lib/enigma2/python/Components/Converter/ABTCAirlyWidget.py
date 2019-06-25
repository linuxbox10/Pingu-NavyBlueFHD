# -*- coding: utf-8 -*-
#						   Airly Polska
#					Based on http://map.airly.eu
#							 1.0-r18
#
#    Copyright (C) 2018  Ampersand
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
from Components.Converter.Converter import Converter
from enigma import eTimer
from Components.Element import cached
from Poll import Poll
from Tools.Directories import fileExists
import os, datetime
from os import path

TMP_PATH = "/tmp"

class ABTCAirlyWidget(Poll, Converter, object):
	PM1 = 1
	PM25 = 2
	PM10 = 3
	PRES = 4
	HUM = 5
	TEMP = 6
	CAQI = 7
	INDEXBACKPNG = 8
	SCHTIME = 9
	HOMEID = 10
	CITY = 11
	STREET = 12

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.type = {
			"pm1": self.PM1,
			"pm25": self.PM25,
			"pm10": self.PM10,
			"pres": self.PRES,
			"hum": self.HUM,
			"temp": self.TEMP,
			"caqi": self.CAQI,
			"indexBackPNG": self.INDEXBACKPNG,
			"schtime": self.SCHTIME,
			"homeid": self.HOMEID,
			"city": self.CITY,
			"street": self.STREET
		}[type]
		self.DynamicTimer = eTimer()
		self.DynamicTimer.callback.append(self.doSwitch)
			
	def getPm1Value(self):
		pm1 = ''
		pmunits = ' \xB5g/m\xB3'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pm1 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "PM1:" in item:
						pm1 = item.strip().split(':')[1]
						pm11 = pm1.split('.')[0]
						pm12 = pm1.split('.')[1]
						if int(pm12[0]) >= 5:
							pm1 = int(float(pm1))
							pm1 += 1
							pm1 = 'PM1: ' + str(pm1) + pmunits
						else:
							pm1 = pm11
							pm1 = 'PM1: ' + str(pm1) + pmunits
			except:
				pm1 = ''
		else:
			pm1 = ''
		return pm1
		
	def getPm25Value(self):
		pm25 = ''
		pmunits = ' \xB5g/m\xB3'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pm25 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "PM25:" in item:
						pm25 = item.strip().split(':')[1]
						pm251 = pm25.split('.')[0]
						pm252 = pm25.split('.')[1]
						if int(pm252[0]) >= 5:
							pm25 = int(float(pm25))
							pm25 += 1
							pm25 = 'PM2.5: ' + str(pm25) + pmunits
						else:
							pm25 = pm251
							pm25 = 'PM2.5: ' + str(pm25) + pmunits
			except:
				pm25 = ''
		else:
			pm25 = ''
		return pm25
		
	def getPm10Value(self):
		pm10 = ''
		pmunits = ' \xB5g/m\xB3'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pm10 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "PM10:" in item:
						pm10 = item.strip().split(':')[1]
						pm101 = pm10.split('.')[0]
						pm102 = pm10.split('.')[1]
						if int(pm102[0]) >= 5:
							pm10 = int(float(pm10))
							pm10 += 1
							pm10 = 'PM10: ' + str(pm10) + pmunits
						else:
							pm10 = pm101
							pm10 = 'PM10: ' + str(pm10) + pmunits
			except:
				pm10 = ''
		else:
			pm10 = ''
		return pm10
		
	def getTempValue(self):
		temp = ''
		tempunits = ' °C'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			temp = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "TEMPERATURE:" in item:
						temp = item.strip().split(':')[1]
						temp1 = temp.split('.')[0]
						temp2 = temp.split('.')[1]
						if int(temp2[0]) >= 5:
							if temp.startswith('-'):
								temp = int(float(temp))
								temp -= 1
								temp = str(temp) + tempunits
							else:
								temp = int(float(temp))
								temp += 1
								temp = str(temp) + tempunits
						else:
							if temp.startswith('-0'):
								temp = temp1[1]
								temp = str(temp) + tempunits
							else:
								temp = temp1
								temp = str(temp) + tempunits
			except:
				temp = ''	
		else:
			temp = ''
		return temp
		
	def getPresValue(self):
		pres = ''
		preunits = ' hPa'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pres = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "PRESSURE:" in item:
						pres = item.strip().split(':')[1]
						pres1 = pres.split('.')[0]
						pres2 = pres.split('.')[1]
						if int(pres2[0]) >= 5:
							pres = int(float(pres))
							pres += 1
							pres = str(pres) + preunits
						else:
							pres = pres1
							pres = str(pres) + preunits
			except:
				pres = ''
		else:
			pres = ''
		return pres
		
	def getHumValue(self):
		hum = ''
		huunits = ' %'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			hum = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "HUMIDITY:" in item:
						hum = item.strip().split(':')[1]
						hum1 = hum.split('.')[0]
						hum2 = hum.split('.')[1]
						if int(hum2[0]) >= 5:
							hum = int(float(hum))
							hum += 1
							hum = str(hum) + huunits
						else:
							hum = hum1
							hum = str(hum) + huunits
			except:
				hum = ''
		else:
			hum = ''
		return hum
		
	def getCaqiValue(self):
		caqi = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			caqi = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "AIRLY_CAQI:" in item:
						caqi = item.strip().split(':')[1]
						caqi1 = caqi.split('.')[0]
						caqi2 = caqi.split('.')[1]
						if int(caqi2[0]) >= 5:
							caqi = int(float(caqi))
							caqi += 1
							caqi = str(caqi)
						else:
							caqi = caqi1
							caqi = str(caqi)
			except:
				caqi = ''
		else:
			caqi = ''
		return caqi
		
	def getIndexBackPNGValue(self):
		level = ''
		indexBackPNG = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/0.png'
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "level:" in item:
						level = item.strip().split(':')[1]
				if level == 'VERY_LOW':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/1.png'
				elif level == 'LOW':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/2.png'
				elif level == 'MEDIUM':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/3.png'
				elif level == 'HIGH':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/4.png'
				elif level == 'VERY_HIGH':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/5.png'
				elif level == 'EXTREME':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/6.png'
				elif level == 'AIRMAGEDDON':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/7.png'
				else:
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/0.png'
			except:
				pass
		else:
			indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/AirlyPoland/gfx/indexbacks/0.png'
		return indexBackPNG
			
	def getSchTime(self):
		if fileExists(TMP_PATH + '/airly.sch'):
			TIME_FORMAT = '%Y-%m-%d  %H:%M'
			t = os.path.getmtime(TMP_PATH + '/airly.sch')
			return str(datetime.datetime.fromtimestamp(t).strftime(TIME_FORMAT))
			
	def getIDValue(self):
		homeid = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			homeid = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "id:" in item:
						homeid = item.strip().split(':')[1]
						homeid = 'ID: ' + str(homeid)
				for item in output:
					if "mode:" in item:
						homeid = 'ID:Brak (Pomiar interpolowany)'
				homeid = str(homeid)
			except:
				homeid = ''
		else:
			homeid = ''
		return homeid
		
	def getCityValue(self):
		city = ''
		title = 'Airly Polska'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			city = title
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "city:" in item:
						city = item.strip().split(':')[1]
			except:
				city = ''
		else:
			city = title
		return city
		
	def getStreetValue(self):
		street = ''
		number = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			street = ''
			number = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				f = open(TMP_PATH + '/airly.sch', 'rb')
				output = f.readlines()
				f.close()
				for item in output:
					if "street:" in item:
						street = item.strip().split(':')[1]
				for item in output:
					if "number:" in item:
						number = item.strip().split(':')[1]
				street = str(street) + ' ' + str(number)
			except:
				street = ''
		else:
			street = ''
		return street
		
	@cached
	def getText(self):
		self.DynamicTimer.start(500)
		
		if self.type == self.PM1:
			return self.getPm1Value()
		elif self.type == self.PM25:
			return self.getPm25Value()
		elif self.type == self.PM10:
			return self.getPm10Value()
		elif self.type == self.TEMP :
			return self.getTempValue()
		elif self.type == self.PRES :
			return self.getPresValue()
		elif self.type == self.HUM :
			return self.getHumValue()
		elif self.type == self.CAQI :
			return self.getCaqiValue()
		elif self.type == self.SCHTIME :
			return self.getSchTime()
		elif self.type == self.HOMEID :
			return self.getIDValue()
		elif self.type == self.CITY :
			return self.getCityValue()
		elif self.type == self.STREET :
			return self.getStreetValue()

	text = property(getText)
	
	@cached
	def getIconFilename(self):
		if self.type == self.INDEXBACKPNG :
			return self.getIndexBackPNGValue()
			
	iconfilename = property(getIconFilename)

	def changed(self, what):
		self.what = what
		Converter.changed(self, what)

	def doSwitch(self):
		self.DynamicTimer.stop()
		Converter.changed(self, self.what)
