# AntWorld ML - Training Guide

## Overview

Two ML tasks:
1. **Classification** - "Is this an ant?" (confidence threshold)
2. **Object Detection** - Find head, mesosoma, metasoma in image

Both use **MobileNetV2** backbone (Apache 2.0 license, fully open source).

## Setup

```bash
cd /var/mnt//Documents/WEB/ANTWORLD
source ml/venv/bin/activate
```

## Folder Structure

```
ml/
├── venv/                     # Python environment
├── scripts/
│   ├── train.py              # Classification training
│   ├── train_detection.py    # Object detection training
│   └── convert_to_tfjs.sh    # Convert to browser format
├── models/
│   ├── checkpoints/          # Training checkpoints
│   ├── saved_model/          # Classification model
│   └── detection/            # Detection model
├── config.json               # Classification config
├── config_detection.json     # Detection config
└── README.md                 # This file

TrainingSets/
├── images/                   # Training images (for detection)
├── annotations/              # Bounding box annotations
├── Stack_Formica_fusca/      # Existing classification data
└── Stack_Lasius_fuliginosus/ # Existing classification data
```

## Task 1: Classification

Already set up with existing data in `Stack_*` folders.

```bash
python ml/scripts/train.py
```

## Task 2: Object Detection (Body Parts)

### Step 1: Prepare Images

Copy ant images to:
```
TrainingSets/images/
```

### Step 2: Annotate with LabelImg

```bash
source ml/venv/bin/activate
labelImg TrainingSets/images TrainingSets/annotations
```

**Classes to annotate:**
- `head` - The head capsule
- `mesosoma` - Thorax region
- `metasoma` - Abdomen (gaster + petiole)
- `petiole` - Waist segment(s)
- `antenna` - Antennae
- `leg` - Legs

**Tips:**
- Draw tight bounding boxes around each part
- Save in Pascal VOC format (.xml)
- Aim for 50+ images minimum, 200+ for good accuracy

### Step 3: Train

```bash
python ml/scripts/train_detection.py
```

### Step 4: Convert for Browser

```bash
./ml/scripts/convert_to_tfjs.sh
```

## Data Sources

### AntWeb.org
Millions of standardized ant images. Can be scraped for training.
- High-resolution specimen photos
- Multiple views (head, profile, dorsal)
- CC BY license

### Your Own Photos
- Upload to `TrainingSets/images/`
- Annotate with LabelImg

## Model Architecture

### MobileNetV2 (Backbone)
- **License:** Apache 2.0 (open source)
- **Developer:** Google
- **Size:** ~14MB
- **Speed:** ~25ms inference on modern browser

### SSD (Detection Head)
- Single Shot Detector
- Multiple anchor boxes
- Real-time detection

## Browser Deployment

Models are converted to TensorFlow.js format:
```
antworld.org/alpha/js/ml/
├── ant_model/          # Classification model
└── ant_detector/       # Detection model
```

Load in JavaScript:
```javascript
const model = await tf.loadGraphModel('js/ml/ant_detector/model.json');
const predictions = model.predict(imageTensor);
```

## Minimum Requirements

| Task | Min Images | Recommended |
|------|-----------|-------------|
| Classification | 20/class | 100+/class |
| Detection | 50 total | 200+ total |

With data augmentation, these numbers are effectively 5-10x higher.
