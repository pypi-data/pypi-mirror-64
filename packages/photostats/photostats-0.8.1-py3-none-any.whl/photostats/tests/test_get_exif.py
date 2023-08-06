"""Test get_exif.py"""

import pytest

from photostats import get_exif

file_paths = ['photostats/tests/test_images/Canon/Canon EOS Rebel T1i.jpg',
              'photostats/tests/test_images/Canon/Canon EOS Rebel T6s.CR2',
              'photostats/tests/test_images/Canon/Canon EOS Rebel XT.dng',
              'photostats/tests/test_images/Canon/Canon EOS Rebel XTi.dng',
              'photostats/tests/test_images/Canon/Canon PowerShot A720 IS.jpg',
              'photostats/tests/test_images/Canon/Canon PowerShot S100.dng',
              'photostats/tests/test_images/Canon/Canon PowerShot SD980 IS.jpg',
              'photostats/tests/test_images/Fujifilm/Fujifilm FinePix2650.JPG',
              'photostats/tests/test_images/Fujifilm/Fujifilm FinePix A345.JPG',
              'photostats/tests/test_images/Fujifilm/Fujifilm Finepix S7000.JPG',
              'photostats/tests/test_images/Apple/Apple iPhone 4S.JPG',
              'photostats/tests/test_images/Motorola/Motorola Droid2.jpg',
              'photostats/tests/test_images/Motorola/Motorola XT1060.jpg',
              'photostats/tests/test_images/LG/LGE Nexus 5X.jpg',
              'photostats/tests/test_images/LG/LG LG-VN250.jpg',
              'photostats/tests/test_images/LG/LG LG-VN271.jpg',
              'photostats/tests/test_images/Google/Google Pixel.jpg',
              'photostats/tests/test_images/Kodak/Kodak DX3600.JPG',
              'photostats/tests/test_images/HTC/HTC ADR6350.jpg',
              'photostats/tests/test_images/Nikon/Nikon D7200.jpg',
              'photostats/tests/test_images/Olympus/Olympus C4100Z.jpg',
              'photostats/tests/test_images/Sony/Sony Cybershot.JPG',
              'photostats/tests/test_images/VTech/VTech Kidizoom camera.JPG']

test_directory = "photostats/tests/test_images"


def test_scan_test():
    scan_tree = get_exif.scan_tree(test_directory)
    photos = []
    for file in scan_tree:
        photos.append(file.path)
    assert photos.sort() == file_paths.sort()


def test_get_photos():
    photo_list = get_exif.get_photos(test_directory)
    assert photo_list.sort() == file_paths.sort()


def test_get_exif():
    exif = get_exif.get_exif(file_paths)
    assert exif[-1] == {'Exif.Image.ExifTag': '88', 'Exif.Image.Make': 'VTech', 'Exif.Image.Model': 'Kidizoom camera',
                        'Exif.Photo.DateTimeOriginal': '2018:12:26 19:18:50'}
