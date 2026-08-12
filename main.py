from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [{"id": 1,"title": "Job","done": False}, 
         {"id": 2,"title": "Fly","done": True}, 
         {"id": 3,"title": "AI","done": False},  
         ]

@app.get("/")
def home():
    return { 
            "name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] 
            }

    
@app.get("/health")
def health():
    return{
        "status": "ok"
        }
    
@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_id(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
        
    raise HTTPException(status_code=404, detail=f"Task {id} not found")
        
