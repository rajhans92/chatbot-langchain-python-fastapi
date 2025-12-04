from fastapi import FastAPI
from app.helpers.database import engine, Base
from app.routers import users

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(users.router)



@app.get("/")
def read_root():
    return {"Hello": "World"}