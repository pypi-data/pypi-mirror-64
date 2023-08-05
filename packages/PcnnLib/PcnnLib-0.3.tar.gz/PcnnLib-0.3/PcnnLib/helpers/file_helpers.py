import os


def get_filename(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]


def find_file(dir_path, filename):
    for file in os.listdir(dir_path):
        if get_filename(file) == filename:
            return os.path.join(dir_path, file)
    return None
