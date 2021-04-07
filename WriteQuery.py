from neo4j import GraphDatabase
from Exceptions import *
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import properties
import logging
from Neo4jConnection import Neo4jConnection
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)

class WriteQuery:
    def __init__(self, uri, user, pwd):
        # self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD)
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            logging.info("Initializing Neo4J connection..")
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            logging.error("Failed to create the driver",exc_info=True)
        logging.info("Successfully initialized NEO4J Database connection")

    def write_query(self, query, db=None, json_obj=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, batch=json_obj))
        except Exception as e:
            if e.code == "Neo.ClientError.Database.DatabaseNotFound":
                logging.error("Caught exception ",exc_info=True)
                raise Neo4JWrongDB(str(e))
            else:
                logging.error("Caught exception ",exc_info=True)
                raise Neo4JFailedRequest(str(e))
            exit()
        finally: 
            if session is not None:
                session.close()
        return self.__tojson(response)

    def __tojson(self, result):
        jsonArray = list()
        for i in result:
            jsonArray.append(dict(i))
        return jsonArray 