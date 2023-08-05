import inspect

from typing import List
from typing import Optional

from .frame import Frame
from .frame_collection import FrameCollection


class Inspector:
    def __init__(self, exception: Exception):
        self._exception = exception
        self._frames = None
        self._outer_frames = None
        self._inner_frames = None
        self._previous_exception = exception.__context__

    @property
    def exception(self) -> Exception:
        return self._exception

    @property
    def exception_name(self) -> str:
        return self._exception.__class__.__name__

    @property
    def exception_message(self) -> str:
        return str(self._exception)

    @property
    def frames(self) -> FrameCollection:
        if self._frames is not None:
            return self._frames

        self._frames = FrameCollection(self.outer_frames + self.inner_frames)

        return self._frames

    @property
    def outer_frames(self) -> FrameCollection:
        if self._outer_frames is not None:
            return self._outer_frames

        tb = self._exception.__traceback__

        outer_frames = FrameCollection()
        for frame_info in inspect.getouterframes(tb.tb_frame)[1:]:
            outer_frames.append(Frame(frame_info))

        self._outer_frames = outer_frames

        return self._outer_frames

    @property
    def inner_frames(self) -> FrameCollection:
        if self._inner_frames is not None:
            return self._inner_frames

        tb = self._exception.__traceback__

        inner_frames = FrameCollection()
        for frame_info in inspect.getinnerframes(tb):
            inner_frames.append(Frame(frame_info))

        self._inner_frames = inner_frames

        return self._inner_frames

    @property
    def previous_exception(self) -> Optional[Exception]:
        return self._previous_exception

    def has_previous_exception(self) -> bool:
        return self._previous_exception is not None
