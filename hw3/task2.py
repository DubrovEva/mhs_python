from pathlib import Path
import numpy as np


class ToFileMixin:
    def to_file(self, filename):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(filename, self._data, fmt='%d')


class StrMixin:
    def __str__(self):
        return str(self._data)


class GetSetMixin:
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = np.array(value)
    
    @property
    def shape(self):
        return self._data.shape


class Matrix(np.lib.mixins.NDArrayOperatorsMixin, ToFileMixin, StrMixin, GetSetMixin):
    def __init__(self, input_array):
        self._data = np.asarray(input_array)
    
    def __array__(self, dtype=None):
        return np.asarray(self._data, dtype=dtype)
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        args = []
        for i in inputs:
            if isinstance(i, Matrix):
                args.append(i._data)
            else:
                args.append(i)
        
        outputs = kwargs.pop('out', None)
        if outputs:
            out_args = []
            for o in outputs:
                if isinstance(o, Matrix):
                    out_args.append(o._data)
                else:
                    out_args.append(o)
            kwargs['out'] = tuple(out_args)
        
        result = getattr(ufunc, method)(*args, **kwargs)
        
        if type(result) is tuple:
            return tuple(Matrix(r) if isinstance(r, np.ndarray) else r for r in result)
        elif method == 'at':
            return None
        else:
            return Matrix(result) if isinstance(result, np.ndarray) else result


if __name__ == "__main__":
    np.random.seed(0)

    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    matrix_add = matrix1 + matrix2
    matrix_sub = matrix1 - matrix2
    matrix_mul = matrix1 * matrix2
    matrix_matmul = matrix1 @ matrix2

    matrix_add.to_file('artifacts/3.2/matrix+.txt')
    matrix_sub.to_file('artifacts/3.2/matrix-.txt')
    matrix_mul.to_file('artifacts/3.2/matrix*.txt')
    matrix_matmul.to_file('artifacts/3.2/matrix@.txt')
