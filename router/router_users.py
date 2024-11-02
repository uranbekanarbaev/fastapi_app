"""
This module defines the API routes for managing users in the application.

It includes routes for:
- Retrieving all users.
- Retrieving a specific user by their ID.
- Creating a new user or authenticating an existing user.
- Updating user information.
- Deleting a user by their ID.
- Reading and setting cookies for session management.

Dependencies:
- FastAPI and its components for request handling, response generation, and dependency injection.
- SQLAlchemy for database interactions.
- Pydantic for data validation and serialization.
- Custom modules for database operations and JWT token generation.
- Logging for monitoring and debugging.

Usage:
- The API routes are registered with the FastAPI application and can be accessed via HTTP methods (GET, POST, PUT, DELETE).
"""


from fastapi.routing import APIRouter
from fastapi import Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from fastapi import Depends

from db.crud import (
    authenticate_user, get_all_users, get_user_by_username,
    create_user, get_user_by_user_id,
    update_user, delete_user
)
from auth.jwt_gen import create_access_token
from db.database import get_db
from db.schemas import UserResponse, UserCreate
from sqlalchemy.orm import Session 
from fastapi import HTTPException, status  
from auth.jwt_gen import create_access_token
from logs.logger import logger
from fastapi import Cookie
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

def user_not_found(task):
    if not task:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/users", response_class=HTMLResponse)
def users(request: Request, db: Session = Depends(get_db)):
    """Retrieve all users.

    Args:
        request (Request): The incoming request.
        db (Session): The database session.

    Returns:
        TemplateResponse: Renders the 'index.html' template with user data.
    """
    data = get_all_users(db)
    logger.info(f'data available {data}')
    return templates.TemplateResponse(request, 'index.html', {"data": data})

@router.get("/users/{user_id}")
def get_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific user by their ID.

    Args:
        request (Request): The incoming request.
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        User: The user data if found.
    """
    data = get_user_by_user_id(db, user_id)
    user_not_found(data)
    return data

@router.post("/users")
def register_user(
    response: Response,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user.

    Args:
        response (Response): The response object.
        user (UserCreate): The user data for registration.
        db (Session): The database session.

    Returns:
        JSONResponse: A response containing a message and user data.
    """
    try:
        existing_user = get_user_by_username(db, user.username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        
        new_user = create_user(db, user.username, user.password, user.email)

        logger.info(f'User {new_user.username} created successfully.')

        return JSONResponse(content={
            "message": "User created successfully",
            "user_data": UserResponse.from_orm(new_user).dict()
        })

    except Exception as e:
        logger.error(f"User creation failed: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed")

@router.post("/login")
def login_user(
    response: Response,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Authenticate an existing user.

    Args:
        response (Response): The response object.
        user (UserCreate): The user data for login.
        db (Session): The database session.

    Returns:
        JSONResponse: A response containing a message, access token, and user data.
    """
    authenticated_user = authenticate_user(db, user.username, user.password)
    
    if not authenticated_user:
        logger.warning(f"Invalid login attempt for username: {user.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": authenticated_user.username})
    logger.info(f'Access token generated for user {authenticated_user.username}')

    response = JSONResponse(content={
        "message": "Login successful",
        "token": access_token,
        "user_data": UserResponse.from_orm(authenticated_user).dict()
    })
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False
    )
    return response

@router.get("/read-cookie")
def read_cookie(access_token: str = Cookie(None)):
    """Read the access token from the cookie.

    Args:
        access_token (str): The access token from the cookie.

    Returns:
        dict: A dictionary containing the access token.
    
    Raises:
        HTTPException: If the access token cookie is not found.
    """
    if access_token is None:
        logger.warning("Cookie 'access_token' not found in request headers")
        raise HTTPException(status_code=400, detail="Cookie 'access_token' not found")
    return {"access_token_in_cookies": access_token}

@router.get("/debug-cookie")
async def debug_cookie(request: Request):
    """Debug endpoint to check cookies in the request.

    Args:
        request (Request): The incoming request.

    Returns:
        dict: A dictionary containing the token from the cookie if found.
    """
    cookies = request.cookies
    logger.info(f"All cookies in request: {cookies}")
    token = cookies.get("access_token")
    return {"token": token if token else "Token cookie not found"}

@router.post("/set-cookies")
async def set_cookies(request: Request, response: Response):
    """Set a fake session cookie.

    Args:
        request (Request): The incoming request.
        response (Response): The response object.

    Returns:
        Response: The response object with the cookie set.
    """
    response.set_cookie(key="fakesession123", value="fake123-cookie-session-value")

@router.put("/users/{user_id}")
def update_user_route(
    request: Request,
    user: UserCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update user information.

    Args:
        request (Request): The incoming request.
        user_id (int): The ID of the user to update.
        db (Session): The database session.
        username (str): The new username.
        email (str): The new email.

    Returns:
        dict: A dictionary containing the updated user information, or an error message.
    """
    updated_user = update_user(db, user_id, user.email, user.username)
    if updated_user:
        return {"username": updated_user.username, "email": updated_user.email}
    else:
        return {"error": "User not found"}, 404

@router.delete("/users/{user_id}")
def delete_user_route(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Delete a user by their ID.

    Args:
        request (Request): The incoming request.
        user_id (int): The ID of the user to delete.
        db (Session): The database session.

    Returns:
        RedirectResponse: Redirects to the URL of the page with users list.
    """
    data = delete_user(db, user_id)
    user_not_found(data)
    return RedirectResponse(url=f'/users', status_code=200)
