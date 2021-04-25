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
from WriteWorkers.Operation import Operation
from WriteWorkers.JobTracker import JobTracker
import properties
import json
import os


class Processor(object):
    def insert_data_tx(self,tx,name):
        result = tx.run(name)
        record = result.single()
        return record

    def _process_msg(self,q, c):
        msg = q.get(timeout=60)  # Set timeout to care for POSIX<3.0 and Windows.
        logging.info(
            '#%sT%s - Received message: %s',
            os.getpid(), threading.get_ident(), msg.value().decode('utf-8')
        )
        json_obj = json.loads(msg.value().decode('utf-8'))
        try:
            query,responsePart = self.operation.perform(msg)
        except Exception as e:
            logging.error("Exception %s", e)
            c.commit(msg)
        database = json_obj['database']
        try:
            session = self.sessionLocal.session
            if self.currentDBLocal.currentDB != database:
                logging.info("Changing session database context in Worker: {} Thread:{}".format(os.getpid(),threading.current_thread().name))
                self.sessionLocal.close()
                self.sessionLocal.session = self.driver.session(database=database)
        except AttributeError:
            logging.info("Creating Neo4j session in Worker: {} Thread:{}".format(os.getpid(),threading.current_thread().name))
            self.currentDBLocal.currentDB = database
            self.sessionLocal.session = self.driver.session(database = database)
        try:
            with self.sessionLocal.session as session:
                list(session.run(query, batch=json_obj))
                #self.sessionLocal.session.write_transaction(self.insert_data_tx, query) 
                logging.info("Successfully wrote {} to Neo4J".format(json_obj))
                self.operation.markJobEnd(jobid=json_obj['jobID'],jobType=responsePart,sucess=True)
        except Exception as e:
            logging.error("Error in Writing the data {} to Neo4j".format(json_obj))
            self.jobTracker.markPushingJob(json_obj['jobID'],"Error in Writing the data {} to Neo4j".format(json_obj))
        q.task_done()
        c.commit(msg)

    def _consume(self,config):
        c = Consumer(**config['kafka_kwargs'])
        c.subscribe([config['topic']])
        q = Queue(maxsize=config['num_threads'])

        while True:
            logging.info('#%s - Waiting for message...', os.getpid())
            try:
                msg = c.poll(config['polling_time'])
                if msg is None:
                    continue
                if msg.error():
                    logging.error(
                        '#%s - Consumer error: %s', os.getpid(), msg.error()
                    )
                    self.jobTracker.markPushingJob("Consumer Error %s", os.getpid())
                    continue
                q.put(msg)
                # Use default daemon=False to stop threads gracefully in order to
                # release resources properly.
                logging.info("Submmitting to the Thread")
                self.executor.submit(self._process_msg,q=q,c=c)
            except Exception:
                logging.exception('#%s - Worker terminated.', os.getpid())
                c.close()

    def __init__(self,num_threads):
        logging.info('Starting worker #%s', os.getpid())
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.jobTracker = JobTracker()
        self.driver = GraphDatabase.driver(properties.NEO4J_SERVER_URL,auth=(properties.NEO4J_SERVER_USERNAME, properties.NEO4J_SERVER_PASSWORD))
        self.sessionLocal = threading.local()
        self.currentDBLocal = threading.local()
        self.operation = Operation()
        
    def startConumsing(self,config):
        self._consume(config)


def createWorker(config):
    processor = Processor(config['num_threads'])
    processor.startConumsing(config)

def main(config):
    pool = Pool(processes=config['num_workers'])
    pool.map(createWorker,[config for i in range(config['num_workers'])])
    logging.info("{} Workers Initialized".format(config['num_workers']))

if __name__ == '__main__':
    logging.basicConfig(
        level=getattr(logging, os.getenv('LOGLEVEL', '').upper(), 'INFO'),
        format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    )
    main(config={
        'num_workers': int(os.environ['NUM_WORKERS']),
        'num_threads': int(os.environ['NUM_WORKER_THREADS']),
        'topic': os.environ['KAFKA_TOPIC'],
        'polling_time':int(os.environ['POLL_TIME']),
        'kafka_kwargs': {
            'bootstrap.servers': ','.join([
                os.environ['KAFKA_BOOTSTRAP_SERVERS'],
            ]),
            'group.id': os.environ['KAFKA_CONSUMER_GROUP'],
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        },
    })