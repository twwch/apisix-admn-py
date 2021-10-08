import json
import traceback

from common.auth import authenticated
from common.handler import BaseHandler
from config.log import logger
from services.apisix import *

class RouteHandler(BaseHandler):
    @authenticated()
    def get(self):
        try:
            id = self.get_argument("id", "")
            data = {"id": id}
            code, data = route_list_or_get(data)
            return self.response_json(code, data=data)
        except:
            logger.error("RouteHandler get has err: {}".format(traceback.format_exc()))
            print("RouteHandler get has err: {}".format(traceback.format_exc()))
            return self.response_json(CODE_SYSTEM_ERROR, message=traceback.format_exc())

    @authenticated()
    def post(self):
        try:
            data = json.loads(self.request.body)
            code, data = route_create(data)
            return self.response_json(code, data=data)
        except:
            logger.error("RouteHandler post has err: {}".format(traceback.format_exc()))
            print("RouteHandler post has err: {}".format(traceback.format_exc()))
            return self.response_json(CODE_SYSTEM_ERROR)


class UpstreamHandler(BaseHandler):
    @authenticated()
    def get(self):
        try:
            code, data = upstream_list()
            return self.response_json(code, data=data)
        except:
            logger.error("UpstreamHandler get has err: {}".format(traceback.format_exc()))
            print("UpstreamHandler get has err: {}".format(traceback.format_exc()))
            return self.response_json(CODE_SYSTEM_ERROR)
