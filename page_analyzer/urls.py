from urllib.parse import urlparse
from validators import url as url_validator

MAX_URL_LENGTH = 255


def validate(url):
    errors = []
    if not url_validator(url):
        errors.append('Некорректный URL')
    if len(url) > MAX_URL_LENGTH:
        errors.append('URL превышает 255 символов')
    elif not url:
        errors.append('URL обязателен')
    return errors


def normalize(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
