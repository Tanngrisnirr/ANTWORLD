#!/bin/bash
# promote-to-delta.sh
# Archives current delta and promotes beta to delta (production)
# Usage: ./scripts/promote-to-delta.sh

set -e

BASE_DIR="/var/mnt/DATUX/Documents/WEB/ANTWORLD/antworld.org"
BACKUP_BASE="/var/mnt/DATUX/Documents/WEB/ANTWORLD"
BETA_DIR="$BASE_DIR/beta"
DELTA_DIR="$BASE_DIR/delta"
BACKUP_DIR="$BACKUP_BASE/backups"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="delta_$TIMESTAMP"

echo "=== Promote Beta to Delta ==="
echo "This will:"
echo "  1. Archive current delta to backups/$BACKUP_NAME/"
echo "  2. Replace delta with contents of beta"
echo ""

# Check if beta exists and has content
if [ ! -d "$BETA_DIR" ] || [ -z "$(ls -A $BETA_DIR 2>/dev/null)" ]; then
    echo "ERROR: Beta directory is empty or does not exist!"
    echo "Run minify-to-beta.sh first."
    exit 1
fi

# Confirm action
read -p "Are you sure you want to promote beta to delta? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Create backup directory if needed
mkdir -p "$BACKUP_DIR"

# Archive current delta
echo "Archiving current delta to $BACKUP_DIR/$BACKUP_NAME..."
if [ -d "$DELTA_DIR" ] && [ -n "$(ls -A $DELTA_DIR 2>/dev/null)" ]; then
    cp -r "$DELTA_DIR" "$BACKUP_DIR/$BACKUP_NAME"
    echo "Backup created: $BACKUP_DIR/$BACKUP_NAME"
else
    echo "Warning: Delta was empty, nothing to backup."
fi

# Clear delta
echo "Clearing delta directory..."
rm -rf "$DELTA_DIR"/*

# Copy beta to delta
echo "Copying beta to delta..."
cp -r "$BETA_DIR"/* "$DELTA_DIR"/

echo ""
echo "=== Done! ==="
echo "Delta is now updated with the contents of beta."
echo "Backup of old delta: $BACKUP_DIR/$BACKUP_NAME"
echo ""
echo "Next step: Upload delta/ to your production server."
