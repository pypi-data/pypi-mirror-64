"""Get EXIF data from a directory of photos"""

from pyexiv2 import Image  # type: ignore
import os
import re


def scan_tree(directory: str):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            yield from scan_tree(entry.path)  # see below for Python 2.x
        else:
            yield entry


def get_photos(this_directory: str) -> list:
    """Get photos from a directory.

    :param this_directory: a directory containing photos
    :returns: A list containing photo files with complete path
    """
    directory_files: list = scan_tree(this_directory)
    regex = re.compile('CR2$|jpg$')  # needs to be generalized for all possible photo extensions
    photos: list = []
    for file in directory_files:
        if regex.search(file.name) and file.is_file():
            photos.append(file.path)
    return photos


def get_exif(photo_list: list) -> list:
    """Obtain exif data for each photo from the list.

    :param photo_list: A list of photos from a directory
    :returns: A list of exif dictionaries from photos
    """
    exif_list = []
    for image in photo_list:
        this_image = Image(image)
        try:
            this_image_exif = this_image.read_exif()
        except UnicodeDecodeError:
            print(f"Could not get exif data for {image}")
        exif_list.append(this_image_exif)
    return exif_list
