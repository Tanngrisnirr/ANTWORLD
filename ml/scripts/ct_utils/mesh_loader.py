"""
Mesh loading utilities for STL and other 3D formats.
Uses trimesh for cross-format support.
"""

import trimesh
from pathlib import Path


def load_stl(path: str | Path) -> trimesh.Trimesh:
    """
    Load an STL file and return a trimesh object.

    Args:
        path: Path to STL file

    Returns:
        trimesh.Trimesh object with computed normals
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"STL file not found: {path}")

    mesh = trimesh.load(path, force='mesh')

    # Ensure we have vertex normals for rendering
    if not hasattr(mesh, 'vertex_normals') or mesh.vertex_normals is None:
        mesh.fix_normals()

    return mesh


def load_mesh(path: str | Path) -> trimesh.Trimesh:
    """
    Load any supported mesh format (STL, OBJ, PLY, etc.).

    Args:
        path: Path to mesh file

    Returns:
        trimesh.Trimesh object
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Mesh file not found: {path}")

    mesh = trimesh.load(path, force='mesh')

    # Handle scene exports (multiple meshes)
    if isinstance(mesh, trimesh.Scene):
        # Combine all meshes into one
        meshes = [g for g in mesh.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if not meshes:
            raise ValueError(f"No valid meshes found in: {path}")
        mesh = trimesh.util.concatenate(meshes)

    mesh.fix_normals()
    return mesh


def center_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """
    Center mesh at origin.

    Args:
        mesh: Input mesh

    Returns:
        Centered mesh (modified in place)
    """
    mesh.vertices -= mesh.centroid
    return mesh


def get_mesh_stats(mesh: trimesh.Trimesh) -> dict:
    """
    Get basic statistics about a mesh.

    Args:
        mesh: Input mesh

    Returns:
        Dict with vertex count, face count, bounds, etc.
    """
    bounds = mesh.bounds
    size = bounds[1] - bounds[0]

    return {
        'vertices': len(mesh.vertices),
        'faces': len(mesh.faces),
        'bounds_min': bounds[0].tolist(),
        'bounds_max': bounds[1].tolist(),
        'size': size.tolist(),
        'centroid': mesh.centroid.tolist(),
        'is_watertight': mesh.is_watertight,
    }
