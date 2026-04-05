from fastapi import FastAPI, HTTPException, Query, status, Response, Cookie,  Header

from models import UserCreate, ProductResponse
from models import LoginUserRequest, UserResponse

from uuid import UUID

from db import ProductsStorage
from db import UsersStorage

from itsdangerous import URLSafeSerializer, BadSignature
import time

from typing import Annotated
from models import CommonHeaders
from datetime import datetime

app = FastAPI()
ps = ProductsStorage()
us = UsersStorage()
SECRET_KEY = "cRgNManhynSh"
serializer = URLSafeSerializer(SECRET_KEY)

# Task 3.1
@app.post("/create_user",  response_model=UserCreate)
async def create_user(user: UserCreate):
    return user


# Task 3.2

@app.get("/products/search",  response_model=list[ProductResponse])
async def search_products(keyword: str = Query(...), category: str | None = Query(None), limit: int = Query(10, gt=0)):
    products = ps.search_products(keyword, category, limit)
    return products


@app.get("/product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    product = ps.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Task 5.1
@app.post("/login")
def login(user: LoginUserRequest, response: Response):
    user_data = us.check_user(user.username, user.password)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    session = str(us.create_session(user_data["user_id"]))
    response.set_cookie(key="session_token",
                        value=session,
                        httponly=True) # только для HTTP
    return {"message": "Login successful"}

@app.get("/user", response_model=UserResponse)
def get_user(session_token: UUID | None = Cookie(default=None)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = us.get_user(session_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return UserResponse(user_id=user["user_id"],
                        username=user["username"],
                        email=user["email"])

# Task 5.2 - 5.3
@app.post("/login2")
def login2(user:LoginUserRequest, response: Response):
    user_data = us.check_user(user.username, user.password)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user_id = str(user_data["user_id"])

    payload = {
        "user_id": user_id,
        "ts": int(time.time())
    }
    session_token = serializer.dumps(payload)

    response.set_cookie(key="session_token",
                        value=session_token,
                        httponly=True,
                        max_age=300,
                        secure=False)
    return {"message": "Login successful"}

@app.get("/profile2", response_model=UserResponse)
def profile2(response:Response, session_token: str | None = Cookie(default=None)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        data = serializer.loads(session_token)
    except BadSignature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    user_id = data["user_id"]
    user = us.get_user_by_id(UUID(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    last_ts = data["ts"]
    now = int(time.time())
    delta = now - last_ts

    if delta >= 300:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    if 180 <= delta < 300:
        payload = {
            "user_id": user_id,
            "ts": int(time.time())
        }
        session_token = serializer.dumps(payload)

        response.set_cookie(key="session_token",
                            value=session_token,
                            httponly=True,
                            max_age=300,
                            secure=False)

    return UserResponse(
        user_id=user["user_id"],
        username=user["username"],
        email=user["email"]
    )

# Task 5.4
@app.get("/headers")
def get_headers(user_agent: str | None = Header(default=None),
                accept_language: str | None = Header(default=None)):
    if not user_agent:
        raise HTTPException(status_code=400, detail="User-Agent header is required")

    if not accept_language:
        raise HTTPException(status_code=400, detail="Accept-Language header is required")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }

# Task 5.5
@app.get("/headers2")
def get_headers2(headers: Annotated[CommonHeaders, Header()]):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }


@app.get("/info2")
def get_info2(response: Response, headers: Annotated[CommonHeaders, Header()]):
    response.headers["X-Server-Time"] = datetime.now().isoformat()

    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }