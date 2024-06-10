from fastapi import FastAPI

app = FastAPI()

def startup():
    print("API startup ---- ")

def shutdown():
    print("API shutdown ---- ")

app.add_event_handler('startup', startup)
app.add_event_handler('shutdown', shutdown)


@app.get("/")
def root():
    return {"Info": "Sensirion VOC/NOX calculation utils"}
