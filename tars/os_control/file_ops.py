import os

def list_files(path="."):
    """Return list of files in directory."""
    return os.listdir(path)

def create_file(path):
    """Create an empty file."""
    open(path, "w").close()

def delete_file(path):
    """Delete a file if it exists."""
    if os.path.exists(path):
        os.remove(path)
