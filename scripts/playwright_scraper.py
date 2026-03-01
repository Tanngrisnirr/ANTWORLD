#!/usr/bin/env python3
"""
AntWeb Playwright Scraper - Bypasses Cloudflare protection

Uses Playwright browser automation to download ant images from AntWeb.org
since direct HTTP requests are blocked by Cloudflare.

Usage:
    python playwright_scraper.py                          # Scrape all target species
    python playwright_scraper.py --species "Formica rufa" # Single species
    python playwright_scraper.py --dry-run                # Preview only

Requirements:
    pip install playwright
    playwright install chromium
"""

import os
import sys
import json
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# Configuration
BASE_URL = "https://www.antweb.org"
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
TRAINING_SETS_DIR = PROJECT_ROOT / "TrainingSets"
RAW_DIR = TRAINING_SETS_DIR / "raw"
ML_DIR = PROJECT_ROOT / "ml"
TARGET_SPECIES_FILE = ML_DIR / "target_species.json"
PROGRESS_FILE = ML_DIR / "progress.json"

# Views to download (skip 'l' for labels)
VIEWS = ["h", "p", "d"]  # head, profile, dorsal
IMAGE_SIZE = "high"  # high resolution


class PlaywrightScraper:
    def __init__(self, output_dir=None, dry_run=False, headless=True):
        self.output_dir = Path(output_dir) if output_dir else RAW_DIR
        self.dry_run = dry_run
        self.headless = headless
        self.browser = None
        self.page = None
        self.stats = {
            "species_processed": 0,
            "specimens_found": 0,
            "images_downloaded": 0,
            "images_skipped": 0,
            "errors": 0,
        }

    async def start(self):
        """Start the browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
        )
        self.page = await self.context.new_page()
        print("Browser started")

    async def stop(self):
        """Stop the browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser stopped")

    async def wait_for_cloudflare(self):
        """Wait for Cloudflare challenge to pass."""
        try:
            # Wait for page to not be "Just a moment..."
            for _ in range(30):  # 30 second timeout
                title = await self.page.title()
                if "Just a moment" not in title:
                    return True
                await asyncio.sleep(1)
            return False
        except Exception:
            return True  # Assume passed if error

    async def get_specimen_codes(self, genus, species):
        """Get all specimen codes for a species."""
        url = f"{BASE_URL}/images.do?genus={genus}&species={species}"
        print(f"  Fetching: {url}")

        await self.page.goto(url)
        await self.wait_for_cloudflare()

        # Extract specimen codes
        specimens = await self.page.evaluate("""
            () => {
                const specimens = [];
                document.querySelectorAll('a[href*="specimenImages.do?name="]').forEach(link => {
                    const match = link.href.match(/name=([a-zA-Z0-9]+)/);
                    if (match && !specimens.includes(match[1])) {
                        specimens.push(match[1]);
                    }
                });
                return specimens;
            }
        """)

        return specimens

    async def download_image(self, specimen_code, view, shot_num, output_dir):
        """Download a single image by navigating to it."""
        url = f"{BASE_URL}/images/{specimen_code}/{specimen_code}_{view}_{shot_num}_{IMAGE_SIZE}.jpg"
        filename = f"{specimen_code}_{view}_{shot_num}.png"
        filepath = output_dir / filename

        if filepath.exists():
            print(f"    Exists: {filename}")
            self.stats["images_skipped"] += 1
            return True

        if self.dry_run:
            print(f"    [DRY RUN] Would download: {filename}")
            return True

        try:
            # Navigate to image
            response = await self.page.goto(url)

            if response and response.status == 404:
                return False

            # Check if it's actually an image page
            content_type = response.headers.get("content-type", "") if response else ""
            if "image" not in content_type:
                # Might be Cloudflare, wait
                await self.wait_for_cloudflare()

            # Take screenshot of the image
            output_dir.mkdir(parents=True, exist_ok=True)
            await self.page.screenshot(path=str(filepath))

            print(f"    Downloaded: {filename}")
            self.stats["images_downloaded"] += 1
            return True

        except Exception as e:
            print(f"    ERROR: {filename} - {e}")
            self.stats["errors"] += 1
            return False

    async def scrape_species(self, genus, species, subfamily=None):
        """Scrape all images for a species."""
        print(f"\n{'='*60}")
        print(f"Scraping {genus} {species}")
        print(f"{'='*60}")

        # Get specimen codes
        specimens = await self.get_specimen_codes(genus, species)
        print(f"  Found {len(specimens)} specimens")
        self.stats["specimens_found"] += len(specimens)

        if not specimens:
            print("  No specimens found!")
            return

        # Set up output directory
        species_key = f"{genus}_{species}"
        if subfamily:
            species_dir = self.output_dir / subfamily / species_key
        else:
            species_dir = self.output_dir / species_key

        # Download images for each specimen
        for i, specimen in enumerate(specimens):
            print(f"\n  [{i+1}/{len(specimens)}] Specimen: {specimen}")
            specimen_dir = species_dir / specimen

            for view in VIEWS:
                for shot_num in [1, 2]:
                    await self.download_image(specimen, view, shot_num, specimen_dir)

            # Save metadata
            if not self.dry_run:
                specimen_dir.mkdir(parents=True, exist_ok=True)
                metadata = {
                    "specimen_code": specimen,
                    "genus": genus,
                    "species": species,
                    "subfamily": subfamily,
                    "source": "AntWeb.org",
                    "license": "CC BY",
                    "attribution": f"From www.antweb.org, specimen {specimen}",
                    "download_date": datetime.now().isoformat(),
                }
                with open(specimen_dir / "metadata.json", "w") as f:
                    json.dump(metadata, f, indent=2)

        self.stats["species_processed"] += 1

    async def scrape_from_target_file(self, target_file=None):
        """Scrape all species from target_species.json."""
        target_file = Path(target_file) if target_file else TARGET_SPECIES_FILE

        if not target_file.exists():
            print(f"ERROR: Target species file not found: {target_file}")
            return

        with open(target_file) as f:
            targets = json.load(f)

        total_species = targets["totals"]["species"]
        total_subfamilies = targets["totals"]["subfamilies"]

        print(f"{'='*60}")
        print(f"AntWeb Playwright Scraper")
        print(f"{'='*60}")
        print(f"Target: {total_species} species from {total_subfamilies} subfamilies")
        print(f"Output: {self.output_dir}")
        print(f"Mode: {'Dry run' if self.dry_run else 'Download'}")
        print(f"{'='*60}")

        await self.start()

        try:
            for subfamily_name, subfamily_data in targets["subfamilies"].items():
                print(f"\n{'#'*60}")
                print(f"# Subfamily: {subfamily_name}")
                print(f"{'#'*60}")

                for species_info in subfamily_data["species"]:
                    genus = species_info["genus"]
                    species = species_info["species"]
                    await self.scrape_species(genus, species, subfamily=subfamily_name)

                    # Brief pause between species
                    await asyncio.sleep(2)

        finally:
            await self.stop()

        # Print final stats
        print(f"\n{'='*60}")
        print("SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"Species processed: {self.stats['species_processed']}")
        print(f"Specimens found: {self.stats['specimens_found']}")
        print(f"Images downloaded: {self.stats['images_downloaded']}")
        print(f"Images skipped: {self.stats['images_skipped']}")
        print(f"Errors: {self.stats['errors']}")


async def main():
    parser = argparse.ArgumentParser(description="Scrape ant images from AntWeb using Playwright")
    parser.add_argument("--species", help="Single species (format: 'Genus species')")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview without downloading")
    parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    parser.add_argument("--target-file", help="Custom target species JSON file")

    args = parser.parse_args()

    scraper = PlaywrightScraper(
        output_dir=args.output,
        dry_run=args.dry_run,
        headless=not args.no_headless,
    )

    if args.species:
        parts = args.species.split()
        if len(parts) >= 2:
            await scraper.start()
            try:
                await scraper.scrape_species(parts[0], parts[1])
            finally:
                await scraper.stop()
        else:
            print("ERROR: Species must be in format 'Genus species'")
            sys.exit(1)
    else:
        await scraper.scrape_from_target_file(args.target_file)


if __name__ == "__main__":
    asyncio.run(main())
