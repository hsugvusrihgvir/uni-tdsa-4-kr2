from uuid import UUID
import re
from pydantic import BaseModel, conint, EmailStr, field_validator

# Task 3.1
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: conint(gt=0) | None = None
    is_subscribed: bool = False


# Task 3.2
class ProductResponse(BaseModel):
    product_id: int
    name: str
    category: str
    price: float

# Задание 5.1
class LoginUserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr



# Task 5.5
A = re.compile(
    r"^[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=\d(\.\d)?)?(,\s*[a-zA-Z]{2}(-[a-zA-Z]{2})?(;q=\d(\.\d)?)?)*$"
)


class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, value: str) -> str:
        if not A.fullmatch(value):
            raise ValueError("Invalid Accept-Language format")
        return value