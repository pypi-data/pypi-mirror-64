# -*- coding: utf-8 -*-


class MPCSDKException(Exception):
    """huaweicloudapi sdk 异常类"""

    def __init__(self, code=None, msg=None, request_id=None):
        self.code = code
        self.msg = msg
        self.request_id = request_id

    def __str__(self):
        return "[MPCSDKException] code: {0}, msg: {1}, request_id: {2}".format(
            self.code, self.msg, self.request_id)

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg

    def get_request_id(self):
        return self.request_id

