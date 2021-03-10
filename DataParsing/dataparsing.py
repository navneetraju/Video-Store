import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Parser import parse
from Neo4jConnection import Neo4jConnection
import Constants
import properties

myParser = parse.Parser()

class DataParser:
    def __init__(self):
        self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD)

    def query(self,queryRequest):
        requestDictionary = queryRequest[Constants.PARSED_DICT]
        neo4j_query = self.generateNeo4jQuery(requestDictionary)
        #print(neo4j_query)
        try:
            databaseName = requestDictionary['database'][0]
            res = self.conn.query(neo4j_query,db=databaseName)
        except:
            print("WRONG DB!")

    def generateNeo4jQuery(self,requestDictionary):
        neo4j_query = ""
        neo4j_query += Constants.MATCH + Constants.SPACE
        for key in requestDictionary:
            if key != Constants.DATABASE.lower():
                neo4j_query += Constants.NEO4J_NODE_TYPE_MAPPING[key] + Constants.COMMA
                neo4j_query += Constants.SPACE
        neo4j_query += Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO] + Constants.SPACE
        neo4j_query += Constants.WHERE + Constants.SPACE
        for key in requestDictionary:
            if key.lower() != Constants.DATABASE.lower():
                conditionalStatement = self.__generateConditions(Constants.NEO4J_NODE_SIMPLE_MAPPING[key.lower()],requestDictionary[key][0])
                if len(conditionalStatement) != 0:
                    neo4j_query += conditionalStatement + Constants.SPACE + Constants.AND + Constants.SPACE
        neo4j_query = neo4j_query.rsplit(' ',1)[0].rsplit(' ',1)[0]
        neo4j_query += Constants.SPACE + Constants.NEO4J_SELECT_RETURN
        return neo4j_query
    
    def __generateConditions(self,type,value):
        conditionalString = ""
        if value == None:
            return None
        if type == Constants.EXPERENTIAL:
            conditionalString += Constants.NEO4J_CONDITIONAL_MAPPING[Constants.EXPERENTIAL] + "\"{}\"".format(value)
        elif type == Constants.INFORMATIONAL:
            conditionalString += Constants.NEO4J_CONDITIONAL_MAPPING[Constants.INFORMATIONAL] + "\"{}\"".format(value)
        elif type == Constants.SPATIAL:
            conditionalString += Constants.NEO4J_CONDITIONAL_MAPPING[Constants.SPATIAL] + "\"{}\"".format(value)
        return conditionalString