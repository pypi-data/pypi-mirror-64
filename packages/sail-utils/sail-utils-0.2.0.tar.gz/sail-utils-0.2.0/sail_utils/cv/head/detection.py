# -*- coding: utf-8 -*-
"""
detection module
"""

import cv2
import grpc

from sail_utils import LOGGER
from sail_utils.cv.head.config import (
    DEFAULT_TIME_OUT,
    THRESHOLD
)
from sail_utils.cv.head.protobuf import (
    inference_head_detection_pb2,
    inference_head_detection_pb2_grpc
)


def _unary_detect(stub, img, time_out=None):
    request = inference_head_detection_pb2. \
        ObjectDetectionRequest(request_info="called by Python client",
                               model_version=0)
    img_encode = cv2.imencode('.jpg', img)[1]
    request.image_data = img_encode.tobytes()
    response_f = stub.DetectHead.future(request)
    try:
        response = response_f.result(timeout=time_out)
    except grpc.FutureTimeoutError:
        LOGGER.warning(f"grpc <{stub.DetectHead}> time out. just skip")
        rtn_value = []
    else:
        rtn_value = response.objects
    return rtn_value


class _Mapper:

    def __init__(self, src: int, dst: int):
        self._src = src
        self._dst = dst
        LOGGER.info(f"mapper from <{self._src}> to <{self._dst}>")

    def resize(self, img):
        """
        resize pic to destination size
        :param img:
        :return:
        """
        return cv2.resize(img, (self._dst, self._dst), interpolation=cv2.INTER_AREA)

    def __call__(self, bbox):
        scale = self._src / self._dst
        return [
            int(bbox[0] * scale),
            int(bbox[1] * scale),
            int(bbox[2] * scale),
            int(bbox[3] * scale),
        ]

    def __str__(self):
        return f"source: <{self._src} - destination: <{self._dst}>"


def _format(resp, epoch: int, threshold: float, calibrator: _Mapper):
    results = []
    for i, res in enumerate(resp):
        if res.score >= threshold:
            box = res.box
            xmin = box.xmin
            ymin = box.ymin
            xmax = box.xmax
            ymax = box.ymax
            score = res.score

            results.append(
                dict(
                    id=i + 1,
                    location=calibrator([int(xmin), int(ymin), int(xmax), int(ymax)]),
                    time_stamp=epoch,
                    score=score
                )
            )
    return sorted(results, key=lambda x: x['time_stamp'])


class Detector:
    """
    class for detection functionality
    """

    def __init__(self,
                 server: str,
                 src_size: int,
                 dst_size: int = 416,
                 threshold: float = THRESHOLD,
                 timeout: float = DEFAULT_TIME_OUT):
        self._server = server
        self._threshold = threshold
        self._mapper = _Mapper(src_size, dst_size)
        self._timeout = timeout
        LOGGER.info(f"detector at: <{self._server}> with threshold <{self._threshold:.2f}>")

    def detect(self, img, epoch):
        """
        detect on one image
        :param img:
        :param epoch:
        :return:
        """
        img = self._mapper.resize(img)
        with grpc.insecure_channel(self._server) as channel:
            stub = inference_head_detection_pb2_grpc.HeadDetectionStub(channel)
            resp = _unary_detect(stub, img, self._timeout)
            return _format(resp, epoch, self._threshold, self._mapper)

    def __str__(self):
        return f"mapper: {self._mapper}\nserver: {self._server}"
