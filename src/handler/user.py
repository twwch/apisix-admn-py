import json

from common.auth import authenticated
from common.const import CODE_SYSTEM_ERROR
from common.handler import BaseHandler
from services.user import login, user_info


class LoginHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            code, res = login(data.get("account"), data.get("password"))
            return self.response_json(code, data=res)
        except Exception as e:
            return self.response_json(CODE_SYSTEM_ERROR, msg=e)


class UserInfoHandler(BaseHandler):
    @authenticated()
    def get(self):
        try:
            token = self.request.headers.get("Token")
            code, res = user_info(token)
            return self.response_json(code, data=res)
        except Exception as e:
            return self.response_json(CODE_SYSTEM_ERROR, msg=e)
