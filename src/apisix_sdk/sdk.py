import time

import requests

from config.env import env


class ApiSixSdk(object):
    def __init__(self):
        self.headers = {
            "X-API-KEY": env.get("apisix_auth_key"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.host = env.get("apisix_host")
        self.route_url = "/apisix/admin/routes"
        self.upstream_url = "/apisix/admin/upstreams"

    def __get_req_data(self, data: dict):
        temp = dict()
        for key, value in data.items():
            if value:
                temp.update({key: value})
        return temp

    def request_data(self, url, method, data=None):
        retry = 3
        while retry > 0:
            rsp = requests.request(method=method, url=url, json=data, headres=self.headers)
            if rsp.status_code == 200:
                resp = rsp.json()
                return resp
            retry = retry - 1
            time.sleep(1)
        return {}

    def route_list(self):
        return self.request_data(url=self.route_url, method="GET")

    def get_route(self, id):
        url = "{}/{}".format(self.route_url, id)
        return self.request_data(url=url, method="GET")

    def route_create(self, id, data: dict):
        data.update({"upstream_id": id})
        temp = self.__get_req_data(data)
        url = "{}/{}".format(self.route_url, id)
        return self.request_data(url, method="PUT", data=temp)

    def upstream_list(self):
        return self.request_data(url=self.upstream_url, method="GET")

    def get_upstream(self, id):
        url = "{}/{}".format(self.upstream_url, id)
        return self.request_data(url=url, method="GET")

    def upstream_create(self, id, data: dict):
        upstream_type = "roundrobin"
        data.update({"type": upstream_type})
        temp = self.__get_req_data(data)
        url = "{}/{}".format(self.upstream_url, id)
        return self.request_data(url, method="PUT", data=temp)

    def upstream_delete(self, id):
        url = "{}/{}".format(self.upstream_url, id)
        return self.request_data(url, method="DELETE")
