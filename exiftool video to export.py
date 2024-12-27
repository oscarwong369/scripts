import os
import subprocess

# Prompt for the common file path prefix
PREFIX = input("Enter the common file path prefix: ")

VIDEO_DIR = os.path.join(PREFIX, "video")
EXPORT_DIR = os.path.join(PREFIX, "export")

# Create the export directory if it doesn't exist
os.makedirs(EXPORT_DIR, exist_ok=True)

# Define the file extensions
EXTENSIONS = ["MOV", "MP4"]

# Initialize counters
processed_count = 0
failed_count = 0

# Loop through each extension and run exiftool if the source file exists
for ext in EXTENSIONS:
    files_found = False
    for file in os.listdir(VIDEO_DIR):
        if file.lower().endswith(f".{ext.lower()}"):
            files_found = True
            file_path = os.path.join(VIDEO_DIR, file)
            output_file = os.path.join(EXPORT_DIR, f"{os.path.splitext(file)[0]}.mp4")
            result = subprocess.run([
                "exiftool", "-ee", "-tagsFromFile", file_path, "-all:all", "-overwrite_original", output_file
            ], capture_output=True)
            if result.returncode == 0:
                print(f"Successfully processed {file_path} to {output_file}")
                processed_count += 1
            else:
                print(f"Failed to process {file_path}")
                failed_count += 1
    if not files_found:
        print(f"No {ext} files found in {VIDEO_DIR}")

# Print summary
print(f"Total files processed: {processed_count}")
print(f"Total files failed: {failed_count}")