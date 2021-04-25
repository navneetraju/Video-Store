import csv 
from io import StringIO
import os, sys
import pandas as pd
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from KafkaProducer.Producer import KafkaProducer
from Import.JobTracker import JobTracker
import properties
import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)
class ImportHandler:
    def __init__(self):
        self.kafkaProducer = KafkaProducer('10.10.1.146:9092','test_topic_perf')
        self.jobTracker = JobTracker()
    def writeCSV(self,csvFile,database,dataset,jobID):
        logging.info("Recieved CSV job {}, starting parsing".format(jobID))
        self.jobTracker.markPushingJob(jobID,"PARSING JOB STARTED")
        df = pd.read_csv(StringIO(csvFile.file.read().decode()))
        header_list = list(df.columns.values)
        li = []
        numRows = df.shape[0]
        first = True
        for index, row in df.iterrows():
            insertionData = dict()
            insertionData['ingestionType'] = 'CSV'
            if first:
                insertionData['first'] = True 
                insertionData['last'] = False
                first = False
            elif index == numRows - 1:
                insertionData['last'] = True 
                insertionData['first'] = False
            else:
                insertionData['last'] = False
                insertionData['first'] = False 
            insertionData['database'] = database
            insertionData['dataset'] = dataset
            insertionData['jobID'] = jobID
            for i in range(0,len(row)):
                insertionData[header_list[i]] = row[header_list[i]]
            li.append(insertionData)
        logging.info("CSV job {} parsing complete".format(jobID))
        self.jobTracker.markPushingJob(jobID,"PARSING JOB COMPLETED,STARTED KAFKA TOPIC PUSH")
        jobStatus,message = self.kafkaProducer.writeCSVToTopic(li,jobID)
        if jobStatus == "SUCCESS":
            logging.info("Data pushed for CSV, jobId: {}".format(jobID))
            self.jobTracker.markPushingJob(jobID,"DATA PUSHED INTO KAFKA")
        elif jobStatus == "ERROR":
            logging.error("Error pushing CSV data for jobId: {}".format(jobID))
            self.jobTracker.markPushingJob(jobID,"ERROR IN PUSHING DATA: {}".format(message))
    
    def writeJSON(self,jsonRequest,jobID):
        logging.info("Recieved JSON job {}".format(jobID))
        self.jobTracker.markPushingJob(jobID,"JSON Request RECEIVED")
        jsonRequest['jobID'] = jobID
        jsonRequest['ingestionType'] = 'API'
        jobStatus,message = self.kafkaProducer.writeToTopic(jsonRequest,jobID)
        if jobStatus == "SUCCESS":
            logging.info("Data pushed for JSON, jobId: {}".format(jobID))
            self.jobTracker.markPushingJob(jobID,"DATA PUSHED INTO KAFKA")
            return {"status":202,"message":"Successfully pushed data into topic"}
        elif jobStatus == "ERROR":
            logging.error("Error pushing JSON data for jobId: {}".format(jobID))
            self.jobTracker.markPushingJob(jobID,"ERROR IN PUSHING DATA: {}".format(message))
            return {"status":400,"message":str(message)}
        else:
            return {"status":500,"message":str(message)}