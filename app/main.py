from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

my_posts = [{"id" : 1, "title" : "title of post 1", "content" : "content of post 1"},
            {"id" : 2, "title" : "Favorite food", "content" : "Pizza"}]

@app.get("/")
def main():
    return {"message" : "Welcome to my api!"}

@app.get("/posts")
def get_posts():
    return {"data" :  my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randint(0, 100000000)
    my_posts.append(post_dict)
    return {"data": post}

def find_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i, post

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    _, post = find_post(id)
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error" : f"post with {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    i, _ = find_post(id)
    my_posts.pop(i)
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with {id} was not found")

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    i, target = find_post(id)
    post = post.model_dump()
    post['id'] = target['id']
    print(post)
    my_posts[i] = post

    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with {id} was not found")
    
    return {"data": post}