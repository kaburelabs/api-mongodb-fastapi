from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends, Request, status

from config.hashing import Hash
from typing import Optional, List

from pymongo import MongoClient
from bson import ObjectId
import datetime
from decouple import config

from config.oauth import get_current_user
from config.jwttoken import create_access_token

from schemas import schema

client = MongoClient(config("DB_URL"))
DB_NAME = config("DATABASE_NAME")
db = client[DB_NAME]

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_post", response_model=schema.coursesCreation)
def creating_product_post(
    post: schema.coursesCreation, current_user: schema.User = Depends(get_current_user)
):

    posts_conn = db["posts"]

    if current_user.username:

        time_now = datetime.datetime.now()
        user_conn = db["users"].find_one({"username": current_user.username})
        request_object = dict(post)
        request_object.update(
            {
                "Author": f"{user_conn['first_name']} {user_conn['last_name']}",
                "username": user_conn["username"],
                "created_at": time_now,
                "last_modification": time_now,
            }
        )

        new_post = posts_conn.insert_one(request_object)

        return posts_conn.find_one({"_id": new_post.inserted_id})
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED(
                detail="User not Authenticated. Please log first."
            )
        )


def parse_mongo(result_list):
    def convert_mongo_id(product_dict):
        product_dict["id"] = str(product_dict["_id"])
        return product_dict

    return [convert_mongo_id(product) for product in result_list]


@app.get("/posts", response_model=List[schema.coursesCreationDisplay])
def get_all_posts():
    posts_conn = db["posts"]
    time_now = datetime.datetime.now()
    posts = posts_conn.find({})

    return parse_mongo(posts)


@app.get("/posts/my", response_model=List[schema.coursesCreationDisplay])
def get_my_posts(current_user: schema.User = Depends(get_current_user)):

    if current_user.username:
        user_conn = db["posts"].find({"username": current_user.username})

    return parse_mongo(user_conn)


@app.delete("/posts/{id}")
def creating_product_post(id: str):

    posts_conn = db["posts"]
    post = posts_conn.delete_one({"_id": ObjectId(id)})

    return {"status": f"post deleted {id}"}


@app.post("/register", response_model=schema.UserDisplay)
def create_user(request: schema.UserRegister):

    user = db["users"].find_one({"username": request.username})

    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This email is used already in use.",
        )
    else:
        hashed_pass = Hash.bcrypt(request.password)
        user_object = dict(request)

        # user_object["id"] = request.username
        user_object["password"] = hashed_pass
        user_object["register_date"] = datetime.datetime.now()
        user_id = db["users"].insert_one(user_object)
        new_user = db["users"].find_one({"_id": user_id.inserted_id})

        return new_user


@app.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):

    user = db["users"].find_one({"username": request.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="username or password aren't correct.",
        )
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="username or password aren't correct.",
        )

    access_token = create_access_token(data={"sub": user["username"]})

    return {"access_token": access_token, "token_type": "bearer"}


@app.put("/update/me", response_model=schema.UserDisplay)
def update_user(
    new_user_data: schema.UpdateUserModel,
    current_user: schema.User = Depends(get_current_user),
):

    if current_user.username:

        values_to_change = {}
        for (k, v) in new_user_data.dict().items():

            user_conn = db["users"]

            if v is not None:
                values_to_change.update({k: v})

        new_values = {"$set": values_to_change}
        query = {"username": current_user.username}

        user_conn.update_one(query, new_values)

        user = db["users"].find_one({"username": current_user.username})

        return user


@app.put("/update/product", response_model=schema.UserDisplay)
def update_product(
    new_user_data: schema.UpdateUserModel,
    current_user: schema.User = Depends(get_current_user),
):
    user_conn = db["users"]

    if current_user.username:

        for (k, v) in new_user_data.dict().items():

            values_to_change = {}
            if v is not None:
                values_to_change[k] = v

        new_values = {"$set": values_to_change}
        query = {"username": current_user.username}

        user_conn.update_one(query, new_values)

        user = user_conn.find_one({"username": current_user.username})

        return user
