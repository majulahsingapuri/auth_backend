from django.conf import settings
from django.http import HttpResponse
from ninja_extra import api_controller, http_post
from ninja_jwt.controller import TokenObtainPairController, TokenVerificationController
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings

schema = SchemaControl(api_settings)


@api_controller("token", tags=["Auth"])
class AuthTokenController(TokenObtainPairController, TokenVerificationController):
    auto_import = False

    @http_post(
        "/pair",
        response=schema.obtain_pair_schema.get_response_schema(),
        url_name="token_obtain_pair",
        auth=None,
    )
    def obtain_token(
        self, user_token: schema.obtain_pair_schema, response: HttpResponse
    ):
        user_token.check_user_authentication_rule()
        res = user_token.to_response_schema()
        response.set_cookie(
            key="access",
            value=res.access,
            domain=settings.SESSION_COOKIE_DOMAIN[1:],
            secure=False,
        )
        response.set_cookie(
            key="refresh",
            value=res.refresh,
            domain=settings.SESSION_COOKIE_DOMAIN[1:],
            secure=False,
        )
        return res

    @http_post(
        "/refresh",
        response=schema.obtain_pair_refresh_schema.get_response_schema(),
        url_name="token_refresh",
        auth=None,
    )
    def refresh_token(
        self, refresh_token: schema.obtain_pair_refresh_schema, response: HttpResponse
    ):
        res = refresh_token.to_response_schema()
        response.set_cookie(
            key="access",
            value=res.access,
            domain=settings.SESSION_COOKIE_DOMAIN[1:],
            secure=False,
        )
        response.set_cookie(
            key="refresh",
            value=res.refresh,
            domain=settings.SESSION_COOKIE_DOMAIN[1:],
            secure=False,
        )
        return res

    @http_post(
        "/logout",
        response=schema.blacklist_schema.get_response_schema(),
        url_name="token_logout",
    )
    def logout_token(self, tokens: schema.blacklist_schema, response: HttpResponse):
        res = tokens.to_response_schema()
        response.delete_cookie("access", domain=settings.SESSION_COOKIE_DOMAIN[1:])
        response.delete_cookie("refresh", domain=settings.SESSION_COOKIE_DOMAIN[1:])
        return res
