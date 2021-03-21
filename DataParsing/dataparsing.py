import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Parser import parse
from Neo4jConnection import Neo4jConnection
import Constants
import properties
from youtube import YoutubeDataAPI
import json
from Exceptions import *
import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)


class DataParser:
    def __init__(self):
        self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD)
        self.youtubeAPI = YoutubeDataAPI()

    def query(self,queryRequest:dict):
        logging.info("Received simple query ...")
        requestDictionary = queryRequest[Constants.PARSED_DICT]
        neo4j_query = self.__generateNeo4jQuery(requestDictionary)
        res = None
        try:
            databaseName = requestDictionary['database'][0]
            logging.info("Querying Neo4J..")
            res = self.conn.query(neo4j_query,db=databaseName)
        except Neo4JWrongDB as e:
            logging.error("Handling exception: ",exc_info=True)
            return json.dumps({"code":400,"message":"Queried database not found: "+ str(e)})
        except Neo4JFailedRequest as e:
            logging.error("Handling exception: ",exc_info=True)
            return json.dumps({"code":500,"message":"Failed to query Neo4J Database: "+ str(e)})
        return json.dumps({"code":200,"response":self.__postProcessResult(res)})
    
    def fuzzyQuery(self,queryRequest:dict):
        logging.info("Received fuzzy query ...")
        requestDictionary = queryRequest[Constants.PARSED_DICT]
        neo4j_fuzzy_query = self.__generateNeo4jFuzzyQuery(requestDictionary)
        res = None
        try:
            databaseName = requestDictionary['database'][0]
            logging.info("Querying(fuzzy) Neo4J..")
            res = self.conn.query(neo4j_fuzzy_query,db=databaseName)
        except Neo4JWrongDB as e:
            logging.error("Handling exception: ",exc_info=True)
            return json.dumps({"code":400,"message":"Queried database not found: "+ str(e)})
        except Neo4JFailedRequest as e:
            logging.error("Handling exception: ",exc_info=True)
            return json.dumps({"code":500,"message":"Failed to query Neo4J Database: "+ str(e)})
        return json.dumps({"code":200,"response":self.__postProcessFuzzyResult(res)})

    def __generateNeo4jQuery(self,requestDictionary):
        logging.info("Creating Neo4J query")
        neo4j_query = ""
        neo4j_query += Constants.MATCH + Constants.NEO4J_FILTERS[Constants.EXPERENTIAL](requestDictionary['event'][0]) + Constants.NEO4J_SELECT_RETURN + Constants.SPACE

        for key in requestDictionary:
            if key!="database":
                neo4j_query += Constants.UNION_MATCH + Constants.NEO4J_FILTERS[Constants.NEO4J_NODE_MAPPING[key]](requestDictionary[key][0]) + Constants.NEO4J_SELECT_RETURN + Constants.SPACE
        return neo4j_query

    def __generateNeo4jFuzzyQuery(self,requestDictionary):
        neo4j_query = ""
        index_count = 0
        for key in requestDictionary:
            if key!="database":
                neo4j_query += Constants.NEO4J_FUZZY_INDEX[Constants.NEO4J_NODE_MAPPING[key]](requestDictionary[key][0],index_count)  + Constants.SPACE
                index_count += 1
        neo4j_query += Constants.MATCH
        for key in requestDictionary:
            if key!="database":
                neo4j_query += Constants.NEO4J_RELATIONSHIPS[Constants.NEO4J_NODE_MAPPING[key]] + Constants.COMMA
        neo4j_query += Constants.NEO4J_RELATIONSHIPS[Constants.TEMPORAL]
        neo4j_query += Constants.NEO4J_SELECT_RETURN + Constants.COMMA
        for key in requestDictionary:
            if key!=requestDictionary:
                if(key=='event'):
                    neo4j_query+="event,"
                elif key=="informational":
                    neo4j_query+="info,"
                elif key=="spatial":
                    neo4j_query+="spatial,"
        neo4j_query +=  Constants.SPACE
        neo4j_query += Constants.NEO4J_FUZZY_SCORE_AGGR(index_count)
        return neo4j_query

    def __postProcessResult(self,resultArray):
        logging.info("Post processing Neo4J response..")
        final_converted_list = []
        for result in resultArray:
            res = dict()
            video_node = result['video']
            temporal_node = result['temporal']
            res['video_id'] = video_node['video_id']
            res['video_url'] = self.youtubeAPI.getFinalYoutubeURL(video_node['video_url'],int(temporal_node['start_frame']))
            res['video_location'] = video_node['Location']
            res['start_frame'] = temporal_node['start_frame']
            res['end_frame'] = temporal_node['end_frame']
            final_converted_list.append(res)
        result = dict()
        result['responseList'] = final_converted_list
        logging.info("Generated final response")
        return result

    def __postProcessFuzzyResult(self,resultArray):
        logging.info("Post processing Neo4J fuzzy response..")
        final_converted_list = []
        for result in resultArray:
            res = dict()
            matched_tags = []
            video_node = result['video']
            temporal_node = result['temporal']
            res['video_id'] = video_node['video_id']
            res['video_url'] = self.youtubeAPI.getFinalYoutubeURL(video_node['video_url'],int(temporal_node['start_frame']))
            res['video_location'] = video_node['Location']
            res['start_frame'] = temporal_node['start_frame']
            res['end_frame'] = temporal_node['end_frame']
            res['score'] = result['score']
            if 'event' in result:
                matched_tags.append(result['event']['event'])
            if 'info' in result:
                matched_tags.append(result['info']['information'])
            if 'spatial' in result:
                matched_tags.append(result['spatial']['place'])
            res['tags'] = matched_tags
            final_converted_list.append(res)
        result = dict()
        result['responseList'] = final_converted_list
        logging.info("Generated final fuzzy response")
        return result
    