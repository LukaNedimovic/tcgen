import pytest

from tcgen.dtype import int32


@pytest.mark.parametrize(
    "val, exp",
    [
        (1, int32(1)),
        (5, int32(5)),
        (-1, int32(-1)),
    ],
)
def test_conv(val, exp):
    assert int32(val) == exp
