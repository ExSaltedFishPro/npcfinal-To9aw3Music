# removing .DS_Store files recursively
import os
import fnmatch
import sys

def remove_ds_store_files(directory):
    """
    Recursively remove all .DS_Store files from the given directory.
    """
    for root, dirs, files in os.walk(directory):
        for file in fnmatch.filter(files, '.DS_Store'):
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

if __name__ == "__main__":
    # Check if the directory is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python remove_ds_store.py <directory>")
        sys.exit(1)

    # Get the directory from the command line argument
    directory = sys.argv[1]

    # Remove .DS_Store files from the specified directory
    remove_ds_store_files(directory)