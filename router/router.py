from fastapi.routing import APIRouter
from fastapi import Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from db.crud import authenticate_user, get_all_users, get_user_by_username, create_user, get_tasks_by_user, create_task, get_user_by_user_id, update_user, delete_user, get_task_by_id, update_task, delete_task
from auth.jwt_gen import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db.database import get_db
from db.schemas import UserCreate, TaskCreate, UserResponse
from sqlalchemy.orm import Session 
from fastapi import HTTPException, status  
from auth.user_auth import get_current_user
from auth.jwt_gen import create_access_token, pwd_context
from db.models import User
from loggs.logger import logger
from fastapi import Cookie

router = APIRouter()

templates = Jinja2Templates(directory="/home/uranbekanarbaev/framework_project/templates")

@router.get("/users", response_class=HTMLResponse)
def users(request: Request, db: Session = Depends(get_db)):
    data = get_all_users(db)
    logger.info(f'data available {data}')
    return templates.TemplateResponse(request, 'index.html', {"data": data})

@router.get("/users/{user_id}")
def users(request: Request, user_id: int, db: Session = Depends(get_db)):
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
            "user_data": UserResponse.from_orm(user).dict()  # Serialize the user data
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
    if access_token is None:
        logger.warning("Cookie 'access_token' not found in request headers")
        raise HTTPException(status_code=400, detail="Cookie 'access_token' not found")
    return {"access_token_in_cookies": access_token}

@router.get("/debug-cookie")
async def debug_cookie(request: Request):
    cookies = request.cookies
    logger.info(f"All cookies in request: {cookies}")
    token = cookies.get("access_token")
    return {"token": token if token else "Token cookie not found"}

@router.post("/set-cookies")
async def set_cookies(request: Request, response: Response):
    response.set_cookie(key="fakesession123", value="fake123-cookie-session-value")

@router.put("/users/{user_id}")
def update_user_route(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    username: str = Form(...),
    email: str = Form(...),
):
    updated_user = update_user(db, user_id, email, username)
    if updated_user:
        return {"username": updated_user.username, "email": updated_user.email}
    else:
        return {"error": "User not found"}, 404

@router.delete("/users/{user_id}")
def users(request: Request, user_id: int, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return RedirectResponse(url=f'/users/{user_id}', status_code=200)

@router.get("/tasks")
async def tasks(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = get_tasks_by_user(db, current_user.id)
    return templates.TemplateResponse(request, 'tasks.html', {"data": data})

@router.get("/tasks/{task_id}", response_class=HTMLResponse)
def users(request: Request, task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = get_task_by_id(db, current_user.id, task_id)
    return templates.TemplateResponse(request, 'tasks.html', {"data": data})

@router.post("/tasks")
def users(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    create_task(db, task.description, current_user.id)
    return {"message": "Task created successfully"}

@router.put("/tasks/{task_id}")
def users(request: Request, task_id: int, name: str = Form(...), description: str = Form(...), status: bool = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    update_task(db, current_user.id, task_id, name, description, status)
    return RedirectResponse(url='/tasks', status_code=303)

@router.delete("/tasks/{task_id}")
def users(request: Request, task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_task(db, current_user.id, task_id)
    return RedirectResponse(url='/tasks', status_code=303)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}