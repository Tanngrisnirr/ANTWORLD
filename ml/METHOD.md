# AntWorld ML - Method & Approach

**Date:** 2026-02-28
**Status:** Infrastructure ready, awaiting training data

---

## 1. Project Goals

### Primary Goal
Help users identify ants from photographs using client-side ML (no server calls).

### Two-Stage Approach

```
User uploads image
        │
        ▼
┌───────────────────┐
│ Stage 1: Detection│  "Is this an ant? Where are body parts?"
│ (Object Detection)│
└─────────┬─────────┘
          │ If ant detected with body parts
          ▼
┌───────────────────┐
│ Stage 2: Identify │  "Which species? What features visible?"
│ (Classification)  │
└───────────────────┘
```

---

## 2. Why This Approach?

### Problem: "Not an Ant" Detection

**Original idea:** Binary classifier (ant vs not-ant)
- Requires massive "not ant" dataset (infinite variety)
- Hard to define what "not ant" means

**Our solution:** Confidence threshold + body part detection
- Train ONLY on ant images
- Low confidence = "Cannot identify"
- If no body parts detected = "Not recognizable as ant"
- No need for negative examples

### Advantage: Body Part Detection First

Instead of asking "is this an ant?", we ask "can I find ant body parts?"

- If we find head + mesosoma + metasoma → It's an ant
- If we find partial parts → "Partial view, try different angle"
- If we find nothing → "Cannot identify as ant"

This is more robust and provides actionable feedback.

---

## 3. Model Architecture

### Backbone: MobileNetV2

**Why MobileNetV2:**
- Open source (Apache 2.0)
- Pre-trained on ImageNet (knows insect-like shapes)
- Small (~14MB) - loads fast in browser
- Fast inference (~25ms)
- Designed for mobile/edge deployment

**Transfer Learning:**
- Use pre-trained weights
- Freeze early layers (general features)
- Fine-tune late layers (ant-specific features)

### Detection Head: SSD (Single Shot Detector)

**Why SSD:**
- Single forward pass (fast)
- Multi-scale detection (finds large and small parts)
- Works well with MobileNetV2 backbone
- TensorFlow.js compatible

**Architecture:**
```
Input Image (320×320×3)
        │
        ▼
┌─────────────────┐
│  MobileNetV2    │  Pre-trained backbone
│  (frozen)       │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│ C4    │ │ C5    │  Feature maps at different scales
│20×20  │ │10×10  │
└───┬───┘ └───┬───┘
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│ Det   │ │ Det   │  Detection heads
│ Head  │ │ Head  │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         ▼
┌─────────────────┐
│ Boxes + Classes │  Per-anchor predictions
│ NMS filtering   │
└─────────────────┘
```

---

## 4. Classes to Detect

| Class | Description | Importance |
|-------|-------------|------------|
| head | Head capsule (caput) | Critical for ID |
| mesosoma | Thorax region | Shape varies by species |
| metasoma | Abdomen + gaster | Size/shape diagnostic |
| petiole | Waist segment(s) | Key taxonomic feature |
| antenna | Antennae | Segment count diagnostic |
| leg | Legs | Proportions useful |

**Minimum for "ant detected":** head + mesosoma + metasoma

---

## 5. Training Data Strategy

### Data Sources

1. **AntWeb.org** (Primary)
   - Millions of standardized specimen photos
   - Multiple views: head (H), profile (P), dorsal (D)
   - CC BY license
   - High quality, consistent

2. **User submissions** (Future)
   - Real-world photos
   - Variable quality
   - Helps model generalize

3. **Data Augmentation**
   - Horizontal flip
   - Rotation (±15°)
   - Zoom (±10%)
   - Brightness variation
   - Effectively 5-10× more data

### Annotation Format

**Pascal VOC (.xml)** - Created with LabelImg

```xml
<annotation>
  <filename>ant_001.jpg</filename>
  <object>
    <name>head</name>
    <bndbox>
      <xmin>120</xmin>
      <ymin>80</ymin>
      <xmax>200</xmax>
      <ymax>160</ymax>
    </bndbox>
  </object>
  <object>
    <name>mesosoma</name>
    <bndbox>...</bndbox>
  </object>
</annotation>
```

### Recommended Dataset Size

| Stage | Minimum | Good | Excellent |
|-------|---------|------|-----------|
| Detection | 50 images | 200 images | 500+ images |
| Classification | 20/species | 100/species | 500+/species |

---

## 6. Inference Pipeline (Browser)

```javascript
// Load model once
const detector = await tf.loadGraphModel('js/ml/ant_detector/model.json');

// Process user image
const image = tf.browser.fromPixels(canvas);
const resized = tf.image.resizeBilinear(image, [320, 320]);
const normalized = resized.div(255.0);
const batched = normalized.expandDims(0);

// Run detection
const [boxes, scores, classes] = await detector.predict(batched);

// Filter by confidence
const detections = filterByConfidence(boxes, scores, classes, 0.5);

// Check if ant
if (hasRequiredParts(detections, ['head', 'mesosoma', 'metasoma'])) {
    showBodyPartOverlay(detections);
    proceedToIdentification();
} else {
    showMessage("Cannot identify as ant. Try a clearer image.");
}
```

---

## 7. Privacy & Offline Capability

**All processing is client-side:**
- Model loaded once, cached in browser
- Images never leave user's device
- Works offline after initial load
- No tracking, no data collection

This aligns with AntWorld's privacy-first policy.

---

## 8. Next Steps

### Phase 1: Detection (Current)
- [ ] Annotate 50+ images with LabelImg
- [ ] Train detection model
- [ ] Convert to TensorFlow.js
- [ ] Integrate into morpho.html

### Phase 2: Classification
- [ ] Expand species dataset
- [ ] Train classifier per body part
- [ ] Add species identification

### Phase 3: Feature Extraction
- [ ] Measure morphometric features from detected parts
- [ ] Compare to database
- [ ] Suggest possible species matches

---

## 9. Technical Notes

### Why Not YOLO?
- YOLOv5+ requires PyTorch (larger ecosystem)
- SSD MobileNetV2 is pure TensorFlow
- Easier TensorFlow.js conversion
- Similar accuracy for our use case

### Why Not Cloud API?
- AntWorld policy: no external server calls
- User privacy
- Offline capability
- No ongoing costs

### Browser Compatibility
- TensorFlow.js works in all modern browsers
- WebGL acceleration when available
- Falls back to CPU if needed
- Mobile-friendly (MobileNet designed for this)

---

## 10. References

- MobileNetV2: https://arxiv.org/abs/1801.04381
- SSD: https://arxiv.org/abs/1512.02325
- TensorFlow.js: https://www.tensorflow.org/js
- LabelImg: https://github.com/heartexlabs/labelImg
- AntWeb: https://www.antweb.org/
