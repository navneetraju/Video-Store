import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Neo4jConnection import Neo4jConnection
import Constants
import properties

import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)


class Connect_DB:
    def __init__(self, dbName):
        self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD)
        self.dbName = dbName
        self.connect_to_db(self.dbName)
        
    def connect_to_db(self, dbName):
        try:
            logging.info("Creating the Database "+dbName)
            self.conn.query("CREATE DATABASE youtube IF NOT EXISTS")
            logging.info("Database " + dbName + " Created...")
        except:
            logging.error("Database is not Created.. Something went Wrong")
            exit()
               