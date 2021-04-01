import csv
import collections
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from Import import connect_db
from Import import create_node_relations
import logging
import properties
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)
import Constants
import time

class Combine:

    def __init__(self):
        self.dbName = "youtube"
        connect_db.Connect_DB(self.dbName)
        
        self.node_object = create_node_relations.Node_Relations(self.dbName)

    def combine(self, filename, filename2):
        with open(filename) as csv1:
            read = csv.reader(csv1, delimiter=',')
            res = collections.defaultdict()
            line_count = 0
            for row in read:
                if(line_count != 0):
                    if(row[1] == "scene"):
                        res[row[0]] = "spatial"
                    if(row[1] == "object" or row[1] == "attribute"):
                        res[row[0]] = "inforational"
                    if(row[1] == "action" or row[1] == "event"):
                        res[row[0]] = "experiential"
                line_count += 1
            # print(res)

        
        with open(filename2) as csv2:
            read = csv.reader(csv2, delimiter = ',')
            line_count = 0
            for row in read:
                if(line_count != 0):
                    v_value = {}
                    v_value["video_id"] = row[1]
                    v_value["video_url"] = "https://www.youtube.com/watch?v="+row[1]
                    v_value["Location"] = "Youtube"
                    self.node_object.create_node(v_value, Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])

                    tags = row[0].split("|")
                    s_value = {}
                    i_value = {}
                    e_value = {}
                    for tag in tags:
                        if(tag in res ):
                            if(res[tag] == "spatial"):
                                s_value = {"place": tag}
                                self.node_object.create_node(s_value, Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
                            
                            if(res[tag] == "informational"):
                                i_value = {"information": tag}
                                self.node_object.create_node(s_value, Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
                            
                            if(res[tag] == "experiential"):
                                e_value = {"event": tag}
                                self.node_object.create_node(e_value, Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
                        else:
                            print("Tag not present ", tag)
                            
                    t_value = {}
                    t_value["video_id"] = row[0]
                    t_value["start_frame"] = row[2]
                    t_value["end_frame"] = row[3]
                    self.node_object.create_node(t_value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])

                    self.node_object.create_oneway_relation(t_value, v_value, Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                        Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO], Constants.NEO4J_RELATIONSHIP_VT)

                    if(e_value):
                        self.node_object.create_twoway_relation(e_value, t_value, \
                            Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_ET)
                    if(i_value):
                        self.node_object.create_twoway_relation(i_value, t_value, \
                            Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_IT)
                    
                    if(s_value):
                        self.node_object.create_twoway_relation(s_value, t_value, \
                            Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_ST)

                line_count += 1

if(__name__ == '__main__'):
    combineObj = Combine()
    combineObj.combine("../../HVU_Tags_Categories_V1.0.csv", "../../HVU_Train_V1.0.csv")
    #combine("HVU_Tags_Categories_V1.0.csv", "HVU_Train_V1.0.csv")