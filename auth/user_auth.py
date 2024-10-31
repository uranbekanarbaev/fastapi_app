from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.database import get_db  # Ensure your get_db function is correctly imported
from db.crud import get_user_by_username  # Ensure your user models are imported
from auth.jwt_gen import oauth2_scheme, SECRET_KEY, ALGORITHM
from fastapi import Cookie
from loggs.logger import logger

credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credential problems"
        )

from jose import ExpiredSignatureError

from fastapi import Cookie, HTTPException, Depends, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.crud import get_user_by_username
from auth.jwt_gen import SECRET_KEY, ALGORITHM
from loggs.logger import logger

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credential problems"
)

def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )
    try:
        logger.info(f"get current user func received the following access_token: {access_token}")
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info("Payload finished successfully")
        username: str = payload.get("sub")
        logger.info("Payload found username successfully")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except JWTError as e:
        logger.info(f"jwt error appeared {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )