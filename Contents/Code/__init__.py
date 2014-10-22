# -*- coding: utf-8 -*-
import datetime

NAME 		= 'OpenWeatherMap'
API_URL		= 'http://api.openweathermap.org/data/2.5/%s?q='
GEOIP_URL	= 'http://freegeoip.net/json/'

ART		= 'art-default.jpg'
ICON		= 'icon-default.png'
ICON_PARENT	= 'icon-parent.png'
UNKNOWN 	= 'NoData'

###################################################################################################
def ConstructURL():

	# Location
	if (Prefs['location1'] == "Geolocation"):
		geoip_req = JSON.ObjectFromURL(GEOIP_URL)
		geoip_loc = geoip_req['city'] + ',' + geoip_req['country_code']
		WEATHER_API_URL = API_URL + geoip_loc
	else:
		WEATHER_API_URL = API_URL + Prefs['location1']

	# Units
	if (Prefs['use_celsius']):
		WEATHER_API_URL += '&units=metric'
	else:
		WEATHER_API_URL += '&units=imperial'

	# Language
	if (Prefs['use_language']):
		WEATHER_API_URL += '&lang=' + Prefs['use_language']
	else:
		WEATHER_API_URL += '&lang=en'

	return WEATHER_API_URL

###################################################################################################
def Start():

  ObjectContainer.title1 = NAME
  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-Agent'] = 'PLEX/OpenWeatherMap'

###################################################################################################
@handler('/video/openweathermap', NAME)
def MainMenu():

	oc = ObjectContainer()
  
	oc.add(
		DirectoryObject(
			key=Callback(current, title="Current Weather", day='weather'),
			title='Current',
			tagline='Current Weather',
			summary='Current Weather',
			thumb = R(ICON_PARENT),
			art = R(ART)
		)
	)
	oc.add(
		DirectoryObject(
			key=Callback(hourly, title="Hourly Forecast", day='forecast'),
			title='Hourly',
			tagline='Hourly Forecast',
			summary='Hourly Forecast',
			thumb = R(ICON_PARENT),
			art = R(ART)
		)
	)
	oc.add(
		DirectoryObject(
			key=Callback(daily, title="Daily Forecast", day='forecast/daily'),
			title='Daily',
			tagline='Daily Forecast',
			summary='Daily Forecast',
			thumb = R(ICON_PARENT),
			art = R(ART)
		)
	)
	oc.add(
		PrefsObject(
			title='Preferences',
			thumb = R(ICON_PARENT),
			art = R(ART)
		)
	)

	return oc

###################################################################################################
@route('/video/openweathermap/current')
def current(title, day):

	oc = ObjectContainer(title2=title)
	query_string = '%s' % (day)

	result = JSON.ObjectFromURL(ConstructURL() % (query_string))

	# Units
	if (Prefs['use_celsius']):
	  TEMP_UNIT	= u'\N{DEGREE SIGN}C' 
	  SPEED_UNIT	= ' km/h'
	else:
	  TEMP_UNIT	= u'\N{DEGREE SIGN}F' 
	  SPEED_UNIT	= ' mph'

	if (Prefs['use_24hour']):
	  TIME_UNIT	= '%H:%M'
	else:
  	  TIME_UNIT	= '%I:%M %p'

	# Parsing
	object_location = str(result['name'] + ', ' + result['sys']['country'])

	for object in result['weather']:
		object_cond_short = object['main']
		object_cond_long  = object['description']
		object_cond_icon  = object['icon'] + '_icon.png'
		object_cond_art   = object['icon'] + '_art.jpg'

	object_temp_rnd = round(result['main']['temp'],1)
	object_temp_cur = str(object_temp_rnd) + TEMP_UNIT
	object_temp_rnd = round(result['main']['temp_min'],1)
	object_temp_min = str(object_temp_rnd) + TEMP_UNIT
	object_temp_rnd = round(result['main']['temp_max'],1)
	object_temp_max = str(object_temp_rnd) + TEMP_UNIT

	object_sunrise_unixtime	= result['sys']['sunrise']
	object_sunrise_datetime	= datetime.datetime.fromtimestamp(object_sunrise_unixtime)
	object_sunrise		= str(object_sunrise_datetime.strftime(TIME_UNIT))

	object_sunset_unixtime	= result['sys']['sunset']
	object_sunset_datetime	= datetime.datetime.fromtimestamp(object_sunset_unixtime)
	object_sunset		= str(object_sunset_datetime.strftime(TIME_UNIT))

	object_pressure = str(result['main']['pressure']) + ' hPa'
	object_humidity = str(result['main']['humidity']) + '%'
	object_clouds	= str(result['clouds']['all']) + '%'

	object_windspeed	= str(result['wind']['speed']) + SPEED_UNIT

	object_temp_summary	= 'Min:' + object_temp_min + '\nMax:' + object_temp_max
	object_loc_summary	= 'Sunrise:' + object_sunrise + '\nSunset:' + object_sunset
	object_cond_summary	= object_cond_long + ' (' + object_clouds + ')' + '\nWind: ' + object_windspeed + '\nPressure: ' + object_pressure + '\nHumidity: ' + object_humidity

	# Location
	oc.add(DirectoryObject(
		title = object_location,
		thumb = R(object_cond_icon),
		art = R(object_cond_art),
		summary = object_loc_summary
	))

	# Condition
	oc.add(DirectoryObject(
		title = object_cond_short,
		thumb = R(object_cond_icon),
		art = R(object_cond_art),
		summary = object_cond_summary
	))

	# Temperature
	oc.add(DirectoryObject(
		title = object_temp_cur,
		thumb = R(object_cond_icon),
		art = R(object_cond_art),
		summary = object_temp_summary
	))

	return oc

###################################################################################################
@route('/video/openweathermap/hourly')
def hourly(title, day):

	oc = ObjectContainer(title2=title)
	query_string = '%s' % (day)
	result = JSON.ObjectFromURL(ConstructURL() % (query_string))

	# Units
	if (Prefs['use_celsius']):
	  TEMP_UNIT	= u'\N{DEGREE SIGN}C' 
	  SPEED_UNIT	= ' km/h'
	else:
	  TEMP_UNIT	= u'\N{DEGREE SIGN}F' 
	  SPEED_UNIT	= ' mph'

	if (Prefs['use_24hour']):
	  TIME_UNIT	= '%y-%m-%d %H:%M'
	else:
  	  TIME_UNIT	= '%y-%m-%d %I:%M %p'
		
	# Location
	oc.add(DirectoryObject(
		title = result['city']['name'] + ', ' + result['city']['country'],
		thumb = R(ICON),
		art = R(ART)
	))

	# List
	for object in result['list']:
		object_unixtime	= object['dt']
		object_datetime	= datetime.datetime.fromtimestamp(object_unixtime)
		object_time	= str(object_datetime.strftime(TIME_UNIT))

		object_temp_rnd = round(object['main']['temp'],1)
		object_temp_cur = str(object_temp_rnd) + TEMP_UNIT
		object_temp_rnd = round(object['main']['temp_min'],1)
		object_temp_min = str(object_temp_rnd) + TEMP_UNIT
		object_temp_rnd = round(object['main']['temp_max'],1)
		object_temp_max = str(object_temp_rnd) + TEMP_UNIT
		object_pressure = str(object['main']['pressure']) + ' hPa'
		object_humidity = str(object['main']['humidity']) + '%'
		object_clouds	= str(object['clouds']['all']) + '%'
		object_windspeed= str(object['wind']['speed']) + SPEED_UNIT

		for weather in object['weather']:
			object_cond_short = weather['main']
			object_cond_long  = weather['description']
			object_cond_icon  = weather['icon'] + '_icon.png'
			object_cond_art   = weather['icon'] + '_art.jpg'


		# Summary
		object_hourly_summary = object_cond_long + ' (' + object_clouds + ')' + '\nMin: ' + object_temp_min + ', Max: ' + object_temp_max + '\nWind: ' + object_windspeed + '\nPressure: ' + object_pressure + ', Humidity: ' + object_humidity

		# Object
		oc.add(DirectoryObject(
			title = object_time + ': ' + object_temp_cur + ', ' + object_cond_short,
			thumb = R(object_cond_icon),
			art = R(object_cond_art),
			summary = object_hourly_summary
		))


	return oc

###################################################################################################
@route('/video/openweathermap/daily')
def daily(title, day):

	oc = ObjectContainer(title2=title)
	query_string = '%s' % (day)
	result = JSON.ObjectFromURL(ConstructURL() % (query_string))

	# Location
	oc.add(DirectoryObject(
		title = result['city']['name'] + ', ' + result['city']['country'],
		thumb = R(ICON),
		art = R(ART)
	))

	# Units
	if (Prefs['use_celsius']):
	  TEMP_UNIT	= u'\N{DEGREE SIGN}C' 
	  SPEED_UNIT	= ' km/h'
	else:
	  TEMP_UNIT	= u'\N{DEGREE SIGN}F' 
	  SPEED_UNIT	= ' mph'

	for object in result['list']:
		object_unixtime	= object['dt']
		object_datetime	= datetime.datetime.fromtimestamp(object_unixtime)
		object_time	= str(object_datetime.strftime('%y-%m-%d'))

		object_pressure = str(object['pressure']) + ' hPa'
		object_humidity = str(object['humidity']) + '%'
		object_windspeed= str(object['speed']) + SPEED_UNIT
		object_clouds	= str(object['clouds']) + '%'

		object_temp_rnd = round(object['temp']['day'],1)
		object_temp_cur = str(object_temp_rnd) + TEMP_UNIT

		object_temp_rnd = round(object['temp']['min'],1)
		object_temp_min = str(object_temp_rnd) + TEMP_UNIT
		object_temp_rnd = round(object['temp']['max'],1)
		object_temp_max = str(object_temp_rnd) + TEMP_UNIT
		object_temp_rnd = round(object['temp']['night'],1)
		object_temp_ngt = str(object_temp_rnd) + TEMP_UNIT

		for weather in object['weather']:
			object_cond_short	= weather['main']
			object_cond_long	= weather['description']
			object_cond_icon	= weather['icon'] + '_icon.png'
			object_cond_art		= weather['icon'] + '_art.jpg'

		# Summary
		object_daily_summary = object_cond_long + ' (' + object_clouds + ')' + '\nMin: ' + object_temp_min + ', Max: ' + object_temp_max + ', Night: ' + object_temp_ngt + '\nWind: ' + object_windspeed + '\nPressure: ' + object_pressure + ', Humidity: ' + object_humidity

		# Object
		oc.add(DirectoryObject(
			title = object_time + ': ' + object_temp_cur + ', ' + object_cond_short,
			thumb = R(object_cond_icon),
			art = R(object_cond_art),
			summary = object_daily_summary
		))


	return oc

###################################################################################################
def ValidatePrefs():
  ConstructURL()

