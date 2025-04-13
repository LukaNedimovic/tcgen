from typing import List

from .char import char
from .dtype import dtype


class str(dtype):
    """
    Class containing the implementation of a string.
    """

    min = None
    max = None

    def __init__(
        self, val=None, signed: bool = False, rand: bool = False, len: int = 32
    ):
        """
        Instantiate a string.
        """
        if super()._is_same_class(self, val):
            super()._deepcopy(self, val)
            return

        super().__init__(val, signed=signed)

        str.min = 0
        str.max = 255

        self.val: List[char] = []
        self.len = len

        if val is not None:
            for c in val:
                self.val.append(char(c))

        if rand:
            self.val = self._rand()

    def _rand(self):
        return [char(rand=True) for _ in range(self.len)]

    def __str__(self):
        return "".join(c.__str__() for c in self.val)

    def __add__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '+' for dtypes: {dtype1, dtype2}")

        print(self.val)
        print(other.val)
        print(self.val + other.val)

        return res_dtype(self.val + other.val)
