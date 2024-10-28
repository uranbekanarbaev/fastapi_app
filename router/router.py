from fastapi.routing import APIRouter
from fastapi import Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from db.crud import authenticate_user, get_all_users, get_user_by_username, create_user
from auth.jwt_gen import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db.deps import get_db
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
    return templates.TemplateResponse('index.html', {"request": request, "data": data})

@router.get("/users/{user_id}")
def users(request: Request, user_id: int, db: Session = Depends(get_db)):
    data = get_user_by_username(db, user_id)
    return data

@router.post("/users")
def users(
    request: Request,
    response: Response,
    username: str = Form(...),
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
            user = create_user(db, username, password)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed")

    # Generate access token
    access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=False,
        samesite="None",
        secure=False,
        path="/"  # Makes the cookie accessible throughout the domain
    )
    logger.info(f"Response headers after setting cookie: {response.headers}")
    logger.info(f"Token set successfully: {access_token}")

    return RedirectResponse(url="/tasks", status_code=status.HTTP_302_FOUND)

@router.get("/read-cookie")
def read_cookie(some_data: str = Cookie("access_token")):
    if some_data is None:
        raise HTTPException(status_code=400, detail="Cookie 'some_data_in_cookies' not found")
    return {"some_data_in_cookies": some_data}

@router.get("/debug-cookie")
async def debug_cookie(request: Request):
    cookies = request.cookies
    logger.info(f"All cookies in request: {cookies}")
    token = cookies.get("access_token")
    return {"token": token if token else "Token cookie not found"}

@router.put("/users", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@router.delete("/users", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@router.get("/tasks")
async def tasks(request: Request, token: str = Cookie(None)):
    logger.info(f"Cookies received in request: {request.cookies}")
    logger.info(f"Token received in get_current_user: {token}")
    if not token:
        return {"error": "Token not found"}
    # Proceed with normal token processing

@router.get("/tasks/{task_id}", response_class=HTMLResponse)
def users(request: Request, user_id: int):
    return templates.TemplateResponse('index.html', {"request": request})

@router.post("/tasks", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@router.put("/tasks", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@router.delete("/tasks", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


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