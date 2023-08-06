# -*- coding: utf-8 -*-

from common.base_client import BaseClient
from common import signer
from common.exception.mpc_sdk_exception import MPCSDKException
from mpc import task_model
from mpc import template_model
from mpc.response import BaseResponse


class MPCClient(BaseClient):

    def CreateBatchTranscodeTask(self, requests):
        create_batch_task_rsp = task_model.CreateBatchTranscodeTaskResponse
        temp_responses = []
        if requests is not None:
            for request in requests:
                create_single_task_rsp = task_model.CreateTaskResponse()
                try:
                    if request.output is not None:
                        output_object = request.output.object
                        if "/" in output_object:
                            object_key = output_object[:output_object.rindex("/")]
                            output_filename = output_object[output_object.rindex("/")+1:]
                            if "." in output_filename:
                                request.output.object = object_key
                                request.output_filenames = output_filename
                        create_single_task_rsp = self.CreateTranscodeTask(request)
                        temp_responses.append(create_single_task_rsp)
                except Exception as e:
                    if isinstance(e, MPCSDKException):
                        create_single_task_rsp.error_code = e.get_code()
                        create_single_task_rsp.error_msg = e.get_msg()
                        create_single_task_rsp.request_status = BaseResponse.FAILED
                    else:
                        mpc_exce = MPCSDKException(None, e.args)
                        create_single_task_rsp.error_code = mpc_exce.get_code()
                        create_single_task_rsp.error_msg = mpc_exce.get_msg()
                        create_single_task_rsp.request_status = BaseResponse.FAILED
                    temp_responses.append(create_single_task_rsp)

        create_batch_task_rsp.task_array = temp_responses
        return create_batch_task_rsp

    def CreateTranscodeTask(self, request):
        """CreateTranscodeTask 用于创建一个转码任务。

        :param request: 调用CreateTranscodeTask所需参数的结构体。
        :type request: :class:`CreateTranscodeTaskRequest`
        :rtype: :class:`CreateTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/transcodings"
            data = request._serialize()
            rsp = task_model.CreateTaskResponse()
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def CreateThumbnailTask(self, request):
        """CreateThumbnailTask 用于创建一个截图任务。

        :param request: 调用CreateThumbnailTask所需参数的结构体。
        :type request: :class:`CreateThumbnailTaskRequest`
        :rtype: :class:`CreateTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/thumbnails"
            data = request._serialize()
            rsp = task_model.CreateTaskResponse()
            print("start send")
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryThumbnailTask(self, request):
        """QueryThumbnailTask 用于查询截图任务。

        :param request: 调用QueryThumbnailTask所需参数的结构体。
        :type request: :class:`QueryTaskRequest`
        :rtype: :class:`QueryTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/thumbnails"
            query = request._serialize()
            rsp = task_model.QueryThumbTaskResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteThumbnailTask(self, request):
        """DeleteTranscodeTask 用于删除截图任务。

        :param request: 调用DeleteThumbnailTask所需参数的结构体。
        :type request: :class:`DeleteTaskRequest`
        :rtype: :class:`DeleteTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/thumbnails"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def CreateExtractTask(self, request):
        """CreateExtractTask 用于创建一个截图任务。

        :param request: 调用CreateExtractTask所需参数的结构体。
        :type request: :class:`CreateExtractTaskRequest`
        :rtype: :class:`CreateTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/extract-metadata"
            data = request._serialize()
            rsp = task_model.CreateTaskResponse()
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def CreateEncryptTask(self, request):
        """CreateEncryptTask 用于创建一个加密任务。
        """
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/encryptions"
            data = request._serialize()
            rsp = task_model.CreateTaskResponse()
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryEncryptTask(self, request):
        """QueryEncryptTask 用于查询加密任务。
        """
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/encryptions"
            query = request._serialize()
            rsp = task_model.QueryEncryptTaskResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def CreateAnimatedGraphicsTask(self, request):
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/animated-graphics"
            data = request._serialize()
            rsp = task_model.CreateTaskResponse()
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def CreateRemuxTask(self, request):
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/remux"
            data = request._serialize()
            rsp = task_model.CreateTaskResponse()
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryAnimatedGraphicsTask(self, request):
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/animated-graphics"
            query = request._serialize()
            rsp = task_model.QueryAnimatedGraphicsTaskResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteAnimatedGraphicsTask(self, request):
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/animated-graphics"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryExtractTask(self, request):
        """QueryExtractTask 用于查询解析任务。

        :param request: 调用QueryExtractTask所需参数的结构体。
        :type request: :class:`QueryTaskRequest`
        :rtype: :class:`QueryTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/extract-metadata"
            query = request._serialize()
            rsp = task_model.QueryExtractTaskResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryRemuxTask(self, request):
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/remux"
            query = request._serialize()
            rsp = task_model.QueryRemuxTaskResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteRemuxTask(self, request):
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/remux"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)
    def RetryRemuxTask(self, request):
        try:
            r = signer.HttpRequest()
            r.method = "PUT"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/remux"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteEncryptTask(self, request):
        """DeleteEncryptTask 用于删除加密任务。
        """
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/encryptions"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteExtractTask(self, request):
        """DeleteExtractTask 用于删除视频解析任务。

        :param request: 调用DeleteExtractTask所需参数的结构体。
        :type request: :class:`DeleteStrTaskRequest`
        :rtype: :class:`DeleteTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/extract-metadata"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryTranscodeTasks(self, request):
        """QueryTranscodeTasks 用于查询转码任务。

        :param request: 调用QueryTranscodeTasks所需参数的结构体。
        :type request: :class:`QueryTaskRequest`
        :rtype: :class:`QueryTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/transcodings"
            query = request._serialize()
            rsp = task_model.QueryTaskResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryTranscodeDetailTasks(self, request):
        """QueryTranscodeDetailTasks 用于查询转码详情任务。

        :param request: 调用QueryTranscodeDetailTasks所需参数的结构体。
        :type request: :class:`QueryTaskDetailRequest`
        :rtype: :class:`QueryTaskDetailResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/transcodings/detail"
            query = request._serialize()
            rsp = task_model.QueryTaskDetailResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteTranscodeTask(self, request):
        """DeleteTranscodeTask 用于删除转码任务。

        :param request: 调用DeleteTranscodeTask所需参数的结构体。
        :type request: :class:`DeleteTaskRequest`
        :rtype: :class:`DeleteTaskResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/transcodings"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def CreateTranscodeTemplate(self, request):
        """CreateTranscodeTemplate 用于查询转码模板。

        :param request: 调用CreateTranscodeTemplate所需参数的结构体。
        :type request: :class:`TransTemplate`
        :rtype: :class:`CreateTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/transcodings"
            data = request._serialize()
            rsp = template_model.CreateTemplateResponse()
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryTranscodeTemplates(self, request):
        """QueryTranscodeTemplates 用于查询转码模板。

        :param request: 调用QueryTranscodeTemplates所需参数的结构体。
        :type request: :class:`QueryTemplateRequest`
        :rtype: :class:`QueryTranscodeTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/transcodings"
            query = request._serialize()
            rsp = template_model.QueryTranscodeTemplateResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def UpdateTranscodeTemplate(self, request):
        """UpdateTranscodeTemplate 用于更新转码模板。

        :param request: 调用UpdateTranscodeTemplate所需参数的结构体。
        :type request: :class:`TransTemplate`
        :rtype: :class:`UpdateTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "PUT"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/transcodings"
            query = {}
            if request.template_id is not None:
                query.update({"template_id": str(request.template_id)})
            data = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, data, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteTranscodeTemplate(self, request):
        """DeleteTranscodeTemplate 用于删除转码模板。

        :param request: 调用DeleteTranscodeTemplate所需参数的结构体。
        :type request: :class:`DeleteTemplateRequest`
        :rtype: :class:`DeleteTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/transcodings"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def CreateWatermarkTemplate(self, request):
        """CreateWatermarkTemplate 用于查询水印模板。

        :param request: 调用CreateWatermarkTemplate所需参数的结构体。
        :type request: :class:`WatermarkTemplate`
        :rtype: :class:`CreateTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "POST"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/watermark"
            data = request._serialize()
            rsp = template_model.CreateTemplateResponse()
            response = self.send(r, data, None, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def QueryWatermarkTemplates(self, request):
        """QueryWatermarkTemplates 用于查询水印模板。

        :param request: QueryWatermarkTemplates。
        :type request: :class:`QueryTemplateRequest`
        :rtype: :class:`QueryWatermarkTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "GET"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/watermark"
            query = request._serialize()
            rsp = template_model.QueryWatermarkTemplateResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def UpdateWatermarkTemplate(self, request):
        """UpdateWatermarkTemplate 用于更新水印模板。

        :param request: 调用UpdateWatermarkTemplate所需参数的结构体。
        :type request: :class:`WatermarkTemplate`
        :rtype: :class:`UpdateTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "PUT"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/watermark"
            query = {}
            if request.template_id is not None:
                query.update({"template_id": str(request.template_id)})
            data = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, data, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)

    def DeleteWatermarkTemplate(self, request):
        """DeleteWatermarkTemplate 用于删除水印模板。

        :param request: 调用DeleteWatermarkTemplate所需参数的结构体。
        :type request: :class:`DeleteTemplateRequest`
        :rtype: :class:`DeleteTemplateResponse`

        """
        try:
            r = signer.HttpRequest()
            r.method = "DELETE"
            r.scheme = "https"
            r.uri = "/v1/{project_id}/template/watermark"
            query = request._serialize()
            rsp = BaseResponse()
            response = self.send(r, None, query, rsp)
            return response
        except Exception as e:
            if isinstance(e, MPCSDKException):
                raise e
            else:
                raise MPCSDKException(None, e.args)




