# ANTWORLD ML Strategy

## Overview

This document consolidates the complete machine learning strategy for AntWorld, including architecture, training requirements, quality filtering, and deployment.

**Core principle:** Instead of one massive model trying to classify 936+ species, we use a **layered system** where specialized models handle each taxonomic level. The subfamily classifier doubles as the ant detector - if no subfamily matches with sufficient confidence, the image is rejected.

**Training approach:** Positive data only. We train on ant images exclusively. Non-recognition (low confidence across all classes) indicates "not an ant" - no negative samples needed.

**Open Source & Privacy:**

All model architectures are fully open source and run locally:

| Model | License | Source | Data Privacy |
|-------|---------|--------|--------------|
| EfficientNet | Apache 2.0 | Google (downloadable) | ✓ Runs locally |
| Vision Transformer (ViT) | Apache 2.0 | Google (downloadable) | ✓ Runs locally |
| MobileNetV2 | Apache 2.0 | Google (downloadable) | ✓ Runs locally |

**No data leaves your system:**
- Pre-trained ImageNet weights are downloaded once, then stored locally
- Fine-tuning on ant images happens entirely on your hardware
- Browser inference via TensorFlow.js is 100% client-side
- No API calls, no telemetry, no cloud dependency
- Users' uploaded photos never leave their browser

This aligns with ANTWORLD's **Client-Side Only Policy**.

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
| Cranium | Poly | Head capsule only — EXCLUDE antennae, stop at torulus |
| Mesosoma | Poly | Pronotum to propodeum — EXCLUDE coxae (coxae belong to legs) |
| Gaster | Box or Poly | Include petiole attachment |
| Petiole | Box | Tight box fine |
| Post-petiole | Box | If present (Myrmicinae) |
| Legs | Box | **Group all visible legs in ONE box** — not diagnostic, save time |
| Antennae | Poly | Each antenna separate — scape + funiculus |
| Wings | Poly | Irregular shapes (alates only) |
| Sting | Box | Small box if visible |

**Legs — Capture for Testing:**

Legs are traditionally considered non-diagnostic, but this assumption should be tested empirically.

**Annotation approach:**
- Draw ONE box covering all visible legs per side (minimal effort)
- This gives us data to run ablation tests

**Planned experiment:**
| Training Set | Includes |
|--------------|----------|
| A: Full body | Cranium + mesosoma + gaster + petiole + legs |
| B: Core only | Cranium + mesosoma + gaster + petiole (no legs) |

Compare accuracy metrics on same test set. If legs improve accuracy, keep them. If not, we can drop leg annotations in future batches to save time.

**Hypothesis:** Legs may encode:
- Relative proportions (leg length vs body size)
- Tibial spur morphology (some genera)
- Color patterns (bicolored legs in some species)

Worth testing rather than assuming.

**Precision rules:**
- Boxes with ~80% target part coverage are acceptable
- Minor overlap with adjacent parts is fine (model learns from many examples)
- Don't agonize over pixel-perfect boundaries
- Save polygons for curved/irregular parts where boxes include too much background

**Why overlap is OK:**
- Object detection models (YOLO, Faster R-CNN) expect some background in boxes
- IoU metrics account for this
- Model learns to focus on central object, not edges
- Hundreds of examples average out minor inconsistencies

**Cranium vs Antennae — Draw Separately:**

The cranium (head capsule) and antennae must be annotated as **separate polygons**:

| Annotation | Include | Exclude |
|------------|---------|---------|
| Cranium | Head capsule, eyes, clypeus, mandibles | Antennae |
| Antennae | Scape + funiculus (per antenna) | Head capsule |

**Why separate:**
- Morphometric head measurements (CL, CW, CS) exclude antennae
- Scape length (SL) is an independent measurement
- Cleaner segmentation masks for both parts
- Antenna insertion point (torulus) becomes a learnable landmark

**Practical approach:**
1. Draw cranium polygon following head capsule outline
2. Stop at antennal socket (torulus)
3. Draw each antenna as a separate polygon (2 total)

### Setae (Pilosity) Considerations

**Diagnostic importance:**

Setae (erect hairs) are critical for identifying cryptic species complexes:

| Species Pair | Diagnostic Setae Feature |
|--------------|--------------------------|
| *Lasius niger* vs *L. platythorax* | Erect hair count/position on mesosoma edge |
| *Camponotus* species | Pilosity pattern on gaster, head |
| *Formica* species groups | Setae density on pronotum |
| *Myrmica* species | Scape pilosity (erect vs appressed) |

**Annotation strategy for setae:**

Do NOT try to trace individual hairs in bounding boxes. Instead:

1. **Standard body part boxes:** Draw around solid cuticle, ignore protruding setae
2. **The model learns pilosity from texture inside the box**
3. **Future pilosity classifier:** Separate model layer specifically for setae analysis

**Why this works:**
- CNNs extract texture features (hair density, distribution) from interior pixels
- Inconsistent hair-tracing hurts training more than consistent cuticle-only boxes
- Low contrast between setae and background makes tracing unreliable

### Setae-Aware Model Options

For cryptic species requiring precise pilosity analysis, consider these architectures:

| Architecture | Resolution | Setae Capability | Trade-off |
|--------------|------------|------------------|-----------|
| MobileNetV2 | 224×224 | Basic texture | Fast, small |
| EfficientNet-B0 | 224×224 | Good texture | Balanced |
| EfficientNet-B4 | 380×380 | Fine detail visible | Larger model |
| EfficientNet-B7 | 600×600 | Individual setae | Very large |
| Vision Transformer (ViT) | 384×384 | Attention to specific features | High compute |

**Recommended approach for pilosity-dependent species:**

```
Standard Pipeline              Pilosity-Enhanced Pipeline

Image → Subfamily → Genus      Image → Subfamily → Genus
              ↓                              ↓
         Species                    ┌────────┴────────┐
                                    ↓                 ↓
                              Standard           Pilosity
                              Species            Classifier
                              Classifier         (high-res)
                                    ↓                 ↓
                                    └────────┬────────┘
                                             ↓
                                      Combined Score
```

**Pilosity classifier specs:**
```yaml
architecture: EfficientNet-B4 or ViT-B/16
input_size: 380x380 minimum (600x600 preferred)
focus_regions: mesosoma edge, scape, gaster
output: pilosity pattern classes or setae count estimate
use_case: cryptic species disambiguation (Lasius, Camponotus, etc.)
```

**Training data for pilosity:**
- Crop to specific body regions (mesosoma profile, scape close-up)
- Label with setae count ranges or pattern classes
- Requires high-resolution source images (Grade A-B only)

---

## 5. Model Specifications

### Design Philosophy: Accuracy Over Everything

**Context:** Human identification of an unknown ant can take **2+ hours** with keys, microscope, and literature. If ML takes 30 seconds with high accuracy, that's a 240x speedup. There is no reason to sacrifice accuracy for speed.

**Why tiered architectures were wrong for us:**

The tiered approach (fast triage → accurate ID) optimizes for user experience in apps where users expect instant results. But our users are:
- Researchers who will wait for accuracy
- Students learning identification
- Enthusiasts who want correct answers

**None of them would prefer a fast wrong answer over a slow correct one.**

### Architecture Options

**Option A: Balanced (Original)**
```
TIER 1: TRIAGE (always loaded, ~30MB total)
├── Quality Assessor (15MB) — 224×224, fast
└── Subfamily Classifier (14MB) — 224×224, fast

TIER 2: IDENTIFICATION (lazy loaded, 50-80MB per path)
├── Genus Classifier — 384×384
└── Species Classifier — 384×384 to 512×512

TIER 3: CRYPTIC SPECIES (optional, 80-120MB)
└── Pilosity/Detail Analyzer — 512×512+
```
Total time: 2-5 seconds | Total download: 100-200MB

**Option B: Accuracy-First (Recommended)**
```
ALL LAYERS: MAXIMUM RESOLUTION
├── Quality Assessor — 384×384, EfficientNet-B4
├── Subfamily Classifier — 512×512, ViT-B/16
├── Genus Classifier — 512×512, ViT-B/16
├── Species Classifier — 600×600, ViT-L/16 or EfficientNet-B7
└── No separate cryptic tier needed — base models see setae
```
Total time: 15-30 seconds | Total download: 300-500MB

**Why Option B is better:**
- High-res subfamily model catches features low-res would miss
- No "cryptic species specialist" needed — the main models see pilosity
- Consistent quality across the entire cascade
- If image passes quality check, every subsequent layer has maximum detail
- 30 seconds vs 2 hours human time = still 240x faster

### Hierarchy Still Matters (But Not for Speed)

The subfamily → genus → species cascade exists for **training efficiency**, not inference speed:

| Approach | Training Images Needed | Why |
|----------|------------------------|-----|
| Flat (1 model → 3000 species) | 1,400,000+ | Must distinguish all species at once |
| Hierarchical (cascading models) | ~99,000 | Each model has narrower scope |

Each layer narrows the search space. But each layer should use the **best possible model** for that task.

### Model Specifications (Accuracy-First / Option B)

All models use maximum practical resolution. No compromises.

### Quality Assessor
```yaml
architecture: EfficientNet-B4
input_size: 384x384
parameters: ~19M
output: 5 quality dimensions + grade
size_on_disk: ~50MB
inference_time: 200-300ms
note: High-res catches subtle blur, sees if setae are resolvable
```

### Subfamily Model (+ Ant Detection)
```yaml
architecture: ViT-B/16
input_size: 512x512
parameters: ~86M
output: 17 classes (softmax)
size_on_disk: ~90MB
inference_time: 400-600ms
note: Attention mechanism focuses on diagnostic regions; catches subfamily
      features that MobileNetV2 would miss at edges
```

### Genus Models
```yaml
architecture: ViT-B/16
input_size: 512x512
parameters: ~86M per model
output: varies (1-140 classes)
size_on_disk: ~90MB each
inference_time: 400-600ms
note: Same architecture as subfamily; transfer learning possible
```

### Species Models
```yaml
architecture: ViT-L/16 or EfficientNet-B7
input_size: 600x600
parameters: 66-304M per model
output: varies (2-100 classes)
size_on_disk: 100-150MB each
inference_time: 800-1500ms
note: Maximum resolution; pilosity, sculpture, fine morphology all visible
      No separate cryptic species model needed — this IS the high-res model
```

### Why No Separate Cryptic Species Tier

With 600×600 input and ViT-L/16 attention:
- Individual setae visible and countable by the model
- Propodeal sculpture patterns resolved
- Scape pilosity distinguishable

The "cryptic species problem" disappears when resolution is sufficient.
A separate tier was only needed to compensate for low-res base models.

---

## 6. Hardware Requirements

### Minimum (Quality + Subfamily training — Tier 1)
- CPU: Any modern multi-core
- RAM: 16GB
- Storage: 50GB SSD
- GPU: Optional but helpful (MobileNetV2 trains fast on CPU)

### Recommended (Genus training — Tier 2 with EfficientNet-B4)
- CPU: 8+ cores
- RAM: 32GB
- Storage: 500GB SSD
- GPU: NVIDIA RTX 3060+ (12GB VRAM) — B4 at 384×384 needs ~8GB

### Optimal (Species + ViT training — Tier 2/3)
- CPU: 16+ cores
- RAM: 64GB+
- Storage: 2TB+ SSD
- GPU: NVIDIA RTX 4090 (24GB VRAM) or A100 (40/80GB)
- Note: ViT-L/16 and EfficientNet-B7 require 16-24GB VRAM at batch size 16

### Cloud Options (Updated for High-Res Models)

| Provider | GPU | VRAM | Cost/Hour | Best For |
|----------|-----|------|-----------|----------|
| Google Colab Free | T4 | 16GB | Free | Prototyping, Tier 1 |
| Colab Pro | V100 | 16GB | ~$10/month | Tier 1-2, small batches |
| Colab Pro+ | A100 | 40GB | ~$50/month | Tier 2-3, ViT training |
| Lambda Labs | A100 | 40GB | $1.10/hour | Heavy training |
| RunPod | A100/H100 | 40-80GB | $1.50-3/hour | Full pipeline |
| Vast.ai | Various | Variable | $0.20+/hour | Budget option |

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

## 13. Automated Morphometrics

### Overview

Beyond identification, the ML system can automatically extract morphometric measurements from images. This requires:
1. **Scale calibration** — pixels-per-mm ratio from annotated scale bars
2. **Precise segmentation** — pixel-perfect body part boundaries
3. **Landmark detection** — key measurement points

### Scale Annotation System

The grader tool captures scale bar annotations:

```json
{
  "type": "line",
  "part": "scale",
  "x1": 921, "y1": 757,
  "x2": 800, "y2": 756,
  "pixelLength": 121,
  "realValue": 0.2,
  "unit": "mm",
  "pixelsPerUnit": 605
}
```

This calibration enables conversion from pixels to real-world measurements.

### From Bounding Boxes to Segmentation Masks

**Current:** Rough bounding boxes/polygons for training data

**Future:** ML outputs pixel-perfect segmentation masks

```
Training Data (manual)          ML Output (automatic)
┌─────────────────┐            ┌─────────────────┐
│  ┌──────────┐   │            │    ████████     │
│  │  HEAD    │   │     →      │   ██████████    │
│  │  (box)   │   │            │  ████████████   │
│  └──────────┘   │            │   ██████████    │
└─────────────────┘            └─────────────────┘
   Rough box                   Precise mask (pixel-level)
```

**Model architectures for segmentation:**
- U-Net — lightweight, good for medical/scientific imaging
- Mask R-CNN — instance segmentation (separates multiple legs, antennae)
- SAM (Segment Anything) — pre-trained, fine-tune for ants

### Automatic Surface Area Calculation

Once segmentation masks exist:

```javascript
// Count pixels in mask
const pixelCount = mask.filter(p => p > 0).length;

// Convert to real-world area
const pixelsPerMm = scaleAnnotation.pixelsPerUnit;
const areaMm2 = pixelCount / (pixelsPerMm * pixelsPerMm);

// Example:
// Head mask = 45,000 pixels
// Scale = 605 px/mm
// Area = 45,000 / (605)² = 0.123 mm²
```

### Distance Measurements Between Parts

**Why distances matter:** Morphometric indices are ratios of measurements, crucial for taxonomy.

**Key indices:**

| Index | Formula | Diagnostic Value |
|-------|---------|------------------|
| Cephalic Index (CI) | HW/HL × 100 | Head shape |
| Scape Index (SI) | SL/HW × 100 | Antenna proportions |
| Weber's Length (WL) | Diagonal mesosoma | Overall size |
| Petiole Index (PI) | PW/PL × 100 | Petiole shape |
| Eye Index (EI) | EL/HL × 100 | Eye size relative to head |

**Measurement types:**

```
HEAD MEASUREMENTS
┌─────────────────────────┐
│         HW              │  HW = Head Width (max)
│    ←─────────→          │  HL = Head Length
│    ╭─────────╮          │  SL = Scape Length
│   ╱     ○     ╲   ▲     │  EL = Eye Length
│  │           │   │      │
│  │    ───    │   HL     │
│   ╲         ╱    │      │
│    ╲_______╱     ▼      │
└─────────────────────────┘

PROFILE MEASUREMENTS
┌─────────────────────────────────────────┐
│                                          │
│    ○──┬────────────┬──○──┬──○           │
│       │     WL     │     │              │
│       ←────────────→     │              │
│            │             PL             │
│       Mesosoma      Petiole             │
└─────────────────────────────────────────┘
```

### Standard Morphometric Abbreviations

References:
- Csősz & Schulz (2010) - Zootaxa 2401
- GLAD (GlobalAnts) trait measurement protocol

**Head Measurements (full-face view):**

| Abbrev | Name | Description | GLAD Priority |
|--------|------|-------------|---------------|
| HL | Head Length | Anteriormost clypeal margin to posterior head margin | 1 |
| HW | Head Width | Maximum width across compound eyes | 1 |
| CS | Cephalic Size | (HL + HW) / 2 — body size indicator | - |
| IOW | Inter-ocular Width | Distance between inner eye margins | 1 |
| EW | Max Eye Width | Maximum diameter of compound eye | 1 |
| EH | Eye Height | Minimum diameter of compound eye | - |
| EL | Eye Length | Maximum length of compound eye | - |
| ClyL | Clypeus Length | Length of clypeus (full-face view) | 2 |
| MdL | Mandible Length | Mandible base to tip | 1 |
| OMD | Oculo-Malar Distance | Eye margin to mandibular junction (profile) | - |
| FLW | Frontal Lobes Width | Max distance between frontal lobe borders | - |
| FR | Frons Width | Minimum width between frontal carinae | - |
| POC | Postocular Distance | Posterior eye margin to posterior head margin | - |
| SL | Scape Length | Proximal scape lobe to distal end | 2 |

**Mesosoma Measurements:**

| Abbrev | Name | Description | GLAD Priority |
|--------|------|-------------|---------------|
| WL | Weber's Length | Diagonal mesosoma length (profile) | 2 |
| ML | Mesosoma Length | Pronotal slope to propodeal lobes (profile) | - |
| PW | Pronotum Width | Maximum width of pronotum (dorsal) | 2 |
| MW | Mesosoma Width | Maximum mesosoma width (dorsal) | - |
| SPL | Spiracle-Declivity | Propodeal spiracle center to declivity | - |
| SPSP | Propodeal Spine Length | Spine tip to propodeal spiracle (profile) | - |

**Leg Measurements:**

| Abbrev | Name | Description | GLAD Priority |
|--------|------|-------------|---------------|
| HFL | Hind Femur Length | Length of hind leg femur | 1 |

**Petiole Measurements:**

| Abbrev | Name | Description | GLAD Priority |
|--------|------|-------------|---------------|
| NOH | Petiolar Node Height | Maximum height of petiolar node | - |
| NOL | Petiolar Node Length | Length of petiolar node | - |
| PEH | Petiole Height | Maximum petiole height (profile) | - |
| PEL | Petiole Length | Posteriormost point to petiolar spiracle | - |
| PEW | Petiole Width | Maximum width (dorsal) | - |

**Postpetiole Measurements:**

| Abbrev | Name | Description | GLAD Priority |
|--------|------|-------------|---------------|
| PPH | Postpetiole Height | Maximum height (profile) | - |
| PPL | Postpetiole Length | Maximum length (profile) | - |
| PPW | Postpetiole Width | Maximum width (dorsal) | - |

### Ordinal Traits (Non-Measurements)

**Sculpturing:**

| Value | Description |
|-------|-------------|
| 1 | Cuticle appears completely smooth, often shiny |
| 2 | Shallow wrinkles or pits |
| 3 | Surface heavily textured with ridges, grooves or pits |

*Note: Intermediate values allowed (e.g., 1.5, 2.5)*

**Pilosity:**
- Count of all hairs crossing the border of the mesosoma in profile view
- Interior hairs not counted

**Number of Spines:**
- Total spines on alitrunk (mesosoma) and petiole/s
- Counted separately for each region

### Implementation Approach

**Phase 1: Landmark annotation (manual)**
- Add landmark points to grader tool (e.g., "head_left", "head_right")
- Train landmark detection model

**Phase 2: Automatic landmark detection**
- Model predicts key measurement points
- Calculate distances using scale calibration

**Phase 3: Full segmentation**
- Train segmentation model using bounding box annotations
- Extract precise boundaries automatically
- Calculate surface areas

### Grader Tool Support

Current annotation types:
- `box` — bounding box (x, y, w, h)
- `poly` — polygon (array of points)
- `line` — scale bar (x1, y1, x2, y2, realValue, unit, pixelsPerUnit)
- `measurement` — morphometric line annotation (x1, y1, x2, y2, measurement, pixelLength)
- `ignore` — regions to exclude from training

**Measurement annotation format:**
```json
{
  "type": "line",
  "part": "measurement",
  "measurement": "CL",
  "measurementName": "Cephalic Length",
  "bodyPart": "head",
  "view": "full-face",
  "x1": 150, "y1": 200,
  "x2": 150, "y2": 450,
  "pixelLength": 250
}
```

**Keyboard shortcuts:**
- `N` — Select measurement mode
- `H` — Cranium, `M` — Mesosoma, `G` — Gaster
- `R` — Scale bar, `X` — Ignore region

Future additions:
- `landmark` — single point markers for measurement endpoints
- `distance` — line between two landmarks with automatic mm calculation

### Training Data Requirements

| Task | Images Needed | Notes |
|------|---------------|-------|
| Segmentation masks | 1,000+ per body part | Can bootstrap from boxes |
| Landmark detection | 2,000+ | Manual point annotation |
| Distance prediction | 500+ | Derived from landmarks |

### Output Format

```json
{
  "image": "casent0106203_h_1.jpg",
  "scale": {
    "pixelsPerMm": 605
  },
  "measurements": {
    "head_width_mm": 1.52,
    "head_length_mm": 1.38,
    "cephalic_index": 110.1,
    "scape_length_mm": 1.21,
    "scape_index": 79.6,
    "eye_length_mm": 0.34
  },
  "areas": {
    "head_mm2": 1.65,
    "mesosoma_mm2": 2.12,
    "gaster_mm2": 1.89
  },
  "segmentation_masks": {
    "head": "base64_encoded_mask...",
    "mesosoma": "base64_encoded_mask..."
  }
}
```

---

*Last updated: 2026-03-20*
