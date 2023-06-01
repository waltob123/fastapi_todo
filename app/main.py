from fastapi import FastAPI

from .routers import users, auth, tasks
from .database import get_db
from .utils import set_all_inactive_tasks_to_false


# Application instance
app = FastAPI()


# Routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)

# set all inactive tasks to false
set_all_inactive_tasks_to_false()

# default endpoint
@app.get('/')
def root():
    return {'msg': 'root'}
