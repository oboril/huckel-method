import unittest
import numpy as np
import adjacency_matrices

def linear_polyene(n : int) -> np.ndarray:
    """Creates Huckel (connectivity) matrix for linear polyene"""
    M = np.eye(n-1)
    M = np.pad(M, ((1,0),(0,1)))
    M = M + M.T
    
    return M

def cyclic_polyene(n : int) -> np.ndarray:
    """Creates Huckel (connectivity) matrix for cyclic polyene"""
    M = linear_polyene(n)
    M[-1,0] = 1.
    M[0,-1] = 1.

    return M


def platonic_solid(n : int) -> np.ndarray:
    """
    Returns adjacency matrix for the given platonic solid
    """
    if n == 4:
        M = adjacency_matrices.tetrahedron
    elif n == 6:
        M = adjacency_matrices.octahedron
    elif n == 8:
        M = adjacency_matrices.cube
    elif n == 12:
        M = adjacency_matrices.icosahedron
    elif n == 20:
        M = adjacency_matrices.dodecahedron
    elif n == 60:
        M = adjacency_matrices.fullerene60
    else:
        raise Exception("Unreachable code")
    
    return np.array(M, dtype=float)



# TESTS
class Tests(unittest.TestCase):

    def test_linear_polyene(self):
        lin_poly2 = np.array([[0,1],[1,0]], dtype=float)
        assert (linear_polyene(2) == lin_poly2).all()

        lin_poly3 = np.array([[0,1,0],[1,0,1],[0,1,0]], dtype=float)
        assert (linear_polyene(3) == lin_poly3).all()

    def test_cyclic_polyene(self):
        cyclic_poly3 = np.array([[0,1,1],[1,0,1],[1,1,0]], dtype=float)
        assert (cyclic_polyene(3) == cyclic_poly3).all()

        cyclic_poly4 = np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]], dtype=float)
        assert (cyclic_polyene(4) == cyclic_poly4).all()

if __name__ == '__main__':
    unittest.main()