from fastapi import FastAPI, File, UploadFile
import tab2pydic

app = FastAPI()

@app.get("/process")
def process(file: UploadFile = File()(...)):
    return tab2pydic.process(file.file)

