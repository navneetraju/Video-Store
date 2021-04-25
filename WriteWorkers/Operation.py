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
from WriteWorkers.JobTracker import JobTracker
import properties
import json

class Operation:
    def __init__(self):
        self.config_obj = ConfigService()
        self.jobtracker = JobTracker()
    
    def markJobEnd(self,jobid,jobType,sucess):
        if jobType == 'LAST_CSV':
            if sucess:
                self.jobtracker.markPushingJob(jobid,"CSV JOB Completed")
            else:
                self.jobtracker.markPushingJob(jobid,"Issue in completing CSV job")
        elif jobType == 'API':
            if sucess:
                self.jobtracker.markPushingJob(jobid,"API JOB Completed")
            else:
                self.jobtracker.markPushingJob(jobid,"Issue in completing API request")

    def perform(self, msg):
        json_obj = json.loads(msg.value().decode('utf-8'))
        database = json_obj["database"]
        dataset = json_obj["dataset"]
        combine_obj = Combine()
        jobID = json_obj['jobID']
        first = False
        last = False
        try:
            logging.info("Fetching the Database config")
            response = self.config_obj.getDatabaseConfig(database)
            logging.info("Finished fetching the Database config")
        except Exception as e:
            logging.error("Error in Getting Database Config ", e)
            self.jobtracker.markPushingJob(jobID,"Error in getting database config for database:{}".format(database))
            raise Exception("Error in getting database config for database:{}".format(database))
        if(response["status"] == 400):
            self.jobtracker.markPushingJob(jobID, "Database configuration could not be found in the ConfigService for database:{}".format(database))
            logging.error("Database configuration could not be found in the ConfigService for database:{}".format(database))
            raise Exception("Database configuration could not be found in the ConfigService for database:{}".format(database))
        elif(response["status"] == 500):
            logging.error("ConfigService Error in Getting Database Config ", e)
            self.jobtracker.markPushingJob(jobID,"Error in getting database config for database:{}".format(database))
            raise Exception("ConfigService Error in getting database config for database:{}".format(database))
        elif(response["status"] == 200):
            json_response = response    
            if('first' in json_obj and json_obj['first']):
                first = True
                self.jobtracker.markPushingJob(jobID, "Started Consuming the first chunk of data from topic")
                logging.info("Started Consuming the First chunk of data from Topic")
            elif('last' in json_obj and json_obj['last']):
                last = True
                logging.info("Staring consumption of the last chunk of data from topic")
            elif(json_obj['ingestionType']!='CSV'):
                self.jobtracker.markPushingJob(jobID, "JSON Received at worker")
                logging.info("JSON Received at worker")
            responsePart = None
            if last:
                responsePart = 'LAST_CSV'
            elif json_obj['ingestionType'] == 'API':
                responsePart = 'API'
            else:
                responsePart = 'PART'
            for val in json_response['config']["datasets"]:
                if(dataset == val['name']):                    
                    if(val['mappings']['type'] == 'MultiColumn'):
                        try:
                            logging.info("Generating the multiColumn query")
                            return (combine_obj.combine_multi(json_obj, val),responsePart)
                        except Exception as e:
                            logging.error("Error in generating the query for multicolumn")
                            self.jobtracker.markPushingJob(jobID,"Error in generating the query for multicolumn")
                            raise Exception("Error in generating the query for multicolumn")
                    else:
                        try:
                            logging.info("Fetching the Category Mapping")
                            resp = self.config_obj.getCategoryMapping(val['mappings']['categoryMappingName'])
                            logging.info("Finished fetching the category mapping")
                        except:
                            logging.error("Error in getting the Category mapping")
                            self.jobtracker.markPushingJob(jobID,"Error in getting the Category mapping")
                            raise Exception("Error in getting the Category mapping")
                        
                        if(resp["status"] == 400):
                            self.jobtracker.markPushingJob(jobID, "ConfigService could not find the mapping")
                            logging.error("ConfigService could not find the mapping")
                        elif(resp["status"] == 500):
                            self.jobtracker.markPushingJob(jobID, "ConfigService error while fetching the mapping config")
                            logging.error("ConfigService error while fetching the mapping config")
                        elif(resp["status"] == 200):
                            try:
                                logging.info("Generating Query for Single Column")
                                return (combine_obj.combine_single(json_obj, resp['mapping'], val),responsePart)
                                logging.info("Completed generating query for single column")
                            except Exception as e:
                                logging.error("Error in generating the query for Single Column")
                                self.jobtracker.markPushingJob(jobID,"Error in generating the query for Single Column")
                    break
