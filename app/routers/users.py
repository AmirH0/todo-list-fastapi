from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database, schemas, crud
from auth.jwt_handler import createAccesToken
from auth.hashing import Hash


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=schemas.UserRead)
def registerUser(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    getuser = crud.getUserByEmail(db, user.email)
    if getuser:
        raise HTTPException(status_code=400, detail="email is already exist")

    newUser = crud.createUser(db, user)
    return newUser


@router.post("/login")
def LoginUser(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    dbUser = crud.getUserByEmail(db, user.email)
    if not dbUser:
        raise HTTPException(status_code=400, detail="invalid")

    if not Hash.verify(user.password, dbUser.password):
        raise HTTPException(status_code=400, detail="invalid")

    acces_Token = createAccesToken({"user_id": dbUser.id})
    return {"access_token": acces_Token, "token_type": "bearer"}
