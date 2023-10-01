from datetime import date
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Post
from settings import DATABASE_URL

# DISCLAIMER:
# This for my client Mushraf


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "client proeject"}


@app.post("/posts")
def create_post(title: str, pages: int):
    session = Session()
    post = Post(title=title, pages=pages, created_at=date.today())
    session.add(post)
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


@app.get("/posts/{id}")
def find_post(id: int):
    session = Session()
    post = session.query(Post).filter(Post.id == id).first()
    session.close()

    result = jsonable_encoder({"post": post})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


@app.get("/posts")
def get_post(page_size: int = 10, page: int = 1):
    if page_size > 100 or page_size < 0:
        page_size = 100

    session = Session()
    posts = session.query(Post).limit(page_size).offset((page - 1) * page_size).all()
    session.close()

    result = jsonable_encoder({"posts": posts})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


@app.put("/posts")
def update_post(id: int, title: Optional[str] = None, pages: Optional[int] = None):
    session = Session()
    post = session.query(Post).get(id)
    if title is not None:
        post.title = title
    if pages is not None:
        post.pages = pages
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


@app.delete("/posts")
def delete_post(id: int):
    session = Session()
    post = session.query(Post).get(id)
    session.delete(post)
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


@app.exception_handler(Exception)
def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(
        status_code=status_code,
        content={"status_code": status_code, "message": message},
    )
