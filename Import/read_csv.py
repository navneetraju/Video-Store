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

class ReadCsv:
    def __init__(self, filename, dbName):
        self.dbName = dbName
        connect_db.Connect_DB("youtube")
        if(filename):
            self.filename = filename
        else:
            logging.info("Filename not Provided...")
            exit()
        self.node_object = create_node_relations.Node_Relations(self.dbName)

    def read_csv(self):
        """
        Read the data from the CSV File and convert the datapoints to the corresponding JSON Object.
        
        Input: File name of the CSV File
        Operation: 
        Output: Updated DB
        """
        import csv
        
        logging.info("Reading the file...")
        with open(self.filename) as csv1:
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
                        logging.info("Creating a Video Node...")       
                        self.node_object.create_node(entry_data[Constants.VIDEO], Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO])
                        logging.info("Video Node Created...!")
                        
                    if(entry_data[Constants.TEMPORAL]):
                        logging.info("Creating a Temporal Node...")
                        self.node_object.create_node(entry_data[Constants.TEMPORAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL])
                        logging.info("Temporal Node Created...!")
                        
                    if(entry_data[Constants.SPATIAL]):
                        logging.info("Creating Spatial Node...")
                        self.node_object.create_node(entry_data[Constants.SPATIAL], Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL])
                        logging.info("Spatial Node Created...!")
                        
                    if(entry_data[Constants.EXPERENTIAL]):
                        logging.info("Creating Experiential Node...")
                        self.node_object.create_node(entry_data[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL])
                        logging.info("Experiential Node Created...!")
                        
                    if(entry_data[Constants.INFORMATIONAL]):
                        logging.info("Creating Informational Node...")
                        self.node_object.create_node(entry_data[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL])
                        logging.info("Informational Node Created...!")
                        
                    if(entry_data[Constants.CAUSALITY]):
                        logging.info("Creating Causality Node...")
                        self.node_object.create_node(entry_data[Constants.CAUSALITY], Constants.NEO4J_NODE_NAMES[Constants.CAUSALITY], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.CAUSALITY])
                        logging.info("Causality Node Created...!")
                        
                    logging.info("Creating One way relation to the Video and Temporal Node...")
                    self.node_object.create_oneway_relation(entry_data[Constants.TEMPORAL], entry_data[Constants.VIDEO], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                        Constants.NEO4J_NODE_NAMES[Constants.VIDEO], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_TYPE_MAPPING[Constants.VIDEO], Constants.NEO4J_RELATIONSHIP_VT)
                    logging.info("One Way relation to the Video and Temporal Node is created...!")

                    if(entry_data[Constants.EXPERENTIAL]):
                        logging.info("Creating Two way relation to the Experiential and Temporal Node...")
                        self.node_object.create_twoway_relation(entry_data[Constants.EXPERENTIAL], entry_data[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_NAMES[Constants.EXPERENTIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.EXPERENTIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_ET)
                        logging.info("Two Way relation to the Experiential and Temporal Node is created...!")

                    if(entry_data[Constants.INFORMATIONAL]):
                        logging.info("Creating Two way relation to the Informational and Temporal Node...")
                        self.node_object.create_twoway_relation(entry_data[Constants.INFORMATIONAL], entry_data[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_NAMES[Constants.INFORMATIONAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.INFORMATIONAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_IT)
                        logging.info("Two Way relation to the Informational and Temporal Node is created...!")
                                            
                    if(entry_data[Constants.SPATIAL]):
                        logging.info("Creating One way relation to the Spatial and Temporal Node...")
                        self.node_object.create_twoway_relation(entry_data[Constants.SPATIAL], entry_data[Constants.TEMPORAL], \
                            Constants.NEO4J_NODE_NAMES[Constants.SPATIAL], Constants.NEO4J_NODE_NAMES[Constants.TEMPORAL], \
                                Constants.NEO4J_NODE_TYPE_MAPPING[Constants.SPATIAL], Constants.NEO4J_NODE_TYPE_MAPPING[Constants.TEMPORAL], \
                                    Constants.NEO4J_RELATIONSHIP_ST)
                        logging.info("Two Way relation to the Spatial and Temporal Node is created...!")
                    
                line_count += 1

if(__name__ == '__main__'):
    ReadCsv("Converted_Dataset.csv", "youtube")