import platform

from handler.state import StateHandler
from handler.user import LoginHandler, UserInfoHandler
import handler.apisix as apisix

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from argparse import ArgumentParser
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from config.env import env

try:
    import sentry_sdk as sentry
except ImportError:
    sentry = None

routes = [
    (r"/apisix_admin/v1/state", StateHandler),
    (r"/apisix_admin/v1/organization/user/login", LoginHandler),
    (r"/apisix_admin/v1/organization/user/info", UserInfoHandler),
    (r"/apisix_admin/v1/apisix/route/list", apisix.RouteHandler),
    (r"/apisix_admin/v1/apisix/route/get", apisix.RouteHandler),
    (r"/apisix_admin/v1/apisix/route/create", apisix.RouteHandler),
    (r"/apisix_admin/v1/apisix/upstream/list", apisix.UpstreamHandler),
]

if __name__ == "__main__":
    [print(i[0]) for i in routes]

    parser = ArgumentParser()
    parser.add_argument("--port", default=9913, type=int, help="listen port")
    parser.add_argument("--numprocs", default=0, type=int, help="number of sub-process to fork")
    options, _ = parser.parse_known_args()

    app = Application(routes, **env["tornado"])
    server = HTTPServer(app, xheaders=True)

    port = options.port or env["port"]
    num_procs = options.numprocs or env["numprocs"]

    if env["tornado"]["debug"]:
        print('server.listen({})'.format(port))
        server.listen(port)
    else:
        print('server.listen({})'.format(port))
        server.bind(port)
        server.start(num_procs)
    IOLoop.current().start()
