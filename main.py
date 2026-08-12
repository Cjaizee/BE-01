from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None
    done: bool | None = None

    
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

@app.put("/tasks/{id}")
async def update_task(id: int, task_data: TaskCreate):
    if task_data.title is None and task_data.done is None:
        raise HTTPException(status_code=400, detail="Bad Request: Body cannot be empty.")
    
    if task_data.title is not None and not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Bad Request: Title cannot be empty.")
    
    for task in tasks:
        if task["id"] == id:
            if task_data.title is not None:
                task["title"] = task_data.title.strip()
            if task_data.done is not None:
                task["done"] = task_data.done
            return task
    
    raise HTTPException(status_code=404, detail=f"task {id} not found.")

@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return
    
    raise HTTPException(status_code=404, detail=f"Task {id} not found")