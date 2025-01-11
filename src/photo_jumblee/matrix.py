import numpy as np 
from itertools import batched

def chop(matrix, width, height):
    """
    Yield parts of a matrix, starting row-wise
    """
    n_vert = int(matrix.shape[0] / height) * height
    n_horiz = int(matrix.shape[1] / width) * width
    for y in range(0, n_vert, height):
        for x in range(0, n_horiz, width):
            yield matrix[:, x:x+width][y:y+height]

def fuse(pieces, width):
    rows = []
    for batch in batched(pieces, width):
        rows.append(np.concatenate(batch, axis=1))
    return np.concatenate(rows, axis=0)

def reorder_sequence(seq, new_order):
    assert len(new_order) == len(seq)
    return [seq[i] for i in new_order]
