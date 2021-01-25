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
        t_value = {}
        s_value = {}
        i_value = {}
        e_value = {}
        c_value = {}
        t_value["name"] = row[0]
        t_value["start_frame"] = row[1]
        t_value["end_frame"] = row[2]
        t_value["creator"] = [{}]

        i_value["player"] = row[4]
        i_value["creator"] = [{}]

        e_value["action"] = row[3]
        e_value["creator"] = [{}]

        if(t_value):
            temporal.insert_one(t_value)
        if(s_value):
            spatial.insert_one(s_value)
        if(i_value):
            informational.insert_one(i_value)
        if(e_value):
            experiential.insert_one(e_value)
        if(c_value):
            causality.insert_one(c_value)
            

        print(row)