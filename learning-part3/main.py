from fastapi import FastAPI, Depends, HTTPException, Body, Path
from model import Todos
import model
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

model.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, )
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@app.get("/")
async def read_all(db: db_dependency):
    todo_model = db.query(Todos).all() 
    if todo_model is not None:
        return todo_model 
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos/{todos_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, todos_id: int = Path(gt=0)):
    todo_id_model = db.query(Todos).filter(todos_id).first()
    if todo_id_model is not None:
        return todo_id_model 
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos/add_todos/", status_code = status.HTTP_201_CREATED)
async def add_todos(db: db_dependency, todo_list: TodoRequest):
    todo_model = Todos(**todo_list)

    db.add(todo_model)
    db.commit()

@app.put("/todos/update_todos", status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(db: db_dependency, todo_id: int, todo_request: TodoRequest):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
