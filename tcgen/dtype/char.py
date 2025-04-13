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

        # In case of character being provided,
        # convert it to its integer value
        if isinstance(val, str):
            if len(val) != 1:
                raise ValueError(f"Cannot wrap more than one character: {val}")
            val = ord(val)

        super().__init__(val, signed=signed)

        char.min = 0
        char.max = 255

        if rand:
            self.val = self._rand()

    def _rand(self):
        return random.randint(char.min, char.max)

    def __str__(self):
        return chr(self.val)
