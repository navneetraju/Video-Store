from fastapi import FastAPI,Response, status, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from Handler import Handler
from typing import Optional
from RecommendationEngine import engine
from Import.ImportHandler import ImportHandler
from Import.JobTracker import JobTracker
from fastapi import BackgroundTasks, FastAPI
import uuid

class Item(BaseModel):
    query: str

class JSONRequest(BaseModel):
    database: str
    dataset: str
    data: str

handler = Handler()
app = FastAPI()
query_engine=engine.QueryEngine()
importHandler = ImportHandler()
jobTracker = JobTracker()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://10.10.1.146:3000",
    "http://10.10.1.146",
    "http://10.10.1.146:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/recommend/{video_id}/{db_name}")
async def recommend(video_id: str, db_name: str, start: Optional[str] = None, end: Optional[str] = None):
    if start and end:
        recommended_list = query_engine.get_recommendation(video_id,start,end,db_name)
        return {'videos':recommended_list},200
    else:
        return json.dumps({'msg': 'Missing JSON'}),400


@app.post("/api/query")
async def main(fuzzy: str,request: Item,response: Response, status_code=200):
    val = fuzzy
    if val.lower() == "true":
        val = True
    else:
        val = False
    input_query = request
    if not input_query:
        return  json.dumps({'msg': 'Missing JSON'}),400
    handlerResponse = None
    if val:
        handlerResponse = await handler.query(input_query.query,True)
    else:
        handlerResponse = await handler.query(input_query.query,False)
    response.status_code = int(handlerResponse['code'])
    return handlerResponse

def insert(dataFile,database,dataset,jobID):
    importHandler.writeCSV(dataFile,database,dataset,jobID)

@app.post("/api/insert/csv",status_code=202)
async def csvDataInsertion(background_tasks: BackgroundTasks,database:str = Form(...) , dataset:str = Form(...),dataFile: UploadFile = File(...)):
    if dataFile.content_type != 'text/csv':
        raise HTTPException(status_code=400,detail="Expected file to be of CSV type")
    jobID = uuid.uuid1()
    background_tasks.add_task(insert, dataFile, database,dataset,str(jobID))
    return {"message": "Job accepted","jobID":jobID}

@app.post("/api/insert",status_code=202)
async def jsonDataInsertion(request: Request):
    body =  await request.json()
    if "database" not in body or "dataset" not in body:
        raise HTTPException(status_code=400,detail="Bad JSON, database and dataset fields not found")
    jobID = uuid.uuid1()
    jobID = str(jobID)
    resp = importHandler.writeJSON(body,jobID)
    if resp['status'] == 202:
        return {"message":resp["message"],"jobID":jobID}
    else:
        raise HTTPException(status_code=resp['status'],detail={"message":resp["message"],"jobID":jobID})
    

@app.get("/api/jobs/tracker",status_code=200)
async def checkJobStatus(jobID: str):
    resp = jobTracker.getJobStatus(jobID)
    if resp['status'] == 200:
        return resp['job']
    else:
        raise HTTPException(status_code=400,detail=resp['message'])