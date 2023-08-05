import collections
import functools

import numpy as np

from garnett.trajectory import *
from garnett.trajectory import Trajectory as GarnettTrajectory
from garnett.trajectory import Frame as GarnettFrame

_FRAME_OVERRIDES = {
    '_garnett_frame',
}

class Frame:
    def __init__(self, garnett_frame):
        self._garnett_frame = garnett_frame

    def __getattr__(self, name):
        if name == 'types':
            type_names = self._garnett_frame.types
            result = [type_names[i] for i in self._garnett_frame.typeid]
            return result
        elif name == 'type_names':
            return self._garnett_frame.types
        elif name in _FRAME_OVERRIDES:
            return super().__getattr__(name)

        return getattr(self._garnett_frame, name)

    def __setattr__(self, name, value):
        if name == 'types':
            type_map = collections.defaultdict(lambda: len(type_map))
            typeids = [type_map[t] for t in value]
            type_names = list(type_map)
            self._garnett_frame.typeid = typeids
            self._garnett_frame.types = type_names
            return
        elif name == 'type_names':
            return
        elif name in _FRAME_OVERRIDES:
            return super().__setattr__(name, value)

        return setattr(self._garnett_frame, name, value)

class Trajectory:
    def __init__(self, traj):
        self._garnett_trajectory = traj

    def __getattr__(self, name):
        if name == '_garnett_trajectory':
            return super().__getattr__(name)

        return getattr(self._garnett_trajectory, name)

    def __setattr__(self, name, value):
        if name == '_garnett_trajectory':
            return super().__setattr__(name, value)

        setattr(self._garnett_trajectory, name, value)

    def __iter__(self):
        for frame in self._garnett_trajectory:
            yield Frame(frame)

    def __getitem__(self, index):
        frame_or_frames = self._garnett_trajectory[index]
        try:
            # slice
            return map(Frame, frame_or_frames)
        except TypeError: # index
            return Frame(frame_or_frames)
