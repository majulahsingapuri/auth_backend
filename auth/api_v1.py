from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth

from auth_token.api_v1 import AuthTokenController
from users.api_v1 import UserController

api = NinjaExtraAPI(auth=JWTAuth(), csrf=True)
api.register_controllers(AuthTokenController)
api.register_controllers(UserController)
