# -*- coding: utf-8 -*-
"""
tts streaming client
"""
from __future__ import print_function

import grpc
from . import tts_streaming_pb2
from . import tts_streaming_pb2_grpc


class TtsClient(object):
    """ version modify log,
    from version 1.0.7: change init method, move product_id and enable_flush_data to be must params;
    """

    request = tts_streaming_pb2.TtsFragmentRequest()

    def __init__(self, server_ip, port, per,
                 lan="zh",
                 ctp=10,
                 aue=3,
                 pdt=993,
                 cuid="xxx",
                 vol=5,
                 pit=5,
                 spd=5):
        self.server_ip = server_ip
        self.port = port
        self.host = server_ip + ":" + port
        # 说话人
        self.request.per = per
        # 语言选择，只支持zh
        self.request.lan = lan
        # 流式识别默认为10
        self.request.ctp = ctp
        # 输出格式，默认为3，MP3;4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k）;
        # 注意aue=4，5，6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
        self.request.aue = aue
        # 默认993
        self.request.pdt = pdt
        # 用户唯一标识，用来区分用户，可以填写机器 MAC 地址，长度为60以内
        self.request.cuid = cuid
        # 音量，取值0-15，默认为5中音量
        self.request.vol = vol
        # 音调，取值0-15，默认为5中语调
        self.request.pit = pit
        # 语速，取值0-15，默认为5中语速
        self.request.spd = spd

    def get_result(self, tex):
        """
        通过文件路径获取最终解码结果的迭代器
        :param file_path:
        :return: response的迭代
        """

        # 添加ca认证
        # with open(
        #         '/path/of/xxx.crt',
        #         'rb') as f:
        #     creds = grpc.ssl_channel_credentials(f.read())
        # with grpc.secure_channel(self.host, creds) as channel:

        with grpc.insecure_channel(target=self.host, options=[('grpc.keepalive_timeout_ms', 1000000), ]) as channel:
            stub = tts_streaming_pb2_grpc.TtsServiceStub(channel)
            self.request.tex = tex
            responses = stub.getAudio(self.request, timeout=100000)
            for response in responses:
                yield response