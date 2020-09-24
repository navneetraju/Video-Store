import csv
from inverted_index_base import *
from index_store import *
from clip_vid import *

def read_from_csv(path):
	index=InvertedIndex()
	with open(path) as csv_file:
		csv_reader=csv.reader(csv_file,delimiter=',')
		line_count =0
		for row in csv_reader:
			if line_count == 0:
				line_count+=1
				continue
			else:
				line_count+=1
				f=row[0].split('/')
				if len(row[2])==0 or row[2]=='0':
					row[2]=get_num_frames("Videos/"+f[0]+"/"+f[1])
				index.add_sport_action(f[0].lower(),row[3].lower(),("Videos/"+f[0]+"/"+f[1],int(row[1]),int(row[2])))
	store_index(index)
