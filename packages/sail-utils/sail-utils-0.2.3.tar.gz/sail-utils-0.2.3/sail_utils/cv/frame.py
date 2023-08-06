# -*- coding: utf-8 -*-
"""
module for reading in stream
"""

import glob
import time
from pathlib import Path

import cv2


class LiveStreamer:
    """
    class for read from a live feed
    """

    def __init__(self, source: str, rate: int, max_errors: int = 3600):
        self._stream = cv2.VideoCapture(source)
        self._current_time = time.time()
        self._rate = rate
        self._error_frames = 0
        self._max_errors = max_errors

    @property
    def rate(self) -> int:
        """
        get snapshot frequency
        :return:
        """
        return self._rate

    @property
    def current_time(self) -> float:
        """
        get current snapshot time
        :return:
        """
        return self._current_time

    @property
    def stream(self) -> cv2.VideoCapture:
        """
        get live stream
        :return:
        """
        return self._stream

    @property
    def max_errors_allowed(self) -> int:
        """
        get number of max errors allowed
        :return:
        """
        return self._max_errors

    def __iter__(self):
        return self

    def __next__(self):
        while self._stream.isOpened():
            ret, frame = self._stream.read()
            if ret:
                self._error_frames = 0
                next_time = time.time()
                elapsed = next_time - self._current_time
                if elapsed >= 1. / self._rate:
                    self._current_time = next_time
                    return frame, next_time
            else:
                self._error_frames += 1
                if self._error_frames >= self._max_errors:
                    raise StopIteration("# of error is greater than allowed. stop stream")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            raise StopIteration("stream is closed")

    def __del__(self):
        self._stream.release()


class ImageFileStreamer:
    """
    class for read from a folders file
    """

    def __init__(self, source, suffix: str = 'jpg', rate: int = 1):
        self._source = Path(source)
        self._files = glob.glob((self._source / ("**" + suffix)).as_posix(), recursive=True)
        self._files = sorted(self._files, key=lambda x: (len(x), x))
        self._rate = rate
        self._start = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._start >= len(self._files):
            raise StopIteration()

        file_loc = self._files[self._start]
        self._start += self._rate
        img = cv2.imread(file_loc, cv2.IMREAD_COLOR)
        return img, file_loc
