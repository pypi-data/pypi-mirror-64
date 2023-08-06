# -*- coding: utf-8 -*-
from common.base_model import BaseModel
from mpc.response import BaseResponse


class ObsInfo(BaseModel):
    """ObsInfo OBS参数结构体

    """
    def __init__(self):
        """
        :param bucket: OBS的bucket名称
        :type bucket: str
        :param location: 输入的OBS bucket所在的数据中心
        :type location: str
        :param object: OBS对象路径，当用于指示input时，需要指定到具体对象
                       当用于指示output时，只需指定到转码输出路径即可
        :type object: str

        """
        self.bucket = None
        self.location = None
        self.object = None

    def _deserialize(self, params):
        self.bucket = params.get("bucket")
        self.location = params.get("location")
        self.object = params.get("object")


class Video(BaseModel):
    """Video 视频参数结构体

    """
    def __init__(self):
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
        self.sr_factor = None

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
        self.sr_factor = params.get("sr_factor")


class Audio(BaseModel):
    """Audio 音频参数结构体

    """
    def __init__(self):
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
    """Common 公共参数结构体

    """
    def __init__(self):

        self.PVC = None
        self.QDS = None
        self.PVC_version = None
        self.PVC_strength = None
        self.hls_interval = None
        self.dash_interval = None
        self.pack_type = None

    def _deserialize(self, params):
        self.PVC = params.get("PVC")
        self.QDS = params.get("QDS")
        self.PVC_version = params.get("PVC_version")
        self.PVC_strength = params.get("PVC_strength")
        self.hls_interval = params.get("hls_interval")
        self.dash_interval = params.get("dash_interval")
        self.pack_type = params.get("pack_type")


class Error(BaseModel):
    """Error 错误参数结构体

    """
    def __init__(self):
        """
        :param error_code: 错误码
        :type error_code: str
        :param error_msg: 错误描述
        :type error_msg: str

        """
        self.error_code = None
        self.error_msg = None

    def _deserialize(self, params):
        self.error_code = params.get("error_code")
        self.error_msg = params.get("error_msg")


class DetailError(BaseModel):
    """DetailError 转码模板信息参数结构体

    """
    def __init__(self):
        """
        :param template_id: 转码失败的模板ID
        :type template_id: Int
        :param error: 转码失败的错误信息
        :type error: Error

        """
        self.template_id = None
        self.error = None

    def _deserialize(self, params):
        self.template_id = params.get("template_id")
        if params.get("error") is not None:
            self.error = Error()
            self.error._deserialize(params.get("error"))


class MediaDetail(BaseModel):
    """MediaDetail 转码媒资的详情参数结构体

    """
    def __init__(self):
        """
        :param features:
        :type features: list of str
        :param origin_para: 原始片源信息
        :type origin_para: OriginPara
        :param output_video_paras: 输出视频信息
        :type output_video_paras: list of OutputVideoPara
        :param output_thumbnail_para: 输出抽帧截图信息
        :type output_thumbnail_para: OutputVideoPara
        :param output_watermark_paras: 输出水印信息
        :type output_watermark_paras: OutputWatermarkPara
        """

        self.features = None
        self.origin_para = None
        self.output_video_paras = None
        self.output_thumbnail_para = None
        self.output_watermark_paras = None

    def _deserialize(self, params):
        self.features = params.get("features")
        if params.get("origin_para") is not None:
            self.origin_para = OriginPara()
            self.origin_para._deserialize(params.get("origin_para"))

        if params.get("output_video_paras") is not None:
            self.output_video_paras = []
            for item in params.get("output_video_paras"):
                obj = OutputVideoPara()
                obj._deserialize(item)
                self.output_video_paras.append(obj)

        if params.get("output_thumbnail_para") is not None:
            self.output_thumbnail_para = OutputThumbnailPara()
            self.output_thumbnail_para._deserialize(params.get("output_thumbnail_para"))

        if params.get("output_watermark_paras") is not None:
            self.output_watermark_paras = OutputWatermarkPara()
            self.output_watermark_paras._deserialize(params.get("output_watermark_paras"))


class OriginPara(BaseModel):
    """OriginPara 原始片源信息参数结构体

    """
    def __init__(self):
        """
        :param duration: 片源时长
        :type duration: int
        :param file_format:  文件格式
        :type file_format: str
        :param video: 原始片源视频信息
        :type video: VideoInfo
        :param audio: 原始片源音频信息
        :type audio: AudioInfo

        """
        self.duration = None
        self.file_format = None
        self.video = None
        self.audio = None

    def _deserialize(self, params):
        self.duration = params.get("duration")
        self.file_format = params.get("file_format")
        if params.get("video") is not None:
            self.video = VideoInfo()
            self.video._deserialize(params.get("video"))
        if params.get("audio") is not None:
            self.audio = AudioInfo()
            self.audio._deserialize(params.get("audio"))


class VideoInfo(BaseModel):
    """VideoInfo 原始片源视频信息参数结构体

    """
    def __init__(self):
        """
        :param width: 视频宽度
        :type width: int
        :param height:  视频高度
        :type height: int
        :param bitrate:  视频码率
        :type bitrate: int
        :param frame_rate: 视频帧率
        :type frame_rate: int
        :param codec: 视频编码格式
        :type codec: str

        """
        self.width = None
        self.height = None
        self.bitrate = None
        self.frame_rate = None
        self.codec = None

    def _deserialize(self, params):
        self.width = params.get("width")
        self.height = params.get("height")
        self.bitrate = params.get("bitrate")
        self.frame_rate = params.get("frame_rate")
        self.codec = params.get("codec")


class AudioInfo(BaseModel):
    """VideoInfo 原始片源视频信息参数结构体

    """
    def __init__(self):
        """
        :param sample: 音频采样率
        :type sample: int
        :param channels:  音频信道
        :type channels: int
        :param bitrate:  音频码率
        :type bitrate: int
        :param codec: 音频编码格式
        :type codec: str

        """
        self.sample = None
        self.channels = None
        self.bitrate = None
        self.codec = None

    def _deserialize(self, params):
        self.sample = params.get("sample")
        self.channels = params.get("channels")
        self.bitrate = params.get("bitrate")
        self.codec = params.get("codec")


class OutputVideoPara(BaseModel):
    """OutputVideoPara 输出视频信息参数结构体

    """
    def __init__(self):
        """
        :param size: 视频大小
        :type size: int
        :param pack:  视频封装格式
        :type pack: str
        :param file_name:  输出片源文件名
        :type file_name: str
        :param video: 输出片源视频信息
        :type video: VideoInfo
        :param audio: 输出片源音频信息
        :type audio: AudioInfo

        """
        self.size = None
        self.pack = None
        self.file_name = None
        self.video = None
        self.audio = None

    def _deserialize(self, params):
        self.size = params.get("size")
        self.pack = params.get("pack")
        self.file_name = params.get("file_name")
        if params.get("video") is not None:
            self.video = VideoInfo()
            self.video._deserialize(params.get("video"))
        if params.get("audio") is not None:
            self.audio = AudioInfo()
            self.audio._deserialize(params.get("audio"))


class OutputThumbnailPara(BaseModel):
    """OutputThumbnailPara  输出抽帧图片参数结构体

    """
    def __init__(self):
        """
        :param total_pictures: 片源时长
        :type total_pictures: int
        :param width:  抽帧图片宽度
        :type width: int
        :param height: 抽帧图片高度
        :type height: int
        :param file_name:  抽帧文件名
        :type file_name: str
        :param output: 抽帧任务的输出信息
        :type output: ObsInfo

        """
        self.total_pictures = None
        self.width = None
        self.height = None
        self.file_name = None
        self.output = None

    def _deserialize(self, params):
        self.total_pictures = params.get("total_pictures")
        self.width = params.get("width")
        self.height = params.get("height")
        self.file_name = params.get("file_name")
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))


class OutputWatermarkPara(BaseModel):
    """OutputWatermarkPara  输出水印参数结构体

    """
    def __init__(self):
        """
        :param time_duration: 水印时长
        :type time_duration: int

        """
        self.time_duration = None


class TranscodeDetail(BaseModel):
    """TranscodeDetail 转码信息参数结构体

    """
    def __init__(self):
        """
        :param multitask_info: 转码失败的模板ID以及失败信息
        :type multitask_info: list of DetailError

        """
        self.multitask_info = None

    def _deserialize(self, params):
        if params.get("multitask_info") is not None:
            self.multitask_info = []
            for item in params.get("multitask_info"):
                obj = DetailError()
                obj._deserialize(item)
                self.multitask_info.append(obj)


class TaskInfo(BaseModel):
    """TaskInfo 任务信息参数结构体

    """
    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: str
        :param status: 任务执行状态
        :type status: str
        :param create_time: 任务开始时间
        :type create_time: str
        :param end_time: 任务结束时间
        :type end_time: str
        :param input: 文件输入地址
        :type input: ObsInfo
        :param output: 文件输出地址
        :type output: ObsInfo
        :param description: 转码任务描述，当转码出现异常时，此字段为异常的原因
        :type description: str
        :param output_file_name: 转码生成的文件名
        :type output_file_name: list of str
        :param trans_template_id: 转码任务对应的模板ID
        :type trans_template_id: list of int
        :param transcode_detail: 一进多出情况下部分转码失败信息
        :type transcode_detail: TranscodeDetail

        """
        self.task_id = None
        self.status = None
        self.create_time = None
        self.end_time = None
        self.input = None
        self.output = None
        self.description = None
        self.output_file_name = None
        self.trans_template_id = None
        self.transcode_detail = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.create_time = params.get("create_time")
        self.end_time = params.get("end_time")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        self.description = params.get("description")
        self.output_file_name = params.get("output_file_name")
        self.trans_template_id = params.get("trans_template_id")
        if params.get("transcode_detail") is not None:
            self.transcode_detail = TranscodeDetail()
            self.transcode_detail._deserialize(params.get("transcode_detail"))


class TaskDetailInfo(BaseModel):
    """TaskDetailInfo 任务信息参数结构体

    """
    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: str
        :param status: 任务执行状态
        :type status: str
        :param create_time: 任务开始时间
        :type create_time: str
        :param end_time: 任务结束时间
        :type end_time: str
        :param input: 文件输入地址
        :type input: ObsInfo
        :param output: 文件输出地址
        :type output: ObsInfo
        :param description: 转码任务描述，当转码出现异常时，此字段为异常的原因
        :type description: str
        :param media_detail: 转码媒资的详情，包括原始片源的格式/时长等,转码输出视频的信息
        :type media_detail: MediaDetail

        """
        self.task_id = None
        self.status = None
        self.create_time = None
        self.end_time = None
        self.input = None
        self.output = None
        self.description = None
        self.output_file_name = None
        self.media_detail = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.create_time = params.get("create_time")
        self.end_time = params.get("end_time")

        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        self.description = params.get("description")
        self.output_file_name = params.get("output_file_name")
        if params.get("media_detail") is not None:
            self.media_detail = MediaDetail()
            self.media_detail._deserialize(params.get("media_detail"))


class ThumbnailPara(BaseModel):
    """ThumbnailPara 抽帧参数结构体

    """
    def __init__(self):
        """
        :param type: 采样类型。支持三种采样方式（当前只支持“TIME”）：
                     “PERCENT”：根据视频时长的百分比间隔采样
                     “TIME”：根据时间间隔采样
                     “DOTS” : 指定时间点截图  当前只支持是TIME
        :type type: str
        :param time: 预览图生成间隔时间（单位：秒）范围[1，100]
        :type time: int
        :param format: 图片格式，当前只支持jpg, 暂不开放，1 : jpg
        :type format: int
        :param aspect_ratio: 纵横比（保留,图像缩放方式）0：自适应（保持原有宽高比）1：16:9
        :type aspect_ratio: int
        :param width: 图片宽度，[96, 3840]
        :type width: int
        :param height: 图片高度，[96, 2160]
        :type height: int
        :param max_length: 预览图最长边尺寸（单位：像素）(宽边尺寸按照MaxSize与原始视频像素
                           等比缩放计算)范围[240,3840], 缺省值：480
        :type max_length: int
        """
        self.type = None
        self.time = None
        self.start_time = None
        self.percent = None
        self.duration = None
        self.dots = None
        self.format = None
        self.aspect_ratio = None
        self.width = None
        self.height = None
        self.max_length = None

    def _deserialize(self, params):
        self.type = params.get("type")
        self.time = params.get("time")
        self.percent = params.get("percent")
        self.start_time = params.get("start_time")
        self.duration = params.get("duration")
        self.dots = params.get("dots")
        self.format = params.get("format")
        self.aspect_ratio = params.get("aspect_ratio")
        self.width = params.get("width")
        self.height = params.get("height")
        self.max_length = params.get("max_length")


class Thumbnail(BaseModel):
    """Thumbnail 抽帧截图参数结构体

    """
    def __init__(self):
        """
        :param tar: 是否将生成的图片压缩成tar包，1表示不压缩，0表示压缩
        :type tar: int
        :param out: 抽帧截图输出路径，不填写时与转码输出在一起
        :type out: ObsInfo
        :param params: 抽帧參數
        :type params: ThumbnailPara

        """
        self.tar = None
        self.out = None
        self.params = None

    def _deserialize(self, params):
        self.tar = params.get("tar")
        if params.get("out") is not None:
            self.out = ObsInfo()
            self.out._deserialize(params.get("out"))
        if params.get("params") is not None:
            self.params = ThumbnailPara()
            self.params._deserialize(params.get("params"))

class CreateThumbnailTaskRequest(BaseModel):
    """Thumbnail 抽帧截图参数结构体

    """
    def __init__(self):
        """
        :param tar: 是否将生成的图片压缩成tar包，1表示不压缩，0表示压缩
        :type tar: int
        :param sync: 是否同步处理，同步处理是指不下载全部文件，快速定位到截图位置进行截图。，1表示同步处理，暂只支持按时间点截单张图，0排队处理
        :type sync: int
        :param output: 抽帧截图输出路径
        :type output: ObsInfo
        :param input: 抽帧截图源文件地址
        :type input: ObsInfo
        :param params: 抽帧參數
        :type params: Thumbnail_para

        """
        self.tar = None
        self.sync = None
        self.output = None
        self.input = None
        self.params = None

    def _deserialize(self, params):
        self.sync = params.get("sync")
        self.tar = params.get("tar")
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("thumbnail_para") is not None:
            self.thumbnail_para = Thumbnail_para()
            self.thumbnail_para._deserialize(params.get("thumbnail_para"))

class Thumbnail_para(BaseModel):
    """ThumbnailPara 抽帧参数结构体

    """
    def __init__(self):
        """
        :param type: 采样类型。支持三种采样方式（当前只支持“TIME”）：
                     “PERCENT”：根据视频时长的百分比间隔采样
                     “TIME”：根据时间间隔采样
                     “DOTS” : 指定时间点截图  当前只支持是TIME
        :type type: str
        :param time: 预览图生成间隔时间（单位：秒）范围[1，100]
        :type time: int
        :param start_time: 采样类型为“TIME”模式的开始时间，和“time”配合使用。默认值：0,单位：秒。
        :type start_time: int
        :param duration: 采样类型为“TIME”模式的持续时间，和“time”、“start_time”配合使用,取值范围：[数字，ToEND]
        :type duration: int
        :param dots: 指定时间截图时的时间点数组
        :type dots: list of ints
        :param format: 图片格式，当前只支持jpg, 暂不开放，1 : jpg
        :type format: int
        :param aspect_ratio: 纵横比（保留,图像缩放方式）0：自适应（保持原有宽高比）1：16:9
        :type aspect_ratio: int
        :param width: 图片宽度，[96, 3840]
        :type width: int
        :param height: 图片高度，[96, 2160]
        :type height: int
        :param max_length: 预览图最长边尺寸（单位：像素）(宽边尺寸按照MaxSize与原始视频像素
                           等比缩放计算)范围[240,3840], 缺省值：480
        :type max_length: int
        """
        self.type = None
        self.percent = None
        self.time = None
        self.start_time = None
        self.duration = None
        self.dots = None
        self.format = None
        self.aspect_ratio = None
        self.width = None
        self.height = None
        self.max_length = None

    def _deserialize(self, params):
        self.type = params.get("type")
        self.time = params.get("time")
        self.percent = params.get("percent")
        self.start_time = params.get("start_time")
        self.duration = params.get("duration")
        self.dots = params.get("dots")
        self.format = params.get("format")
        self.aspect_ratio = params.get("aspect_ratio")
        self.width = params.get("width")
        self.height = params.get("height")
        self.max_length = params.get("max_length")


class AnimatedGraphicsOutputParam(BaseModel):
    def __init__(self):
        self.format = None
        self.width = None
        self.height = None
        self.start = None
        self.end = None
        self.frame_rate = None

    def _deserialize(self, params):
        self.format = params.get("format")
        self.width = params.get("width")
        self.height = params.get("height")
        self.start = params.get("start")
        self.end = params.get("end")
        self.frame_rate = params.get("frame_rate")


class CreateAnimatedGraphicsTaskReq(BaseModel):

    def __init__(self):
        self.output_param = None
        self.output = None
        self.input = None

    def _deserialize(self, params):
        if params.get("output_param") is not None:
            self.output_param = AnimatedGraphicsOutputParam()
            self.output_param._deserialize(params.get("output_param"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))

class CreateEncryptRequest(BaseModel):
    def __init__(self):
        self.encryption = None
        self.output = None
        self.input = None

    def _deserialize(self, params):
        if params.get("encryption") is not None:
            self.encryption = Encryption()
            self.encryption._deserialize(params.get("encryption"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))


class CreateExtractTaskRequest(BaseModel):

    def __init__(self):
        """
        :param sync: 是否同步处理，同步处理是指不下载全部文件，快速定位到截图位置进行截图。，1表示同步处理，暂只支持按时间点截单张图，0排队处理
        :type sync: int
        :param output: 抽帧截图输出路径
        :type output: ObsInfo
        :param input: 抽帧截图源文件地址
        :type input: ObsInfo

        """
        self.sync = None
        self.output = None
        self.input = None

    def _deserialize(self, params):
        self.sync = params.get("sync")
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))


class RemuxOutputParam(BaseModel):
    def __init__(self):

        self.format = None
        self.segment_duration = None

    def _deserialize(self, params):
        self.sync = params.get("format")
        self.segment_duration = params.get("segment_duration")

class CreateRemuxTaskRequest(BaseModel):

    def __init__(self):
        self.output_param = None
        self.output = None
        self.input = None

    def _deserialize(self, params):
        if params.get("output_param") is not None:
            self.output_param = RemuxOutputParam()
            self.output_param._deserialize(params.get("output_param"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))

class Watermark(BaseModel):
    """Watermark 水印参数结构体

    """
    def __init__(self):
        """
        :param input: 水印图片地址
        :type input: ObsInfo
        :param template_id: 水印模板ID
        :type template_id: str
        :param image_watermark: 图片水印参数，用于覆盖图片水印模板中的同名参数。
        :type image_watermark: ImageWatermark
        :param text_content: 图片水印参数，用于覆盖图片水印模板中的同名参数。
        :type text_content: str
        :param text_watermark: 文字水印配置，若设置“text_context”，则此配置项不能为空。
        :type text_watermark: TextWatermark

        """
        self.input = None
        self.template_id = None
        self.image_watermark = None
        self.text_content = None
        self.text_watermark = None

    def _deserialize(self, params):
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        self.template_id = params.get("template_id")
        if params.get("image_watermark") is not None:
            self.image_watermark = ImageWatermark()
            self.image_watermark._deserialize(params.get("image_watermark"))
        self.text_content = params.get("text_content")
        if params.get("text_watermark") is not None:
            self.text_watermark = TextWatermark()
            self.text_watermark._deserialize(params.get("text_watermark"))


class ImageWatermark(BaseModel):
    """ImageWatermark 图片水印参数结构体

    """

    def __init__(self):
        """
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
        :param base: 水印叠加的基础视频,取值如下：（默认取值 “input”）
                     "input" ：水印基于输入片源叠加
                     “output” ：水印基于转码输出片源叠加。
                     （注意：只有1入1出场景支持设置为"output"；叠加多个水印时，该值必须相等，否则按第0个水印设置的值叠加水印）
        :type base: str

        """

        self.image_process = None
        self.width = None
        self.height = None
        self.dx = None
        self.dy = None
        self.referpos = None
        self.timeline_start = None
        self.timeline_duration = None
        self.base = None

    def _deserialize(self, params):
        self.image_process = params.get("image_process")
        self.width = params.get("width")
        self.height = params.get("height")
        self.dx = params.get("dx")
        self.dy = params.get("dy")
        self.referpos = params.get("referpos")
        self.timeline_start = params.get("timeline_start")
        self.timeline_duration = params.get("timeline_duration")
        self.base = params.get("base")


class TextWatermark(BaseModel):
    """TextWatermark 文字水印参数结构体

    """

    def __init__(self):
        """
        :param font_name: 文字水印字体，取值为fzyouh/msyh，默认值为msyh
        :type font_name: str
        :param font_size: 字体大小，默认值16，范围是（4,20）
        :type font_size: str
        :param font_color: 字体颜色，默认值：white
        :type font_color: str
        :param dx: 相对输出视频的水平偏移量，默认值是0。值有两种形式：整数型代表偏移像素，范围
                   [8，4096]，单位px。小数型代表水平偏移量与输出分辨率宽的比率，范围(0，1)，支持4位小
                   数，如0.9999，超出部分系统自动丢弃。
        :type dx: str
        :param dy: 相对输出视频的垂直偏移量，默认值是0。值有两种形式：整数型代表偏移像素，范围
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
        :param base: 水印叠加的基础视频,取值如下：（默认取值 “input”）
                     "input" ：水印基于输入片源叠加
                     “output” ：水印基于转码输出片源叠加。
                     （注意：只有1入1出场景支持设置为"output"；叠加多个水印时，该值必须相等，否则按第0个水印设置的值叠加水印）
        :type base: str

        """

        self.font_name = None
        self.font_size = None
        self.font_color = None
        self.dx = None
        self.dy = None
        self.referpos = None
        self.timeline_start = None
        self.timeline_duration = None
        self.base = None

    def _deserialize(self, params):
        self.font_name = params.get("font_name")
        self.font_size = params.get("font_size")
        self.font_color = params.get("font_color")
        self.dx = params.get("dx")
        self.dy = params.get("dy")
        self.referpos = params.get("referpos")
        self.timeline_start = params.get("timeline_start")
        self.timeline_duration = params.get("timeline_duration")
        self.base = params.get("base")


class AvParameter(BaseModel):
    """AvParameter 音视频参数结构体

    """
    def __init__(self):
        """
        :param video: 视频参数
        :type video: Video
        :param audio: 音频参数
        :type audio: Audio
        :param common: 公共参数
        :type common: Common

        """
        self.video = None
        self.audio = None
        self.common = None

    def _deserialize(self, params):
        if params.get("video") is not None:
            self.video = Video()
            self.video._deserialize(params.get("video"))

        if params.get("audio") is not None:
            self.audio = Audio()
            self.audio._deserialize(params.get("audio"))

        if params.get("common") is not None:
            self.common = Common()
            self.common._deserialize(params.get("common"))


class Audit(BaseModel):
    """Audit 内容质检参数结构体

    """
    def __init__(self):
        """
        :param position: 内容质检位置，0: 关闭定量类质检（花屏、卡顿、块效应）
                                      1：对原始片源质检，
                                      2：对转码后片源质检
        :type position: Int
        :param index: 转码模板ID索引（base 0）,当position=2时，此字段生效，表示
                      对转码后的第index路质检。针对定量类质检，要求：
                      1. 原始分辨率必须是1280*720之上（包含）
                      2. 对转码后片源检测，index对应的一路必须和原始分辨率一致，
                         若不一致，会在其它路输出中挑选与原始片源分辨率相同的。
        :type index: Int

        """
        self.position = None
        self.index = None

    def _deserialize(self, params):
        self.position = params.get("position")
        self.index = params.get("index")


class MulInputFileInfo(BaseModel):
    """多字幕文件地址

    """
    def __init__(self):
        self.language = None
        self.input = None

    def _deserialize(self, params):
        self.language = params.get("language")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))

class Subtitle(BaseModel):
    """Subtitle 字幕参数结构体

    """
    def __init__(self):
        """

        :param subtitle_type: 字幕类型，0 不输出字幕，1外部字幕文件嵌入视频流
        :type subtitle_type: str
        :param input: 字幕文件地址，当subtitle_type=1时，此字段必填
        :type input: ObsInfo

        """
        self.input = None
        self.inputs = None
        self.subtitle_type = None

    def _deserialize(self, params):
        self.subtitle_type = params.get("subtitle_type")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("inputs") is not None:
            self.input = MulInputFileInfo()
            self.input._deserialize(params.get("inputs"))


class CreateBatchTranscodeTaskRequest(BaseModel):
    """CreateBatchTranscodeTaskRequest 创建任务请求参数结构体

    """

    def __init__(self):
        """
        :param requests:
        :type requests: list of CreateTranscodeTaskRequest

        """
        self.requests = None

    def _deserialize(self, params):

        if params.get("requests") is not None:
            self.requests = []
            for item in params.get("requests"):
                obj = CreateTranscodeTaskRequest()
                obj._deserialize(item)
                self.requests.append(obj)


class HlsEncrypt(BaseModel):

    def __init__(self):
        """
        :param key: 内容加密密钥，base64Binary
        :type key: String
        :param url: 密钥获取服务的地址
        :type url: String
        :param iv: 初始向量，base64Binary，随机数
        :type iv: String
        :param algorithm: 加密算法
        :type algorithm: String
        """

        self.key = None
        self.url = None
        self.iv = None
        self.algorithm = None

    def _deserialize(self, params):
        self.key = params.get("key")
        self.url = params.get("url")
        self.iv = params.get("iv")
        self.algorithm = params.get("algorithm")


class Multidrm(BaseModel):
    """对接第三方DRM参数。
    """
    def __init__(self):

        self.content_id = None
        self.streaming_mode = None
        self.encrypt_audio = None
        self.emi = None
        self.drm_list = None

    def _deserialize(self, params):
        self.key = params.get("content_id")
        self.url = params.get("streaming_mode")
        self.iv = params.get("encrypt_audio")
        self.algorithm = params.get("emi")
        self.algorithm = params.get("drm_list")

class Encryption(BaseModel):
    """Encryption 视频加密控制参数
    """
    def __init__(self):
        """
        :param hls_encrypt: HLS视频加密控制参数
        :type hls_encrypt: HlsEncrypt
        """
        self.hls_encrypt = None
        self.multidrm = None
        self.preview_duration = None

    def _deserialize(self, params):
        self.preview_duration = params.get("preview_duration")
        if params.get("hls_encrypt") is not None:
            self.hls_encrypt = HlsEncrypt()
            self.hls_encrypt._deserialize(params.get("hls_encrypt"))
        if params.get("multidrm") is not None:
            self.multidrm = Multidrm()
            self.hls_encrypt._deserialize(params.get("multidrm"))


class VideoProcess(BaseModel):

    def __init__(self):
        """
        :param rotate: 视频顺时针旋转角度
        :type rotate: Integer
        :param adaptation: 长短边自适应控制字段
        :type adaptation: String
        :param upsample: 是否开启上采样
        :type upsample: Integer
        """

        self.rotate = None
        self.adaptation = None
        self.upsample = None

    def _deserialize(self, params):
        self.rotate = params.get("rotate")
        self.adaptation = params.get("adaptation")
        self.upsample = params.get("upsample")


class AudioProcess(BaseModel):

    def __init__(self):
        """
        :param volume: 音量调整方式
        :type volume: String
        :param volume_expr: 音量调整幅值
        :type volume_expr: Integer
        """

        self.volume = None
        self.volume_expr = None

    def _deserialize(self, params):
        self.volume = params.get("volume")
        self.volume_expr = params.get("volume_expr")


class QualityEnhance(BaseModel):

    def __init__(self):
        """
        :param normal_enhance: 针对一般质量、无明显问题的普通片源，通过增强、锐化等技术明显提升主观效果。单纯该处理操作前后，分辨率、帧率等参数不发生变化
        :type normal_enhance: String
        """

        self.normal_enhance = None
        self.revive = None
        self.sdr_to_hdr = None

    def _deserialize(self, params):
        self.normal_enhance = params.get("normal_enhance")
        self.revive = params.get("revive")
        self.sdr_to_hdr = params.get("sdr_to_hdr")

class DigitalWatermark(BaseModel):

    def __init__(self):
        """
        :param profile: 水印鲁棒性
        :type profile: String
        """

        self.profile = None

    def _deserialize(self, params):
        self.profile = params.get("profile")


class AudioTrackInfo(BaseModel):

    def __init__(self):
        """
        :param channel_layout: 音频轨的声道layout
        :type channel_layout: String
        :param language: 音频轨对应语言描述
        :type language: String
        """

        self.channel_layout = None
        self.language = None

    def _deserialize(self, params):
        self.channel_layout = params.get("channel_layout")
        self.language = params.get("language")


class AudioFile(BaseModel):

    def __init__(self):
        """
        :param input: 独立音频文件地址
        :type input: ObsInfo
        :param tracks_info: 文件中，各个音频轨信息
        :type tracks_info: Array of AudioTrackInfo
        """

        self.input = None
        self.tracks_info = None

    def _deserialize(self, params):
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("tracks_info") is not None:
            self.tracks_info = []
            for item in params.get("tracks_info"):
                obj = AudioTrackInfo()
                obj._deserialize(item)
                self.tracks_info.append(obj)


class MultiAudio(BaseModel):

    def __init__(self):
        """
        :param tracks_info: 源文件中（即请求参数中的input输入文件），各个音频轨信息
        :type tracks_info: Array of AudioTrackInfo
        :param audio_files: 独立音频文件参数
        :type audio_files: Array of AudioFile
        :param default_language: 默认语言
        :type default_language: String
        """

        self.tracks_info = None
        self.audio_files = None
        self.default_language = None


    def _deserialize(self, params):
        self.priority = params.get("priority")
        if params.get("tracks_info") is not None:
            self.tracks_info = []
            for item in params.get("tracks_info"):
                obj = AudioTrackInfo()
                obj._deserialize(item)
                self.tracks_info.append(obj)
        if params.get("audio_files") is not None:
            self.audio_files = []
            for item in params.get("audio_files"):
                obj = AudioFile()
                obj._deserialize(item)
                self.audio_files.append(obj)


class Crop(BaseModel):

    def __init__(self):
        """
        :param duration: 截取的视频时长，从0秒开始算起
        :type duration: Integer
        """
        self.duration = None

    def _deserialize(self, params):
        self.duration = params.get("duration")

class AudioTrack(BaseModel):

    def __init__(self):
        """
        :param type: 音轨选取方式
        :type type: Integer
        :param left: 选取左声道所在的音轨编号
        :type left: Integer
        :param right: 选取右声道所在的音轨编号
        :type right: Integer
        """

        self.type = None
        self.left = None
        self.right = None

    def _deserialize(self, params):
        self.type = params.get("type")
        self.left = params.get("left")
        self.right = params.get("right")


class SystemProcess(BaseModel):
    def __init__(self):
        self.hls_index = None
        self.dash_index = None

    def _deserialize(self, params):
        if params.get("hls_index") is not None:
            self.hls_index = ObsInfo()
            self.hls_index._deserialize(params.get("hls_index"))

class CreateTranscodeTaskRequest(BaseModel):
    """CreateTranscodeTask 创建转码任务请求参数结构体

    """

    def __init__(self):
        """
        :param input: 源文件地址
        :type input: ObsInfo
        :param output: 输出文件地址
        :type output: ObsInfo
        :param priority: 任务优先级，取值范围[1,9]，9代表最高优先级，目前只支持6和9
        :type priority: Int
        :param trans_template_id: 转码模板ID
        :type trans_template_id: list of int
        :param thumbnail: 抽帧截图参数
        :type thumbnail: Thumbnail
        :param watermarks: 图片水印参数
        :type watermarks: list of Watermark
        :param audit: 内容质检参数
        :type audit: Audit
        :param subtitle: 字幕参数
        :type subtitle: Subtitle
        :param output_filenames: 输出文件名称,每一路转码输出对应一个名称，且需和转码
                                 模板ID按数组顺序一一对应。若设置该参数，表示输出文件
                                 按该参数命名；若不设置该参数，表示输出文件按默认方式命名
        :type output_filenames: list of str

        :param av_parameters: 音视频参数
        :type av_parameters : list of AvParameter
        :param encryption: 视频加密控制参数
        :type encryption : Encryption
        :param video_process: 视频处理参数
        :type video_process : VideoProcess
        :param audio_process: 音频处理参数
        :type audio_process : AudioProcess
        :param quality_enhance: 画质增强参数
        :type quality_enhance : QualityEnhance
        :param digital_watermark: 数字水印属性
        :type digital_watermark : DigitalWatermark
        :param multi_audio: 音频多语言多声道参数设置
        :type multi_audio : MultiAudio
        :param crop: 截取前多少秒进行转码
        :type crop : Crop
        :param audio_track: 音轨参数
        :type audio_track : AudioTrack

        """
        self.input = None
        self.output = None
        self.priority = None
        self.trans_template_id = None
        self.thumbnail = None
        self.watermarks = None
        self.audit = None
        self.subtitle = None
        self.output_filenames = None
        self.av_parameters = None
        self.encryption = None
        self.video_process = None
        self.audio_process = None
        self.quality_enhance = None
        self.digital_watermark = None
        self.multi_audio = None
        self.crop = None
        self.audio_track = None
        self.system_process = None

    def _deserialize(self, params):
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        self.priority = params.get("priority")
        self.trans_template_id = params.get("trans_template_id")
        if params.get("thumbnail") is not None:
            self.thumbnail = Thumbnail()
            self.thumbnail._deserialize(params.get("thumbnail"))
        if params.get("watermarks") is not None:
            self.watermarks = []
            for item in params.get("watermarks"):
                obj = Watermark()
                obj._deserialize(item)
                self.watermarks.append(obj)
        if params.get("audit") is not None:
            self.audit = Audit()
            self.audit._deserialize(params.get("audit"))
        if params.get("subtitle") is not None:
            self.subtitle = Subtitle()
            self.subtitle._deserialize(params.get("subtitle"))
        self.output_filenames = params.get("output_filenames")

        if params.get("av_parameters") is not None:
            self.av_parameters = []
            for item in params.get("av_parameters"):
                obj = AvParameter()
                obj._deserialize(item)
                self.av_parameters.append(obj)
        if params.get("encryption") is not None:
            self.encryption = Encryption()
            self.encryption._deserialize(params.get("encryption"))
        if params.get("thumbnail") is not None:
            self.thumbnail = Thumbnail()
            self.thumbnail._deserialize(params.get("thumbnail"))
        if params.get("video_process") is not None:
            self.video_process = VideoProcess()
            self.video_process._deserialize(params.get("video_process"))
        if params.get("audio_process") is not None:
            self.audio_process = AudioProcess()
            self.audio_process._deserialize(params.get("audio_process"))
        if params.get("quality_enhance") is not None:
            self.quality_enhance = QualityEnhance()
            self.quality_enhance._deserialize(params.get("quality_enhance"))
        if params.get("digital_watermark") is not None:
            self.digital_watermark = DigitalWatermark()
            self.digital_watermark._deserialize(params.get("digital_watermark"))
        if params.get("multi_audio") is not None:
            self.multi_audio = MultiAudio()
            self.multi_audio._deserialize(params.get("multi_audio"))
        if params.get("crop") is not None:
            self.crop = Crop()
            self.crop._deserialize(params.get("crop"))
        if params.get("audio_track") is not None:
            self.audio_track = AudioTrack()
            self.audio_track._deserialize(params.get("audio_track"))
        if params.get("system_process") is not None:
            self.system_process = SystemProcess()
            self.system_process._deserialize(params.get("system_process"))


class CreateBatchTranscodeTaskResponse(BaseModel):
    """CreateBatchTranscodeTaskResponse 创建任务返回参数结构体

    """

    def __init__(self):
        """
        :param task_array:
        :type task_array: list of CreateTaskResponse

        """
        self.task_array = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("task_array") is not None:
            self.task_array = []
            for item in params.get("task_array"):
                obj = CreateTaskResponse()
                obj._deserialize(item)
                self.task_array.append(obj)


class CreateTaskResponse(BaseResponse):
    """CreateTaskResponse 创建任务返回参数结构体

    """
    def __init__(self):
        """
        :param task_id: 唯一任务标识ID，创建成功时返回。
        :type task_id: Int

        """
        BaseResponse.__init__(self)
        self.task_id = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        self.task_id = params.get("task_id")


class QueryTaskDetailRequest(BaseModel):
    """QueryTaskDetailRequest 查询任务请求参数结构体

    """

    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: list of str

        """
        self.task_id = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")


class QueryTaskRequest(BaseModel):
    """QueryTaskRequest 查询任务请求参数结构体

    """

    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: list of str
        :param status: 任务执行状态
        :type status: str
        :param start_time: 起始时间，格式为yyyymmddhhmmss。必须是与时区无关的UTC时间。
        :type start_time: str
        :param end_time: 结束时间。格式为yyyymmddhhmmss。必须是与时区无关的UTC时间。
        :type end_time: str
        :param page: 分页编号，默认为0。指定task_id时该参数无效。
        :type page: Int
        :param size: 每页记录数。默认10，范围[1,100]。指定task_id时该参数无效。
        :type size: Int

        """
        self.task_id = None
        self.status = None
        self.start_time = None
        self.end_time = None
        self.page = None
        self.size = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.start_time = params.get("start_time")
        self.end_time = params.get("end_time")
        self.page = params.get("page")
        self.size = params.get("size")


class QueryTaskResponse(BaseResponse):
    """QueryTaskResponse 查询任务返回参数结构体

    """

    def __init__(self):
        """
        :param is_truncated: 查询结果是否被截取，0: 未被截取，即所有结果已被返回
                             1: 被截取，即还有结果未被返回，可以通过设置page和size参数继续查询
        :type is_truncated: Int
        :param task_array: 具体的转码任务查询结果的列表
        :type task_array: list of TaskInfo
        :param total: 满足除page和size之外的输入的查询条件的所有结果的数量
        :type total: long int

        """
        BaseResponse.__init__(self)
        self.is_truncated = None
        self.task_array = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        self.is_truncated = params.get("is_truncated")
        if params.get("task_array") is not None:
            self.task_array = []
            for item in params.get("task_array"):
                obj = TaskInfo()
                obj._deserialize(item)
                self.task_array.append(obj)
        self.total = params.get("total")

class QueryThumbTaskResponse(BaseResponse):
    """QueryThumbTaskResponse 查询截图任务返回参数结构体

    """

    def __init__(self):
        """
        :param is_truncated: 查询结果是否被截取，0: 未被截取，即所有结果已被返回
                             1: 被截取，即还有结果未被返回，可以通过设置page和size参数继续查询
        :type is_truncated: Int
        :param task_array: 截图任务查询结果数组
        :type task_array: list of ThumbTask
        :param total: 截图任务查询结果总数
        :type total: long int

        """
        BaseResponse.__init__(self)
        self.is_truncated = None
        self.task_array = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        self.is_truncated = params.get("is_truncated")
        if params.get("task_array") is not None:
            self.task_array = []
            for item in params.get("task_array"):
                obj = ThumbTask()
                obj._deserialize(item)
                self.task_array.append(obj)
        self.total = params.get("total")

class ThumbTask(BaseResponse):
    """ThumbTask 截图任务查询结果

    """

    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: str
        :param status: 任务状态
        :type status: str
        :param create_time: 任务创建时间
        :type create_time: str
        :param end_time: 任务结束时间
        :type end_time: str
        :param description: 任务描述，如当任务异常时，此字段为异常的具体信息
        :type description: str
        :param input: 源文件信息
        :type input: ObsInfo
        :param output: 抽帧任务的输出信息
        :type output: ObsInfo
        :param thumbnail_info: 截图文件信息
        :type thumbnail_info: list of str
        :param output_file_name: 生成的截图文件的名称
        :type output_file_name: list of str
        """

        self.task_id = None
        self.status = None
        self.create_time = None
        self.end_time = None
        self.input = None
        self.output = None
        self.description = None
        self.thumbnail_info = None
        self.output_file_name = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.create_time = params.get("create_time")
        self.end_time = params.get("end_time")
        self.description = params.get("description")
        self.thumbnail_info = params.get("thumbnail_info")
        self.thumbnail_info = params.get("output_file_name")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))


class QueryExtractTaskResponse(BaseResponse):
    """QueryExtractTaskResponse 查询解析任务返回参数结构体

    """

    def __init__(self):
        """
        :param tasks: 任务信息
        :type tasks: list of ExtractTask
        :param total: 任务数量
        :type total: int

        """
        BaseResponse.__init__(self)
        self.tasks = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("tasks") is not None:
            self.tasks = []
            for item in params.get("tasks"):
                obj = ExtractTask()
                obj._deserialize(item)
                self.tasks.append(obj)
        self.total = params.get("total")


class EachEncryptRsp(BaseResponse):
    """ExtractTask 查询单个加密任务返回参数结构体
        """

    def __init__(self):
        self.task_id = None
        self.status = None
        self.create_time = None
        self.start_time = None
        self.end_time = None
        self.input = None
        self.output = None
        self.description = None
        self.output_file_name = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.create_time = params.get("create_time")
        self.start_time = params.get("start_time")
        self.end_time = params.get("end_time")
        self.description = params.get("description")
        self.output_file_name = params.get("output_file_name")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))

class QueryEncryptTaskResponse(BaseResponse):
    """QueryEncryptTaskResponse 查询加密任务返回参数结构体
    """

    def __init__(self):
        BaseResponse.__init__(self)
        self.task_array = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("task_array") is not None:
            self.task_array = []
            for item in params.get("task_array"):
                obj = EachEncryptRsp()
                obj._deserialize(item)
                self.task_array.append(obj)
        self.total = params.get("total")

class AnimatedGraphicsTask(BaseResponse):
    def __init__(self):

        self.task_id = None
        self.status = None
        self.create_time = None
        self.start_time = None
        self.end_time = None
        self.input = None
        self.output = None
        self.description = None
        self.animatedGraphicsOutputParam = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.create_time = params.get("create_time")
        self.start_time = params.get("start_time")
        self.end_time = params.get("end_time")
        self.description = params.get("description")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("output_param") is not None:
            self.animatedGraphicsOutputParam = AnimatedGraphicsOutputParam()
            self.animatedGraphicsOutputParam._deserialize(params.get("output_param"))

class QueryAnimatedGraphicsTaskResponse(BaseResponse):

    def __init__(self):
        BaseResponse.__init__(self)
        self.tasks = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("tasks") is not None:
            self.tasks = []
            for item in params.get("tasks"):
                obj = AnimatedGraphicsTask()
                obj._deserialize(item)
                self.tasks.append(obj)
        self.total = params.get("total")

class QueryRemuxTaskResponse(BaseResponse):
    """QueryRemuxTaskResponse 查询转封装任务返回参数结构体

    """

    def __init__(self):
        """
        :param tasks: 任务信息
        :type tasks: list of RemuxTask
        :param total: 任务数量
        :type total: int

        """
        BaseResponse.__init__(self)
        self.tasks = None
        self.total = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("tasks") is not None:
            self.tasks = []
            for item in params.get("tasks"):
                obj = RemuxTask()
                obj._deserialize(item)
                self.tasks.append(obj)
        self.total = params.get("total")

class RemuxTask(BaseResponse):
    """RemuxTask 查询单个转封装任务返回参数结构体
    """

    def __init__(self):

        self.task_id = None
        self.status = None
        self.create_time = None
        self.start_time = None
        self.end_time = None
        self.input = None
        self.output = None
        self.description = None
        self.RemuxOutputParam = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.create_time = params.get("create_time")
        self.start_time = params.get("start_time")
        self.end_time = params.get("end_time")
        self.description = params.get("description")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("output_param") is not None:
            self.RemuxOutputParam = RemuxOutputParam()
            self.RemuxOutputParam._deserialize(params.get("output_param"))

class ExtractTask(BaseResponse):
    """ExtractTask 查询单个解析任务返回参数结构体
    """

    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: str
        :param status: 任务状态
        :type status: str
        :param create_time: 任务创建时间
        :type create_time: str
        :param start_time: 任务启动时间，指任务排完对正式开始执行的时间
        :type start_time: str
        :param end_time: 任务结束时间
        :type end_time: str
        :param description: 任务描述，如当任务异常时，此字段为异常的具体信息
        :type description: str
        :param input: 源文件信息
        :type input: ObsInfo
        :param output: 抽帧任务的输出信息
        :type output: ObsInfo
        :param metadata: 抽帧任务的输出信息
        :type metadata: MetaData

        """
        self.task_id = None
        self.status = None
        self.create_time = None
        self.start_time = None
        self.end_time = None
        self.input = None
        self.output = None
        self.description = None
        self.metadata = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")
        self.status = params.get("status")
        self.create_time = params.get("create_time")
        self.start_time = params.get("start_time")
        self.end_time = params.get("end_time")
        self.description = params.get("description")
        if params.get("input") is not None:
            self.input = ObsInfo()
            self.input._deserialize(params.get("input"))
        if params.get("output") is not None:
            self.output = ObsInfo()
            self.output._deserialize(params.get("output"))
        if params.get("metadata") is not None:
            self.metadata = MetaData()
            self.metadata._deserialize(params.get("metadata"))

class MetaData(BaseModel):
    """MetaData metadata参数结构体
    """
    def __init__(self):
        """
        :param size: 文件大小
        :type size: int
        :param duration: 视频时长,单位：秒
        :type duration: int
        :param format: 文件封装格式
        :type format: str
        :param bitrate: 总码率
        :type bitrate: int
        :param video: 视频流元数据
        :type video: VideoInfo
        :param audio: 视频流元数据
        :type audio: AudioInfo

        """

        self.size = None
        self.duration = None
        self.format = None
        self.bitrate = None
        self.video = None
        self.audio = None

    def _deserialize(self, params):
        self.size = params.get("size")
        self.duration = params.get("duration")
        self.format = params.get("format")
        self.bitrate = params.get("bitrate")
        if params.get("video") is not None:
            self.video = VideoInfo()
            self.video._deserialize(params.get("video"))
        if params.get("audio") is not None:
            self.audio = AudioInfo()
            self.audio._deserialize(params.get("audio"))

class QueryTaskDetailResponse(BaseResponse):
    """QueryTaskDetailResponse 查询任务返回参数结构体

    """

    def __init__(self):
        """
        :param task_array: 具体的转码任务查询结果的列表
        :type task_array: list of TaskInfo

        """
        BaseResponse.__init__(self)
        self.task_array = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("task_array") is not None:
            self.task_array = []
            for item in params.get("task_array"):
                obj = TaskDetailInfo()
                obj._deserialize(item)
                self.task_array.append(obj)


class QueryTaskDetailResponse(BaseResponse):
    """QueryTaskDetailResponse 查询任务返回参数结构体

    """

    def __init__(self):
        """
        :param task_array: 具体的转码任务查询结果的列表
        :type task_array: list of TaskInfo

        """
        BaseResponse.__init__(self)
        self.task_array = None

    def _deserialize(self, params):
        BaseResponse._deserialize(self, params)
        if params.get("task_array") is not None:
            self.task_array = []
            for item in params.get("task_array"):
                obj = TaskDetailInfo()
                obj._deserialize(item)
                self.task_array.append(obj)


class DeleteTaskRequest(BaseModel):
    """DeleteTaskRequest 删除任务请求参数结构体

    """

    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: Int

        """
        self.task_id = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")

class DeleteStrTaskRequest(BaseModel):
    """DeleteTaskRequest 删除任务请求参数结构体

    """

    def __init__(self):
        """
        :param task_id: 任务ID
        :type task_id: str

        """
        self.task_id = None

    def _deserialize(self, params):
        self.task_id = params.get("task_id")








