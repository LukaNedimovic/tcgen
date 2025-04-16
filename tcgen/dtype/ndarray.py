import numbers
from typing import Any, List, Optional, Tuple, Union

from .dtype import dtype
from .int32 import int32


class ndarray(dtype):
    """
    Class containing the implementation of an ndarray
    """

    min = None
    max = None

    def __init__(
        self,
        val: Union[List[Any], None] = None,
        elem_type=int32,
        signed=True,
        rand: bool = False,
        shape: Tuple[int, ...] = (32,),
        strides: Optional[Tuple[int, ...]] = None,
        order: str = "C",
    ):
        """
        Instantiate an array of `elem_type` elements.

        Parameters:
            val: Input data (list or nested list)
            elem_type: Type of array elements
            signed: Whether the type is signed
            rand: If True, fill with random values
            shape: Desired shape of the array
            strides: Memory strides
            order: 'C' for row-major, 'F' for column-major
        """
        if super()._is_same_class(self, val):
            super()._deepcopy(self, val)
            return

        super().__init__(val, signed=signed)

        ndarray.min = elem_type.min
        ndarray.max = elem_type.max

        self.shape = tuple(shape)
        self.type = elem_type
        self.size = self._compute_size(self.shape)
        self.ndim = len(self.shape)
        self.itemsize = 4
        self.order = order

        # Calculate strides if not provided
        if strides is None:
            self.strides = self._compute_strides(self.shape, self.itemsize, order)
        else:
            self.strides = strides

        if rand:
            self.val = self._rand()
        else:
            if val is not None:
                flat_val = self._flatten(val)
                if len(flat_val) != self.size:
                    raise ValueError(
                        f"Shape {shape} incompatible with "
                        f"number of elements {len(flat_val)}."
                    )
                self.val = [self.type(v) for v in flat_val]
            else:
                self.val = [self.type() for _ in range(self.size)]

    def _rand(self):
        # TODO implement dynamic element type for rand function
        return [self.type(rand=True) for _ in range(self.size)]

    def _compute_strides(self, shape, itemsize, order="C"):
        """Compute strides based on shape and memory order."""
        if order == "F":  # Column-major
            strides = [itemsize]
            for dim in shape[:-1]:
                strides.append(strides[-1] * dim)
            strides = tuple(strides)
        else:  # Row-major
            strides = [itemsize]
            for dim in reversed(shape[1:]):
                strides.append(strides[-1] * dim)
            strides = tuple(reversed(strides))
        return strides

    def _flatten(self, nested_list):
        """Flattens arbitrarily nested list of values."""
        if not isinstance(nested_list, (list, tuple)):
            return [nested_list]
        flat = []
        for elem in nested_list:
            flat.extend(self._flatten(elem))
        return flat

    def _compute_size(self, shape: Tuple[int, ...]) -> int:
        size = 1
        for dim in shape:
            size *= dim
        return size

    def __str__(self):
        return self._format_str(self.val, self.shape)

    def _format_str(self, flat, shape):
        """Converts flat list to nested string representation."""
        if not shape:
            return str(flat[0])

        dim = shape[0]
        subsize = len(flat) // dim

        nested = [
            self._format_str(
                flat[i * subsize : (i + 1) * subsize], shape[1:]  # noqa: E203
            )
            for i in range(dim)
        ]

        if len(shape) > 1:
            return "[" + ",\n ".join(nested) + "]"
        else:
            return "[" + ", ".join(nested) + "]"

    def __getitem__(self, key):
        """Support for indexing and slicing."""
        if isinstance(key, numbers.Integral):
            # Single integer index
            if self.ndim == 1:
                return self.val[key]
            else:
                # Handle multi-dimensional array with single index
                return self._get_subarray(key)
        elif isinstance(key, tuple):
            # Multi-dimensional indexing
            return self._get_multidim(key)
        elif isinstance(key, slice):
            # TODO implement slicing
            raise NotImplementedError("Advanced indexing not implemented")
        else:
            raise TypeError(f"Invalid index type: {type(key)}")

    def _get_subarray(self, idx):
        """Get subarray for single index on multi-dimensional array."""
        if idx < 0:
            idx += self.shape[0]
        if not (0 <= idx < self.shape[0]):
            raise IndexError(
                f"Index {idx} out of bounds for axis 0 with size {self.shape[0]}"
            )

        subsize = self.size // self.shape[0]
        sub_val = self.val[idx * subsize : (idx + 1) * subsize]  # noqa: E203

        # Create view
        new_array = ndarray(sub_val, elem_type=self.type, shape=self.shape[1:])
        return new_array

    def _get_multidim(self, key):
        """Handle multi-dimensional indexing."""
        if len(key) > self.ndim:
            raise IndexError(
                f"Too many indices for array: array is {self.ndim}-dimensional, "
                f"but {len(key)} were indexed"
            )

        # Handle simple integer indices
        if all(isinstance(k, numbers.Integral) for k in key):
            flat_idx = 0
            for i, (k, stride) in enumerate(zip(key, self.strides)):
                if k < 0:
                    k += self.shape[i]
                if not (0 <= k < self.shape[i]):
                    raise IndexError(
                        f"Index {k} out of bounds for axis {i} "
                        f"with size {self.shape[i]}"
                    )
                flat_idx += k * stride // self.itemsize
            return self.val[flat_idx]

        raise NotImplementedError("Advanced indexing not implemented")

    def reshape(self, new_shape):
        """Reshape the array."""

        # TODO implement reshaping for higher dimensional arrays
        if self._compute_size(new_shape) != self.size:
            raise ValueError(
                f"Cannot reshape array of size {self.size} into shape {new_shape}"
            )

        # Create view
        new_array = ndarray(self.val, elem_type=self.type, shape=new_shape)
        return new_array

    def transpose(self):
        """Transpose the array."""
        if self.ndim != 2:
            # TODO implement transposing for higher dimensional arrays
            raise NotImplementedError("Transpose only implemented for 2D arrays")

        # For 2D arrays
        rows, cols = self.shape
        transposed = []
        for j in range(cols):
            for i in range(rows):
                transposed.append(self.val[i * cols + j])

        new_array = ndarray(transposed, elem_type=self.type, shape=(cols, rows))
        return new_array

    def __add__(self, other):
        if not isinstance(other, ndarray):
            raise TypeError(
                f"Unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'"
            )

        if self.shape != other.shape:
            raise ValueError(
                f"Cannot add arrays of shape {self.shape} and {other.shape} together"
            )

        # Element-wise addition of values
        result_vals = [self.type(a + b) for a, b in zip(self.val, other.val)]

        # Create new ndarray with result
        return ndarray(result_vals, elem_type=self.type, shape=self.shape)

    def __sub__(self, other):
        if not isinstance(other, ndarray):
            raise TypeError(
                f"Unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'"
            )

        if self.shape != other.shape:
            raise ValueError(
                f"Cannot subtract arrays of shape "
                f"{self.shape} and {other.shape} together"
            )

        # Element-wise subtraction
        result_vals = [self.type(a - b) for a, b in zip(self.val, other.val)]

        # Return new ndarray
        return ndarray(result_vals, elem_type=self.type, shape=self.shape)

    def __mul__(self, other):
        if not isinstance(other, ndarray):
            raise TypeError(
                f"Unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'"
            )

        if self.shape != other.shape:
            raise ValueError(
                f"Cannot multiply arrays of shape "
                f"{self.shape} and {other.shape} together"
            )

        # Element-wise multiplication
        result_vals = [self.type(a * b) for a, b in zip(self.val, other.val)]

        # Return new ndarray with result
        return ndarray(result_vals, elem_type=self.type, shape=self.shape)

    def __truediv__(self, other):
        if not isinstance(other, ndarray):
            raise TypeError(
                f"Unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'"
            )

        if self.shape != other.shape:
            raise ValueError(
                f"Cannot divide arrays of shape "
                f"{self.shape} and {other.shape} together"
            )

        # Element-wise division
        result_vals = [self.type(a / b) for a, b in zip(self.val, other.val)]

        # Return new ndarray with result
        return ndarray(result_vals, elem_type=self.type, shape=self.shape)

    def __floordiv__(self, other):
        if not isinstance(other, ndarray):
            raise TypeError(
                f"Unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'"
            )

        if self.shape != other.shape:
            raise ValueError(
                f"Cannot divide arrays of shape "
                f"{self.shape} and {other.shape} together"
            )

        # Element-wise division
        result_vals = [self.type(a // b) for a, b in zip(self.val, other.val)]

        # Return new ndarray with result
        return ndarray(result_vals, elem_type=self.type, shape=self.shape)

    def dot(self, other):
        if not isinstance(other, ndarray):
            raise TypeError("dot product requires both operands to be ndarrays")

        if self.ndim == 1 and other.ndim == 1:
            # Element-wise multiplication
            sum = self.type(0)
            for val in [self.type(a * b) for a, b in zip(self.val, other.val)]:
                sum += val

            # Return the sum
            return sum

        m, n = self.shape
        n2, p = other.shape

        if n != n2:
            raise ValueError(
                f"Incompatible shapes for matrix multiplication: "
                f"{self.shape} and {other.shape}"
            )

        result_vals = []
        for i in range(m):
            for j in range(p):
                sum_val = self.type(0)
                for k in range(n):
                    a = self[i, k]
                    b = other[k, j]
                    sum_val += a * b
                result_vals.append(sum_val)

        return ndarray(result_vals, elem_type=self.type, shape=(m, p))

    def matmul(self, other):
        if not isinstance(other, ndarray):
            raise TypeError("matmul requires both operands to be ndarrays")

        # 2D matrix multiplication
        if self.ndim == 2 and other.ndim == 2:
            m, n = self.shape
            n2, p = other.shape

            if n != n2:
                raise ValueError(
                    f"Incompatible shapes for matrix multiplication: "
                    f"{self.shape} and {other.shape}"
                )

            result_vals = []
            for i in range(m):
                for j in range(p):
                    sum_val = self.type(0)
                    for k in range(n):
                        a = self[i, k]
                        b = other[k, j]
                        sum_val += a * b
                    result_vals.append(sum_val)

            return ndarray(result_vals, elem_type=self.type, shape=(m, p))

        # For higher-dimensional arrays
        elif self.ndim >= 2 and other.ndim >= 2:
            # Broadcasting rule: handle dimensions other than the last two
            if self.shape[-1] != other.shape[-2]:
                raise ValueError(
                    f"Incompatible shapes for matrix multiplication: "
                    f"{self.shape} and {other.shape}"
                )

            # Prepare the result array for broadcasting
            result_shape = self.shape[:-2] + other.shape[-2:]
            result_vals = []

            # Iterate over the broadcasted dimensions
            for indices in self._broadcast_indices(self.shape[:-2], other.shape[:-2]):
                subarray_self = self[indices + (slice(None), slice(None))]
                subarray_other = other[indices + (slice(None), slice(None))]

                # Perform matrix multiplication on the last two dimensions
                sub_result = subarray_self.matmul(subarray_other)
                result_vals.append(sub_result)

            # Flatten the result and return
            return ndarray(result_vals, elem_type=self.type, shape=result_shape)

        else:
            raise ValueError("Invalid shapes for matmul: ndim mismatch")

    def sum(self):
        if not self.val:
            raise ValueError("Cannot compute sum of empty array")
        sum = self.type(0)
        for v in self.val:
            sum = sum + v
        return sum

    def mean(self):
        if not self.val:
            raise ValueError("Cannot compute mean of empty array")
        total = self.sum()
        return total / self.type(self.size)

    def max_val(self):
        if not self.val:
            raise ValueError("Cannot compute max of empty array")
        max_val = self.val[0]
        for v in self.val[1:]:
            if v > max_val:
                max_val = v
        return max_val

    def min_val(self):
        if not self.val:
            raise ValueError("Cannot compute min of empty array")
        min_val = self.val[0]
        for v in self.val[1:]:
            if v < min_val:
                min_val = v
        return min_val
