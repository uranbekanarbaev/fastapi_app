from fastapi import FastAPI
from fastapi.routing import APIRouter
from router.router import router

app = FastAPI()

app.include_router(router)

