# ANTWORLD ML Progress Charter

> **Goal:** Build a proof-of-concept ant recognition model and rally community support for more training data.

**Last Updated:** 2026-03-01

---

## Data Collection Progress

| Metric | Current | Target | Progress |
|--------|---------|--------|----------|
| Subfamilies | 0 | 17 | ![](https://progress-bar.dev/0/?width=200) |
| Species | 0 | 32 | ![](https://progress-bar.dev/0/?width=200) |
| Images | 0 | ~960 | ![](https://progress-bar.dev/0/?width=200) |

### Species Status

| Subfamily | Species | Images | Status |
|-----------|---------|--------|--------|
| Formicinae | *Formica rufa* | 0 | Pending |
| Formicinae | *Camponotus herculeanus* | 0 | Pending |
| Formicinae | *Lasius niger* | 0 | Pending |
| Myrmicinae | *Atta cephalotes* | 0 | Pending |
| Myrmicinae | *Myrmica rubra* | 0 | Pending |
| Myrmicinae | *Pheidole megacephala* | 0 | Pending |
| Ponerinae | *Odontomachus bauri* | 0 | Pending |
| Ponerinae | *Neoponera villosa* | 0 | Pending |
| Dolichoderinae | *Linepithema humile* | 0 | Pending |
| Dolichoderinae | *Tapinoma sessile* | 0 | Pending |
| Dorylinae | *Eciton burchellii* | 0 | Pending |
| Dorylinae | *Dorylus nigricans* | 0 | Pending |
| Myrmeciinae | *Myrmecia gulosa* | 0 | Pending |
| Myrmeciinae | *Nothomyrmecia macrops* | 0 | Pending |
| Paraponerinae | *Paraponera clavata* | 0 | Pending |
| ... | *(+14 more species)* | ... | ... |

---

## Model Training Progress

### Gate 0: Binary Ant Detector
> "Is this an ant?"

| Metric | Value |
|--------|-------|
| Status | Not Started |
| Training Accuracy | -- |
| Validation Accuracy | -- |
| Test Accuracy | -- |

### Gate 1: Quality Assessor
> "Is this photo usable?"

| Metric | Value |
|--------|-------|
| Status | Not Started |
| Training Accuracy | -- |
| Validation Accuracy | -- |
| Test Accuracy | -- |

### Subfamily Classifier
> "Which of 17 subfamilies?"

| Metric | Value |
|--------|-------|
| Status | Not Started |
| Training Accuracy | -- |
| Validation Accuracy | -- |
| Test Accuracy | -- |

---

## Milestones

- [x] **Infrastructure Ready** - Scripts, configs, target species list
- [ ] **First Species Scraped** - Formica rufa images downloaded
- [ ] **All Species Scraped** - 32 species across 17 subfamilies
- [ ] **Preprocessing Complete** - Split, resized, augmented
- [ ] **Gate 0 Training Started** - Binary classifier in progress
- [ ] **Gate 0 > 90% Accuracy** - First working model
- [ ] **Model Deployed to Web** - Live on antworld.org

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
2. Email: *(coming soon)*
3. AntWeb contribution: https://www.antweb.org/participate.do

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

*This charter is auto-generated from `ml/progress.json`. Run `local/scripts/update_progress.py` to refresh.*
