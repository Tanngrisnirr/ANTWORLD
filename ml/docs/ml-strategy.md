# ANTWORLD ML Strategy

## Overview

This document consolidates the complete machine learning strategy for AntWorld, including architecture, training requirements, quality filtering, and deployment.

**Core principle:** Instead of one massive model trying to classify 936+ species, we use a **layered system** where specialized models handle each taxonomic level. The subfamily classifier doubles as the ant detector - if no subfamily matches with sufficient confidence, the image is rejected.

**Training approach:** Positive data only. We train on ant images exclusively. Non-recognition (low confidence across all classes) indicates "not an ant" - no negative samples needed.

---

## 1. Pre-Filtering Pipeline

Before classification begins, images pass through quality assessment. Non-ants are detected by the subfamily classifier's inability to match any subfamily with confidence.

### Quality Assessment (Gate 1)

**Purpose:** Reject photos that can't provide useful data.

```
User uploads image
       │
       ▼
┌───────────────────┐
│  QUALITY ASSESSOR │
│  Multi-label CNN  │
└───────────┬───────┘
            │
     ┌──────┴──────┐
     ▼             ▼
  USABLE       UNUSABLE
(continue)     (feedback)
                  │
                  ▼
         Specific feedback:
         • "Image too blurry"
         • "Ant too small in frame"
         • "Need profile view"
         • "Lighting too dark"
```

**Quality dimensions assessed:**

| Dimension | Pass | Fail |
|-----------|------|------|
| Focus/Blur | Sharp enough to see setae | Blurry, motion blur |
| Subject size | Subject fills >20% of frame | Subject tiny in landscape |
| Lighting | Even, diagnostic details visible | Over/underexposed |
| Angle | Head, profile, or dorsal | Unclear angle, partial |
| Occlusion | Key features visible | Covered by debris/fingers |

**Output:** Quality score (A-E) + specific improvement suggestions

| Grade | Meaning | Action |
|-------|---------|--------|
| A | Museum-grade | Full cascade, ML training data |
| B | Good macro | Full cascade |
| C | Acceptable field | Cascade with lower confidence |
| D | Poor but usable | Subfamily only, suggest retake |
| E | Unusable | Reject with feedback |

**Model:** Multi-output CNN (blur detection + object detection + exposure analysis)
**Training:** 5,000 graded ant images across quality spectrum
**Size:** ~15MB

### Combined Pipeline

```
User uploads image
        │
        ▼
┌───────────────────┐
│ Quality Assessment│──── GRADE E ───→ "Photo unusable: [reason]"
└────────┬──────────┘
         │ GRADE A-D
         ▼
┌───────────────────┐
│ Subfamily         │──── ALL < threshold ───→ "Not recognized as an ant"
│ Classifier        │
└────────┬──────────┘
         │ (match found)
         ▼
┌───────────────────┐
│ Genus → Species   │
│ Cascade           │
└───────────────────┘
```

**User experience:**
- Helpful feedback for poor photos
- Non-ants rejected via low confidence (no subfamily match)
- No wasted time on impossible identifications

---

## 2. Hierarchical Classification Architecture

### Cascade Diagram

```
                    ┌─────────────────────────┐
                    │      INPUT IMAGE        │
                    │   (passed Quality)      │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   SUBFAMILY CLASSIFIER  │
                    │      (17 classes)       │
                    │                         │
                    │  Also serves as:        │
                    │  ANT DETECTOR           │
                    │  (low conf = not ant)   │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
       ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
       │ Formicinae  │   │ Myrmicinae  │   │  Ponerinae  │  ...
       │ Genus Agent │   │ Genus Agent │   │ Genus Agent │
       │ (51 genera) │   │ (140 genera)│   │ (47 genera) │
       └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
              │                 │                 │
              ▼                 ▼                 ▼
       ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
       │   Formica   │   │   Myrmica   │   │  Ponera     │
       │Species Agent│   │Species Agent│   │Species Agent│
       │ (89 species)│   │ (45 species)│   │ (12 species)│
       └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
              │                 │                 │
              ▼                 ▼                 ▼
       ┌─────────────────────────────────────────────────┐
       │              FINAL IDENTIFICATION               │
       │   Species: Formica rufa                         │
       │   Confidence: 87%                               │
       │   Path: Formicinae → Formica → F. rufa          │
       └─────────────────────────────────────────────────┘
```

### Layer 1: Subfamily Classifier (+ Ant Detector)

**Single model, 17 classes, dual purpose:**
1. Classifies ants into subfamilies
2. Detects non-ants via low confidence across ALL classes

| Subfamily | Global Genera | Notes |
|-----------|---------------|-------|
| Agroecomyrmecinae | 2 | Neotropical only |
| Amblyoponinae | 13 | Worldwide |
| Aneuretinae | 1 | Sri Lanka endemic |
| Dolichoderinae | 22 | Worldwide |
| Dorylinae | 28 | Army/driver ants |
| Ectatomminae | 4 | Tropical |
| Formicinae | 51 | Largest, worldwide |
| Heteroponerinae | 3 | Tropical |
| Leptanillinae | 7 | Subterranean |
| Martialinae | 1 | Amazon, 1 species |
| Myrmeciinae | 2 | Australia only |
| Myrmicinae | 140 | Largest subfamily |
| Paraponerinae | 1 | Bullet ant |
| Ponerinae | 47 | Worldwide |
| Proceratiinae | 3 | Worldwide |
| Pseudomyrmecinae | 3 | Worldwide |

**Ant detection logic:**
```javascript
const predictions = model.predict(image); // 17 subfamily scores
const maxConfidence = Math.max(...predictions);

if (maxConfidence < RECOGNITION_THRESHOLD) {
  return { recognized: false, message: "Not recognized as an ant" };
}
// Continue with classification...
```

### Layer 2: Genus Classifiers (17 models)

One model per subfamily:

| Subfamily Model | Genera | Images Needed |
|-----------------|--------|---------------|
| Formicinae Agent | 51 | 7,650 |
| Myrmicinae Agent | 140 | 21,000 |
| Ponerinae Agent | 47 | 7,050 |
| Dolichoderinae Agent | 22 | 3,300 |
| Dorylinae Agent | 28 | 4,200 |
| Others (12) | ~37 | 5,550 |
| **TOTAL** | 370 | **49,200** |

### Layer 3: Species Classifiers (~300 models)

One model per genus (where >1 species). Monotypic genera skip this layer.

---

## 3. Confidence & Kickback System

### Thresholds

```javascript
const THRESHOLDS = {
  RECOGNITION: 0.30,  // Below this = not recognized as ant
  CONFIDENT: 0.85,    // Proceed to next layer
  UNCERTAIN: 0.50,    // Show options to user
  KICKBACK: 0.30      // Kick back up one layer
};
```

### Decision Flow

```
SUBFAMILY CLASSIFIER OUTPUT:

ALL CLASSES < 30% (recognition threshold):
→ "Not recognized as an ant"
   (No subfamily matched - likely not an ant)

MAX CLASS > 85% (confident):
→ "This is subfamily Formicinae"
   (Continue to genus classifier)

MAX CLASS 50-85% (uncertain):
→ "This appears to be one of:"
   1. Formicinae (62%)
   2. Myrmicinae (28%)
   (User selects, cascade continues)

MAX CLASS 30-50% (low confidence):
→ "Unable to determine subfamily"
   (Suggest better photo)
```

### Example Flows

**Successful:**
```
Input: ant_photo.jpg
→ Quality: Grade B ✓
→ Subfamily: Formicinae (97%) ✓
  → Genus: Formica (91%) ✓
    → Species: Formica rufa (88%) ✓

Result: Formica rufa (88% confidence)
```

**Kickback:**
```
Input: blurry_ant.jpg
→ Quality: Grade C (blurry)
→ Subfamily: Myrmicinae (72%) ✓
  → Genus: ??? (34%) ✗ KICKED BACK

Result: Myrmicinae (subfamily level only)
Suggestion: "Try profile view with clear petiole"
```

**Not recognized (non-ant or unrecognizable):**
```
Input: wasp_photo.jpg
→ Quality: Grade B ✓
→ Subfamily: ALL < 30%
  - Formicinae: 8%
  - Myrmicinae: 12%
  - Ponerinae: 5%
  - ... (all low)

Result: NOT RECOGNIZED
Message: "Not recognized as an ant"
```

---

## 4. Training Data Requirements

### Complete Pipeline Summary

**Training approach: Positive data only (ants)**

| Layer | Models | Classes | Images Needed | With Augmentation (24x) |
|-------|--------|---------|---------------|------------------------|
| Quality | 1 | 5 grades | 5,000 | 120,000 |
| Subfamily | 1 | 17 | 5,100 | 122,400 |
| Genus | 17 | 370 | 49,200 | 1,180,800 |
| Species | ~300 | ~3,000 | ~40,000 | 960,000 |
| **TOTAL** | **~319** | - | **~99,300** | ~2.4M |

### Comparison: Flat vs Hierarchical

| Approach | Models | Images Needed |
|----------|--------|---------------|
| Flat (1 model, all species) | 1 | 1,400,000+ |
| **Hierarchical** | ~319 | **~99,300** |
| **Savings** | - | **93%** |

### Data Augmentation Techniques

**Recommended:**

| Technique | Multiplier | Notes |
|-----------|------------|-------|
| Horizontal flip | 2x | Standard |
| Rotation (±15°) | 3x | Light rotation only |
| Brightness (±20%) | 2x | Simulate lighting |
| Crop variations | 2x | Random 90% crops |
| **Combined** | **~24x** | |

**NOT recommended for ants:**

| Technique | Why Avoid |
|-----------|-----------|
| Vertical flip | Ants don't appear upside-down |
| Heavy distortion | Destroys morphological features |
| Extreme color shifts | Color is diagnostic |

### Body Part Annotation Guidelines

**Bounding Boxes vs Polygons:**

| Part | Method | Notes |
|------|--------|-------|
| Head | Box | Include whole head, small pronotum overlap OK |
| Mesosoma | Box | Natural rectangular shape |
| Gaster | Box | Same |
| Petiole | Box | Tight box fine |
| Post-petiole | Box | If present |
| Legs | Box or Poly | Poly if bent/curved |
| Antennae | Poly preferred | Curved shapes benefit from polygons |
| Wings | Poly | Irregular shapes |
| Sting | Box | Small box if visible |

**Precision rules:**
- Boxes with ~80% target part coverage are acceptable
- Minor overlap with adjacent parts is fine (model learns from many examples)
- Don't agonize over pixel-perfect boundaries
- Save polygons for curved/irregular parts where boxes include too much background
- Multiple annotations per part allowed (6 legs, 2 antennae, etc.)

**Why overlap is OK:**
- Object detection models (YOLO, Faster R-CNN) expect some background in boxes
- IoU metrics account for this
- Model learns to focus on central object, not edges
- Hundreds of examples average out minor inconsistencies

---

## 5. Model Specifications

### Quality Assessor
```yaml
architecture: Custom multi-output CNN
input_size: 224x224
parameters: ~5M
output: 5 quality dimensions + grade
size_on_disk: ~15MB
inference_time: <75ms
```

### Subfamily Model (+ Ant Detection)
```yaml
architecture: MobileNetV2
input_size: 224x224
parameters: ~3.5M
output: 17 classes (softmax)
size_on_disk: ~14MB
inference_time: <100ms
note: Low max confidence = not recognized as ant
```

### Genus Models
```yaml
architecture: EfficientNet-B0 to B2
input_size: 224x224 to 260x260
parameters: 5-9M per model
output: varies (1-140 classes)
size_on_disk: 20-35MB each
inference_time: 100-200ms
```

### Species Models
```yaml
architecture: EfficientNet-B0
input_size: 224x224
parameters: ~5M per model
output: varies (2-100 classes)
size_on_disk: ~20MB each
inference_time: <150ms
```

---

## 6. Hardware Requirements

### Minimum (Quality + Subfamily training)
- CPU: Any modern multi-core
- RAM: 16GB
- Storage: 50GB SSD
- GPU: Optional but helpful

### Recommended (Full genus training)
- CPU: 8+ cores
- RAM: 32GB
- Storage: 500GB SSD
- GPU: NVIDIA GTX 1060+ (6GB VRAM)

### Optimal (Species training)
- CPU: 16+ cores
- RAM: 64GB+
- Storage: 2TB+ SSD
- GPU: NVIDIA RTX 3080+ (10GB+ VRAM)

### Cloud Options

| Provider | GPU | Cost/Hour | Best For |
|----------|-----|-----------|----------|
| Google Colab | T4 | Free (limited) | Prototyping |
| Colab Pro | T4/V100 | ~$10/month | Quality + Subfamily |
| Lambda Labs | A100 | $1.10/hour | Heavy training |

---

## 7. Deployment Strategy

### Web (Browser-based)

```
User uploads image
        │
        ▼
┌─────────────────┐
│ Quality model   │  ← Always loaded (~15MB)
│ (TensorFlow.js) │
└────────┬────────┘
         │ (if passes)
         ▼
┌─────────────────┐
│ Subfamily model │  ← Always loaded (~14MB)
│ (+ ant detect)  │
└────────┬────────┘
         │ (if recognized)
         ▼
┌─────────────────┐
│  Genus model    │  ← Lazy loaded on demand (~25MB)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Species model   │  ← Lazy loaded on demand (~20MB)
└─────────────────┘
```

**Total initial load:** ~29MB (Quality + Subfamily)
**Max additional load:** ~45MB (one Genus + one Species model)

---

## 8. Accuracy Expectations

### Per-Layer Targets

| Layer | Top-1 | Top-3 | Notes |
|-------|-------|-------|-------|
| Quality | 90%+ | N/A | <5% good photos rejected |
| Subfamily | 95% | 99% | Also detects non-ants |
| Genus | 85% | 95% | <10% kickback |
| Species | 75% | 90% | <15% kickback |

### Non-Ant Rejection
- Non-ant images should have max subfamily confidence <30%
- Expected rejection rate for non-ant inputs: >95%
- False negatives (ants rejected): <2%

### Combined End-to-End (Top-1)

```
Quality pass × Subfamily × Genus × Species
0.95 × 0.95 × 0.85 × 0.75 = 58% exact species
```

### With Top-3 Options

```
0.95 × 0.99 × 0.95 × 0.90 = 80% correct in top 3
```

### Practical User Experience

```
100 identifications submitted:
├── 10 → Rejected by Quality (unusable photo)
├── 5  → Not recognized (non-ant or unrecognizable)
└── 85 → Enter cascade:
    ├── 50 → Correct species (auto, confident)    ✓
    ├── 18 → "Top 3 options" (user picks)         ✓ assisted
    ├── 13 → Partial ID (genus/subfamily only)   ~ partial
    └──  4 → Uncertain, suggest better photo     ✗ retry

Effective success rate: 80% (50 auto + 18 assisted)
Zero confident wrong answers shown.
```

---

## 9. Development Phases

### Phase 1: Foundation
- [ ] Collect 5,000 graded quality images
- [ ] Train Quality Assessor
- [ ] Deploy to web
- [ ] Create "How to photograph ants" guide

### Phase 2: Subfamily (+ Ant Detection)
- [ ] Collect 5,100 subfamily images (ants only)
- [ ] Train MobileNetV2 (17 classes)
- [ ] Implement confidence threshold for non-ant rejection
- [ ] Integrate with Quality model
- [ ] Target: 95% subfamily accuracy, >95% non-ant rejection

### Phase 3: Major Genera
- [ ] Formicinae genus model (51 genera)
- [ ] Myrmicinae genus model (140 genera)
- [ ] Ponerinae genus model (47 genera)
- [ ] Kickback system implementation

### Phase 4: Complete Genus Layer
- [ ] Remaining 14 subfamily genus models
- [ ] Integration testing

### Phase 5: Common Species
- [ ] Top 50 genera species models
- [ ] Focus on Palearctic first

### Phase 6: Full Coverage
- [ ] Remaining species models
- [ ] Continuous improvement

---

## 10. View-Specific Considerations

### Which views matter most?

| View | Code | Best For | Priority |
|------|------|----------|----------|
| Head (face) | h | Mandibles, eyes, antennae | High |
| Profile (lateral) | p | Petiole, overall shape | High |
| Dorsal (top) | d | Thorax sculpture, propodeum | Medium |

### Strategy

1. **Start with profile view** — most diagnostic
2. **Add head view** — for fine distinctions
3. **Dorsal optional** — adds accuracy but not critical

---

## 11. Upload UI Requirements

### Animated Tutorial GIF

**Location:** Front page, directly below the "Upload your images" option

**Purpose:** Show users how the system works at a glance

**Content to demonstrate:**
- Drag and drop interface
- Click to select files option
- Maximum 5 images per submission
- Supported formats (JPG, PNG)
- Upload progress indicator
- What happens after upload (processing → results)

**Format:** Looping animated GIF or short video (WebM fallback)
**Size:** Keep under 2MB for fast loading

---

## 12. Photo Guide Requirements

A user-facing guide ("How to Photograph Ants for ID") should cover:

### What Makes a Good Photo

| Requirement | Good | Bad |
|-------------|------|-----|
| **Focus** | Sharp, setae visible | Blurry, motion blur |
| **Size** | Ant fills >30% of frame | Tiny ant in landscape |
| **Angle** | Clear profile OR head | Ambiguous, partial |
| **Lighting** | Even, no harsh shadows | Overexposed, dark |
| **Background** | Neutral, contrasting | Busy, camouflaging |

### Recommended Equipment

| Budget | Equipment | Quality |
|--------|-----------|---------|
| Free | Smartphone + steady hands | C-D grade |
| $20 | Smartphone + clip-on macro lens | B-C grade |
| $100 | USB microscope | B grade |
| $500+ | DSLR + macro lens | A-B grade |

### Angle Guide with Diagrams

```
PROFILE VIEW (preferred)
┌─────────────────┐
│    ┌──┐         │
│ ○──┤  ├──○──○   │  ← Clear petiole, gaster, legs
│    └──┘         │
└─────────────────┘

HEAD VIEW
┌─────────────────┐
│     ╭───╮       │
│    ╱  ○  ╲      │  ← Mandibles, antennae, eyes
│   │ ╲___╱ │     │
│    ╲_____╱      │
└─────────────────┘

DORSAL VIEW
┌─────────────────┐
│   ┌─────────┐   │
│   │ ┌─┐ ┌─┐ │   │  ← Thorax sculpture, propodeum
│   │ └─┴─┘   │   │
│   └────┬────┘   │
└─────────────────┘
```

---

*Last updated: 2026-03-16*
