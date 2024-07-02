from fastapi import FastAPI
from pydantic import BaseModel
from calcgasindex import *
from datetime import datetime

class ServerConfig(BaseModel):
    nodeFolder: str = "./nodes"
    

class Node(BaseModel):
    name: str
    vocParams:GasIndexAlgorithmParams = GasIndexAlgorithmParams()
    noxParams:GasIndexAlgorithmParams = GasIndexAlgorithmParams()
    class Config:
        arbitrary_types_allowed = True

def init():
    loadConfigFile()
    debugInit()
    
def loadConfigFile():
    print("Loading server configuration ...")
    
def debugInit():
    print("Debug Init: adding two demo nodes")
    nodes["N00T1"] = Node(name = "N00T1")
    nodes["N00T2"] = Node(name = "N00T2")

def startup():
    print("API startup ---- ", datetime.now(), datetime.utcnow())
    init()

def shutdown():
    print("API shutdown ---- ")

app = FastAPI()
app.add_event_handler('startup', startup)
app.add_event_handler('shutdown', shutdown)

nodes = {}

@app.get("/")
def root():
    return {"Info": "Sensirion VOC/NOX calculation utils"}

@app.get("/nodecount")
def nodecount():
    return {"NodeCount": getNodeCount()}

@app.get("/nodecount/obj")
def nodecount_obj():
    return getNodeCount()

@app.get("/nodelist")
def nodelist():
    #Test code
    return nodes["N00T1"].name
    
#----------------------------------------

def getNodeCount() -> int:
    return len(nodes)
