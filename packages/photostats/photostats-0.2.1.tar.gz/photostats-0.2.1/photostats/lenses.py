"""Create a graphs relating to lens usage on a directory of photos."""

from collections import Counter
import matplotlib.pyplot as plt  # type: ignore

from photostats import get_exif


def get_lens_make_model(exif_list: list) -> dict:
    """Obtain lens make and model for each photo passed in.

    :param exif_list: A list of photo files.
    :returns: A Counter dictionary, counting the makes/models of lenses.
    """
    lens_list = []
    for data in exif_list:
        if data.get("Exif.Photo.LensModel") is None:
            pass
        else:
            lens_list.append((data.get("Exif.Photo.LensModel")))
    return Counter(lens_list)


def get_focal_length(exif_list: list) -> dict:
    """Obtain focal length for each photo passed in.

        :param exif_list: A list of photo files.
        :returns: A Counter dictionary, counting the focal length of lenses.
        """
    focal_length_list = []
    for data in exif_list:
        pre_fixed_string = f"{data.get('Exif.Photo.FocalLength')}"
        fixed_string = f"{pre_fixed_string[:pre_fixed_string.find('/')]}"
        if int(fixed_string) > 1000:
            pass
        else:
            fixed_string = fixed_string + " mm"
            focal_length_list.append(fixed_string)
    return Counter(focal_length_list)


def main(directory):
    photos = get_exif.get_photos(directory)
    exif = get_exif.get_exif(photos)
    lens_count = get_lens_make_model(exif)
    print("Lens Model Count:")
    for lens, count in lens_count.items():
        print(f'{lens} : {count}')
    plt.bar(lens_count.keys(), lens_count.values())
    plt.show()
    print("\nFocal Length Count:")
    focal_length_count = get_focal_length(exif)
    for focal_length, count in focal_length_count.items():
        print(f'{focal_length} : {count}')
    plt.bar(focal_length_count.keys(), focal_length_count.values())
    plt.show()


if __name__ == '__main__':
    test_directory = "/media/Photos/My Photos 2005 and on/2020/"
    main(test_directory)
