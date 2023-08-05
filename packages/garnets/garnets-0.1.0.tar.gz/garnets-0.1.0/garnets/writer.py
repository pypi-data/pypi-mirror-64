
import garnett

from .trajectory import Trajectory

def _WriterDecorator(cls):
    class DecoratedWriter(cls):
        def write(self, trajectory, *args, **kwargs):
            try:
                trajectory = trajectory._garnett_trajectory
            except AttributeError:
                pass
            return self.write(trajectory, *args, **kwargs)

    return DecoratedWriter

WRITER_NAMES = [
    'PosFileWriter',
    'CifFileWriter',
    'GSDHOOMDFileWriter',
    'GetarFileWriter',
]

for name in WRITER_NAMES:
    decorated = _WriterDecorator(getattr(garnett.writer, name))
    globals()[name] = decorated

def write(traj, *args, **kwargs):
    trajectory = [getattr(frame, '_garnett_frame', frame) for frame in traj]
    garnett.write(trajectory, *args, **kwargs)
