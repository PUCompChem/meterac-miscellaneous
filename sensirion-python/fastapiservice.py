from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Info": "Sensirion VOC/NOX calculation utils"}
