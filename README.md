<p align="center">
  <img src="https://raw.githubusercontent.com/Tanngrisnirr/ANTWORLD/master/antworld.org/alpha/img/og-default.jpg" alt="AntWorld Logo" width="400"/>
</p>

<h1 align="center">AntWorld.org</h1>

<p align="center">
  <strong>Open Tools for Ant Identification</strong><br>
  Interactive keys + ML-powered visual ID + Open data
</p>

<p align="center">
  <a href="https://antworld.org">Website</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#contributing">Contribute</a> •
  <a href="#roadmap">Roadmap</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/species-936+-green?style=flat-square" alt="Species"/>
  <img src="https://img.shields.io/badge/subfamilies-8-blue?style=flat-square" alt="Subfamilies"/>
  <img src="https://img.shields.io/badge/genera-74+-orange?style=flat-square" alt="Genera"/>
  <img src="https://img.shields.io/badge/license-CC--BY--NC-lightgrey?style=flat-square" alt="License"/>
</p>

---

## The Problem

Ant identification is hard. Really hard.

- **48,600+ articles** on AntWiki — dense, academic, overwhelming for beginners
- **iNaturalist's AI** struggles with ants — generic models miss diagnostic morphology
- **No interactive keys** exist that actually teach you *how* to identify

Researchers dig through PDFs. Students give up. Citizen scientists guess.

## The Solution

**AntWorld bridges the gap.**

We are building the world's first platform that combines:

| Feature | Status |
|---------|--------|
| Interactive dichotomous keys | **Live** — 70+ keys, 936 species |
| ML-powered visual identification (TensorFlow) | *In development* |
| Progressive learning courses | *Planned* |
| Open API for researchers | *Planned* |
| Expert validation pipeline | *Planned* |

**Our model:** [Xeno-canto](https://xeno-canto.org) did it for bird sounds. We are doing it for ants looks.

---

## Quick Start

### View the Site

```
https://antworld.org
```

### Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Tanngrisnirr/antworld.git
```

**2. Choose your environment:**

#### XAMPP (Windows/Mac/Linux)
1. Copy `antworld.org` folder to `C:\xampp\htdocs\` (or `/opt/lampp/htdocs/`)
2. Edit `httpd.conf` (in `xampp/apache/conf/`), add:
   ```
   AddHandler application/x-httpd-php .html
   ```
3. Restart Apache from XAMPP Control Panel
4. Open: `http://localhost/antworld.org/alpha/`

#### WAMP (Windows)
1. Copy `antworld.org` folder to `C:\wamp64\www\`
2. Click WAMP icon → Apache → httpd.conf, add:
   ```
   AddHandler application/x-httpd-php .html
   ```
3. Restart Apache (click WAMP icon → Restart All Services)
4. Open: `http://localhost/antworld.org/alpha/`

#### Podman/Docker (Linux/Mac)
```bash
cd antworld
podman run -d --name antworld -p 8090:80 \
  -v ./antworld.org:/var/www/html:Z \
  php:8.2-apache

podman exec antworld bash -c "a2enmod rewrite && \
  echo 'AddHandler application/x-httpd-php .html' >> /etc/apache2/conf-available/php-html.conf && \
  a2enconf php-html && \
  sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf && \
  service apache2 reload"
```
Open: `http://localhost:8090/alpha/`

---

## Project Structure

```
antworld/
├── antworld.org/           # The website (deployable)
│   ├── alpha/              # Development version
│   ├── beta/               # Minified, tested on staging
│   └── delta/              # Production-ready
├── scripts/                # Build & deploy workflow
│   ├── minify-to-beta.sh   # Strip comments, minify
│   ├── promote-to-delta.sh # Push to production
│   └── sync-alpha-from-delta.sh
└── README.md
```

**Workflow:** `alpha/` → `beta/` → `delta/` → production server

---

## Contributing

**We need you.** Seriously.

### Roles We Are Looking For

| Role | Skills | Impact |
|------|--------|--------|
| **Myrmecologist** | Ant taxonomy | Validate species data, review training sets, provide specimen photos |
| **Translator** | ES, RU, AR, ZH, PT | Expand to 5+ languages |
| **Designer for Kids** | Illustration | Kid-friendly ant drawings for children's section |

### Good First Issues

Look for issues tagged:
- `good-first-issue` — Perfect for newcomers
- `help-wanted` — We need assistance
- `taxonomy` — Species data validation

### How to Contribute

1. **Fork** the repo
2. **Create a branch** (`git checkout -b feature/amazing-thing`)
3. **Work in `alpha/`** — never edit `delta/` directly
4. **Test locally** at `http://localhost:8090/alpha/`
5. **Submit a PR** with a clear description

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Roadmap

### Phase 1 — Foundation ✓
- [x] Interactive dichotomous keys (70+ keys)
- [x] Species database (936 species)
- [x] Responsive design
- [x] Modernize frontend (jQuery consolidated)
- [x] Mobile-first CSS
- [x] Accessibility improvements

### Phase 2 — Intelligence (Current)
- [x] Training dataset: 44 species, 15 subfamilies, 1428 images
- [ ] Visual identification engine (subfamily → genus → species)
- [ ] Photo quality assessment
- [ ] Spaced repetition training

### Phase 3 — Platform
- [ ] Expert validation pipeline
- [ ] Open ML models (downloadable)
- [ ] Kids section (coloring pages, games)
- [ ] Nearctic region expansion

### Phase 4 — Global Coverage
- [ ] All biogeographic regions
- [ ] Afrotropics & Indomalaya expansion
- [ ] DOI-registered citable resource

---

## The Ecosystem

We do not replace — we **connect**.

| Platform | Their Role | Our Integration |
|----------|-----------|-----------------|
| [AntWeb](https://antweb.org) | Specimen images | Training data source |
| [AntWiki](https://antwiki.org) | Encyclopedia | Deep links for species |
| [AntMaps](https://antmaps.org) | Distribution maps | Inline maps on species pages |
| [AntCat](https://antcat.org) | Taxonomic catalog | Nomenclatural authority |
| [iNaturalist](https://inaturalist.org) | Citizen science | Share button integration |
| [GBIF](https://gbif.org) | Biodiversity data | Data exchange |

---

## Tech Stack

**Frontend:**
- HTML5, CSS3, Vanilla JS + jQuery
- D3.js, Highcharts (client-side only)

**Backend:**
- PHP 8.x, Apache
- Podman/Docker

**Development:**
- AI-assisted design and website functionality (Claude)
- TensorFlow / neural networks for species identification
- Training data: AntWeb specimens (CC BY-SA 3.0)

---

## Philosophy

1. **Open by default** — CC for content, open-source for code
2. **Science-first** — Rigorous taxonomy, traceable sources
3. **ML as amplifier** — Experts remain the gold standard
4. **Teach, do not just answer** — Every interaction educates
5. **Connect, do not replace** — Interoperate with the ecosystem
6. **Sustainable without commerce** — No ads, no paywalls, ever

---

## License

- **Content:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
- **Code:** [MIT License](LICENSE)

---

## Contact

- **Website:** [antworld.org](https://antworld.org)
- **Issues:** [GitHub Issues](https://github.com/Tanngrisnirr/antworld/issues)

---

<p align="center">
  <i>"Nobody currently occupies the intersection of rigorous key-based identification, ML-based visual ID, structured progressive learning, and open data — all without commerce, all open, all connected."</i>
</p>

<p align="center">
  <strong>Be part of building the global reference for myrmecology.</strong>
</p>
