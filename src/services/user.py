from common.const import CODE_USER_NOT_EXISTS, CODE_OK, CODE_TOKEN_ERROR, CODE_PASSWORD_ERROR, CODE_NOT_LOGINED, \
    CODE_TOKEN_GEN_ERROR
from models.user import UserModel
from utils.account import fill_login_name, get_sha_password
from utils.jwt_util import get_token, check_token


def get_user(account):
    account = fill_login_name(account)
    return dict(UserModel().find_one({"$or": [{"mobile": account}, {"email": account}], "active": True}))


def login(account, password):
    account = fill_login_name(account)
    user = get_user(account)
    if not user:
        return CODE_USER_NOT_EXISTS, None
    if get_sha_password(password) == user.get("password"):
        data = {
            "user_info": {
                "name": user.get("name"),
                "user_id": user.get("user_id"),
                "email": user.get("email"),
            }
        }
        token = get_token(data)
        if token:
            data.update({"token": token})
            return CODE_OK, data
        return CODE_TOKEN_GEN_ERROR, None
    return CODE_PASSWORD_ERROR, None


def user_info(token):
    if not token:
        return CODE_NOT_LOGINED, None
    ok, msg, data = check_token(token)
    if not ok:
        return CODE_TOKEN_ERROR, None
    return CODE_OK, data.get("custom", {}).get("user_info")