import concurrent.futures
from multiprocessing import Process,Pool
from confluent_kafka import Consumer
import logging
from neo4j import GraphDatabase
from queue import Queue
import threading
import time
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from datetime import datetime
from WriteWorkers.Combine import Combine
from WriteWorkers.ConfigService import ConfigService
from Import.JobTracker import JobTracker
import properties
import json

class Operation:
    def __init__(self):
        # print("Operation")
        self.config_obj = ConfigService()
        self.jobtracker = JobTracker()
    def perform(self, msg):
        print("started the operation")
        json_obj = json.loads(msg.value().decode('utf-8'))
        database = json_obj["database"]
        dataset = json_obj["dataset"]
        combine_obj = Combine()
        # response = requests.get(properties.CONFIG_SERVICE_DB_URL.format(database))
        jobID = json_obj['jobID']
        response = self.config_obj.getDatabaseConfig(database)
        # print("Database Config ", response)
        if(response["status"] == 400):
            self.jobTracker.markPushingJob(jobID, "Configuration could not be found in the ConfigService")
            logging.error("Configuration could not be found in the ConfigService")
        elif(response["status"] == 500):
            self.jobTracker.markPushingJob(jobID, "ConfigService error while fetching database config")
            logging.error("ConfigService error while fetching database config")
        elif(response["status"] == 200):
            json_response = response 
            print("JsonObj", json_obj)   
            # print("From Topic ", json_obj)
            # print("Database COnfig ", json_response)
            if('first' in json_obj and json_obj['first']):
                self.jobTracker.markPushingJob(jobID, "Started Consuming the First chunk of data from Topic")
                logging.error("Started Consuming the First chunk of data from Topic")
            # else:
            #     self.jobtracker.markPushingJob(jobID, "Started Consuming from the Topic...")
            #     logging.info("Started Comsuming the data from Topic ")
            for val in json_response['config']["datasets"]:
                if(dataset == val['name']):
                    # print("dataset matched")
                    
                    if(val['mappings']['type'] == 'MultiColumn'): 
                        return combine_obj.combine_multi(json_obj, val)
                    else:
                        print("Single Column")
                        
                        # resp = requests.get(properties.CONFIG_SERVICE_MAPPING_URL.format(val['mappings']['categoryMappingName']))
                        resp = self.config_obj.getCategoryMapping(val['mappings']['categoryMappingName'])
                        
                        if(resp["status"] == 400):
                            self.jobTracker.markPushingJob(jobID, "ConfigService could not find the mapping")
                            logging.error("ConfigService could not find the mapping")
                        elif(resp["status"] == 500):
                            self.jobTracker.markPushingJob(jobID, "ConfigService error while fetching the mapping config")
                            logging.error("ConfigService error while fetching the mapping config")
                        elif(resp["status"] == 200):
                            print("CAlling Combine Single")
                            return combine_obj.combine_single(json_obj, resp['mapping'], val)
                    break
           
            if('last' in json_obj and json_obj['last']):
                self.jobTracker.markPushingJob(jobID, "Finished Consuming the Last chunk of data from Topic")
                logging.error("Finished Consuming the Last chunk of data from Topic")
        logging.info("Updated the Job Tracker {}".format(jobID))