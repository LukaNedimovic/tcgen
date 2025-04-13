import random

from .dtype import dtype


class char(dtype):
    """
    Class containing the implementation of a char.
    """

    min = None
    max = None

    def __init__(self, val=None, signed: bool = False, rand: bool = False):
        """
        Instantiate a single char.
        """
        super().__init__(val, signed=signed)

        char.min = 0
        char.max = 255

        if rand:
            self.val = self._rand()

    def _rand(self):
        return random.randint(char.min, char.max)

    def __str__(self):
        return chr(self.val)
