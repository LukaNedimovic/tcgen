from .dtype import dtype as tcgen_dtype


def rand(dtype) -> tcgen_dtype:
    """
    Generate a random value, given the data type.
    TODO: Automatically assign type, based on provided value.

    Args:
        dtype: Data type to create a single instance of.

    Returns:
        dtype: Value wrapped inside a `tcgen.dtype` class,
            respective of `dtype` argument provided.
    """
    if tcgen_dtype.is_dtype(dtype):
        return dtype(rand=True)
    else:
        # TODO: Automatic type assignment
        return dtype(None)


def val(value=None, dtype=None):
    """
    Create object with with the given value and of the `dtype` datatype.

    Args:
        value: Value to assign.
        dtype: Data type of the wrapped object.

    Returns:
        dtype: Value wrapped inside a `tcgen.dtype` class,
            respective of `dtype` argument provided.
    """
    if not tcgen_dtype.is_dtype(dtype):
        raise ValueError(f"dtype provided is not a tcgen dtype: {dtype}")
    return dtype(value)
