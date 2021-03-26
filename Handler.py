from Parser import parse
import Neo4jConnection 
from DataParsing import dataparsing
from Import import read_csv
import sys
import Constants
from Exceptions import *
import json
import logging
import properties
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)


parserObj = parse.Parser()
dataParserObj = dataparsing.DataParser()

class Handler:
    def __init__(self):
        self.parserObj = parse.Parser()
        self.queryProcessor = dataparsing.DataParser()

    def query(self,requestQuery:str,fuzzy:bool):
        logging.info("Recieved query request, starting handling...")
        if requestQuery == None or len(requestQuery) == 0:
            return json.dumps({"code":400,"message":"Invalid request query"})
        parsedDictionary = None 
        try:
            parsedDictionary = self.parserObj.parseQuery(requestQuery)[0]
        except Exception as e:
            logging.error("Handling parsing exception ",exc_info=True)
            return json.dumps({"code":400,"message":"Query syntax error: "+ str(e)})

        if parsedDictionary['type'] == Constants.INSERT:
            #To-do @Durga to add insert object call and handle exceptions
            try:
                logging.info("Reading the CSV and Inserting into the Database...")
                self.readObj = read_csv.ReadCsv("Converted_Dataset.csv", "youtube")
                self.readObj.read_csv()
                return json.dumps({"code": 200, "message": "CSV File is read and data is inserted into the DB"})
            except:
                logging.error("Something Went Wrong with reading the CSV...!")
            pass 
        elif parsedDictionary['type'] == Constants.SELECT:
            result = None
            if fuzzy:
                logging.info("Starting fuzzy query")
                result = self.queryProcessor.fuzzyQuery(parsedDictionary)
            else:
                logging.info("Starting simple query")
                result = self.queryProcessor.query(parsedDictionary)
            return result


'''
For reference only

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
'''