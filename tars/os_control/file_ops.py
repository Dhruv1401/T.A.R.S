import os

def list_files(dir="."):
    return os.listdir(dir)

def create_file(name):
    open(name, "w").close()

def delete_file(name):
    if os.path.exists(name):
        os.remove(name)
