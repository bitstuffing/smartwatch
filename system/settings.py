import ujson
import os

class Settings():

	path = "/system/settings.json"
	syspath = "/system/"

	@staticmethod
	def load():
		jsonObject = {}
		jsonContent = "{}"
		if os.path.exists(Settings.path):
			f = open(Settings.path)
			jsonContent = f.read()
			f.close()
		else:
			if os.path.exists(Settings.path):
				os.mkdir(Settings.syspath)
			open(Settings.path, 'w').close()
		try:
			jsonObject = ujson.loads(jsonContent)
		except:
			#TODO, log
			pass
		return jsonObject
		
	@staticmethod
	def store(settings):
		try:
			jsonString = ujson.dumps(settings)
			f = open(Settings.path,'w')
			f.write(jsonString)
			f.close()
		except:
			#TODO log
			pass
		

	@staticmethod
	def get(key):
		value = ""
		try:
			settings = Settings.load()
			if settings.has_key(key):
				value = str(settings[key])
		except:
			#TODO, log
			pass
		
		return value
		
	@staticmethod
	def set(key,value):
		try:
			settings = Settings.load()
			settings[key] = value
			Settings.store(settings)
		except:
			#TODO, log
			pass
		
	
