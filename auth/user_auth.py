from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.deps import get_db  # Ensure your get_db function is correctly imported
from db.crud import get_user_by_username  # Ensure your user models are imported
from auth.jwt_gen import oauth2_scheme, SECRET_KEY, ALGORITHM
from fastapi import Cookie
from loggs.logger import logger

credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credential problems"
        )

async def get_current_user(db: Session = Depends(get_db), token: str = Cookie(None)):
    # Check if token is present
    if token is None:
        logger.info("Token was NOT found!!!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    logger.info("Token was found!!!")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user