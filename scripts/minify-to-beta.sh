#!/bin/bash
# minify-to-beta.sh
# Copies alpha/ to beta/ with minification and comment removal
# Usage: ./scripts/minify-to-beta.sh

set -e

BASE_DIR="/var/mnt/DATUX/Documents/WEB/ANTWORLD/antworld.org"
ALPHA_DIR="$BASE_DIR/alpha"
BETA_DIR="$BASE_DIR/beta"

echo "=== Minify Alpha to Beta ==="
echo "Source: $ALPHA_DIR"
echo "Target: $BETA_DIR"
echo ""

# Check if alpha exists
if [ ! -d "$ALPHA_DIR" ]; then
    echo "ERROR: Alpha directory does not exist!"
    exit 1
fi

# Clear beta directory (keep the directory itself)
echo "Clearing beta directory..."
rm -rf "$BETA_DIR"/*

# Copy all files from alpha to beta
echo "Copying files from alpha to beta..."
cp -r "$ALPHA_DIR"/* "$BETA_DIR"/

# Remove HTML comments from HTML files
echo "Removing HTML comments from .html files..."
find "$BETA_DIR" -name "*.html" -type f | while read file; do
    # Remove HTML comments (<!-- ... -->)
    sed -i 's/<!--.*-->//g' "$file"
    # Remove multi-line comments (basic approach)
    sed -i '/<!--/,/-->/d' "$file"
done

# Remove CSS comments from CSS files
echo "Removing CSS comments from .css files..."
find "$BETA_DIR" -name "*.css" -type f | while read file; do
    # Remove /* ... */ comments
    sed -i 's/\/\*.*\*\///g' "$file"
done

# Remove JS single-line comments (be careful with URLs containing //)
echo "Removing JS comments from .js files (single-line only)..."
find "$BETA_DIR" -name "*.js" -type f | while read file; do
    # Remove // comments at start of line or after whitespace (not in URLs)
    sed -i 's/^\s*\/\/.*$//g' "$file"
done

# Remove PHP comments from PHP files
echo "Removing PHP comments from .php files..."
find "$BETA_DIR" -name "*.php" -type f | while read file; do
    # Remove // and # comments
    sed -i 's/^\s*\/\/.*$//g' "$file"
    sed -i 's/^\s*#.*$//g' "$file"
done

# Remove empty lines (optional - uncomment if desired)
# echo "Removing empty lines..."
# find "$BETA_DIR" -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.php" | while read file; do
#     sed -i '/^\s*$/d' "$file"
# done

echo ""
echo "=== Done! ==="
echo "Beta directory is ready for testing on remote subdomain."
echo "Next step: Upload beta/ to your test server."
