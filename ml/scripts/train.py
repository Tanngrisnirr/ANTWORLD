#!/usr/bin/env python3
"""
AntWorld ML Training Script
Binary classification: Ant recognized vs Cannot identify

Uses MobileNetV2 transfer learning for browser deployment.
No external API calls - all local processing.
"""

import os
import json
import numpy as np
from pathlib import Path
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
CONFIG_PATH = SCRIPT_DIR.parent / "config.json"
TRAINING_DATA = PROJECT_DIR / "TrainingSets"
MODELS_DIR = SCRIPT_DIR.parent / "models"
CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
SAVED_MODEL_DIR = MODELS_DIR / "saved_model"

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

IMG_SIZE = tuple(config["model"]["input_size"][:2])  # (224, 224)
BATCH_SIZE = config["training"]["batch_size"]
EPOCHS = config["training"]["epochs"]
VALIDATION_SPLIT = config["training"]["validation_split"]
LEARNING_RATE = config["training"]["learning_rate"]
FINE_TUNE_LAYERS = config["training"]["fine_tune_layers"]


def load_images_from_folder(folder_path, label):
    """Load all images from a folder with given label."""
    images = []
    labels = []
    folder = Path(folder_path)

    for img_path in folder.glob("*"):
        if img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            try:
                img = Image.open(img_path).convert("RGB")
                img = img.resize(IMG_SIZE)
                img_array = np.array(img) / 255.0  # Normalize to [0, 1]
                images.append(img_array)
                labels.append(label)
                print(f"  Loaded: {img_path.name}")
            except Exception as e:
                print(f"  Error loading {img_path.name}: {e}")

    return images, labels


def load_training_data():
    """Load all training images from TrainingSets folder."""
    all_images = []
    all_labels = []
    class_names = []

    print("\nLoading training data...")

    for folder in sorted(TRAINING_DATA.iterdir()):
        if folder.is_dir() and folder.name.startswith("Stack_"):
            class_name = folder.name.replace("Stack_", "").replace("_", " ")
            class_idx = len(class_names)
            class_names.append(class_name)

            print(f"\nClass {class_idx}: {class_name}")
            images, labels = load_images_from_folder(folder, class_idx)
            all_images.extend(images)
            all_labels.extend(labels)

    X = np.array(all_images)
    y = np.array(all_labels)

    print(f"\nTotal images: {len(X)}")
    print(f"Classes: {class_names}")

    return X, y, class_names


def create_model(num_classes):
    """Create MobileNetV2-based model for transfer learning."""

    # Load pretrained MobileNetV2 (no top layers)
    base_model = keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )

    # Freeze base model initially
    base_model.trainable = False

    # Add classification head
    model = keras.Sequential([
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model, base_model


def fine_tune_model(model, base_model):
    """Unfreeze top layers of base model for fine-tuning."""

    base_model.trainable = True

    # Freeze all except last N layers
    for layer in base_model.layers[:-FINE_TUNE_LAYERS]:
        layer.trainable = False

    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def main():
    print("=" * 60)
    print("AntWorld ML Training")
    print("=" * 60)

    # Load data
    X, y, class_names = load_training_data()

    if len(X) == 0:
        print("No training data found!")
        return

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y,
        test_size=VALIDATION_SPLIT,
        random_state=42,
        stratify=y
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")

    # Create model
    num_classes = len(class_names)
    print(f"\nCreating model for {num_classes} classes...")
    model, base_model = create_model(num_classes)
    model.summary()

    # Data augmentation
    data_augmentation = keras.Sequential([
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.2),
        keras.layers.RandomZoom(0.1),
        keras.layers.RandomContrast(0.1),
    ])

    # Augment training data
    X_train_aug = np.concatenate([X_train, data_augmentation(X_train).numpy()])
    y_train_aug = np.concatenate([y_train, y_train])

    print(f"After augmentation: {len(X_train_aug)} training samples")

    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=10,
            restore_best_weights=True
        ),
        keras.callbacks.ModelCheckpoint(
            CHECKPOINTS_DIR / "best_model.keras",
            monitor="val_accuracy",
            save_best_only=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=5
        )
    ]

    # Phase 1: Train with frozen base
    print("\n" + "=" * 60)
    print("Phase 1: Training classification head...")
    print("=" * 60)

    history1 = model.fit(
        X_train_aug, y_train_aug,
        epochs=EPOCHS // 2,
        batch_size=BATCH_SIZE,
        validation_data=(X_val, y_val),
        callbacks=callbacks
    )

    # Phase 2: Fine-tune
    print("\n" + "=" * 60)
    print("Phase 2: Fine-tuning top layers...")
    print("=" * 60)

    model = fine_tune_model(model, base_model)

    history2 = model.fit(
        X_train_aug, y_train_aug,
        epochs=EPOCHS // 2,
        batch_size=BATCH_SIZE,
        validation_data=(X_val, y_val),
        callbacks=callbacks
    )

    # Evaluate
    print("\n" + "=" * 60)
    print("Final Evaluation")
    print("=" * 60)

    loss, accuracy = model.evaluate(X_val, y_val)
    print(f"\nValidation Loss: {loss:.4f}")
    print(f"Validation Accuracy: {accuracy:.4f}")

    # Save model
    print("\nSaving model...")
    SAVED_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save(SAVED_MODEL_DIR / "ant_classifier")

    # Save class names
    with open(SAVED_MODEL_DIR / "class_names.json", "w") as f:
        json.dump(class_names, f, indent=2)

    print(f"\nModel saved to: {SAVED_MODEL_DIR}")
    print("\nNext step: Convert to TensorFlow.js format")
    print("  tensorflowjs_converter --input_format=tf_saved_model \\")
    print(f"    {SAVED_MODEL_DIR}/ant_classifier \\")
    print(f"    {PROJECT_DIR}/antworld.org/alpha/js/ml/ant_model/")


if __name__ == "__main__":
    main()
