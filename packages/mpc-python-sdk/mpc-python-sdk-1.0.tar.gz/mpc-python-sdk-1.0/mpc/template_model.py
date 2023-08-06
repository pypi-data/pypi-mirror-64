# -*- coding: utf-8 -*-
from common.base_model import BaseModel
from mpc.response import BaseResponse


class Video(BaseModel):
    """Video 模板视频相关参数结构体

    """

    def __init__(self):
        """
        :param codec: 视频编码格式 (有效值范围)。VIDEO_CODEC_H264 = 1
                                              VIDEO_CODEC_H265 = 2
        :type codec: int
        :param bitrate: 输出平均码率（单位：kbit/s）。有效值范围[0,30000]。
                        输出平均码率值为0，则输出平均码率自适应
        :type bitrate: int
        :param profile: 编码档次(有效值范围) 。 VIDEO_PROFILE_H264_BASE = 1,
                                              VIDEO_PROFILE_H264_MAIN = 2,
                                              VIDEO_PROFILE_H264_HIGH = 3,
                                              VIDEO_PROFILE_H265_MAIN = 4,
        :type profile: int
        :param level: 编码级别(有效值范围)。VIDEO_LEVEL_1_0 = 1,VIDEO_LEVEL_1_1 = 2,
                                          VIDEO_LEVEL_1_2 = 3,VIDEO_LEVEL_1_3 = 4,
                                          VIDEO_LEVEL_2_0 = 5,VIDEO_LEVEL_2_1 = 6,
                                          VIDEO_LEVEL_2_2 = 7,VIDEO_LEVEL_3_0 = 8,
                                          VIDEO_LEVEL_3_1 = 9,VIDEO_LEVEL_3_2 = 10,
                                          VIDEO_LEVEL_4_0 = 11,VIDEO_LEVEL_4_1 = 12,
                                          VIDEO_LEVEL_4_2 = 13,VIDEO_LEVEL_5_0 = 14,
                                          VIDEO_LEVEL_5_1 = 15, (default)
        :type level: int
        :param preset: 编码质量等级 (有效值范围)。VIDEO_PRESET_HSPEED2 = 1,//(只用于h.265, h.265 default)
                                               VIDEO_PRESET_HSPEED = 2,//(只用于h.265)
                                               VIDEO_PRESET_NORMAL = 3, // (h264/h.265可用，h.264 default)
        :type preset: int
        :param ref_frames_count: 最大参考帧数（单位：帧）。H264：范围[1，8] ，缺省值4。H265：固定值4。
        :type ref_frames_count: int
        :param max_iframes_interval: 帧最大间隔（单位:秒）。范围[2，5]，缺省值：5。
        :type max_iframes_interval: int
        :param bframes_count: 最大B帧间隔（单位：帧）。H264：范围[0，8] ，缺省值4。H265：固定值7。
        :type bframes_count: int
        :param frame_rate: 帧率（单位：帧每秒） (有效值范围)。FRAMERATE_AUTO = 1,FRAMERATE_10 = 2,
                                                          FRAMERATE_15 = 3,FRAMERATE_2397 = 4, // 23.97 fps
                                                          FRAMERATE_24 = 5,FRAMERATE_25 = 6,
                                                          FRAMERATE_2997 = 7, // 29.97 fps
                                                          FRAMERATE_30 = 8,FRAMERATE_50 = 9,
                                                          FRAMERATE_60 = 10
        :type frame_rate: int
        :param width: 视频宽度（单位：像素）。H264：范围[32,3840]，必须为2的倍数。
                      H265：范围[320,3840] ,必须是2的倍数。视频宽度值取0时，视频宽度值自适应
        :type width: int
        :param height: 视频高度（单位：像素）。H264：范围[32,2160],必须为2的倍数。
                       H265：范围[240,2160] ,必须是2的倍数。视频高度值取0时，视频高度值自适应
        :type height: int
        :param black_cut: 黑边剪裁类型。0：不开启黑边剪裁，1：开启黑边剪裁，低复杂度算法，针对长视频（>5分钟）（盖亚默认）
                                      2：开启黑边剪裁，高复杂度算法，针对短视频（<=5分钟）
        :type black_cut: int
        :param aspect_ratio: 纵横比（保留,图像缩放方式）。0：自适应（保持原有宽高比）。
                             1：补黑边（16:9），2：裁黑边（18:9）
        :type aspect_ratio: int
        :param GOP_structure: GOP类型（暂不开放）。0：Closed (Default)。1：Open。
        :type GOP_structure: int

        """
        self.codec = None
        self.bitrate = None
        self.profile = None
        self.level = None
        self.preset = None
        self.ref_frames_count = None
        self.max_iframes_interval = None
        self.bframes_count = None
        self.frame_rate = None
        self.width = None
        self.height = None
        self.black_cut = None
        self.aspect_ratio = None
        self.GOP_structure = None

    def _deserialize(self, params):
        self.codec = params.get("codec")
        self.bitrate = params.get("bitrate")
        self.profile = params.get("profile")
        self.level = params.get("level")
        self.preset = params.get("preset")
        self.ref_frames_count = params.get("ref_frames_count")
        self.max_iframes_interval = params.get("max_iframes_interval")
        self.bframes_count = params.get("bframes_count")
        self.frame_rate = params.get("frame_rate")
        self.width = params.get("width")
        self.height = params.get("height")
        self.black_cut = params.get("black_cut")
        self.aspect_ratio = params.get("aspect_ratio")
        self.GOP_structure = params.get("GOP_structure")


class Audio(BaseModel):
    """Audio 模板音频相关参数结构体

    """

    def __init__(self):
        """
        :param codec: 音频编码格式 (有效值范围)。AUDIO_CODECTYPE_AAC=1 (default)
                                              AUDIO_CODECTYPE_HEAAC1=2
                                              AUDIO_CODECTYPE_HEAAC2=3
        :type codec: int
        :param sample_rate: 音频采样率(有效值范围)。AUDIO_SAMPLE_22050=1,
                                                 AUDIO_SAMPLE_32000=2,
                                                 AUDIO_SAMPLE_44100=3,
                                                 AUDIO_SAMPLE_48000=4,
                                                 AUDIO_SAMPLE_96000=5,
        :type sample_rate: int
        :param bitrate: 音频码率（单位：kbit/s）。范围[64,320]。
        :type bitrate: int
        :param channels: 声道数(有效值范围)。AUDIO_CHANNELS_1=1,
                                           AUDIO_CHANNELS_2=2,
        :type channels: int

        """
        self.codec = None
        self.sample_rate = None
        self.bitrate = None
        self.channels = None

    def _deserialize(self, params):
        self.codec = params.get("codec")
        self.sample_rate = params.get("sample_rate")
        self.bitrate = params.get("bitrate")
        self.channels = params.get("channels")


class Common(BaseModel):
    """Common 模板公共参数结构体

    """

    def __init__(self):
        """
        :param QDS: QDS开关。0：关闭（当前默认关闭）。1：开启。
        :type QDS: Boolean
        :param PVC: PVC开关。0：关闭（当前默认关闭）。1：开启。
        :type PVC: Boolean
        :param PVC_version: PVC版本。0：PVC 1.0（高清低码）。1：PVC 2.0（高清低码和画质增强）
        :type PVC_version: str
        :param hls_interval: HLS分片间隔（单位：秒）。范围：[2，10]，缺省 5。
        :type hls_interval: int
        :param dash_interval: DASH间隔（单位：秒）。范围：[2，10]，缺省 5。
        :type dash_interval: int
        :param pack_type: 封装类型（DASH+MP4、HLS+TS）。
                          按bitmap来描述封装格式，每个bit代表一种封装格式，目前支持两种：
                          0000 0001 表示DASH+MP4格式。
                          0000 0010 表示HLS+TS格式。
                          0000 0011 表示HLS+TS和DASH+MP4格式。
                          0000 0100 表示DASH+MP4（普通）格式。
        :type pack_type: int

        """
        self.QDS = None
        self.PVC = None
        self.PVC_version = None
        self.PVC_strength = None
        self.hls_interval = None
        self.dash_interval = None
        self.pack_type = None

    def _deserialize(self, params):
        self.QDS = params.get("QDS")
        self.PVC = params.get("PVC")
        self.PVC_version = params.get("PVC_version")
        self.PVC_strength = params.get("PVC_strength")
        self.hls_interval = params.get("hls_interval")
        self.dash_interval = params.get("dash_interval")
        self.pack_type = params.get("pack_type")


class TransTemplate(BaseModel):
    """TransTemplate 转码模板参数结构体

    """

    def __init__(self):
        """
        :param template_id: 转码模板ID
        :type template_id: int
        :param template_name: 转码模板名称
        :type template_name: str
        :param tenant_id: 租户ID
        :type tenant_id: str
        :param video: 模板视频相关参数
        :type video: Video
        :param audio: 模板音频相关参数
        :type audio: Audio
        :param common: 模板公共参数
        :type common: Common

        """
        self.template_id = None
        self.template_name = None
        self.tenant_id = None
        self.video = None
        self.audio = None
        self.common = None

    def _deserialize(self, params):
        self.template_id = params.get("template_id")
        self.template_name = params.get("template_name")
        self.tenant_id = params.get("tenant_id")
        if params.get("video") is not None:
            self.video = Video()
            self.video._deserialize(params.get("video"))
        if params.get("audio") is not None:
            self.audio = Audio()
            self.audio._deserialize(params.get("audio"))
        if params.get("common") is not None:
            self.common = Common()
            self.common._deserialize(params.get("common"))


class WatermarkTemplate(BaseModel):
    """WatermarkTemplate 水印模板参数结构体

    """

    def __init__(self):
        """
        :param template_id: 水印模板ID
        :type template_id: str
        :param template_name: 水印模板名称
        :type template_name: str
        :param tenant_id: 租户ID
        :type tenant_id: str
        :param type: 水印类型，当前只支持Image（图片水印）。后续根据需求再支持Text（文字水印）。
        :type type: str
        :param image_process: 图片水印处理方式，type设置为Image时有效，目前包括Original（只做
                              简单缩放，不做其他处理），Grayed（彩色图片变灰）。
        :type image_process: str
        :param width: 水印图片宽，值有两种形式：整数型代表水印图片宽的像素值，范围[8，4096]，单位px。
                      小数型代表相对输出视频分辨率宽的比率，范围(0,1)，支持4位小数，如0.9999，超出部
                      分系统自动丢弃。
        :type width: str
        :param height: 水印图片高，值有两种形式：整数型代表水印图片高的像素值，范围[8，4096]，单位px。
                       小数型代表相对输出视频分辨率高的比率，范围(0，1)，支持4位小数，如0.9999，超出部
                       分系统自动丢弃。
        :type height: str
        :param dx: 水印图片相对输出视频的水平偏移量，默认值是0。值有两种形式：整数型代表偏移像素，范围
                   [8，4096]，单位px。小数型代表水平偏移量与输出分辨率宽的比率，范围(0，1)，支持4位小
                   数，如0.9999，超出部分系统自动丢弃。
        :type dx: str
        :param dy: 水印图片相对输出视频的垂直偏移量，默认值是0。值有两种形式：整数型代表偏移像素，范围
                   [8，4096]，单位px。小数型代表垂直偏移量与输出分辨率高的比率，范围(0，1)，支持4位小
                   数，如0.9999，超出部分系统自动丢弃。
        :type dy: str
        :param referpos: 水印的位置，值范围TopRight、TopLeft、BottomRight、BottomLeft。
        :type referpos: str
        :param timeline_start: 水印开始时间，和timeline_duration配合使用。单位：秒。取值范围：数字，
                               默认值0。
        :type timeline_start: str
        :param timeline_duration: 水印持续时间，和timeline_start配合使用。取值范围：[数字，ToEND],
                                  默认值ToEND。
        :type timeline_duration: str

        """
        self.template_id = None
        self.template_name = None
        self.tenant_id = None
        self.type = None
        self.image_process = None
        self.width = None
        self.height = None
        self.dx = None
        self.dy = None
        self.base = None
        self.referpos = None
        self.timeline_start = None
        self.timeline_duration = None

    def _deserialize(self, params):
        self.template_id = params.get("template_id")
        self.template_name = params.get("template_name")
        self.tenant_id = params.get("tenant_id")
        self.type = params.get("type")
        self.image_process = params.get("image_process")
        self.width = params.get("width")
        self.height = params.get("height")
        self.dx = params.get("dx")
        self.dy = params.get("dy")
        self.dy = params.get("base")
        self.referpos = params.get("referpos")
        self.timeline_start = params.get("timeline_start")
        self.timeline_duration = params.get("timeline_duration")


class CreateTemplateResponse(BaseResponse):
    """CreateTemplateResponse 创建模板返回参数结构体

    """

    def __init__(self):
        """
        :param template_id: 唯一模板标识ID，创建成功时返回。
        :type template_id: Int

        """
        BaseResponse.__init__(self)
        self.template_id = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        self.template_id = params.get("template_id")


class QueryTemplateRequest(BaseModel):
    """QueryTemplateRequest 查询模板请求参数结构体

    """

    def __init__(self):
        """
        :param template_id: 模板ID
        :type template_id: list of int
        :param page: 分页编号。默认为0。指定template_id时该参数无效。
        :type page: int
        :param size: 每页记录数。默认10，范围[1,100]。指定template_id时该参数无效。
        :type size: int

        """
        self.template_id = None
        self.page = None
        self.size = None

    def _deserialize(self, params):
        self.template_id = params.get("template_id")
        self.page = params.get("page")
        self.size = params.get("size")


class QueryOneTranscodeTemplateResponse(BaseResponse):
    """QueryOneTranscodeTemplateResponse 查询单个转码模板响应参数结构体

    """

    def __init__(self):
        """
        :param template_id: 转码模板ID
        :type template_id: int
        :param template: 转码模板参数结构体
        :type template: TransTemplate
        :param error_code: 错误码
        :type error_code: str
        :param error_msg: 错误描述
        :type error_msg: str

        """
        self.template_id = None
        self.template = None
        self.error_code = None
        self.error_msg = None

    def _deserialize(self, params):
        self.template_id = params.get("template_id")
        if params.get("template") is not None:
            self.template = TransTemplate()
            self.template._deserialize(params.get("template"))
        self.error_code = params.get("error_code")
        self.error_msg = params.get("error_msg")


class QueryOneWatermarkTemplateResponse(BaseResponse):
    """QueryOneWatermarkTemplateResponse 查询单个水印模板响应参数结构体

    """

    def __init__(self):
        """
        :param template_id: 水印模板ID
        :type template_id: int
        :param template: 水印模板参数结构体
        :type template: WatermarkTemplate
        :param error_code: 错误码
        :type error_code: str
        :param error_msg: 错误描述
        :type error_msg: str

        """
        self.template_id = None
        self.template = None
        self.error_code = None
        self.error_msg = None

    def _deserialize(self, params):
        self.template_id = params.get("template_id")
        if params.get("template") is not None:
            self.template = WatermarkTemplate()
            self.template._deserialize(params.get("template"))
        self.error_code = params.get("error_code")
        self.error_msg = params.get("error_msg")


class QueryTranscodeTemplateResponse(BaseResponse):
    """QueryTranscodeTemplateResponse 查询转码模板响应参数结构体

    """

    def __init__(self):
        """
        :param template_array: 转码模板信息
        :type template_array: list of QueryOneTranscodeTemplateResponse
        :param total: 转码模板总数
        :type total: int

        """
        BaseResponse.__init__(self)
        self.template_array = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("template_array") is not None:
            self.template_array = []
            for item in params.get("template_array"):
                obj = QueryOneTranscodeTemplateResponse()
                obj._deserialize(item)
                self.template_array.append(obj)
        self.total = params.get("total")


class QueryWatermarkTemplateResponse(BaseResponse):
    """QueryWatermarkTemplateResponse 查询水印模板响应参数结构体

    """

    def __init__(self):
        """
        :param template_array: 转码模板信息
        :type template_array: list of QueryOneWatermarkTemplateResponse
        :param total: 转码模板总数
        :type total: int

        """
        BaseResponse.__init__(self)
        self.template_array = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("template_array") is not None:
            self.template_array = []
            for item in params.get("template_array"):
                obj = QueryOneWatermarkTemplateResponse()
                obj._deserialize(item)
                self.template_array.append(obj)
        self.total = params.get("total")


class DeleteTemplateRequest(BaseModel):
    """DeleteTemplateRequest 删除模板请求参数结构体

    """

    def __init__(self):
        """
        :param template_id: 模板ID
        :type template_id: Int

        """
        self.template_id = None

    def _deserialize(self, params):
        self.template_id = params.get("template_id")


