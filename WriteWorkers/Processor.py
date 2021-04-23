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
# from WriteWorkers.Combine import Combine
from WriteWorkers.Connect_DB import Connect_DB
from WriteWorkers.Operation import Operation
from Import.JobTracker import JobTracker
import properties


class Processor(object):
    def create_node_tx(self,tx,name):
        print('Current Thread: {}'.format(
            threading.current_thread().name)
        )
        print('Process: ',os.getpid())
        print(name)
        result = tx.run(name)
        print(result.single())
        record = result.single()
        current_time = str(datetime.now())
        return (record,current_time)

    def _process_msg(self,q, c):
        msg = q.get(timeout=60)  # Set timeout to care for POSIX<3.0 and Windows.
        print('Current Thread: {}'.format(
            threading.current_thread().name)
        )
        print("Current process: ",os.getpid())
        logging.info(
            '#%sT%s - Received message: %s',
            os.getpid(), threading.get_ident(), msg.value().decode('utf-8')
        )
        
        with self.driver.session(database="youtube") as session:
            # print("Going to Combine")
            op_obj = Operation()
            query = op_obj.perform(msg)
            # print("Finished Operation")
            print(session.write_transaction(self.create_node_tx, query) )
            print("WROTE TO NEO4j")
        q.task_done()
        c.commit(msg)

    def _consume(self,config):
        c = Consumer(**config['kafka_kwargs'])
        c.subscribe([config['topic']])
        q = Queue(maxsize=config['num_threads'])

        while True:
            logging.info('#%s - Waiting for message...', os.getpid())
            try:
                msg = c.poll(60)
                if msg is None:
                    # print("Going to Continue")
                    continue
                if msg.error():
                    print("Consumer Error")
                    logging.error(
                        '#%s - Consumer error: %s', os.getpid(), msg.error()
                    )
                    continue
                q.put(msg)
                # Use default daemon=False to stop threads gracefully in order to
                # release resources properly.
                print('submitting to thread')
                self.executor.submit(self._process_msg,q=q,c=c)
            except Exception:
                logging.exception('#%s - Worker terminated.', os.getpid())
                c.close()

    def __init__(self):
        """Initialize the class with 'global' variables"""
        print('Starting worker #%s', os.getpid())
        logging.info('Starting worker #%s', os.getpid())
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        # uri = "neo4j://10.10.1.146:7687"
        self.driver = GraphDatabase.driver(properties.NEO4J_SERVER_URL,auth=(properties.NEO4J_SERVER_USERNAME, properties.NEO4J_SERVER_PASSWORD))
        
        Connect_DB("youtube")
        
    def startConumsing(self,config):
        self._consume(config)

    def __call__(self, data):
        """Do something with the cursor and data"""
        print('here')
        self.cursor.find(data.key)

def createWorker(config):
    processor = Processor()
    processor.startConumsing(config)

def main(config):
    """
    Simple program that consumes messages from Kafka topic and prints to
    STDOUT.
    """
    # print("Inside Main")
    results = []
    pool = Pool(processes=5)
    # pool.map(createWorker,[config,config,config,config,config])
    pool.map(createWorker,[config for i in range(5)])
    
    logging.info("Created the Pool of Processes")
    '''
    for i in range(5):
        Process(target=createWorker,args=(config,),daemon=True).start()
        print("Done")
    while True:
        continue
    '''

if __name__ == '__main__':
    logging.basicConfig(
        level=getattr(logging, os.getenv('LOGLEVEL', '').upper(), 'INFO'),
        format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    )
    # print("About to Call Main")
    # processor_obj = Processor()
    main(config={
        # At most, this should be the total number of Kafka partitions on
        # the topic.
        'num_workers': 3,
        'num_threads': 4,
        'topic': 'test_topic_perf',
        'kafka_kwargs': {
            'bootstrap.servers': ','.join([
                '10.10.1.146:9092',
            ]),
            'group.id': 'my_consumer_group',
            'auto.offset.reset': 'earliest',
            # Commit manually to care for abrupt shutdown.
            'enable.auto.commit': False,
        },
    })