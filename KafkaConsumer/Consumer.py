from confluent_kafka import Consumer
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import properties
import Constants
import logging
from Import.JobTracker import JobTracker
from WriteWorkers import create_node_relations
from WriteWorkers.WriteQuery import WriteQuery
from WriteWorkers.constraint_combine import Combine
from WriteWorkers.Neo4jConnection import Neo4jConnection
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)
import json
import threading
from multiprocessing import Process
from queue import Queue
import time
import requests

SUCCESS = "SUCCESS"
ERROR = "ERROR"
UDF = "UDF"

class KafkaConsumer():
    def __init__(self,broker,topic, jobID):
        self.broker = broker 
        self.topic = topic
        self.jobID = jobID
        self.jobTracker = JobTracker() 
        # self.conf = {'bootstrap.servers': broker, 'num_workers': 4, 'num_threads': 4, 'group_id': 'kafka_consumer_group', 'auto.offset.reset': 'earliest', 'enable.auto.commit' : False}
        self.config={
            # At most, this should be the total number of Kafka partitions on
            # the topic.
            'num_workers': 1,
            'num_threads': 1,
            'topic': 'test',
            'kafka_kwargs': {
                'bootstrap.servers': broker,
                # 'bootstrap.servers': ','.join([
                #     'cluster1.mykafka.com',
                #     'cluster2.mykafka.com',
                #     'cluster3.mykafka.com',
                # ]),
                'group.id': 'my_consumer_group',
                'auto.offset.reset': 'earliest',
                # Commit manually to care for abrupt shutdown.
                'enable.auto.commit': False,
            },
        }
        # self.consumer = Consumer(**self.config)
        self.main(self.config)
        self.flushReport = None
        self.jobStatus = None

    def _process_msg(self, q, c):
        msg = q.get(timeout=60)  # Set timeout to care for POSIX<3.0 and Windows.
        # logging.info('# {} T {} - Received message: {}'.format(os.getpid(), threading.get_ident(), msg.value().decode('utf-8')))
        
        json_obj = json.loads(msg.value().decode('utf-8'))
        database = json_obj["database"]
        dataset = json_obj["dataset"]
        self.combine_obj = Combine(database)
        response = requests.get(properties.CONFIG_SERVICE_DB_URL.format(database))
        status = response.status_code
        if(status == 400):
            self.jobTracker.markPushingJob(self.jobID, "Configuration could not be found in the ConfigService")
            logging.error("Configuration could not be found in the ConfigService")
        elif(status == 500):
            self.jobTracker.markPushingJob(self.jobID, "ConfigService error while fetching database config")
            logging.error("ConfigService error while fetching database config")
        elif(status == 200):
            json_response = json.loads(response.text)
            # print("From Topic ", json_obj)
            # print("Database COnfig ", json_response)
            if('first' in json_obj and json_obj['first']):
                self.jobTracker.markPushingJob(self.jobID, "Started Consuming the First chunk of data from Topic")
                logging.error("Started Consuming the First chunk of data from Topic")
            for val in json_response["datasets"]:
                if(dataset == val['name']):
                    # print("dataset matched")
                    final_query = ""
                    if(val['mappings']['type'] == 'MultiColumn'):
                        
                        self.combine_obj.combine_multi(json_obj, val)
                        
                    else:
                        # print("Single Column")
                        
                        resp = requests.get(properties.CONFIG_SERVICE_MAPPING_URL.format(val['mappings']['categoryMappingName']))
                        status_code = resp.status_code
                        if(status_code == 400):
                            self.jobTracker.markPushingJob(self.jobID, "ConfigService could not find the mapping")
                            logging.error("ConfigService could not find the mapping")
                        elif(status_code == 500):
                            self.jobTracker.markPushingJob(self.jobID, "ConfigService error while fetching the mapping config")
                            logging.error("ConfigService error while fetching the mapping config")
                        elif(status_code == 200):
                            # singlecol_response = json.loads(resp)
                            # print(singlecol_response)
                            # print("Single Column Response", resp.text)
                            self.combine_obj.combine_single(json_obj, json.loads(resp.text), val)
                    break
           
            if('last' in json_obj and json_obj['last']):
                self.jobTracker.markPushingJob(self.jobID, "Finished Consuming the Last chunk of data from Topic")
                logging.error("Finished Consuming the Last chunk of data from Topic")
        logging.info("Updated the Job Tracker {}".format(self.jobID))
        # self.jobStatus = ""
        # resp = (self.jobStatus,self.flushReport)
        time.sleep(5)
        q.task_done()
        c.commit(msg)


    def _consume(self, config):
        logging.info(
            '# {}- Starting consumer group={}, topic={}'.format(os.getpid(), config['kafka_kwargs']['group.id'], config['topic']))
        self.jobTracker.markPushingJob(self.jobID, "Started the Consumer")
        
        c = Consumer(**self.config['kafka_kwargs'])
        c.subscribe([self.config['topic']])
        q = Queue(maxsize=self.config['num_threads'])

        while True:
            logging.info('#{} - Waiting for message...'.format(os.getpid()))
            try:
                msg = c.poll(60)
                if msg is None:
                    continue
                if msg.error():
                    logging.error('# {} - Consumer error: {}'.format(os.getpid(), msg.error()))

                    continue
                q.put(msg)
                # Use default daemon=False to stop threads gracefully in order to
                # release resources properly.
                t = threading.Thread(target=self._process_msg, args=(q, c))
                t.start()
                
            except Exception:
                logging.exception('# {} - Worker terminated.'.format(os.getpid()))
                self.jobStatus = ERROR
                self.flushReport = "Worker Terminated {}".format(os.getpid())
                resp = (self.jobStatus, self.flushReport)
                c.close()


    def main(self, config):
        """
        Simple program that consumes messages from Kafka topic and prints to
        STDOUT.
        """
        workers = []
        while True:
            num_alive = len([w for w in workers if w.is_alive()])
            if config['num_workers'] == num_alive:
                continue
            # self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD, dbName="youtube")
            for _ in range(config['num_workers']-num_alive):
                p = Process(target=self._consume, daemon=True, args=(config,))
                p.start()
                workers.append(p)
                logging.info('Starting worker #%s', p.pid)

if(__name__ == "__main__"):
    KafkaConsumer('10.10.1.146:9092','test', "1234")
   
    
    # def getDataFromTopic(self, jobID):
    #     # message = json.dumps(dataObject)
    #     logging.info("Retrieving the data from Kafka topic")
    #     self.consumer.subscribe(self.topic, callback=self.delivery_callback)
    #     msg = self.producer.poll(0)
    #     self.producer.flush()
    #     resp = (self.jobStatus,self.flushReport)
    #     self.jobStatus = UDF
    #     self.flushReport = None 
    #     return resp

    # def writeCSVToTopic(self,dataObject,jobID):
    #     logging.info("Staring CSV Push to Kafka topic for jobID:{}".format(jobID))
    #     count = 0
    #     for i in dataObject:
    #         if self.jobStatus == ERROR:
    #             resp = (self.jobStatus,self.flushReport)
    #             self.jobStatus = UDF
    #             self.flushReport = None
    #             return resp
    #         count += 1
    #         message = json.dumps(i)
    #         self.producer.produce(self.topic, message,callback=self.csv_callback)
    #         if count%1000 == 0:             
    #             try:
    #                 self.producer.flush(10)
    #             except Exception:
    #                 resp = (self.jobStatus,self.flushReport)
    #                 self.jobStatus = UDF
    #                 self.flushReport = None
    #                 return resp
    #     self.producer.poll(0)
    #     self.producer.flush(10)
    #     resp = (self.jobStatus,self.flushReport)
    #     self.jobStatus = UDF
    #     self.flushReport = None 
    #     return resp

    # def csv_callback(self,err,msg):
    #     if err:
    #         self.jobStatus = SUCCESS
    #         self.flushReport= err
    #         logging.error('%% Message failed delivery: %s\n' % err)
    #     else:
    #         self.jobStatus  = SUCCESS
    #         self.flushReport = msg
        
    # def delivery_callback(self,err, msg):
    #     if err:
    #         self.jobStatus = ERROR
    #         self.flushReport = err
    #         logging.error('%% Message failed delivery: %s\n' % err)
    #     else:
    #         self.jobStatus = SUCCESS
    #         self.flushReport = msg
    #         logging.info('%% Message delivered to %s [%d] @ %d\n' %
    #                          (msg.topic(), msg.partition(), msg.offset()))


    