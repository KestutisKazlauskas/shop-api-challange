import requests


def does_image_exists(url: str) -> bool:
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(url)
    if r.headers["content-type"] in image_formats:
        return True
    return False
