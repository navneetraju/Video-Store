import csv
import nltk

# 1: Temporal
# 2: Spatial
# 3: Informational
# 4: Experiential
# 5: Causality

def convert(filename):
    """
   
    """

    import collections

    with open(filename, "r") as file:
        csv_read = csv.reader(file, delimiter = ",")
        line = 0
        write_csv = open("converted.csv", "w")
        for row in csv_read:
            res = collections.defaultdict(dict)
            if(line == 50):
                break
            if(line == 0):
                line += 1
                write_csv.write("video_id,action,start_time,end_time"+"\n")
            else:
                tags = row[0].split("|")
                res[1] = {"name": row[1], "start_frame": row[2], "end_frame": row[3]}
                res[3] = {"action": tags[0]}
                
                pos_tag = nltk.pos_tag(tags)
                                        
                verbs = [word for word, tag in pos_tag if tag == 'VBG']
                
                line += 1
                print(verbs)
                for val in verbs:
                    write_csv.write(val+','+row[1]+','+row[2]+','+row[3]+"\n")
        write_csv.close()
            

convert("MHVU_Train.csv")