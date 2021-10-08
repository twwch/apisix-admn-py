import time

from apisix_sdk.sdk import ApiSixSdk
from common.const import CODE_OK, CODE_SYSTEM_ERROR, CODE_CREATE_UPSTREAM_ERROR, CODE_CREATE_ROUTE_ERROR

apisix_sdk = ApiSixSdk()


def route_list_or_get(data: dict):
    id = data.get("id")
    if not id:
        routes = apisix_sdk.route_list()
        if routes:
            data = {
                "routes": routes,
                "total": len(routes)
            }
            return CODE_OK, data
        return CODE_SYSTEM_ERROR, None
    route = apisix_sdk.get_route(id)
    upstream = apisix_sdk.get_upstream(id)
    if route and upstream:
        nodes = upstream.get("value", {}).get("nodes") or {}
        resp = {
            "route": route.get("value", {}),
            "upstream": upstream.get("value", {}),
            "nodes": [{"node_key": key, "node_value": value} for key, value in nodes.items()]
        }
        return CODE_OK, resp
    else:
        return CODE_SYSTEM_ERROR, None


def route_create(data: dict):
    route = data.get("route")
    upstream = data.get("upstream")
    id = str(int(time.time()))
    if data.get("id"):
        id = data.get("id")
    if upstream.get("name"):
        del upstream["name"]
    create_upstream = apisix_sdk.upstream_create(id, upstream)
    if not create_upstream:
        return CODE_CREATE_UPSTREAM_ERROR, None
    create_route = apisix_sdk.route_create(id, route)
    if not create_route:
        apisix_sdk.upstream_delete(id)
        return CODE_CREATE_ROUTE_ERROR, None
    return CODE_OK, None


def upstream_list():
    upstreams = apisix_sdk.upstream_list()
    if upstreams:
        data = {
            "upstreams": upstreams,
            "total": len(upstreams)
        }
        return CODE_OK, data
    return CODE_SYSTEM_ERROR, None
