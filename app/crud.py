from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from auth.hashing import Hash


def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def createUser(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        username=user.username, email=user.email, password=Hash.hashing(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
