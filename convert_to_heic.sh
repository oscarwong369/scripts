#!/bin/bash

# Check if the target path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <target-path>"
    exit 1
fi

# Get the target path
TARGET_PATH="$1"

# Ensure the target path exists
if [ ! -d "$TARGET_PATH" ]; then
    echo "Error: The specified path does not exist or is not a directory."
    exit 1
fi

# Create the output directory ../heic/ relative to the target path
OUTPUT_PATH="${TARGET_PATH%/}/../heic"
mkdir -p "$OUTPUT_PATH"

# Convert all images in the target path
for file in "$TARGET_PATH"/*; do
    if [[ -f "$file" ]]; then
        # Get the filename without the extension
        FILENAME=$(basename "$file")
        FILENAME_NO_EXT="${FILENAME%.*}"
        
        # Convert to HEIC
        sips -s format heic "$file" --out "$OUTPUT_PATH/${FILENAME_NO_EXT}.heic"
        echo "Converted: $file -> $OUTPUT_PATH/${FILENAME_NO_EXT}.heic"
    fi
done

echo "All images converted to HEIC and stored in: $OUTPUT_PATH"