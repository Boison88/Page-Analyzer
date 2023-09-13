import requests

from page_analyzer.page_parser import get_page_data
from urllib.parse import urlparse
from validators import url as url_validator
from flask import flash

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


def get_page(url):
    response = requests.get(url)
    decode_content = response.content.decode()
    status_code = response.status_code
    try:
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        new_check = {'status_code': status_code}
        new_check.update(get_page_data(decode_content))
        return new_check
