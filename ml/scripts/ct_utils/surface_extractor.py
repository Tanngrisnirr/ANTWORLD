"""
Surface extraction from TIF volume data.
Uses marching cubes to convert 3D voxel data to mesh.
"""

import numpy as np
import trimesh
import tifffile
from pathlib import Path
from skimage import measure
from skimage.filters import threshold_otsu


def load_tif_volume(path: str | Path) -> np.ndarray:
    """
    Load a TIF stack as a 3D numpy array.

    Args:
        path: Path to TIF file

    Returns:
        3D numpy array (z, y, x) of voxel intensities
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"TIF file not found: {path}")

    volume = tifffile.imread(path)

    # Ensure 3D
    if volume.ndim == 2:
        raise ValueError(f"TIF is 2D, expected 3D volume: {path}")

    print(f"Loaded volume: shape={volume.shape}, dtype={volume.dtype}")
    return volume


def estimate_threshold(volume: np.ndarray, method: str = 'otsu') -> float:
    """
    Estimate threshold for separating ant tissue from air.

    Args:
        volume: 3D voxel array
        method: 'otsu' or 'percentile'

    Returns:
        Threshold value
    """
    # Flatten and sample if too large (for speed)
    flat = volume.ravel()
    if len(flat) > 10_000_000:
        flat = np.random.choice(flat, 10_000_000, replace=False)

    if method == 'otsu':
        thresh = threshold_otsu(flat)
    elif method == 'percentile':
        # Use 80th percentile as rough estimate
        thresh = np.percentile(flat, 80)
    else:
        raise ValueError(f"Unknown method: {method}")

    print(f"Estimated threshold ({method}): {thresh}")
    return thresh


def extract_surface(
    path: str | Path,
    threshold: float | None = None,
    downsample: int = 1,
    smooth: bool = True
) -> trimesh.Trimesh:
    """
    Extract surface mesh from TIF volume using marching cubes.

    Args:
        path: Path to TIF file
        threshold: Intensity threshold (auto if None)
        downsample: Downsample factor (2 = half resolution)
        smooth: Apply Laplacian smoothing

    Returns:
        trimesh.Trimesh of extracted surface
    """
    # Load volume
    volume = load_tif_volume(path)

    # Downsample if requested (reduces memory/time)
    if downsample > 1:
        volume = volume[::downsample, ::downsample, ::downsample]
        print(f"Downsampled to: {volume.shape}")

    # Auto-threshold if not specified
    if threshold is None:
        threshold = estimate_threshold(volume)

    # Create binary volume
    binary = volume > threshold

    # Clean up with morphological operations
    from scipy import ndimage
    binary = ndimage.binary_opening(binary, iterations=1)
    binary = ndimage.binary_closing(binary, iterations=1)

    # Check we have something
    if not binary.any():
        raise ValueError(f"No voxels above threshold {threshold}")

    voxel_count = binary.sum()
    print(f"Voxels above threshold: {voxel_count:,}")

    # Marching cubes to extract surface
    print("Running marching cubes...")
    verts, faces, normals, values = measure.marching_cubes(
        binary.astype(float),
        level=0.5,
        spacing=(1.0, 1.0, 1.0)
    )

    print(f"Extracted mesh: {len(verts):,} vertices, {len(faces):,} faces")

    # Create trimesh
    mesh = trimesh.Trimesh(
        vertices=verts,
        faces=faces,
        vertex_normals=normals
    )

    # Optional smoothing
    if smooth:
        trimesh.smoothing.filter_laplacian(mesh, iterations=2)

    # Center at origin
    mesh.vertices -= mesh.centroid

    return mesh


def extract_surface_chunked(
    path: str | Path,
    threshold: float | None = None,
    chunk_size: int = 500
) -> trimesh.Trimesh:
    """
    Extract surface from large TIF files using chunked processing.
    Use this for files > 2GB.

    Args:
        path: Path to TIF file
        threshold: Intensity threshold
        chunk_size: Size of chunks in Z direction

    Returns:
        trimesh.Trimesh of extracted surface
    """
    # For very large files, process in chunks
    # This is a placeholder - full implementation would need
    # careful handling of chunk boundaries
    raise NotImplementedError(
        "Chunked processing not yet implemented. "
        "Use downsample parameter instead: extract_surface(path, downsample=2)"
    )
