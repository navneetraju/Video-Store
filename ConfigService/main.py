from fastapi import FastAPI, File, UploadFile, HTTPException
import yaml
from pymongo import MongoClient
import csv 
from io import StringIO
from schema import SchemaValidator
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)

mongo_connect=MongoClient('mongodb://%s:%s@10.10.1.146:27017' % ("root", "CLCFVSItr1"))
schemaValidator = SchemaValidator()

app = FastAPI()
    
@app.post("/api/config/data",status_code=201)
async def writeDataConfig(config: UploadFile = File(...)):
    logging.info("Received request for creating data config..")
    if config.content_type!="content/yaml" and config.content_type!="text/yaml":
        logging.error("Received config is not a YAML file")
        raise HTTPException(status_code=400,detail="Expected YAML file")
    s = yaml.load(config.file)
    is_valid, msg = schemaValidator.validate_json(s,"DATA")
    if not is_valid:
        raise HTTPException(status_code=400,detail=msg)
    config_db=mongo_connect['configurations']
    data_col=config_db["data"]
    if len(list(data_col.find({"database":s['database']}))) != 0:
        logging.info("Record already exists in mongodb, updating existing record")
        newvalues={"$set":s}
        data_col.update_one({"database":s['database']},newvalues)
        logging.info("Updated existing record")
        return {'detail':'Updated config successfully'}
    else:
        logging.info("Storing config into database")
        data_col.insert_one(s)
    return {'detail':'Added config successfully'}

@app.get("/api/config/data",status_code=200)
async def readDataConfig(database: str):
    logging.info("Recived request for retrieving config")
    config_db=mongo_connect['configurations']
    data_col=config_db["data"]
    mongo_fetch_query={'database':database}
    fetched_doc=data_col.find(mongo_fetch_query)
    fetched_doc=list(fetched_doc)
    if len(fetched_doc)==0:
        logging.error("No record found in mongodb")
        raise HTTPException(status_code=400,detail='Config not found for given database')
    else: 
        logging.info("Found record in mongodb")
        config = fetched_doc[0]
        del config['_id']
        return config


@app.post("/api/config/mapping",status_code=201)
async def writeMappingConfig(mapping: UploadFile = File(...),config: UploadFile = File(...)):
    logging.info("Received request for creating mapping config..")
    if config.content_type!="content/yaml" and config.content_type!="text/yaml":
        logging.error("Received config is not a YAML file")
        raise HTTPException(status_code=400,detail="Expected config to YAML file")
    if mapping.content_type!="text/csv":
        logging.error("Received mapping is not a CSV file")
        raise HTTPException(status_code=400,detail="Expected mapping to be a CSV file")
    config = yaml.load(config.file)
    is_valid, msg = schemaValidator.validate_json(config,"MAPPING")
    if not is_valid:
        raise HTTPException(status_code=400,detail=msg)
    config = config['categoryMappings']
    mappingDict = dict()
    mappingDict['name'] = config['name']
    mappingDict['mappings'] = dict()
    modelMapping = config['eventModelMapping']
    f = StringIO(mapping.file.read().decode())
    reader = csv.reader(f, delimiter=',')
    l = next(reader)
    tag_index = l.index(config['tag'])
    category_index = l.index(config['category'])
    logging.info("Starting parsing for mapping CSV")
    for row in reader:
        tag = row[tag_index]
        category = row[category_index]
        if modelMapping[category] == "Ignore":
            continue
        mappingDict['mappings'][tag] = modelMapping[category]
    logging.info("Finished parsing for mapping CSV")
    config_db=mongo_connect['configurations']
    mapping_col=config_db["mapping"]
    if len(list(mapping_col.find({"name":config['name']}))) != 0:
        logging.info("Record already exists in mongodb, updating existing record")
        newvalues={"$set":mappingDict}
        mapping_col.update_one({"name":config['name']},newvalues)
        return {'detail':'Updated mapping config successfully'}
    else:
        logging.info("Storing mapping into database")
        mapping_col.insert_one(mappingDict)
    return {'detail':'Added mapping config successfully'}

@app.get("/api/config/mapping",status_code=200)
async def readDataMapping(configName: str):
    logging.info("Recived request for retrieving mapping config")
    config_db=mongo_connect['configurations']
    data_col=config_db["mapping"]
    mongo_fetch_query={'name':configName}
    fetched_doc=data_col.find(mongo_fetch_query)
    fetched_doc=list(fetched_doc)
    if len(fetched_doc)==0:
        logging.error("No record found in mongodb")
        raise HTTPException(status_code=400,detail='Mapping config not found for given database')
    else: 
        logging.info("Found record in mongodb")
        config = fetched_doc[0]
        del config['_id']
        return config