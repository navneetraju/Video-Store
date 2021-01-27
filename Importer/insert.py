
# Import the client 
from pymongo import MongoClient

# Connecting to the Client
client = MongoClient("mongodb+srv://saioni:mongodb0605@cluster0.gblcy.mongodb.net/test?authSource=admin&replicaSet=atlas-l0sheq-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")

dbs = client.list_database_names()

if("Test" not in dbs):
    # connecting to the DB
    db = client["Test"]
else:
    db = client.Test

# List of collections
collections = db.list_collection_names()

if("Temporal" not in collections):
    temporal = db["Temporal"]
else:
    temporal = db.Temporal

if("Spatial" not in collections):
    spatial = db["Spatial"]
else:
    spatial = db["Spatial"]

if("Informational" not in collections):
    informational = db["Informational"]
else:
    informational = db["Informational"]

if("Experiential" not in collections):
    experiential = db["Experiential"]
else:
    experiential = db["Experiential"]

if("Causality" not in collections):
    causality = db["Causality"]
else:
    causality = db["Causality"]


# Read the data from the CSV file
import csv

with open("first.csv") as csv1:
    read = csv.reader(csv1, delimiter=',')
    line_count = 0
    print(read)
    # Assuming we know the required parameters
    # t_value = {}
    # s_value = {}
    # i_value = {}
    # e_value = {}
    # c_value = {}
    for row in read:
        if(line_count != 0):
            t_value = {}
            s_value = {}
            i_value = {}
            e_value = {}
            c_value = {}
            t_index = None
            s_index = None
            i_index = None
            e_index = None
            c_index = None
            
            t_value["name"] = row[0]
            t_value["start_frame"] = row[1]
            t_value["end_frame"] = row[2]

            i_value["player"] = row[4]

            e_value["action"] = row[3]
            
            # To keep track of how many collections were updated after each data entry
            # 1: Temporal
            # 2: Spatial
            # 3: Informational
            # 4: Experiential
            # 5: Causality
            ref = {1:temporal, 2: spatial, 3: informational, 4: experiential, 5: causality}
            name = {1:"Temporal", 2:"Spatial", 3:"Informational", 4:"Experiential", 5:"Causality"}
            # to find the correct document to update the links
            check = {1:t_value, 2: s_value, 3: i_value, 4: e_value, 5: c_value}
            
            new_entry = {}
            if(t_value):
                pre_check = temporal.find_one(t_value)
                if(pre_check):
                    t_index = pre_check["_id"]
                else:
                    t_val = temporal.insert_one(t_value)
                    t_index = t_val.inserted_id
                new_entry[1] = t_index
                
            if(s_value):
                pre_check = spatial.find_one(s_value)
                if(pre_check):
                    s_index = pre_check["_id"]
                else:
                    s_val = spatial.insert_one(s_value)
                    s_index = s_val.inserted_id
                new_entry[2] = s_index

            if(i_value):
                pre_check = informational.find_one(i_value)
                if(pre_check):
                    i_index = pre_check["_id"]
                else:
                    i_val = informational.insert_one(i_value)
                    i_index = i_val.inserted_id
                new_entry[3] = i_index

            if(e_value):
                pre_check = experiential.find_one(e_value)
                if(pre_check):
                    e_index = pre_check["_id"]
                else:
                    e_val = experiential.insert_one(e_value)
                    e_index = e_val.inserted_id
                new_entry[4] = e_index

            if(c_value):
                pre_check = causality.find_one(c_value)
                if(pre_check):
                    c_index = pre_check["_id"]
                else:
                    c_val = causality.insert_one(c_value)
                    c_index = c_val.inserted_id
                new_entry[5] = c_index

            index = {1:t_index, 2: s_index, 3: i_index, 4: e_index, 5: c_index}
         
            # Updating the links between the documents
            for i in new_entry:
                dest = i
                for j in new_entry:
                    if(i != j):
                        res = ref[dest].update(check[dest], {'$push' : {"creator": {'$ref': name[j], '$id': index[j]}}})
            
        line_count += 1