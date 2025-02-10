import os
from src.WikiHandler import (
    create_url_full_path,
    get_local_image_path,
    download_picture
)


def test_create_url_full_path():
    # Checking if the function creates a full URL
    relative_path = "wiki/List_of_animal_names"
    full_url = create_url_full_path(relative_path)
    assert full_url == "https://en.wikipedia.org/wiki/List_of_animal_names", "Full URL is incorrect"


def test_invalid_image():
    # test if the program save just valid picture
    url = "https://upload.wikimedia.org/wikipedia/commons/invalid.jpg"
    animal_name = "invalid_pict"
    img_path = get_local_image_path(animal_name)

    download_picture(url, animal_name)

    assert not os.path.exists(img_path), "Invalid image should not be saved"
