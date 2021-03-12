import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Neo4jConnection import Neo4jConnection
import Constants
import properties

class InsertData:
    def __init__(self, dbName, filename):
        self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD)
        self.dbName = dbName
        self.filename = filename
        self.connect_to_db(self.dbName)
        self.read_csv(filename)
        
    def connect_to_db(self, dbName):
        try:
            self.conn.query("CREATE DATABASE youtube IF NOT EXISTS")
        except:
            print("Database is not Created.. Something went Wrong")
            exit()
         
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

    def create_node(self, json, node_name, node_mapping):
        """
        json : entry_data[Constants.VIDEO]
        node_name : Constants.NEO4J_NODE_NAMES[Constants.VIDEO]
        node_mapping : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO]
        """
        match_video_query = "MATCH " + node_mapping + " WHERE "
        n = len(json)
        for key in json:
            match_video_query += node_name + "." + key + "=\'" + json[key] + "\'"
            n -= 1
            if(n >= 1):
                match_video_query += " AND "
        match_video_query += " RETURN " + node_name
        res_video = self.conn.query(match_video_query, self.dbName)
        if(res_video):
            pass
        else:
            create_video_query = "UNWIND $batch as row CREATE " + node_mapping + \
            " SET " + node_name + "+= row" + " RETURN " + node_name
            res_video = self.conn.query(create_video_query, self.dbName, json)

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
        relation_match = "MATCH " + node_mapping1 + "-[relation:" + node_relation + "]->" + node_mapping2 + " WHERE "
        relation_match += data_after_where
        relation_match += " RETURN relation"
        res_relation = self.conn.query(relation_match, self.dbName)
        # print(res_relation)
        if(not res_relation):
            relation = "MATCH " + node_mapping2 + ", " + node_mapping1 + " WHERE "
            relation += data_after_where
            relation_forward = " CREATE (" + node_name1+ ")-[:" + node_relation + "]->(" + node_name2 + ") RETURN " + node_name1 + ", " + node_name2
            self.conn.query(relation + relation_forward, self.dbName)   

    def create_twoway_relation(self, json1, json2, node_name1, node_name2, node_mapping1, node_mapping2, node_relation):
        """
        json1 : entry_data[Constants.INFORMATIONAL]
        json2 : entry_data[Constants.TEMPORAL]
        node_name1 : Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL]
        node_name2 : Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL]
        node_mapping1 : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL]
        node_mapping2 : Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL]
        """
        data_after_where = self.combine_check_data(json1, json2, node_name1, node_name2)
        relation_match = "MATCH " + node_mapping1 + "-[relation:" + node_relation + "]->" + node_mapping2 + " WHERE "
        relation_match += data_after_where
        relation_match += " RETURN relation"
        res_relation = self.conn.query(relation_match, self.dbName)
        # print(res_relation)
        if(not res_relation):
            relation = "MATCH " + node_mapping2 + ", " + node_mapping1 + " WHERE "
            relation += data_after_where
            relation_forward = " CREATE (" + node_name1+ ")-[:" + node_relation + "]->(" + node_name2 + ") RETURN " + node_name1 + ", " + node_name2
            relation_backward = " CREATE (" + node_name2 + ")-[:" + node_relation + "]->(" + node_name1 + ") RETURN " + node_name2 + ", " + node_name1
            self.conn.query(relation + relation_forward, self.dbName)   
            self.conn.query(relation + relation_backward, self.dbName)

    def read_csv(self, filename):
        """
        Read the data from the CSV File and convert the datapoints to the corresponding JSON Object.
        
        Input: File name of the CSV File
        Operation: 
        Output: Updated DB
        """
        import csv

        with open(filename) as csv1:
            read = csv.reader(csv1, delimiter=',')
            line_count = 0
            # Assuming we know the required parameters
            for row in read:
                # if(line_count == 50):
                #     break
                if(line_count > 0):
                    v_value = {}
                    t_value = {}
                    s_value = {}
                    i_value = {}
                    e_value = {}
                    c_value = {}

                    v_value["video_id"] = row[0]
                    v_value["video_url"] = "https://www.youtube.com/watch?v="+row[0]
                    v_value["Location"] = "Youtube"

                    t_value["video_id"] = row[0]
                    t_value["start_frame"] = row[1]
                    t_value["end_frame"] = row[2]

                    if(row[3]):
                        s_value["place"] = row[3]

                    if(row[4]):
                        i_value["information"] = row[4]

                    if(row[5]):
                        e_value["event"] = row[5]
                    
                    if(row[6]):
                        c_value["causality"] = row[6]

                    entry_data = {Constants.VIDEO:v_value, Constants.TEMPORAL:t_value, \
                        Constants.SPATIAL: s_value, Constants.INFORMATIONAL: i_value, \
                            Constants.EXPERENTIAL: e_value, Constants.CAUSALITY: c_value}                 
                    
                    if(entry_data[Constants.VIDEO]):
                        # print("Execute Video")       
                        self.create_node(entry_data[Constants.VIDEO], Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])                                         
                        
                    if(entry_data[Constants.TEMPORAL]):
                        # print("Execute Temporal")
                        self.create_node(entry_data[Constants.TEMPORAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])
                        
                    if(entry_data[Constants.SPATIAL]):
                        # print("Execute Spatial")
                        self.create_node(entry_data[Constants.SPATIAL], Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
                        
                    if(entry_data[Constants.EXPERENTIAL]):
                        # print("Excute Experiential")
                        self.create_node(entry_data[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
                        
                    if(entry_data[Constants.INFORMATIONAL]):
                        # print("Execute Informational")
                        self.create_node(entry_data[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
                        
                    if(entry_data[Constants.CAUSALITY]):
                        # print("Execute Causality")
                        self.create_node(entry_data[Constants.CAUSALITY], Constants.NEO4J_NODE_NAMES[Constants.CAUSALITY], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.CAUSALITY])
                        
                    self.create_oneway_relation(entry_data[Constants.TEMPORAL], entry_data[Constants.VIDEO], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                        Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO], Constants.NEO4J_RELATIONSHIP_VT)
                                       
                    if(entry_data[Constants.EXPERENTIAL]):
                        self.create_twoway_relation(entry_data[Constants.EXPERENTIAL], entry_data[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_ET)

                    if(entry_data[Constants.INFORMATIONAL]):
                        self.create_twoway_relation(entry_data[Constants.INFORMATIONAL], entry_data[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_IT)
                                            
                    if(entry_data[Constants.SPATIAL]):
                        self.create_twoway_relation(entry_data[Constants.SPATIAL], entry_data[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_ST)
                    
                line_count += 1

if(__name__ == '__main__'):
    InsertData("youtube", "Converted_Dataset.csv")
    