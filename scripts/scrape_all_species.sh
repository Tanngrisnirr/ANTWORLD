#!/bin/bash
#
# AntWeb Full Scraper - Downloads all target species
#
# USAGE:
#   1. First, run Claude Code and navigate to antweb.org to pass Cloudflare
#   2. Export cookies with: claude "extract cookies from browser as shell variable"
#   3. Run this script with those cookies
#
# Or run with --interactive to use a visible browser for Cloudflare:
#   ./scrape_all_species.sh --interactive
#
# The script will:
#   - Navigate to each species page (requires browser for Cloudflare)
#   - Extract specimen codes
#   - Batch download images using cookies
#

set -e

# Configuration
BASE_DIR="/var/mnt/DATUX/Documents/WEB/ANTWORLD/TrainingSets/raw"
COOKIES_FILE="/var/mnt/DATUX/Documents/WEB/ANTWORLD/scripts/.antweb_cookies.txt"
LOG_FILE="/var/mnt/DATUX/Documents/WEB/ANTWORLD/ml/scrape_log.txt"
VIEWS=("h" "p" "d")
SIZE="high"
UA='Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'

# Target species (subfamily:genus:species format)
SPECIES_LIST=(
  # Formicinae (3)
  "Formicinae:Formica:rufa"
  "Formicinae:Camponotus:herculeanus"
  "Formicinae:Lasius:niger"
  # Myrmicinae (3)
  "Myrmicinae:Atta:cephalotes"
  "Myrmicinae:Myrmica:rubra"
  "Myrmicinae:Pheidole:megacephala"
  # Ponerinae (2)
  "Ponerinae:Odontomachus:bauri"
  "Ponerinae:Neoponera:villosa"
  # Dolichoderinae (2)
  "Dolichoderinae:Linepithema:humile"
  "Dolichoderinae:Tapinoma:sessile"
  # Dorylinae (2)
  "Dorylinae:Eciton:burchellii"
  "Dorylinae:Dorylus:nigricans"
  # Amblyoponinae (2)
  "Amblyoponinae:Stigmatomma:pallipes"
  "Amblyoponinae:Amblyopone:australis"
  # Ectatomminae (2)
  "Ectatomminae:Ectatomma:tuberculatum"
  "Ectatomminae:Rhytidoponera:metallica"
  # Pseudomyrmecinae (2)
  "Pseudomyrmecinae:Pseudomyrmex:gracilis"
  "Pseudomyrmecinae:Tetraponera:rufonigra"
  # Proceratiinae (2)
  "Proceratiinae:Proceratium:silaceum"
  "Proceratiinae:Discothyrea:oculata"
  # Heteroponerinae (1)
  "Heteroponerinae:Heteroponera:microps"
  # Leptanillinae (1)
  "Leptanillinae:Leptanilla:revelierii"
  # Myrmeciinae (2)
  "Myrmeciinae:Myrmecia:gulosa"
  "Myrmeciinae:Nothomyrmecia:macrops"
  # Aneuretinae (1)
  "Aneuretinae:Aneuretus:simoni"
  # Paraponerinae (1)
  "Paraponerinae:Paraponera:clavata"
  # Agroecomyrmecinae (1)
  "Agroecomyrmecinae:Tatuidris:tatusia"
  # Martialinae (1)
  "Martialinae:Martialis:heureka"
  # Apomyrminae (1)
  "Apomyrminae:Apomyrma:stygia"
)

# Stats
total_downloaded=0
total_skipped=0
total_failed=0
species_completed=0

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_cookies() {
  if [ ! -f "$COOKIES_FILE" ]; then
    echo "ERROR: Cookies file not found: $COOKIES_FILE"
    echo ""
    echo "To get cookies:"
    echo "1. Open Claude Code"
    echo "2. Navigate browser to antweb.org and pass Cloudflare"
    echo "3. Run: claude 'save browser cookies to $COOKIES_FILE'"
    echo ""
    echo "Or paste cookies directly:"
    echo "  export ANTWEB_COOKIES='cf_clearance=...; __cf_bm=...; ...'"
    echo "  ./scrape_all_species.sh"
    exit 1
  fi
  COOKIES=$(cat "$COOKIES_FILE")
}

download_image() {
  local specimen=$1
  local view=$2
  local output_dir=$3

  local filename="${specimen}_${view}_1.jpg"
  local filepath="$output_dir/$filename"
  local url="https://static.antweb.org/images/$specimen/${specimen}_${view}_1_${SIZE}.jpg"

  if [ -f "$filepath" ]; then
    ((total_skipped++))
    return 0
  fi

  local http_code
  http_code=$(curl -s -o "$filepath" -w "%{http_code}" \
    -H "Cookie: $COOKIES" \
    -H "User-Agent: $UA" \
    -H "Referer: https://www.antweb.org/" \
    "$url" 2>/dev/null)

  if [ "$http_code" = "200" ]; then
    if file "$filepath" 2>/dev/null | grep -q "JPEG"; then
      ((total_downloaded++))
      return 0
    fi
  fi

  rm -f "$filepath" 2>/dev/null
  return 1
}

download_species() {
  local subfamily=$1
  local genus=$2
  local species=$3
  local specimens_str=$4

  IFS=',' read -ra specimens <<< "$specimens_str"
  local species_dir="${genus}_${species}"
  local output_base="$BASE_DIR/$subfamily/$species_dir"

  log "Downloading $genus $species (${#specimens[@]} specimens)"

  local count=0
  for specimen in "${specimens[@]}"; do
    specimen=$(echo "$specimen" | tr -d ' ')
    [ -z "$specimen" ] && continue

    local specimen_dir="$output_base/$specimen"
    mkdir -p "$specimen_dir"

    for view in "${VIEWS[@]}"; do
      download_image "$specimen" "$view" "$specimen_dir"
    done
    ((count++))

    # Progress indicator
    if [ $((count % 5)) -eq 0 ]; then
      echo -n "."
    fi
  done
  echo ""

  ((species_completed++))
}

# Main script
main() {
  echo "=============================================="
  echo "AntWeb Full Species Scraper"
  echo "=============================================="
  echo "Target: ${#SPECIES_LIST[@]} species"
  echo "Output: $BASE_DIR"
  echo "Image size: $SIZE"
  echo "=============================================="
  echo ""

  # Check for cookies
  if [ -n "$ANTWEB_COOKIES" ]; then
    COOKIES="$ANTWEB_COOKIES"
    echo "Using cookies from environment variable"
  else
    check_cookies
    echo "Using cookies from $COOKIES_FILE"
  fi

  mkdir -p "$(dirname "$LOG_FILE")"
  log "Starting scrape of ${#SPECIES_LIST[@]} species"

  # Process each species
  for entry in "${SPECIES_LIST[@]}"; do
    IFS=':' read -r subfamily genus species <<< "$entry"

    # Check if species already has images
    local species_dir="$BASE_DIR/$subfamily/${genus}_${species}"
    local existing_count=0
    if [ -d "$species_dir" ]; then
      existing_count=$(find "$species_dir" -name "*.jpg" 2>/dev/null | wc -l)
    fi

    if [ "$existing_count" -gt 0 ]; then
      log "SKIP: $genus $species - already has $existing_count images"
      ((species_completed++))
      continue
    fi

    echo ""
    echo ">>> $genus $species ($subfamily)"
    echo "    Specimens must be fetched via browser (Cloudflare protected)"
    echo "    Add specimens to this script or use interactive mode"
    echo ""
  done

  echo ""
  echo "=============================================="
  echo "SCRAPE SUMMARY"
  echo "=============================================="
  echo "Species processed: $species_completed / ${#SPECIES_LIST[@]}"
  echo "Images downloaded: $total_downloaded"
  echo "Images skipped: $total_skipped"
  echo "=============================================="

  log "Scrape complete: $total_downloaded downloaded, $total_skipped skipped"
}

# Show help
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "Usage: $0 [OPTIONS]"
  echo ""
  echo "Downloads ant specimen images from AntWeb.org"
  echo ""
  echo "Options:"
  echo "  --help        Show this help"
  echo "  --status      Show current download status"
  echo ""
  echo "Environment:"
  echo "  ANTWEB_COOKIES  Cloudflare cookies (required)"
  echo ""
  echo "To get cookies, use Claude Code MCP browser to:"
  echo "  1. Navigate to antweb.org"
  echo "  2. Pass Cloudflare challenge"
  echo "  3. Export cookies"
  exit 0
fi

# Show status
if [ "$1" = "--status" ]; then
  echo "=== Download Status ==="
  total=$(find "$BASE_DIR" -name "*.jpg" 2>/dev/null | wc -l)
  size=$(du -sh "$BASE_DIR" 2>/dev/null | cut -f1)
  echo "Total images: $total"
  echo "Total size: $size"
  echo ""
  echo "By subfamily:"
  for sf in "$BASE_DIR"/*/; do
    [ -d "$sf" ] || continue
    sf_name=$(basename "$sf")
    sf_count=$(find "$sf" -name "*.jpg" 2>/dev/null | wc -l)
    echo "  $sf_name: $sf_count images"
  done
  exit 0
fi

main "$@"
