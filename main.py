from Parser import parse
import Neo4jConnection 
from DataParsing import dataparsing
import sys

parserObj = parse.Parser()
dataParserObj = dataparsing.DataParser()

if __name__ == "__main__":
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
        parsedDictionary = dict()
        try:
            parsedDictionary = parserObj.parseQuery(user_writing)[0]
        except Exception:
            print("INVALID QUERY")
        dataParserObj.query(parsedDictionary)
        #print(dataParserObj.generateNeo4jQuery(parsedDictionary))