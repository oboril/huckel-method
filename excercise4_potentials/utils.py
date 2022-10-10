import numpy as np
import potentials

def vec_to_xyz(vec):
    """
    Converts 1D vector of values into a ndarray of xyz coordinates.
    First 6 redundant coordinates are set to 0 (x1,y1,z1,x2,y2,x3).
    """

    vec = np.insert(vec,1,0)
    leading_zeros = np.zeros(5)
    vec = np.concatenate([leading_zeros,vec])

    xyz = np.reshape(vec, (len(vec)//3,3))

    return xyz

def distance_matrix(xyz):
    """Returns the distance matrix for the given coordinates"""
    N = len(xyz)
    M = np.stack([xyz,]*N, axis=0)
    M = M-M.transpose(1,0,2)
    M = np.sum(M**2, axis=2)
    M = np.sqrt(M)
    return M

def sum_potential(distance_matrix, potential):
    """Returns the potential energy given the distance matrix and potential energy function"""
    N = len(distance_matrix)

    # Create mask where only the values above main diagonal are 1, other entries are 0
    mask = 1-np.tril(np.ones([N,N]))

    # Calculate and sum the energies
    distance_matrix = distance_matrix*mask+(1-mask) # this prevents division-by-zero errors
    energies = np.where(mask==1, potential(distance_matrix), 0)
    energy = np.sum(energies)

    return energy

def get_energy(vec, potential):
    """Returns the potential energy for the system represented by the 1D vector"""
    xyz = vec_to_xyz(vec)
    dist_mat = distance_matrix(xyz)
    energy = sum_potential(dist_mat, potential)
    return energy

def save_coordinates(vec, filename, note):
    xyz = vec_to_xyz(vec)
    with open(filename, 'w') as f:
        f.write(f"{len(xyz)}\n")
        f.write(note+"\n")
        for line in xyz:
            f.write("H {: .5f}  {: .5f} {: .5f}\n".format(*line))

def distance_matrix_to_str(vec):
    """Returns string representation of the distance matrix"""
    xyz = vec_to_xyz(vec)
    dist_mat = distance_matrix(xyz)

    lines = []
    for line in dist_mat:
        text = ' '.join([f"{n:00.4f}" for n in line])
        lines.append(text)
    
    return '\n'.join(lines)

# Run this file to run the tests
if __name__ == '__main__':
    print("Running tests...")

    assert (vec_to_xyz(np.array([1,2,3,4,5,6])) == np.array([[0,0,0],[0,0,1],[0,2,3],[4,5,6]])).all()

    dist_mat = distance_matrix(np.array([[0,0,0],[1,0,0],[0,1,0]]))
    assert (dist_mat == np.array([[0,1,1],[1,0,np.sqrt(2)],[1,np.sqrt(2),0]])).all()

    assert abs(sum_potential(dist_mat, potentials.lennard_jones) - (1/2**6-1/2**3)) < 1e-5

    print("All tests passed")
