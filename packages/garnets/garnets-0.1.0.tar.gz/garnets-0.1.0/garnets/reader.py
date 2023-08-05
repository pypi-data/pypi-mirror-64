
import contextlib

import garnett

from .trajectory import Trajectory

def _ReaderDecorator(cls):
    class DecoratedReader(cls):
        def read(self, *args, **kwargs):
            return Trajectory(super().read(*args, **kwargs))

    return DecoratedReader

READER_NAMES = [
    'PosFileReader',
    'HOOMDXMLFileReader',
    'DCDFileReader',
    'GSDHOOMDFileReader',
    'GetarFileReader',
    'CifFileReader',
]

for name in READER_NAMES:
    decorated = _ReaderDecorator(getattr(garnett.reader, name))
    globals()[name] = decorated

@contextlib.contextmanager
def read(*args, **kwargs):
    with garnett.read(*args, **kwargs) as traj:
        yield Trajectory(traj)
