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
        # match_video_query = "MATCH " + node_mapping + " WHERE "
        # n = len(json)
        # for key in json:
        #     match_video_query += node_name + "." + key + "=\'" + json[key] + "\'"
        #     n -= 1
        #     if(n >= 1):
        #         match_video_query += " AND "
        # match_video_query += " RETURN " + node_name
        # res_video = self.conn.query(match_video_query, self.dbName)
        # if(res_video):
        #     logging.info("Node Already exists and using the same...")
        # else:
        # create_node_query = "UNWIND $batch as row MERGE " + node_mapping + \
        # " SET " + node_name + "+= row"+ "; "
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
        # logging.info("Starting to Create a Node...")
        return create_node_query + "; "
        # res_video = self.conn.query(create_video_query, self.dbName, json)
        # logging.info("Node Created...!")

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
        # relation_match = "MATCH " + node_mapping1 + "-[relation:" + node_relation + "]->" + node_mapping2 + " WHERE "
        # relation_match += data_after_where
        # relation_match += " RETURN relation"
        # res_relation = self.conn.query(relation_match, self.dbName)
        # # print(res_relation)
        # if(not res_relation):
        logging.info("Creating One Way Relationship...")
        relation = "MATCH " + node_mapping2 + ", " + node_mapping1 + " WHERE "
        relation += data_after_where
        relation_forward = " MERGE (" + node_name1+ ")-[:" + node_relation + "]->(" + node_name2 + ") RETURN " + node_name1 + ", " + node_name2 + "; "
        # self.conn.query(relation + relation_forward, self.dbName)
        return relation + relation_forward
        # logging.info("Relationship Created...!")
        # else:
        #     logging.error("Relation Already Exist...")   

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
        # data_after_where = self.combine_check_data(json1, json2, node_name1, node_name2)
        # relation_match = "MATCH " + node_mapping1 + "-[relation:" + node_relation + "]->" + node_mapping2 + " WHERE "
        # relation_match += data_after_where
        # relation_match += " RETURN relation"
        # res_relation = self.conn.query(relation_match, self.dbName)
        # # print(res_relation)
        # if(not res_relation):
        data_after_where = self.combine_check_data(json1, json2, node_name1, node_name2)
        relation = "MATCH " + node_mapping2 + ", " + node_mapping1  + " WHERE "
        relation += data_after_where
        relation_forward = " MERGE (" + node_name1+ ")-[:" + node_relation + "]->(" + node_name2 + ") RETURN " + node_name1 + ", " + node_name2 + "; "  
        relation_backward = " MERGE (" + node_name2 + ")-[:" + node_relation + "]->(" + node_name1 + ") RETURN " + node_name2 + ", " + node_name1 + "; "
        logging.info("Creating Two Way Relationships...")
        # self.conn.query(relation + relation_forward, self.dbName)   
        # self.conn.query(relation + relation_backward, self.dbName)
        
        return relation + relation_forward + relation +  relation_backward
        # logging.info("Relationships got created...!")
        # else:
        #     logging.error("Relations Already Exist...")