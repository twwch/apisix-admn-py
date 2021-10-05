import time

from apisix_sdk.sdk import ApiSixSdk
from common.const import CODE_OK, CODE_SYSTEM_ERROR, CODE_CREATE_UPSTREAM_ERROR, CODE_CREATE_ROUTE_ERROR

apisix_sdk = ApiSixSdk()


def route_list_or_get(data: dict):
    id = data.get("id")
    if not id:
        routes = apisix_sdk.route_list()
        if routes:
            return CODE_OK, routes
        return CODE_SYSTEM_ERROR, None
    route = apisix_sdk.get_route(id)
    upstream = apisix_sdk.get_upstream(id)
    if route and upstream:
        resp = {
            "route": route,
            "upstream": upstream,
            "nodes": list()
        }
        return CODE_OK, resp
    else:
        return CODE_SYSTEM_ERROR, None


def route_create(data: dict):
    route = data.get("route")
    upstream = data.get("upstream")
    id = str(int(time.time()))
    create_upstream = apisix_sdk.route_create(id, upstream)
    if not create_upstream:
        return CODE_CREATE_UPSTREAM_ERROR, None
    create_route = apisix_sdk.route_create(id, route)
    if not create_route:
        apisix_sdk.upstream_delete(id)
        return CODE_CREATE_ROUTE_ERROR, None
    return CODE_OK, None


def upstream_list():
    upstreams = apisix_sdk.get_upstream(id)
    if upstreams:
        return CODE_OK, upstreams
    return CODE_SYSTEM_ERROR, None
