#!/bin/bash
# sync-alpha-from-delta.sh
# Resets alpha to match current delta (production)
# Use this when you want to start development from the current production state
# Usage: ./scripts/sync-alpha-from-delta.sh

set -e

BASE_DIR="/var/mnt/DATUX/Documents/WEB/ANTWORLD/antworld.org"
ALPHA_DIR="$BASE_DIR/alpha"
DELTA_DIR="$BASE_DIR/delta"

echo "=== Sync Alpha from Delta ==="
echo "This will REPLACE all contents of alpha with delta."
echo "Any uncommitted changes in alpha will be LOST."
echo ""

# Confirm action
read -p "Are you sure? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Check if delta exists
if [ ! -d "$DELTA_DIR" ] || [ -z "$(ls -A $DELTA_DIR 2>/dev/null)" ]; then
    echo "ERROR: Delta directory is empty or does not exist!"
    exit 1
fi

# Clear alpha
echo "Clearing alpha directory..."
rm -rf "$ALPHA_DIR"/*

# Copy delta to alpha
echo "Copying delta to alpha..."
cp -r "$DELTA_DIR"/* "$ALPHA_DIR"/

echo ""
echo "=== Done! ==="
echo "Alpha is now synced with delta."
echo "You can now begin development in alpha/."
