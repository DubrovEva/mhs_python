from pathlib import Path
from typing import Protocol
import numpy as np


class HasDataProtocol(Protocol):
    @property
    def data(self) -> np.ndarray:
        ...


class ToFileMixin(HasDataProtocol):
    def to_file(self, filename):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(filename, self.data, fmt='%d')


class StrMixin(HasDataProtocol):
    def __str__(self):
        return str(self.data)


class HashMixin(HasDataProtocol):
    def __hash__(self):
        data = self.data
        diag_sum = np.trace(data)
        corners = data[0, 0] + data[0, -1] + data[-1, 0] + data[-1, -1]
        total = np.sum(data)
        return int(diag_sum + corners + total)


class CacheMixin(HasDataProtocol):
    _cache = {}

    def __matmul__(self, other):
        key = (hash(self), hash(other))
        if key not in CacheMixin._cache:
            CacheMixin._cache[key] = Matrix(self.data @ other.data)
        return CacheMixin._cache[key]


class Matrix(ToFileMixin, StrMixin, HashMixin, CacheMixin):
    def __init__(self, input_array):
        self._data = np.array(input_array)

    @property
    def data(self):
        return self._data

    @property
    def shape(self):
        return self._data.shape

    def __add__(self, other):
        return Matrix(self._data + other.data)

    def __sub__(self, other):
        return Matrix(self._data - other.data)

    def __mul__(self, other):
        return Matrix(self._data * other.data)

    def __truediv__(self, other):
        return Matrix(self._data / other.data)

    def __matmul__(self, other):
        return super().__matmul__(other)


if __name__ == "__main__":
    np.random.seed(0)

    A = Matrix(np.random.randint(0, 10, (10, 10)))
    B = Matrix(np.random.randint(0, 10, (10, 10)))
    C = Matrix(np.random.randint(0, 10, (10, 10)))
    D = B

    while not (
            hash(A) == hash(C)
            and not np.array_equal(A.data, C.data)
            and not np.array_equal(A.data @ B.data, C.data @ D.data)
    ):
        C = Matrix(np.random.randint(0, 10, (10, 10)))

    AB = A @ B
    CD = C @ D

    A.to_file('artifacts/3.3/A.txt')
    B.to_file('artifacts/3.3/B.txt')
    C.to_file('artifacts/3.3/C.txt')
    D.to_file('artifacts/3.3/D.txt')
    AB.to_file('artifacts/3.3/AB.txt')
    CD.to_file('artifacts/3.3/CD.txt')

    with open('artifacts/3.3/hash.txt', 'w') as f:
        f.write(f'hash(AB): {hash(AB)}\n')
        f.write(f'hash(CD): {hash(CD)}\n')
