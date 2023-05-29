from fastapi import FastAPI


from .routers import users, auth

# Application instance
app = FastAPI()


# Routers
app.include_router(users.router)
app.include_router(auth.router)

# default endpoint
@app.get('/')
def root():
    return {'msg': 'root'}