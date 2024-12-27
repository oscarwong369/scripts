import os
import subprocess
import json

# Prompt for the common file path prefix
PREFIX = input("Enter the common file path prefix: ").strip("'\"")

VIDEO_DIR = os.path.join(PREFIX, "video")
EXPORT_DIR = os.path.join(PREFIX, "export")

# Create the export directory if it doesn't exist
os.makedirs(EXPORT_DIR, exist_ok=True)

# Define the file extensions
EXTENSIONS = ["MOV", "MP4"]

# Initialize counters
processed_count = 0
failed_count = 0
mismatch_count = 0

# Define the EXIF fields to check
EXIF_FIELDS = ["CreateDate", "ModifyDate", "MediaCreateDate", "MediaModifyDate"]

# Function to extract EXIF metadata
def extract_exif(file_path):
    try:
        result = subprocess.run(
            ["exiftool", "-json", file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            metadata = json.loads(result.stdout)
            return metadata[0]  # Return the metadata dictionary
        else:
            print(f"Error extracting EXIF for {file_path}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception while extracting EXIF: {e}")
        return None

# Loop through each extension and process the files
for ext in EXTENSIONS:
    files_found = False
    for file in os.listdir(VIDEO_DIR):
        if file.lower().endswith(f".{ext.lower()}"):
            files_found = True
            file_path = os.path.join(VIDEO_DIR, file)
            output_file = os.path.join(EXPORT_DIR, f"{os.path.splitext(file)[0]}.mov")

            # Run exiftool to copy metadata
            result = subprocess.run([
                "exiftool", "-ee", "-tagsFromFile", file_path, "-all:all", "-overwrite_original", output_file
            ], capture_output=True)

            if result.returncode == 0:
                print(f"Successfully processed {file_path} to {output_file}")
                processed_count += 1

                # Cross-check metadata
                source_metadata = extract_exif(file_path)
                target_metadata = extract_exif(output_file)

                if source_metadata and target_metadata:
                    mismatches = [
                        field for field in EXIF_FIELDS
                        if source_metadata.get(field) != target_metadata.get(field)
                    ]
                    if mismatches:
                        print(f"Metadata mismatch for {file}: {mismatches}")
                        mismatch_count += 1
                else:
                    print(f"Failed to extract EXIF for source or target of {file}")
                    mismatch_count += 1

            else:
                print(f"Failed to process {file_path}")
                failed_count += 1

    if not files_found:
        print(f"No {ext} files found in {VIDEO_DIR}")

# Print summary
print(f"Total files processed: {processed_count}")
print(f"Total files failed: {failed_count}")
print(f"Total files with metadata mismatches: {mismatch_count}")