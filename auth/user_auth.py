from fastapi import Depends, HTTPException, status, Cookie
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.database import get_db
from db.crud import get_user_by_username
from auth.jwt_gen import SECRET_KEY, ALGORITHM
from loggs.logger import logger

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credential problems"
)

def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    """Retrieve the current user based on the provided access token.

    Args:
        access_token (str): The JWT access token provided via cookies.
        db (Session): The database session dependency.

    Raises:
        HTTPException: If the access token is missing, invalid, or the user is not found.

    Returns:
        User: The user object retrieved from the database.
    """
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
