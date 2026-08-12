from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None

    
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
        
@app.post("/tasks", status_code=201)
async def create_task(task_data: TaskCreate):
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Bad Request")
    
    new_id = len(tasks)+1
    new_task = {
        "id": new_id,
        "title": task_data.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

