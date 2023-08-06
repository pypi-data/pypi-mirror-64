import numpy as np
from scipy.sparse import csc_matrix

from pyHiGHS import highs_wrapper
from pyHiGHS import (
    HIGHS_CONST_INF,
    HIGHS_CONST_TINY,
)

if __name__ == '__main__':

    c = np.array([-3, -2]).astype('double')
    A = csc_matrix(np.array([[2, 1], [1, 1], [1, 0]])).astype('double')
    rhs = np.array([10, 8, 4]).astype('double')
    lhs= np.array([-HIGHS_CONST_INF]*3).astype('double')
    lb= np.array([0, 0]).astype('double')
    ub= np.array([HIGHS_CONST_INF]*2).astype('double')

    res = highs_wrapper(c, A, rhs, lhs, lb, ub, {'sense':1, 'presolve':True, 'solver':'simplex'})
    print(res)
