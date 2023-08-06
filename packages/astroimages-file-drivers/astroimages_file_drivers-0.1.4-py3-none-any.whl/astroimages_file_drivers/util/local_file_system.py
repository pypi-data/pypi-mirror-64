import os


# List all files in a directory using os.listdir
def list_files_in_folder(path, extension):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if extension in file:
                files.append(os.path.join(r, file))
    return files
