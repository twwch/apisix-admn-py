import re
import json
import traceback
from datetime import datetime
from tornado.web import RequestHandler, RedirectHandler
from .vo import to_json_type
from .const import *
from config.log import logger, rlogger

try:
    import sentry_sdk as sentry
except ImportError:
    sentry = None

XML_CPL = re.compile(r"text/xml.*")
JSON_CPL = re.compile(r"application/json.*")


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_default_headers(self):
        if 'Origin' in self.request.headers:
            origin = self.request.headers['Origin']
            self.set_header("Access-Control-Allow-Origin", origin)
            self.set_header("Access-Control-Allow-Headers", "x-requested-with, xiaoduo-platform")
            self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.set_header('Access-Control-Allow-Credentials', "true")

    def prepare(self):
        super().prepare()

        logger.debug(
            "request: {}".format(
                (
                    self.request.method,
                    self.request.path,
                    self.request.arguments,
                    self.request.headers,
                )
            )
        )

        for h in ("Accept", "Accept-Language", "User-Agent"):
            v = self.get_argument("_".join([""] + h.split("-")).lower(), None)
            if v is not None:
                self.request.headers[h] = v

        accept = self.request.headers.get("Accept", "application/json")
        if XML_CPL.match(accept):
            self.response_type = "xml"
        elif JSON_CPL.match(accept):
            self.response_type = "json"
        else:
            self.response_type = "html"
        self.code, self.message = CODE_UNDEFINED, None

    def response_json(
            self, code=CODE_OK, message=None, status_code=200, **kwargs):
        self.code, self.message = code, message
        message = message or MESSAGES.get(code, "")
        data = {
            "code": code,
            "message": (message if isinstance(message, str) else json.dumps(message)),
        }
        data.update(kwargs)

        self.set_status(status_code)
        ua = self.request.headers.get('User-Agent', "")
        if re.match(r".+\s+MSIE\s+.+", ua):
            self.set_header("Content-Type", "text/html; charset=utf-8")
        else:
            self.set_header("Content-Type", "application/json; charset=utf-8")
        self.finish(json.dumps(
            to_json_type(data),
            ensure_ascii=False))
        logger.debug('(test){}'.format(json.dumps(to_json_type(data), ensure_ascii=False)))

    def response_html(
            self, template, code=CODE_OK, message=None, status_code=200, **kwargs
    ):
        self.code, self.message = code, message

        message = message or ""
        data = {
            "code": code,
            "message": (message if isinstance(message, str) else json.dumps(message)),
        }
        data.update(kwargs)

        self.set_status(status_code)
        self.set_header("Content-Type", "text/html; charset=utf-8")
        self.render(template, **data)

    def response(
            self,
            content,
            content_type_header="text/plain; charset=utf-8",
            code=CODE_OK,
            message=None,
            status_code=200,
    ):
        self.code, self.message = code, message

        self.set_status(status_code)
        self.set_header("Content-Type", content_type_header)
        self.finish(content)

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            logger.error(traceback.format_exception(*kwargs["exc_info"]))
            if sentry:
                sentry.capture_exception(kwargs["exc_info"][1])
            message = ""
        else:
            message = self._reason

        return self.response_json(CODE_SYSTEM_ERROR, message)

    def on_finish(self):
        request_method = self.request.method
        request_path = self.request.path
        _info = {
            "request_time": datetime.utcnow(),
            "time_served": self.request.request_time(),
            "http_user_agent": self.request.headers.get("User-Agent", ""),
            "remote_ip": self.request.remote_ip,
            "arguments": {
                k.translate({ord("."): "_", ord("'"): "_", ord('"'): "_"}): v[0].decode(
                    errors="replace"
                )
                for k, v in self.request.arguments.items()
            },
            "code": self.code,
        }
        rlogger.info(
            "{} {} {}".format(
                request_method,
                request_path,
                json.dumps(to_json_type(_info), ensure_ascii=False),
            )
        )
