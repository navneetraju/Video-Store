import csv
import collections
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from WriteWorkers import connect_db
from WriteWorkers import create_node_relations
import logging
import properties
from WriteWorkers.WriteQuery import WriteQuery
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)
import Constants
import time

class Combine:

    def __init__(self, dbName):
        self.dbName = dbName
        connect_db.Connect_DB(self.dbName)
        
        self.node_object = create_node_relations.Node_Relations()
        # self.write_object = WriteQuery()
        self.write_object = WriteQuery(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD, dbName=self.dbName)

    def combine_multi(self, json1, json2):
        # json1 : message from topic
        # json2 : message from database config
        final_query = ""
        print("MutiColumn")
        if(json2['mappings']['unique_id'] in json1):
            value = {'video_id': json1[json2['mappings']['unique_id']]}
            value['video_url'] = "https://www.youtube.com/watch?v="+json1[json2['mappings']['unique_id']]
            value['Location'] = "Youtube"
            final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])
        if(json2['mappings']['temporal']['temporal_start'] in json1):
            value = {'start_frame': json1[json2['mappings']['temporal']['temporal_start']]}
            value['end_frame'] = json1[json2['mappings']['temporal']['temporal_end']]
            value['video_id'] = json1[json2['mappings']['unique_id']]
            final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])
        if(json2['mappings']['Experiential'] in json1):
            value = {'event': json1[json2['mappings']['Experiential']]}
            final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
        if(json2['mappings']['Informational'] in json1):
            value = {'information': json1[json2['mappings']['Informational']]}
            final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
        
        # if(json2['mappings']['Spatial'] in json1):
        #     value = {'place': json1[json2['mappings']['Spatial']]}
        #     final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
        self.write_object.write_query(final_query, self.dbName)

    def combine_single(self, json1, json2, json3):
        # json1: message from topic
        # json2: message from mapping config
        # json3: message from database config
        print("Started Executing Single Coulmn")
        final_query = ""
        tags = json1[json3['mappings']['SingleColumnName']].split(json3['mappings']['delimiter'])
        if(json3['mappings']['unique_id'] in json1):
            value = {'video_id': json1[json3['mappings']['unique_id']]}
            value['video_url'] = "https://www.youtube.com/watch?v="+json1[json3['mappings']['unique_id']]
            value['Location'] = "Youtube"
            final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])
        if(json3['mappings']['temporal']['temporal_start']):
            value = {'start_frame': json1[json3['mappings']['temporal']['temporal_start']]}
            value['end_frame'] = json1[json3['mappings']['temporal']['temporal_end']]
            value['video_id'] = json1[json3['mappings']['unique_id']]
            final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])
        for val in tags:
            if(val in json2['mappings'] and json2['mappings'][val] == "spatial"):
                value = {'place': val}
                final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
            if(val in json2['mappings'] and json2['mappings'][val] == "Experiential"):
                value = {'event': val}
                final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
            if(val in json2['mappings'] and json2['mappings'][val] == "Informational"):
                value = {'information': val}
                final_query += self.node_object.create_node(value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
        self.write_object.write_query(final_query, self.dbName)
        print("Finished Execution Single Column")


        # with open(filename) as csv1:
        #     read = csv.reader(csv1, delimiter=',')
        #     res = collections.defaultdict()
        #     line_count = 0
        #     for row in read:
        #         if(line_count != 0):
        #             if(row[1] == "scene"):
        #                 res[row[0]] = "spatial"
        #             if(row[1] == "object" or row[1] == "attribute"):
        #                 res[row[0]] = "inforational"
        #             if(row[1] == "action" or row[1] == "event"):
        #                 res[row[0]] = "experiential"
        #         line_count += 1
        #     # print(res)

        
        # with open(filename2) as csv2:
        #     read = csv.reader(csv2, delimiter = ',')
        #     line_count = 0
        #     for row in read:
        #         if(line_count != 0):
        #             v_value = {}
        #             v_value["video_id"] = row[1]
        #             v_value["video_url"] = "https://www.youtube.com/watch?v="+row[1]
        #             v_value["Location"] = "Youtube"
        #             # v_value = []
        #             # v_value.append(row[1])
        #             # v_value.append("Youtube")
        #             # v_value.append("https://www.youtube.com/watch?v="+row[1])
        #             create_video = self.node_object.create_node(v_value, Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])

        #             tags = row[0].split("|")
        #             s_value = {}
        #             i_value = {}
        #             e_value = {}
        #             create_spatial = " "
        #             create_experiential = " "
        #             create_informational = " "
        #             for tag in tags:
        #                 if(tag in res ):
        #                     if(res[tag] == "spatial"):
        #                         s_value = {"place": tag}
        #                         # s_value = tag
        #                         create_spatial = self.node_object.create_node(s_value, Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
                            
        #                     if(res[tag] == "informational"):
        #                         i_value = {"information": tag}
        #                         # i_value = tag
        #                         create_informational = self.node_object.create_node(s_value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
                            
        #                     if(res[tag] == "experiential"):
        #                         e_value = {"event": tag}
        #                         # e_value = tag
        #                         create_experiential = self.node_object.create_node(e_value, Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
        #                 else:
        #                     print("Tag not present ", tag)
                            
        #             t_value = {}
        #             t_value["video_id"] = row[1]
        #             t_value["start_frame"] = row[2]
        #             t_value["end_frame"] = row[3]
        #             # t_value = []
        #             # t_value.append(row[0])
        #             # t_value.append(row[2])
        #             # t_value.append(row[3])
        #             create_temporal = self.node_object.create_node(t_value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])

        #             create_nodes = create_video + create_temporal + create_informational + create_experiential + create_spatial
                    
        #             one_way_relation = self.node_object.create_oneway_relation(t_value, v_value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
        #                 Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
        #                     Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO], Constants.NEO4J_RELATIONSHIP_VT)

        #             # relations_query = self.node_object.create_twoway_relation(i_value, t_value, e_value, s_value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]\
        #             #     , Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
        #             #         Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL], Constants.NEO4J_RELATIONSHIP_IT, Constants.NEO4J_RELATIONSHIP_ET, Constants.NEO4J_RELATIONSHIP_ST)

        #             if(e_value):
        #                 two_way_relation = self.node_object.create_twoway_relation(e_value, t_value, \
        #                     Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
        #                         Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
        #                             Constants.NEO4J_RELATIONSHIP_ET)
        #             if(i_value):
        #                 two_way_relation = self.node_object.create_twoway_relation(i_value, t_value, \
        #                     Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
        #                         Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
        #                             Constants.NEO4J_RELATIONSHIP_IT)
                    
        #             if(s_value):
        #                 two_way_relation = self.node_object.create_twoway_relation(s_value, t_value, \
        #                     Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
        #                         Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
        #                             Constants.NEO4J_RELATIONSHIP_ST)
        #             print(create_nodes, one_way_relation, two_way_relation)
        #             final_query = create_nodes + one_way_relation + two_way_relation
        #             self.write_object.write_query(final_query, self.dbName)
        #         line_count += 1

# if(__name__ == '__main__'):
#     combineObj = Combine()
#     combineObj.combine("../../HVU_Tags_Categories_V1.0.csv", "../../HVU_Train_V1.0.csv")
    #combine("HVU_Tags_Categories_V1.0.csv", "HVU_Train_V1.0.csv")