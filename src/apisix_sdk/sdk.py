import time

import requests

from config.log import logger


class ApiSixSdk(object):
    def __init__(self):
        self.headers = {
            "X-API-KEY": "edd1c9f034335f136f87ad84b625c8f1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
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
        url = "http://10.20.111.110:80/{}".format(url)
        while retry > 0:
            rsp = requests.request(method=method, url=url, json=data, headers=self.headers)
            rsp.encoding = rsp.apparent_encoding
            print(url, rsp.status_code, rsp, rsp.text)
            if rsp.status_code == 200:
                resp = rsp.json()
                return resp
            logger.error("request apisix error: {}: {}".format(url, rsp.text))
            retry = retry - 1
            time.sleep(1)
        return None

    def route_list(self):
        res = self.request_data(url=self.route_url, method="GET") or {}
        res = res.get("node") or {}
        if res:
            for item in res.get("nodes"):
                value = item.get("value") or {}
                keys = str(item.get("key")).split("/")
                id = keys[len(keys) - 1]
                value.update({"id": id})
        return res.get("nodes")

    def get_route(self, id):
        url = "{}/{}".format(self.route_url, id)
        res = self.request_data(url=url, method="GET") or {}
        return res.get("node", {})

    def route_create(self, id, data: dict):
        data.update({"upstream_id": id})
        temp = self.__get_req_data(data)
        url = "{}/{}".format(self.route_url, id)
        return self.request_data(url, method="PUT", data=temp)

    def upstream_list(self):
        res = self.request_data(url=self.upstream_url, method="GET") or {}
        res = res.get("node") or {}
        return res.get("nodes")

    def get_upstream(self, id):
        url = "{}/{}".format(self.upstream_url, id)
        res = self.request_data(url=url, method="GET") or {}
        return res.get("node", {})

    def upstream_create(self, id, data: dict):
        upstream_type = "roundrobin"
        data.update({"type": upstream_type})
        temp = self.__get_req_data(data)
        url = "{}/{}".format(self.upstream_url, id)
        return self.request_data(url, method="PUT", data=temp)

    def upstream_delete(self, id):
        url = "{}/{}".format(self.upstream_url, id)
        return self.request_data(url, method="DELETE")
