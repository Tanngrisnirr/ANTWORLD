#!/bin/bash
# Convert TensorFlow SavedModel to TensorFlow.js format
#
# Option 1: Using Docker (recommended for compatibility)
# Option 2: Using pip tensorflowjs (if numpy compatibility is fixed)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SAVED_MODEL="$SCRIPT_DIR/../models/saved_model/ant_classifier"
OUTPUT_DIR="$PROJECT_DIR/antworld.org/alpha/js/ml/ant_model"

echo "Converting model to TensorFlow.js format..."
echo "Source: $SAVED_MODEL"
echo "Output: $OUTPUT_DIR"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Option 1: Docker approach (works regardless of local Python version)
if command -v docker &> /dev/null; then
    echo ""
    echo "Using Docker for conversion..."
    docker run --rm \
        -v "$SAVED_MODEL:/model" \
        -v "$OUTPUT_DIR:/output" \
        tensorflow/tensorflow:latest-py3 \
        bash -c "pip install tensorflowjs && tensorflowjs_converter --input_format=tf_saved_model /model /output"

    if [ $? -eq 0 ]; then
        echo "Conversion successful!"
        echo "Model files are in: $OUTPUT_DIR"
        ls -la "$OUTPUT_DIR"
        exit 0
    fi
fi

# Option 2: Try local tensorflowjs_converter
if command -v tensorflowjs_converter &> /dev/null; then
    echo ""
    echo "Using local tensorflowjs_converter..."
    tensorflowjs_converter \
        --input_format=tf_saved_model \
        "$SAVED_MODEL" \
        "$OUTPUT_DIR"

    if [ $? -eq 0 ]; then
        echo "Conversion successful!"
        exit 0
    fi
fi

# Option 3: Manual instructions
echo ""
echo "=============================================="
echo "Automatic conversion failed. Manual options:"
echo "=============================================="
echo ""
echo "Option A: Use the online converter"
echo "  1. Zip the saved_model folder"
echo "  2. Go to: https://www.tensorflow.org/js/guide/conversion"
echo "  3. Upload and download the converted model"
echo ""
echo "Option B: Use Docker manually"
echo "  docker run -it --rm \\"
echo "    -v $SAVED_MODEL:/model \\"
echo "    -v $OUTPUT_DIR:/output \\"
echo "    python:3.10 bash"
echo "  # Then inside container:"
echo "  pip install tensorflowjs"
echo "  tensorflowjs_converter --input_format=tf_saved_model /model /output"
echo ""
echo "Option C: Use Podman (if Docker unavailable)"
echo "  podman run -it --rm \\"
echo "    -v $SAVED_MODEL:/model:Z \\"
echo "    -v $OUTPUT_DIR:/output:Z \\"
echo "    python:3.10 bash"
