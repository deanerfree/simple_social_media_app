# To get the app started setup the virtual environment source venv/bin/activate
#  To start the server uvicorn app.main:app --reload

# from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import psycopg2

# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import mode
from . import models
from .db import engine
from .routers import post, users, auth, vote


# models.Base.metadata.create_all(bind=engine)

origins = [
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# used to run raw SQL
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected")
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print("Error: ", error)
#         time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Welcome"}

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
