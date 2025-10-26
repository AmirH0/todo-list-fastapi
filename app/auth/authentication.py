from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import crud, database, models
from . import jwt_handler


oauth2_pass = OAuth2PasswordBearer(tokenUrl="login")


def getCurrentUser(
    token: str = Depends(oauth2_pass), db: Session = Depends(database.get_db)
):
    user_id = jwt_handler.verifyAccesKey(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user
