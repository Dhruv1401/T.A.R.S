import os

def list_files(directory="."):
    return os.listdir(directory)

def create_file(filename):
    with open(filename, "w") as f:
        f.write("")

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
