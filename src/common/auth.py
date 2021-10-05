import functools

from common.const import CODE_NOT_LOGINED, CODE_NOT_AUTH
from utils.jwt_util import check_token


def authenticated():
    def _authenticated(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.get_current_user():
                token = self.request.headers.get("Token")
                if not token:
                    return self.response_json(CODE_NOT_AUTH)
                ok, msg, _ = check_token(token)
                if not ok:
                    return self.response_json(CODE_NOT_LOGINED, msg)
            return method(self, *args, **kwargs)

        return wrapper

    return _authenticated
