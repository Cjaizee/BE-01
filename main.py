from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import copy
app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None
    done: bool | None = None
    
    
DEFAULT_TASKS = [{"id": 1,"title": "Job","done": False}, 
         {"id": 2,"title": "Fly","done": True}, 
         {"id": 3,"title": "AI","done": False},  
         ]

tasks = copy.deepcopy(DEFAULT_TASKS)

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
    
@app.get("/stats")
async def stats():
    total_tasks = len(tasks)
    done_tasks = 0
    for task in tasks:
        if task["done"] == True:
            done_tasks += 1
    open_tasks = total_tasks - done_tasks
    
    return{
        "total": total_tasks,
        "done": done_tasks,
        "open": open_tasks
    }

@app.get("/tasks")
def get_tasks(done: bool  = None, search: str = None):    
    result = tasks
    if done is not None:
        result = [task for task in result if task["done"] == done]
    if search is not None:
        result = [task for task in result if search.lower() in task["title"].lower()]
    return result

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

@app.post("/reset")
async def reset():
    global tasks
    tasks = copy.deepcopy(DEFAULT_TASKS)
    return {
        "message": "Success",
        "tasks": tasks
    }


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
