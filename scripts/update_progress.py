#!/usr/bin/env python3
"""
Update ANTWORLD ML Progress Charter

Scans downloaded images and training logs to update:
- ml/progress.json (machine-readable)
- ml/PROGRESS.md (GitHub-friendly markdown)

Usage:
    python update_progress.py           # Full update
    python update_progress.py --json    # Only update JSON
    python update_progress.py --md      # Only update markdown
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
ML_DIR = PROJECT_ROOT / "ml"
TRAINING_SETS_DIR = PROJECT_ROOT / "TrainingSets"
RAW_DIR = TRAINING_SETS_DIR / "raw"
PROCESSED_DIR = TRAINING_SETS_DIR / "processed"

PROGRESS_JSON = ML_DIR / "progress.json"
PROGRESS_MD = ML_DIR / "PROGRESS.md"
TARGET_SPECIES_FILE = ML_DIR / "target_species.json"


def count_raw_images():
    """Count images in raw directory by species."""
    species_counts = defaultdict(lambda: {"images": 0, "specimens": 0})
    subfamily_counts = defaultdict(int)
    total_images = 0
    total_specimens = 0

    if not RAW_DIR.exists():
        return species_counts, subfamily_counts, 0, 0

    for subfamily_dir in RAW_DIR.iterdir():
        if not subfamily_dir.is_dir():
            continue

        subfamily = subfamily_dir.name

        for species_dir in subfamily_dir.iterdir():
            if not species_dir.is_dir():
                continue

            parts = species_dir.name.split("_", 1)
            genus = parts[0] if parts else "unknown"
            species = parts[1] if len(parts) > 1 else "unknown"
            key = f"{genus}_{species}"

            for specimen_dir in species_dir.iterdir():
                if not specimen_dir.is_dir():
                    continue

                images = list(specimen_dir.glob("*.jpg")) + list(specimen_dir.glob("*.jpeg"))
                image_count = len([p for p in images if not p.name.startswith(".")])

                if image_count > 0:
                    species_counts[key]["images"] += image_count
                    species_counts[key]["specimens"] += 1
                    species_counts[key]["subfamily"] = subfamily
                    species_counts[key]["genus"] = genus
                    species_counts[key]["species"] = species
                    total_images += image_count
                    total_specimens += 1
                    subfamily_counts[subfamily] += 1

    return dict(species_counts), dict(subfamily_counts), total_images, total_specimens


def count_processed_images():
    """Count images in processed directory by split."""
    counts = {"train": 0, "val": 0, "test": 0}

    for split in counts.keys():
        split_dir = PROCESSED_DIR / split / "ant"
        if split_dir.exists():
            counts[split] = len(list(split_dir.glob("*.jpg")))

    return counts


def update_progress_json(species_counts, subfamily_counts, total_images, total_specimens, processed_counts):
    """Update the progress.json file with current counts."""

    # Load existing progress
    if PROGRESS_JSON.exists():
        with open(PROGRESS_JSON) as f:
            progress = json.load(f)
    else:
        progress = {}

    # Update timestamp
    progress["last_updated"] = datetime.now().isoformat()

    # Update data collection stats
    progress.setdefault("data_collection", {})
    progress["data_collection"]["subfamilies"] = {
        "current": len(subfamily_counts),
        "target": 17,
    }
    progress["data_collection"]["species"] = {
        "current": len(species_counts),
        "target": progress["data_collection"].get("species", {}).get("target", 32),
    }
    progress["data_collection"]["specimens"] = {
        "current": total_specimens,
        "target": None,
    }
    progress["data_collection"]["images"] = {
        "current": total_images,
        "target": progress["data_collection"].get("images", {}).get("target", 960),
    }

    # Update preprocessing stats
    progress.setdefault("preprocessing", {})
    progress["preprocessing"]["train_images"] = processed_counts["train"]
    progress["preprocessing"]["val_images"] = processed_counts["val"]
    progress["preprocessing"]["test_images"] = processed_counts["test"]
    total_processed = sum(processed_counts.values())
    progress["preprocessing"]["status"] = "complete" if total_processed > 0 else "not_started"

    # Update species status
    if "species_status" in progress:
        for spec in progress["species_status"]:
            key = f"{spec['genus']}_{spec['species']}"
            if key in species_counts:
                spec["images"] = species_counts[key]["images"]
                spec["status"] = "complete" if species_counts[key]["images"] > 0 else "pending"

    # Update milestones
    if "milestones" in progress:
        for milestone in progress["milestones"]:
            if milestone["name"] == "First Species Scraped" and len(species_counts) > 0:
                milestone["completed"] = True
                if not milestone.get("completed_date"):
                    milestone["completed_date"] = datetime.now().strftime("%Y-%m-%d")

            if milestone["name"] == "All Species Scraped":
                target = progress["data_collection"]["species"]["target"]
                if len(species_counts) >= target:
                    milestone["completed"] = True
                    if not milestone.get("completed_date"):
                        milestone["completed_date"] = datetime.now().strftime("%Y-%m-%d")

            if milestone["name"] == "Preprocessing Complete" and total_processed > 0:
                milestone["completed"] = True
                if not milestone.get("completed_date"):
                    milestone["completed_date"] = datetime.now().strftime("%Y-%m-%d")

    # Save updated progress
    with open(PROGRESS_JSON, "w") as f:
        json.dump(progress, f, indent=2)

    return progress


def generate_progress_bar(current, target, width=20):
    """Generate a text-based progress bar."""
    if target is None or target == 0:
        return "[" + "?" * width + "]"

    filled = int(width * min(current / target, 1.0))
    empty = width - filled
    percent = int(100 * current / target)
    return f"[{'█' * filled}{'░' * empty}] {percent}%"


def update_progress_md(progress):
    """Generate the PROGRESS.md file from progress.json."""

    # Calculate progress percentages
    dc = progress.get("data_collection", {})
    subfam_pct = int(100 * dc.get("subfamilies", {}).get("current", 0) / max(dc.get("subfamilies", {}).get("target", 17), 1))
    species_pct = int(100 * dc.get("species", {}).get("current", 0) / max(dc.get("species", {}).get("target", 32), 1))
    images_pct = int(100 * dc.get("images", {}).get("current", 0) / max(dc.get("images", {}).get("target", 960), 1))

    # Build species table
    species_rows = []
    for spec in progress.get("species_status", [])[:15]:  # Show first 15
        status_emoji = "✅" if spec.get("status") == "complete" else "⏳"
        species_rows.append(
            f"| {spec['subfamily']} | *{spec['genus']} {spec['species']}* | {spec.get('images', 0)} | {status_emoji} {spec.get('status', 'pending').title()} |"
        )

    remaining = len(progress.get("species_status", [])) - 15
    if remaining > 0:
        species_rows.append(f"| ... | *({remaining} more species)* | ... | ... |")

    # Build milestones
    milestone_lines = []
    for m in progress.get("milestones", []):
        check = "x" if m.get("completed") else " "
        date_str = f" ({m['completed_date']})" if m.get("completed_date") else ""
        milestone_lines.append(f"- [{check}] **{m['name']}**{date_str}")

    # Build model status tables
    def model_table(model_data):
        status = model_data.get("status", "not_started").replace("_", " ").title()
        train_acc = f"{model_data.get('accuracy', '--')}%" if model_data.get('accuracy') else "--"
        val_acc = f"{model_data.get('val_accuracy', '--')}%" if model_data.get('val_accuracy') else "--"
        test_acc = f"{model_data.get('test_accuracy', '--')}%" if model_data.get('test_accuracy') else "--"
        return f"""| Metric | Value |
|--------|-------|
| Status | {status} |
| Training Accuracy | {train_acc} |
| Validation Accuracy | {val_acc} |
| Test Accuracy | {test_acc} |"""

    models = progress.get("models", {})
    gate0_table = model_table(models.get("gate0", {}))
    gate1_table = model_table(models.get("gate1", {}))
    subfamily_table = model_table(models.get("subfamily", {}))

    # Generate markdown
    md_content = f"""# ANTWORLD ML Progress Charter

> **Goal:** Build a proof-of-concept ant recognition model and rally community support for more training data.

**Last Updated:** {progress.get('last_updated', 'Unknown')[:10]}

---

## Data Collection Progress

| Metric | Current | Target | Progress |
|--------|---------|--------|----------|
| Subfamilies | {dc.get('subfamilies', {}).get('current', 0)} | {dc.get('subfamilies', {}).get('target', 17)} | ![](https://progress-bar.dev/{subfam_pct}/?width=200) |
| Species | {dc.get('species', {}).get('current', 0)} | {dc.get('species', {}).get('target', 32)} | ![](https://progress-bar.dev/{species_pct}/?width=200) |
| Specimens | {dc.get('specimens', {}).get('current', 0)} | -- | -- |
| Images | {dc.get('images', {}).get('current', 0)} | ~{dc.get('images', {}).get('target', 960)} | ![](https://progress-bar.dev/{images_pct}/?width=200) |

### Species Status

| Subfamily | Species | Images | Status |
|-----------|---------|--------|--------|
{chr(10).join(species_rows)}

---

## Model Training Progress

### Gate 0: Binary Ant Detector
> "Is this an ant?"

{gate0_table}

### Gate 1: Quality Assessor
> "Is this photo usable?"

{gate1_table}

### Subfamily Classifier
> "Which of 17 subfamilies?"

{subfamily_table}

---

## Milestones

{chr(10).join(milestone_lines)}

---

## How You Can Help

We need **more ant images** to improve accuracy! Even lower-quality photos help train the model to handle real-world conditions.

### Image Requirements
- Clear view of the ant (head, profile, or dorsal)
- Identified to at least subfamily level
- Any quality welcome (we use degradation augmentation)

### Priority Taxa
- Rare subfamilies: Leptanillinae, Martialinae, Aneuretinae
- "Odd" morphologies: army ants, trap-jaw ants, bulldog ants
- Regional gaps: check species_status for needs

### How to Contribute
1. Submit images via [GitHub Issues](../../issues)
2. AntWeb contribution: https://www.antweb.org/participate.do

---

## Technical Details

### Data Pipeline
```
AntWeb.org → Scraper → Raw Images → Preprocessing → Train/Val/Test
                                    ├── Resize (224x224)
                                    ├── Specimen-based split (no leakage)
                                    └── Augmentation (24x)
                                        ├── Rotation (±15°)
                                        ├── Brightness
                                        ├── Blur (degradation)
                                        ├── JPEG artifacts
                                        ├── Noise
                                        └── Low resolution
```

### No Data Leakage Guarantee
All images from the same **specimen** (individual ant) stay in the same split bucket. The model never sees the same ant in both training and testing.

### Model Architecture
- Base: MobileNetV2 (3.5M parameters)
- Input: 224×224×3
- Output: Binary (ant/not-ant) or multi-class
- Target size: ~10-15MB for browser deployment

---

## Attribution

Training images sourced from [AntWeb.org](https://www.antweb.org) under CC BY license.

> AntWeb. Version 8.114. California Academy of Science, online at https://www.antweb.org

---

*This charter is auto-generated from `ml/progress.json`. Run `scripts/update_progress.py` to refresh.*
"""

    with open(PROGRESS_MD, "w") as f:
        f.write(md_content)

    return md_content


def main():
    parser = argparse.ArgumentParser(description="Update ML progress tracking files")
    parser.add_argument("--json", action="store_true", help="Only update JSON")
    parser.add_argument("--md", action="store_true", help="Only update markdown")
    args = parser.parse_args()

    print("Scanning directories...")

    # Count raw images
    species_counts, subfamily_counts, total_images, total_specimens = count_raw_images()
    print(f"  Raw: {total_images} images from {total_specimens} specimens across {len(species_counts)} species")

    # Count processed images
    processed_counts = count_processed_images()
    total_processed = sum(processed_counts.values())
    print(f"  Processed: {total_processed} images (train: {processed_counts['train']}, val: {processed_counts['val']}, test: {processed_counts['test']})")

    if not args.md:
        # Update JSON
        progress = update_progress_json(species_counts, subfamily_counts, total_images, total_specimens, processed_counts)
        print(f"  Updated: {PROGRESS_JSON}")

    if not args.json:
        # Load progress for markdown generation
        if PROGRESS_JSON.exists():
            with open(PROGRESS_JSON) as f:
                progress = json.load(f)
        else:
            progress = {}

        # Update markdown
        update_progress_md(progress)
        print(f"  Updated: {PROGRESS_MD}")

    print("\nDone!")


if __name__ == "__main__":
    main()
