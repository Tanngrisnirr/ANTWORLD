#!/usr/bin/env python3
"""
ANTWORLD Dashboard Sync Script
Monitors project files and updates dashboard history.

Usage:
    python3 sync_dashboard.py [--once]

Options:
    --once    Run once and exit (don't watch)
    --interval N  Check every N seconds (default: 30)
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = SCRIPT_DIR.parent
ANTWORLD_ORG = PROJECT_DIR / "antworld.org"
ALPHA_DIR = ANTWORLD_ORG / "alpha"
HISTORY_FILE = ALPHA_DIR / "php" / "dashboard_history.json"

# File state tracking
last_states = {}


def get_file_state(filepath):
    """Get file modification time and size."""
    try:
        stat = os.stat(filepath)
        return (stat.st_mtime, stat.st_size)
    except:
        return None


def get_dir_size_kb(directory):
    """Calculate directory size in KB."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip backup directories
        dirnames[:] = [d for d in dirnames if d not in ['backup_svg', '.git', 'node_modules']]
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total += os.path.getsize(filepath)
            except:
                pass
    return total // 1024


def count_files_by_ext(directory, extensions):
    """Count files by extension."""
    counts = {ext: 0 for ext in extensions}
    counts['other'] = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        dirnames[:] = [d for d in dirnames if d not in ['backup_svg', '.git', 'node_modules']]
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower().lstrip('.')
            if ext in counts:
                counts[ext] += 1
            else:
                counts['other'] += 1
    return counts


def count_image_assets(directory):
    """Count image files by type."""
    counts = {'jpg': 0, 'png': 0, 'svg': 0, 'webp': 0, 'gif': 0}

    for dirpath, dirnames, filenames in os.walk(directory):
        dirnames[:] = [d for d in dirnames if d not in ['backup_svg', '.git']]
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower().lstrip('.')
            if ext == 'jpeg':
                ext = 'jpg'
            if ext in counts:
                counts[ext] += 1
    return counts


def count_content(alpha_dir):
    """Count content items."""
    content = {
        "Species Pages": 0,
        "ID Pages": 0,
        "Morpho SVGs": 0,
        "Photo Assets": 0,
        "Icon Assets": 0
    }

    # ID pages
    id_dir = alpha_dir / "id"
    if id_dir.exists():
        content["ID Pages"] = len(list(id_dir.glob("*.html")))

    # Morpho SVGs
    morpho_svg_dir = alpha_dir / "img" / "morpho" / "svg"
    if morpho_svg_dir.exists():
        for svg in morpho_svg_dir.rglob("*.svg"):
            if 'backup_svg' not in str(svg):
                content["Morpho SVGs"] += 1

    # Photo assets
    photo_dir = alpha_dir / "img" / "photo"
    if photo_dir.exists():
        content["Photo Assets"] = sum(1 for _ in photo_dir.rglob("*") if _.is_file())

    # Icon assets
    icon_dir = alpha_dir / "icon"
    if icon_dir.exists():
        content["Icon Assets"] = sum(1 for _ in icon_dir.rglob("*") if _.is_file())

    # Species count from list_species.html
    species_file = alpha_dir / "list_species.html"
    if species_file.exists():
        try:
            with open(species_file, 'r') as f:
                html = f.read()
            # Count table rows (rough estimate)
            content["Species Pages"] = html.count('<tr') - 1  # Subtract header
            if content["Species Pages"] < 0:
                content["Species Pages"] = 0
        except:
            pass

    return content


def get_recent_commits(limit=10):
    """Get recent git commits."""
    commits = []
    try:
        result = subprocess.run(
            ['git', 'log', f'-n{limit}', '--format=%h|%ad|%s', '--date=short'],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|', 2)
                    if len(parts) == 3:
                        commits.append({
                            'hash': parts[0],
                            'date': parts[1],
                            'message': parts[2]
                        })
    except:
        pass
    return commits


def load_history():
    """Load project history from JSON file."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'projectHistory': []}


def save_history(data):
    """Save project history to JSON file."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def update_history():
    """Add or update today's entry in project history."""
    today = datetime.now().strftime("%Y-%m-%d")
    size_kb = get_dir_size_kb(ALPHA_DIR)

    data = load_history()
    history = data.get('projectHistory', [])

    # Check if today's entry exists
    today_entry = None
    for i, entry in enumerate(history):
        if entry.get('date') == today:
            today_entry = i
            break

    if today_entry is not None:
        # Update existing entry
        old_size = history[today_entry].get('size_kb', 0)
        diff = size_kb - old_size
        notes = history[today_entry].get('notes', 'Auto-updated')
        if diff != 0 and 'Auto' not in notes:
            notes = f"{notes} ({'+' if diff > 0 else ''}{diff} KB)"
        history[today_entry]['size_kb'] = size_kb
        print(f"Updated {today}: {size_kb} KB")
    else:
        # Add new entry
        history.append({
            'date': today,
            'size_kb': size_kb,
            'notes': 'Auto-updated'
        })
        print(f"Added {today}: {size_kb} KB")

    # Keep last 90 days
    history = history[-90:]

    data['projectHistory'] = history

    # Also update git commits (container can't access git directly)
    data['recentCommits'] = get_recent_commits()

    save_history(data)
    return data


def collect_all_data():
    """Collect all dashboard data."""
    data = {
        'lastUpdate': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'projectSize': {
            'alpha_kb': get_dir_size_kb(ALPHA_DIR),
            'beta_kb': get_dir_size_kb(ANTWORLD_ORG / 'beta'),
            'delta_kb': get_dir_size_kb(ANTWORLD_ORG / 'delta'),
            'total_kb': get_dir_size_kb(ANTWORLD_ORG)
        },
        'fileTypes': count_files_by_ext(ALPHA_DIR, ['html', 'css', 'js', 'php', 'svg', 'json', 'txt']),
        'content': count_content(ALPHA_DIR),
        'imageAssets': count_image_assets(ALPHA_DIR),
        'projectHistory': load_history().get('projectHistory', []),
        'recentCommits': get_recent_commits()
    }
    return data


def check_and_sync():
    """Check for file changes and update history."""
    global last_states

    # Monitor key directories
    dirs_to_watch = [
        ALPHA_DIR / 'id',
        ALPHA_DIR / 'img',
        ALPHA_DIR / 'css',
        ALPHA_DIR / 'js',
        ALPHA_DIR / 'php'
    ]

    changed = False
    for watch_dir in dirs_to_watch:
        if not watch_dir.exists():
            continue
        for filepath in watch_dir.rglob('*'):
            if filepath.is_file() and 'backup_svg' not in str(filepath):
                state = get_file_state(filepath)
                if state and state != last_states.get(str(filepath)):
                    changed = True
                    last_states[str(filepath)] = state

    if changed:
        update_history()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Changes detected, history updated")

    return changed


def print_status():
    """Print current project status."""
    data = collect_all_data()

    print("\n" + "=" * 50)
    print("ANTWORLD Dashboard Status")
    print("=" * 50)
    print(f"Alpha size: {data['projectSize']['alpha_kb']} KB")
    print(f"Beta size:  {data['projectSize']['beta_kb']} KB")
    print(f"Delta size: {data['projectSize']['delta_kb']} KB")
    print("-" * 50)
    print("File types:")
    for ext, count in data['fileTypes'].items():
        if count > 0:
            print(f"  {ext.upper():6} : {count}")
    print("-" * 50)
    print("Content:")
    for item, count in data['content'].items():
        print(f"  {item:15} : {count}")
    print("-" * 50)
    print(f"History entries: {len(data['projectHistory'])}")
    print(f"Recent commits:  {len(data['recentCommits'])}")
    print("=" * 50 + "\n")


def main():
    once = '--once' in sys.argv
    interval = 30

    # Parse interval argument
    for i, arg in enumerate(sys.argv):
        if arg == '--interval' and i + 1 < len(sys.argv):
            try:
                interval = int(sys.argv[i + 1])
            except:
                pass

    print("=" * 50)
    print("ANTWORLD Dashboard Sync Script")
    print("=" * 50)
    print(f"Project dir: {PROJECT_DIR}")
    print(f"Alpha dir:   {ALPHA_DIR}")
    print(f"History:     {HISTORY_FILE}")
    print(f"Interval:    {interval}s")
    print("=" * 50)

    # Initial sync
    update_history()
    print_status()

    if once:
        print("Done (--once mode)")
        return

    print(f"Watching for changes every {interval}s... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(interval)
            check_and_sync()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
