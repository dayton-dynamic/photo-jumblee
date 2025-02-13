from numpy import array, array_equal
from pytest import fixture

from photo_jumblee.matrix import chop, fuse, reorder_sequence


@fixture 
def matrix0():
    return array([
        [0,   1,  2,  3,  4,  5],
        [10, 11, 12, 13, 14, 15],
        [20, 21, 22, 23, 24, 25],
        [30, 31, 32, 33, 34, 35],
                    ])

def test_chop(matrix0):
    all_expected  = [array([[ 0,  1],
       [10, 11]]), array([[ 2,  3],
       [12, 13]]), array([[ 4,  5],
       [14, 15]]), array([[20, 21],
       [30, 31]]), array([[22, 23],
       [32, 33]]), array([[24, 25],
       [34, 35]])]
    chopped = list(chop(matrix0, 2, 2))
    for (expected, result) in zip(all_expected, chopped):
        assert array_equal(expected, result)

def test_fuse(matrix0):
    chopped = list(chop(matrix0, 2, 2))
    fused = fuse(chopped, 3)
    assert array_equal(fused, matrix0)

def test_reorder_sequence():
    new_order = [2, 5, 0, 8, 6, 1, 3, 7, 4, 9]
    result = reorder_sequence('abcdefghij', new_order) 
    assert ''.join(result) == 'cfaigbdhej'

