# -*- coding: utf-8 -*-
import sys
import json
import copy
import requests
from common.exception.mpc_sdk_exception import MPCSDKException
from common import signer
from mpc.response import BaseResponse


class BaseClient(object):
    def __init__(self, AK, SK, EndPoint, ProjectId):
        """BaseClient.

        :param AK: The access key id for signature.
        :type AK: str
        :param SK: The secret access key for signature.
        :type SK: str
        :param EndPoint: The entry of web service.
        :type EndPoint: str
        :param ProjectId: The project id owned by a user who has
                          successfully registered on the public cloud.
        :type ProjectId: str
        """
        if AK is None or AK == "":
            raise MPCSDKException(
                "InvalidAK", "The AK can not be None or invalid.")
        if SK is None or SK == "":
            raise MPCSDKException(
                "InvalidSK", "The SK can not be None or invalid.")
        if EndPoint is None or EndPoint == "":
            raise MPCSDKException(
                "InvalidEndPoint", "The EndPoint can not be None or invalid.")
        if ProjectId is None or ProjectId == "":
            raise MPCSDKException(
                "InvalidProjectId", "The ProjectId can not be None or invalid.")
        self.AK = AK
        self.SK = SK
        self.EndPoint = EndPoint
        self.ProjectId = ProjectId

    def _build_header(self, req):
        req.headers["Content-Type"] = "application/json"

    def _build_request(self, req, data, query):
        sig = signer.Signer()
        sig.AppKey = self.AK
        sig.AppSecret = self.SK

        r = copy.deepcopy(req)
        r.host = self.EndPoint
        r.uri = req.uri.replace("{project_id}", self.ProjectId)
        if data:
            r.body = json.dumps(data, ensure_ascii=False)
        if query:
            r.query = {}
            kv = []
            for k, v in query.items():
                if isinstance(v, (list, tuple)):
                    for v1 in v:
                        kv.append('{0}={1}'.format(signer.urlencode(str(k)), signer.urlencode(str(v1))))
                else:
                    kv.append('{0}={1}'.format(signer.urlencode(str(k)), signer.urlencode(str(v))))
            r.query.update({'&'.join(kv): ''})
        print(r.query)
        sig.Sign(r)
        print(r)
        self._build_header(r)
        return r

    def _build_response(self, http_resp, rsp):
        body = http_resp.content.decode() if sys.version_info[0] > 2 else http_resp.content.decode(encoding='UTF-8')
        rsp.from_json_string(body)
        rsp.http_code = http_resp.status_code
        rsp.x_request_id = http_resp.headers["X-request-id"]
        if http_resp.status_code < 300 and http_resp.status_code >= 200:
            rsp.request_status = BaseResponse.SUCCESS
        else:
            rsp.request_status = BaseResponse.FAILED

    def send(self, req, data, query, rsp):
        r = self._build_request(req, data, query)
        http_resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
        self._build_response(http_resp, rsp)
        return rsp

