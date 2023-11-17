from typing import Optional

from ninja import Schema
from pydantic import EmailStr, Field

from .models import User


class SignUpPasswordSchema(Schema):
    email: EmailStr
    username: str
    password1: str
    password2: str


class ErrorSchema(Schema):
    message: str


class UserSchema(Schema):
    email: EmailStr
    username: str
    firstName: str = Field(alias="first_name")
    lastName: str = Field(alias="last_name")

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )


class UpdateUserSchema(Schema):
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")


class DeleteUserSchema(Schema):
    username: str
    password: str
