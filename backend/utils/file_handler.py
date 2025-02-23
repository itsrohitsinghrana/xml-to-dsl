import os

def save_file(file, folder):
    """
    Saves uploaded file to the given folder.
    """
    file_path = os.path.join(folder, file.filename)
    file.save(file_path)
    return file_path

