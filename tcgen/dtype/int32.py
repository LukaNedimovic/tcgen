import random

from .dtype import dtype


class int32(dtype):
    """
    Class containing the implementation of a 32-bit integer.
    """

    min = None
    max = None

    def __init__(self, val=None, signed: bool = True, rand: bool = False):
        """
        Instantiate a single 32-bit integer.
        """
        if super()._is_same_class(self, val):
            super()._deepcopy(self, val)
            return

        super().__init__(val, signed=signed)

        bits = 32
        if signed:
            int32.min = -(2 ** (bits - 1))
            int32.max = (2 ** (bits - 1)) - 1
        else:
            int32.min = 0
            int32.max = (2**bits) - 1

        if rand:
            self.val = self._rand()

    def _rand(self):
        return random.randint(int32.min, int32.max)
