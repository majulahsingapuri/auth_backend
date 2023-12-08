from typing import Optional

from ninja import Field, Schema
from pydantic import EmailStr, SecretStr


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


class UpdateUserSchema(Schema):
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")


class DeleteUserSchema(Schema):
    username: str
    password: SecretStr
