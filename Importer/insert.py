# To keep track of how many collections were updated after each data entry
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


def read_csv(filename):
    """
    Read the data from the CSV File and convert the datapoints to the corresponding JSON Object.
    Then insert/update the documents in the respective collections. Link the documents based on the events.
    Input: File name of the CSV File
    Operation: Update/Insert the documents in the respective collections and update the links between the documents across collections
    Output: Updated DB
    """
    import csv

    with open(filename) as csv1:
        read = csv.reader(csv1, delimiter=',')
        line_count = 0
        # Assuming we know the required parameters
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
                
                ref = connect("Test")
                name = {1:"Temporal", 2:"Spatial", 3:"Informational", 4:"Experiential", 5:"Causality"}
                # to find the correct document to update the links
                check = {1:t_value, 2: s_value, 3: i_value, 4: e_value, 5: c_value}
                
                new_entry = {}
                if(t_value):
                    pre_check = ref[1].find_one(t_value)
                    if(pre_check):
                        t_index = pre_check["_id"]
                    else:
                        t_val = ref[1].insert_one(t_value)
                        t_index = t_val.inserted_id
                    new_entry[1] = t_index
                    
                if(s_value):
                    pre_check = ref[1].find_one(s_value)
                    if(pre_check):
                        s_index = pre_check["_id"]
                    else:
                        s_val = ref[2].insert_one(s_value)
                        s_index = s_val.inserted_id
                    new_entry[2] = s_index

                if(i_value):
                    pre_check = ref[3].find_one(i_value)
                    if(pre_check):
                        i_index = pre_check["_id"]
                    else:
                        i_val = ref[3].insert_one(i_value)
                        i_index = i_val.inserted_id
                    new_entry[3] = i_index

                if(e_value):
                    pre_check = ref[4].find_one(e_value)
                    if(pre_check):
                        e_index = pre_check["_id"]
                    else:
                        e_val = ref[4].insert_one(e_value)
                        e_index = e_val.inserted_id
                    new_entry[4] = e_index

                if(c_value):
                    pre_check = ref[5].find_one(c_value)
                    if(pre_check):
                        c_index = pre_check["_id"]
                    else:
                        c_val = ref[5].insert_one(c_value)
                        c_index = c_val.inserted_id
                    new_entry[5] = c_index

                index = {1:t_index, 2: s_index, 3: i_index, 4: e_index, 5: c_index}

                for i in new_entry:
                    dest = i
                    for j in new_entry:
                        if(i != j):
                            ref[dest].update(check[dest], {'$push' : {"creator": {'$ref': name[j], '$id': index[j]}}})
                
            line_count += 1
    return "Done..!"

print(read_csv("first.csv"))