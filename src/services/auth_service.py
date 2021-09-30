from http import HTTPStatus

from src.models.user import User
from src.services.user_service import UserService


class AuthService:
    @staticmethod
    def login_user(login_request):
        try:
            user: User = UserService.get_user_by_username(login_request["username"])
            if user is None or not user.check_password(login_request["password"]):
                return {
                    "message": "Username or password is not valid"
                }, HTTPStatus.FORBIDDEN

            return user.generate_access_token(), HTTPStatus.OK

        except:
            return {
                "message": "Something went wrong. Pleas try again"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
