#!/usr/bin/env python3
"""
CT Scan to Training Image Renderer

Renders 3D CT scans (STL meshes, TIF volumes) to 2D PNG images
from multiple camera viewpoints for ML training.

Usage:
    python render_ct_scans.py ../scans/specimen.stl --specimen-id ant001
    python render_ct_scans.py ../scans/volume.tif --specimen-id ant002 --threshold 100
    python render_ct_scans.py ../scans/curled.stl --specimen-id ant003 --skip-pca --rotate 0 45 0

Output:
    Creates {output_dir}/{specimen_id}/ with PNG images for each view:
    - {specimen_id}_dorsal.png
    - {specimen_id}_ventral.png
    - {specimen_id}_anterior.png
    - {specimen_id}_posterior.png
    - {specimen_id}_left.png
    - {specimen_id}_right.png
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ct_utils import (
    load_stl,
    load_mesh,
    extract_surface,
    align_to_pca,
    apply_rotation,
    render_all_views,
    CAMERA_VIEWS,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Render CT scans to training images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'input',
        type=Path,
        help='Input file (STL, OBJ, PLY, or TIF)'
    )

    parser.add_argument(
        '--specimen-id',
        required=True,
        help='Specimen identifier for output filenames'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'data' / 'ct_renders',
        help='Output directory (default: ../data/ct_renders)'
    )

    parser.add_argument(
        '--resolution',
        type=int,
        default=512,
        help='Output image resolution (default: 512)'
    )

    # TIF-specific options
    parser.add_argument(
        '--threshold',
        type=float,
        help='TIF threshold value (auto-detected if not specified)'
    )

    parser.add_argument(
        '--downsample',
        type=int,
        default=1,
        help='TIF downsample factor (default: 1, use 2-4 for large files)'
    )

    # Orientation options
    parser.add_argument(
        '--skip-pca',
        action='store_true',
        help='Skip PCA auto-orientation (for manual rotation)'
    )

    parser.add_argument(
        '--rotate',
        type=float,
        nargs=3,
        metavar=('RX', 'RY', 'RZ'),
        help='Manual rotation in degrees (X Y Z)'
    )

    # View selection
    parser.add_argument(
        '--views',
        nargs='+',
        choices=list(CAMERA_VIEWS.keys()),
        default=list(CAMERA_VIEWS.keys()),
        help='Views to render (default: all)'
    )

    # Background
    parser.add_argument(
        '--bg-color',
        type=float,
        nargs=4,
        default=[1.0, 1.0, 1.0, 1.0],
        metavar=('R', 'G', 'B', 'A'),
        help='Background color RGBA 0-1 (default: white)'
    )

    return parser.parse_args()


def main():
    args = parse_args()

    input_path = args.input.resolve()
    suffix = input_path.suffix.lower()

    print(f"Input: {input_path}")
    print(f"Specimen ID: {args.specimen_id}")
    print(f"Output dir: {args.output_dir}")
    print()

    # Load mesh based on file type
    if suffix in ('.tif', '.tiff'):
        print("Loading TIF volume and extracting surface...")
        mesh = extract_surface(
            input_path,
            threshold=args.threshold,
            downsample=args.downsample
        )
    elif suffix in ('.stl', '.obj', '.ply', '.off', '.glb', '.gltf'):
        print(f"Loading mesh from {suffix.upper()}...")
        if suffix == '.stl':
            mesh = load_stl(input_path)
        else:
            mesh = load_mesh(input_path)
    else:
        print(f"Error: Unsupported file format: {suffix}")
        print("Supported: .stl, .obj, .ply, .tif, .tiff")
        sys.exit(1)

    print(f"Mesh loaded: {len(mesh.vertices):,} vertices, {len(mesh.faces):,} faces")
    print()

    # Center mesh
    mesh.vertices -= mesh.centroid

    # Orientation
    if not args.skip_pca:
        print("Applying PCA auto-orientation...")
        mesh = align_to_pca(mesh, copy=False)

    if args.rotate:
        rx, ry, rz = args.rotate
        print(f"Applying manual rotation: X={rx}, Y={ry}, Z={rz}")
        mesh = apply_rotation(mesh, rx, ry, rz, degrees=True, copy=False)

    print()

    # Render
    print(f"Rendering {len(args.views)} views at {args.resolution}x{args.resolution}...")
    output_dir = args.output_dir / args.specimen_id

    saved = render_all_views(
        mesh,
        output_dir,
        args.specimen_id,
        resolution=args.resolution,
        views=args.views,
        bg_color=tuple(args.bg_color)
    )

    print()
    print(f"Done! {len(saved)} images saved to: {output_dir}")


if __name__ == '__main__':
    main()
