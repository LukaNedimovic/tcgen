from .bool import bool
from .char import char
from .int32 import int32
from .int64 import int64
from .str import str

_prom = {
    # int32
    (int32, int32): int32,
    (int32, int64): int64,
    (int32, bool): int32,
    (int32, char): int32,
    (int32, str): str,
    # int64
    (int64, bool): int64,
    (int64, char): char,
    (int64, str): str,
    # bool
    (bool, bool): bool,
    (bool, char): char,
    (bool, str): str,
    # char
    (char, char): char,
    (char, str): str,
    # str
    (str, str): str,
}
# Add the keys in opposite way
# Example: (int32, int64) -> (int64, int32)
prom_rev = {
    (dtypes[1], dtypes[0]): prom_val
    for dtypes, prom_val in _prom.items()
    if dtypes[0] != dtypes[1]
}
_prom.update(prom_rev)  # type: ignore[arg-type]
