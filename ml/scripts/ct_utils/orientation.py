"""
Mesh orientation using PCA and manual rotation.
Aligns ant specimens to canonical axes for consistent rendering.
"""

import numpy as np
import trimesh
from scipy.spatial.transform import Rotation


def compute_pca_axes(mesh: trimesh.Trimesh) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute principal component axes from mesh vertices.

    Args:
        mesh: Input mesh

    Returns:
        Tuple of (eigenvalues, eigenvectors) sorted by magnitude
        Eigenvectors columns are principal axes (largest to smallest)
    """
    vertices = mesh.vertices
    centered = vertices - vertices.mean(axis=0)

    # Covariance matrix
    cov = np.cov(centered.T)

    # Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    # Sort by eigenvalue (largest first)
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    return eigenvalues, eigenvectors


def align_to_pca(mesh: trimesh.Trimesh, copy: bool = True) -> trimesh.Trimesh:
    """
    Align mesh to principal component axes.

    Convention after alignment:
    - X-axis: Shortest axis (left-right for ant)
    - Y-axis: Medium axis (dorsal-ventral)
    - Z-axis: Longest axis (anterior-posterior / head-tail)

    Args:
        mesh: Input mesh
        copy: If True, return a copy; else modify in place

    Returns:
        Aligned mesh
    """
    if copy:
        mesh = mesh.copy()

    # Center mesh
    mesh.vertices -= mesh.centroid

    # Get PCA axes
    eigenvalues, eigenvectors = compute_pca_axes(mesh)

    # Create rotation matrix from eigenvectors
    # Eigenvectors are already orthonormal, but ensure right-handed
    rotation_matrix = eigenvectors.T  # Transpose to get row vectors

    # Ensure right-handed coordinate system
    if np.linalg.det(rotation_matrix) < 0:
        rotation_matrix[2] *= -1

    # Apply rotation
    mesh.vertices = mesh.vertices @ rotation_matrix.T

    print(f"PCA alignment applied. Eigenvalues: {eigenvalues}")
    return mesh


def apply_rotation(
    mesh: trimesh.Trimesh,
    rx: float = 0,
    ry: float = 0,
    rz: float = 0,
    degrees: bool = True,
    copy: bool = True
) -> trimesh.Trimesh:
    """
    Apply manual rotation to mesh.

    Args:
        mesh: Input mesh
        rx, ry, rz: Rotation angles around X, Y, Z axes
        degrees: If True, angles are in degrees; else radians
        copy: If True, return a copy; else modify in place

    Returns:
        Rotated mesh
    """
    if copy:
        mesh = mesh.copy()

    # Center first
    centroid = mesh.centroid.copy()
    mesh.vertices -= centroid

    # Create rotation
    if degrees:
        rx, ry, rz = np.radians([rx, ry, rz])

    rotation = Rotation.from_euler('xyz', [rx, ry, rz])
    rotation_matrix = rotation.as_matrix()

    # Apply rotation
    mesh.vertices = mesh.vertices @ rotation_matrix.T

    return mesh


def flip_axis(mesh: trimesh.Trimesh, axis: str, copy: bool = True) -> trimesh.Trimesh:
    """
    Flip mesh along an axis.

    Args:
        mesh: Input mesh
        axis: 'x', 'y', or 'z'
        copy: If True, return a copy

    Returns:
        Flipped mesh
    """
    if copy:
        mesh = mesh.copy()

    axis_idx = {'x': 0, 'y': 1, 'z': 2}[axis.lower()]
    mesh.vertices[:, axis_idx] *= -1

    # Fix normals after flip
    mesh.fix_normals()

    return mesh


def get_orientation_bounds(mesh: trimesh.Trimesh) -> dict:
    """
    Get bounding box info for orientation verification.

    Returns:
        Dict with extent along each axis
    """
    bounds = mesh.bounds
    extent = bounds[1] - bounds[0]

    return {
        'x_extent': extent[0],
        'y_extent': extent[1],
        'z_extent': extent[2],
        'longest_axis': ['x', 'y', 'z'][np.argmax(extent)],
        'shortest_axis': ['x', 'y', 'z'][np.argmin(extent)],
    }
