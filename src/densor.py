from typing import Iterable
import numpy as np

URL = 'https://github.com/eurekazheng/dynamic-tensor/issues'


def tensorify(lst):
    result = np.array(lst)
    return result if (result.dtype != object) else False


class dt(object):
    def __init__(self, default, adapt_type=True, *args, **kwargs):
        self._a = np.array(*args or [default], **kwargs)
        # Default value is 0
        try:
            self.default = np.array(0).astype(self._a.dtype)
        except Exception:
            print(f'Bug: default value type not convertible from 0. Open an issue at {URL}')
        self.adapt_type = adapt_type

    @property
    def shape(self):
        return self._a.shape

    def __getitem__(self, idx):
        return self._a.__getitem__(idx)

    def __setitem__(self, idx, val):
        # print(idx)

        # 1. Determine the target shape
        # If idx is a boolean mask, target_shape is determined by idx's shape
        idx_t = tensorify(idx)
        if idx_t is not False and idx_t.dtype == bool:
            target_shape = idx_t.shape
        # Otherwise, things get complicated
        else:
            # Convert idx from tuple to list to enable item assignment
            target_shape = list(idx) if isinstance(idx, tuple) else [idx]
            # Replace ellipsis with non-limiting values (like a's shape or 0)
            # at the corresponding dimension
            assert target_shape.count(Ellipsis) <= 1
            if Ellipsis in target_shape:
                ellipsisPos = target_shape.index(Ellipsis)
                omittedDims = len(self._a.shape) - len(target_shape) + 1
                target_shape = target_shape[:ellipsisPos] + \
                               self._a.shape[ellipsisPos:ellipsisPos + omittedDims] + \
                               target_shape[ellipsisPos + 1:]

            # We need to traverse idx for combining basic and advanced indexing
            for j, i in enumerate(target_shape):
                # Slice is only limiting with stop
                if isinstance(i, slice):
                    if i.stop:
                        target_shape[j] = range(i.start or 0, i.stop, i.step or 1)[-1]
                    else:
                        target_shape[j] = self.shape[j]
                # np.newaxis or None is non-limiting
                elif i == np.newaxis:
                    target_shape[j] = 0
                # Integer array indexing is limiting with the maximum entry
                # at the corresponding dimension
                elif isinstance(i, Iterable):
                    target_shape[j] = np.array(i).max()

        # 2. Based on target_shape, (potentially) expand the dimension of a
        dim_diff = len(target_shape) - len(self.shape)
        if dim_diff > 0:
            self._a = np.expand_dims(self._a, axis=tuple(range(-dim_diff, 0)))
        # 3. (Optional) Based on val dtype, (potentially) change the dtype of a
        if self.adapt_type:
            self._a = self._a.astype(type(val))
        # 4. Based on target_shape, (potentially) change the size of a at each dimension
        try:
            self._a = np.pad(self._a, [(0, max(0, i - self.shape[j] + 1)) for j, i in enumerate(target_shape)],
                             mode='constant', constant_values=self.default)
        except IndexError:
            print(f'Bug: Index out of range. Open an issue at {URL}')
        return self._a.__setitem__(idx, val)

    def __str__(self):
        return self._a.__str__()


if __name__ == '__main__':
    d = dt([[1, 2], [3, 4]])
    d[2, 1:3, [2, 3]] = 5.6
    print(d, d.shape)
