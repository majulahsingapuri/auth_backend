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
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            email=user.email,
            username=user.username,
            firstName=user.first_name,
            lastName=user.last_name,
        )


class UpdateUserSchema(Schema):
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")


class DeleteUserSchema(Schema):
    username: str
    password: str
