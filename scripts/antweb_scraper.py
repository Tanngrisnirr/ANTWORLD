#!/usr/bin/env python3
"""
AntWeb Image Scraper for ANTWORLD ML Training

Scrapes ant specimen images from AntWeb.org for ML training.
Respects rate limits and tracks progress for resume capability.

Usage:
    python antweb_scraper.py                    # Scrape all target species
    python antweb_scraper.py --species "Formica rufa"  # Single species
    python antweb_scraper.py --resume           # Resume interrupted scrape
    python antweb_scraper.py --dry-run          # Preview without downloading

License: Images from AntWeb are CC BY - attribution required.
"""

import os
import sys
import json
import time
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, quote
import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://www.antweb.org"
IMAGES_PAGE_URL = "{base}/images.do?genus={genus}&species={species}"
SPECIMEN_PAGE_URL = "{base}/specimenImages.do?name={specimen_code}"
IMAGE_BASE_URL = "{base}/images/{specimen_code}/{specimen_code}_{view}_{number}_{size}.jpg"

# Paths (relative to script location)
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
TRAINING_SETS_DIR = PROJECT_ROOT / "TrainingSets"
RAW_DIR = TRAINING_SETS_DIR / "raw"
ML_DIR = PROJECT_ROOT / "ml"
TARGET_SPECIES_FILE = ML_DIR / "target_species.json"
PROGRESS_FILE = ML_DIR / "progress.json"
DOWNLOAD_LOG_FILE = TRAINING_SETS_DIR / "download_log.json"

# Rate limiting
REQUEST_DELAY = 1.0  # seconds between requests
IMAGE_DELAY = 0.5    # seconds between image downloads

# Image sizes available on AntWeb
IMAGE_SIZES = {
    "thumb": "thumbview",      # ~150px thumbnail
    "medium": "med",           # ~400px medium
    "large": "high",           # ~1200px high resolution
}

# Default size to download
DEFAULT_SIZE = "medium"

# Views to download
VIEWS = ["h", "p", "d"]  # head, profile, dorsal (skip label 'l')


class AntWebScraper:
    """Scraper for AntWeb specimen images."""

    def __init__(self, output_dir=None, image_size=DEFAULT_SIZE, dry_run=False):
        self.output_dir = Path(output_dir) if output_dir else RAW_DIR
        self.image_size = IMAGE_SIZES.get(image_size, image_size)
        self.dry_run = dry_run
        self.session = self._create_session()
        self.download_log = self._load_download_log()
        self.stats = {
            "species_processed": 0,
            "specimens_found": 0,
            "images_downloaded": 0,
            "images_skipped": 0,
            "errors": 0,
        }

    def _create_session(self):
        """Create requests session with browser-like headers."""
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        return session

    def _load_download_log(self):
        """Load existing download log for resume capability."""
        if DOWNLOAD_LOG_FILE.exists():
            try:
                with open(DOWNLOAD_LOG_FILE) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"downloaded": {}, "errors": []}
        return {"downloaded": {}, "errors": []}

    def _save_download_log(self):
        """Save download log for resume capability."""
        DOWNLOAD_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DOWNLOAD_LOG_FILE, "w") as f:
            json.dump(self.download_log, f, indent=2)

    def _is_downloaded(self, image_url):
        """Check if image was already downloaded."""
        return image_url in self.download_log.get("downloaded", {})

    def _mark_downloaded(self, image_url, local_path):
        """Mark image as downloaded in log."""
        if "downloaded" not in self.download_log:
            self.download_log["downloaded"] = {}
        self.download_log["downloaded"][image_url] = {
            "local_path": str(local_path),
            "timestamp": datetime.now().isoformat(),
        }

    def _fetch_page(self, url, description="page"):
        """Fetch a page with rate limiting and error handling."""
        time.sleep(REQUEST_DELAY)
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Check for Cloudflare challenge
            if "Just a moment" in response.text or response.status_code == 403:
                print(f"  WARNING: Cloudflare challenge detected for {description}")
                print(f"  URL: {url}")
                print(f"  Try running with browser automation or wait and retry")
                return None

            return response.text
        except requests.RequestException as e:
            print(f"  ERROR fetching {description}: {e}")
            self.stats["errors"] += 1
            return None

    def _parse_specimen_codes(self, html):
        """Extract specimen codes from species images page."""
        soup = BeautifulSoup(html, "html.parser")
        specimen_codes = []

        # Find all links to specimen pages
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Match specimenImages.do?name=XXXXX
            match = re.search(r"specimenImages\.do\?name=([a-zA-Z0-9]+)", href)
            if match:
                code = match.group(1)
                if code not in specimen_codes:
                    specimen_codes.append(code)

        return specimen_codes

    def _parse_image_urls(self, html, specimen_code):
        """Extract image URLs from specimen page HTML."""
        soup = BeautifulSoup(html, "html.parser")
        image_urls = []

        # Find background-image URLs in style attributes
        for element in soup.find_all(style=True):
            style = element.get("style", "")
            # Match background-image: url("...")
            matches = re.findall(r'url\(["\']?(https?://[^"\')\s]+)["\']?\)', style)
            for url in matches:
                if specimen_code.lower() in url.lower():
                    # Convert thumbview to our desired size
                    url = url.replace("_thumbview.jpg", f"_{self.image_size}.jpg")
                    if url not in image_urls:
                        image_urls.append(url)

        # Also check img src attributes
        for img in soup.find_all("img", src=True):
            src = img["src"]
            if specimen_code.lower() in src.lower() and "images/" in src:
                if not src.startswith("http"):
                    src = urljoin(BASE_URL, src)
                src = src.replace("_thumbview.jpg", f"_{self.image_size}.jpg")
                if src not in image_urls:
                    image_urls.append(src)

        return image_urls

    def _construct_image_urls(self, specimen_code, views=None):
        """Construct image URLs directly from specimen code pattern."""
        views = views or VIEWS
        urls = []
        for view in views:
            # Try shot number 1 (most common)
            url = f"{BASE_URL}/images/{specimen_code}/{specimen_code}_{view}_1_{self.image_size}.jpg"
            urls.append({"url": url, "view": view, "shot": 1})
        return urls

    def _download_image(self, url, local_path):
        """Download a single image with progress tracking."""
        if self.dry_run:
            print(f"    [DRY RUN] Would download: {url}")
            return True

        if self._is_downloaded(url):
            self.stats["images_skipped"] += 1
            return True

        time.sleep(IMAGE_DELAY)
        try:
            response = self.session.get(url, timeout=30, stream=True)

            if response.status_code == 404:
                # Image doesn't exist at this URL, not an error
                return False

            response.raise_for_status()

            # Ensure directory exists
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Write image
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self._mark_downloaded(url, local_path)
            self.stats["images_downloaded"] += 1
            return True

        except requests.RequestException as e:
            print(f"    ERROR downloading image: {e}")
            self.download_log.setdefault("errors", []).append({
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            })
            self.stats["errors"] += 1
            return False

    def scrape_species(self, genus, species, subfamily=None):
        """Scrape all images for a species."""
        species_key = f"{genus}_{species}"
        print(f"\nScraping {genus} {species}...")

        # Create output directory
        if subfamily:
            species_dir = self.output_dir / subfamily / species_key
        else:
            species_dir = self.output_dir / species_key

        # Fetch species images page
        url = IMAGES_PAGE_URL.format(base=BASE_URL, genus=genus, species=species)
        html = self._fetch_page(url, f"{genus} {species} images page")

        if not html:
            print(f"  Failed to fetch species page")
            return []

        # Extract specimen codes
        specimen_codes = self._parse_specimen_codes(html)
        print(f"  Found {len(specimen_codes)} specimens with images")
        self.stats["specimens_found"] += len(specimen_codes)

        downloaded_images = []

        for i, specimen_code in enumerate(specimen_codes):
            print(f"  [{i+1}/{len(specimen_codes)}] Specimen: {specimen_code}")

            # Create specimen directory
            specimen_dir = species_dir / specimen_code

            # Try direct URL construction first (faster)
            for view in VIEWS:
                for shot_num in [1, 2]:  # Try shot 1 and 2
                    url = f"{BASE_URL}/images/{specimen_code}/{specimen_code}_{view}_{shot_num}_{self.image_size}.jpg"
                    filename = f"{specimen_code}_{view}_{shot_num}.jpg"
                    local_path = specimen_dir / filename

                    if local_path.exists():
                        print(f"    Exists: {filename}")
                        downloaded_images.append(str(local_path))
                        self.stats["images_skipped"] += 1
                        continue

                    if self._download_image(url, local_path):
                        if not self.dry_run and local_path.exists():
                            print(f"    Downloaded: {filename}")
                            downloaded_images.append(str(local_path))

            # Save metadata
            if not self.dry_run:
                metadata = {
                    "specimen_code": specimen_code,
                    "genus": genus,
                    "species": species,
                    "subfamily": subfamily,
                    "source": "AntWeb.org",
                    "license": "CC BY",
                    "attribution": f"From www.antweb.org, specimen {specimen_code}",
                    "download_date": datetime.now().isoformat(),
                }
                metadata_path = specimen_dir / "metadata.json"
                if specimen_dir.exists():
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f, indent=2)

        self.stats["species_processed"] += 1
        self._save_download_log()

        return downloaded_images

    def scrape_from_target_file(self, target_file=None):
        """Scrape all species from target_species.json."""
        target_file = Path(target_file) if target_file else TARGET_SPECIES_FILE

        if not target_file.exists():
            print(f"ERROR: Target species file not found: {target_file}")
            return

        with open(target_file) as f:
            targets = json.load(f)

        print(f"AntWeb Scraper - Target: {targets['totals']['species']} species from {targets['totals']['subfamilies']} subfamilies")
        print(f"Output directory: {self.output_dir}")
        print(f"Image size: {self.image_size}")
        if self.dry_run:
            print("MODE: Dry run (no downloads)")
        print("-" * 60)

        for subfamily_name, subfamily_data in targets["subfamilies"].items():
            print(f"\n=== Subfamily: {subfamily_name} ===")

            for species_info in subfamily_data["species"]:
                genus = species_info["genus"]
                species = species_info["species"]

                self.scrape_species(genus, species, subfamily=subfamily_name)

        # Print final stats
        print("\n" + "=" * 60)
        print("SCRAPING COMPLETE")
        print("=" * 60)
        print(f"Species processed: {self.stats['species_processed']}")
        print(f"Specimens found: {self.stats['specimens_found']}")
        print(f"Images downloaded: {self.stats['images_downloaded']}")
        print(f"Images skipped (existing): {self.stats['images_skipped']}")
        print(f"Errors: {self.stats['errors']}")

        self._save_download_log()
        return self.stats


def main():
    parser = argparse.ArgumentParser(
        description="Scrape ant images from AntWeb.org for ML training"
    )
    parser.add_argument(
        "--species",
        help="Single species to scrape (format: 'Genus species')"
    )
    parser.add_argument(
        "--genus",
        help="Genus (used with --species-name)"
    )
    parser.add_argument(
        "--species-name",
        help="Species epithet (used with --genus)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory (default: TrainingSets/raw)"
    )
    parser.add_argument(
        "--size",
        choices=["thumb", "medium", "large"],
        default="medium",
        help="Image size to download (default: medium)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without downloading"
    )
    parser.add_argument(
        "--target-file",
        help="Custom target species JSON file"
    )

    args = parser.parse_args()

    scraper = AntWebScraper(
        output_dir=args.output,
        image_size=args.size,
        dry_run=args.dry_run,
    )

    if args.species:
        # Single species from command line
        parts = args.species.split()
        if len(parts) >= 2:
            genus, species = parts[0], parts[1]
            scraper.scrape_species(genus, species)
        else:
            print("ERROR: Species must be in format 'Genus species'")
            sys.exit(1)
    elif args.genus and args.species_name:
        scraper.scrape_species(args.genus, args.species_name)
    else:
        # Scrape all from target file
        scraper.scrape_from_target_file(args.target_file)


if __name__ == "__main__":
    main()
