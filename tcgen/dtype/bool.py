import random

from .dtype import dtype


class bool(dtype):
    """
    Class containing the implementation of boolean datatype.
    """

    min = None
    max = None

    def __init__(self, val=None, signed=True, rand=False):
        """
        Instantiate a single 32-bit integer.
        """

        # In case of True or False being provided,
        # convert it to 1 or 0, respectably
        if type(val) is bool:
            val = int(val)

        super().__init__(val, signed=signed)

        bool.min = 0
        bool.max = 1

        if rand:
            self.val = self._rand()

    def _rand(self):
        return random.randint(bool.min, bool.max)

    def __str__(self):
        return "True" if self.val else "False"
