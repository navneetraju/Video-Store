import pickle
import hashedindex
import os.path
from os import path

'''
Stores hashedindex.HashedIndex as file
Return:
    True -> File is stored succesfully
    False -> File Exists/File not stored
'''
def store_index(index: hashedindex.HashedIndex):
    if path.exists('sports.index'):
        return False
    with open('sports.index', 'wb') as sports_index_file:
        try:
            pickle.dump(index, sports_index_file)
            return True
        except:
            return False
    return False

'''
Retrieves index from file and returns
Return:
    hashedindex.HashedIndex -> Index was found and has been returned
    None -> Index not found/Could not read file
'''
def load_index(pathname):
    with open('sports.index', 'rb') as sports_index_file:
        try:
            index = pickle.load(sports_index_file)
            return index
        except:
            return None
    return index