from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, database
from auth.authentication import getCurrentUser


router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=schemas.TodoRead)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(getCurrentUser),
):
    new_todo = models.Todo(
        title=todo.title, description=todo.description, owner_id=current_user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.get("/", response_model=list[schemas.TodoRead])
def get_all_todos(
    db: Session = Depends(database.get_db),
    currnetuser: models.User = Depends(getCurrentUser),
):
    todos = db.query(models.Todo).filter(models.Todo.owner_id == currnetuser.id)
    return todos


@router.get("/{todo_id}", response_model=schemas.TodoRead)
def get_todo(
    todo_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(getCurrentUser),
):

    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id)
        .first()
    )

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(getCurrentUser),
):
    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id)
        .first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Deleted successfully"}
