import os, sys
import functools
import requests
import logging
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import properties

from cache import timed_lru_cache

class ConfigService:

	@timed_lru_cache(600)
	def getDatabaseConfig(self,database):
		print("Config Service Database Config")
		config = requests.get(properties.CONFIG_SERVICE_DB_URL.format(database))
		res = dict()
		if config.status_code == 500:
			logging.error("ConfigService error while fetching database config")
			res['status'] = 500
			res['config'] = None 
			return res
		elif config.status_code == 400:
			logging.error("ConfigService could not find the config for the database:{}".format(database))
			res['status'] = 400
			res['config'] = None 
			return res
		res['status'] = 200
		res['config'] = config.json()
		return res

	@timed_lru_cache(600)
	def getCategoryMapping(self,mappingName):
		mapppingResponse = requests.get(properties.CONFIG_SERVICE_MAPPING_URL.format(mappingName))
		res = dict()
		if mapppingResponse.status_code == 500:
			logging.error("ConfigService error while fetching the mapping config")
			res['status'] = 500
			res['mapping'] = None 
			return res
		elif mapppingResponse.status_code == 400:
			logging.error("ConfigService could not find the mapping :{}".format(mappingName))
			res['status'] = 400
			res['mapping'] = None 
			return res
		res['status'] = 200
		res['mapping'] = mapppingResponse.json()
		return res