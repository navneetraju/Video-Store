from Parser import parse
import Neo4jConnection 
from DataParsing import dataparsing
import sys
import Constants
import pandas as pd
import json


parserObj = parse.Parser()
dataParserObj = dataparsing.DataParser()

class Handler:
    def __init__(self):
        self.parserObj = parse.Parser()
        self.queryProcessor = dataparsing.DataParser()

    def query(self,requestQuery:str,fuzzy:bool):
        if requestQuery == None or len(requestQuery) == 0:
            return json.dumps({"code":400,"message":"Invalid request query"})
        parsedDictionary = None 
        try:
            parsedDictionary = self.parserObj.parseQuery(requestQuery)[0]
        except Exception as e:
            return json.dumps({"code":400,"message":"Invalid request query: "+ str(e)})

        if parsedDictionary['type'] == Constants.INSERT:
            #To-do @Durga to add insert object call and handle exceptions
            pass 
        elif parsedDictionary['type'] == Constants.SELECT:
            result = None
            if fuzzy:
                result = self.queryProcessor.fuzzyQuery(parsedDictionary)
            else:
                result = self.queryProcessor.query(parsedDictionary)
            return result



if __name__ == "__main__":
    handler = Handler()
    while True:
        user_writing = [] 
        print('Enter multiline query: ')
        while True: 
            line = input() 
            if not line: 
                break 
            else: 
                user_writing.append(line) 
        user_writing = '\n'.join(user_writing) 
        print(handler.query(user_writing,True))