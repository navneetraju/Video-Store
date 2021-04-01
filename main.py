from fastapi import FastAPI,Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from Handler import Handler


class Item(BaseModel):
    query: str

handler = Handler()
app = FastAPI()

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
        handlerResponse = handler.query(input_query.query,True)
    else:
        handlerResponse = handler.query(input_query.query,False)
    response.status_code = int(handlerResponse['code'])
    return handlerResponse