#!/usr/bin/env python3
"""
AntWeb Batch Scraper - Optimized for speed

Strategy:
1. Use Playwright to pass Cloudflare once and collect specimen codes
2. Export cookies to use with requests for fast batch downloads
3. Generate predictable image URLs and download in parallel

Usage:
    python antweb_batch_scraper.py                          # Scrape all target species
    python antweb_batch_scraper.py --species "Formica rufa" # Single species
    python antweb_batch_scraper.py --dry-run                # Preview only

Requirements:
    pip install playwright requests
    playwright install chromium
"""

import os
import sys
import json
import asyncio
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# Configuration
BASE_URL = "https://www.antweb.org"
STATIC_URL = "https://static.antweb.org"
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
TRAINING_SETS_DIR = PROJECT_ROOT / "TrainingSets"
RAW_DIR = TRAINING_SETS_DIR / "raw"
ML_DIR = PROJECT_ROOT / "ml"
TARGET_SPECIES_FILE = ML_DIR / "target_species.json"

# Views to download
VIEWS = ["h", "p", "d"]  # head, profile, dorsal
IMAGE_SIZE = "high"  # high, med, thumbview

# Parallel downloads
MAX_WORKERS = 4
REQUEST_TIMEOUT = 30


class AntWebBatchScraper:
    def __init__(self, output_dir=None, dry_run=False, headless=True):
        self.output_dir = Path(output_dir) if output_dir else RAW_DIR
        self.dry_run = dry_run
        self.headless = headless
        self.cookies = {}
        self.session = None
        self.stats = {
            "species_processed": 0,
            "specimens_found": 0,
            "images_downloaded": 0,
            "images_skipped": 0,
            "images_failed": 0,
        }

    async def setup_browser_and_cookies(self):
        """Start browser, pass Cloudflare, and extract cookies."""
        print("Starting browser to pass Cloudflare...")

        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=self.headless)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
        )
        page = await context.new_page()

        # Navigate to AntWeb to trigger Cloudflare
        await page.goto(f"{BASE_URL}/images.do?genus=Formica&species=rufa")

        # Wait for Cloudflare to pass
        print("Waiting for Cloudflare challenge...")
        for _ in range(30):
            title = await page.title()
            if "Just a moment" not in title:
                break
            await asyncio.sleep(1)
        else:
            print("ERROR: Cloudflare challenge timeout. Try running with --no-headless")
            await browser.close()
            await playwright.stop()
            return None

        print("Cloudflare passed! Extracting cookies...")

        # Extract cookies
        cookies = await context.cookies()
        self.cookies = {c["name"]: c["value"] for c in cookies}

        await browser.close()
        await playwright.stop()

        return page

    def setup_session(self):
        """Create requests session with cookies."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": BASE_URL,
        })
        for name, value in self.cookies.items():
            self.session.cookies.set(name, value)

    async def get_specimen_codes_browser(self, genus, species):
        """Use browser to get specimen codes (needs to pass Cloudflare per species page)."""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=self.headless)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
        )
        # Restore cookies
        cookie_list = [{"name": k, "value": v, "domain": ".antweb.org", "path": "/"}
                      for k, v in self.cookies.items()]
        await context.add_cookies(cookie_list)

        page = await context.new_page()

        url = f"{BASE_URL}/images.do?genus={genus}&species={species}"
        print(f"  Fetching specimen list: {genus} {species}")

        await page.goto(url)

        # Wait for Cloudflare if needed
        for _ in range(15):
            title = await page.title()
            if "Just a moment" not in title:
                break
            await asyncio.sleep(1)

        # Extract specimen codes
        specimens = await page.evaluate("""
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

        # Update cookies in case they changed
        new_cookies = await context.cookies()
        self.cookies.update({c["name"]: c["value"] for c in new_cookies})
        self.setup_session()  # Refresh session with new cookies

        await browser.close()
        await playwright.stop()

        return specimens

    def generate_image_urls(self, specimen_codes):
        """Generate all possible image URLs for specimens."""
        urls = []
        for specimen in specimen_codes:
            for view in VIEWS:
                for shot in [1, 2]:  # Most specimens have shot 1, some have shot 2
                    url = f"{STATIC_URL}/images/{specimen}/{specimen}_{view}_{shot}_{IMAGE_SIZE}.jpg"
                    urls.append({
                        "url": url,
                        "specimen": specimen,
                        "view": view,
                        "shot": shot,
                    })
        return urls

    def download_image(self, url_info, output_dir):
        """Download a single image using requests."""
        url = url_info["url"]
        specimen = url_info["specimen"]
        view = url_info["view"]
        shot = url_info["shot"]

        filename = f"{specimen}_{view}_{shot}.jpg"
        filepath = output_dir / specimen / filename

        if filepath.exists():
            return {"status": "skipped", "file": filename}

        if self.dry_run:
            return {"status": "dry_run", "file": filename}

        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)

            if response.status_code == 404:
                return {"status": "not_found", "file": filename}

            if response.status_code != 200:
                return {"status": "error", "file": filename, "code": response.status_code}

            # Verify it's an image
            content_type = response.headers.get("content-type", "")
            if "image" not in content_type:
                return {"status": "not_image", "file": filename}

            # Save image
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(response.content)

            return {"status": "downloaded", "file": filename, "size": len(response.content)}

        except Exception as e:
            return {"status": "error", "file": filename, "error": str(e)}

    def batch_download(self, url_infos, output_dir, species_info=None):
        """Download images in parallel."""
        results = {"downloaded": 0, "skipped": 0, "failed": 0, "not_found": 0}

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(self.download_image, url_info, output_dir): url_info
                for url_info in url_infos
            }

            for future in as_completed(futures):
                result = future.result()
                status = result["status"]

                if status == "downloaded":
                    results["downloaded"] += 1
                    size_kb = result.get("size", 0) // 1024
                    print(f"    ✓ {result['file']} ({size_kb}KB)")
                elif status == "skipped":
                    results["skipped"] += 1
                elif status == "dry_run":
                    print(f"    [DRY RUN] {result['file']}")
                elif status == "not_found":
                    results["not_found"] += 1
                else:
                    results["failed"] += 1
                    print(f"    ✗ {result['file']}: {result.get('error', result.get('code', 'unknown'))}")

        return results

    async def scrape_species(self, genus, species, subfamily=None):
        """Scrape all images for a species."""
        print(f"\n{'='*60}")
        print(f"Species: {genus} {species}")
        print(f"{'='*60}")

        # Get specimen codes using browser
        specimens = await self.get_specimen_codes_browser(genus, species)
        print(f"  Found {len(specimens)} specimens")
        self.stats["specimens_found"] += len(specimens)

        if not specimens:
            print("  No specimens found!")
            return

        # Generate image URLs
        url_infos = self.generate_image_urls(specimens)
        print(f"  Generated {len(url_infos)} image URLs to check")

        # Set up output directory
        species_key = f"{genus}_{species}"
        if subfamily:
            species_dir = self.output_dir / subfamily / species_key
        else:
            species_dir = self.output_dir / species_key

        # Batch download
        results = self.batch_download(url_infos, species_dir, {"genus": genus, "species": species})

        self.stats["images_downloaded"] += results["downloaded"]
        self.stats["images_skipped"] += results["skipped"]
        self.stats["images_failed"] += results["failed"]
        self.stats["species_processed"] += 1

        # Save metadata for each specimen
        if not self.dry_run:
            for specimen in specimens:
                specimen_dir = species_dir / specimen
                if specimen_dir.exists():
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

        print(f"\n  Summary: {results['downloaded']} downloaded, {results['skipped']} skipped, "
              f"{results['not_found']} not found, {results['failed']} failed")

    async def scrape_from_target_file(self, target_file=None):
        """Scrape all species from target file."""
        target_file = Path(target_file) if target_file else TARGET_SPECIES_FILE

        if not target_file.exists():
            print(f"ERROR: Target species file not found: {target_file}")
            return

        with open(target_file) as f:
            targets = json.load(f)

        total_species = targets["totals"]["species"]
        total_subfamilies = targets["totals"]["subfamilies"]

        print(f"{'='*60}")
        print(f"AntWeb Batch Scraper")
        print(f"{'='*60}")
        print(f"Target: {total_species} species from {total_subfamilies} subfamilies")
        print(f"Output: {self.output_dir}")
        print(f"Mode: {'Dry run' if self.dry_run else 'Download'}")
        print(f"{'='*60}")

        # Initial Cloudflare pass
        await self.setup_browser_and_cookies()
        self.setup_session()

        for subfamily_name, subfamily_data in targets["subfamilies"].items():
            print(f"\n{'#'*60}")
            print(f"# Subfamily: {subfamily_name}")
            print(f"{'#'*60}")

            for species_info in subfamily_data["species"]:
                genus = species_info["genus"]
                species = species_info["species"]
                await self.scrape_species(genus, species, subfamily=subfamily_name)

        # Final stats
        print(f"\n{'='*60}")
        print("SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"Species processed: {self.stats['species_processed']}")
        print(f"Specimens found: {self.stats['specimens_found']}")
        print(f"Images downloaded: {self.stats['images_downloaded']}")
        print(f"Images skipped: {self.stats['images_skipped']}")
        print(f"Images failed: {self.stats['images_failed']}")


async def main():
    parser = argparse.ArgumentParser(description="Batch scrape ant images from AntWeb")
    parser.add_argument("--species", help="Single species (format: 'Genus species')")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview without downloading")
    parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    parser.add_argument("--target-file", help="Custom target species JSON file")

    args = parser.parse_args()

    scraper = AntWebBatchScraper(
        output_dir=args.output,
        dry_run=args.dry_run,
        headless=not args.no_headless,
    )

    if args.species:
        parts = args.species.split()
        if len(parts) >= 2:
            await scraper.setup_browser_and_cookies()
            scraper.setup_session()
            await scraper.scrape_species(parts[0], parts[1])
        else:
            print("ERROR: Species must be in format 'Genus species'")
            sys.exit(1)
    else:
        await scraper.scrape_from_target_file(args.target_file)


if __name__ == "__main__":
    asyncio.run(main())
