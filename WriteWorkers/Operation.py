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
        json_obj = json.loads(msg.value().decode('utf-8'))
        database = json_obj["database"]
        dataset = json_obj["dataset"]
        combine_obj = Combine()
        jobID = json_obj['jobID']
        try:
            logging.info("Fetching the Database config")
            response = self.config_obj.getDatabaseConfig(database)
            logging.info("Finished fetching the Database config")
        except Exception as e:
            logging.error("Error in Getting Database Config ", e)
            self.jobtracker.markPushingJob("Error in getting the Database Config")
        if(response["status"] == 400):
            self.jobtracker.markPushingJob(jobID, "Configuration could not be found in the ConfigService")
            logging.error("Configuration could not be found in the ConfigService")
        elif(response["status"] == 500):
            self.jobtracker.markPushingJob(jobID, "ConfigService error while fetching database config")
            logging.error("ConfigService error while fetching database config")
        elif(response["status"] == 200):
            json_response = response    
            if('first' in json_obj and json_obj['first']):
                self.jobtracker.markPushingJob(jobID, "Started Consuming the First chunk of data from Topic")
                logging.error("Started Consuming the First chunk of data from Topic")
            else:
                self.jobtracker.markPushingJob(jobID, "Started Consuming from the Topic...")
                logging.info("Started Comsuming the data from Topic ")
            for val in json_response['config']["datasets"]:
                if(dataset == val['name']):                    
                    if(val['mappings']['type'] == 'MultiColumn'):
                        try:
                            logging.info("Generating the multiColumn query")
                            return combine_obj.combine_multi(json_obj, val)
                            logging.info("Finished generating the multicolumn query")
                        except Exception as e:
                            logging.error("Error in generating the query for multicolumn")
                            self.jobtracker.markPushingJob("Error in generating the query for multicolumn")
                    else:
                        try:
                            logging.info("Fetching the Category Mapping")
                            resp = self.config_obj.getCategoryMapping(val['mappings']['categoryMappingName'])
                            logging.info("Finished fetching the category mapping")
                        except:
                            logging.error("Error in getting the Category mapping")
                            self.jobtracker.markPushingJob("Error in getting the Category mapping")
                        
                        if(resp["status"] == 400):
                            self.jobtracker.markPushingJob(jobID, "ConfigService could not find the mapping")
                            logging.error("ConfigService could not find the mapping")
                        elif(resp["status"] == 500):
                            self.jobtracker.markPushingJob(jobID, "ConfigService error while fetching the mapping config")
                            logging.error("ConfigService error while fetching the mapping config")
                        elif(resp["status"] == 200):
                            try:
                                logging.info("Generating Query for Single Column")
                                return combine_obj.combine_single(json_obj, resp['mapping'], val)
                                logging.info("Completed generating query for single column")
                            except Exception as e:
                                logging.error("Error in generating the query for Single Column")
                                self.jobtracker.markPushingJob("Error in generating the query for Single Column")
                    break
           
            if('last' in json_obj and json_obj['last']):
                self.jobtracker.markPushingJob(jobID, "Finished Consuming the Last chunk of data from Topic")
                logging.error("Finished Consuming the Last chunk of data from Topic")
        logging.info("Updated the Job Tracker {}".format(jobID))