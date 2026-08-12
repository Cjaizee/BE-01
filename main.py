from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello I am Carl John T. Cueto"}