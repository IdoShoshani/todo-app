from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import datetime
import uvicorn
from todo_app import TodoManager, DatabaseConfig, Task, TaskStatus

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize database connection
config = DatabaseConfig()
todo_manager = TodoManager(config)

@app.on_event("startup")
async def startup():
    """Initialize database connection when app starts"""
    todo_manager.connect()
    todo_manager.create_tables()

@app.on_event("shutdown")
async def shutdown():
    """Close database connection when app stops"""
    todo_manager.close()

@app.get("/")
async def home(request: Request):
    """Display home page with all tasks"""
    tasks = todo_manager.get_all_tasks()
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "tasks": tasks,
            "datetime": datetime
        }
    )

@app.post("/add-task")
async def add_task(title: str = Form(...), description: str = Form(...)):
    """Add a new task"""
    task = Task(
        id=None,
        title=title,
        description=description,
        status=TaskStatus.PENDING,
        due_date=None,
        created_at=datetime.now()
    )
    todo_manager.add_task(task)
    return RedirectResponse("/", status_code=303)

@app.post("/update-status/{task_id}")
async def update_status(task_id: int, status: str = Form(...)):
    """Update task status"""
    try:
        new_status = TaskStatus(status)
        todo_manager.update_task_status(task_id, new_status)
        return RedirectResponse("/", status_code=303)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

@app.post("/delete-task/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    success = todo_manager.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete task")
    return RedirectResponse("/", status_code=303)

@app.post("/update-task/{task_id}")
async def update_task(
    task_id: int, 
    title: str = Form(...), 
    description: str = Form(...)
):
    """Update a task"""
    success = todo_manager.update_task(task_id, title, description)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update task")
    return RedirectResponse("/", status_code=303)

