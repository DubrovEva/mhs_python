from pathlib import Path
import numpy as np


class Matrix:
    def __init__(self, data):
        self.data = np.array(data)

    def __add__(self, other):
        if self.data.shape != other.data.shape:
            raise ValueError("Matrices must have the same dimensions for addition")
        return Matrix(self.data + other.data)

    def __mul__(self, other):
        if self.data.shape != other.data.shape:
            raise ValueError("Matrices must have the same dimensions for element-wise multiplication")
        return Matrix(self.data * other.data)

    def __matmul__(self, other):
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Matrices must have compatible dimensions for matrix multiplication")
        return Matrix(self.data @ other.data)

    def __str__(self):
        return str(self.data)

    def to_file(self, filename):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(filename, self.data, fmt='%d')


if __name__ == "__main__":
    np.random.seed(0)

    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    matrix_add = matrix1 + matrix2
    matrix_mul = matrix1 * matrix2
    matrix_matmul = matrix1 @ matrix2

    matrix_add.to_file('artifacts/3.1/matrix+.txt')
    matrix_mul.to_file('artifacts/3.1/matrix*.txt')
    matrix_matmul.to_file('artifacts/3.1/matrix@.txt')
