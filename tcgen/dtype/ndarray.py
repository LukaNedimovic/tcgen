from typing import Any, List

from .dtype import dtype
from .int32 import int32


class ndarray(dtype):
    """
    Class containing the implementation of an array.
    """

    min = None
    max = None

    def __init__(
        self, val=None, elem_type=int32, signed=True, rand: bool = False, len: int = 5
    ):
        """
        Instantiate an array of `elem_type` elements.
        """

        if super()._is_same_class(self, val):
            super()._deepcopy(self, val)
            return

        super().__init__(val, signed=signed)

        ndarray.min = elem_type.min
        ndarray.max = elem_type.max

        self.val: List[Any] = []
        self.len = len
        self.type = elem_type

        if val is not None:
            for elem in val:
                self.val.append(elem_type(elem))

        if rand:
            self.val = self._rand()

    def _rand(self):
        return [self.type(rand=True) for _ in range(self.len)]

    def __str__(self):
        return "[" + ", ".join(str(elem) for elem in self.val) + "]"
