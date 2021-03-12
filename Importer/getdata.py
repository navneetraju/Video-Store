import csv
import nltk

# 1: Temporal
# 2: Spatial
# 3: Informational
# 4: Experiential
# 5: Causality

def connect(dbname):
    """
    Connect to the MongoDB Cluster and then get/create the appropriate DB and Collections.
    Input: DB Name
    Operation: Get/Create the DB and Colelctions
    Output: Details/References of the collections and DB
    """
    from pymongo import MongoClient
    client = MongoClient("mongodb+srv://saioni:mongodb0605@cluster0.gblcy.mongodb.net/test?authSource=admin&replicaSet=atlas-l0sheq-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
    db = client[dbname]

    temporal = db["Temporal"]
    spatial = db["Spatial"]
    informational = db["Informational"]
    experiential = db["Experiential"]
    causality = db["Causality"]
    return {1:temporal, 2: spatial, 3: informational, 4: experiential, 5: causality}


def read_insert(filename, db_ref):
    """
    Read the data from the CSV File and convert data into the appropriate format {1:'', 2:'', 3:'', 4:'', 5:''}
    And also insert the data into the DB.
    Input: filename and the return value from the connect method
    Output: Data will be parsed and added to the DB row by row
    """
    import collections

    t_value = {}
    s_value = {}
    e_value = {}
    i_value = {}
    c_value = {}

    with open(filename, "r") as file:
        csv_read = csv.reader(file, delimiter = ",")
        line = 0
        for row in csv_read:
            res = collections.defaultdict(dict)
            if(line == 30):
                break
            if(line == 0):
                line += 1
            else:
                t_value["name"] = row[0]
                t_value["start_time"] = row[1]
                t_value["end_time"] = row[2]
                res[1] = t_value
                if(row[3]):
                    s_value["spatial"] = row[3]
                    res[2] = s_value

                if(row[4]):
                    e_value["informational"] = row[4]
                    res[3] = i_value

                if(row[5]):
                    i_value["experiencial"] = row[5]
                    res[4] = e_value

                if(row[6]):
                    c_value["causality"] = row[6]
                    res[5] = c_value                        
                               
                db_entry(res, db_ref)

                # tags = row[0].split("|")
                # res[1] = {"name": row[1], "start_frame": row[2], "end_frame": row[3]}
                # res[3] = {"action": tags[0]}
                
                # pos_tag = nltk.pos_tag(tags)
                # for tag in pos_tag:
                #     if(tag[1] not in full):
                #         full[tag[1]] = []
                #         full[tag[1]].append(tag[0])
                #     else:
                #         full[tag[1]].append(tag[0])             
                # verbs = [word for word, tag in pos_tag if tag == 'VBG' or tag == 'VBD' or tag == 'VBP']
                # res[row[1]] = verbs
                line += 1
                # db_entry(res, db_ref)``
                # full_data.append(res)
        # print(full)

def db_entry(entry_data, ref):
    """
    Entry to the DB is made from the input data received. And the ref i.e., the return of the connect method
    Input: JSON Object of the data to be inserted into the DB.
    Output: Data to be inserted into the DB and make the necessary links between collections.
    """
    new_entry = {}
    t_index = None
    s_index = None
    i_index = None
    e_index = None
    c_index = None
    name = {1:"Temporal", 2:"Spatial", 3:"Informational", 4:"Experiential", 5:"Causality"}
    if(entry_data[1]):
        pre_check = ref[1].find_one(entry_data[1])
        if(pre_check):
            t_index = pre_check["_id"]
        else:
            t_val = ref[1].insert_one(entry_data[1])
            t_index = t_val.inserted_id
        new_entry[1] = t_index
        
    if(entry_data[2]):
        pre_check = ref[2].find_one(entry_data[2])
        if(pre_check):
            s_index = pre_check["_id"]
        else:
            s_val = ref[2].insert_one(entry_data[2])
            s_index = s_val.inserted_id
        new_entry[2] = s_index

    if(entry_data[3]):
        pre_check = ref[3].find_one(entry_data[3])
        if(pre_check):
            i_index = pre_check["_id"]
        else:
            i_val = ref[3].insert_one(entry_data[3])
            i_index = i_val.inserted_id
        new_entry[3] = i_index

    if(entry_data[4]):
        pre_check = ref[4].find_one(entry_data[4])
        if(pre_check):
            e_index = pre_check["_id"]
        else:
            e_val = ref[4].insert_one(entry_data[4])
            e_index = e_val.inserted_id
        new_entry[4] = e_index

    if(entry_data[5]):
        pre_check = ref[5].find_one(entry_data[5])
        if(pre_check):
            c_index = pre_check["_id"]
        else:
            c_val = ref[5].insert_one(entry_data[5])
            c_index = c_val.inserted_id
        new_entry[5] = c_index

    index = {1:t_index, 2: s_index, 3: i_index, 4: e_index, 5: c_index}
    
    for i in new_entry:
        dest = i
        for j in new_entry:
            if(i != j):
                ref[dest].update_one(entry_data[dest], {'$push' : {"creator": {'$ref': name[j], '$id': index[j]}}})

ref = connect("Test")
read_insert("Converted_Dataset.csv", ref)

