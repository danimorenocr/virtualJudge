from fastapi import FastAPI
from .database import Base, engine
from .routers import problems, submissions

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(problems.router)
app.include_router(submissions.router)
