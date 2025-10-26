from datetime import datetime, timedelta
from jose import JWTError, jwt

SECURITY_KEY = "79989f0029414af8c502d2fddc9f46f589a492510a44682fdc83ce7cda035dd7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def createAccesToken(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expire})
    jwt_encod = jwt.encode(data_copy, SECURITY_KEY, algorithm=ALGORITHM)
    return jwt_encod


def verifyAccesKey(token: str):
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=ALGORITHM)
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None
