#!/usr/bin/env python3
"""
Image Preprocessing Pipeline for ANTWORLD ML Training

Key features:
- SPECIMEN-BASED SPLITTING: All images from same specimen stay in same split
  (prevents data leakage between train/val/test)
- DEGRADATION AUGMENTATION: Simulates real-world user photo quality
- Reproducible random seed for consistent splits

Usage:
    python preprocess_images.py                    # Process all images
    python preprocess_images.py --no-augment       # Skip augmentation
    python preprocess_images.py --split-only       # Only create splits, no augmentation
    python preprocess_images.py --augment-only     # Only augment existing splits

Output structure:
    TrainingSets/processed/
    ├── train/
    │   └── ant/
    │       ├── CASENT0173862_h_1_original.jpg
    │       ├── CASENT0173862_h_1_rot15.jpg
    │       ├── CASENT0173862_h_1_blur.jpg
    │       └── ...
    ├── val/
    │   └── ant/
    └── test/
        └── ant/
"""

import os
import sys
import json
import random
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import shutil

# Optional imports - graceful degradation if not installed
try:
    from PIL import Image, ImageFilter, ImageEnhance, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("WARNING: PIL/Pillow not installed. Install with: pip install Pillow")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("WARNING: NumPy not installed. Some augmentations disabled.")


# Configuration
RANDOM_SEED = 42  # For reproducible splits
TARGET_SIZE = (224, 224)  # MobileNetV2 input size

SPLIT_RATIOS = {
    "train": 0.70,
    "val": 0.15,
    "test": 0.15,
}

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
TRAINING_SETS_DIR = PROJECT_ROOT / "TrainingSets"
RAW_DIR = TRAINING_SETS_DIR / "raw"
PROCESSED_DIR = TRAINING_SETS_DIR / "processed"
ML_DIR = PROJECT_ROOT / "ml"
SPLIT_LOG_FILE = TRAINING_SETS_DIR / "split_log.json"


# =============================================================================
# AUGMENTATION CONFIGURATION
# =============================================================================

AUGMENTATIONS = {
    # Rotation augmentations
    "rot15": {"type": "rotate", "angle": 15},
    "rot-15": {"type": "rotate", "angle": -15},
    "rot10": {"type": "rotate", "angle": 10},
    "rot-10": {"type": "rotate", "angle": -10},

    # Flip augmentations (horizontal only - ants don't appear upside down)
    "fliph": {"type": "flip_horizontal"},

    # Brightness variations (simulate different lighting)
    "bright": {"type": "brightness", "factor": 1.2},
    "dark": {"type": "brightness", "factor": 0.8},

    # Contrast variations
    "highcon": {"type": "contrast", "factor": 1.3},
    "lowcon": {"type": "contrast", "factor": 0.7},

    # DEGRADATION augmentations (simulate poor user photos)
    "blur": {"type": "blur", "radius": 1.5},
    "blur2": {"type": "blur", "radius": 2.5},

    # JPEG compression artifacts
    "jpeg70": {"type": "jpeg_quality", "quality": 70},
    "jpeg50": {"type": "jpeg_quality", "quality": 50},
    "jpeg30": {"type": "jpeg_quality", "quality": 30},

    # Noise (if numpy available)
    "noise": {"type": "noise", "intensity": 0.03},
    "noise2": {"type": "noise", "intensity": 0.06},

    # Scale down then up (simulate low resolution camera)
    "lowres": {"type": "lowres", "scale": 0.5},
    "lowres2": {"type": "lowres", "scale": 0.25},

    # Random crop (simulate off-center subjects)
    "crop90": {"type": "crop", "ratio": 0.9},
    "crop80": {"type": "crop", "ratio": 0.8},
}

# Default augmentations to apply (subset of above)
DEFAULT_AUGMENTATIONS = [
    "rot15", "rot-15",           # Rotation
    "fliph",                      # Horizontal flip
    "bright", "dark",             # Brightness
    "blur", "blur2",              # Blur degradation
    "jpeg50", "jpeg30",           # Compression artifacts
    "noise",                      # Noise
    "lowres",                     # Low resolution
    "crop90",                     # Off-center crop
]


# =============================================================================
# IMAGE PROCESSING FUNCTIONS
# =============================================================================

def resize_image(img, target_size=TARGET_SIZE):
    """Resize image to target size, maintaining aspect ratio with padding."""
    # Calculate aspect-ratio-preserving resize
    img_ratio = img.width / img.height
    target_ratio = target_size[0] / target_size[1]

    if img_ratio > target_ratio:
        # Image is wider - fit to width
        new_width = target_size[0]
        new_height = int(new_width / img_ratio)
    else:
        # Image is taller - fit to height
        new_height = target_size[1]
        new_width = int(new_height * img_ratio)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create white background and paste
    result = Image.new("RGB", target_size, (255, 255, 255))
    paste_x = (target_size[0] - new_width) // 2
    paste_y = (target_size[1] - new_height) // 2
    result.paste(img, (paste_x, paste_y))

    return result


def apply_augmentation(img, aug_name, aug_config):
    """Apply a single augmentation to an image."""
    aug_type = aug_config["type"]

    if aug_type == "rotate":
        return img.rotate(aug_config["angle"], fillcolor=(255, 255, 255))

    elif aug_type == "flip_horizontal":
        return ImageOps.mirror(img)

    elif aug_type == "brightness":
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(aug_config["factor"])

    elif aug_type == "contrast":
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(aug_config["factor"])

    elif aug_type == "blur":
        return img.filter(ImageFilter.GaussianBlur(radius=aug_config["radius"]))

    elif aug_type == "jpeg_quality":
        # Save to bytes with low quality, then reload
        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=aug_config["quality"])
        buffer.seek(0)
        return Image.open(buffer).convert("RGB")

    elif aug_type == "noise" and NUMPY_AVAILABLE:
        arr = np.array(img).astype(np.float32)
        noise = np.random.normal(0, aug_config["intensity"] * 255, arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)

    elif aug_type == "lowres":
        scale = aug_config["scale"]
        small_size = (int(img.width * scale), int(img.height * scale))
        small = img.resize(small_size, Image.Resampling.BILINEAR)
        return small.resize(img.size, Image.Resampling.BILINEAR)

    elif aug_type == "crop":
        ratio = aug_config["ratio"]
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        left = random.randint(0, img.width - new_w)
        top = random.randint(0, img.height - new_h)
        cropped = img.crop((left, top, left + new_w, top + new_h))
        return cropped.resize(img.size, Image.Resampling.LANCZOS)

    else:
        # Unknown augmentation, return original
        return img


# =============================================================================
# SPECIMEN-BASED SPLITTING
# =============================================================================

def collect_specimens(raw_dir):
    """
    Collect all specimens and their images from raw directory.

    Returns dict: {specimen_code: {
        "images": [path1, path2, ...],
        "subfamily": str,
        "genus": str,
        "species": str,
    }}
    """
    specimens = {}

    for subfamily_dir in raw_dir.iterdir():
        if not subfamily_dir.is_dir():
            continue

        subfamily = subfamily_dir.name

        for species_dir in subfamily_dir.iterdir():
            if not species_dir.is_dir():
                continue

            # Parse genus_species from directory name
            parts = species_dir.name.split("_", 1)
            genus = parts[0] if parts else "unknown"
            species = parts[1] if len(parts) > 1 else "unknown"

            for specimen_dir in species_dir.iterdir():
                if not specimen_dir.is_dir():
                    continue

                specimen_code = specimen_dir.name

                # Collect all image files for this specimen
                images = list(specimen_dir.glob("*.jpg")) + list(specimen_dir.glob("*.jpeg"))
                images = [p for p in images if not p.name.startswith(".")]

                if images:
                    specimens[specimen_code] = {
                        "images": images,
                        "subfamily": subfamily,
                        "genus": genus,
                        "species": species,
                        "specimen_dir": specimen_dir,
                    }

    return specimens


def split_specimens(specimens, seed=RANDOM_SEED):
    """
    Split specimens into train/val/test sets.

    CRITICAL: All images from one specimen go into the same split.
    This prevents data leakage where the model sees the same ant in training and test.
    """
    random.seed(seed)

    specimen_codes = list(specimens.keys())
    random.shuffle(specimen_codes)

    n_total = len(specimen_codes)
    n_train = int(n_total * SPLIT_RATIOS["train"])
    n_val = int(n_total * SPLIT_RATIOS["val"])

    splits = {
        "train": specimen_codes[:n_train],
        "val": specimen_codes[n_train:n_train + n_val],
        "test": specimen_codes[n_train + n_val:],
    }

    return splits


def create_split_log(specimens, splits):
    """Create a log of the split for reproducibility and verification."""
    log = {
        "created": datetime.now().isoformat(),
        "random_seed": RANDOM_SEED,
        "split_ratios": SPLIT_RATIOS,
        "totals": {
            "specimens": len(specimens),
            "train_specimens": len(splits["train"]),
            "val_specimens": len(splits["val"]),
            "test_specimens": len(splits["test"]),
        },
        "splits": {},
    }

    for split_name, specimen_codes in splits.items():
        log["splits"][split_name] = []
        for code in specimen_codes:
            spec = specimens[code]
            log["splits"][split_name].append({
                "specimen_code": code,
                "subfamily": spec["subfamily"],
                "genus": spec["genus"],
                "species": spec["species"],
                "image_count": len(spec["images"]),
            })

    return log


# =============================================================================
# MAIN PROCESSING PIPELINE
# =============================================================================

class ImagePreprocessor:
    """Main preprocessing pipeline."""

    def __init__(self, raw_dir=None, output_dir=None, augmentations=None):
        self.raw_dir = Path(raw_dir) if raw_dir else RAW_DIR
        self.output_dir = Path(output_dir) if output_dir else PROCESSED_DIR
        self.augmentations = augmentations or DEFAULT_AUGMENTATIONS

        self.stats = {
            "specimens_processed": 0,
            "images_processed": 0,
            "augmentations_created": 0,
            "errors": 0,
        }

    def process_all(self, skip_augmentation=False, split_only=False, augment_only=False):
        """Run the full preprocessing pipeline."""

        if not PIL_AVAILABLE:
            print("ERROR: PIL/Pillow is required. Install with: pip install Pillow")
            return

        print("=" * 60)
        print("ANTWORLD Image Preprocessing Pipeline")
        print("=" * 60)
        print(f"Raw images: {self.raw_dir}")
        print(f"Output: {self.output_dir}")
        print(f"Target size: {TARGET_SIZE}")
        print(f"Split ratios: {SPLIT_RATIOS}")
        print(f"Augmentations: {len(self.augmentations)} types")
        print("-" * 60)

        # Step 1: Collect all specimens
        print("\n[1/4] Collecting specimens from raw directory...")
        specimens = collect_specimens(self.raw_dir)
        print(f"  Found {len(specimens)} specimens")

        if not specimens:
            print("ERROR: No specimens found in raw directory")
            return

        # Step 2: Create specimen-based splits
        print("\n[2/4] Creating specimen-based train/val/test splits...")
        splits = split_specimens(specimens)
        print(f"  Train: {len(splits['train'])} specimens")
        print(f"  Val: {len(splits['val'])} specimens")
        print(f"  Test: {len(splits['test'])} specimens")

        # Save split log
        split_log = create_split_log(specimens, splits)
        SPLIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SPLIT_LOG_FILE, "w") as f:
            json.dump(split_log, f, indent=2)
        print(f"  Split log saved to: {SPLIT_LOG_FILE}")

        if split_only:
            print("\n--split-only flag set, stopping here.")
            return split_log

        # Step 3: Process images
        print("\n[3/4] Processing images...")

        for split_name, specimen_codes in splits.items():
            split_dir = self.output_dir / split_name / "ant"
            split_dir.mkdir(parents=True, exist_ok=True)

            print(f"\n  Processing {split_name} split ({len(specimen_codes)} specimens)...")

            for i, specimen_code in enumerate(specimen_codes):
                spec = specimens[specimen_code]
                self._process_specimen(specimen_code, spec, split_dir, skip_augmentation)

                if (i + 1) % 10 == 0:
                    print(f"    Processed {i + 1}/{len(specimen_codes)} specimens")

        # Step 4: Summary
        print("\n" + "=" * 60)
        print("PREPROCESSING COMPLETE")
        print("=" * 60)
        print(f"Specimens processed: {self.stats['specimens_processed']}")
        print(f"Original images: {self.stats['images_processed']}")
        print(f"Augmented images: {self.stats['augmentations_created']}")
        print(f"Total images: {self.stats['images_processed'] + self.stats['augmentations_created']}")
        print(f"Errors: {self.stats['errors']}")

        return self.stats

    def _process_specimen(self, specimen_code, spec_info, output_dir, skip_augmentation=False):
        """Process all images for a single specimen."""

        for img_path in spec_info["images"]:
            try:
                # Load and resize image
                img = Image.open(img_path).convert("RGB")
                img = resize_image(img, TARGET_SIZE)

                # Save original (resized)
                base_name = img_path.stem
                original_path = output_dir / f"{base_name}_original.jpg"
                img.save(original_path, "JPEG", quality=95)
                self.stats["images_processed"] += 1

                # Apply augmentations (only on training set typically, but we do all for now)
                if not skip_augmentation:
                    for aug_name in self.augmentations:
                        aug_config = AUGMENTATIONS.get(aug_name)
                        if not aug_config:
                            continue

                        try:
                            aug_img = apply_augmentation(img.copy(), aug_name, aug_config)
                            aug_path = output_dir / f"{base_name}_{aug_name}.jpg"
                            aug_img.save(aug_path, "JPEG", quality=90)
                            self.stats["augmentations_created"] += 1
                        except Exception as e:
                            # Some augmentations may fail (e.g., noise without numpy)
                            pass

            except Exception as e:
                print(f"      ERROR processing {img_path}: {e}")
                self.stats["errors"] += 1

        self.stats["specimens_processed"] += 1


# =============================================================================
# VERIFICATION
# =============================================================================

def verify_no_leakage(split_log):
    """Verify that no specimen appears in multiple splits."""
    all_specimens = set()
    duplicates = []

    for split_name, specimens in split_log["splits"].items():
        for spec in specimens:
            code = spec["specimen_code"]
            if code in all_specimens:
                duplicates.append(code)
            all_specimens.add(code)

    if duplicates:
        print(f"ERROR: Data leakage detected! Specimens in multiple splits: {duplicates}")
        return False
    else:
        print("VERIFIED: No data leakage - each specimen appears in exactly one split")
        return True


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Preprocess ant images for ML training"
    )
    parser.add_argument(
        "--raw-dir",
        help="Input directory with raw images"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for processed images"
    )
    parser.add_argument(
        "--no-augment",
        action="store_true",
        help="Skip augmentation, only resize and split"
    )
    parser.add_argument(
        "--split-only",
        action="store_true",
        help="Only create splits, don't process images"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify existing split has no leakage"
    )

    args = parser.parse_args()

    if args.verify:
        if SPLIT_LOG_FILE.exists():
            with open(SPLIT_LOG_FILE) as f:
                split_log = json.load(f)
            verify_no_leakage(split_log)
        else:
            print(f"No split log found at {SPLIT_LOG_FILE}")
        return

    preprocessor = ImagePreprocessor(
        raw_dir=args.raw_dir,
        output_dir=args.output_dir,
    )

    preprocessor.process_all(
        skip_augmentation=args.no_augment,
        split_only=args.split_only,
    )


if __name__ == "__main__":
    main()
