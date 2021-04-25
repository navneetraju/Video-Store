import csv
import collections
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from WriteWorkers.create_node_relations import Node_Relations
import logging
import properties
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)
import Constants
import time
import json

class Combine:

    def __init__(self):
        self.node_obj = Node_Relations()
    
    def relation(self, v_value, t_value, e_value, i_value, s_value):
        final_query = ""
        node_obj = Node_Relations()
        if(v_value and t_value):
            final_query += node_obj.create_oneway_relation(t_value, v_value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO], Constants.NEO4J_RELATIONSHIP_VT)
        if(e_value):
            final_query += node_obj.create_twoway_relation(e_value, t_value, Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], Constants.NEO4J_RELATIONSHIP_ET)
        if(i_value):
            final_query += node_obj.create_twoway_relation(i_value, t_value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], Constants.NEO4J_RELATIONSHIP_IT)
        if(s_value):
            final_query += node_obj.create_twoway_relation(s_value, t_value, \
                            Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_ST)
        return final_query

    def combine_multi(self, json1, json2):
        # json1 : message from topic
        # json2 : message from database config
        final_query = ""
        node_obj = Node_Relations()
        v_value = {}
        t_value = {}
        e_value = {}
        s_value = {}
        i_value = {}
        if("id" in json1):
            v_value = {'video_id': json1["id"]}
            v_value['video_url'] = "https://www.youtube.com/watch?v="+json1["id"]
            v_value['Location'] = "Youtube"
            final_query += node_obj.create_node(v_value, Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])
        if(json2['mappings']['temporal']['temporal_start'] in json1):
            t_value = {'start_frame': json1[json2['mappings']['temporal']['temporal_start']]}
            t_value['end_frame'] = json1[json2['mappings']['temporal']['temporal_end']]
            t_value['video_id'] = json1[json2['mappings']['unique_id']]
            final_query += node_obj.create_node(t_value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])
        if(json2['mappings']['Experiential'] in json1):
            e_value = {'event': json1[json2['mappings']['Experiential']]}
            final_query += node_obj.create_node(e_value, Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
        if(json2['mappings']['Informational'] in json1):
            i_value = {'information': json1[json2['mappings']['Informational']]}
            final_query += node_obj.create_node(i_value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
        
        if(json2['mappings']['Spatial'] in json1):
            s_value = {'place': json1[json2['mappings']['Spatial']]}
            final_query += self.node_object.create_node(s_value, Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
        self.write_object.write_query(final_query, self.dbName)
        return final_query + self.relation(v_value, t_value, e_value, i_value, s_value)

    def combine_single(self, json1, json2, json3):
        # json1: message from topic
        # json2: message from mapping config
        # json3: message from database config
        final_query = ""
        tags = json1[json3['mappings']['SingleColumnName']].split(json3['mappings']['delimiter'])
        node_obj = Node_Relations()
        v_value = {}
        t_value = {}
        e_value = {}
        s_value = {}
        i_value = {}
        if(json3['mappings']['unique_id'] in json1):
            v_value = dict()
            v_value["video_id"] = json1[json3['mappings']['unique_id']]
            v_value['video_url'] = "https://www.youtube.com/watch?v="+json1[json3['mappings']['unique_id']]
            v_value['Location'] = "Youtube"
            final_query += node_obj.create_node(v_value, Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])
        if(json3['mappings']['temporal']['temporal_start'] in json1):
            t_value = dict()
            t_value['start_frame'] = json1[json3['mappings']['temporal']['temporal_start']]
            t_value['end_frame'] = json1[json3['mappings']['temporal']['temporal_end']]
            t_value['video_id'] = json1[json3['mappings']['unique_id']]
            final_query += node_obj.create_node(t_value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])
        for val in tags:
            if(val in json2['mappings'] and json2['mappings'][val] == "Spatial"):
                s_value = {'place': val}
                final_query += node_obj.create_node(s_value, Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
            if(val in json2['mappings'] and json2['mappings'][val] == "Experiential"):
                e_value = {'event': val}
                final_query += node_obj.create_node(e_value, Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
            if(val in json2['mappings'] and json2['mappings'][val] == "Informational"):
                i_value = {'information': val}
                final_query += node_obj.create_node(i_value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
            final_query += self.relation(v_value, t_value, e_value, i_value, s_value)
        #logging.info("Final Query: " + final_query)
        return final_query
        