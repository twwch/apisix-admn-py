import json
import traceback

from common.const import CODE_SYSTEM_ERROR
from common.handler import BaseHandler
from config.log import logger
from services.apisix import *

class RouteHandler(BaseHandler):
    def get(self):
        try:
            data = json.loads(self.request.arguments)
            code, data = route_list_or_get(data)
            return self.response_json(code, data=data)
        except:
            logger.error("RouteHandler get has err: {}".format(traceback.format_exc()))
            return self.response_json(CODE_SYSTEM_ERROR)

    def post(self):
        try:
            data = json.loads(self.request.body)
            code, data = route_create(data)
            return self.response_json(code, data=data)
        except:
            logger.error("RouteHandler post has err: {}".format(traceback.format_exc()))
            return self.response_json(CODE_SYSTEM_ERROR)


class UpstreamHandler(BaseHandler):
    def get(self):
        try:
            code, data = upstream_list()
            return self.response_json(code, data=data)
        except:
            logger.error("UpstreamHandler get has err: {}".format(traceback.format_exc()))
            return self.response_json(CODE_SYSTEM_ERROR)
