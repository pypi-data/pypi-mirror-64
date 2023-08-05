# -*- coding: utf-8 -*-
"""
test module for reading in stream
"""

import unittest.mock as mock
import cv2
from sail_utils.cv.frame import LiveStreamer


@mock.patch("time.time", return_value="150000")
@mock.patch("cv2.VideoCapture")
def test_live_streamer_init(mocked_video, mocked_time):
    """
    test live streamer construction
    :param mocked_video:
    :param mocked_time:
    :return:
    """
    streamer = LiveStreamer(source="test_stream",
                            rate=15)

    assert mocked_time() == streamer.current_time
    assert mocked_video is cv2.VideoCapture
    assert streamer.rate == 15
