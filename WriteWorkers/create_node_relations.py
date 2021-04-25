import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# from Neo4jConnection import Neo4jConnection
import Constants
import properties
import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)


class Node_Relations:
    
    def combine_check_data(self, json1, json2, param1, param2):
        """
        json1 : entry_data[Constants.VIDEO]
        json2 : entry_data[Constants.TEMPORAL]
        param1 : Constants.NEO4J_NODE_NAMES[Constants.VIDEO]
        param2 : Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]
        """
        if(param1 == Constants.NEO4J_NODE_NAMES[Constants.VIDEO]):
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            param1 = json1['video_id'].replace("-", "")
        if(param1 == Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]):
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            param1 = json1['video_id'].replace("-", "") + str(int(json1['start_frame'])) + str(int(json1['end_frame']))
        if(param1 == Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]):
            param1 = json1['information']
        if(param1 == Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL]):
            param1 = json1['event']
        if(param1 == Constants.NEO4J_NODE_NAMES[Constants.SPATIAL]):
            param1 = json1['place']

        if(param2 == Constants.NEO4J_NODE_NAMES[Constants.VIDEO]):
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            param2 = json2['video_id'].replace("-", "")
        if(param2 == Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]):
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            param2 = json2['video_id'].replace("-", "") + str(int(json2['start_frame'])) + str(int(json2['end_frame']))
        if(param2 == Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]):
            param2 = json2['information']
        if(param2 == Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL]):
            param2 = json2['event']
        if(param2 == Constants.NEO4J_NODE_NAMES[Constants.SPATIAL]):
            param2 = json2['place']
        res_string = ""
        for key in json1:
            res_string += param1 + "." + key + "=\'" + \
                    str(json1[key]) + "\' AND "
        n = len(json2)
        for key in json2:
            res_string += param2 + "." + key + "=\'" + \
                str(json2[key]) + "\'"
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
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.VIDEO]):
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            node_name1 = json1['video_id'].replace("-", "")
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]):
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            node_name1 = json1['video_id'].replace("-", "") + str(int(json1['start_frame'])) + str(int(json1['end_frame']))
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]):
            node_name1 = json1['information']
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL]):
            node_name1 = json1['event']
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.SPATIAL]):
            node_name1 = json1['place']

        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.VIDEO]):
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            node_name2 = json2['video_id'].replace("-", "")
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]):
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            param2 = json2['video_id'].replace("-", "")
            node_name2 = json2['video_id'].replace("-", "") + str(int(json2['start_frame'])) + str(int(json2['end_frame']))
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]):
            node_name2 = json2['information']
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL]):
            node_name2 = json2['event']
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.SPATIAL]):
            node_name2 = json2['place']
        
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
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.VIDEO]):
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            if(json1['video_id'][0].isdigit()):
                json['video_id'] = json1['video_id'][1:]
            node_name1 = json1['video_id'].replace("-", "")
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]):
            if(json1['video_id'][0].isdigit()):
                json1['video_id'] = json1['video_id'][1:]
            if(json1['video_id'][0].isdigit()):
                json['video_id'] = json1['video_id'][1:]
            node_name1 = json1['video_id'].replace("-", "") + str(int(json1['start_frame'])) + str(int(json1['end_frame']))
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]):
            node_name1 = json1['information']
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL]):
            node_name1 = json1['event']
        if(node_name1 == Constants.NEO4J_NODE_NAMES[Constants.SPATIAL]):
            node_name1 = json1['place']
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.VIDEO]):
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            node_name2 = json2['video_id'].replace("-", "")
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]):
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            if(json2['video_id'][0].isdigit()):
                json2['video_id'] = json2['video_id'][1:]
            node_name2 = json2['video_id'].replace("-", "") + str(int(json2['start_frame'])) + str(int(json2['end_frame']))
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]):
            node_name2 = json2['information']
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL]):
            node_name2 = json2['event']
        if(node_name2 == Constants.NEO4J_NODE_NAMES[Constants.SPATIAL]):
            node_name2 = json2['place']
        relation_forward = "MERGE (" + node_name1+ ")-[:" + node_relation + "]->(" + node_name2 + ")\n"  
        relation_backward = "MERGE (" + node_name2 + ")-[:" + node_relation + "]->(" + node_name1 + ")\n"
        return  relation_forward +  relation_backward
        