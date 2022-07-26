from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from app import models
from app.database import engine
from app.routers import post, user, auth, vote
from app.config import settings


print(settings.database_username)


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World, How are you? I am excited...."}


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Shalini!1',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print('Connection to database failed!')
#         print("Error: ", error)
#         time.sleep(2)

# my_posts = [{"title": "title1- the fish", "content": "there are so many species out of those, i like fish", "id": 1},
#             {"title": "title2- the dog", "content": "there are so many species out of those, i like dogs as well", "id":
#                 2}]

#
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#
#
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
