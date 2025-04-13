import random

from .dtype import dtype


class int64(dtype):
    """
    Class containing the implementation of a 64-bit integer.
    """

    min = None
    max = None

    def __init__(self, val=None, signed: bool = True, rand: bool = False):
        super().__init__(val, signed=signed)

        bits = 64
        if signed:
            int64.min = -(2 ** (bits - 1))
            int64.max = (2 ** (bits - 1)) - 1
        else:
            int64.min = 0
            int64.max = (2**bits) - 1

        if rand:
            self.val = self._rand()

    def _rand(self):
        return random.randint(int64.min, int64.max)
