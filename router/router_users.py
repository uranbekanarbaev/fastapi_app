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
from db.schemas import UserResponse
from sqlalchemy.orm import Session 
from fastapi import HTTPException, status  
from auth.jwt_gen import create_access_token
from loggs.logger import logger
from fastapi import Cookie

router = APIRouter()

templates = Jinja2Templates(directory="/home/uranbekanarbaev/framework_project/templates")

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
    return data

@router.post("/users")
def users_post(
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Create a new user or authenticate an existing user.

    Args:
        response (Response): The response object.
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        db (Session): The database session.

    Returns:
        JSONResponse: A response containing a message, access token, and user data.
    """
    user = get_user_by_username(db, username)

    if user:
        # Authenticate if user exists
        authenticated_user = authenticate_user(db, username, password)
        if not authenticated_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    else:
        # Register if user doesn't exist
        try:
            user = create_user(db, username, password, email)
        except Exception as e:
            logger.error(f"User creation failed: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed")

    # Generate access token
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f'Access token value while posting user is {access_token}')

    # Use JSONResponse directly to set the cookie in the same response
    response = JSONResponse(content={
            "message": "Cookie set",
            "token": access_token,
            "user_data": UserResponse.from_orm(user).dict()
        })
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Protects the cookie
        samesite="Lax",
        secure=False  # Set True if using HTTPS
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
    user_id: int,
    db: Session = Depends(get_db),
    username: str = Form(...),
    email: str = Form(...),
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
    updated_user = update_user(db, user_id, email, username)
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
        RedirectResponse: Redirects to the URL of the deleted user.
    """
    delete_user(db, user_id)
    return RedirectResponse(url=f'/users/{user_id}', status_code=200)
