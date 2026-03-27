"""
Headless rendering using pyrender.
Renders mesh from multiple camera viewpoints to PNG images.
"""

import numpy as np
import trimesh
import pyrender
from PIL import Image
from pathlib import Path


# Camera view definitions
# Each view: (camera_position_direction, up_vector, name)
CAMERA_VIEWS = {
    'dorsal': {
        'direction': np.array([0, 1, 0]),   # Looking down from above
        'up': np.array([0, 0, -1]),         # Z pointing "back"
        'description': 'Top-down view (dorsal)',
    },
    'ventral': {
        'direction': np.array([0, -1, 0]),  # Looking up from below
        'up': np.array([0, 0, 1]),
        'description': 'Bottom-up view (ventral)',
    },
    'anterior': {
        'direction': np.array([0, 0, 1]),   # Looking at front (head)
        'up': np.array([0, 1, 0]),
        'description': 'Front view (head)',
    },
    'posterior': {
        'direction': np.array([0, 0, -1]),  # Looking at back (gaster)
        'up': np.array([0, 1, 0]),
        'description': 'Back view (gaster)',
    },
    'left': {
        'direction': np.array([-1, 0, 0]),  # Looking from left side
        'up': np.array([0, 1, 0]),
        'description': 'Left profile view',
    },
    'right': {
        'direction': np.array([1, 0, 0]),   # Looking from right side
        'up': np.array([0, 1, 0]),
        'description': 'Right profile view',
    },
}


def create_camera_pose(direction: np.ndarray, up: np.ndarray, distance: float) -> np.ndarray:
    """
    Create 4x4 camera pose matrix for pyrender.

    Pyrender cameras look down their -Z axis by convention.

    Args:
        direction: Direction FROM origin TO camera (camera position direction)
        up: Up vector
        distance: Distance from origin

    Returns:
        4x4 transformation matrix
    """
    # Normalize direction
    direction = direction / np.linalg.norm(direction)

    # Camera position
    position = direction * distance

    # Forward vector: from camera toward origin (opposite of position direction)
    forward = -direction

    # Right vector
    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)

    # Corrected up vector
    up_corrected = np.cross(right, forward)

    # Build 4x4 matrix
    # Pyrender expects camera looking down -Z, so we use -forward for Z column
    pose = np.eye(4)
    pose[:3, 0] = right
    pose[:3, 1] = up_corrected
    pose[:3, 2] = -forward  # Camera looks down -Z
    pose[:3, 3] = position

    return pose


def setup_scene(mesh: trimesh.Trimesh, bg_color: tuple = (1.0, 1.0, 1.0, 1.0)) -> pyrender.Scene:
    """
    Create pyrender scene with mesh and lighting.

    Args:
        mesh: Trimesh object
        bg_color: Background color RGBA (default white)

    Returns:
        pyrender.Scene
    """
    scene = pyrender.Scene(bg_color=bg_color, ambient_light=[0.3, 0.3, 0.3])

    # Convert trimesh to pyrender mesh
    # Use a neutral color for the ant surface
    material = pyrender.MetallicRoughnessMaterial(
        baseColorFactor=[0.7, 0.5, 0.4, 1.0],  # Brownish ant color
        metallicFactor=0.1,
        roughnessFactor=0.8,
    )

    py_mesh = pyrender.Mesh.from_trimesh(mesh, material=material)
    scene.add(py_mesh)

    # Add directional lights for good surface detail
    # Key light (main)
    key_light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=3.0)
    key_pose = np.eye(4)
    key_pose[:3, :3] = trimesh.transformations.rotation_matrix(
        np.radians(-45), [1, 0, 0])[:3, :3]
    scene.add(key_light, pose=key_pose)

    # Fill light (softer, opposite side)
    fill_light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=1.5)
    fill_pose = np.eye(4)
    fill_pose[:3, :3] = trimesh.transformations.rotation_matrix(
        np.radians(45), [1, 0, 0])[:3, :3]
    scene.add(fill_light, pose=fill_pose)

    return scene


def normalize_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """
    Normalize mesh to fit within a unit sphere.
    This ensures consistent rendering regardless of original scale.

    Args:
        mesh: Input mesh

    Returns:
        Normalized mesh (copy)
    """
    mesh = mesh.copy()

    # Center at origin
    mesh.vertices -= mesh.centroid

    # Scale to fit in unit sphere
    bounds = mesh.bounds
    max_extent = np.max(bounds[1] - bounds[0])
    if max_extent > 0:
        mesh.vertices /= max_extent

    return mesh


def render_view(
    mesh: trimesh.Trimesh,
    view: str,
    output_path: str | Path,
    resolution: int = 512,
    bg_color: tuple = (1.0, 1.0, 1.0, 1.0)
) -> Path:
    """
    Render mesh from specified viewpoint and save to PNG.

    Args:
        mesh: Trimesh object (should be centered at origin)
        view: View name from CAMERA_VIEWS
        output_path: Output PNG path
        resolution: Image resolution (square)
        bg_color: Background RGBA

    Returns:
        Path to saved image
    """
    if view not in CAMERA_VIEWS:
        raise ValueError(f"Unknown view: {view}. Available: {list(CAMERA_VIEWS.keys())}")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Normalize mesh to unit scale for consistent rendering
    normalized_mesh = normalize_mesh(mesh)

    # Camera distance for unit-scale mesh
    camera_distance = 2.5  # Good distance for unit-sized object with 45deg FOV

    # Create scene with normalized mesh
    scene = setup_scene(normalized_mesh, bg_color)

    # Add camera with appropriate clipping planes
    camera = pyrender.PerspectiveCamera(
        yfov=np.pi / 4.0,
        aspectRatio=1.0,
        znear=0.1,
        zfar=100.0
    )
    view_config = CAMERA_VIEWS[view]
    camera_pose = create_camera_pose(
        view_config['direction'],
        view_config['up'],
        camera_distance
    )
    scene.add(camera, pose=camera_pose)

    # Render
    renderer = pyrender.OffscreenRenderer(resolution, resolution)
    try:
        color, depth = renderer.render(scene)
    finally:
        renderer.delete()

    # Save image
    image = Image.fromarray(color)
    image.save(output_path)

    return output_path


def render_all_views(
    mesh: trimesh.Trimesh,
    output_dir: str | Path,
    specimen_id: str,
    resolution: int = 512,
    views: list[str] | None = None,
    bg_color: tuple = (1.0, 1.0, 1.0, 1.0)
) -> list[Path]:
    """
    Render mesh from all viewpoints.

    Args:
        mesh: Trimesh object
        output_dir: Output directory
        specimen_id: Specimen identifier for filenames
        resolution: Image resolution
        views: List of views to render (default: all)
        bg_color: Background RGBA

    Returns:
        List of saved image paths
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if views is None:
        views = list(CAMERA_VIEWS.keys())

    saved = []
    for view in views:
        output_path = output_dir / f"{specimen_id}_{view}.png"
        render_view(mesh, view, output_path, resolution, bg_color)
        print(f"  Rendered: {output_path.name}")
        saved.append(output_path)

    return saved
