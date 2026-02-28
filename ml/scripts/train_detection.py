#!/usr/bin/env python3
"""
AntWorld ML - Object Detection Training Script
Detects ant body parts: head, mesosoma, metasoma, petiole, antenna, leg

Uses SSD with MobileNetV2 backbone for browser deployment.
All local processing - no external API calls.
"""

import os
import json
import numpy as np
from pathlib import Path
from PIL import Image
import tensorflow as tf
from tensorflow import keras

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
CONFIG_PATH = SCRIPT_DIR.parent / "config_detection.json"

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

IMG_SIZE = tuple(config["model"]["input_size"][:2])
CLASSES = config["classes"]
NUM_CLASSES = len(CLASSES)
BATCH_SIZE = config["training"]["batch_size"]
EPOCHS = config["training"]["epochs"]
LEARNING_RATE = config["training"]["learning_rate"]

ANNOTATIONS_DIR = PROJECT_DIR / config["paths"]["annotations"].lstrip("../")
IMAGES_DIR = PROJECT_DIR / config["paths"]["images"].lstrip("../")
MODELS_DIR = SCRIPT_DIR.parent / "models" / "detection"


def parse_pascal_voc(xml_path):
    """Parse Pascal VOC format annotation file."""
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_path)
    root = tree.getroot()

    boxes = []
    labels = []

    for obj in root.findall("object"):
        label = obj.find("name").text.lower()
        if label in CLASSES:
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(CLASSES.index(label))

    return np.array(boxes), np.array(labels)


def parse_yolo(txt_path, img_width, img_height):
    """Parse YOLO format annotation file."""
    boxes = []
    labels = []

    with open(txt_path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                class_id = int(parts[0])
                x_center = float(parts[1]) * img_width
                y_center = float(parts[2]) * img_height
                width = float(parts[3]) * img_width
                height = float(parts[4]) * img_height

                xmin = x_center - width / 2
                ymin = y_center - height / 2
                xmax = x_center + width / 2
                ymax = y_center + height / 2

                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(class_id)

    return np.array(boxes), np.array(labels)


def load_dataset():
    """Load images and annotations."""
    images = []
    all_boxes = []
    all_labels = []

    print("\nLoading dataset...")
    print(f"Images dir: {IMAGES_DIR}")
    print(f"Annotations dir: {ANNOTATIONS_DIR}")

    if not IMAGES_DIR.exists():
        print(f"ERROR: Images directory not found: {IMAGES_DIR}")
        return None, None, None

    for img_path in IMAGES_DIR.glob("*"):
        if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue

        # Look for annotation file
        xml_path = ANNOTATIONS_DIR / f"{img_path.stem}.xml"
        txt_path = ANNOTATIONS_DIR / f"{img_path.stem}.txt"

        boxes = None
        labels = None

        if xml_path.exists():
            boxes, labels = parse_pascal_voc(xml_path)
        elif txt_path.exists():
            img = Image.open(img_path)
            boxes, labels = parse_yolo(txt_path, img.width, img.height)
        else:
            print(f"  No annotation for: {img_path.name}")
            continue

        if len(boxes) == 0:
            continue

        # Load and resize image
        img = Image.open(img_path).convert("RGB")
        orig_w, orig_h = img.size
        img = img.resize(IMG_SIZE)

        # Scale boxes to new size
        scale_x = IMG_SIZE[0] / orig_w
        scale_y = IMG_SIZE[1] / orig_h
        boxes = boxes * np.array([scale_x, scale_y, scale_x, scale_y])

        # Normalize image
        img_array = np.array(img) / 255.0

        images.append(img_array)
        all_boxes.append(boxes)
        all_labels.append(labels)

        print(f"  Loaded: {img_path.name} ({len(boxes)} objects)")

    print(f"\nTotal images: {len(images)}")
    return images, all_boxes, all_labels


def create_ssd_model():
    """Create SSD-like detection model with MobileNetV2 backbone."""

    # Load MobileNetV2 as backbone
    backbone = keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )
    backbone.trainable = False

    # Get feature maps from different levels
    c4 = backbone.get_layer("block_13_expand_relu").output  # 20x20
    c5 = backbone.get_layer("out_relu").output  # 10x10

    # Detection head for c4 (larger objects)
    x4 = keras.layers.Conv2D(256, 3, padding="same", activation="relu")(c4)
    x4 = keras.layers.Conv2D(256, 3, padding="same", activation="relu")(x4)

    # Each cell predicts: 4 box coords + num_classes scores per anchor
    # Using 3 anchors per cell
    num_anchors = 3
    box_output_4 = keras.layers.Conv2D(num_anchors * 4, 3, padding="same")(x4)
    class_output_4 = keras.layers.Conv2D(num_anchors * (NUM_CLASSES + 1), 3, padding="same")(x4)

    # Detection head for c5 (smaller objects)
    x5 = keras.layers.Conv2D(256, 3, padding="same", activation="relu")(c5)
    x5 = keras.layers.Conv2D(256, 3, padding="same", activation="relu")(x5)

    box_output_5 = keras.layers.Conv2D(num_anchors * 4, 3, padding="same")(x5)
    class_output_5 = keras.layers.Conv2D(num_anchors * (NUM_CLASSES + 1), 3, padding="same")(x5)

    # Reshape outputs
    box_4 = keras.layers.Reshape((-1, 4))(box_output_4)
    class_4 = keras.layers.Reshape((-1, NUM_CLASSES + 1))(class_output_4)

    box_5 = keras.layers.Reshape((-1, 4))(box_output_5)
    class_5 = keras.layers.Reshape((-1, NUM_CLASSES + 1))(class_output_5)

    # Concatenate all predictions
    boxes = keras.layers.Concatenate(axis=1)([box_4, box_5])
    classes = keras.layers.Concatenate(axis=1)([class_4, class_5])
    classes = keras.layers.Softmax()(classes)

    model = keras.Model(
        inputs=backbone.input,
        outputs=[boxes, classes]
    )

    return model, backbone


def detection_loss(y_true_boxes, y_true_classes, y_pred_boxes, y_pred_classes):
    """Combined localization and classification loss."""

    # Smooth L1 loss for box regression
    box_loss = tf.losses.huber(y_true_boxes, y_pred_boxes)

    # Cross-entropy for classification
    class_loss = tf.losses.sparse_categorical_crossentropy(
        y_true_classes, y_pred_classes
    )

    return box_loss + class_loss


def main():
    print("=" * 60)
    print("AntWorld ML - Object Detection Training")
    print("=" * 60)
    print(f"\nClasses: {CLASSES}")

    # Load data
    images, boxes, labels = load_dataset()

    if images is None or len(images) == 0:
        print("\n" + "=" * 60)
        print("NO TRAINING DATA FOUND!")
        print("=" * 60)
        print("\nTo train the object detection model, you need to:")
        print("")
        print("1. Copy ant images to:")
        print(f"   {IMAGES_DIR}/")
        print("")
        print("2. Create annotations (bounding boxes) in:")
        print(f"   {ANNOTATIONS_DIR}/")
        print("")
        print("Supported annotation formats:")
        print("  - Pascal VOC (.xml) - use LabelImg")
        print("  - YOLO (.txt) - use LabelImg or CVAT")
        print("")
        print("Recommended tool: LabelImg")
        print("  pip install labelImg")
        print("  labelImg")
        print("")
        print("Classes to annotate:")
        for i, cls in enumerate(CLASSES):
            print(f"  {i}: {cls}")
        return

    # Create model
    print("\nCreating SSD MobileNetV2 model...")
    model, backbone = create_ssd_model()
    model.summary()

    # For now, just show that setup is complete
    print("\n" + "=" * 60)
    print("Model created successfully!")
    print("=" * 60)
    print(f"\nFound {len(images)} annotated images")
    print("Ready for training once more annotations are added.")
    print("")
    print("Minimum recommended: 50+ images with annotations")
    print("For good accuracy: 200+ images per class")

    # Save model architecture
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model.save(MODELS_DIR / "ssd_mobilenetv2_untrained")
    print(f"\nUntrained model saved to: {MODELS_DIR}")


if __name__ == "__main__":
    main()
