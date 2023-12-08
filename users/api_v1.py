from django.db.models import Q
from ninja_extra import api_controller, http_delete, http_get, http_patch, http_post

from .models import User
from .schemas import (
    DeleteUserSchema,
    ErrorSchema,
    SignUpPasswordSchema,
    UpdateUserSchema,
    UserSchema,
)


@api_controller("users", tags=["User"])
class UserController:
    auto_import = False

    @http_post(
        "",
        response={201: UserSchema, 400: ErrorSchema},
        url_name="signup_user_password",
        auth=None,
    )
    def signup_user_password(self, signup_params: SignUpPasswordSchema):
        if User.objects.filter(
            Q(username=signup_params.username) | Q(email=signup_params.email)
        ).exists():
            return 400, ErrorSchema(message="User already exists")
        user = User.objects.create_user(
            username=signup_params.username,
            email=signup_params.email,
            password=signup_params.password1,
        )
        return 201, UserSchema.from_orm(user)

    @http_get("/me", response={200: UserSchema, 400: ErrorSchema}, url_name="get_user")
    def get_user(self):
        return 200, self.context.request.auth

    @http_patch(
        "/me", response={200: UserSchema, 304: ErrorSchema}, url_name="update_user"
    )
    def update_user(self, update_params: UpdateUserSchema):
        user = self.context.request.user
        for field, value in update_params.dict().items():
            if value:
                setattr(user, field, value)
        try:
            user.save()
        except ValueError:
            return 304, ErrorSchema(message="User failed to save")
        return 200, user

    @http_delete(
        "/me",
        response={202: UserSchema, 304: ErrorSchema, 400: ErrorSchema},
        url_name="delete_user",
    )
    def delete_user(self, delete_params: DeleteUserSchema):
        user = self.context.request.user
        if delete_params.username == user.username and user.check_password(
            delete_params.password.get_secret_value()
        ):
            user.is_active = False
            try:
                user.save()
            except ValueError:
                return 304, ErrorSchema(message="Failed to delete user")
            return 202, UserSchema.from_orm(user)
        return 400, ErrorSchema(message="Username or Password does not match")
