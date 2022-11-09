# dynamic-tensor

_(This package is still developing and not formally tested. Please report any potential issues. Constantly reshaping the tensor could be inefficient and not suitable for high-performance computing)_

A Python package for automatically and minimally expanding tensors for `__setitems()__` operations based on NumPy. You don't need to worry about tensor shape initialization, `reshape()`, or `expand_dims()` anymore as if the tensor has an infinite size. Both basic (integer, slice, `np.newaxis`, ellipsis) and advanced (integer & boolean array) indexing are supported (refer to [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html#)). 

You can also configure a `DynamicTensor` to adapt the tensor type to the new value to avoid `astype()` (enabled by default).

## Usage

Requires Python 3.6+ and NumPy 1.16+.

```bash
pip install dynamic-tensor
# or using conda
conda install dynamic-tensor
```

Or install from source:

```bash
git clone https://github.com/eurekazheng/dynamic-tensor.git
cd dynamic-tensor
# build the package
python setup.py sdist bdist_wheel
pip install -e .
```

Usage:

```python
import densor
d = densor.dt([[1, 2], [3, 4]])
d[2, 1:3, [2, 3]] = 5.6
print(d, d.shape)

# Expected output:
# [[[1.  0.  0.  0. ]
#   [2.  0.  0.  0. ]
#   [0.  0.  0.  0. ]]
# 
#  [[3.  0.  0.  0. ]
#   [4.  0.  0.  0. ]
#   [0.  0.  0.  0. ]]
# 
#  [[0.  0.  0.  0. ]
#   [0.  0.  5.6 5.6]
#   [0.  0.  5.6 5.6]]] (3, 3, 4)

# Helper: convert a list to tensor when possible
densor.tensorify([[1, 2], [3, 4]])    # return ndarray
densor.tensorify([[1, 2], [3, 4, 5]]) # return False
```

## Rationale

The underlying data structure of `densor.dt` is `numpy.ndarray` `_a`. Upon a `__setitem(idx, val)__` call, the following preprocessing is done:

1. Determine the target shape.
2. Based on target shape, (potentially) expand the dimension of `_a`.
3. (Optional) Based on `val` dtype, (potentially) change the dtype of `_a`.
4. Based on target shape, (potentially) change the size of `_a` at each dimension.

Refer to `src/densor.py` for more details.