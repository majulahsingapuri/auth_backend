from dj_ninja_auth.jwt.authentication import JWTAuth
from dj_ninja_auth.jwt.controller import NinjaAuthJWTController
from ninja_extra import NinjaExtraAPI

from csrf.api_v1 import router as csrf_router
from users.api_v1 import UserController

api = NinjaExtraAPI(auth=[JWTAuth()], csrf=True)
api.register_controllers(NinjaAuthJWTController)
api.register_controllers(UserController)
api.add_router("/", csrf_router, tags=["CSRF"])
