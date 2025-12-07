from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.helpers.database import engine, Base
from app.routers import users
from app.helpers.exceptionHandler import (
    http_exception_handler,
    validation_exception_handler,
    value_error_handler,
    global_exception_handler
)

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)


app.include_router(users.router,prefix="/api/v1")



@app.get("/")
def read_root():
    return {"Hello": "World"}