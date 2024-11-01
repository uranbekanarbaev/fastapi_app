from fastapi import FastAPI
from router.router_users import router as router_users
from router.router_tasks import router as router_tasks

app = FastAPI()

app.include_router(router_users)
app.include_router(router_tasks)