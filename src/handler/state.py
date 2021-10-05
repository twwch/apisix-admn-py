from common.const import CODE_OK
from common.handler import BaseHandler


class StateHandler(BaseHandler):
    def get(self):
        return self.response_json(CODE_OK, data="service is ok")
