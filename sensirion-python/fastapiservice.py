from fastapi import FastAPI
from pydantic import BaseModel


class Node(BaseModel):
    name: str
    class Config:
        arbitrary_types_allowed = True

nodes = []


def debugInit():
    print("Debug Init: adding two demo nodes")
    nodes.append(Node(name = "N00T1"))
    nodes.append(Node(name = "N00T2"))

def startup():
    print("API startup ---- ")
    debugInit()

def shutdown():
    print("API shutdown ---- ")

app = FastAPI()
app.add_event_handler('startup', startup)
app.add_event_handler('shutdown', shutdown)


@app.get("/")
def root():
    return {"Info": "Sensirion VOC/NOX calculation utils"}

@app.get("/nodecount")
def nodecount():
    count = len(nodes)
    return {"NodeCount": count}
    #return count
