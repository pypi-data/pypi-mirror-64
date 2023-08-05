"""Create a graphs relating to lens usage on a directory of photos."""

from collections import Counter

from photostats import get_exif
from photostats.utils import create_plot


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

        :param exif_list: A list of photo exif metadata.
        :returns: A Counter dictionary, counting the focal length of lenses.
        """
    focal_length_list = []
    for data in exif_list:
        pre_fixed_string = f"{data.get('Exif.Photo.FocalLength')}"
        fixed_string = f"{pre_fixed_string[:pre_fixed_string.find('/')]}"
        try:
            if int(fixed_string) > 1000:
                pass
            else:
                focal_length_list.append(fixed_string)
        except ValueError:
            pass
    return Counter(sorted(focal_length_list, key=int))


def main(exif, graph_path):
    lens_count = get_lens_make_model(exif)
    print("Lens Model Count:")
    for lens, count in lens_count.items():
        print(f'{lens} : {count}')
    create_plot.create_plot(lens_count.keys(), lens_count.values(), x_label="Lens Model", y_label="Number of Photos",
                            title="Number of Photos Taken by Each Lens", graph_path=graph_path,
                            graph_filename="lens_models")
    print("\nFocal Length Count:")
    focal_length_count = get_focal_length(exif)
    for focal_length, count in focal_length_count.items():
        print(f'{focal_length} mm : {count}')
    create_plot.create_plot(focal_length_count.keys(), focal_length_count.values(), x_label="Focal Length (mm)",
                            y_label="Number of Photos", title="Number of Photos Taken at Each Focal Length",
                            graph_path=graph_path, graph_filename="lens_focal_length")


if __name__ == '__main__':  # pragma: no cover
    test_directory = "/media/Photos/My Photos 2005 and on/2020/"
    test_graph_path = "/home/ermesa/tmp/photostats"
    test_photos = get_exif.get_photos(test_directory)
    test_exif = get_exif.get_exif(test_photos)
    main(test_exif, test_graph_path)
