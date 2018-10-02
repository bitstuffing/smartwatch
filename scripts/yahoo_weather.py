from library.httputils import HttpUtils
import ujson as json
import gc

class YahooWeather():

	API_URL = 'https://query.yahooapis.com/v1/public/yql?format=json&q='
	QUERY = 'select%%20*%%20from%%20weather.forecast%%20where%%20woeid%%20in%%20(select%%20woeid%%20from%%20geo.places(1)%%20where%%20text%%3D%%22%s%%22)'

	@staticmethod
	def query(place):
		address = YahooWeather.API_URL
		place = place.replace(" ","%20") #urllib.quote_plus(place) give you in troubles
		address += YahooWeather.QUERY % (place,)
		bruteJson = HttpUtils.get_url(address)
		gc.collect()
		jsonLoaded = json.loads(bruteJson)
		gc.collect()
		return jsonLoaded["query"] #.has_key("query") is true

	@staticmethod
	def getWeek(place,format=True):
		results = YahooWeather.query(place)
		value = results["results"]
		week = []
		if(len(value)>0):
			for key2,value2 in value["channel"].items():
				if key2 == 'item':
					if format:
						for forecast in value2["forecast"]:
							week.append(YahooWeather.formatForecast(forecast))
					else: #pain, in Fahrenheit format
						return value2["forecast"]
			return week
		else:
			return ["No results for "+city]

	@staticmethod
	def formatForecast(forecast):
		if "day" in forecast and "date" in forecast and "high" in forecast and "low" in forecast and "text" in forecast:
			return forecast["day"]+", "+forecast["date"]+" |HIGH| "+"{0:.2f}".format(YahooWeather.convertFahrenheitTo(float(forecast["high"])))+" |LOW| "+"{0:.2f}".format(YahooWeather.convertFahrenheitTo(float(forecast["low"])))+" Description ->"+forecast["text"]
		else:
			return "No Parseable Data"

	@staticmethod
	def convertCelsiusTo(celsius):
		return 9.0/5.0 * celsius + 32

	@staticmethod
	def convertFahrenheitTo(fahrenheit):
		return (fahrenheit - 32) * 5.0/9.0
