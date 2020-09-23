from inverted_index_base import *
from clip_vid import *
from query_parser import *
from index_store import *
from play_video import *
from read_csv import *
import os.path
from os import path

'''
Use this file for integration of all modules and system testing.
Each module has to be written in a seperate .py file and imported as above
This helps code maintenance and debugging.
'''

if __name__ =="__main__":
    if path.exists('sports.index'):
        index=load_index('sports.index')
    else:
        read_from_csv('BoundingBoxes.csv')
        index=load_index('sports.index')
    query="query"
    while query!='q':
        query=input('Enter Query: ')
        if query=='q':
            exit()
        keywords=get_Keywords(query)
        print(keywords)
        if len(keywords)==2:
            retrDocs=index.get_sport_activity(keywords[0],keywords[1])
        else:
            retrDocs=index.get_sport(keywords[0])
        if retrDocs ==None or len(retrDocs)==0:
            print('NO VIDEOS FOUND!')
            continue
        retrDocs=list(retrDocs.keys())
        #print(retrDocs)
        play_video(retrDocs)
