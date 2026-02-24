#!/bin/bash
# Rotate SVG backups - keep only the 5 most recent per SVG file
# Usage: ./rotate-svg-backups.sh [archive_dir]

ARCHIVE_DIR="${1:-antworld.org/alpha/img/morpho/svg/archives}"
MAX_BACKUPS=5

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "Archive directory not found: $ARCHIVE_DIR"
    exit 1
fi

# Get unique base names (without timestamp)
for base in $(ls "$ARCHIVE_DIR"/*.svg 2>/dev/null | sed 's/_[0-9]\{8\}_[0-9]\{6\}\.svg$//' | sort -u); do
    base_name=$(basename "$base")
    
    # Count backups for this file
    count=$(ls "$ARCHIVE_DIR/${base_name}_"*.svg 2>/dev/null | wc -l)
    
    if [ "$count" -gt "$MAX_BACKUPS" ]; then
        # Get files to delete (oldest first, skip the newest 5)
        to_delete=$((count - MAX_BACKUPS))
        echo "Rotating $base_name: removing $to_delete old backup(s)"
        
        ls "$ARCHIVE_DIR/${base_name}_"*.svg | sort | head -n "$to_delete" | while read f; do
            echo "  Deleting: $(basename "$f")"
            rm "$f"
        done
    fi
done

echo "Done. Current backups:"
ls -la "$ARCHIVE_DIR"/*.svg 2>/dev/null | wc -l
