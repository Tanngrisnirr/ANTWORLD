# Contributing to AntWorld

First off: **thank you**. You are about to help build something that does not exist yet — an open, ML-powered platform for ant identification that actually teaches people to identify ants.

This guide will get you from zero to your first contribution.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [What Can I Work On?](#what-can-i-work-on)
- [Submitting Changes](#submitting-changes)
- [Style Guide](#style-guide)
- [Recognition](#recognition)

---

## Code of Conduct

**Be excellent to each other.**

- We are scientists, developers, and enthusiasts united by curiosity
- Assume good intentions
- Respect expertise (and lack thereof — everyone starts somewhere)
- No gatekeeping
- Constructive feedback only

We are building a resource, not a fortress.

---

## Getting Started

### Prerequisites

- Git
- A browser
- One of: XAMPP, WAMP, or Podman/Docker

### Setup

**1. Fork and clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/antworld.git
cd antworld
git remote add upstream https://github.com/Tanngrisnirr/ANTWORLD.git
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

You should see the AntWorld homepage.

---

## Development Workflow

### The Three Environments

```
alpha/  →  beta/  →  delta/
 (dev)    (test)    (prod)
```

| Directory | Purpose | Edit Here? |
|-----------|---------|------------|
| `alpha/` | Development, with comments | **YES** |
| `beta/` | Minified, staging tests | NO |
| `delta/` | Production-ready | NEVER |

**Golden Rule:** All changes happen in `alpha/`. Period.

### Branching Strategy

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for fixes
git checkout -b fix/issue-123-description
```

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## What Can I Work On?

### Issue Labels

| Label | Meaning |
|-------|---------|
| `good-first-issue` | Perfect for newcomers |
| `help-wanted` | We need assistance |
| `bug` | Something is broken |
| `enhancement` | New feature or improvement |
| `kids-design` | Children's illustrations |
| `training-data` | Species images and datasets |
| `taxonomy` | Species data, identification keys |
| `translation` | Language localization |

### Areas of Focus

#### Myrmecologists
- Validate species data and identification keys
- Review training/testing sets for ML model accuracy
- Provide non-commercial use pictures of specimens
- Confirm taxonomic classifications

#### Translation
- ES, RU, AR, ZH, PT, JA
- Scientific terminology review

#### Designer for Kids
- Create kid-friendly ant drawings and illustrations
- Simple, colorful representations of ant anatomy
- Educational graphics for the children's section
- Make ants approachable and fun for young learners

---

## Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
type(scope): short description

[optional body]

[optional footer]
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation
- `style` — Formatting (no code change)
- `refactor` — Code restructuring
- `test` — Adding tests
- `chore` — Maintenance

**Examples:**
```
feat(api): add GET /species endpoint
fix(nav): mobile menu not closing on click
docs(readme): add local setup instructions
refactor(js): consolidate jQuery to single version
```

### Pull Request Process

1. **Update your branch** with latest upstream
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes** at `http://localhost:8090/alpha/`

3. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request** with:
   - Clear title
   - Description of changes
   - Screenshots (if visual changes)
   - Link to related issue(s)

5. **Respond to feedback** — we review quickly

### PR Checklist

- [ ] Changes are in `alpha/` only
- [ ] Tested locally
- [ ] No console errors
- [ ] Mobile-friendly (if frontend)
- [ ] Commit messages follow convention
- [ ] PR description is clear

---

## Style Guide

### HTML
- Semantic HTML5 elements (`<article>`, `<nav>`, `<section>`)
- Meaningful `class` names (not `.div1`, `.red-text`)
- Indent with 2 spaces

### CSS
- Mobile-first media queries
- BEM naming convention preferred
- No `!important` unless absolutely necessary

### JavaScript
- Vanilla JS preferred over jQuery (migration in progress)
- `const` > `let` > `var`
- Descriptive variable names
- Comment complex logic

### PHP
- PSR-12 coding standard
- Type hints where possible
- Meaningful function names

---

## Recognition

All contributors are recognized in:
- `humans.txt` (in the website root)
- GitHub contributors list
- Annual acknowledgments on the site

**Significant contributors** may be invited as collaborators.

---

## Questions?

- Open a [GitHub Discussion](https://github.com/Tanngrisnirr/antworld/discussions)
- Check existing issues first
- Be specific about what you need help with

---

## Thank You

You are not just contributing code — you are helping build the global reference for myrmecology.

Every identification key, every accessibility fix, every translation brings us closer to a world where anyone can learn about ants.

**Welcome to AntWorld.**
