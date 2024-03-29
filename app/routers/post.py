from fastapi import Response, status, HTTPException, Depends, APIRouter
from app.schemas import PostCreate, Post
from sqlalchemy.orm import Session
from app import models, oauth2
from app.database import get_db
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=['Posts'])


# instead of using /posts everywhere in the path, we can make this more comfrotable by just adding the path inside the
# APT router as a prefix and remove the /posts and just use /


# @router.get("/", response_model=List[Post])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.AllPosts).filter(models.AllPosts.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.AllPosts, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote,   models.Vote.post_id == models.AllPosts.id, isouter=True).group_by(models.AllPosts.id).filter(
        models.AllPosts.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title,
    #                                                                                                       post.content,
    #                                                                                                       post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 100000000)
    # my_posts.append(post_dict)
    # new_post = models.AllPosts(title=post.title, content=post.content, published=post.published)--
    # if we have 50 columns this is bit difficult to call all the columns in th table instead,
    # below is the efficient and easy method
    print(current_user.email)
    new_post = models.AllPosts(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# getting specific post that's the reason we mentioned id in the url
# @router.get("/{id}", response_model=Post)
@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",  str(id))
    # post = cursor.fetchone()
    print(current_user)
    post = db.query(models.AllPosts, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote,   models.Vote.post_id == models.AllPosts.id, isouter=True).group_by(models.AllPosts.id).filter(
        models.AllPosts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    post_query = db.query(models.AllPosts).filter(models.AllPosts.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# this is the normal update using main.py coding
# @app.put("/posts/{id}")
# def update_posts(id: int, post: Post):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f 'post with id {id} does not exist')
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {'data': post_dict}c


# this is the update using postgres commands
@router.put("/{id}", response_model=Post)
def update_posts(id: int, post: PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title= %s, content= %s, published=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query_for_update = db.query(models.AllPosts).filter(models.AllPosts.id == id)
    updated_post = post_query_for_update.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} does not exist')
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")
    post_query_for_update.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query_for_update.first()
