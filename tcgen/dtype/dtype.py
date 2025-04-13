class dtype:
    """
    Base class for data type implementation.
    """

    def __init__(self, val=None, signed: bool = True):
        self.val = val
        self.signed = signed

    def __str__(self):
        return f"{self.val}"

    def __repr__(self):
        return f"(val={self.val}, dtype=tcgen.{self.__class__.__name__})"

    def __add__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '+' for dtypes: {dtype1, dtype2}")

        return res_dtype(self.val + other.val)

    def __sub__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '-' for dtypes: {dtype1, dtype2}")

        return res_dtype(self.val - other.val)

    def __mul__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '*' for dtypes: {dtype1, dtype2}")

        return res_dtype(self.val * other.val)

    def __truediv__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '//' for dtypes: {dtype1, dtype2}")

        return res_dtype(self.val // other.val)

    def __floordiv__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '/' for dtypes: {dtype1, dtype2}")

        return res_dtype(self.val / other.val)

    def __mod__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '%' for dtypes: {dtype1, dtype2}")

        return res_dtype(self.val % other.val)

    def __pow__(self, other):
        dtype1, dtype2 = self.__class__, other.__class__
        res_dtype = self._promote(dtype1, dtype2)
        if res_dtype is None:
            raise ValueError(f"Cannot perform '+' for dtypes: {dtype1, dtype2}")

        return res_dtype(self.val**other.val)

    def __eq__(self, other):
        return self.val == other.val and self.__class__ == other.__class__

    def __lt__(self, other):
        return self.val < other.val

    def __le__(self, other):
        return self.val <= other.val

    def __gt__(self, other):
        return self.val > other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __neg__(self):
        return -self.val

    def __pos__(self):
        return +self.val

    def _promote(self, dtype1, dtype2):
        from .prom import _prom

        return _prom.get((dtype1, dtype2), None)

    @staticmethod
    def is_class(cls):
        return isinstance(cls, type)

    @staticmethod
    def is_dtype(type):
        return dtype.is_class(type) and (type == dtype or issubclass(type, dtype))

    @staticmethod
    def rand(dtype_):
        return dtype_._rand()
