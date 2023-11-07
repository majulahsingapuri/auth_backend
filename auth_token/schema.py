from typing import Dict, Type

import ninja_jwt.exceptions as exceptions
from ninja import Schema
from ninja_jwt.schema import InputSchemaMixin
from ninja_jwt.tokens import AccessToken, RefreshToken
from ninja_jwt.utils import token_error
from pydantic import root_validator


class AuthTokenBlacklistOutputSchema(Schema):
    success: bool


class AuthTokenBlacklistInputSchema(Schema, InputSchemaMixin):
    access: str
    refresh: str

    @root_validator
    @token_error
    def validate_schema(cls, values: Dict) -> dict:
        if not values.get("access"):
            raise exceptions.ValidationError({"access": "access token is required"})
        if not values.get("refresh"):
            raise exceptions.ValidationError({"refresh": "refresh token is required"})
        access = AccessToken(values["access"])
        refresh = RefreshToken(values["refresh"])
        try:
            access.blacklist()
            refresh.blacklist()
        except AttributeError:
            pass
        return values

    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return AuthTokenBlacklistOutputSchema

    def to_response_schema(self):
        return {"success": True}
