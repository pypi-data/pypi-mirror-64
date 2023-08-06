# -*- coding: utf-8 -*-
from common.base_model import BaseModel


class BaseResponse(BaseModel):
    """BaseResponse 基础响应结构体

    """
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    def __init__(self):
        """
        :param http_code: http状态码。
        :type http_code: Int
        :param request_status: 请求状态。
        :type request_status: Str
        :param x_request_id: 请求ID。
        :type x_request_id: str
        :param error_code: 错误码，失败时返回
        :type error_code: str
        :param error_msg: 错误描述，失败时返回
        :type error_msg: str

        """
        self.http_code = None
        self.request_status = None
        self.x_request_id = None
        self.error_code = None
        self.error_msg = None

    def _deserialize(self, params):
        self.http_code = params.get("http_code")
        self.request_status = params.get("request_status")
        self.x_request_id = params.get("x_request_id")
        self.error_code = params.get("error_code")
        self.error_msg = params.get("error_msg")

