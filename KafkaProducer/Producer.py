from confluent_kafka import Producer
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import properties
import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)
import json

SUCCESS = "SUCCESS"
ERROR = "ERROR"
UDF = "UDF"

class KafkaProducer():
    def __init__(self,broker,topic):
        self.broker = broker 
        self.topic = topic
        conf = {'bootstrap.servers': broker}
        self.producer = Producer(**conf)
        self.flushReport = None
        self.jobStatus = None
    
    def writeToTopic(self,dataObject,jobID):
        message = json.dumps(dataObject)
        logging.info("Pushing {} to Kafka topic".format(message))
        self.producer.produce(self.topic, message, callback=self.delivery_callback)
        msg = self.producer.poll(0)
        self.producer.flush()
        resp = (self.jobStatus,self.flushReport)
        self.jobStatus = UDF
        self.flushReport = None 
        return resp

    def writeCSVToTopic(self,dataObject,jobID):
        logging.info("Staring CSV Push to Kafka topic for jobID:{}".format(jobID))
        count = 0
        for i in dataObject:
            if self.jobStatus == ERROR:
                resp = (self.jobStatus,self.flushReport)
                self.jobStatus = UDF
                self.flushReport = None
                return resp
            count += 1
            message = json.dumps(i)
            self.producer.produce(self.topic, message,callback=self.csv_callback)
            if count%1000 == 0:             
                try:
                    self.producer.flush(10)
                except Exception:
                    resp = (self.jobStatus,self.flushReport)
                    self.jobStatus = UDF
                    self.flushReport = None
                    return resp
        self.producer.poll(0)
        self.producer.flush(10)
        resp = (self.jobStatus,self.flushReport)
        self.jobStatus = UDF
        self.flushReport = None 
        return resp

    def csv_callback(self,err,msg):
        if err:
            self.jobStatus = SUCCESS
            self.flushReport= err
            logging.error('%% Message failed delivery: %s\n' % err)
        else:
            self.jobStatus  = SUCCESS
            self.flushReport = msg
        
    def delivery_callback(self,err, msg):
        if err:
            self.jobStatus = ERROR
            self.flushReport = err
            logging.error('%% Message failed delivery: %s\n' % err)
        else:
            self.jobStatus = SUCCESS
            self.flushReport = msg
            logging.info('%% Message delivered to %s [%d] @ %d\n' %
                             (msg.topic(), msg.partition(), msg.offset()))