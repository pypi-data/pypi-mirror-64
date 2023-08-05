"""Obtain camera information for statistics and graphing."""

from collections import Counter
from typing import Tuple

from photostats import get_exif
from photostats.utils import create_plot


def get_camera_make_model(exif_list: list) -> Tuple[Counter, Counter, Counter]:
    """Obtain camera make and model for each photo passed in.

    Depending on how complex your photo collection is, there may be no difference in the three values returned.\
    But if you have more than one camera from the same company, then these numbers may diverge.

    :param exif_list: A list of photo exif metadata.
    :returns: For maximum flexibility, returns a tuple of lists - one of make, one of model, and one of make/model.
    """
    make_list = []
    model_list = []
    make_model_list = []
    for data in exif_list:
        make_list.append(data.get('Exif.Image.Make'))
        model_list.append(data.get('Exif.Image.Model'))
        make_model_list.append(f"{data.get('Exif.Image.Make')} {data.get('Exif.Image.Model')}")
    return Counter(make_list), Counter(model_list), Counter(make_model_list)


def main(exif, graph_path):
    make_count, model_count, make_model_count = get_camera_make_model(exif)
    print("\nMake count:")
    for make, count in make_count.items():
        print(f'{make} : {count}')
    create_plot.create_plot(make_count.keys(), make_count.values(), x_label="Make/Company", y_label="Number of Photos",
                            title="Number of Photos Taken with a camera per company", graph_path=graph_path,
                            graph_filename="camera_make")
    print("\nModel Count:")
    for model, count in model_count.items():
        print(f'{model} : {count}')
    create_plot.create_plot(model_count.keys(), model_count.values(), x_label="Camera Model",
                            y_label="Number of Photos", title="Number of Photos Taken with a camera model per company",
                            graph_path=graph_path, graph_filename="camera_model")
    print("\nMake-Model Count:")
    for make_model, count in make_model_count.items():
        print(f'{make_model} : {count}')
    create_plot.create_plot(make_model_count.keys(), make_model_count.values(), x_label="Camera Make/Model",
                            y_label="Number of Photos",
                            title="Number of Photos Taken with a camera Make/Model per company",
                            graph_path=graph_path, graph_filename="camera_make_model")


if __name__ == '__main__':  # pragma: no cover
    test_directory = "/media/Photos/My Photos 2005 and on/2020/"
    test_graph_path = "/home/ermesa/tmp/photostats"
    test_photos = get_exif.get_photos(test_directory)
    test_exif = get_exif.get_exif(test_photos)
    main(test_exif, test_graph_path)
