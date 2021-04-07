import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Neo4jConnection import Neo4jConnection
import Constants
import properties
import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)


class Node_Relations:
    # def __init__(self, dbName):
        # self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD)
        # self.dbName = dbName

    def combine_check_data(self, json1, json2, param1, param2):
        """
        json1 : entry_data[Constants.VIDEO]
        json2 : entry_data[Constants.TEMPORAL]
        param1 : Constants.NEO4J_NODE_NAMES[Constants.VIDEO]
        param2 : Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]
        """
        res_string = ""
        for key in json1:
            res_string += param1 + "." + key + "=\'" + \
                    json1[key] + "\' AND "
        n = len(json2)
        for key in json2:
            res_string += param2 + "." + key + "=\'" + \
                json2[key] + "\'"
            n -= 1
            if(n >= 1):
                res_string += " AND "
        return res_string

    def add_constraints(self, node_name, node_mapping, property):
        """
        node_name: Constants.NEO4J_NODE_NAMES[Constants.VIDEO]
        node_mapping: Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO]
        property: Constraint to be added on
        """
        query_constraint = "CREATE CONSTRAINT ON " + node_mapping + " ASSERT " + node_name + "." + property + " IS UNIQUE; "
        return query_constraint

    def create_node(self, json, node_name, node_mapping):
        """
        json : entry_data[Constants.VIDEO]
        node_name : Constants.NEO4J_NODE_NAMES[Constants.VIDEO]
        node_mapping : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO]
        """
        
        if(node_name == Constants.NEO4J_NODE_NAMES[Constants.VIDEO]):
            create_node_query = Constants.NEO4J_NODE_VIDEO(json)
        if(node_name == Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]):
            create_node_query = Constants.NEO4J_NODE_TEMPORAL(json)
        if(node_name == Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]):
            create_node_query = Constants.NEO4J_NODE_INFORMATIONAL(json)
        if(node_name == Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL]):
            create_node_query = Constants.NEO4J_NODE_EXPERIENTIAL(json)
        if(node_name == Constants.NEO4J_NODE_NAMES[Constants.SPATIAL]):
            create_node_query = Constants.NEO4J_NODE_SPATIAL(json)
        
        return create_node_query + "\n"
        

    def create_oneway_relation(self, json1, json2, node_name1, node_name2, node_mapping1, node_mapping2, node_relation):
        """
        json1 : entry_data[Constants.INFORMATIONAL]
        json2 : entry_data[Constants.TEMPORAL]
        node_name1 : Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]
        node_name2 : Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]
        node_mapping1 : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL]
        node_mapping2 : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL]
        """
        data_after_where = self.combine_check_data(json1, json2, node_name1, node_name2)
        relation_forward = "MERGE (" + node_name1+ ")-[:" + node_relation + "]->(" + node_name2 + ")\n"
        return  relation_forward
         

    def create_twoway_relation(self, json1, json2, node_name1, node_name2, node_mapping1, node_mapping2, node_relation):
        """
        json1 : entry_data[Constants.INFORMATIONAL]
        json2 : entry_data[Constants.TEMPORAL]
        
        node_name1 : Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]
        node_name2 : Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]
        
        node_mapping1 : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL]
        node_mapping2 : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL]
        
        node_relation : Constants.NEO4J_RELATIONSHIP_IT
        
        """
        
        relation_forward = "MERGE (" + node_name1+ ")-[:" + node_relation + "]->(" + node_name2 + ")\n"  
        relation_backward = "MERGE (" + node_name2 + ")-[:" + node_relation + "]->(" + node_name1 + ")\n"
        logging.info("Creating Two Way Relationships...")
        
        return  relation_forward +  relation_backward
        